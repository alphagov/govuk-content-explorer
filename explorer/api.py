from flask import Flask, render_template, request
from .search import perform_search
import urllib

app = Flask(__name__)


class Scope(object):
    def __init__(self, args):
        self.q = args.get("q", "")
        self.filters = {}
        for (name, values) in args.iterlists():
            if name.startswith("filter_"):
                self.filters.setdefault(name[7:], []).extend(values)

    def form_args(self):
        result = {
            "q": self.q,
            "filters": self.filters
        }
        return result

    def search_args(self):
        result = {
            "q": self.q,
            "count": 100,
            "facet_specialist_sectors": "1000",
            "facet_mainstream_browse_pages": "1000",
            "facet_organisations": "1000",
            "facet_format": "1000",
            "facet_manual": "1000",
            "fields": "title,link,slug,display_type,format,description,specialist_sectors,mainstream_browse_pages,organisations,format,manual",
        }
        for field, values in self.filters.items():
            result["filter_" + field] = values
        return result

    def base_link_params(self):
        params = {
            "q": self.q,
        }
        for f, values in self.filters.items():
            params["filter_" + f] = list(values)
        return params

    def filter_link(self, field, value, remove=False):
        params = self.base_link_params()
        if remove:
            params["filter_" + field] = [
                v
                for v in params["filter_" + field]
                if v != value
            ]
        else:
            params.setdefault("filter_" + field, []).append(value)
        return "/?" + urllib.urlencode(params, doseq=True)

    def compare_link(self, field_a, field_b):
        params = self.base_link_params()
        params["compare"] = "%s,%s" % (field_a, field_b)
        return "/?" + urllib.urlencode(params, doseq=True)

    def document_link(self, document):
        link = document.link
        if link.startswith("http"):
            return link
        if not link.startswith("/"):
            link = "/" + link
        return "https://www.gov.uk" + link

    def search(self):
        args = self.search_args()
        return perform_search(**args)

    def compare(self, field_a, field_b):
        args = {
            "q": self.q,
            "count": 0,
        }
        for field, values in self.filters.items():
            args["filter_" + field] = values
        args["facet_" + field_a] = "1000,example_scope:global,examples:1000,example_fields:%s" % (
            field_b,
        )
        return perform_search(**args)


class Document(object):
    def __init__(self, fields):
        self.fields = fields

    def strfield(self, fieldname):
        val = self.fields.get(fieldname, None)
        if val is None:
            return None
        elif isinstance(val, basestring):
            return val
        else:
            return val[0]

    def tuplefield(self, fieldname):
        val = self.fields.get(fieldname, ())
        if val is None:
            return ()
        if isinstance(val, basestring):
            return (val,)
        else:
            return tuple(val)

    @staticmethod
    def to_tuple(value):
        if value is None:
            return None
        if isinstance(value, basestring):
            return (value,)
        return tuple(value)

    @property
    def format(self):
        """The format field often has duplicated entries.

        We don't want to display these, so just remove duplicates.  The order
        isn't significant, so we then sort to make it consistent.

        """
        return tuple(sorted(set(self.tuplefield("format"))))

    def __getattr__(self, fieldname):
        if fieldname in (
            "title",
            "link",
            "slug",
            "document_type",
            "index",
            "display_type",
            "description",
        ):
            return self.strfield(fieldname)
        return self.tuplefield(fieldname)


def title_or_slug(item):
    if isinstance(item, basestring):
        return item

    title = item.get("title", None)
    if isinstance(title, basestring):
        return title
    return item.get("slug", "")


@app.route("/")
def main(**params):
    scope = Scope(request.args)
    context = scope.form_args()

    compare = request.args.get("compare", "")
    if compare:
        field_a, field_b = compare.split(",", 2)
        return compare_page(scope, context, field_a, field_b)
    else:
        return main_page(scope, context)

def main_page(scope, context):
    results = scope.search()
    context["result_count"] = results["total"]
    context["results"] = {
        "count": results["total"],
        "documents": [Document(result)
            for result in results["results"]
        ],
        "facets": results["facets"],
    }
    context["filter_link"] = scope.filter_link
    context["compare_link"] = scope.compare_link
    context["document_link"] = scope.document_link
    context["title_or_slug"] = title_or_slug
    return render_template("index.html", **context)

def compare_page(scope, context, field_a, field_b):
    context["field_a"] = field_a
    context["field_b"] = field_b
    context["filter_link"] = scope.filter_link

    results = scope.compare(field_a, field_b)

    return render_template("compare.html", **context)

import collections
import urllib

from .search import perform_search


class Scope(object):
    """Define the scope of documents being considered

    """

    FACET_FIELDS = (
        "specialist_sectors",
        "mainstream_browse_pages",
        "organisations",
        "format",
    )

    DISPLAY_FIELDS = (
        "title",
        "link",
        "slug",
        "display_type",
        "description",
        "specialist_sectors",
        "mainstream_browse_pages",
        "organisations",
        "format",
    )

    def __init__(self, args):
        self.q = args.get("q", "")
        self.filters = self._parse_filters(args)

    def _parse_filters(self, args):
        result = {}
        for (name, values) in args.iterlists():
            if name.startswith("filter_"):
                field = name[7:]
                result.setdefault(field, []).extend(values)
        return result

    def form_args(self):
        result = {
            "q": self.q,
            "filters": self.filters
        }
        return result

    def search_args(self):
        result = {
            "q": self.q,
            "count": 1000,
            "facet_specialist_sectors": "1000",
            "facet_mainstream_browse_pages": "1000",
            "facet_organisations": "1000",
            "facet_format": "1000",
            "fields": ",".join(self.DISPLAY_FIELDS),
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
            if field != field_a:
                args["filter_" + field] = values
        args["facet_" + field_a] = "1000000,example_scope:query,examples:1000000,example_fields:%s" % (
            field_b,
        )
        search_results = perform_search(**args)
        result = []
        for option in search_results["facets"][field_a]["options"]:
            value = option["value"]
            counts = collections.Counter()
            no_value_count = 0
            for example in value["example_info"]["examples"]:
                if example is None:
                    no_value_count += 1
                else:
                    for field_b_value in example[field_b]:
                        counts[field_b_value] += 1

            title = value.get("title", value.get("slug", value.get("link")))
            result.append(dict(
                title=title,
                documents=option["documents"],
                no_value_count=no_value_count,
                counts=sorted(counts.items(), key=lambda x: x[1], reverse=True)
            ))
        return result

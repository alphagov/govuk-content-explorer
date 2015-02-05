from flask import Flask, render_template, request

from .document import Document
from .scope import Scope

app = Flask(__name__)


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
    field_overlap = scope.compare(field_a, field_b)

    context["field_a"] = field_a
    context["field_b"] = field_b
    context["filter_link"] = scope.filter_link
    context["field_overlap"] = field_overlap

    return render_template("compare.html", **context)

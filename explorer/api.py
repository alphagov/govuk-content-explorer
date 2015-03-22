from flask import Flask, render_template, request

from .document import Document
from .scope import Scope
from .search import fetch_documents

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
    scope = Scope(request)
    context = dict(scope=scope)

    compare = request.args.get("compare", "")
    if compare:
        field_a, field_b = compare.split(",", 2)
        return compare_page(scope, context, field_a, field_b)
    else:
        return main_page(scope, context)

def main_page(scope, context):
    context["results"] = fetch_documents(scope)
    context["title_or_slug"] = title_or_slug
    return render_template("index.html", **context)

def compare_page(scope, context, field_a, field_b):
    field_overlap = scope.compare(field_a, field_b)

    context["field_a"] = field_a
    context["field_b"] = field_b
    context["field_overlap"] = field_overlap

    return render_template("compare.html", **context)

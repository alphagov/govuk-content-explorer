import csv
from flask import Flask, render_template, request, Response
from StringIO import StringIO

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

    format = request.args.get("format", "")
    compare = request.args.get("compare", "")
    if compare:
        field_a, field_b = compare.split(",", 2)
        return compare_page(scope, context, field_a, field_b, format)
    else:
        return main_page(scope, context)

def main_page(scope, context):
    context["results"] = fetch_documents(scope)
    context["title_or_slug"] = title_or_slug
    return render_template("index.html", **context)

def compare_page(scope, context, field_a, field_b, format):
    field_overlap = scope.compare(field_a, field_b)

    context["field_a"] = field_a
    context["field_b"] = field_b
    context["field_overlap"] = field_overlap

    if format == "csv":
        return render_compare_csv(context)
    return render_template("compare.html", **context)

def render_compare_csv(context):
    output = StringIO()
    writer = csv.writer(output)
    for row in context["field_overlap"]:
        items = [u"%s %d" % (item[0], item[1]) for item in row["counts"]]
        writer.writerow([row["title"], row["documents"], row["no_value_count"]] + items)
    return Response(output.getvalue(), mimetype='text/csv')

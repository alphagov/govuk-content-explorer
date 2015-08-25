from . import config
from .document import Document
import requests
from time import time


def perform_search(**params):
    response = requests.get(
        config.GOVUK_SEARCH_API,
        params=params,
        auth=config.AUTH,
    )
    return response.json()


def fetch_documents(scope):
    documents = perform_search(**fetch_document_args(scope))
    facets = {}
    for field in Document.FACET_FIELDS:
        start = time()
        facet_results = perform_search(**fetch_facet_args(scope, field))
        facets[field] = facet_results["facets"][field]
        print "Fetched %s facet in %fs" % (field, time() - start)
    return present_documents(documents, facets)


def fetch_lots_of_documents(scope, max_documents):
    fetched = 0
    search_args = fetch_document_args(scope)
    while fetched < max_documents:
        search_args["start"] = fetched
        documents = perform_search(**search_args).get("results", [])
        if len(documents) == 0:
            break
        for document in documents:
            yield Document(document)
            fetched += 1


def fetch_document_args(scope):
    args = scope.search_args()
    args["count"] = 1000
    args["fields"] = ",".join(Document.DISPLAY_FIELDS)
    return args


def fetch_facet_args(scope, facet_field):
    args = scope.search_args()
    args["count"] = 0
    args["facet_" + facet_field] = "1000,scope:all_filters"
    return args


def present_documents(documents, facets):
    return {
        "count": documents["total"],
        "documents": [Document(document)
            for document in documents["results"]
        ],
        "facets": facets,
    }

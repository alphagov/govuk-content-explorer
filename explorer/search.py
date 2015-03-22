from . import config
from .document import Document
import requests


def perform_search(**params):
    response = requests.get(
        config.GOVUK_SEARCH_API,
        params=params,
        auth=config.AUTH,
    )
    return response.json()


def fetch_documents(scope):
    args = fetch_document_args(scope)
    results = perform_search(**args)
    return present_documents(results)


def fetch_document_args(scope):
    args = scope.search_args()
    args["count"] = 1000
    args["fields"] = ",".join(Document.DISPLAY_FIELDS)
    for field in Document.FACET_FIELDS:
        args["facet_" + field] = "1000,scope:all_filters"
    return args


def present_documents(results):
    return {
        "count": results["total"],
        "documents": [Document(result)
            for result in results["results"]
        ],
        "facets": results["facets"],
    }

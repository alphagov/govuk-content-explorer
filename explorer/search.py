import requests

GOVUK_SEARCH_API="http://www.dev.gov.uk/api/search.json"
#GOVUK_SEARCH_API="https://www.gov.uk/api/search.json"

def perform_search(**params):
    r = requests.get(GOVUK_SEARCH_API, params=params).json()
    return r

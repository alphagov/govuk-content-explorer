from . import config
import requests

def perform_search(**params):
    r = requests.get(config.GOVUK_SEARCH_API, params=params).json()
    return r

from . import config
import requests


def perform_search(**params):
    response = requests.get(
        config.GOVUK_SEARCH_API,
        params=params,
        auth=config.AUTH,
        verify=False,
    )
    return response.json()

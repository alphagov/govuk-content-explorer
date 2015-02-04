import os

env = os.environ.get("ENV", "live")
if env == "live":
    GOVUK_SEARCH_API = "https://www.gov.uk/api/search.json"
else:
    GOVUK_SEARCH_API = "http://www.dev.gov.uk/api/search.json"

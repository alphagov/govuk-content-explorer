import os


env = os.environ.get("ENV", "live")
if env == "live":
    GOVUK_SEARCH_API = "https://www.gov.uk/api/search.json"
elif env == "dev":
    GOVUK_SEARCH_API = "http://www.dev.gov.uk/api/search.json"
else:
    raise RuntimeError("Unknown value for ENV environment variable: %r" % env)

gsi = os.environ.get("GOVUK_SEARCH_API")
if gsi:
    GOVUK_SEARCH_API = gsi

auth_password = os.environ.get("AUTH_PASSWORD")
auth_username = os.environ.get("AUTH_USERNAME")

if auth_password:
    AUTH = (auth_username, auth_password)
else:
    AUTH = None

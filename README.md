# GOVUK Content Explorer

This tool is intended to help explore the content on GOV.UK, allowing it to be
segmented by section, topic, organisation, format and other tags.  You can see
it in action at https://govuk-content-explorer.herokuapp.com/

It gathers its data from the GOV.UK search API, so it's view of what's on
GOV.UK is based on what is in the search index.  This is reasonably
comprehensive, but not 100% accurate.

## Live examples

- [govuk-content-explorer](http://govuk-content-explorer.herokuapp.com/)

## Technical documentation

This is a Python / Flask app. Deployed on Heroku.

### Setup

```
virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt
```

### Running the application

```
source ENV/bin/activate
./start.py
```

The app will run on [localhost:5000](http://localhost:5000)

To run the explorer in dev mode against a Rummager instance running on `dev.gov.uk`:

```
source ENV/bin/activate
ENV=dev ./start.py -d
```

## Licence

[MIT License](LICENCE)

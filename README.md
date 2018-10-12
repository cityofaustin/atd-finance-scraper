# finance-scraper
This repo houses Python utilities for scraping accounting codes from the Controller's Office Intranet for the purpose systems integration.

## Quick Start

Requires Python 3. We currently support fetching of objects, units, or master agreements from the Controller's Office Intranet website. If you know what these are, you've come to the right place.

1. Install transportation-data-utils and knackpy from PyPi:
```bash
$ pip install tdutils
```

2. Create `secrets.py` in the root folder:

```python
KNACK_CREDENTIALS = {
    "my_destination_app_name" : {
        "app_id" : "knack-assigned-app-id",
        "api_key" : "secretest-key-ever"
    }
}
```

3. Update `config.py` with your Knack scene, view, and reference objects (see [knackpy](http://github.com/cityofaustin/knackpy) docs).

4. Pass a resource name and app name to the scripts:

```bash
$ python finance_scraper.py master_agreements my_destination_app_name
```

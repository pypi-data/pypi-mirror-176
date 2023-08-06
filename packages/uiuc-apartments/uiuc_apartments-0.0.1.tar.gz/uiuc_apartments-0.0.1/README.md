# UIUC Apartment Kit

A wrapper around a webscraper for popular rental agencies on UIUC campus

Installation:
```
pip install uiuc_apartments
```

Usage:
```py
from uiuc_apartments import AllAgencies

for agency in AllAgencies:
    print(agency.get_all())
```
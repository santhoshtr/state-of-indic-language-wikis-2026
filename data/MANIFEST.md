# Data manifest

Each entry: what the file is, which script makes it, when it was last fetched.

## wikis.csv

* What: one row per Indic language wiki. Language metadata, project,
  domain, closed flag, and four founding-date signals:
  - `first_revision`: timestamp of the earliest revision.
    Imported revisions can make this earlier than the wiki creation.
  - `first_edit_month`: first month with any edit, from Wikistats.
    Also polluted by imports (Wikistats keeps original timestamps).
  - `first_active_month`: first month with 10+ edits, from Wikistats.
  - `inception_wikidata`: inception date (P571) from the wiki's
    Wikidata item, found via P1800 (Wikimedia database name).
    Missing for many wikis.
  - `launch_date`: launch date from the List of Wikipedias article
    on English Wikipedia. Wikipedia rows only. This is the canonical
    founding date for cohort analysis (decision 2026-08-27).
  - `review_dates`: set on rows without launch_date when the other
    signals disagree by more than a year. Decide these dates by hand
    before use.
* Script: `scripts/fetch_inventory.py`
* Sources: Wikimedia sitematrix API, per-wiki MediaWiki API,
  Wikistats REST API, Wikidata Query Service.
* Last fetched: 2026-08-27

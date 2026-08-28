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

## snapshot.csv

* What: current Special:Statistics numbers for every open wiki,
  one row per wiki, with the fetch date.
* Caution: `activeusers` = users with any activity in the last
  30 days. This is NOT the Wikistats "active editors" metric
  (registered non-bot users with 5+ edits in a month, in
  wikistats_monthly.csv). Do not mix the two on one slide.
* Script: `scripts/fetch_snapshot.py`
* Source: per-wiki siteinfo API (siprop=statistics).
* Last fetched: 2026-08-28

## wikistats_monthly.csv

* What: monthly time series per open wiki, full history since launch.
  Columns: edits (all / registered users / anonymous; bot edits =
  all - user - anon), registered non-bot editors in four activity
  buckets (1-4, 5-24, 25-99, 100+ edits per month; "active editors"
  = sum of the top three), new content pages, new registered users.
* Caution: cumulative new_pages approximates article growth but
  drifts from the true count (deletions, redirect churn).
  Verified 2026-08-28: median drift vs snapshot articles is 1%.
* Caution: the newest month in a series can be incomplete (data lag).
  Drop the last month when a chart shows a tail dip.
* Caution: summing editors across wikis counts a person once per
  wiki they are active on. Use sums for trend shape, not headcount.
* Script: `scripts/fetch_wikistats.py` (appends per wiki; resumes an
  interrupted run; delete the file for a full refresh)
* Source: Wikistats REST API (wikimedia.org/api/rest_v1/metrics).
* Last fetched: 2026-08-28

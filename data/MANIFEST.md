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

## pageviews_monthly.csv

* What: monthly pageviews per open wiki since 2015-07 (the API
  start), split by access method (desktop, mobile web, mobile app).
  Human traffic only (agent=user).
* Caution: bot detection improved in 2024-2025 and reclassified much
  traffic from "user" to automated. Pre-2024 "user" numbers are
  inflated by then-undetected bots. Present the post-2023 decline as
  partly measurement correction, partly real (AI answers, search
  changes). Do not present it as raw reader loss.
* Script: `scripts/fetch_pageviews.py` (appends per wiki; resumes)
* Source: Wikimedia Pageviews API.
* Last fetched: 2026-08-29

## top_articles.csv

* What: top 50 viewed pages per wiki, last full month, all access.
  Includes non-article pages (Main Page, Special:...).
* Note: mag.wikipedia (launched 2026-06) and mni.wiktionary have no
  top-pages data in the API yet.
* Script: `scripts/fetch_pageviews.py`
* Last fetched: 2026-08-29 (month 2026-07)

## cx_translations_monthly.csv, cx_language_pairs.csv, cx_deletions.csv, cx_translators.csv

* What: Content Translation statistics filtered to the languages in
  scope. Monthly published translations per target language;
  lifetime source-target pair counts (either side Indic); lifetime
  deleted translations per target; lifetime translators per target.
* Caution: language codes are wiki codes (bh = Bhojpuri). The pair
  and translator files hold lifetime totals, not time series.
* Script: `scripts/fetch_cx_stats.py`
* Source: public CX TSV datasets on analytics.wikimedia.org
  (the same files behind cxstats.toolforge.org).
* Last fetched: 2026-08-29

## pageviews_by_country.csv

* What: pageviews by reader country per wiki, last full month.
  Counts are privacy ceilings (views_ceil), not exact.
* Caution: countries on the WMF country protection list are absent.
  Bangladesh and Pakistan are absent: reader-country stories for
  Bengali and Urdu are structurally incomplete. Nepal and Sri Lanka
  are present.
* Caution: BR or MX appear in the top-5 for 31 of 32 Wikipedias.
  That is residual automated traffic passing the agent=user filter,
  not real readers. Home-country shares (IN, NP, LK) are the
  trustworthy part; diaspora shares are directional only.
* Script: `scripts/fetch_pageviews.py`
* Last fetched: 2026-08-29 (month 2026-07)

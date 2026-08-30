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
* Caution: language codes are wiki codes. The script maps CX ISO
  codes to wiki codes (bho -> bh). The pair and translator files
  hold lifetime totals, not time series.
* Caution: "share of articles from translation" divides lifetime
  published translations by current surviving articles; the ~7%
  deleted translations sit in the numerator, so true surviving
  shares are a few points lower.
* Script: `scripts/fetch_cx_stats.py`
* Source: public CX TSV datasets on analytics.wikimedia.org
  (the same files behind cxstats.toolforge.org).
* Last fetched: 2026-08-29

## topic_pageviews.csv, topic_edits.csv

* What: top 25 categories per Wikipedia by pageviews and by edits,
  for a recent 60-day window (the columns record the window), with
  each category's top article. Category titles are English labels.
* Caution: topictrends holds recent data only; no history.
  magwiki is not indexed. Some small-wiki English labels resolve
  to wrong languages; clean before charting.
* Script: `scripts/fetch_topictrends.py`
* Source: topictrends.wmcloud.org API.
* Last fetched: 2026-08-30 (window 2026-07-01..2026-08-29)

## gaps.csv

* What: knowledge gap discovery per Wikipedia. Top 50 categories
  where the target lacks articles the reference has, ranked by
  estimated missing readership (reference pageviews x gap share).
  References: enwiki for every wiki; all pairs among the eight
  largest communities; a family anchor for smaller wikis
  (editorial choice, see the script).
* Caution: the ranking weight uses the REFERENCE wiki's pageviews,
  so gaps vs English skew to high-traffic American topics. That
  skew is a finding, not an error; peer references avoid it.
* Caution: category_title is in the reference wiki's language for
  peer rows (Tamil titles for reference tawiki, and so on).
* Caution: one category label leaks in Bashkir
  (a person-by-alphabet category) in the enwiki-reference top-10 of
  most wikis. Filter it before charting.
* Script: `scripts/fetch_topictrends.py`
* Source: topictrends.wmcloud.org, coverage snapshot 2026-06-23.
* Last fetched: 2026-08-30

## wikidata_stats.csv

* What: per language, the count of Wikidata entities with a label
  in the language; the count of India-related items (P17=Q668)
  with a label (denominator repeated in india_items_total); and
  the lexeme count.
* Caution: labels_total counts all entity types and is inflated by
  mass bot imports on some languages (bn above 10M). The
  India-item coverage is the honest comparison metric.
* Caution: Hindi and Urdu lexemes are mostly filed under
  Hindustani (Q11051), which is counted in both rows. Wikidata
  splits some label languages by script; variants are summed.
* Caution: rows for languages without a wiki (doi, khw, lus, brx)
  are unverified; a label code QLever does not know counts 0
  silently.
* Script: `scripts/fetch_wikidata.py`
* Source: QLever Wikidata endpoint (qlever.dev) — a periodic
  snapshot, so numbers can trail live Wikidata by days. The WDQS
  60s limit cannot serve these counts.
* Last fetched: 2026-08-30

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

## deck_data.json

* What: the aggregates the presentation embeds, derived from the
  files above. One JSON with per-Wikipedia cards, yearly series,
  CX summaries, gap postcards, and Wikidata coverage.
* Script: `scripts/build_deck_data.py` (also injects the JSON into
  presentation.html between the DECK-DATA markers).
* Caution: the world lexeme top-10 is a static constant in the
  script, fetched from QLever on 2026-08-30.
* Last built: 2026-08-30

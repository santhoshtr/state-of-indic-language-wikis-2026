#!/usr/bin/env python3
"""Fetch monthly time series for every open Indic wiki from Wikistats.

Reads data/wikis.csv (closed wikis are skipped). For each wiki, gets
the full monthly history from the Wikistats REST API:

  - edits by all editors, by registered users, and by anonymous users
    (bot edits = all - user - anonymous)
  - editors (registered, non-bot) in four activity buckets:
    1-4, 5-24, 25-99, and 100+ edits per month
    (active editors, the standard 5+ definition = sum of top three)
  - new content pages
  - new registered users

Writes data/wikistats_monthly.csv, one row per wiki per month.

The script appends one wiki at a time and skips wikis already in the
output file, so an interrupted run continues where it stopped.
For a full refresh, delete data/wikistats_monthly.csv first.

Usage: uv run scripts/fetch_wikistats.py
"""

import csv
import sys
import time
from datetime import datetime, timezone

from wmapi import REPO, get, load_wikis

OUTPUT_FILE = REPO / "data" / "wikistats_monthly.csv"

AQS = "https://wikimedia.org/api/rest_v1/metrics"

COLUMNS = [
    "domain", "month",
    "edits_all", "edits_user", "edits_anon",
    "editors_1_4", "editors_5_24", "editors_25_99", "editors_100plus",
    "new_pages", "new_registered_users",
]

# (column, url template, value key in the response)
SERIES = [
    ("edits_all",
     AQS + "/edits/aggregate/{domain}/all-editor-types/all-page-types/monthly/{start}/{end}",
     "edits"),
    ("edits_user",
     AQS + "/edits/aggregate/{domain}/user/all-page-types/monthly/{start}/{end}",
     "edits"),
    ("edits_anon",
     AQS + "/edits/aggregate/{domain}/anonymous/all-page-types/monthly/{start}/{end}",
     "edits"),
    ("editors_1_4",
     AQS + "/editors/aggregate/{domain}/user/all-page-types/1..4-edits/monthly/{start}/{end}",
     "editors"),
    ("editors_5_24",
     AQS + "/editors/aggregate/{domain}/user/all-page-types/5..24-edits/monthly/{start}/{end}",
     "editors"),
    ("editors_25_99",
     AQS + "/editors/aggregate/{domain}/user/all-page-types/25..99-edits/monthly/{start}/{end}",
     "editors"),
    ("editors_100plus",
     AQS + "/editors/aggregate/{domain}/user/all-page-types/100..-edits/monthly/{start}/{end}",
     "editors"),
    ("new_pages",
     AQS + "/edited-pages/new/{domain}/all-editor-types/content/monthly/{start}/{end}",
     "new_pages"),
    ("new_registered_users",
     AQS + "/registered-users/new/{domain}/monthly/{start}/{end}",
     "new_registered_users"),
]


def fetch_series(domain, template, value_key, end):
    """Return {month: value} for one metric of one wiki."""
    url = template.format(domain=domain, start="2001010100", end=end)
    resp = get(url)
    if resp.status_code == 404:
        return {}  # no data for this wiki and metric
    resp.raise_for_status()
    result = {}
    for item in resp.json()["items"]:
        for row in item["results"]:
            result[row["timestamp"][:7]] = row[value_key]
    return result


def done_domains():
    if not OUTPUT_FILE.exists():
        return set()
    with open(OUTPUT_FILE) as f:
        return {row["domain"] for row in csv.DictReader(f)}


def main():
    wikis = load_wikis()
    end = datetime.now(timezone.utc).strftime("%Y%m%d00")
    skip = done_domains()
    if skip:
        print(f"Resuming: {len(skip)} wikis already in the output file")
    failures = 0

    write_header = not OUTPUT_FILE.exists()
    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        if write_header:
            writer.writeheader()

        for wiki in wikis:
            domain = wiki["domain"]
            if domain in skip:
                continue
            print(domain)
            months = {}
            try:
                for column, template, value_key in SERIES:
                    for month, value in fetch_series(
                        domain, template, value_key, end
                    ).items():
                        months.setdefault(month, {})[column] = value
                    time.sleep(0.5)
            except Exception as e:
                failures += 1
                print(f"  FAILED: {e}", file=sys.stderr)
                continue  # wiki left out entirely; a re-run picks it up

            for month in sorted(months):
                row = {"domain": domain, "month": month}
                row.update(months[month])
                writer.writerow(row)
            f.flush()

    print(f"\nDone. Output: {OUTPUT_FILE}")
    if failures:
        print(f"ERROR: {failures} wikis failed. Re-run to fetch them.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

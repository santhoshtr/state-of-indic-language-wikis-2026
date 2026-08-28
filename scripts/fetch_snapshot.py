#!/usr/bin/env python3
"""Fetch a current-stats snapshot of every open Indic wiki.

Reads data/wikis.csv (closed wikis are skipped). For each wiki, gets
the Special:Statistics numbers from the siteinfo API.

Writes data/snapshot.csv, one row per wiki, with a fetched date.

Caution: `activeusers` counts users with any activity in the last
30 days. It is not the same as the Wikistats "active editors"
metric (registered non-bot users with 5+ edits in a month).

Usage: uv run scripts/fetch_snapshot.py
"""

import csv
import sys
from datetime import date

from wmapi import REPO, get, load_wikis

OUTPUT_FILE = REPO / "data" / "snapshot.csv"

FIELDS = ["articles", "pages", "edits", "users", "activeusers", "admins", "images"]


def main():
    wikis = load_wikis()
    today = date.today().isoformat()
    failures = 0

    rows = []
    for wiki in wikis:
        domain = wiki["domain"]
        print(domain)
        try:
            resp = get(
                f"https://{domain}/w/api.php",
                params={
                    "action": "query",
                    "meta": "siteinfo",
                    "siprop": "statistics",
                    "format": "json",
                    "formatversion": "2",
                },
            )
            resp.raise_for_status()
            stats = resp.json()["query"]["statistics"]
        except Exception as e:
            failures += 1
            print(f"  FAILED: {e}", file=sys.stderr)
            continue
        row = {
            "lang": wiki["lang"],
            "project": wiki["project"],
            "domain": domain,
            "fetched": today,
        }
        for field in FIELDS:
            row[field] = stats.get(field, "")
        rows.append(row)

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["lang", "project", "domain", "fetched"] + FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} wikis to {OUTPUT_FILE}")
    if failures:
        print(f"ERROR: {failures} fetches failed. Data is incomplete. Re-run.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

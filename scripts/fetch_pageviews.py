#!/usr/bin/env python3
"""Fetch reader data for every open Indic wiki from the Pageviews API.

Reads data/wikis.csv (closed wikis are skipped). Fetches:

  1. Monthly pageviews per wiki since 2015-07 (the API start), split
     by access method: desktop, mobile-web, mobile-app.
     Human traffic only (agent=user).
     -> data/pageviews_monthly.csv (appends per wiki; an interrupted
        run continues where it stopped; delete for a full refresh)
  2. Top 50 viewed pages per wiki for the last full month.
     -> data/top_articles.csv (rewritten whole each run)
  3. Pageviews by reader country per wiki for the last full month.
     Counts are privacy-preserving ceilings (views_ceil).
     -> data/pageviews_by_country.csv (rewritten whole each run)

Usage: uv run scripts/fetch_pageviews.py
"""

import csv
import sys
import time
from datetime import datetime, timezone

from wmapi import REPO, get, load_wikis

MONTHLY_FILE = REPO / "data" / "pageviews_monthly.csv"
TOP_FILE = REPO / "data" / "top_articles.csv"
COUNTRY_FILE = REPO / "data" / "pageviews_by_country.csv"

AQS = "https://wikimedia.org/api/rest_v1/metrics/pageviews"
ACCESS_METHODS = ["desktop", "mobile-web", "mobile-app"]
TOP_LIMIT = 50


def last_full_month():
    now = datetime.now(timezone.utc)
    year, month = (now.year, now.month - 1) if now.month > 1 else (now.year - 1, 12)
    return year, month


def fetch_monthly(domain, access, end):
    url = (f"{AQS}/aggregate/{domain}/{access}/user/monthly/"
           f"2015070100/{end}")
    resp = get(url)
    if resp.status_code == 404:
        return {}
    resp.raise_for_status()
    return {
        row["timestamp"][:6]: row["views"]
        for row in resp.json()["items"]
    }


def fetch_top(domain, year, month):
    resp = get(f"{AQS}/top/{domain}/all-access/{year}/{month:02d}/all-days")
    if resp.status_code == 404:
        return []
    resp.raise_for_status()
    return resp.json()["items"][0]["articles"][:TOP_LIMIT]


def fetch_by_country(domain, year, month):
    resp = get(f"{AQS}/top-by-country/{domain}/all-access/{year}/{month:02d}")
    if resp.status_code == 404:
        return []
    resp.raise_for_status()
    return resp.json()["items"][0]["countries"]


def reset_if_stale(path, header, month_label):
    """Start the file over when it holds a different month.

    Returns the set of domains already fetched for month_label.
    A wiki with no data at all is refetched on every run: the API
    can return an empty result for a transient error, and retrying
    a few small wikis is cheaper than telling the cases apart.
    """
    done = set()
    if path.exists():
        with open(path) as f:
            rows = list(csv.DictReader(f))
        if rows and rows[0]["month"] == month_label:
            done = {r["domain"] for r in rows}
            return done
    with open(path, "w", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(header)
    return done


def write_tops(wikis, year, month):
    """Fetch the two last-full-month files, one wiki at a time."""
    month_label = f"{year}-{month:02d}"
    top_done = reset_if_stale(
        TOP_FILE, ["domain", "month", "rank", "page", "views"], month_label)
    country_done = reset_if_stale(
        COUNTRY_FILE, ["domain", "month", "rank", "country", "views_ceil"],
        month_label)
    with open(TOP_FILE, "a", newline="") as tf, \
         open(COUNTRY_FILE, "a", newline="") as cf:
        top_writer = csv.writer(tf, lineterminator="\n")
        country_writer = csv.writer(cf, lineterminator="\n")
        for wiki in wikis:
            domain = wiki["domain"]
            if domain in top_done and domain in country_done:
                continue
            print(f"top pages and countries: {domain}")
            if domain not in top_done:
                articles = fetch_top(domain, year, month)
                if not articles:
                    print(f"  no top pages for {domain}", file=sys.stderr)
                for a in articles:
                    top_writer.writerow(
                        [domain, month_label, a["rank"], a["article"], a["views"]])
                tf.flush()
            if domain not in country_done:
                countries = fetch_by_country(domain, year, month)
                if not countries:
                    print(f"  no country data for {domain}", file=sys.stderr)
                for c in countries:
                    country_writer.writerow(
                        [domain, month_label, c["rank"], c["country"],
                         c["views_ceil"]])
                cf.flush()
            time.sleep(0.5)


def done_domains():
    if not MONTHLY_FILE.exists():
        return set()
    with open(MONTHLY_FILE) as f:
        return {row["domain"] for row in csv.DictReader(f)}


def main():
    wikis = load_wikis()
    year, month = last_full_month()
    failures = 0

    write_tops(wikis, year, month)

    end = datetime.now(timezone.utc).strftime("%Y%m%d00")
    skip = done_domains()
    if skip:
        print(f"Resuming: {len(skip)} wikis already in the monthly file")

    write_header = not MONTHLY_FILE.exists()
    with open(MONTHLY_FILE, "a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["domain", "month", "desktop", "mobile_web",
                        "mobile_app", "total"],
            lineterminator="\n",
        )
        if write_header:
            writer.writeheader()
        for wiki in wikis:
            domain = wiki["domain"]
            if domain in skip:
                continue
            print(f"monthly pageviews: {domain}")
            months = {}
            try:
                for access in ACCESS_METHODS:
                    key = access.replace("-", "_")
                    for m, views in fetch_monthly(domain, access, end).items():
                        months.setdefault(m, {})[key] = views
                    time.sleep(0.5)
            except Exception as e:
                failures += 1
                print(f"  FAILED: {e}", file=sys.stderr)
                continue
            for m in sorted(months):
                row = {"domain": domain,
                       "month": f"{m[:4]}-{m[4:6]}",
                       **months[m]}
                row["total"] = sum(months[m].values())
                writer.writerow(row)
            f.flush()

    print("\nDone.")
    if failures:
        print(f"ERROR: {failures} wikis failed. Re-run to fetch them.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

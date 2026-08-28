#!/usr/bin/env python3
"""Build the inventory of Indic language wikis.

Reads languages.yaml (entries with status exclude are skipped).
For each language:
  1. Finds its wikis in the Wikimedia sitematrix.
  2. For each wiki, gets the first revision timestamp.
  3. For each wiki, gets edit activity start from the Wikistats REST API.
  4. Gets inception dates from Wikidata (P571) for all wikis, and
     launch dates from the List of Wikipedias article for Wikipedias.

Writes data/wikis.csv, one row per wiki.

launch_date is the canonical founding date for Wikipedias.
For other wikis, the date signals can disagree: imported revisions
keep their original timestamps. A disagreement of more than one year
sets the review_dates flag.

Usage: uv run scripts/fetch_inventory.py
"""

import csv
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

REPO = Path(__file__).resolve().parent.parent
LANGUAGES_FILE = REPO / "languages.yaml"
OUTPUT_FILE = REPO / "data" / "wikis.csv"

SITEMATRIX_API = "https://meta.wikimedia.org/w/api.php"
WIKISTATS_EDITS = (
    "https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/"
    "{domain}/all-editor-types/all-page-types/monthly/2001010100/{end}"
)

# Wikimedia API etiquette asks for a descriptive User-Agent.
USER_AGENT = (
    "state-of-indic-language-wikis/0.1 "
    "(research for Wiki Conference India 2026 keynote)"
)

PROJECTS = [
    "wikipedia",
    "wiktionary",
    "wikisource",
    "wikiquote",
    "wikibooks",
    "wikinews",
    "wikivoyage",
    "wikiversity",
]

session = requests.Session()
session.headers["User-Agent"] = USER_AGENT

failures = 0


def get(url, **kwargs):
    """GET with retries on rate limits (HTTP 429) and timeouts."""
    delay = 30
    for attempt in range(5):
        try:
            resp = session.get(url, timeout=60, **kwargs)
        except requests.RequestException as e:
            if attempt == 4:
                raise
            print(f"  request failed ({e}), retrying in {delay}s ...")
            time.sleep(delay)
            delay *= 2
            continue
        if resp.status_code != 429:
            return resp
        # Cap the wait: Wikimedia can send very large Retry-After values.
        wait = min(int(resp.headers.get("Retry-After", delay)), 120)
        print(f"  rate limited, waiting {wait}s ...")
        time.sleep(wait)
        delay *= 2
    return resp


def load_languages():
    with open(LANGUAGES_FILE) as f:
        return yaml.safe_load(f)["languages"]


def fetch_sitematrix():
    """Return {lang_code: [site, ...]} from the sitematrix API."""
    print("Fetching sitematrix ...")
    resp = get(
        SITEMATRIX_API,
        params={
            "action": "sitematrix",
            "format": "json",
            "formatversion": "2",
            "smtype": "language",
        },
    )
    resp.raise_for_status()
    matrix = resp.json()["sitematrix"]
    result = {}
    for key, entry in matrix.items():
        if not key.isdigit():
            continue  # skip "count" and "specials"
        result[entry["code"]] = entry.get("site", [])
    print(f"  {len(result)} languages in sitematrix")
    return result


def fetch_first_revision(domain):
    """Return the timestamp of the earliest revision on the wiki."""
    resp = get(
        f"https://{domain}/w/api.php",
        params={
            "action": "query",
            "list": "allrevisions",
            "arvdir": "newer",
            "arvlimit": "1",
            "arvprop": "timestamp",
            "format": "json",
            "formatversion": "2",
        },
    )
    resp.raise_for_status()
    revisions = resp.json()["query"]["allrevisions"]
    if not revisions:
        return None
    return revisions[0]["revisions"][0]["timestamp"]


def fetch_activity_start(domain):
    """Return (first_month_with_edits, first_month_with_10_edits)."""
    end = datetime.now(timezone.utc).strftime("%Y%m%d00")
    resp = get(WIKISTATS_EDITS.format(domain=domain, end=end))
    if resp.status_code == 404:
        return None, None  # wiki unknown to Wikistats
    resp.raise_for_status()
    results = resp.json()["items"][0]["results"]
    first_edit_month = None
    first_active_month = None
    for row in results:
        edits = row["edits"]
        month = row["timestamp"][:7]
        if edits > 0 and first_edit_month is None:
            first_edit_month = month
        if edits >= 10 and first_active_month is None:
            first_active_month = month
            break
    return first_edit_month, first_active_month


def fetch_inceptions(dbnames):
    """Return {dbname: inception date} from Wikidata (P571 via P1800).

    First-revision and Wikistats dates are both wrong for wikis that
    imported content from other wikis. Wikidata inception is curated
    by hand, so it serves as the authoritative founding date.
    """
    print("Fetching inception dates from Wikidata ...")
    values = " ".join(f'"{db}"' for db in dbnames)
    query = f"""
    SELECT ?db ?inception WHERE {{
      VALUES ?db {{ {values} }}
      ?item wdt:P1800 ?db .
      OPTIONAL {{ ?item wdt:P571 ?inception }}
    }}"""
    resp = get(
        "https://query.wikidata.org/sparql",
        params={"query": query, "format": "json"},
    )
    resp.raise_for_status()
    result = {}
    for binding in resp.json()["results"]["bindings"]:
        if "inception" not in binding:
            continue
        db = binding["db"]["value"]
        result[db] = binding["inception"]["value"][:10]
    print(f"  {len(result)} inception dates found")
    return result


def fetch_launch_dates():
    """Return {lang_code: launch date} for Wikipedias.

    Source: the List of Wikipedias article on English Wikipedia.
    Its launch dates are community curated and reviewed, so this is
    the canonical founding date source for Wikipedias (decision from
    Santhosh, 2026-08-27). Sister projects have no such list.
    """
    print("Fetching launch dates from List of Wikipedias ...")
    resp = get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "parse",
            "page": "List_of_Wikipedias",
            "prop": "text",
            "format": "json",
            "formatversion": "2",
        },
    )
    resp.raise_for_status()
    html = resp.json()["parse"]["text"]
    result = {}
    # Each table row carries the launch date in a data-sort-value
    # attribute (ISO date, zero padded). Row tags can have attributes,
    # so split with a regex, and keep one date per row only.
    for row in re.split(r"<tr[^>]*>", html)[1:]:
        dates = re.findall(r'data-sort-value="0*(\d{4}-\d{2}-\d{2})', row)
        if len(dates) != 1:
            continue
        for code in re.findall(r'https://([a-z-]+)\.wikipedia\.org/wiki/', row):
            result.setdefault(code, dates[0])
    print(f"  {len(result)} launch dates found")
    return result


def years_between(iso_a, iso_b):
    a = datetime.fromisoformat(iso_a.replace("Z", "+00:00"))
    b = datetime.strptime(iso_b, "%Y-%m").replace(tzinfo=timezone.utc)
    return abs((b - a).days) / 365.25


def main():
    global failures
    languages = load_languages()
    sitematrix = fetch_sitematrix()

    rows = []
    missing = []
    for lang in languages:
        if lang["status"] == "exclude":
            continue
        code = lang["code"]
        sites = sitematrix.get(code)
        if not sites:
            missing.append(code)
            continue
        for site in sites:
            project = site["code"]
            if project == "wiki":
                project = "wikipedia"
            if project not in PROJECTS:
                continue
            domain = site["url"].removeprefix("https://")
            closed = site.get("closed", False)
            print(f"{domain} ({lang['name']}, {project})"
                  f"{' [closed]' if closed else ''}")

            first_revision = None
            first_edit_month = None
            first_active_month = None
            try:
                first_revision = fetch_first_revision(domain)
            except Exception as e:
                failures += 1
                print(f"  first revision FAILED: {e}", file=sys.stderr)
            try:
                first_edit_month, first_active_month = fetch_activity_start(domain)
            except Exception as e:
                failures += 1
                print(f"  wikistats FAILED: {e}", file=sys.stderr)

            rows.append({
                "lang": code,
                "language": lang["name"],
                "family": lang["family"],
                "script": lang["script"],
                "status": lang["status"],
                "project": project,
                "dbname": site["dbname"],
                "domain": domain,
                "closed": "yes" if closed else "",
                "first_revision": first_revision or "",
                "first_edit_month": first_edit_month or "",
                "first_active_month": first_active_month or "",
                "inception_wikidata": "",
                "launch_date": "",
                "review_dates": "",
            })
            time.sleep(1)

    inceptions = fetch_inceptions([r["dbname"] for r in rows])
    launch_dates = fetch_launch_dates()
    for row in rows:
        row["inception_wikidata"] = inceptions.get(row["dbname"], "")
        if row["project"] == "wikipedia":
            row["launch_date"] = launch_dates.get(row["lang"], "")

        # launch_date is canonical for Wikipedias. Rows without it get
        # a review flag when the other signals disagree by more than a
        # year: imported revisions make first_revision (and sometimes
        # the Wikistats months) earlier than the real founding date.
        if row["launch_date"]:
            continue
        review = ""
        inception = row["inception_wikidata"]
        first_revision = row["first_revision"]
        if inception and first_revision:
            if abs(int(first_revision[:4]) - int(inception[:4])) > 1:
                review = "yes"
        elif first_revision and row["first_active_month"]:
            if years_between(first_revision, row["first_active_month"]) > 1:
                review = "yes"
        row["review_dates"] = review

    rows.sort(key=lambda r: (r["lang"], PROJECTS.index(r["project"])))

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} wikis to {OUTPUT_FILE}")
    if missing:
        print(f"Languages with no wiki (not in sitematrix): {', '.join(missing)}")
    wp = sum(1 for r in rows if r["project"] == "wikipedia")
    ws = sum(1 for r in rows if r["project"] == "wikisource")
    wt = sum(1 for r in rows if r["project"] == "wiktionary")
    print(f"Wikipedias: {wp}, Wikisources: {ws}, Wiktionaries: {wt}")
    if failures:
        print(f"ERROR: {failures} fetches failed. Data is incomplete. Re-run.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

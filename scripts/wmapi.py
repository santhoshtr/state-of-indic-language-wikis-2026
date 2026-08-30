"""Shared Wikimedia API helpers for the fetch scripts."""

import csv
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent
WIKIS_FILE = REPO / "data" / "wikis.csv"

# Wikimedia API etiquette asks for a descriptive User-Agent.
USER_AGENT = (
    "state-of-indic-language-wikis/0.1 "
    "(research for Wiki Conference India 2026 keynote)"
)

session = requests.Session()
session.headers["User-Agent"] = USER_AGENT


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
        if resp.status_code != 429 and resp.status_code < 500:
            return resp
        if resp.status_code == 429:
            # Cap the wait: Wikimedia can send very large Retry-After values.
            wait = min(int(resp.headers.get("Retry-After", delay)), 120)
            print(f"  rate limited, waiting {wait}s ...")
        else:
            # A persistent 5xx usually means the data does not exist.
            # Two quick retries cover the transient case.
            if attempt >= 2:
                return resp
            wait = min(delay, 60)
            print(f"  server error {resp.status_code}, retrying in {wait}s ...")
        time.sleep(wait)
        delay *= 2
    return resp


def load_wikis(project=None, include_closed=False):
    """Return the wiki rows from data/wikis.csv."""
    with open(WIKIS_FILE) as f:
        rows = list(csv.DictReader(f))
    if project:
        rows = [r for r in rows if r["project"] == project]
    if not include_closed:
        rows = [r for r in rows if not r["closed"]]
    return rows

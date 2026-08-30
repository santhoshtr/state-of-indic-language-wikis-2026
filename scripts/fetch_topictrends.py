#!/usr/bin/env python3
"""Fetch topic trends and knowledge gaps from topictrends.wmcloud.org.

Covers the Wikipedias in data/wikis.csv. Topictrends holds only
recent data (about the last 60 days), so the topic files describe
a recent window, not history. The gap data comes from a monthly
coverage snapshot; the response records the snapshot date.

Fetches:
  1. Top 25 categories by pageviews, last 60 days.
     -> data/topic_pageviews.csv
  2. Top 25 categories by edits, last 60 days.
     -> data/topic_edits.csv
  3. Knowledge gap discovery per wiki:
     - against English (reference enwiki), and
     - against peers: all pairs among the eight largest active
       communities, and a family anchor for the smaller wikis.
       The peer choice is editorial; see MAJORS and FAMILY_ANCHORS.
     Ranked by estimated missing readership (the API default).
     -> data/gaps.csv

All three files are rewritten whole on each run.

Usage: uv run scripts/fetch_topictrends.py
"""

import csv
import sys
import time
from datetime import date, timedelta

from wmapi import REPO, get, load_wikis

TT = "https://topictrends.wmcloud.org/api"
TOP_N = 25
GAP_LIMIT = 50
WINDOW_DAYS = 60

# The eight largest active communities: compare each against each.
MAJORS = ["bnwiki", "hiwiki", "tawiki", "tewiki",
          "mlwiki", "mrwiki", "knwiki", "urwiki"]

# Family anchor for the smaller wikis (editorial choice):
# Indo-Aryan wikis compare against Hindi, Dravidian against Tamil.
# Santali and Meitei compare against Bengali (geography), Newar
# against Nepali (geography).
FAMILY_ANCHORS = {
    "indo-aryan": "hiwiki",
    "dravidian": "tawiki",
    "munda": "bnwiki",
    "tibeto-burman": "bnwiki",
}
ANCHOR_OVERRIDES = {"newwiki": "newiki"}

# Wikis that topictrends does not index (confirmed by Santhosh).
NOT_INDEXED = {"magwiki"}

failures = 0


def fetch(path, params):
    global failures
    resp = get(f"{TT}/{path}", params=params)
    if resp.status_code in (404, 500):
        failures += 1
        print(f"  no data: {path} {params} ({resp.status_code})",
              file=sys.stderr)
        return None
    resp.raise_for_status()
    return resp.json()


def main():
    global failures
    wikis = load_wikis(project="wikipedia")
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=WINDOW_DAYS - 1)
    window = {"start_date": start.isoformat(), "end_date": end.isoformat()}
    print(f"Window: {window['start_date']} .. {window['end_date']}")

    topic_rows = {"pageviews": [], "pageedits": []}
    for wiki in wikis:
        db = wiki["dbname"]
        if db in NOT_INDEXED:
            continue
        print(db)
        for kind, value_key in [("pageviews", "views"), ("pageedits", "edits")]:
            data = fetch(f"{kind}/top_categories",
                         {"wiki": db, "top_n": TOP_N, **window})
            if data is None:
                continue
            for rank, c in enumerate(data["categories"], 1):
                top = c["top_articles"][0] if c["top_articles"] else {}
                topic_rows[kind].append([
                    wiki["lang"], window["start_date"], window["end_date"],
                    rank, c["qid"], c.get("title_en", c["title"]),
                    c[value_key],
                    top.get("title_en", top.get("title", "")),
                ])
            time.sleep(1)

    for kind, name, value_col in [
        ("pageviews", "topic_pageviews.csv", "views"),
        ("pageedits", "topic_edits.csv", "edits"),
    ]:
        path = REPO / "data" / name
        with open(path, "w", newline="") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(["lang", "start_date", "end_date", "rank",
                             "category_qid", "category_en", value_col,
                             "top_article_en"])
            writer.writerows(topic_rows[kind])
        print(f"Wrote {len(topic_rows[kind])} rows to {path}")

    pairs = []
    for wiki in wikis:
        db = wiki["dbname"]
        if db in NOT_INDEXED:
            continue
        pairs.append((db, "enwiki"))
        if db in MAJORS:
            pairs.extend((db, ref) for ref in MAJORS if ref != db)
        else:
            anchor = ANCHOR_OVERRIDES.get(
                db, FAMILY_ANCHORS[wiki["family"]])
            if anchor != db:
                pairs.append((db, anchor))

    gap_rows = []
    for target, reference in pairs:
        print(f"gaps: {target} vs {reference}")
        data = fetch("gap_discovery/categories",
                     {"reference": reference, "target": target,
                      "limit": GAP_LIMIT})
        if data is None:
            continue
        for rank, c in enumerate(data["categories"], 1):
            gap_rows.append([
                target, reference, data["reference_date"], rank,
                c["category_qid"], c["category_title"], c["gap"],
                c["overlap_target"], c["overlap_reference"],
                round(c["coverage_pct"], 4), c.get("weighted_score", ""),
            ])
        time.sleep(1)

    path = REPO / "data" / "gaps.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["target", "reference", "snapshot_date", "rank",
                         "category_qid", "category_en", "gap",
                         "overlap_target", "overlap_reference",
                         "coverage_pct", "weighted_score"])
        writer.writerows(gap_rows)
    print(f"Wrote {len(gap_rows)} rows to {path}")

    if failures:
        print(f"WARNING: {failures} requests had no data.", file=sys.stderr)


if __name__ == "__main__":
    main()

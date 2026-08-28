#!/usr/bin/env python3
"""Fetch Content Translation statistics for the Indic languages.

Reads languages.yaml. Downloads the public CX datasets (the same
TSV files that cxstats.toolforge.org aggregates) and filters them
to the languages in scope. Writes:

  - data/cx_translations_monthly.csv: published translations per
    month per target language (from the daily per-wiki file)
  - data/cx_language_pairs.csv: lifetime translation counts per
    source-target pair where either side is an Indic language
  - data/cx_deletions.csv: lifetime deleted translations per
    target language
  - data/cx_translators.csv: lifetime translator count per
    target language

Usage: uv run scripts/fetch_cx_stats.py
"""

import csv
import io
from collections import defaultdict

import yaml

from wmapi import REPO, get

BASE = ("https://analytics.wikimedia.org/published/datasets/"
        "periodic/reports/metrics/cx")


def load_codes():
    with open(REPO / "languages.yaml") as f:
        langs = yaml.safe_load(f)["languages"]
    return {l["code"] for l in langs if l["status"] == "include"}


def fetch_tsv(name):
    print(f"Fetching {name} ...")
    resp = get(f"{BASE}/{name}")
    resp.raise_for_status()
    return csv.DictReader(io.StringIO(resp.text), delimiter="\t")


def write(name, header, rows):
    path = REPO / "data" / name
    with open(path, "w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    print(f"  wrote {len(rows)} rows to {path}")


def main():
    codes = load_codes()

    monthly = defaultdict(int)
    for row in fetch_tsv("published_cx_translations_per_wiki.tsv"):
        lang = row["language"]
        if lang in codes:
            month = row["published_date"][:7]
            monthly[(month, lang)] += int(row["cx2_published_translations"])
    write("cx_translations_monthly.csv",
          ["month", "target_lang", "translations"],
          [(m, l, c) for (m, l), c in sorted(monthly.items())])

    pairs = []
    for row in fetch_tsv("translation_language_pairs.tsv"):
        if row["source_language"] in codes or row["target_language"] in codes:
            pairs.append((row["source_language"], row["target_language"],
                          int(row["no_translations"])))
    pairs.sort(key=lambda r: -r[2])
    write("cx_language_pairs.csv",
          ["source_lang", "target_lang", "translations"], pairs)

    deletions = defaultdict(int)
    for row in fetch_tsv("cx_deletions.tsv"):
        if row["wiki"] in codes:
            deletions[row["wiki"]] += int(row["count"])
    write("cx_deletions.csv", ["target_lang", "deleted"],
          sorted(deletions.items()))

    translators = [
        (row["translation_target_language"], int(row["number_of_translators"]))
        for row in fetch_tsv("translators_per_wiki.tsv")
        if row["translation_target_language"] in codes
    ]
    write("cx_translators.csv", ["target_lang", "translators"],
          sorted(translators, key=lambda r: -r[1]))


if __name__ == "__main__":
    main()

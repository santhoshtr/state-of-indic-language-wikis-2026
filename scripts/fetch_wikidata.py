#!/usr/bin/env python3
"""Fetch Wikidata coverage statistics for the Indic languages.

Uses the QLever Wikidata SPARQL endpoint (qlever.dev): the official
WDQS endpoint cannot count labels inside its 60 second limit.
QLever serves a periodic snapshot of Wikidata, so numbers can trail
live Wikidata by days.

For each language in scope:
  1. Total entities with a label in the language.
  2. India-related items (country = India, P17=Q668) with a label
     in the language. The same query with reference languages (en)
     gives the comparison baseline.
  3. Lexeme count for the language.

Writes data/wikidata_stats.csv. The india_items_total column repeats
the denominator so the file is self-contained.

Label language codes follow Wikidata, which splits some languages
by script (gom-deva, ks-arab, ...); variants are summed.

Usage: uv run scripts/fetch_wikidata.py
"""

import csv
import sys
import time

import yaml

from wmapi import REPO, get

QLEVER = "https://qlever.dev/api/wikidata"

PREFIXES = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
"""

# Wiki code -> Wikidata label language codes (script variants summed).
LABEL_VARIANTS = {
    "bh": ["bho"],
    "gom": ["gom", "gom-deva", "gom-latn"],
    "ks": ["ks", "ks-arab", "ks-deva"],
    "mni": ["mni", "mni-beng"],
    "pi": ["pi"],
}

# Language items whose lexemes P424 resolution misses. Lexemes for
# Hindi and Urdu are mostly filed under Hindustani (Q11051), which
# therefore counts for both; Punjabi (Q58635) lacks a P424 claim.
LEXEME_QID_EXTRAS = {
    "hi": ["Q1568", "Q11051"],
    "ur": ["Q1617", "Q11051"],
    "pa": ["Q58635"],
}

failures = 0


def load_languages():
    with open(REPO / "languages.yaml") as f:
        langs = yaml.safe_load(f)["languages"]
    return [l for l in langs if l["status"] == "include"]


def sparql_count(query):
    global failures
    resp = get(QLEVER, params={"query": PREFIXES + query},
               headers={"Accept": "application/sparql-results+json"})
    if resp.status_code != 200:
        failures += 1
        print(f"  FAILED ({resp.status_code}): {query[:80]}", file=sys.stderr)
        return None
    data = resp.json()
    if "exception" in data:
        failures += 1
        print(f"  FAILED: {data['exception'][:100]}", file=sys.stderr)
        return None
    return int(data["results"]["bindings"][0]["n"]["value"])


def count_labels(label_code, restrict=""):
    return sparql_count(
        f"SELECT (COUNT(*) AS ?n) WHERE {{ {restrict} "
        f"?i @{label_code}@rdfs:label ?l }}"
    )


def lexemes_per_code(codes):
    """Map wiki code -> lexeme count.

    P424 (Wikimedia language code) is ambiguous: a code can point to
    the language item and to Wikipedia-edition items. Counting
    lexemes per candidate resolves it, because only the real
    language item has lexemes.
    """
    resp = get(QLEVER, params={"query": PREFIXES + """
        SELECT ?lang (COUNT(*) AS ?n) WHERE {
          ?l a ontolex:LexicalEntry ; dct:language ?lang .
        } GROUP BY ?lang"""},
        headers={"Accept": "application/sparql-results+json"})
    resp.raise_for_status()
    by_qid = {}
    for b in resp.json()["results"]["bindings"]:
        by_qid[b["lang"]["value"].split("/")[-1]] = int(b["n"]["value"])

    values = " ".join(f'"{c}"' for c in codes)
    resp = get(QLEVER, params={"query": PREFIXES + f"""
        SELECT ?code ?lang WHERE {{
          VALUES ?code {{ {values} }}
          ?lang wdt:P424 ?code .
        }}"""},
        headers={"Accept": "application/sparql-results+json"})
    resp.raise_for_status()
    candidates = {}
    for b in resp.json()["results"]["bindings"]:
        code = b["code"]["value"]
        qid = b["lang"]["value"].split("/")[-1]
        candidates.setdefault(code, set()).add(qid)
    for code, extras in LEXEME_QID_EXTRAS.items():
        candidates.setdefault(code, set()).update(extras)
    return {
        code: sum(by_qid.get(q, 0) for q in qids)
        for code, qids in candidates.items()
    }


def main():
    languages = load_languages()
    codes = [l["code"] for l in languages]

    india_total = sparql_count(
        "SELECT (COUNT(*) AS ?n) WHERE { ?i wdt:P17 wd:Q668 }")
    en_india = count_labels("en", "?i wdt:P17 wd:Q668 .")
    print(f"India items: {india_total}; with English label: {en_india}")

    # Lexeme lookup uses ISO codes (bho for the bh wiki).
    iso = {c: LABEL_VARIANTS.get(c, [c])[0] for c in codes}
    lexemes_by_iso = lexemes_per_code(sorted(set(iso.values())))

    rows = []
    for lang in languages:
        code = lang["code"]
        print(code)
        variants = LABEL_VARIANTS.get(code, [code])
        labels = sum(filter(None, (count_labels(v) for v in variants)))
        india = sum(filter(None, (
            count_labels(v, "?i wdt:P17 wd:Q668 .") for v in variants)))
        rows.append({
            "lang": code,
            "labels_total": labels,
            "india_items_with_label": india,
            "india_items_total": india_total,
            "lexemes": lexemes_by_iso.get(iso[code], 0),
        })
        time.sleep(0.3)

    path = REPO / "data" / "wikidata_stats.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()),
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {len(rows)} rows to {path}")
    print(f"(India items with English label: {en_india} of {india_total})")
    if failures:
        print(f"WARNING: {failures} queries failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

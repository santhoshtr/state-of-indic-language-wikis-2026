#!/usr/bin/env python3
"""Dump every Malayalam lexeme on Wikidata for manual inspection.

Background: Malayalam is morphologically productive, so a
materialized lexeme list is a debated way to model it. This dump
supports that inspection: one row per lexeme with its lemma,
lexical category, and sense/form counts.

Writes data/ml_lexemes.csv, sorted by lemma.

Uses the QLever Wikidata endpoint (a periodic snapshot; counts can
trail live Wikidata by days).

Usage: uv run scripts/fetch_ml_lexemes.py
"""

import csv
import io

from wmapi import REPO, get

QLEVER = "https://qlever.dev/api/wikidata"
OUTPUT = REPO / "data" / "ml_lexemes.csv"

QUERY = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
SELECT ?lexeme ?lemma ?category
       (COUNT(DISTINCT ?sense) AS ?senses)
       (COUNT(DISTINCT ?form) AS ?forms) WHERE {
  ?lexeme a ontolex:LexicalEntry ;
          dct:language wd:Q36236 ;
          wikibase:lemma ?lemma .
  OPTIONAL { ?lexeme wikibase:lexicalCategory ?cat .
             ?cat @en@rdfs:label ?category }
  OPTIONAL { ?lexeme ontolex:sense ?sense }
  OPTIONAL { ?lexeme ontolex:lexicalForm ?form }
}
GROUP BY ?lexeme ?lemma ?category
"""


def main():
    print("Querying QLever for all Malayalam lexemes ...")
    resp = get(QLEVER, params={"query": QUERY},
               headers={"Accept": "text/csv"})
    resp.raise_for_status()
    # the endpoint omits the charset; requests would guess latin-1
    resp.encoding = "utf-8"

    reader = csv.DictReader(io.StringIO(resp.text))
    rows = []
    for r in reader:
        rows.append({
            "lexeme_id": r["lexeme"].rsplit("/", 1)[-1],
            "lemma": r["lemma"],
            "category": r["category"],
            "senses": r["senses"],
            "forms": r["forms"],
        })
    rows.sort(key=lambda r: r["lemma"])

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["lexeme_id", "lemma", "category",
                           "senses", "forms"],
            lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} lexemes to {OUTPUT}")


if __name__ == "__main__":
    main()

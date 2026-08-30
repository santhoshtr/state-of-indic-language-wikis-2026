#!/usr/bin/env python3
"""Build the aggregate data that the presentation embeds.

Reads the fetched files in data/ and derives the small aggregates
the deck charts need. Writes data/deck_data.json, and when
presentation.html exists, replaces the JSON between the
DECK-DATA-START / DECK-DATA-END markers in place.

Usage: uv run scripts/build_deck_data.py
"""

import csv
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
OUT = DATA / "deck_data.json"
DECK = REPO / "presentation.html"

# World top-10 languages by Wikidata lexeme count, from the QLever
# Wikidata endpoint on 2026-08-30 (see scripts/fetch_wikidata.py for
# the endpoint; query: lexemes grouped by dct:language).
LEXEMES_WORLD_TOP10 = [
    ["German", 241979], ["Russian", 102347], ["Danish", 99767],
    ["Estonian", 83227], ["English", 74778], ["Malayalam", 67372],
    ["Spanish", 65788], ["Italian", 64927], ["Arabic", 57553],
    ["Latin", 56347],
]


# Main Page titles per wiki, so the top-article pick skips them.
MAIN_PAGES = {
    "मुख्य_पृष्ठ", "বেটুপাত", "प्रधान_पन्ना", "প্রধান_পাতা", "পয়লা_পাতা",
    "मुख्य_पन्ना", "މައި_ޞަފްޙާ", "मुखेल_पान", "મુખપૃષ્ઠ", "ಮುಖ್ಯ_ಪುಟ",
    "اَہَم_صَفہٕ", "सम्मुख_पन्ना", "പ്രധാന_താൾ", "ꯃꯔꯨꯑꯣꯏꯕ_ꯂꯃꯥꯏ", "मुखपृष्ठ",
    "मू_पौ", "ପ୍ରଧାନ_ପୃଷ୍ଠା", "ਮੁੱਖ_ਸਫ਼ਾ", "पमुख_पत्त_Pamukha_patta",
    "پہلا_صفہ", "मुख्यपृष्ठम्", "مُک_صفحو", "මුල්_පිටුව", "முதற்_பக்கம்",
    "మొదటి_పేజీ", "صفحۂ_اول", "ᱢᱩᱬᱩᱛ_ᱥᱟᱦᱴᱟ", "Main_Page",
}


def rows(name):
    with open(DATA / name) as f:
        return list(csv.DictReader(f))


def year_of(month):
    return int(month[:4])


def main():
    wikis = rows("wikis.csv")
    snapshot = {r["domain"]: r for r in rows("snapshot.csv")}
    ts = rows("wikistats_monthly.csv")
    pv = rows("pageviews_monthly.csv")
    cx_monthly = rows("cx_translations_monthly.csv")
    cx_pairs = rows("cx_language_pairs.csv")
    cx_translators = rows("cx_translators.csv")
    tops = rows("top_articles.csv")
    countries = rows("pageviews_by_country.csv")
    gaps = rows("gaps.csv")
    wd = rows("wikidata_stats.csv")

    langs = {r["lang"]: r for r in wikis if r["project"] == "wikipedia"}

    # --- monthly series prep -------------------------------------
    active = defaultdict(lambda: defaultdict(list))   # domain -> year -> [..]
    new_pages = defaultdict(lambda: defaultdict(int))  # domain -> year -> n
    edits = defaultdict(lambda: [0, 0])                # domain -> [all, bots]
    for r in ts:
        d, y = r["domain"], year_of(r["month"])
        a = sum(int(float(r[k] or 0)) for k in
                ("editors_5_24", "editors_25_99", "editors_100plus"))
        active[d][y].append(a)
        new_pages[d][y] += int(float(r["new_pages"] or 0))
        all_e = int(float(r["edits_all"] or 0))
        human = int(float(r["edits_user"] or 0)) + int(float(r["edits_anon"] or 0))
        edits[d][0] += all_e
        edits[d][1] += max(all_e - human, 0)

    def yearly_avg(domain):
        return {y: round(sum(v) / len(v), 1)
                for y, v in sorted(active[domain].items())}

    pv_yearly_by_domain = defaultdict(lambda: defaultdict(int))
    mobile = defaultdict(lambda: [0, 0])  # domain -> [mobile_2025, total_2025]
    for r in pv:
        d, y = r["domain"], year_of(r["month"])
        total = int(float(r["total"] or 0))
        pv_yearly_by_domain[d][y] += total
        if y == 2025:
            m = int(float(r["mobile_web"] or 0)) + int(float(r["mobile_app"] or 0))
            mobile[d][0] += m
            mobile[d][1] += total

    # --- per-Wikipedia cards -------------------------------------
    cx_total_by_lang = defaultdict(int)
    for r in cx_monthly:
        cx_total_by_lang[r["target_lang"]] += int(r["translations"])

    top_article = {}
    for r in tops:
        lang = r["domain"].split(".")[0]
        if r["domain"].split(".")[1] != "wikipedia" or lang in top_article:
            continue
        page = r["page"]
        if ":" in page or page in MAIN_PAGES:
            continue
        top_article[lang] = [page.replace("_", " "), int(r["views"])]

    country_top = defaultdict(list)
    country_tot = defaultdict(int)
    for r in countries:
        if r["domain"].split(".")[1] != "wikipedia":
            continue
        country_tot[r["domain"]] += int(r["views_ceil"])
    for r in countries:
        d = r["domain"]
        if d.split(".")[1] != "wikipedia" or len(country_top[d]) >= 5:
            continue
        pct = round(int(r["views_ceil"]) / country_tot[d] * 100, 1)
        country_top[d].append([r["country"], pct])

    wd_by_lang = {r["lang"]: r for r in wd}
    india_total = int(wd[0]["india_items_total"]) if wd else 0

    wikipedias = []
    for lang, w in sorted(langs.items()):
        d = w["domain"]
        snap = snapshot.get(d, {})
        articles = int(snap.get("articles") or 0)
        ya = yearly_avg(d)
        peak_year, peak = max(ya.items(), key=lambda kv: kv[1]) if ya else (0, 0)
        e_all, e_bot = edits[d]
        wrow = wd_by_lang.get(lang, {})
        growth = []
        cum = 0
        for y in sorted(new_pages[d]):
            cum += new_pages[d][y]
            growth.append([y, cum])
        wikipedias.append({
            "lang": lang,
            "name": w["language"],
            "family": w["family"],
            "script": w["script"],
            "launch": w["launch_date"],
            "articles": articles,
            "bot_pct": round(e_bot / e_all * 100, 1) if e_all else 0,
            "active": ya,
            "active_2025": ya.get(2025, 0),
            "peak": peak,
            "peak_year": peak_year,
            "mobile_pct": round(mobile[d][0] / mobile[d][1] * 100)
            if mobile[d][1] else None,
            "pv_2025_m": round(pv_yearly_by_domain[d].get(2025, 0) / 1e6, 1),
            "cx_total": cx_total_by_lang.get(lang, 0),
            "cx_share": round(cx_total_by_lang.get(lang, 0) / articles * 100, 1)
            if articles else 0,
            "growth": growth,
            "admins": int(snap.get("admins") or 0),
            "top_article": top_article.get(lang),
            "countries": country_top.get(d, []),
            "india_label_pct": round(
                int(wrow.get("india_items_with_label") or 0) / india_total * 100, 1)
            if india_total else None,
            "lexemes": int(wrow.get("lexemes") or 0),
            "sisters": {
                r2["project"]: int(snapshot.get(r2["domain"], {}).get("articles") or 0)
                for r2 in wikis
                if r2["lang"] == lang and r2["project"] != "wikipedia"
                and not r2["closed"]
            },
        })

    # --- family aggregates ---------------------------------------
    def agg_yearly(domains, source):
        out = defaultdict(int)
        for d in domains:
            for y, v in source[d].items():
                out[y] += v
        return dict(sorted(out.items()))

    wp_domains = [w["domain"] for w in wikis if w["project"] == "wikipedia"]
    editors_yearly = defaultdict(float)
    for d in wp_domains:
        for y, v in yearly_avg(d).items():
            editors_yearly[y] += v
    editors_yearly = {y: round(v) for y, v in sorted(editors_yearly.items())
                      if 2003 <= y <= 2025}

    pageviews_yearly = agg_yearly(wp_domains, pv_yearly_by_domain)
    pageviews_yearly = {y: round(v / 1e6) for y, v in pageviews_yearly.items()
                        if y <= 2025}

    sister_yearly = {}
    for project in ("wikisource", "wiktionary"):
        doms = [w["domain"] for w in wikis
                if w["project"] == project and not w["closed"]]
        agg = defaultdict(float)
        for d in doms:
            for y, v in yearly_avg(d).items():
                agg[y] += v
        sister_yearly[project] = {y: round(v) for y, v in sorted(agg.items())
                                  if 2006 <= y <= 2025}

    cx_yearly = defaultdict(int)
    for r in cx_monthly:
        cx_yearly[year_of(r["month"])] += int(r["translations"])
    cx_yearly = dict(sorted(cx_yearly.items()))

    # CX source shares (into Indic wikis)
    into = [r for r in cx_pairs if r["target_lang"] in langs]
    total_into = sum(int(r["translations"]) for r in into)
    src = defaultdict(int)
    for r in into:
        src[r["source_lang"]] += int(r["translations"])
    indic_pairs = sorted(
        ([r["source_lang"], r["target_lang"], int(r["translations"])]
         for r in into if r["source_lang"] in langs),
        key=lambda x: -x[2])[:6]
    cx_sources = {
        "total": total_into,
        "en_pct": round(src["en"] / total_into * 100, 1),
        "ar_pct": round(src["ar"] / total_into * 100, 1),
        "indic_pct": round(
            sum(v for k, v in src.items() if k in langs) / total_into * 100, 1),
        "indic_pairs": indic_pairs,
    }

    # Gap postcards: top rows per peer pair (non-English references)
    postcards = defaultdict(list)
    for r in gaps:
        if r["reference"] == "enwiki":
            continue
        key = f'{r["target"]}|{r["reference"]}'
        if len(postcards[key]) < 3:
            postcards[key].append(
                [r["category_title"].replace("_", " "), int(r["gap"])])

    # Most frequent top-10 gap categories vs English
    en_cat = defaultdict(int)
    for r in gaps:
        if r["reference"] == "enwiki" and int(r["rank"]) <= 10:
            en_cat[r["category_title"].replace("_", " ")] += 1
    gaps_en_common = sorted(en_cat.items(), key=lambda kv: -kv[1])[:8]

    deck = {
        "generated": date.today().isoformat(),
        "wikipedias": wikipedias,
        "editors_yearly": editors_yearly,
        "pageviews_yearly": pageviews_yearly,
        "sister_yearly": sister_yearly,
        "cx_yearly": cx_yearly,
        "cx_sources": cx_sources,
        "cx_translators": {r["target_lang"]: int(r["translators"])
                           for r in cx_translators},
        "gaps_en_common": gaps_en_common,
        "gap_postcards": postcards,
        "lexemes_world_top10": LEXEMES_WORLD_TOP10,
        "india_items_total": india_total,
        "india_label_en_pct": 89.1,
    }

    payload = json.dumps(deck, ensure_ascii=False, separators=(",", ":"))
    OUT.write_text(payload + "\n")
    print(f"Wrote {OUT} ({len(payload) // 1024} KB)")

    if DECK.exists():
        html = DECK.read_text()
        marked = re.sub(
            r"(/\* DECK-DATA-START \*/).*?(/\* DECK-DATA-END \*/)",
            lambda m: m.group(1) + "window.DECK=" + payload + ";" + m.group(2),
            html, flags=re.S)
        DECK.write_text(marked)
        print(f"Updated data block in {DECK}")


if __name__ == "__main__":
    main()

# Insights, trivia, and celebration candidates

Record candidates here as the research finds them.
Each entry: the fact, the data behind it, and how it can serve the talk.

## From the inventory (A)

* **89 open Indic wikis exist**: 30 Wikipedias, 20 Wiktionaries,
  14 Wikisources, plus Wikiquote, Wikibooks, Wikivoyage,
  Wikiversity. The family is much bigger than "Wikipedia".
  (Counts exclude closed wikis, and the scope excludes pnb and dv
  since 2026-08-31.)
* **First revision timestamps lie.** Bhojpuri Wikipedia launched on
  21 Feb 2003 (List of Wikipedias), but its database holds a revision
  from 2001-08. Doteli shows edits from 2002 for a 2017 wiki.
  Founding dates come from the List of Wikipedias (`launch_date`
  column), never from first revisions.
* **Two founding waves, eight silent years between.** Pioneer wave
  2002-2006: 21 Wikipedias in five years (or, as, ne, pa in June 2002
  through bpy in 2006). Then total silence 2007-2014.
  Incubator-graduation wave 2014-2026: mai 2014, gom 2015,
  tcy 2016, dty 2017, sat 2018, awa 2020, mni 2021,
  anp 2023, mag 2026. Cohort story: what closed the pipeline, and
  what reopened it? (Dates confirmed by List of Wikipedias and
  Wikidata; two-wave picture confirmed by Santhosh.)
* **Odia was the first Indic Wikipedia** (1 June 2002), with
  Assamese, Nepali, and Punjabi following in the same week.
  Four communities share a June 2002 birthday.
* **Magahi Wikipedia launched on 18 June 2026** — weeks before this
  conference. A newborn wiki in the room. Celebration moment.
  (List of Wikipedias and Wikidata agree on the date.)
* **Four languages wait in the incubator**: Dogri (doi), Khowar (khw),
  Mizo (lus), Bodo (brx). "Who is next?" framing.
* **Incubator imports hide true ages.** Doteli shows edits from 2002
  because it imported content; the wiki really started 2017-04.
  Never present first-edit dates as founding dates without the
  review_dates check.
* **Script diversity**: the inventory spans 15+ writing systems,
  including Ol Chiki (Santali), Meitei Mayek (Manipuri), and
  Thaana (Dhivehi). Possible visual moment.

## From the snapshot (B, current stats, fetched 2026-08-28)

* **Urdu Wikipedia is the largest Indic Wikipedia** by articles
  (674k), far ahead of Bengali (191k), Tamil (190k), Hindi (171k).
  Check the bot and translation share before presenting: the article
  count alone can mislead.
* **Bengali Wikipedia has the largest active community** (1,937
  active users in 30 days), almost twice Hindi (1,005). Community
  size and article count rank differently — health is not size.
* **Sister projects outperform their Wikipedias in places.**
  Kannada Wiktionary (266k entries) is 7x Kannada Wikipedia (36k
  articles). Tamil Wiktionary: 409k entries. Gujarati Wikisource
  (66k text pages) is the largest Indic Wikisource, while Gujarati
  Wikipedia (31k) is mid-table. Celebration material, by name.
* **Admin capacity is thin at the edges**: 10 Wikipedias run with
  1-2 admins; tcy.wiktionary has zero. Newar Wikipedia holds 74k
  articles with 2 admins and 32 active users (bot-created legacy?).
* **Newar and Bishnupriya paradox**: large article counts (74k, 25k)
  with tiny communities (32, 15 active users). Legacy of the
  2006-2008 bot-stub era. Contrast with hand-built wikis.

## From the time series (B, fetched 2026-08-28)

* **The Urdu paradox resolved**: the largest Indic Wikipedia (674k
  articles) has a 67% lifetime bot edit share. Newar: 91%, Bishnupriya:
  85%. Article count is not community. Present size
  always next to human activity.
* (Team decision 2026-09-01: keep the Urdu growth story off the
  slides; the data stays here and in data/.)
* **Urdu became the largest Indic Wikipedia only in 2026**: ~390k
  content pages were created between March and July 2026 (peak
  175k in June). Not a bot run: Santhosh verified from the recent
  edits (2026-08-31) that this is rapid human creation. Before the
  drive, Urdu had ~240k created pages, similar to Bengali and
  Tamil. (Wikistats new_pages.)
* **Indic active editors (5+/month) peaked in 2020 at ~1,450 and
  declined ~27% to ~1,060 in 2025.** Growth 2004-2020 was almost
  monotonic; the decline since is steady. The honest health headline,
  and the reason this conference matters. (COVID bump in 2020-21?)
  Caveat: the sum over wikis counts a person once per wiki they are
  active on. The trend shape holds; the absolute number is inflated.
* **Per-wiki peaks cluster in two eras**: 2016-2018 (kn 2016, or 2016,
  sa 2016, ta 2017, pa 2017, mr 2018) and 2020-2022 (hi 2020, bn 2021,
  ur 2022). Worth asking: what were the programs behind each era?
* **Bengali is the resilience story**: 2025 activity is 92% of its
  all-time peak, now the largest active Indic community.
  **Assamese hit its all-time high in 2024-2025** — the only major
  wiki still at peak. Celebration moments.
* **The sobering list**: Kannada at 25% of its 2016 peak, Sanskrit
  27%, Malayalam 37%, Hindi 41%, Odia 34%. Frame as "what will
  reverse this?", not as failure.
* **Angika's deletion rate**: 3,184 articles created, 1,694 survive
  (47% deleted). Quality-control signal worth a mention with care.

## From the readers data (C, fetched 2026-08-29)

* **The pageview cliff.** All-Indic Wikipedia pageviews (human,
  per the API): 197M in 2015 (half year), climbing to a 1.73B peak
  in 2023, then 1.47B (2024) and 968M (2025). MANDATORY CAVEAT:
  bot detection improved in 2024-25, so pre-2024 numbers are
  inflated; the drop is partly measurement correction, partly real
  (AI answers, changed search). Frame as "the AI era is visible in
  our charts" — a keynote moment, handled honestly.
  VERIFY BEFORE USE: the bot-reclassification claim needs the WMF
  Diff announcement (late 2025) as the citation on the slide.
* **Readers are mobile-first: 78-88% mobile** for major wikis
  (Hindi 88%). Editing tools and editor culture remain desktop-first.
  Structural friction worth naming. Exceptions: Urdu and Punjabi
  (~57% mobile) — Urdu's country pattern (US 32%, BR 10%, MX 4%,
  PK invisible) suggests automated traffic still passing the user
  filter; treat Urdu reader numbers with suspicion.
* **Diaspora readership is real but contaminated.** Clear signals:
  Nepal is only 34% of Nepali readership; Sri Lanka 44% of Sinhala;
  the US is #2 for nearly every wiki. But BR or MX sit in the top-5
  reader countries of 31 of 32 Wikipedias — residual bot traffic
  passing the user filter, fleet-wide. Use US share as directional
  only; NP/LK/IN home shares are the trustworthy part. Bangladesh
  and Pakistan are absent by design (privacy protection list).
* **Small-wiki "resilience" is partly bots.** Punjabi's 2025
  readership all-time high comes with IN at only 31% (US 28%,
  BR 6%): likely inflated. Sanskrit reads 95% of peak but IN is 9%
  of its readers (US 32%, SG 10%): mostly not human. Do NOT
  celebrate these numbers. The smaller the wiki, the larger the
  bot share of its "readers".
* **Kannada declines on both axes** (editors at 25% of peak,
  readers at 23% of the 2022 peak, IN-share 68% so the reader
  signal is real). The single most worrying wiki in the data.
* **Top-articles trivia (July 2026):** Hindi #1 is the Ramayanam
  2026 film (319k views). Lamine Yamal appears in the Malayalam AND
  Bengali top-5. Malayalam's list mixes Basheer, S. Janaki, and
  Kathakali with football. Good "what do our readers want" slide.

## From Content Translation (F, fetched 2026-08-29)

* **~300,000 articles came to Indic wikis through translation**
  (298k of the 2.5M global CX total, 12%). Per wiki, the share of
  current articles that arrived via CX: Punjabi 48%, Kashmiri 46%,
  Bengali 33%, Telugu 23%, Tamil 23%, Kannada 20%, Malayalam 15%.
  For several communities, translation is not a side channel;
  it is how the wiki grows.
* **Translation is the counter-trend to the editor decline.**
  Active editors fell ~27% since 2020; CX output nearly tripled:
  18.7k (2020), 24.9k (2021), 32.4k (2022), 51.2k (2023), ~53k
  (2025). Fewer editors, better tools, more articles. A hopeful
  keynote beat after the honest decline. Honesty note: 2026 is
  pacing lower, ~40k annualized from 25k through mid-August.
* **2,612 people have translated into Bengali** (1,766 Hindi,
  1,347 Tamil). Translation has the widest participation funnel
  of any editing workflow. Bengali is the largest Indic CX user
  (64k articles) and en->bn is the largest single pair (62k).
* **English is 93% of the source.** Indic-to-Indic translation is
  just 2.1% (6.4k articles). Urdu->Sindhi (1.1k), Hindi->Punjabi
  (568), Kannada->Tulu (334) show what is possible. A missed
  opportunity to name from the stage: sibling languages barely
  speak to each other. Arabic is the #2 source (4.4%), almost all
  into Urdu (12k) — a reminder that not every gap fills from English.
* **Quality holds: the median CX deletion ratio is 7.4%** of
  published translations, lifetime. The tool's bad reputation for
  raw machine dumps is not supported by survival numbers on most
  Indic wikis.

## From topic trends (D, window 2026-07-01..2026-08-29)

* **Readers come to Indic wikis for identity.** "India" is the #1
  reader category on most wikis, and each wiki's top article is
  local: Zubeen Garg (as), Basheer (ml), K. Kamaraj (ta),
  Bhanubhakta Acharya (ne), Sigiriya (si), Annabhau Sathe (mr).
  Urdu's #1 category is Islam; Telugu and Tulu: Hinduism.
  The Indic wikis are identity encyclopedias; English serves the
  global topics. A defining slide.
* **Readers and editors mostly align.** 7-8 of the top-10 reader
  categories are also top-10 editor categories on hi, as, kn, ne.
  Lowest alignment: bpy, anp, new (bot-built wikis), but also
  Tamil and Sindhi (3 of 10) — editors editing what readers do not
  read. Program-driven editing? Worth a look before presenting.
* **Bhojpuri anomaly: its top reader category is Gambling, top
  article Sports betting.** Likely SEO-driven traffic. Investigate
  before showing; interesting either way.
* Data quirk: some small-wiki category labels resolve to wrong
  languages (anp shows Abkhaz labels). Clean before charting.

## From knowledge gaps (E, coverage snapshot 2026-06-23)

* **The gap to English is mostly a gap of American actors.**
  For every single Indic wiki, the top gap categories vs English
  are: United States, American people, Film actors, Television
  actors. Measuring against English measures distance from
  American pop culture. This VALIDATES the talk's peer-comparison
  thesis: the English gap is not the gap communities should chase.
* **Peer gaps are local, actionable, and asymmetric.**
  Malayalam lacks 5,429 Tamil-cinema articles Tamil has; Tamil
  lacks only 158 Malayalam-poet articles Malayalam has.
  Hindi lacks 3,149 football articles Bengali has (Bengal's
  football culture, visible in data). Kannada lacks 5,546 India
  articles Telugu has; Telugu lacks 561 Kannada-literature
  articles. Each pair tells both wikis what to borrow.
  These make great "gap postcards" between communities.
* topictrends does not index magwiki (too new). Window data is
  recent-only by design; no historic topic shifts.

## From sister projects and Wikidata (G, fetched 2026-08-30)

* **Sister projects buck the Wikipedia editor decline.** Indic
  Wiktionary active editors hit a record in 2025 (59 vs 44 in
  2015). Wikisource recovered from its 2023 dip (137 -> 173).
  While Wikipedias lose editors, the sister projects hold or grow.
* **Tamil Wikisource has ~40 active editors** (2025) — a larger
  active community than most Indic Wikipedias. Bengali Wikisource
  and Tulu Wikisource are at all-time highs; so is Santali
  Wiktionary (~12 active). Celebration moments by name.
* CAUTION (added 2026-08-31): Santhosh questions the lexeme count.
  Malayalam is morphologically productive; a materialized lexeme
  list is a debated model for it. The dump (data/ml_lexemes.csv)
  shows 83% of the lexemes have zero senses and 80% are nouns —
  a bulk word-list import. Soften or reframe the slide below
  before presenting.
* RETIRED CLAIM (2026-08-31): "Malayalam is #6 in the world for
  Wikidata lexemes" is invalid as a celebration — the count is a
  bulk word-list import (83% senseless, 80% nouns), and lexeme
  materialization is a debated model for a morphologically
  productive language. The slide now shows Indic lexeme counts
  with that caveat. Raw counts stay in wikidata_stats.csv.
* **India's knowledge graph speaks English.** Of 912,073 Wikidata
  items about India (country = India), 89% have an English label.
  The best Indic coverage: Hindi 7.8%, Malayalam 7.2%, Tamil 6.2%,
  Telugu 5.8%, Bengali 4.8%. Fewer than 1 in 12 items about India
  can say its own name in an Indian language. The starkest gap in
  the whole research, and it feeds every reuse of Wikidata
  (infoboxes, search, assistants). Strong closing slide before
  "what this conference is for".

## Human edits analysis (2026-09-02; on a slide since 2026-09-02,
minus the IP-editing line and any Urdu mention, per team decisions)

Question: is there a story in human edit counts (registered + IP),
next to the active-editor story the deck already tells?

* **Total human edits look healthy — but the record is borrowed.**
  All-Indic human edits hit all-time highs in 2024 (2.24M) and 2025
  (2.23M), above the 2020-21 peak (2.09M). Without Urdu, 2025 is
  1.74M — 11% below the 2020-21 level. So: editors fell 27%, edits
  (ex-Urdu) fell only 11%.
* **The remaining editors do much more each.** Registered human
  edits per active editor held at ~100-120 per month for a decade,
  then rose to 148 (2024) and 165 (2025). Concentration plus better
  tools (translation among them). Defends the -27% slide against
  "but edit counts are fine!"
* **Urdu's surge is human and enormous**: 134k edits/year
  (2019-21 avg) to 491k (2025), and ~707k in seven months of 2026
  during the creation drive. Matches Santhosh's verification that
  the drive is human editing.
* **Edit winners**: Bengali at an all-time high (630k, 2025);
  Assamese all-time high (93k); Tamil at 90% of its 2013 peak.
* **Edit decliners, sharper than the editor numbers**: Hindi at 33%
  of its 2020 peak (389k -> 132k); Malayalam 27%; Sanskrit 8%;
  Kannada 43%.
* **IP editing is disappearing**: ~45% of human edits in 2004-07,
  12% through 2015-23, 8% in 2025, 4% in 2026 so far.
  Caveat: temporary accounts (IP masking) roll-out reclassifies
  IP edits; the 2024-26 drop is partly measurement. Verify the
  roll-out date per wiki before presenting this line.

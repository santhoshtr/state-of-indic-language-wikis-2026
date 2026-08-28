# Insights, trivia, and celebration candidates

Record candidates here as the research finds them.
Each entry: the fact, the data behind it, and how it can serve the talk.

## From the inventory (A)

* **103 Indic wikis exist**: 32 Wikipedias, 25 Wiktionaries,
  14 Wikisources, plus Wikiquote, Wikibooks, Wikinews, Wikivoyage,
  Wikiversity. The family is much bigger than "Wikipedia".
* **First revision timestamps lie.** Bhojpuri Wikipedia launched on
  21 Feb 2003 (List of Wikipedias), but its database holds a revision
  from 2001-08. Doteli shows edits from 2002 for a 2017 wiki.
  Founding dates come from the List of Wikipedias (`launch_date`
  column), never from first revisions.
* **Two founding waves, six silent years between.** Pioneer wave
  2002-2006: 22 Wikipedias in five years (or, as, ne, pa in June 2002
  through bpy in 2006). Then pnb alone in 2008, and total silence
  2009-2014. Incubator-graduation wave 2014-2026: mai 2014, gom 2015,
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
* **Admin capacity is thin at the edges**: 12 Wikipedias run with
  1-2 admins; tcy.wiktionary has zero. Newar Wikipedia holds 74k
  articles with 2 admins and 32 active users (bot-created legacy?).
* **Newar and Bishnupriya paradox**: large article counts (74k, 25k)
  with tiny communities (32, 15 active users). Legacy of the
  2006-2008 bot-stub era. Contrast with hand-built wikis.

## From the time series (B, fetched 2026-08-28)

* **The Urdu paradox resolved**: the largest Indic Wikipedia (674k
  articles) has a 67% lifetime bot edit share. Newar: 91%, Bishnupriya:
  85%, Dhivehi: 63%. Article count is not community. Present size
  always next to human activity.
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

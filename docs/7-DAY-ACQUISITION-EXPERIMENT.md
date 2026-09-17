# Inside the Number — 7-day traffic sprint

**Window:** Thu Sep 17 → Wed Sep 23, 2026
**Branch:** `sprint-m27` @ `2c8dc65`, based on `origin/main` `fab7551`
**Deployment:** **BLOCKED** — see `docs/deployment-handoff.md`. Nothing in this sprint is live yet.

This is the operating document. The other three are its parts:

| File | What it is |
|---|---|
| `docs/seo-content-map.md` | 7 articles, fully specified |
| `docs/social-distribution-kit.md` | 7 days × X + Reddit + Instagram, drafts ready to send |
| `docs/measurement-dashboard.md` | UTMs, thresholds, and the pass/fail call |
| `docs/deployment-handoff.md` | the one thing Claude cannot do |

---

## The honest starting position

| | |
|---|---|
| Live site | Public since August, on `fab7551` |
| Subscribers | **3 active.** 10 ever acquired, **7 churned** |
| New subscribers, last 7 days | **0** |
| Subscriber sources, all time | homepage embed ×2, homepage direct ×1 — **no guide page has ever converted anyone** |
| Search Console impressions, three newest guides | **0** — they are not in the live sitemap |
| Social posts published by this project | **0** |
| Earnings | $0 |

A 90.9% open rate on three addresses is one person opening an email. Nothing here will produce a statistically meaningful rate. **The sprint answers a different question: will a stranger find a page, read it, click once more, and leave an address?**

---

## The three acquisition problems, in priority order

### 1 · The link graph was inverted — FIXED this sprint

Counting body links only (nav and footer excluded), the three long guides that carry `Article` + `FAQPage` schema and target real search intent were the most orphaned pages on the site:

```
BEFORE                              AFTER (commit 2c8dc65)
/ufc-331-odds             2          /ufc-331-odds             5
/football-line-movement   4          /football-line-movement   7
/mlb-playoffs             5          /mlb-playoffs             8
/games                   24          /games                   24
/no-vig-calculator       23          /no-vig-calculator       23
```

Ten calculators all linked to `/games` and `/no-vig-calculator` and to nothing else, so internal equity pooled in the two pages with the *least* search intent while the pages built to rank starved. A "Read next" block on `/nfl`, `/cfb`, `/games` and `/no-vig-calculator` now routes to the guides.

### 2 · Nothing is discoverable — BLOCKED on deployment

The live sitemap has **28 entries and omits all three guides**. The release candidate fixes this (29 entries) and cannot be deployed from here. Until it ships, the guides are reachable only by internal links, and every Search Console measurement in this sprint reads zero for a reason unrelated to content.

**This is the binding constraint on the entire sprint.**

### 3 · The two highest-intent seasonal pages were structurally thin — PARTLY FIXED

`/nfl` and `/cfb` are where a searcher lands for "NFL Week 2 odds" or "college football spreads".

| | `/nfl` | `/cfb` |
|---|---|---|
| Words | 484 | 334 |
| `<h2>` elements | 1 | **0** |
| Schema | `BreadcrumbList` only | `Organization`, `WebPage`, `BreadcrumbList` |

Fixed: "How to read this board" was a `<div class="pick-tag">` on both — it is that section's heading, so it is now an `<h2>` with the same class plus a margin reset, rendering identically. `/nfl` gained the `Organization` + `WebPage` schema every other priority page already had.

**Not fixed, deliberately:** the word counts. Padding a live board with prose to hit a number is the thin-content move this brief rules out. The articles in `seo-content-map.md` are the right answer — they take the informational queries, and the boards stay boards.

---

## What shipped in code this sprint

One commit, `2c8dc65`, four files:

| File | Change |
|---|---|
| `nfl.html` | Read-next block → 3 guides · `h2` promotion · `Organization`+`WebPage` schema |
| `cfb.html` | Read-next block → 3 guides · `h2` promotion (first `h2` on the page) |
| `games.html` | Read-next block → 3 guides |
| `no-vig-calculator.html` | Read-next block → 3 guides |

No new pages. No keyword pages. No sports added. No design changes.

---

## The daily loop

Six actions, about 45 minutes, same order every day.

```
08:30  VERIFY   open the ESPN board for today's sport. Copy the number from
                there, not from any document. If it moved, use the new one.
                If the game moved, drop the piece.
09:00  SITE     one dated line or section on the page being promoted
09:30  X        one post, the day's number, one link
10:30  REDDIT   one teaching post or comment, no link in the opening
11:30  IG       one carousel, text-first, original
12:00  LINK     one internal link added somewhere
17:00  MEASURE  fill one row of the dashboard
```

**Skip a piece rather than rush it.** A day with only the X post and the measurement row is a good day. A day with a number nobody checked is a bad one.

---

## The seven days

| Day | Sport | Page promoted | Article | Verified hook |
|---|---|---|---|---|
| **Thu 9/17** | NFL | `/no-vig-calculator` | — | BUF −5.5, total 54.5 |
| **Fri 9/18** | CFB | `/cfb` | *Why big spreads have no moneyline* | ORE −57.5, o/u 67.5, **no ML posted** |
| **Sat 9/19** | UFC | `/ufc-331-odds` | — | UFC 331, first bout 5:00 PM ET, 12 bouts |
| **Sun 9/20** | NFL | `/football-line-movement` | *Key numbers 3 and 7* | **2 of 16** Week 2 spreads sit exactly on 7; **none** on 3 |
| **Mon 9/21** | NFL | `/break-even-calculator` | *What −110 actually requires* | LAR −7, total 48.5 |
| **Tue 9/22** | MLB | `/mlb-playoffs` | *Series prices vs game prices* | Wild Card starts Tue Sep 29 |
| **Wed 9/23** | Tools | `/parlay-calculator` | *Why parlays pay so much* | pure arithmetic |

Every hook was read from the live ESPN feed at **3:22 PM ET, Sep 17** and is marked `[VERIFY BEFORE POSTING]` in the kit, because prices move.

---

## Deliberately not in this sprint

- **No NBA, NHL, PGA or college basketball.** `/pga` stays indexed — the Biltmore Championship is live Sep 17–20 and the page is accurate — but gains no new inbound links, because linking to it would be making the site look larger rather than better.
- **No daily picks**, in any form, on any channel.
- **No new pages beyond the seven articles**, and those only if the loop is actually running.
- **No X automation.** Every post is sent by hand.
- **No paid tools.** Cloudflare Web Analytics, Search Console, Beehiiv — all free, all already connected.

---

## When we stop redesigning

**Wednesday Sep 23, at the 5 PM measurement.** From that point the site is judged by the dashboard, not by page-level opinion.

1. **No design or copy change** to a priority page unless the dashboard shows a specific problem — traffic with no onward clicks, or clicks with no signups.
2. **No new page** unless an existing page proved the format works.
3. The only work that continues unconditionally is the **daily loop** and **verification**.

If the loop ran seven days and the thresholds in `measurement-dashboard.md` are not met, the answer is not a redesign. It is a different channel or a different topic — and the dashboard will say which.

---

# Per-day execution sheet

Every day: **destination · audience question · target URL · CTA · same-day facts · X · Reddit · Instagram · internal link · UTM · success metric.**
Full copy for X, Reddit and Instagram is in `social-distribution-kit.md`; slide layouts and the pre-publish checklist are in `SOCIAL-PUBLISHING-KIT.md`.

**The experiment starts the day the release is live, not before.** Two of the seven destinations are absent from the live sitemap.

### Day 1 — Thu Sep 17 · NFL
- **Question** "What does the price next to the spread actually cost me?"
- **URL** `/no-vig-calculator` · **CTA** Strip the vig on any market yourself
- **Verify** BUF −5.5, total 54.5 **[VERIFY]**
- **Internal link** `/nfl` intro → `/no-vig-calculator` on the words "true price"
- **UTM** `…/no-vig-calculator?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d1-novig`
- **Metric** ≥1 click from `x.com` · **plus:** Search Console baseline recorded, sitemap resubmitted

### Day 2 — Fri Sep 18 · College football
- **Question** "Why does this blowout have no moneyline?"
- **URL** `/cfb` · **CTA** Friday's full board, read live
- **Verify** ORE −57.5, total 67.5, no moneyline posted **[VERIFY]**
- **Internal link** `/cfb` board header → `/football-line-movement`
- **UTM** `…/cfb?…&utm_content=d2-nomoneyline`
- **Metric** `/cfb` Friday views ≥ last Friday

### Day 3 — Sat Sep 19 · UFC
- **Question** "What is this fight price actually claiming?"
- **URL** `/ufc-331-odds` · **CTA** Every fight, priced the same way
- **Verify** both main-event moneylines, twice; main event unchanged **[VERIFY]**
- **Internal link** `/ufc` archive → `/ufc-331-odds`
- **UTM** `…/ufc-331-odds?…&utm_content=d3-ufc331`
- **Metric** `/ufc-331-odds` is the day's top page

### Day 4 — Sun Sep 20 · NFL
- **Question** "Why do people care so much about 3 and 7?"
- **URL** `/football-line-movement` · **CTA** Why the numbers move
- **Verify** **recount the board** — 2 of 16 on 7, 0 on 3, 10 between **[VERIFY]**
- **Internal link** `/nfl` → `/football-line-movement#key-numbers`
- **UTM** `…/football-line-movement?…&utm_content=d4-keynumbers`
- **Metric** ≥1 visit with a `reddit.com` referrer

### Day 5 — Mon Sep 21 · NFL
- **Question** "How often do I actually need to be right?"
- **URL** `/break-even-calculator` · **CTA** Check your own rate against your prices
- **Verify** LAR −7, total 48.5 **[VERIFY]**
- **Internal link** `/glossary` "break-even" and "vig" → their calculators
- **UTM** `…/break-even-calculator?…&utm_content=d5-breakeven`
- **Metric** weekly Search Console read — any impression on a new guide

### Day 6 — Tue Sep 22 · MLB
- **Question** "Why is this series priced so close when the teams aren't?"
- **URL** `/mlb-playoffs` · **CTA** How postseason markets are built
- **Verify** Wild Card still Tue Sep 29. **No team names** **[VERIFY]**
- **Internal link** `/learn` explainer list → `/mlb-playoffs`
- **UTM** `…/mlb-playoffs?…&utm_content=d6-series`
- **Metric** ≥1 new subscriber vs the baseline of 3

### Day 7 — Wed Sep 23 · Tools
- **Question** "Why do parlays pay so much and hit so rarely?"
- **URL** `/parlay-calculator` · **CTA** Run your own
- **Verify** nothing external; confirm the calculator returns +596
- **Internal link** `/tools` ↔ each calculator, made uniform
- **UTM** `…/parlay-calculator?…&utm_content=d7-parlay`
- **Metric** scorecard complete, next week's top two named

### If a fact will not verify
Post the **evergreen version** in `social-distribution-kit.md`, or skip the day. Days 1, 5 and 7 are pure arithmetic and always safe. **Never invent a schedule, odds, injury or matchup.**

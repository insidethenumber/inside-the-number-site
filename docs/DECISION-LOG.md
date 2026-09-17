# Decision log — the 30-day freeze

**Opened:** Thu Sep 17, 2026 · **Expires:** Sat Oct 17, 2026
**Purpose:** stop the churn. This project has had seven consecutive audit-and-polish cycles and zero distribution cycles.

The wedge, from `PRODUCT-PROOF-REPORT.md`: *explain the number, show the move, remove the vig, make every step checkable — and never claim to know who bet.*

---

## KEEP — directly supports the wedge

| Asset | Why it stays |
|---|---|
| **The three guides** — `/football-line-movement`, `/mlb-playoffs`, `/ufc-331-odds` | 1,900–2,100 words, `Article`+`FAQPage` schema, one search intent each. The only pages capable of ranking |
| **`/no-vig-calculator`** | Commodity category, but it is the proof mechanism — every claim on the site is re-checkable here in under a minute |
| **The live boards** — `/nfl`, `/cfb`, `/games` | Open vs current on every row, read from a feed, nothing hand-typed. This is "show the move" |
| **The Morning Board + its promise** | Specific, honest, no picks. The only conversion event that exists |
| **The refusal to say "sharp money"** | §4 of the proof report. This is the differentiation. It is a *feature*, and it must be defended in copy |
| **Anonymity** | No persona to maintain, no credibility to fake, no record to grade |
| **Board freshness guard + dynamic stamp** | The site tells a visitor when it is stale rather than pretending |
| **10 calculators, all verified** | The reference layer the guides link into |

---

## FREEZE — good enough. Do not touch for 30 days.

| Asset | State | The temptation to resist |
|---|---|---|
| **Site-wide navigation** (`96a8fa2`) | 8 items, identical on all 35 pages | Rearranging it again. It has been "fixed" three times |
| **Mobile Home/section context row** (`3ff5eee` + M25) | On all 33 interior pages | — |
| **Homepage hero, CTA, stat strip** | H1 states the proposition, one CTA matching the signup heading, four distinct stat cells | Rewriting the H1 a fourth time |
| **Visual system** — colors, type, dark theme | Consistent, accessible, AA contrast throughout | "Refreshing" it |
| **All 10 calculator pages** | Correct math, correct titles, context rows, signup forms | Redesigning calculator layouts |
| **`/learn`, `/glossary`, the 4 explainers** | Accurate, linked, indexed | — |
| **`/parlay`, `/dfs`** | `noindex,follow`, reachable, not competing | Reviving them |
| **`/pga`** | Indexed, accurate, event live Sep 17–20, deliberately unlinked | Building a PGA section |
| **Page word counts on `/nfl` and `/cfb`** | 484 and 334 words | Padding them to hit a number. That is the thin-content move |

---

## FIX NOW — blocks discovery, trust, navigation, signup or measurement

Only these. Everything else waits.

| # | Blocks | Issue | Status |
|---|---|---|---|
| 1 | **Discovery** | Live sitemap has 28 entries, omits all three guides. Google has never been told they exist | **BLOCKED — needs owner push.** Fixed in the release, undeployed |
| 2 | **Discovery** | Internal equity pointed at `/games` and `/no-vig-calculator` (24, 23) while guides had 2, 4, 5 | ✅ **DONE** `2c8dc65` — now 5, 7, 8 |
| 3 | **Discovery** | `/cfb` had zero `<h2>`; `/nfl` had no `Organization` schema | ✅ **DONE** `2c8dc65` |
| 4 | **Trust** | Beehiiv publication description still reads *"one free pick every morning"* while the homepage says "0 — Picks. Ever." | **BLOCKED — owner only.** Copy supplied |
| 5 | **Trust** | Homepage board stamp read a day stale | ✅ **DONE** M26 — now written from the live feed, with the guard retained |
| 6 | **Measurement** | Chuck's own visits counted in every number | **BLOCKED — owner.** Open each browser once with `?itn_internal=1` |
| 7 | **Measurement** | No UTM convention, so no channel is attributable | ✅ **DONE** — `measurement-dashboard.md` |
| 8 | **Signup** | `/odds-converter` has no email capture at all — 2.5-screen page, form would sit above the fold | **OPEN** — smallest remaining justified fix |

---

## The 30-day rule

**No visual redesign** of any frozen asset unless a test shows a conversion or usability problem. "Test" means a number in `measurement-dashboard.md`, not an opinion formed while looking at the page.

**No new sport section** — NBA, NHL, PGA, college basketball — unless there is a verified search or audience reason. "Verified" means Search Console impressions on an existing related page, or a repeated audience request. Wanting the site to look bigger is not a reason.

**No new page** unless it is one of the seven in `seo-content-map.md`, and only on a day the distribution loop actually ran.

**No monetisation work** before the 30-day North Star is hit. Per the proof report, 30-day revenue is $0 in every scenario.

### What overrides the freeze

Exactly three things:
1. A **factual error** on a live page.
2. A **broken route, form or feed**.
3. A **measurement finding** that names a specific page and a specific failure.

### How this log gets closed

**Oct 17, 2026.** Against the North Star: 50 organic visits to the three guides, and 10 subscribers who did not arrive via the homepage. Met → the freeze lifts and the next cycle is volume. Not met → §11 of the proof report, not another redesign.


---

## M28 entry — Thu Sep 17, 2026 (revalidation gate)

**What happened.** Production advanced to `dd29053` while the release sat unpushed. The guarded deploy script refused to merge and exited. That refusal was correct and was not overridden.

**What was done.** Rebased onto `dd29053`, zero conflicts, `data/` byte-identical to production, full QA re-run against the new base, eight routes rendered at 390px and 1280px from SHA-verified committed bytes.

**Two fixes admitted under the freeze**, both inside the "correctness, not redesign" exception already written into this log:

| Fix | Why it is not scope creep |
|---|---|
| `/ufc-331-odds` title 62 → 58 chars | An indexed title being truncated by Google is a defect in a shipped SEO change, not a new idea |
| Seven British spellings across 34 pages | A standing instruction ("Use English US only"), previously applied to only five files |

**One finding logged and deliberately NOT fixed.** Eight pages — `/cfb`, `/nfl`, `/games`, `/pga`, `/ufc`, `/thanks`, `/confirm`, `/post` — carry the responsible-gambling notice in their footer prose ("For entertainment purposes only… Please gamble responsibly") but do **not** link to `/responsible-gambling`, which the other 21 pages do. This is a real consistency gap. It is not in the stated release contents, the pages are compliant as they stand, and the freeze exists precisely to stop "while we're in there" edits. **Decision: defer to the next release. Not an emergency, not silently fixed.**

**The freeze end date does not move.** Still **Sat Oct 17, 2026**. Revalidating a blocked release is not a new polish cycle and does not buy more polishing time.

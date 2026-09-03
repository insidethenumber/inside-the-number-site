# Marketing punch list — Inside the Number

**This is the list. Every Monday morning the `itn-monday-growth-report` task
reads it and sends Chuck the open items plus last week's numbers, so nothing
here gets forgotten.** Sources: `docs/inputs/` (Chuck's external strategy
docs), FRANCHISES.md, NORTH_STAR.md, and the Sep 2 investigation.

Status: ☐ open · ◐ in progress · ☑ done · ✗ won't do (with reason)
Owner: **C** = Claude, **CW** = Chuck

---

## 0. Gate — before X turns back on

| | Item | Owner | Source |
|---|---|---|---|
| ☐ | Draft the new X ruleset for Chuck's approval (voice, franchises, image rule, cadence, what is banned) | C | Chuck 9/2 |
| ☐ | Chuck approves the ruleset | CW | Chuck 9/2 |
| ☐ | Re-enable `itn-x-engagement-hourly` AND restore the cron in `x-posts.yml` (both, or posts silently never resume) | C | — |

## 1. Identity and entity (Google + brand)

| | Item | Owner | Source |
|---|---|---|---|
| ☑ | Site → X link on every page (179 pages, `rel="me"`) | C | input A |
| ☑ | X bio rewritten | C | input A |
| ☑ | Newsletter carries "Follow on X — @thenumberdesk" every issue | C | input A |
| ☑ | Name consistency locked: Inside the Number / @thenumberdesk / insidethenumber.com; ITN = mark only | C | input A |
| ☐ | `sameAs` in the site's Organization schema pointing to the X profile (and Beehiiv) | C | input B §12 |
| ☐ | Beehiiv web profile → X link (in the website builder footer) | C | input A |
| ☐ | GitHub org profile → site + X | C | input A |
| ☐ | Check Google for `site:x.com/thenumberdesk` weekly until it indexes | C | input A |

## 2. X — the awareness engine (paused)

| | Item | Owner | Source |
|---|---|---|---|
| ☑ | Six franchises defined (FRANCHISES.md) | C | input A |
| ☑ | Image required on every original; media upload via API | C | Chuck 9/2 |
| ☑ | Card library: split, board, matchup, bignumber, trend | C | — |
| ☐ | Run `cache-logos.yml` once so team logos appear on cards | C | — |
| ☐ | Cache Anton / Barlow Condensed via CI so cards use the brand face | C | — |
| ☐ | Franchise card templates with the name baked in — target 10-15 | C | input A §7, input B §3 |
| ☐ | Monitor list: 200-500 relevant accounts in buckets (NFL, CFB, MLB, NBA, DFS, betting, media, analytics, journalists, influencers, industry) | C | input B §6 |
| ☐ | Real-time reaction protocol: news → what it did to the number, same hour | C | input B §A, §18 |
| ☐ | Weekly "viral data story" hunt (one shareable finding a week) | C | input B §17 |
| ☐ | Every post passes the "why would someone stop scrolling?" test — write it into the task | C | input B §26 |
| ✗ | Ticket/money splits in posts | — | we do not have the data |
| ✗ | "ITN EDGE" / model-vs-market edge posts | — | fabricated; model has no edge; record 12-18 |

## 3. Reddit — the second engine

| | Item | Owner | Source |
|---|---|---|---|
| ☑ | Ammo pack rewritten for u/kceza1; dead tasks paused | C | Chuck 9/2 |
| ☐ | Chuck posts from u/kceza1, 90% contribution / ≤10% promotion | CW | input B §7 |
| ☐ | One original data project post per month ("I tracked every MLB total move this season…") — uses only data we actually have (open/close) | C | input B §8 |
| ☐ | Subreddit-specific versions; never the same post in five subs | C | input B §7 |

## 4. Search — the compounding engine

| | Item | Owner | Source |
|---|---|---|---|
| ☑ | Game pages retitled "Prediction, Picks & Odds" with projection + FAQ schema (152) | C | Sep 2 |
| ☑ | 10 standalone calculator pages | C | input B §11 |
| ☐ | Game pages: add opening line, movement, injuries, weather, timestamp (the input B §12 spec) | C | input B §12 |
| ☐ | Calculator pages: answer the query in the first screen, then introduce ITN | C | input B §11 |
| ☐ | Weekly GSC check: which query family is climbing; double down | C | NORTH_STAR |

## 5. Email — the owned audience

| | Item | Owner | Source |
|---|---|---|---|
| ☑ | Newsletter named "the Morning Board"; site CTA rewritten | C | input B §13 |
| ☐ | Morning Board format: 1 free pick · biggest overnight move · one number to know · one market observation · today's slate | C | input B §13 |
| ☐ | Lead magnets: No-Vig Cheat Sheet, How to Read Line Movement, EV Cheat Sheet, Bankroll Guide, NFL Numbers Guide — each a separate entry point | C | input B §14 |
| ☐ | Referral program (Beehiiv has one built in): 3 → perk, 5 → 1 mo Pro, 10 → 3 mo Pro | C/CW | input B §20 |
| ☐ | Chuck's own network: 20 real people this week | CW | Sep 2 |

## 6. Video — the breakout channel

| | Item | Owner | Source |
|---|---|---|---|
| ☐ | Decide: 20-45s shorts, no face needed (charts, text animation, voiceover) | CW | input B §10 |
| ☐ | If yes: one per day, "the line just moved two points, here's why" | C/CW | input B §10 |
| ☐ | Instagram: repurpose best X cards as carousels | C | input B §9 |

## 7. Product and money

| | Item | Owner | Source |
|---|---|---|---|
| ☐ | Affiliate: BetMGM one attempt (Chuck: login step) | CW | pack |
| ✗ | Caesars affiliate form — broken on their end, do not retry | — | DECISIONS |
| ☐ | PrizePicks / Underdog: awaiting reply (applied Sep 1) | — | pack |
| ☐ | Fanatics via Impact — untried | C | pack |
| ☐ | Wire affiliate links + FTC disclosure the day a program approves | C | pack |
| ☐ | Pro: waitlist → purchasable, when there are subscribers (Chuck's call on timing) | CW | input B §15 |
| ☐ | Stripe on Beehiiv | CW | — |
| ✗ | Public ITN RECORD with W/L/ROI/CLV | — | retired Aug 22 (Chuck); record is losing; input B §16 wants it — revisit only if Chuck reverses |
| ✗ | Ads on the site now | — | input B §19 agrees: traffic first |

## 8. Measurement

| | Item | Owner | Source |
|---|---|---|---|
| ☐ | Monday ITN GROWTH REPORT: impressions, profile visits, site clicks, uniques, signups, conversion, open rate, tool usage, organic clicks, Reddit referrals | C | input B §24 |
| ☐ | 30-day directional targets on the report: email subs, monthly impressions, sessions, posts over 10K, one over 50K, recurring series established | C | input B §25 |

## 9. Standing rules that came out of Sep 2

- No fabricated numbers, ever. Splits, edges, "sharps" — banned.
- A form that renders is not a form that works. Verify to submit or call it UNVERIFIED.
- Every session logged to `docs/sessions/`. Every decision to `docs/DECISIONS.md`.
- Every external strategy doc filed to `docs/inputs/` and mined into this list.

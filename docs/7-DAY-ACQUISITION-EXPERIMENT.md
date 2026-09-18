# 7-day acquisition proof sprint

**Window:** Fri Sep 18 → Thu Sep 24, 2026 · **Judged:** Thu Sep 24, 5:00 PM CT
**Baseline:** `docs/ACQUISITION-BASELINE.md` · **Copy:** `docs/TRAFFIC-CONTENT-PACK.md`
**Cost:** $0. Search Console, Cloudflare Web Analytics and Beehiiv are all free tiers already in use. Nothing new is purchased.

**The question this answers, and nothing else:** *can this site, as it stands today, earn organic traffic and a subscriber from somewhere other than the homepage?* Not "is the content good." Not "is the design right." Those are settled and frozen.

> **Nothing is published to X, Reddit or Instagram without Chuck's explicit go-ahead, post by post.** Every draft in the content pack is a draft.

---

## Ground rules that do not move

1. **Re-verify every number before it goes out.** Lines move — in the ten hours of this session, `MIA @ WAKE` went from MIA −21 / 56.5 to **MIA −20.5 / 55.5**. A post with yesterday's number is the exact failure this product exists to criticize.
2. **No picks, no leans, no "I like".** No lock, no guarantee, no record, no profit claim, no fake urgency.
3. **Never say "sharp money".** From outside a sportsbook nobody can see who bet. That refusal is the product.
4. **Cite the book and the read time** on any live price.
5. **Reddit: teach first, no link in the opening comment.** Post inside the daily discussion thread, not as a standalone. Answer with the link only if asked.
6. **No licensed logos, player photos or broadcast stills.** Type and numbers only.

---

## Daily actions

Each day: **one Search Console action, one X draft, one Reddit draft, one Instagram card brief, one measurement read.** Fifteen to twenty minutes.

| Day | Target query | URL | Channel | CTA | Measurement event |
|---|---|---|---|---|---|
| **1 · Fri 9/18** | "college football odds week 3" | `/cfb` | X + Reddit + IG | Friday's full board, read live | GSC: request indexing `/cfb`. CF: visits + referrer |
| **2 · Sat 9/19** | "ufc 331 odds" | `/ufc-331-odds` | X + Reddit + IG | Every fight, vig stripped | GSC: impressions on `/ufc-331-odds`. CF: visits |
| **3 · Sun 9/20** | "nfl week 2 odds" | `/nfl` | X + Reddit + IG | Every game, the fair price | CF: visits + referrer. Beehiiv: new subs + source |
| **4 · Mon 9/21** | "why do betting lines move" | `/football-line-movement` | X + Reddit + IG | The guide behind the board | GSC: weekly read — impressions on all 3 guides |
| **5 · Tue 9/22** | "mlb playoff odds explained" | `/mlb-playoffs` | X + Reddit + IG | How a series is priced | CF: visits. Beehiiv: delta vs 3 |
| **6 · Wed 9/23** | "no vig calculator" | `/no-vig-calculator` | X + Reddit + IG | Strip the vig yourself | CF: visits. Beehiiv: form source |
| **7 · Thu 9/24** | "break even win rate betting" | `/break-even-calculator` | X + Reddit + IG | What you must hit to break even | Build the scorecard |

### The free Search Console routine

- **Tonight, once:** confirm `sitemap.xml` is submitted and shows 29 URLs discovered. If the M29 hotfix has deployed, resubmit so the crawl is re-triggered.
- **Day 1:** request indexing for `/cfb`, `/nfl`, `/mlb-playoffs`, `/ufc-331-odds`, `/football-line-movement`. Five URLs, roughly two minutes total.
- **Day 4:** one weekly read — impressions, clicks and average position for the three guides. This is the only search number that matters this week.
- Do not request indexing repeatedly. It does not speed anything up.

---

## What gets recorded

Fill one row per day. Six fields, nothing else.

| Date | Page | Channel | Visits | GSC impr. | GSC clicks | New subs | Source | Notes |
|---|---|---|---|---|---|---|---|---|
| Fri 9/18 | `/cfb` | | | | | | | |
| Sat 9/19 | `/ufc-331-odds` | | | | | | | biggest event of the week |
| Sun 9/20 | `/nfl` | | | | | | | |
| Mon 9/21 | `/football-line-movement` | | | | | | | weekly GSC read |
| Tue 9/22 | `/mlb-playoffs` | | | | | | | |
| Wed 9/23 | `/no-vig-calculator` | | | | | | | |
| Thu 9/24 | `/break-even-calculator` | | | | | | | scorecard |

**Search Console lags 2–3 days.** Days 1–2 will show nothing in search. That is the tool, not the result.

**Exclude your own visits.** Open the site once with `?itn_internal=1` in every browser you use. This has been raised in nine audits and remains the single largest source of error in a dataset this small.

---

## Success thresholds — four, binary, deliberately small

| # | Passes when | Why this one |
|---|---|---|
| 1 | **One subscriber from a non-homepage source** — Beehiiv Acquisition Details shows any source that is not the homepage embed | All 10 subscribers ever came through the homepage. If content pages cannot convert, the content strategy is wrong, and a week is a cheap way to learn it |
| 2 | **One Search Console impression on `/football-line-movement`, `/mlb-playoffs` or `/ufc-331-odds`** | Tests whether the guides are indexed at all |
| 3 | **At least one visit from each of X, Reddit and Instagram** in Cloudflare referrers | Proves each channel can move one human. Three visits is a pass |
| 4 | **A ranked table of the seven pages by visits** | The only output that changes what happens next week |

**Not goals this week:** a subscriber count, a traffic target, a conversion rate, a follower count, an open rate. With three subscribers, each of those is noise wearing a number's clothes.

---

## What 7 days can and cannot prove

**Can be proven:**
- Whether a page other than the homepage can convert a single subscriber.
- Whether the three guides are indexed and being served at all.
- Which of X, Reddit and Instagram moves a human to the site — and which moves none.
- Relative interest across seven pages, ranked.

**Cannot be proven, and must not be claimed:**
- Any conversion *rate*. Three subscribers cannot support a percentage.
- Whether the content is "good". One week of data on pages nobody has linked to measures distribution, not quality.
- Anything about SEO ranking. New pages do not rank in seven days; impressions are the ceiling of what is observable.
- Whether Saturday's UFC spike generalizes. One event is one data point, and `/ufc-331-odds` goes stale the moment the card is fought, while the evergreen guides will still be earning impressions in December.

---

## Stop / pivot rule — decided now, in advance

Judged **Thu Sep 24, 5:00 PM CT**, against the four thresholds.

| Outcome | Rule |
|---|---|
| **3 or 4 pass** | The channel works. Run it again for 3 more weeks, same cadence, no redesign. Add the four unbuilt articles in `seo-content-map.md`, one per week |
| **2 pass** | Keep only the channels that produced a visit. Drop the others outright. Re-run one week |
| **0 or 1 pass** | **Stop publishing.** The distribution hypothesis is disproven for this format. Do not respond by rebuilding the site — that is the trap this project has fallen into seven times. Either commit to a channel with a human audience (one real community, participating for a month without links) or accept the site as a portfolio piece and stop spending on it |

**The freeze holds regardless of outcome.** No redesign before **Oct 17, 2026**. A bad result is information about distribution, not a mandate to move buttons.

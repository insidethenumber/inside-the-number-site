# Product proof report

**Date:** Thursday, September 17, 2026
**Evidence:** the live site, the repository at `origin/main` `dd29053`, the Beehiiv API, and competitor SERPs checked today.
**Assumptions are labelled.** Nothing here claims profitability.

---

## 1 · What Inside the Number actually is today

Not what it aspires to be. What is on the server right now:

| | Evidence |
|---|---|
| **35 HTML pages**, 29 indexable | repo count, sitemap |
| **10 working calculators** | odds converter, no-vig, vig/hold, break-even, EV, edge, Kelly, parlay, hedge, bankroll drawdown — all verified against known values |
| **3 live boards** reading ESPN's public feed | `/nfl`, `/cfb`, `/games` — open vs current on every row, nothing hand-typed |
| **3 long guides**, 1,900–2,100 words, `Article`+`FAQPage` schema | `/football-line-movement`, `/mlb-playoffs`, `/ufc-331-odds` |
| **1 free newsletter**, double opt-in | the Morning Board, Beehiiv |
| **3 active subscribers** | 10 ever, **7 churned**, 0 new in 7 days |
| **$0 revenue**, ever | Beehiiv earnings |
| **0 social posts** published by the current strategy | — |

**It is a small, technically sound, entirely anonymous betting-math reference site with a newsletter nobody has found yet.** The engineering is real. The audience does not exist.

---

## 2 · The first realistic audience

Not "sports bettors." That is 30 million people and every one of them is already served.

**The person who has just started asking why the number is what it is.** Specifically:

- They bet occasionally, recreationally, and have done for under two years.
- They have noticed that −110 appears everywhere and do not know why.
- They have seen a line move and been told "sharp money" and found that unsatisfying.
- They are searching phrases like *"what does −238 mean"*, *"why is there no moneyline"*, *"break even win rate"*.
- **They are not looking for a pick.** A person looking for a pick bounces off this site in four seconds.

**[ASSUMPTION]** This audience exists in meaningful numbers. Evidence for: the query patterns are informational and the competitor set is large enough to imply demand. Evidence against: **we have zero first-party data**, because no guide page has ever produced a subscriber.

---

## 3 · Honest competitive position

Checked today. This is the uncomfortable part.

| Competitor | What they do | Where ITN stands |
|---|---|---|
| **Action Network** | Odds, picks, public betting %, PRO tools, huge editorial staff | ITN cannot compete on scope, data licensing or authority. Not close |
| **Covers / OddsShark** | Odds comparison, consensus, forums, 20+ years of domain authority | ITN cannot compete on rankings for head terms |
| **RotoWire** | Projections, DFS, injury feeds, subscription product | Different product entirely |
| **BetMGM content** | Operator-funded, distribution-first | ITN has no budget and no operator relationship |
| **Unabated, betstamp, The Rundown, OddsGPT, BettorEdge, OddsOrca, eGamingHQ, Bettor Ed, Bet Hero** | **Free no-vig calculators** — at least nine of them | **The calculator is not a wedge. It is a commodity.** Nine-plus competitors have one, several with far better domain authority |
| **BetQL, OddsTrader, Bet Better, ProComputerGambler, PropsBot** | **Line-movement trackers** — open vs current, "steam", "sharp money tracker", "where the money's going" | **The tracker is not a wedge either.** But look at the framing |

### The two findings that matter

**Finding 1 — the calculator category is saturated.** `/no-vig-calculator` is ITN's second-most-linked page and it competes against nine free calculators from stronger domains. Ranking for "no vig calculator" is not a realistic 90-day goal. *Anyone planning around it is planning around a loss.*

**Finding 2 — and this is the opening.** Nearly every line-movement product in that list sells the same narrative: *"sharp money"*, *"where the money's going"*, *"steam"*, *"reverse line movement"*. That framing implies the product can see who is betting. **From outside a sportsbook, nobody can.** It is an unfalsifiable claim used to make a data feed feel like inside information.

ITN already refuses to make it. `/football-line-movement` says so explicitly:

> "You will see every move attributed to 'sharp money.' We do not write it that way, because from outside a sportsbook nobody can see it."

That refusal is the only genuinely differentiated thing this product has.

---

## 4 · The wedge

**Explain the number, show the move, remove the vig, and make every step checkable.**

Four properties, all currently true, none of which the competitor set combines:

1. **Every number is derived, not asserted.** Boards read from a public feed; open vs current is shown on every row.
2. **The arithmetic is exposed and reproducible.** Ten calculators; a reader can redo any claim in under a minute.
3. **No pick, no record, no confidence rating.** Nothing to grade, nothing to fake.
4. **It says what it cannot know.** No sharp money, no insider framing, no implied edge.

Nobody wins a category by being the tenth calculator. **A small anonymous site can win a narrow one by being the source that shows its work and admits its limits** — because the large players structurally cannot. Their business model requires the mystique.

---

## 5 · Why a stranger visits once

One reason only, and it is a search reason: **they typed a specific confused question and a page answered it directly.**

*"Why does this game have no moneyline?"* · *"What does −238 actually mean?"* · *"How often do I need to win at −110?"*

They do **not** visit for the board — ESPN, Covers and their sportsbook already show it, faster and with more books.

## 6 · Why they return

Honestly: **most will not**, and planning otherwise is a mistake.

The realistic return trigger is **seasonal recurrence of the same confusion** — the reader who learned about key numbers in September comes back in January when the playoff spreads land on 3 again. That is a long loop and a weak one.

The stronger return mechanism is the newsletter, which is why step 3 matters more than step 4.

## 7 · Why they subscribe to the Morning Board

The current promise is good and specific:

> "The Morning Board reads the market out loud: what moved overnight, which numbers are sitting on 3 and 7, and the true price under each one. Plus the No-Vig Cheat Sheet when you join. No credit card. No spam."

That earns an email **from someone who already found the explanation useful.** It will not earn one from a cold visitor, which is why every guide page must teach first and ask second.

**[EVIDENCE AGAINST]** All 10 subscribers ever acquired came from the homepage. **No guide page has ever converted anyone.** Until that changes once, this section is a hypothesis.

---

## 8 · Revenue, plainly

### What can plausibly produce revenue

| Horizon | Path | Realistic scale | Conditions |
|---|---|---|---|
| **30 days** | **Nothing.** | **$0** | With 3 subscribers and no traffic baseline there is nothing to monetise. Attempting it now costs trust and earns cents |
| **60 days** | **Sportsbook affiliate links**, placed only where genuinely useful | **$0–50** | Requires 500+ monthly visitors, a licensed-state disclosure, and a placement that does not contradict "we don't tell you what to bet". `bet365` and Underdog applications already exist |
| **60 days** | **Beehiiv recommendation network** — already enabled | **$0–30** | Requires a subscriber base worth recommending to. Below ~100 it pays nothing |
| **90 days** | **One paid tier**, $7.99–$12.99/mo | **$0–150** | Requires **≥300 free subscribers** and a paid product that is not just "the same thing sooner" |
| **90 days** | **Newsletter sponsorship**, one slot | **$50–200/send** | Requires ~1,000 subscribers and an open rate measured on a real sample |

### What cannot realistically produce revenue yet

- **A paid tier now.** 3 subscribers. A paywall would be theatre.
- **Picks or a premium pick product.** The entire brand is built on refusing this. Reversing it destroys the only differentiation identified in §4.
- **Display advertising.** Needs traffic orders of magnitude beyond current.
- **A course or ebook.** Needs an audience that trusts the author, and the author is deliberately anonymous.
- **DFS tooling.** `/dfs` is already paused and noindexed.

**The honest read: this is a 90-day-to-first-dollar business at best, and only if traffic arrives first.** Every hour spent on monetisation before traffic is an hour spent on the wrong problem.

---

## 9 · The three biggest reasons traffic and subscribers are low

### Reason 1 — the site is not discoverable *(mechanical, fixable, unfixed)*

The live `sitemap.xml` has **28 entries and omits all three guides**. The pages built to rank have never been declared to Google. The fix is written and tested; it is not deployed. **This is the binding constraint.**

### Reason 2 — internal equity pointed at the wrong pages *(fixed this sprint)*

Counting body links only, the three rankable guides had **2, 4 and 5** inbound links while `/games` and `/no-vig-calculator` had **24 and 23**. Ten calculators linked only to those two. Now 5, 7 and 8.

### Reason 3 — nothing has ever been distributed

**Zero** social posts published under the current strategy. Zero Reddit comments. The newsletter has sent to three people. A site with no inbound links, no social presence and no sitemap entry is not underperforming — it is unlaunched.

**Note the ordering.** None of these three is a design problem. None is fixed by editing a page.

---

## 10 · Evidence that would prove this is working

In order of how much each would tell us:

1. **One subscriber from a non-homepage page.** Has never happened. Proves the guide→signup path exists at all.
2. **Search Console impressions on a guide, then a click.** Proves the content matches a real query.
3. **A returning visitor on a different sport.** Proves the topic transfers, not just the page.
4. **A Reddit comment that gets upvoted without a link.** Proves the voice works where the audience already is.
5. **≥10 two-page sessions in a week.** Proves the "Read next" fix works.

## 11 · Evidence that would say pivot or stop

- **Traffic arrives and nobody subscribes** — two consecutive weeks of >200 visits with 0 signups. The offer is wrong, not the traffic.
- **Guides get impressions but no clicks** — titles and snippets are not competitive; the head terms are unwinnable and the long tail needs rebuilding.
- **Nothing ranks in 90 days with the sitemap live** — domain authority is the binding constraint, and the answer is distribution, not more pages.
- **Chuck stops running the daily loop.** The honest failure mode. This product needs ~45 minutes a day of human distribution for months. If that is not sustainable, the site should become a static reference and the newsletter should stop.

---

## Positioning statement

> **Inside the Number is the betting-market site that shows its work and admits what it cannot know: every number is read from a public feed, every claim can be re-checked in under a minute, and nobody here will ever tell you where the sharp money went — because from outside a sportsbook, nobody can see it.**

## 30-day North Star

> **50 organic search visits to the three guide pages, and 10 newsletter subscribers who did not arrive via the homepage.**

One is discovery, one is conversion, both are currently zero, and neither can be faked. If both are met by **October 17, 2026**, the wedge is real and the next 30 days are about volume. If neither is met, §11 applies.

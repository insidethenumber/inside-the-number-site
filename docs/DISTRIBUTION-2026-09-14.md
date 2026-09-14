# Distribution: where the first 100 readers actually come from
**Written Mon Sep 14, 2026 — after six weeks.**

## The number that matters

Six weeks in: **3 subscribers.** Roughly **ten real human visitors a day** —
Cloudflare reports 250–355 "uniques", but filtered to real browsers requesting
HTML it collapses to single digits and low teens. The rest is bots and
vulnerability scanners.

The site is not broken. **It is unvisited.** Three subscribers from ten daily
visitors is not a bad conversion rate — it is a normal conversion rate applied
to almost no traffic. Every hour spent on the product is an hour spent widening
a funnel that nothing is entering.

That reframes six weeks of work. We have been building, not distributing.

## What the channels have actually produced

| Channel | Effort spent | Result | Read |
|---|---|---|---|
| **Golf / PGA search** | Almost none | ~141 impressions/mo, unprompted | **The only unforced demand we have** |
| **X** | Very high — 704 posts | 61 followers | ~0.09 followers per post. Dead at this size |
| **Newsletter** | High | 3 subs, 100% open | The product, not a channel |
| **Reddit** | Almost none | — | Untested, and the best structural fit |
| **Instagram** | Moderate | — | Too early to judge; just automated today |

Two honest conclusions:

**X is not working and more X will not fix it.** 704 posts produced 61
followers. The platform does not distribute small accounts to strangers any
more; it distributes replies into existing conversations. The daily posting
cadence is the single largest consumer of effort here and the clearest
negative-return activity we have.

**Golf is the tell.** 141 impressions a month arrived with no promotion, no
backlinks, no posting — purely because the pages exist and answer a question
people type into Google. That is the only place the market has volunteered
anything. It is also the cheapest to expand, because it compounds and does not
need a daily human.

## The recommendation: two channels, thirty days, nothing else

**1. Golf search — build out what already works.**
People search outright odds, cut lines, and "who wins the <tournament>" every
week of the season, and they search it in volume, and our page already ranks
for some of it with zero effort. One tournament page per week, published
Monday, is a repeatable unit that accumulates. This is the compounding bet.

**2. Reddit — the only place zero followers costs nothing.**
r/sportsbook and r/dfsports judge a comment on whether it is useful, not on
follower count. A comment that carries one verified number into a live thread
reaches more strangers in an hour than a week of our X posts have. It is also
the highest-risk-of-looking-spammy channel, so: no links, comment only, be
genuinely useful, earn the right later.

**What to stop for thirty days:** the daily X posting cadence (keep replies,
kill scheduled posts), new site features, new page types, and anything that
adds surface without adding reach.

## How we will know

One metric, checked weekly: **new subscribers per week.** Not traffic, not
impressions, not followers. If thirty days of this produces fewer than ten
subscribers, the thesis is wrong and we change it rather than repeating it.

## What is blocking a sharper version of this

The hard numbers above are as-measured earlier this month. Cloudflare's API and
Search Console are both unreachable from the sandbox, so I cannot re-pull them
unattended. That belongs in CI with the tokens as repo secrets, the same fix
applied to Instagram today — then the weekly number arrives on its own instead
of depending on someone being at a desk.

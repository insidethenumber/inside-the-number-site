# Inside the Number — Marketing Plan

**Version 1.0 · September 2, 2026 · written in response to the Growth &
Marketing Directive (docs/inputs/2026-09-02-b-growth-directive.md).**

This is the plan. Not a checklist, not a summary of someone else's document —
what Inside the Number will do, on which platform, how often, with what, and
how we will know whether it worked. The directive is adopted essentially
verbatim. Where I depart from it I say so and say why, and where a departure
is really Chuck's decision I say that too.

The punch list (docs/MARKETING_PUNCHLIST.md) is the execution tracker for this
plan. The Monday growth report (itn-monday-growth-report) is its scorecard.

---

## 0. What we are, in one line

**Inside the Number watches the numbers so you don't have to.**

We are not a picks account. We are a sports-numbers, market-intelligence and
betting-analysis media brand. The tagline is THE NUMBER DOESN'T LIE and we
lean into it everywhere.

**The flywheel:**

```
Free traffic (Google · X · Reddit · Instagram · TikTok/Shorts · direct)
   ↓
Free tools + free game pages + free daily pick
   ↓
The Morning Board (free email, the daily habit)
   ↓
Daily returning visitors
   ↓
Pro subscription  +  advertising around the free audience
```

Free shows people what ITN knows. Pro shows them what ITN thinks. That is
the central message and it is already true of the site.

**What we have that most accounts do not:** the posted price on every game
across eight sports; open *and* current on moneyline, spread and total; the
de-vigged true price and break-even; ten free calculators; a stated side
every day, before kickoff, with the reasoning shown. That is the raw material
for everything below.

**What we do not have, and will not pretend to:** ticket/money splits (Action
Network's proprietary data), a model with a proven edge (ours de-vigs one book
against itself; private record 12-18), and a public track record (retired
Aug 22). Three sections of the directive lean on those. Each one gets an
honest substitute below, and one of them is flagged as Chuck's call.

---

## 1. Content philosophy — the stop-scrolling test

Adopted verbatim. Before any post goes out, the question is:

> **Why would someone stop scrolling for this?**

Acceptable answers: the number is surprising · the market just moved ·
everyone thinks one thing and the data says another · it's funny · it's
visually compelling · it's breaking · people will want to argue about it.

Unacceptable answer: "because it contains our pick."

Every post must carry at least one of: a surprising number, a strong opinion
backed by data, a visual, a timely reaction, a question that creates
discussion, information people didn't have, a compelling comparison, a reason
to click.

Priority order, always: **attention → credibility → traffic → email → revenue.**

This test is written into the X task prompt and the newsletter prompt. A post
that fails it does not go out.

---

## 2. The content engine — six franchises

The directive asks for five post types. We run six recognisable franchises
that cover all five, with the two dishonest ones replaced. Each has a fixed
name, a fixed visual template, and a slot.

| Directive type | ITN franchise | What it is | Honest? |
|---|---|---|---|
| A. Breaking / real-time data | **MARKET MOVERS** (reactive) + replies | news → what it did to the number, same hour | Yes — we have open/close |
| B. THE NUMBER | **THE NUMBER** | one number, huge, context under it | Yes |
| C. MARKET MOVERS | **MARKET MOVERS** (scheduled) | open → now, and what the move implies | Yes |
| D. "The market is wrong?" | **THE PRICE IS THE POINT** | the de-vig on one game: what the price means once the book's cut is out | Yes — substitutes for the fake-edge format |
| E. Entertainment / memes | **FOURTH QUARTER** | the joke; relatable; memes and found video; numbers optional | Yes |
| (implied by A/C) | **THE BOARD** | the slate, sorted, outlier called out — the Morning Board's front door | Yes |
| (from input A) | **WHAT THE MARKET KNOWS** | the teaching post: how to read one real market move | Yes |

Why D is replaced: "Market 47% / ITN projection 58% / 11% gap" requires a
projection with a real edge. We do not have one and publishing a fabricated
gap is the fastest way to be corrected in public and lose the only asset we
have — being right about what the number says. THE PRICE IS THE POINT
creates the same curiosity ("that's what you're actually buying?") without
inventing anything.

Full spec: FRANCHISES.md. Cadence in §5.

---

## 3. Visuals — required, and how they get made

Adopted verbatim: **text-only originals are the exception, not the rule.**
Every original carries an image. Replies may be text.

**What is built (Sep 2):**
- `scripts/cards.py` — five formats (split, board, matchup, bignumber, trend),
  ITN colours, branded footer. The `split` format is the loud one and the
  standard for THE BOARD.
- Media upload through the X API (`post_to_x.py --image`); the queue attaches
  a card automatically when one sits next to the post file.
- Team colours from the scoreboard feed (no downloads needed).

**Being built next (punch list §2):**
- Team logos and the condensed display face cached by CI (the sandbox cannot
  reach ESPN's CDN or Google Fonts; the GitHub runner can).
- One template per franchise with the franchise name baked into the layout,
  so a scroll-by reader recognises it — target 10-15 templates.
- Screenshot play: when a TV graphic or a book's line move tells the story,
  capture it and add the take (CFB Kings got 24K views doing exactly this).
- AI-generated scene images (Grok, via the X account) for FOURTH QUARTER and
  for photo-led cards, composited in the browser with real display type.
- Reaction images and memes for FOURTH QUARTER — found, not generated,
  where the joke depends on a shared reference.

**Video:** see §10. It is the biggest gap and needs a decision.

---

## 4. X — the awareness engine

**Status: paused Sep 2 until Chuck approves the rules in §4.6.**

### 4.1 Daily targets (adopted from the directive)

During major sports windows:
- **6-10 original feed posts** (up from my earlier cap of 3 — the directive
  is explicit and the earlier cap was defensive)
- **10-20 genuinely useful replies**
- **1-3 quote posts**
- **at least 1 visual- or video-heavy post**

Off-peak days (Tuesday in September, say): the low end of each range. The
sports calendar sets the number, not the clock.

One honest caveat, logged so it is not forgotten: X's distribution model
scores account reputation, and a new account posting 10 originals a day
with 33 followers risks reading as automated. The mitigation is not fewer
posts — it is the quality gate in §1 and the fact that the majority of daily
actions are replies, which is where reputation is earned.

### 4.2 The link rule

**No website link in every post.** The account has to be worth following on
its own. Links go where there is a real deeper story:

> "We tracked the entire move here →"
> "Full board and the live number →"
> "The complete breakdown →"

Roughly one in four originals carries a link. THE BOARD always does — it is
the Morning Board's front door. Replies never do.

### 4.3 Own sports conversations — the monitor list

A monitored list of 200-500 accounts in buckets, kept in the repo as
`docs/MONITOR_LIST.md` so the hourly task reads it instead of searching cold:

NFL · College Football · MLB · NBA · NHL · UFC/PGA · DFS · Betting
personalities · Sports media · Sports analytics · Journalists · Influencers ·
Sportsbook/industry.

When something happens in one of those conversations, ITN joins it quickly
**with data**. Never "check out our site". Always the number nobody is
talking about:

> "The interesting part isn't the 3.5-point move. It's where the moneyline went."

Hard rule: never spam replies. Every reply adds something useful, funny,
surprising or analytical, or it is not sent.

### 4.4 Voice

Both registers, every day — Chuck's call: "Everyone on X aren't robots, they
are humans who love memes and relatable content." Meme account with numbers.

- Reaction first, number second or absent. Take a side. Rhetorical questions
  and incomplete sentences are fine.
- Emoji as visual bullets (📈 🚨 👀 💀 🏈), two or three, as signposts.
- Sarcasm punches up — at books, prices, touts, TV narratives. Never at fans,
  players having a bad night, or anyone who lost a bet.
- Every player, team and brand name capitalised normally.
- The [stat] + [percentage] + [tidy conclusion] template is banned; it is
  what got us called "AI" on Aug 28. If a post could be generated about any
  game by swapping nouns, it is deleted.
- Hooks that work: "Everyone is talking about the spread. We're looking at
  something else." · "This number makes no sense. So we dug into it." ·
  "That's the headline. Here's the number nobody is talking about."

### 4.5 Real-time protocol — news → number

The directive's §18, made operational. The hourly task watches the monitor
list and the ESPN scoreboards for: injuries · lineup changes · pitching
changes · QB announcements · coaching news · trades · suspensions · goalie
changes · weather. When one lands, within the hour:

> opening line → current line → what that does to the implied win chance

That is an ITN specialty and it is completely honest: we can see the number
move; we do not claim to know who moved it.

### 4.6 The rules that turn X back on (for Chuck's approval)

1. Every original is one of the six franchises, with the franchise name in
   the graphic. Replies are free-form.
2. Every original carries an image. No exceptions.
3. Every post passes the stop-scrolling test (§1) before it goes out.
4. Daily targets per §4.1, flexed by the sports calendar.
5. Links per §4.2 — about one original in four, never in a reply.
6. Voice per §4.4.
7. Real-time protocol per §4.5.
8. Banned, permanently: fabricated ticket/money splits; claimed model edges;
   any public W/L, ROI or units; "sharps moved it"; promoting a game that
   has started; expanding a name from an initial without checking.
9. Every number verified this run from a live feed or a page just loaded.
10. If someone calls the account a bot: silence. Never defend.
11. Never sell in a reply.
12. No betting jokes in grief, tragedy, lawsuit or politics threads.

When Chuck approves: re-enable `itn-x-engagement-hourly` AND restore the cron
in `x-posts.yml`. Both, or posts silently never resume.

---

## 5. Weekly schedule

Adopted from the directive, mapped onto the franchises and the real calendar.
It flexes with the sports calendar; September is CFB Saturday / NFL Sunday.

| Day | Focus | Franchises |
|---|---|---|
| **Mon** | Weekend recap · weekend lessons · best/worst numbers · market movers | THE BOARD (MLB) · MARKET MOVERS · WHAT THE MARKET KNOWS · FOURTH QUARTER |
| **Tue** | Deep-dive · SEO article · tools promotion | THE BOARD · THE PRICE IS THE POINT · a calculator post ("need the true odds of -145/+130? free no-vig calculator") · FOURTH QUARTER |
| **Wed** | Data story · market analysis · short-form video | THE BOARD · THE NUMBER · the weekly viral data story (§9) · video (§10) · FOURTH QUARTER |
| **Thu** | Big CFB/NFL content · Number of the Week | THE BOARD (CFB Thursday, NFL Thursday) · THE NUMBER (of the week) · MARKET MOVERS · FOURTH QUARTER |
| **Fri** | Weekend preview · top market moves · memes · best bets | THE BOARD (weekend preview) · MARKET MOVERS · FOURTH QUARTER ×2 · the free pick |
| **Sat** | Heavy live posting · CFB · real-time odds movement | THE BOARD (CFB) · MARKET MOVERS live · replies all day · FOURTH QUARTER |
| **Sun** | NFL live numbers · breaking news · injury reactions · line movement | THE BOARD (NFL) · real-time protocol all day · "What the numbers taught us this week" (evening) |

Daily constants: THE BOARD in the morning (it is the newsletter's front
door), FOURTH QUARTER in the evening, replies throughout.

---

## 6. Reddit — the second engine

**Account:** u/kceza1 (Chuck's own, years of history, good standing). Chuck
posts. I prepare. An agent posting scheduled comments from his personal
account is exactly the pattern that got u/RockyTopEdge banned in eleven days,
and the account at risk this time is his real one.

**The ratio:** 90% contribution, 10% or less promotion, and only where the
community's rules permit it. Reddit defines repeated promotion as spam and
several communities use the 10% guideline explicitly.

**The method** (adopted verbatim): become the account that gives the best
answer. Someone asks about tonight's Dodgers game; the answer is not "ITN
likes the Dodgers" — it is "I'd stay away from the side. The interesting
number is the total. It opened 8.5 and moved to 7.5 while the favourite price
barely moved…" and then the reasoning. "I track this every morning at Inside
the Number" comes at the end, only when it fits, only where links are allowed.

**Mechanics:**
- `itn-reddit-ammo-daily` writes a daily pack for kceza1: 3-4 threads, one
  comment each, numbers verified live, subreddit-specific — never the same
  comment in two places. Opens the threads in Chrome tabs.
- Chuck's commitment: 20 minutes a day. Post, then reply to replies.
- **Monthly original data project** (directive §8) — one real analysis using
  data we actually have (open/close on every game, every day): "I tracked
  every MLB total move in September. Here's what I found." Posted as an
  original in r/sportsbook, written like someone who did the work.

Subreddits: r/sportsbook, r/CFB, r/nfl, r/baseball, r/mlb, r/MMA, r/golf,
team subs when a specific number is about them. Never format-enforced
threads (Pick of the Day) with a non-conforming comment.

---

## 7. Instagram

Visual-first, repurposed, low effort per post:
- Every THE BOARD, THE NUMBER and MARKET MOVERS card becomes a single-image
  post. Same card, square crop.
- **Carousels** for the multi-step stories: "THE MARKET MOVED 3 POINTS" →
  here's what happened → open → now → what caused it → what ITN thinks →
  insidethenumber.com. One carousel per notable move.
- FOURTH QUARTER memes go straight over.
- Reels once video exists (§10).

Needs: an @insidethenumber Instagram account (Chuck creates; I fill). Punch
list §6.

---

## 8. SEO — the compounding engine

The directive is right that the free tools are acquisition pages, not
utilities.

**Done:**
- Ten standalone calculator pages, each with FAQ schema, each linking into
  the site.
- 152 game pages retitled "[Team] vs [Team] Prediction, Picks & Odds" with a
  market-implied projection and FAQ schema — the query family Dimers gets
  half its traffic from.
- Both sitemaps submitted; game sitemap resubmitted Sep 2.

**Next (punch list §4):**
- Calculator pages answer the query in the first screen (the calculator
  itself above the fold, the explanation below), then introduce ITN.
- Game pages carry the directive's full spec: opening line, current line,
  movement, no-vig probability, projection, timestamp, and — where we can
  source them honestly — injuries and weather. Historical trends only where
  we have the data.
- `sameAs` in the Organization schema linking to the X profile and Beehiiv.
- Weekly Search Console check on which query family is climbing; build more
  of what Google is already rewarding.

**Honest timeline:** search compounds but it is slow. Impressions tripled
Aug 29-30 on calculator queries at position ~56. Clicks follow position;
position follows time and links. Two to four months to matter.

---

## 9. Viral data stories — weekly

Every Wednesday, one shareable finding built from data we hold:
- the line that moved the most on the board this week, and what it implied
- every book moved a number inside an hour (when we can see it)
- a total that closed exactly where it opened while the price swung —
  the market defending a number

Not "the public is betting Team A at 71%" — we do not have that. Not
"Team A is 2-11 ATS in this situation" unless we have built and checked the
situational dataset (a real project; see the Reddit monthly).

These are stories, not ads. They carry the site link because they earn it.

---

## 10. Short-form video — TikTok / YouTube Shorts / Reels

The directive is right that this is where a zero-follower account can break
out, and that no face is required. 20-45 seconds: charts, text animation,
the number changing on screen, a voiceover, "Inside the Number. The number
doesn't lie." at the end.

**What I can produce today:** animated number changes and chart sequences as
GIF/MP4 from the card library (the `linemove-gif` format already exists);
text-on-motion; screen captures of a line moving.

**What needs a decision:** voiceover (a TTS voice, or Chuck's), and
a rights-safe source for any sports footage. Without footage, the format is
charts + type + voice, which is exactly what the directive describes and is
enough to start.

Proposal: one 30-second video a day, Wednesday first, "The line just moved
two points. Here's why." Chuck decides on the voice. Punch list §6.

---

## 11. Email — the owned audience

The list is worth more than the X following because we own it.

**The Morning Board** (named Sep 2; site CTA and both send tasks updated).
Every morning, in this order:
1. The free pick, with the reasoning
2. The biggest overnight line move
3. One number to know
4. One market observation
5. Today's slate

Plus every other pick on the card (the homepage promises them), the
insidethenumber.com/games line, the @thenumberdesk line, 21+ / 1-800-GAMBLER.
Sends at 10:00 AM CT weekdays, 7:45 AM weekends and holidays.

**Lead magnets** (directive §14) — separate entry points so "get tomorrow's
pick" is not the only reason to subscribe. In order of build:
1. No-Vig Betting Cheat Sheet (one page; we already have the calculator)
2. How to Read Line Movement (the WHAT THE MARKET KNOWS franchise, collected)
3. The Bettor's EV Cheat Sheet
4. Bankroll Management Guide + calculator
5. NFL Betting Numbers Guide (season opener timing)
Each one a PDF behind the Beehiiv form, each one promoted on its own.

**Referral program** (directive §20): Beehiiv has one built in.
3 referrals → the cheat-sheet bundle · 5 → one month of Pro · 10 → three
months. Switch on when there are enough subscribers for it to move.

**Chuck's own network:** the fastest 20 real subscribers we will ever get.
This week.

---

## 12. Paid — Pro

The directive's structure is adopted as the message: **free shows what ITN
knows; Pro shows what ITN thinks.**

| FREE | PRO |
|---|---|
| Daily pick · full board · live odds · line movement · true prices · tools · DFS core plays · the Morning Board | Every pick with full analysis · best bets · parlays · DFS lineup construction · UFC/PGA analysis · projection and confidence on every game |

**The conflict, stated plainly:** the directive says Pro behind a waitlist
makes paid growth impossible and should open now. Chuck's standing order
(August) is not to charge anyone until there are real subscribers. Both are
reasonable. This is Chuck's decision and the plan does not make it for him.
Recommendation: keep the waitlist until the Morning Board has 100 real
subscribers, then open Pro at the founding price to that list first.

Stripe on Beehiiv is the mechanical step, and it is Chuck's (bank details).

---

## 13. Track record — the honest version

The directive calls a public record "absolutely critical" and it is right
that transparency is a marketing asset. Chuck retired the public record on
Aug 22, and the private record since is losing (12-18). Publishing it now
would be honest and self-defeating.

What we do instead, now:
- **PICK_LEDGER.md keeps grading privately, every day, no exceptions.** No
  cherry-picking, no deletions, no rewrites. It is the record whether or not
  it is published.
- **"What the numbers taught us this week"** (Sunday) is the public
  transparency post — the biggest miss, the biggest surprise, stated plainly
  — without a running tally.
- **Shareable results graphics** (directive §21): not yet. "ITN CALLED IT"
  cards are a record by another name. When the record turns, they turn on,
  wins *and* losses.

**Chuck's decision:** if he wants the public record back — losing and all —
it is a day's work to rebuild, and the directive makes a fair case that a
losing-but-honest record beats no record. I would wait for a 30-day sample
that is not underwater. His call.

---

## 14. Advertising — later, and where

Adopted verbatim: no ads now; traffic first. When there is an audience, ads
sit around the free mass content — homepage, game pages, calculators
(highest intent), category pages, newsletter sponsorships — never inside Pro.

The affiliate work (Caesars broken, BetMGM unverified, PrizePicks/Underdog
pending, Fanatics untried) is the first revenue line and needs only traffic
to matter. Links and the FTC disclosure go live the day a program approves.

---

## 15. AI, and not looking like it

The public should never feel ITN is a content farm. AI does the retrieval,
analysis, trend detection, graphics, drafting, scheduling and SEO. The output
has to carry specific numbers, specific observations, specific opinions,
specific visual storytelling and real-time relevance. Generic prose is
forbidden; the noun-swap test (§4.4) enforces it.

---

## 16. Measurement — the Monday growth report

Every Monday at 7:00 AM, `itn-monday-growth-report` pulls, from live pages:

- **Site:** unique visitors (real, outside), sessions, return visitors,
  time on page, tool usage, referer split
- **Email:** signups, signup conversion, open rate, click rate, real
  subscriber count
- **Search:** organic clicks, impressions, average position, top queries
- **X:** impressions, profile visits, link clicks, follower count (when on)
- **Reddit:** referral traffic, comments posted
- **Video/IG:** referral traffic (when on)
- **Money:** Pro conversion, cost per subscriber, revenue per visitor,
  ad RPM (when any of it exists)

Then: what worked, what did not, kill it or double down. Plus every open
punch-list item by owner, so nothing is forgotten. Reports archive to
`docs/reports/`.

Followers are reported but are not the target.

---

## 17. First 30 days — directional targets

Evidence that we can attract an audience, not money. Directional, not
guaranteed, and reported honestly on Mondays:

- 1,000 email subscribers (from 0 real)
- 100,000 monthly social impressions
- meaningful growth in real website sessions (from ~25/week)
- several posts over 10K impressions; one post or video over 50K
- SEO traction: calculator and game pages climbing in Search Console
- the six franchises recognisable as a series
- the Morning Board established as the daily habit
- the private record graded daily without a gap

## 18. Execution — the first four weeks

**Week 1 (Sep 3-9) — foundation, X still paused pending approval**
- Chuck approves §4.6 → X back on with the six franchises and images
- Cache logos and fonts; franchise templates built (10-15)
- Monitor list built (`docs/MONITOR_LIST.md`)
- Morning Board runs on the fixed schedule; verify Sep 3
- First lead magnet (No-Vig Cheat Sheet) live behind the form
- Chuck: 20 real subscribers from his own network; Reddit 20 min/day from kceza1
- NFL Week 1 (Sep 9-14): THE BOARD and MARKET MOVERS every day; real-time protocol live

**Week 2 (Sep 10-16) — volume and voice**
- Daily targets at full rate through NFL Week 1 and CFB Week 3
- First Wednesday data story; first Sunday "what the numbers taught us"
- Instagram account created; cards cross-posted
- Video decision made; first 30-second short if yes
- Game pages carry the full §8 spec

**Week 3 (Sep 17-23) — second engine**
- Reddit monthly data project posted
- Second and third lead magnets
- Referral program switched on if the list is big enough to matter
- First Monday report with week-over-week comparison

**Week 4 (Sep 24-30) — measure and decide**
- 30-day report against §17
- Kill what did not move; double down on what did
- Pro decision (§12) and track-record decision (§13) go to Chuck with the numbers in hand

---

## 19. What I am asking Chuck to decide

1. Approve the X rules (§4.6) so the account turns back on.
2. Video: yes or no, and whose voice.
3. Pro: waitlist until 100 subscribers, or open now.
4. Public record: stay retired, or rebuild losing-and-honest.
5. Instagram account creation.

Everything else in this plan is mine to execute, and the punch list and the
Monday report exist so that neither of us has to remember any of it.

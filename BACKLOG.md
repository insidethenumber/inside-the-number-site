# Inside the Number — Backlog

Parked decisions and future work. Newest items at the top of each section.
This file is internal — excluded from the deployed site via `.assetsignore`.


## Calculator pages — ON PROBATION, review Sept 8 (decided Aug 25, 2026)

Chuck's call, and his reasoning deserves recording: he has gambled for years
and never once used a betting calculator, and most casual bettors don't —
the sportsbook bet slip does the math. The counter-evidence is that Action
Network, Covers, VSiN, RotoWire and SportsLine all maintain standalone
calculator pages as SEO acquisition, so the pages stay up as an experiment,
not a conviction.

**Review on or after Sept 8, 2026** (two weeks of indexing). In Search
Console — signed in as insidethenumber.itn@gmail.com, never another account —
check impressions and clicks for:

  /parlay-calculator.html
  /odds-converter.html
  /no-vig-calculator.html

**The bar:** these pages exist only for search traffic, so search traffic is
the whole grade. If they are indexed but showing ~zero impressions, or
impressions with ~zero clicks, cut them: delete the three files, remove the
three sitemap entries and the .gitignore allowlist lines, and strip the three
"standalone page" links from tools.html. tools.html itself stays either way —
it predates this experiment and costs nothing.

If they ARE pulling impressions, leave them alone and revisit whether the
spread-to-moneyline converter (the one gap vs Action's suite) earns a page.

## Odds API — STAY ON FREE, revisit at a trigger (decided Aug 24, 2026)

Chuck's call: stay on the free tier now, move to the $30/mo 20K-credit plan once
there is traffic. He asked to be reminded rather than left to notice.

**The trigger — raise this with Chuck when ANY of these is true:**

1. `data/odds-usage.json` shows a month closing above **400 credits** (80% of the
   500 cap). At that point we are one slate change away from running dry.
2. A run logs `::warning title=Odds credits low` twice in the same month.
3. Paying subscribers reach roughly **22 at $17.99** (founding rate, set Aug 31
   2026, was $19.99), i.e. ~$400/mo — at which point $30 is under 8% of revenue
   and the constraint stops being worth managing.
4. We want a market the free tier cannot cover: player props, alternate lines, or
   historical odds for backtesting. Historical is EXCLUDED from free entirely,
   so any real backtest work forces the upgrade.

**What the free tier actually buys us** (measured Aug 24, not estimated):
  - 500 credits/month; cost is `markets x regions` per call
  - Our scoped daily pull: 4 credits morning + 3 afternoon = **~210/month**
  - Leaves ~290/month of headroom for UFC card weeks and one-off checks
  - "Most bookmakers" not all, and NO historical odds

**Correction worth remembering.** The budget originally assumed out-of-season
sports were free, because the docs say an empty response is not charged. Measured
on a runner in August: NBA returned 41 events and NHL 32, because books post
next-season lines months ahead. NFL returned 272. **Nothing comes back empty, so
there is no seasonal discount.** A full-board pull is 16 credits year round —
which is why the daily pull is scoped to UFC plus published picks instead.

---

## PGA — PAUSED (decided Aug 24, 2026)

Chuck's call: put PGA on hold and show a "coming soon" state rather than half-build
it at the tail end of the season.

Reasoning: the 2026 PGA season ends with the TOUR Championship (Aug 27-30). Building
outright coverage now buys one tournament before the season closes, while CFB Week 1
and a UFC card both land Aug 29 with far more betting volume behind them.

Also learned while scoping it:
  - ESPN's golf odds endpoint returns EMPTY. There are no outright prices in the free
    feed. Confirmed, not assumed.
  - So outrights need either a paid feed (~$29/mo) or hand entry. For a majors-only
    cadence — four or five events a year — hand entry is the better answer. Do not buy
    a subscription that gets used five times.
  - The TOUR Championship has NO CUT (30-man field). The "post-cut Friday update" idea
    in the original plan does not apply to this event. Any future golf automation must
    check whether an event has a cut before publishing a post-cut anything.

What the coming-soon page now promises for 2027 majors:
  - Full field, every outright converted to a true price
  - Total margin across the field stated at the top — the differentiator, since golf
    outright books run 130%+ against about 102% on a baseball moneyline
  - Majors only, not every week

---

## 1. PGA coverage model (SUPERSEDED by the above) (raised Aug 22, 2026)

Golf doesn't fit the daily-game rhythm, so it gets its own cadence — two
publishing moments per tournament week rather than a pick every day.

**Tuesday — tournament preview (before the event)**
- Post the outright odds for the field
- 2-3 picks across markets, not just the winner:
  - Outright winner (including a genuine darkhorse at a long price)
  - Top 5 finish
  - Top 10 finish
- Rationale: pre-tournament outright markets are among the softest on the
  board. Limits are low, the field is large, and books price the tail of the
  field lazily. This is the opposite of an MLB moneyline.

**Friday evening / very early Saturday — post-cut update**
- Re-pull odds once the cut is in and the field is halved
- Fresh analysis and picks against the new number
- Rationale: prices move hard after the cut and the remaining field is small
  enough to actually model. A player who opened +8000 and made the cut in
  contention is a completely different bet on Saturday morning.

**Open questions before building**
- Which ESPN endpoint (or other source) carries PGA outright and finishing-
  position markets? The current `golf/pga/scoreboard` endpoint gives the
  leaderboard and field but has NOT been verified to carry outrights,
  top-5 or top-10 prices. **Research a real PGA odds page first** — this is
  the blocker, and it may require the paid odds feed rather than ESPN.
- Does this need its own page (`pga.html`) or can `games.html?sport=PGA`
  carry a leaderboard + outright board?
- Scheduling: two extra scheduled tasks (Tue preview, Fri post-cut), or fold
  into the existing daily runs with day-of-week conditionals?

---

## 2. CFB and CBB volume (raised Aug 22, 2026)

**The problem.** A November Saturday can carry 60+ CFB games; CBB routinely
runs 80-150 a day in season. Combined with the existing slate that's ~150+
contests in a single day. The current model — hand-researched analysis per
contest — does not scale to that, and neither does a human reading it.

**Options to weigh**

*A. Power conference only.* Cover the SEC, Big Ten, Big 12 and ACC plus
ranked matchups and anything on national TV. Roughly 15-25 CFB games on a
Saturday instead of 60. For CBB, the equivalent is the major conferences plus
the AP Top 25. Cuts volume by ~70% and keeps the games people actually bet.
Downside: smaller-conference lines are frequently the softest on the board,
so this deliberately walks away from the weakest markets.

*B. Full board, tiered depth.* Every game gets the free market data — line,
movement, no-vig true price — because that's computed, not written. Only a
selected subset gets written analysis and a stated pick. This matches the
free/Pro split the site already runs on and means volume costs nothing on the
free tier.

*C. Full board, model-generated writeups.* Templated prose from model output
on every game, Dimers-style. Highest volume, lowest quality per unit, and it
conflicts with the "reasoning shown on every call" promise if the reasoning
is obviously generated.

**Leaning:** B, because the expensive part is the writing, not the data. The
board can hold 150 games without any additional work per game; the picks stay
at 3-4 a day regardless of how many games exist. Revisit if the Pro tier's
value proposition needs more written volume to justify $17.99.

**Note:** whichever way this goes, the diversification rules in the four
scheduled task prompts cap picks at 2 per sport, so CFB/CBB can't flood the
daily card even in peak season.

---

## 3. Public betting splits — blocked on data (raised Aug 22, 2026)

**The ask:** show where the money is going. "72% of bets on the Rays" — and
more usefully, the gap between % of *bets* and % of *money*, which is the
classic sharp-vs-public tell.

**Why it isn't built yet.** There is no free, CORS-enabled API for this. The
site's JavaScript runs in the visitor's browser and calls ESPN directly;
ESPN carries odds but not betting percentages. Everything that has splits is
either a website (Covers, Wiseguy Team, PlayerProps.ai, Split Labs — HTML
pages, not APIs) or a commercial feed.

**This must not be faked.** Inventing "72% on the Rays" would be publishing
a fabricated statistic to paying customers, and it's the exact thing that
makes tout services worthless. No placeholder numbers, ever.

**Paying for Action PRO does NOT unlock this.** Their terms were read in
full on Aug 22, 2026. Betting percentages are enumerated by name as their
protected Content; the licence granted is limited to personal, non-commercial
home use; republishing any part of the site for a commercial enterprise
requires their written consent; and page-scraping, robots and spiders are
separately prohibited. Their arbitration clause carves out the right to seek
injunctive relief in court for IP violations, with the user indemnifying
their costs. A PRO subscription is a viewing licence, nothing more.

*What a PRO subscription IS good for:* reading it and letting it inform
picks we write ourselves. That's legitimate and cheap at $99.99/yr. The line
is input-to-judgment (fine) versus republished-as-data (not fine).

**Do not buy a splits feed yet.** Sportradar's Betting Splits API is the
licensed answer, but it's enterprise-priced — realistically four figures a
month — and buying it before there are paid subscribers to serve is
backwards. Revisit only if Pro grows to where that's a rounding error.

**If data spend happens, this is the better first purchase.** The Odds API
Business tier at **$99/mo** gets 50+ books including **Pinnacle**:
  - A no-vig Pinnacle line is far closer to true probability than the single
    provider ESPN returns, which would improve the projections themselves
    rather than just adding a stat to the page.
  - Multi-book enables a "best available price" feature on every game, which
    points directly at the sportsbook affiliate links. Improves the product
    and earns at the same time.

**What we currently get free from ESPN** — and it is a lot: scores,
moneyline/spread/total with opening AND closing numbers, team records
including home/road splits, and probable starters with ERA. The whole
projection model and all three market reads run on this at zero cost.

**What we already ship that gets at the same idea.** Line movement is the
honest proxy and it's live now: when a number moves, money moved it. The
game pages state which way each of the three markets travelled and what that
implies. That's a real signal derived from real data — it just can't be
expressed as a percentage of tickets.

**Worth knowing:** bet% and money% disagreeing is the actually valuable
signal (many small tickets one way, big money the other). A single "72%"
figure without that split is close to noise, so if this gets bought, buy the
feed that carries both.

---

## 3b. Beehiiv items needing Chuck's sign-off (found Aug 22 audit)

- **Publication tagline is stale.** The archive header still reads "documented
  picks and sharp analysis" — "documented picks" was the public-record promise,
  which was retired. Changing it is a publication setting, so it needs Chuck to
  approve or do it.
- **All six published posts carry the old thumbnail artwork**, which still says
  "Every result logged the day it settles". The local files were regenerated but
  Beehiiv keeps whatever image was attached at publish time. Fixing means editing
  six posts by hand, or leaving them and having new posts use the new art.
- **Thumbnails crop badly.** The 1200x630 OG image is squeezed into a squarer
  card, slicing the ITN mark off the left edge of every post. Needs a
  purpose-built thumbnail rather than reusing the OG image.

---

## 4. MLB model — next refinements (built Aug 22, 2026)

The predicted-score model is live: team runs scored and allowed, weighted for
the probable starters, run over a joint Poisson distribution so the moneyline,
runline and total all come off one projection. Runs on ESPN's free team
statistics endpoint. Two known limitations, in priority order:

**Two bugs found and fixed in the Aug 22 evening audit — recorded so the
reasoning isn't lost:**

*Unearned runs.* ESPN's pitching block reports EARNED runs allowed; the batting
block reports ALL runs scored. In a closed league those totals must match — every
run scored is a run allowed. Measured live: 4.473 scored per game against 4.099
earned allowed, an 8.4% gap. Every team therefore looked 8% better at preventing
runs than it was, and every projection came in under the market. Across a full
slate that produced total edges up to 22 points, nearly all unders — a systematic
bias reading as a systematic edge. Now corrected by a factor derived from the
data on each load, so it tracks the real unearned rate as the season moves.

*Anchoring the wrong quantity.* The market anchor was blending the model's RUN
SHARE against the market's implied WIN PROBABILITY. Different scales — a 55/45
run split produces roughly a 60/40 win rate — so the moneyline was never actually
anchored. Its edge sat at ~16 points whether the market weight was 62% or 85%.
Now the model's own win probability is read off the distribution, blended with
the market, and the run split solved back by bisection.

Market weight is currently **75%** (`MKT_W`). It is deliberately high because the
model has never been graded. Lower it only against a back-tested sample.

**Park factors.** The raw model assumes a league-average run environment. At
Coors it projected 9.67 runs into a posted total of 11 and called that a
21.6-point edge on the under — which is altitude, not edge. Anchoring to the
posted total currently bounds this (it lands at 10.49 and a 7.4-point gap),
but anchoring is a bandage. Real park run indices — Coors ~1.33, Petco ~0.92,
and so on for all 30 — would fix it at source and let the anchor weight drop,
which would let genuine disagreements show at full size.

**Weather and wind.** Same class of problem, particularly for totals in
Chicago and San Francisco. The market prices it; we don't. Currently absorbed
by the anchor.

**Also worth doing:** back-test the model against completed games before
leaning on it commercially. It has never been graded. Everything it says is
plausible and internally consistent, which is not the same as accurate.

**Other sports.** The Poisson approach fits baseball because scoring is close
to Poisson. It does not transfer to football or basketball — those need a
margin-distribution model (normal around a projected spread) rather than a
run-count model. NFL/NBA/NHL currently fall back to the records-based
moneyline model plus market reads on the other two markets.

---

## 5. Standing items (carried from the Aug 22 audit)

- **Legal pages** — `privacy.html`, `terms.html`, `responsible-gambling.html`
  all still 404. Blocker for Stripe approval on the Pro tier.
- **`sitemap.xml`** — missing. `robots.txt` is still Cloudflare's default
  AI-signals file with no sitemap reference.
- **Custom 404 page** — currently Cloudflare's unbranded default.
- **Beehiiv post thumbnails** — the 1200x630 OG image is being cropped to a
  squarer card, slicing the ITN logo off the left edge of every post. Needs a
  purpose-built thumbnail rather than reusing the OG image.
- **`inside_the_number.html`** — gitignored local duplicate that the daily
  routine used to copy over `index.html`. The task prompts now edit
  `index.html` directly, so this file is dead weight and a staleness trap.
  Safe to delete once a few clean runs confirm nothing references it.
- **CFB/CBB team logos** — not in any lookup table, so college picks render
  without crests wherever logos are used.

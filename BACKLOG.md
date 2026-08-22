# Inside the Number — Backlog

Parked decisions and future work. Newest items at the top of each section.
This file is internal — excluded from the deployed site via `.assetsignore`.

---

## 1. PGA coverage model (raised Aug 22, 2026)

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
value proposition needs more written volume to justify $19.99.

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

## 4. Standing items (carried from the Aug 22 audit)

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

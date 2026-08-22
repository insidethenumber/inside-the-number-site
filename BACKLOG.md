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

## 3. Standing items (carried from the Aug 22 audit)

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

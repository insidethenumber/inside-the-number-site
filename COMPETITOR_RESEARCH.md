# Competitor Research — Aug 20, 2026

Deep dive across Action Network, Covers/Odds Shark, Pickswise, Wunderdog,
Vegas Insider, Pregame, OddsJam, Dimers, DraftKings and Hard Rock Bet.
What each does well, and what we took (or deliberately didn't).

---

## What we implemented

### Dimers → no-vig win probability *(the biggest win)*
Dimers puts a win-probability percentage beside the odds on every game card.
It's the clearest possible expression of "model vs market."

We can't run a proprietary model, but we can do the honest version: American
odds imply a probability, and the two sides always sum to **more than 100%** —
that surplus is the sportsbook's hold. Normalizing both sides back to 100%
strips the margin out and leaves what the market actually thinks.

Verified against real data (Aug 21 slate):

| Game | Odds | Raw sum | No-vig | Hold |
|---|---|---|---|---|
| ATL @ MIL | +123 / -149 | 104.7% | 42.8% / 57.2% | 4.68% |
| SF @ BOS | +149 / -181 | 104.6% | 38.4% / 61.6% | 4.57% |

Those are textbook MLB numbers. Every matchup card now shows both sides'
no-vig probability, a split bar, and the book's hold — **labeled "market
win prob · vig removed," not presented as our own model.** That distinction
matters and should never be blurred.

### Covers → rich matchup cards
Best card design of the group: league tag, both teams with logos, lines,
expert pick, analysis thumbnail, CTA. Our slate cards are modelled on this.

### OddsJam → trust bar
Their hero sits above a four-item proof bar (7-day trial, 1:1 coaching, 150+
books, fastest data). We built the same pattern with claims that are actually
true and checkable: every pick free, losses stay up, live odds not retyped,
reasoning shown. **No invented testimonials or "trusted by 100k bettors."**

Note their positioning — *"Make $500-$1000+ weekly. Use math, not luck."* —
is nearly identical in spirit to *"The number doesn't lie."* Same lane.

### ESPN → live scoreboard, team records, date strip
ESPN's public feed powers our live scoreboard, team records, brand colors
and live line movement. Their date-strip navigation (MON AUG 17 → SUN AUG 23)
is a pattern worth adding to the record page later.

---

## What we found but deliberately did NOT build

### Vegas Insider → multi-book odds grid with best-price highlighting
Their best feature: ten sportsbook columns per game with the **best available
number highlighted in gold.** Genuinely useful — it tells you where to bet.

**We can't build it honestly.** ESPN exposes exactly one book (DraftKings).
A real multi-book grid needs a paid odds feed (The Odds API, OpticOdds and
similar start around $50-100/month). Faking it with one book dressed up as
several would be exactly the kind of thing we spent this project removing.
Revisit if there's ever budget.

### OddsJam / Dimers → third-party verified records
OddsJam cites **Pikkit**, an independent bet tracker, to verify user profits.
Our record is self-reported. Our disclaimer already says so plainly, which is
the right call — but third-party verification is the single strongest trust
upgrade available if this ever grows.

### Pregame → handicapper marketplace + forums
Sell picks from multiple named handicappers, plus contests and forums. Dated
visually (2010s), but it's the mature form of this business model. Only works
with real handicappers and real volume.

### Wunderdog → personality-led trust
One named person, big verifiable claim, press logos ("Featured in ESPN, WSJ"),
"Pick Performance" in the primary nav. Closest business model to ours. The
lesson: **make the record the hero**, not one nav item among six. Also has a
nicely designed custom 404 — worth copying as a polish detail.

### DraftKings / Hard Rock Bet
Blocked — live sportsbooks. Their UI is bet-slip driven, which isn't our
model, so little was lost.

---

## Ideas worth building next

1. **Closing line value (CLV).** Capture the no-vig probability at the moment
   we post a pick, then compare to the closing number. "We beat the close on
   68% of picks" is the most credible metric in this industry — far harder to
   fake than win rate, and nobody at our scale publishes it.
2. **Date-strip navigation** on the record page (ESPN/Vegas Insider pattern).
3. **Per-sport landing pages.** Vegas Insider runs MLB Odds / MLB Free Picks /
   MLB Consensus / MLB Expert Records as separate SEO doorways.
4. **Probable pitchers on cards** — ESPN's feed already carries them, with
   handedness. Directly relevant since our reasoning is usually pitcher-led.
5. **Custom 404.**

---

## Technical note: the odds window

**ESPN drops the odds object the moment a game starts.** Confirmed Aug 20:
every game showed `hasOdds: false` once it went in-progress or final.

Consequences:
- No-vig probability and line movement only render for *upcoming* games.
  That's the correct behaviour — they're pre-game concepts — but it means the
  homepage looks quieter late at night than it does in the morning.
- **The daily routine must capture odds in the morning while they exist.**
  Anything not recorded before first pitch is gone from the feed.

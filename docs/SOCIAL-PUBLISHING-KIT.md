# Social publishing kit

**Text-first, original, no licensed imagery.** No team logos, no player photographs, no broadcast footage, no scraped or stock images. Everything is typography, rules, bars and numbers — producible in any vector tool, Canva, Figma, or a browser screenshot of styled HTML.

**Every post must teach one thing a reader can verify in under a minute.** If a slide cannot be checked with the site's own calculator or a public scoreboard, it does not ship.

---

## Canvas

| | |
|---|---|
| Size | **1080 × 1350** (4:5 — the tallest Instagram allows in feed) |
| Story variant | 1080 × 1920, same layout, +285px top and bottom |
| Safe margins | **80px** all sides |
| Dead zone | bottom **250px** — nothing important (UI overlay) |
| Slides | **5 maximum** |

## Color tokens — from the live site

| Token | Hex | Use |
|---|---|---|
| `bg` | `#050608` | background, always |
| `ink` | `#F0F2F5` | primary type |
| `accent` | `#00D084` | **the answer.** One per slide, never two |
| `second` | `#3BA7FF` | the posted/before number |
| `muted` | `#9CA3AF` | labels, footer |
| `rule` | `#1C2129` | hairlines |

## Type scale

| Role | Face | Size | Treatment |
|---|---|---|---|
| Label | IBM Plex Mono 500 | 32px | uppercase, `letter-spacing 0.16em`, `muted` |
| Hero number | Barlow Condensed 900 | 200–300px | uppercase, tight leading |
| Sub number | Barlow Condensed 900 | 90–120px | — |
| Body | Barlow 400 | 44px | max two lines |
| Footer | IBM Plex Mono 400 | 28px | `muted` |

## Slide hierarchy — identical on every carousel

```
1  HOOK        one number or one question. No explanation.
2  SETUP       the thing most people believe
3  MECHANISM   the arithmetic
4  PAYOFF      the answer, in accent green
5  CTA         one destination, one line of reassurance
```

## The one rule

**One green element per slide.** Green marks the answer. Two green things means nothing is the answer.

## Producing graphics without licensed imagery

1. **Preferred — styled HTML screenshot.** Build a 1080×1350 `div` with the tokens above, open at that viewport, screenshot. Uses the real brand fonts, costs nothing, reproducible.
2. **Canva** — set a 1080×1350 custom size, load Barlow Condensed and IBM Plex Mono (both free on Google Fonts, both already used by the site), build a five-frame master, duplicate per post.
3. **Never** a photo search, a stock library, a team crest, a headshot, or a broadcast still — including "just for the background".
4. Backgrounds: flat `#050608`, optionally a 1px `rule` grid at 120px pitch at 6% opacity. No gradients across the full canvas, no texture.

---

# Three reusable templates

## Template A — LINE MOVEMENT

For: a number that moved, or a number sitting somewhere interesting.

```
1  LABEL: [SPORT] · [DAY]          HERO: the current number
2  LABEL: WHERE IT OPENED          SUB: open → current, second/ink
3  LABEL: WHAT MOVED               BODY: one sentence, mechanism only
4  LABEL: WHAT IT DOES NOT SAY     BODY (accent): "We cannot see who bet. Neither can anyone else."
5  CTA: the board                  insidethenumber.com/[nfl|cfb|games]
```
Slide 4 is mandatory and is the brand. Never attribute a move to sharp money.

## Template B — NO-VIG MATH

For: any two-sided market.

```
1  LABEL: [MARKET]                 HERO: the posted price
2  LABEL: WHAT IT IMPLIES          SUB: X% (second)
3  LABEL: BOTH SIDES               SUB: X% + Y% = Z% — "more than 100%"
4  LABEL: THE TRUE PRICE           HERO (accent): the fair number
5  CTA: /no-vig-calculator
```

## Template C — KEY NUMBER

For: 3 and 7, break-even rates, series compounding.

```
1  LABEL: THE NUMBER               HERO: the figure
2  LABEL: WHY                      BODY: the causal mechanism in one sentence
3  LABEL: THE COMPARISON           two values side by side, one accent
4  LABEL: WHAT IT COSTS            BODY (accent): the practical consequence
5  CTA: the relevant guide
```

---

# Seven post packages

All facts read from the live ESPN feed at **3:22 PM ET, Thu Sep 17, 2026**. Everything marked **[VERIFY]** must be re-read the morning it posts, or the evergreen version goes instead.

### 1 · Thu — Template B — `/no-vig-calculator`
1 `WHAT −110 ACTUALLY COSTS` / **`104.8%`** · 2 `THE SETUP` / `−110 + −110` / "Both sides priced at 52.4%" · 3 `THE PROBLEM` / `52.4 + 52.4` / "A market cannot be 104.8% likely" · 4 `THE MARGIN` / **`4.8%`** *(accent)* / "Divide it out and both sides are +100" · 5 `insidethenumber.com/no-vig-calculator`
**Alt:** *What −110 actually costs. Two sides at minus 110 sum to 104.8 percent; the true price on each is plus 100. The extra 4.8 percent is the margin. Inside the Number, educational.*
**Verify:** nothing — pure arithmetic. Optional hook: BUF −5.5, total 54.5 **[VERIFY]**

### 2 · Fri — Template A — `/cfb`
1 `FRIDAY · COLLEGE FOOTBALL` / **`−57.5`** · 2 `NOT A MISTAKE` / `MONEYLINE: —` · 3 `WHY` / **`−10000`** / "Risk $10,000 to win $100" · 4 `WHAT IT CLAIMS` / **`99%`** *(accent)* / "Nobody wants either side of that" · 5 `insidethenumber.com/cfb`
**Alt:** *Friday college football. A minus 57.5 spread with no moneyline. The moneyline would be near minus 10000, implying 99 percent, so no book posts it. Inside the Number, educational.*
**Verify:** ORE −57.5, total 67.5, **and that no moneyline has appeared** **[VERIFY]**

### 3 · Sat — Template B — `/ufc-331-odds`
1 `UFC 331 · TONIGHT` / **`104%+`** / "Every two-fighter market adds to more than 100%" · 2 `WHY` / "Both sides priced above their true chance" · 3 `THE METHOD` / `Convert → add → divide` · 4 **`THE FAIR PRICE`** *(accent)* / "What the market thinks, before the fee" · 5 `insidethenumber.com/ufc-331-odds`
**Alt:** *UFC 331 tonight. Every two-fighter market sums to more than 100 percent; the excess is the book's margin. Convert, add, divide for the fair price. Inside the Number, educational.*
**Verify:** both main-event moneylines, Saturday morning **and** before the main card; that the main event is unchanged **[VERIFY]**

### 4 · Sun — Template C — `/football-line-movement`
1 `NFL WEEK 2, COUNTED` / **`2 of 16`** / "spreads sit exactly on 7" · 2 `AND` / **`0 of 16`** / "sit exactly on 3" · 3 `WHY` / `3 and 7` / "Field goals and touchdowns make these the most common margins" · 4 **`A HALF-POINT`** *(accent)* / "across 3 or 7 moves more outcomes than anywhere else" · 5 `insidethenumber.com/football-line-movement`
**Alt:** *NFL Week 2 counted: two of sixteen spreads sit exactly on seven, none on three. Field goals and touchdowns make 3 and 7 the most common margins. Inside the Number, educational.*
**Verify:** **recount the board.** Read Sep 17: 16 games, 2 on 7 (PHI −7, LAR −7), 0 on 3, 10 between 3 and 7 **[VERIFY]**

### 5 · Mon — Template C — `/break-even-calculator`
1 `THE QUESTION NOBODY ASKS` / **`50%?`** · 2 `AT −110` / **`52.4%`** *(accent)* · 3 `AT −120` / `54.5%` · 4 `AT +150` / `40.0%` / "A good price lowers the bar a long way" · 5 `insidethenumber.com/break-even-calculator`
**Alt:** *Break-even win rates by price: 52.4 percent at minus 110, 54.5 at minus 120, 40 at plus 150. Inside the Number, educational.*
**Verify:** nothing. Optional hook: LAR −7, total 48.5 **[VERIFY]**

### 6 · Tue — Template C — `/mlb-playoffs`
1 `SAME TEAM. SAME EDGE.` / **`60%`** / "to win any single game" · 2 `BEST OF 3` / `64.8%` · 3 `BEST OF 5` / `68.3%` · 4 `BEST OF 7` / **`71.0%`** *(accent)* / "Eleven points from format alone" · 5 `insidethenumber.com/mlb-playoffs`
**Alt:** *A 60 percent per-game team is 64.8 percent to win a best of three, 68.3 over five, 71.0 over seven. Series length compounds an edge. Inside the Number, educational.*
**Verify:** Wild Card still starts **Tue Sep 29**. **Name no teams** — MLB has not set matchups **[VERIFY]**

### 7 · Wed — Template B — `/parlay-calculator`
1 `3 LEGS. −110 EACH.` / **`+596`** / "Looks generous" · 2 `HOW OFTEN IT LANDS` / **`12.5%`** *(accent)* · 3 `WHAT +596 IMPLIES` / `14.4%` · 4 `THE GAP` / **`THE MARGIN, ×3`** / "4.8% on one bet becomes about 13%" · 5 `insidethenumber.com/parlay-calculator`
**Alt:** *Three-leg parlay at minus 110 pays plus 596 but lands 12.5 percent of the time while the payout implies 14.4. The margin compounds per leg. Inside the Number, educational.*
**Verify:** nothing. Confirm the calculator returns +596 for three −110 legs before linking.

---

## Pre-publish checklist — every post, no exceptions

**Prices** ☐ re-read from the live feed this morning ☐ if it moved, the post uses the new number ☐ if it will not load, the evergreen version goes instead
**Dates** ☐ every date checked against a primary source ☐ no matchup, schedule or injury asserted from memory
**Sources** ☐ the book and feed named on any card carrying a market number ☐ time of read recorded
**Links** ☐ resolves to a live page ☐ UTM appended, per `measurement-dashboard.md` ☐ exactly one link
**Compliance** ☐ no pick, lean or "I like" ☐ no lock, guarantee or profit claim ☐ no "sharp money" ☐ no record or confidence rating ☐ no fake urgency ☐ no injury claim ☐ "educational only" present ☐ "prices move" present on anything with a live number ☐ anonymous voice, no "I"
**Imagery** ☐ no logo, headshot, broadcast still or stock image ☐ every element original
**Slides** ☐ five or fewer ☐ one green element per slide ☐ alt text written ☐ nothing important in the bottom 250px

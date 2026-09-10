# Editorial doctrine — Inside the Number

Set by Chuck, 9 September 2026. This governs every post on every platform and
supersedes any earlier guidance about "making a card." Scheduled tasks and
future sessions read this first.

## Identity — not negotiable

**Inside the Number stands on its own.** Chuck's separate professional
reputation is not attached to this brand, is not a growth lever, and is not to
be raised again. Do not suggest it, do not reference it, do not build creative
around it. ITN builds its own identity from zero.

## The standard

We look like a professional sports-media publisher, not an AI content farm.

    The sports moment is the HERO.
    The Inside the Number data is the INTELLIGENCE.
    The graphic is the SUPPORTING DESIGN.

Do not make a graphic merely because you can. Before anything is built, answer:

> What real image or video would make this impossible to scroll past?

Then build the analytics around that asset. Not the other way round.

## Six questions, every story

1. What just happened?
2. Why does the audience care *right now*?
3. What is the strongest ITN statistic or betting insight?
4. What real photo or video would make this impossible to scroll past?
5. Where can we **legally** obtain that asset?
6. What format: Reel, image, carousel, X post?

Question 5 is the one that kills most ideas. Answer it honestly before writing
copy, not after.

## Priority order for media

    REAL VIDEO  >  REAL GAME PHOTOGRAPHY  >  REAL PLAYER/COACH IMAGERY
    >  REAL REACTIONS  >  REAL CURRENT EVENTS  >  conceptual stock
    >  our own charts and cards

AI-generated athlete imagery is not the default. It is not anything. We do not
use it.

## Never

- Fabricate a moment, reaction, score, injury, quote, line movement or
  highlight. Not once, not "close enough", not as a placeholder.
- Assume that because a video or photo is visible on X, Instagram, YouTube or
  TikTok we may download it and repost it commercially. Visible is not
  licensed. This is the single most common way small publishers get struck.

## What we can actually use today — the honest rights position

This is the constraint that shapes everything above.

**1. Quote-post and embed — our only route to current game video.**
Quoting a post keeps the media hosted by the original account. We are not
making a copy; we are pointing at theirs, with attribution built in. This is
how we legally put tonight's footage next to our number. It is already the
house method for the hourly X rounds and it should now be the default for any
current highlight.
Limits: X and Instagram only. Doesn't give us a Reel asset. Can't be cropped.

**2. Wikimedia Commons — real game photography, licence-checked.**
`assets/photos/` holds 50 files, every licence read at download time and
NC/ND/unknown rejected (see `docs/IMAGE-SOURCING.md`). Real stadiums, real
teams, real game action.
Limits: mostly 2005-2014, amateur, no current players. Good for a stadium
establishing shot, useless for "what happened last night."

**3. Unsplash — conceptual only.**
Turf, lights, goalposts, empty bowls. No identifiable athlete, no team mark.
Safe anywhere including next to a subscribe button.

**4. Our own work.** PIL cards, charts, team logos used to identify the teams
in commentary. Logos are trademark, not copyright: naming and identifying a
team in analysis is defensible; using the mark as decoration, on merchandise,
or in any way implying endorsement is not.

**5. Not available: current wire photography.** Imagn, AP, Getty. We have
bought nothing. Until we do, "real current player imagery" is only reachable
through route 1.

### The gap, stated plainly

The doctrine asks for real current photography and video as the default. Routes
1 and 2 cover perhaps half of that. The other half needs a wire licence.

**Imagn (USA TODAY Sports)** is the realistic one — built for digital-first
publishers our size, deep local-photographer network, current-day game files.
AP is the solid second. Getty is the most complete and the most expensive.

Until one is bought, every brief must state the rights route explicitly, and a
brief whose only viable asset is unlicensed wire art is a brief we kill or
rebuild around a quote-post.

## Editorial-vs-commercial, restated

Editorial use covers reporting, commentary and analysis. It does not cover
selling.

- **Fine:** a real photo of tonight's game beside our breakdown of tonight's
  number.
- **Not fine:** a quarterback's face on a graphic carrying a price, a promo
  code, an affiliate link or the word "premium." That is his likeness selling
  our product, and no photo licence cures it.

## Required output for every proposed post

**EDITORIAL BRIEF** — Story · Why it matters now · Key number · Hook ·
Caption · CTA · Target platform · Ideal length

**MEDIA BRIEF** — Asset type · Exact player/team/event · Exact visual needed ·
Source · Rights status · Crop · Recommended duration

No brief ships without both. "Rights status" may not read "TBD."

---

## Player headshots — settled Sep 9, 2026

Chuck sent over a BettingPros post (five players, five prices, high
engagement) and asked where they source their imagery. They don't buy any.
Those are **ESPN roster portraits** — the team-issued publicity headshot every
club publishes — pulled from `a.espncdn.com/i/headshots/nfl/players/full/<espn
id>.png`, the same API we already call every morning for the numbers.

This retires a month-long assumption that the format we wanted was blocked
behind a $50-$100 wire photo. It wasn't. It was blocked behind not knowing
which endpoint to call.

**What a roster portrait is and isn't.** It is a publicity photo the league
distributes so publishers can identify a player. It is *not* a wire
photographer's copyrighted game frame, and the two are not the same risk. But
it is also not a licence: copyright sits with the league or club, ESPN's CDN
is a delivery host and not a grant, and the player holds a right of publicity
on top. We use them the way we use a team logo — to identify the human a
number belongs to, inside editorial commentary on a real game.

**Do not read "everybody does it" as cover.** BettingPros is owned by
FantasyPros, a real company that almost certainly holds a data-and-image
agreement. We are making a judgment about a lower-risk category of asset, not
relying on somebody else's licence.

**The line, which no file and no price changes:**

> A player's face never appears on a graphic carrying a price, a promo code,
> an affiliate link, or the word "premium."

Odds are fine. "+425 via DraftKings" is a fact about the market and reporting
it is commentary. A DFS salary is a fact. **Our** subscription price beside
the same face is his likeness selling our product, and no licence cures that.

Pipeline: `data/headshot_manifest.json` -> `scripts/fetch_headshots.py` ->
`.github/workflows/fetch-headshots.yml` -> `assets/headshots/<league>/<id>.png`.
CI-routed because the sandbox cannot reach ESPN's CDN. Card formats `duel` and
`lineup` in `scripts/cards.py` read them off disk.

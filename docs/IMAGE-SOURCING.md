# Where our pictures come from

Written Wed 9 Sep 2026. This is the whole policy — if a photo does not come
from one of the two sources below, it does not go out.

## The constraint that shaped this

Chuck's rule, unchanged: **no AI-generated photos or video.** Everything visual
is either a real photograph or a thing we drew ourselves (PIL cards, team logos,
charts).

The second constraint is technical: **the sandbox cannot download images.**
Every image host — `images.unsplash.com`, `upload.wikimedia.org`,
`images.pexels.com`, `api.unsplash.com` — returns 403 through the proxy. Only
`github.com` git traffic and `insidethenumber.com` get through.

So the pipeline runs the other way round: a manifest goes into the repo, GitHub
Actions downloads the photos, commits them back, and the sandbox pulls them.

```
data/photo_manifest.json      you add a line here
        ↓ push
.github/workflows/fetch-photos.yml   runs scripts/fetch_photos.py
        ↓ commit
assets/photos/*.jpg           + assets/photos/CREDITS.json
        ↓ git pull
scripts/cards.py, Reel builders
```

## Source 1 — Unsplash (conceptual only)

Unsplash License: free, commercial use allowed, attribution not legally
required. We credit anyway in `CREDITS.json` because the photographers gave the
work away and it costs us nothing.

**Restriction we impose on ourselves:** Unsplash images are used only where
there is no identifiable athlete and no team mark. Turf, floodlights,
goalposts, an empty bowl, a ball on grass. Those are safe under any use,
including a graphic that sells a subscription.

## Source 2 — Wikimedia Commons (real game photography)

This is the only free source with actual NFL, CFB and MLB game photos of real
teams in real stadiums. Licenses vary per file, so `fetch_photos.py` reads each
file's real license from the Commons API and **rejects** anything that is:

- **NC** (non-commercial) — we run affiliate links; commercial is what we are.
- **ND** (no derivatives) — every card we build crops and overlays. ND makes a
  photo useless to us.
- **unknown** — an unrecognised license string is treated as a rejection, not a
  maybe.

It also rejects anything under 1200×800, because a Reel is 1080×1920 and a soft
upscale looks exactly as cheap as it is.

Accepted files land in `CREDITS.json` with photographer, license and source URL,
so attribution at post time is a lookup, not a memory test.

## The rule that actually matters: editorial vs commercial

Photos of identifiable athletes in uniform are **editorial**. That means they
can illustrate reporting, commentary and analysis. It does **not** mean they can
sell something.

**Fine.** A photo of a game next to our breakdown of that game's number. The
photo illustrates the analysis.

**Not fine.** A quarterback's face on a graphic that says "subscribe for our
premium picks." That is his likeness selling our product — Right of Publicity,
plus the league's trademarks. Different problem, no license fixes it.

The practical test before any graphic ships:

> Is the photo illustrating something we are saying about that game, or is it
> decorating an ad?

If it is decorating an ad, swap in an Unsplash conceptual shot. That is exactly
what those nine files are in the library for.

**Never:** a player photo on the same graphic as a price, a promo code, an
affiliate link, or the word "premium."

## Paid options, if we ever want current-game wire photos

Not bought, and not needed yet — logged so the decision is on record.

| Service | What it is | Realistic fit |
|---|---|---|
| **Imagn** (USA TODAY Sports) | Wire photos, huge local-photographer network | The one to call first. Built for digital-first publishers our size. |
| **AP Images** | Wire service, tiered publisher licensing | Solid second option. |
| **Getty** | The most complete coverage there is | Premium pricing. Overkill until revenue exists. |
| **Adobe Stock / Shutterstock** | Conceptual stock on subscription | Only worth it if Unsplash runs dry, which it has not. |

At $145/mo of running cost and no revenue, none of these clear the bar. Revisit
when affiliate money lands.

## Adding a photo

1. Add an entry to `data/photo_manifest.json`.
2. Commit and push. The workflow fires on that path.
3. `git pull` — the files are in `assets/photos/`.

Never commit a photo by hand. If it is not in the manifest, nothing records its
license, and an uncredited file in the library is one we cannot safely use.

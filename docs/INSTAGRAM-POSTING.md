# Instagram posting — the process, going forward
**Written Fri Sep 11, 2026. Supersedes every earlier hand-off note.**

## The short version

Post from the Mac. Instagram's web uploader accepts Reels directly — no phone,
no Photos app, no messaging yourself.

1. Open **insidethenumber.com/post**
2. **Save video** → lands in `~/Downloads`
3. **Copy caption** → it's on the clipboard
4. **instagram.com** → **Create** (left sidebar) → **Select From Computer** → pick the file
5. Paste the caption → **Share**

Under a minute per Reel once you've done it twice.

---

## Why this replaces the old flow

The old process assumed an iPhone: download the file in Safari, hit the share
icon, **Save Video** to Photos, then open the Instagram app and pick it. That
works on iOS. On macOS it doesn't — a download lands in Downloads as a file,
and getting it into Photos is a separate import step Instagram's app can't
reach anyway, because there is no Instagram app for macOS. Chuck was
AirDropping/messaging the files to himself to bridge the gap. That bridge is
unnecessary; the web uploader has supported Reels from desktop since 2023.

**That was my error, not a platform limitation.** I built the page for the
wrong device.

---

## What the web uploader can and can't do

**Works on desktop web:**

- Reel upload (MP4/MOV, H.264)
- Caption, hashtags, emoji
- Tagging accounts
- Location
- Cover-frame selection
- Scheduling (Creator/Business accounts — Instagram's own scheduler, up to 75 days out)

**Mobile app only — not available on web:**

- **Trending audio library.** You cannot attach an Instagram audio track from desktop.
- Stickers, text effects, filters, green screen, the whole editing suite
- Collabs (co-author posts)

### The audio question

Posting from desktop means the Reel goes up with its own audio only — which
for our cards means silence. Two reasons that's the right trade anyway:

1. **We already ruled out trending audio.** A recognisable commercial track on
   an account carrying sportsbook affiliate links is a takedown and
   brand-safety risk that a small reach bump doesn't justify. That call is in
   `docs/DECISIONS.md`.
2. **These are data cards, not performance video.** Numbers on screen, read
   silently on a muted feed. Audio isn't carrying the content.

If we ever want music on a specific Reel, the phone path still exists and is
documented at the bottom of `/post`. The music selector lives **only** on the
Instagram app's editing screen — once you tap the arrow past it, you can't go
back and add it.

---

## Technical specs — all our Reels already conform

| Requirement | Instagram web | Our reels |
|---|---|---|
| Container | MP4 or MOV | MP4 ✓ |
| Codec | H.264 | H.264 ✓ |
| Aspect | 9:16 (1080×1920 ideal) | 1080×1920 ✓ |
| Duration | 3–90 seconds | 8.0–9.8s ✓ |
| Frame rate | 23–60 fps | 25 fps ✓ |
| File size | under 100 MB | 80 KB–555 KB ✓ |
| Browser | Chrome, Safari, Edge, Firefox | — |

`scripts/` already renders to exactly this spec. **No re-encoding is needed,
and none should be added.** If a future reel fails to upload, check duration
first (under 3s is the likeliest miss), then codec.

---

## Where the files come from

Each Reel ships as a pair on the live site:

- `/reelN.mp4` — the video
- `/rN.txt` — the caption, plain text

`_headers` sets `Content-Disposition: attachment` on the MP4s so clicking
downloads rather than opening an inline player. `/post` reads the `.txt` files
live with a cache-buster, so a caption edit pushed to the repo shows up on the
page immediately — no page redeploy needed.

To queue a new Reel: drop `reelN.mp4` and `rN.txt` in the repo root, add the
`_headers` block for the new MP4, and add a card to `post.html`. Note the repo
`.gitignore` is an **allowlist** — new files need `git add -f` plus an explicit
`!filename` entry, or they will silently not deploy.

---

## The real fix, still outstanding

All of the above is still a manual hand-off. The actual unlock is the
**Instagram Graph API**, which turns Reels into a queue exactly like X:
files in a folder, a GitHub Action posts them on schedule, nobody touches a
browser.

It needs ~45 minutes of Chuck-only setup, once:

1. Instagram settings → Accounts Center → link the Creator account to a Facebook Page
2. developers.facebook.com → create an app → add Instagram Graph API
3. Generate a long-lived access token (60 days, auto-refreshable)
4. Hand over the token + Instagram Business Account ID

After that, "2× a day without you" is real. Until then, `/post` is the process.

---

## Caption rules — as of Sep 11, 2026

These are standing rules. Every `/rN.txt` follows them; no exceptions without
Chuck saying so.

### Hashtags: 3–4. Hard ceiling of 5.

Not ten, not eleven. Pick the ones a human would actually browse:

- one sport (`#nfl`, `#cfb`, `#mlb`)
- one or two topic tags (`#sportsbetting`, `#bettingtips`)
- one specific tag tied to what the Reel is literally about (`#keynumbers`,
  `#vig`, `#pointspread`, a team)

Drop the volume tags that were padding the old captions — `#nflpicks`,
`#linemovement`, `#bettingeducation`, `#sportsbook`, `#juice`. They add no
discovery and they read like spam on a small account.

### Tags: one or two, and only when they're honest.

Tag an account when the Reel is **about** that account — the teams playing, the
league, a book whose price we actually name on screen. A Rams/49ers Reel gets
`@rams @49ers`. A generic no-vig explainer gets nothing, because there is no
account it's about, and tagging a big handle to farm its audience is what
everyone else does and it doesn't work.

**No tag is better than a forced tag.** `r5.txt` ships untagged for exactly
this reason.

### No compliance line in the caption.

`21+ · 1-800-GAMBLER` is off Instagram captions as of Sep 11 — Chuck's call.
Nobody is watching these yet and it was eating the first-line preview.

**Scope of that removal:** Instagram captions and the `/post` page only. The
disclaimer stays where it actually matters and where removing it would be a
real decision: the site footer, the legal pages, the on-image social cards
(`scripts/build_social_card.py` and friends), and the newsletter. Revisit when
there's an affiliate deal or real traffic — whichever lands first.

### Structure

Front-load. Instagram truncates after roughly the first line, so the hook has
to survive on its own. Then short paragraphs, one idea each. `Link in bio.`
Then tags, then hashtags, on their own lines at the bottom.

---

## Cadence

Two posts a day, per the daily checklist: **9:30 AM** and **5:00 PM CT**.
Reels get queued at `/post` the night before, so the morning slot is a
30-second job.

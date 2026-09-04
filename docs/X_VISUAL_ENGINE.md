# Inside the Number — X Visual Content Engine

**Adopted Sep 3, 2026.** This is the standing process for every X post and
marketing asset from tonight forward. Chuck supplied the architecture; this
document maps it onto the tools we actually have, records what already exists
in the repo, and corrects the parts that would get the account picked apart.

Read this before producing anything for X.

---

## 0. The one-sentence version

Claude is the content director. The current sports conversation on X is the
source of the *moment*. Our verified numbers are the source of the *content*.
Canva turns the idea into a branded asset only when a branded asset is the
strongest visual. The GitHub Actions poster publishes, with the image, through
the X API. Nothing goes out that hasn't been read once by a human in Phase 1.

---

## 1. Truth table — what is connected tonight

| Layer | Plan says | Actual state (Sep 3, 2026) |
|---|---|---|
| Canva → Claude | "Connect first" | **Connected and proven.** Four designs built today, edited element-by-element, exported. Connector supports brand kits, brand templates, autofill datasets, and `create-design-from-brand-template` — which is how the "10 templates" get built properly. |
| X publishing | "X API" | **Exists.** `scripts/post_queue.py` + `.github/workflows/x-posts.yml`. Runs on a GitHub runner (which can reach `api.x.com`; the sandbox and browser cannot). Uploads an image if a same-stem file sits next to the `.txt`. Cron **disabled** Sep 2 by Chuck; `workflow_dispatch` still fires a deliberate one-off. This *is* Phase 1. |
| X research | "X API search" | **Works via Chrome.** Search, read threads, read engagement counts. No API needed for research. |
| GIPHY | "GIPHY API" | **No connector exists** in the registry. X's own composer has a GIF picker (GIPHY/Tenor-backed) that Chrome can drive. That covers reaction posts. |
| Sports photos | "current photo" | See §3 — real-person photos are a publicity/NIL problem. Quote-posting the viral post is the legal version of the same move. |
| Odds data | "your model/data" | ESPN scoreboard with **open and close** on moneyline, spread, total. Slate builder captures it nightly. Verified in-browser before anything ships. |
| Image gen | "AI-generated" | Cloudinary `generate-image` (5 model families, **3 generations left** on the quota); Canva's own stock; Gemini Pro via Chrome. |
| Analytics | "feedback loop" | `posts/.sent.json` records every post's id, url, chars, had_link, had_image. Engagement is read off X in Chrome. |

**Net:** steps 1, 3, 4 and 6 of the build order are already done or working.
What's left is the brand kit + templates (step 2), GIPHY-equivalent via the
composer (step 5), and a written analytics pass (step 7).

---

## 2. The pipeline, as it actually runs

```
CURRENT SPORTS WORLD  (X search in Chrome; ESPN board in browser)
        ↓
CLAUDE — finds the moment, asks "is there an Inside the Number angle?"
        ↓
CLAUDE — picks the visual format (§3). Not every post gets a graphic.
        ↓
   ┌────────────────────────┬──────────────────────────────┐
   │ PIPELINE A — reaction  │ PIPELINE B — branded          │
   │ quote-post / GIF /     │ verified number → Canva       │
   │ screenshot / text      │ brand template → export       │
   │ straight to X          │ → posts/NNN.txt + NNN.jpg     │
   └────────────────────────┴──────────────────────────────┘
        ↓
CLAUDE — writes the copy. Every number re-verified at write time.
        ↓
CHUCK — approves (Phase 1)
        ↓
X — via workflow_dispatch on "X posts" (image rides along automatically)
   or via Chrome for replies and quote-posts
        ↓
ANALYTICS — .sent.json + X engagement read → what to do more of
```

The Sep 3 lesson that shaped this: six rounds of graphics were rejected
because every one crammed analysis *into the image*. The post that worked put
**one number on the image** and **the reasoning in the tweet text**. That is
the Bet Labs pattern and it is now the rule.

---

## 3. Visual decision system

Ask, in this order, and stop at the first yes:

1. **Is the moment already on X as an image or video?**
   → Quote-post it. That is what "use a current photo" means for us. We do not
   download and re-upload other people's photos of players or coaches.
2. **Is it primarily a reaction?** → GIF from the X composer's picker, ≤10 words.
3. **Is it funny, absurd, or predictable?** → Meme. Existing if one fits,
   original via Canva "MEME" template (large image + ≤10 words) if not.
4. **Do we have a number nobody else is showing?** → Branded graphic (§4).
   One number as hero. Reasoning goes in the text.
5. **Is it our own product?** → Screenshot of the game page or board. Half of
   Chuck's reference set was product screenshots.
6. **Is there no good existing visual and the idea is visual?** → AI image.
   Prompt rules: no faces, no logos, no jerseys, no readable signage, ask for
   empty space for the caption, never ask for a table or chart.
7. **Otherwise** → text only. A sharp text post beats a decorative image.

### Hard limits (these override everything above)

- **No real-person photography attached to a pick.** Right of publicity, and
  NIL on top of it for college athletes. Quote-post instead.
- **Team logos are fine** in a factual sports context. We have 860 cached at
  `insidethenumber.com/assets/logos/{league}/{ABBR}.png`.
- **No fabricated ticket or money splits.** We do not have that data. Quoting
  someone else's (e.g. br_betting via FanDuel, 69%) is allowed **only with
  credit in the same post.**
- **No claimed model edge, no "ITN MODEL" number, no public W/L, ROI or units.**
  Standing rule from `docs/DECISIONS.md`. The plan's MODEL VS MARKET, FADE
  ALERT and MODEL EDGE templates are therefore **not built** (see §4).
- **Never "sharps moved it."** We say the line moved. We do not say who.
- **Every number on a graphic is re-pulled at build time**, not copied from a
  brief. Sep 3: the brief said 29.8% → 32.5%; the true de-vigged pair was
  28.6% → 32.5% because 29.8 was raw and 32.5 was de-vigged. Caught only
  because the number was re-derived before posting.
- **Read every string on a generated image before it ships.** Canva invented
  "WEIGHS - 3.5%", "Ubasti Tobemazon", and a mislabeled block today. Ideogram
  invented a table. Three hallucinated stats in one day.

---

## 4. The ten Canva brand templates — corrected list

Build these as **Canva brand templates with autofill fields**, so a post is:
pull numbers → fill dataset → `create-design-from-brand-template` → export.
Five minutes per post, not fifty.

| # | Template | Hero (autofill) | Sub (autofill) | Accent | Status |
|---|---|---|---|---|---|
| 1 | THE NUMBER | one figure (`-100000`, `0`, `68`) | one line of meaning | amber | **prototype shipped Sep 3** (Saturday "0") |
| 2 | LINE MOVEMENT | `OPEN → NOW` spread | ML open → now | amber | **prototype shipped Sep 3** (Colorado B) |
| 3 | FAIR PRICE | de-vigged % open → now | "de-vigged from -290/+235" | green | prototype in B |
| 4 | THE HOLD | overround % (`104.3%`) | "the extra 4.3% is the house" | red | to build |
| 5 | BREAK-EVEN | win % needed at price | "what -238 actually asks" | white | to build |
| 6 | THE BOARD | tonight's games, closest first | count of blowouts | blue | `viz.py stack` exists; port to Canva |
| 7 | WTF NUMBER | absurd figure | "WAIT… WHAT?" | amber | to build |
| 8 | TEAM CARD | two logos on team-colour panels | pick + one number | team colours | **shipped Sep 3** (Colorado B) |
| 9 | CREDITED SPLIT | `69%` with `via @source` baked in | our number beside it | white | to build — this replaces "PUBLIC vs MODEL" |
| 10 | MEME | large image | ≤10 words | none | to build |

**Dropped from the plan, on purpose:** MODEL VS MARKET, FADE ALERT, MODEL
EDGE, and any "PUBLIC %" without a credited source. They require data we do
not have or claims we have decided not to make. "FADE ALERT" in particular is
the format that produces receipts against you.

Brand kit to create first (Canva → Brand): logo, `#07090d` ground, green
`#00e08a`, amber `#ffb020`, blue `#1d9bf0`, Colorado-style vegas gold for
warmth, condensed display face + clean sans, 1600×900 as the X master size.

---

## 5. Master prompt — the brain

This is Chuck's instruction, merged with the hard limits above. It is what
the hourly X task runs on once re-enabled.

> **Inside the Number — X Visual Content Engine**
>
> For every candidate post, first identify the emotional or conversational
> angle: humor, disagreement, surprise, a number that shouldn't exist,
> betting psychology, a price moving before anyone played. If there is no
> angle, there is no post.
>
> Then decide whether a visual materially increases the chance someone stops
> scrolling. Never attach a generic image because the post "needs one."
> Choose the strongest format in this order: current viral post (quote it),
> reaction GIF, existing meme, original meme, Inside the Number data graphic,
> AI image, short video, no visual.
>
> When a data graphic wins: **one number is the hero. The reasoning goes in
> the tweet.** Re-derive every figure from the live board before writing it
> down. De-vig both sides from the same overround. Read every string on the
> rendered image before it ships.
>
> Return, for each post: POST IDEA · HOOK · X COPY · VISUAL TYPE · VISUAL
> CONCEPT · SEARCH TERMS (if existing media) · CANVA TEMPLATE (if branded) ·
> EXACT ON-IMAGE TEXT · CTA if any · LINK only when it adds value.
>
> Never: fabricated splits, claimed model edge, W/L, ROI, units, "sharps",
> real-person photos on a pick, or a table in a generated image.
>
> Banned phrases: "here are today's picks", "don't miss these picks", "check
> out our latest predictions", "bet smarter", "let's dive in", "lock",
> "free money."
>
> The account is an intelligent, entertaining sports-and-numbers account
> first and a business second. One link in four posts, never in a reply.

---

## 6. Publishing — Phase 1 mechanics

Phase 1 = Claude creates, Chuck approves, Claude dispatches.

**Original posts with an image:**
1. Save `posts/NNN-slug.txt` (≤280 chars) and `posts/NNN-slug.jpg` (or .png)
   with the **same stem**. Lower sort key = posts first. Use a `000-` prefix
   to jump the queue.
2. Commit and push to `main` (fresh clone, space-free temp dir, ITN Desk
   author — see `docs/GIT_WORKFLOW.md`).
3. Chuck approves in chat.
4. Trigger **Actions → "X posts" → Run workflow**. The poster sends the next
   unsent item with its image and records the URL in `posts/.sent.json`.
5. Verify at `x.com/thenumberdesk`.

**Replies, quote-posts, GIF reactions:** Chrome, directly. Rules: one reply
per account per day, never a link in a reply, click the field's screen
coordinates (the composer drops typed text otherwise), verify each at source.

**Expired items:** move to `posts/expired/`, never delete. A Thursday board
must not post on Saturday because it was next in line.

Phase 2 (Chuck approves categories, not posts) and Phase 3 (low-risk posts
auto-publish — replies with verified numbers, the morning board) come after
two clean weeks of Phase 1. Re-enabling the cron is a one-line change plus the
scheduled task; it is logged in `docs/DECISIONS.md` and is Chuck's call.

---

## 7. Daily rhythm

Not ten posts at 8 AM. Spread through the day, each slot a different format.

| CT | Slot | Format | Source |
|---|---|---|---|
| 8:00 | Morning numbers | THE BOARD or THE NUMBER + link | slate brief |
| 11:00 | What's moving on sports X | quote-post or reply round | Chrome search |
| 1:00 | Reaction | GIF or meme, ≤10 words | X composer picker |
| 3:00 | Price post | LINE MOVEMENT / FAIR PRICE / THE HOLD | ESPN open→now |
| 5:00 | Pre-game | TEAM CARD on the pick | site POTD |
| Game | Live | text first, graphic only if a number swung | live board |
| 10:00 | Tomorrow | teaser + link | next day's board |

Two originals a day carry a link at most. Replies never do.

---

## 8. Analytics loop

`posts/.sent.json` already stores id, url, chars, had_link, had_image per
post. Each morning: read engagement off X for yesterday's posts, append
views/likes/replies to the history entry, and note the format. After 14 days,
rank formats by median views and cut the bottom third. First data point,
Sep 2: **every text-only post got 8–36 views; every competitor post Chuck
pulled carried an image.** Images are the default now.

---

## 9. Build order — where we are

1. ~~Connect Canva → Claude~~ **done Sep 3**
2. Brand kit + 10 brand templates with autofill — **next**; two prototypes shipped
3. ~~Master X prompt~~ **§5 above; `docs/X_TASK_PROMPT.md` carries the hourly version**
4. ~~Current X research~~ **working via Chrome**
5. GIF reactions via X composer picker — **to test on first reaction post**
6. ~~X publishing~~ **exists; Phase 1 via workflow_dispatch**
7. Analytics pass in the morning health check — **to add**

---

## 10. Tonight, Sep 3 — the plan

- **Posted (manual, verified live):** Colorado +6.5 TEAM CARD with link, 4:55 PM CT.
- **Replies posted (verified):** @SBBreakers 22K, @YahooSports 8K, @ChaseDaniel 35K.
- **Queued for ~10 PM CT via the poster:** Saturday THE NUMBER ("0" ranked-vs-ranked) + link. Needs Chuck's go.
- **Reply round at 7:00 CT kickoff and one mid-game**, numbers from the live board only.
- **Expire** `posts/0000-cfb-thursday-board.*` so it cannot post tomorrow.
- **Tomorrow morning:** build the brand kit and the first four autofill templates (THE NUMBER, LINE MOVEMENT, FAIR PRICE, TEAM CARD) from tonight's shipped designs.

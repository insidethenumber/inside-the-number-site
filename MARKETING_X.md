# Inside the Number — X playbook (v2, rewritten Aug 29 2026)

Internal. Excluded from the deployed site via `.assetsignore`.

**This is a full rewrite.** v1 was written in August 2026 and produced 20 followers
and posts averaging 5–17 views. It was not a bad document; it was a document for a
different platform than the one we're actually on. Everything below is grounded in
engagement data scraped live from ~50 competitor posts on Aug 29 2026
(see `X_TEARDOWN_AUG29.md` for the raw findings).

---

## 0. WHAT KILLED v1 — read this before you write anything

Four rules in v1 were actively suppressing us:

| v1 rule | What it actually did | v2 replacement |
|---|---|---|
| "Every post has a number in it. **No exceptions.**" | Made every post read like a Bloomberg terminal. Got us publicly called "AI." | **Every post must be TRUE. Numbers optional.** |
| "Target ~150 characters" | Fine, but paired with the numbers rule it produced identical-shaped posts forever | Length varies by format. Some posts are 6 words. |
| Three posts a day | At 20 followers, our ceiling is surface area, not quality | **10–20 posts/day**, mostly templated + replies |
| No mention of images anywhere | We shipped 200+ text-only posts into a visual feed | **Media on everything that isn't a reply** |

The single hardest lesson from the teardown: **Action Network's best-performing post
on a Saturday with a full slate was "WAKE UP IT'S COLLEGE FOOTBALL SATURDAY!!!!"** —
no numbers, no analysis, no link. 10.5K views. Emotion outperformed their own data.

---

## 0.5 — THE BIGGEST FINDING. READ THIS TWICE.

**Measured Aug 29 2026, searching CFB posts with 2,000+ likes.** Here is what was
actually winning on the biggest college football Saturday of the year:

| Post | Likes | Media? | Data? |
|---|---|---|---|
| @BarstoolGruden — "Time to watch college football." | **17,957** | no | none |
| @espn — "We missed you very much, welcome back college football." | 12,678 | yes | none |
| @CFBHome — "WE SHOULD BUILD ENORMOUS STADIUMS ON COLLEGE CAMPUSES" | 4,154 | no | none |
| @CollegeFBonX — "TCU's offensive coordinator today" | 2,852 | image is the punchline | none |
| @ESPNCFB — "A DUBLIN DUB FOR BELICHICK & THE TAR HEELS" | 2,467 | no | none |
| @3YearLetterman — "College football should only be played on American soil" | 2,092 | no | none |

**Not one has a chart. Not one has a number. The best post of the day was five words.**

This platform runs on **feelings**, not information. Emotion, shared opinions,
jokes, and moments. We had been building data visualizations for a feed that
rewards relatability. Charts are *informative*. These are *relatable*. That is the
entire gap and no amount of design polish on a spread-and-total card closes it.

### The four registers that actually work

1. **Pure emotion** — "Time to watch college football." No data. Just the feeling
   everyone in the timeline already has, said first and said plainly.
2. **A take people can argue with** — "a 37-point spread isn't a betting line, it's
   a threat." Opinions get quote-tweeted. Facts get scrolled past.
3. **The relatable gut-punch** — "Somewhere a guy has USC -37.5 and is watching a
   28-0 game with his head in his hands. We've all been that guy." Name the shared
   experience. The number is a prop, not the point.
4. **Setup line, image is the punchline** — "whoever set the USC number this
   morning" + graphic. The caption is the joke; the graphic is the reveal.

**Where graphics belong:** as the punchline under a funny setup line. NEVER as the
post itself. A beautiful card under a boring line still dies.

**Where numbers belong:** in a supporting role. One per post, maximum, and often
zero. The number makes the joke land — it is not the joke.

---

## 1. THE HOOK IS THE WHOLE GAME

The account we should be copying is **@trendscenterapp** — similar size to us, and
one post did **43K views / 224 likes / 17 reposts** against Action Network's typical
10K views / 20 likes. Their post:

> ⚠️ PERFECT TREND ALERT ⚠️ White Sox overs after a rest day:
> **17-0 to the over**
> Active on White Sox at Twins o8.5

Deconstructed, in order of what did the work:

1. **An extreme, checkable number.** "17-0" sounds impossible. You stop to check it.
2. **A scarcity label.** "PERFECT TREND ALERT" says *this is rare*, so it earns a look.
3. **Immediately actionable.** Names the live bet.
4. **Graphics support it.** They do not lead it.

### The rule that replaces everything in v1

> **First line = the most surprising true thing we know.**
> Not the setup. Not the context. The punch.

| ❌ Dead on arrival | ✅ Stops the scroll |
|---|---|
| "Stanford's spread went from -3 to -4.5 while the total came down from 50.5 to 48.5" | "**3 of today's 8 games are already decided.**" |
| "The break-even on this price is 67%" | "**You need to win 2 out of 3 just to break even.**" |
| "USC is favored by 37.5 points" | "**The market says USC wins by five touchdowns.**" |
| "Here is today's free pick" | "**One number on this board moved 3.5 points and nobody noticed.**" |

---

## 2. SCARCITY LABELS — use one, every time

Every post looking equally important means none of them do. Competitors all have
labels. Ours:

- `⚠️ NUMBER NOBODY IS TALKING ABOUT` — a line move with no obvious cause
- `🚩 THE MARKET DISAGREES WITH ITSELF` — spread and total moving opposite directions
- `📌 DECIDED BEFORE KICKOFF` — mismatch call-out
- `🧾 THE RECEIPT` — break-even math on somebody's parlay
- `✅ TODAY'S FREE PICK` — the daily
- `📊 THE WHOLE BOARD` — slate roundup

Never invent a label to make a boring post sound urgent. If nothing qualifies, post
something funny instead, or post nothing.

---

## 3. VOICE — 2026, not 1920

We got called "AI" in public on Aug 28. The tell was never one post — it was the
**pattern**: every reply built as [stat] + [percentage] + [tidy market conclusion].
Templates are what get you clocked.

**Write like a sharp friend at the bar who happens to know the numbers.**

Do:
- Have a reaction FIRST, put the number in a supporting role or leave it out
- Incomplete sentences. Start with "lol" or "man." Ask rhetorical questions
- Sarcasm, punching UP — at books, prices, touts, TV narratives
- Take a side without hedging
- React to the specific thing someone said, not adjacent to it

Never:
- More than one stat per reply. Many replies get zero
- Hashtags in replies. One event tag on originals, sometimes
- Explaining the joke
- Anything that could be auto-generated about any game by swapping nouns —
  if it passes that test, delete it
- Replying to "you're a bot" accusations. **Silence.** Arguing amplifies it

**Never punch down** — not at fans, not at players having a bad night, not at people
who lost a bet. Celebrate wild finishes. Warmth wins followers; snark loses them.

---

## 4. MEDIA — attach something to every original post

Six formats are built and live in `scripts/build_social_card.py`. All generate from
live odds data in about two seconds.

| Format | When to use | Hook it carries |
|---|---|---|
| **Tier list** (S/A/B/F) | Saturday slates | Argument bait — people quote-tweet to disagree |
| **Group chat** | Parlay math, bad-beat logic | Funniest thing we make. Screenshot-and-send |
| **The divergence** | Spread up + total down | Makes an invisible insight obvious |
| **Big number** | One number translated to English | Most shareable |
| **Board card** | Whole slate, color-coded | Reference object people save |
| **Line-move GIF** | Any meaningful move | Motion in a still feed. Nobody else does this |

**Graphics support, they never lead.** A great card under a boring first line still dies.

### Meme formats we can build from scratch (no copyright exposure)

These are *layout parodies* — instantly recognizable, built from nothing:
- **Group chat / iMessage** (built)
- **Tier list** (built)
- **Notes app apology** — for a genuinely wild bad beat
- **Spotify Wrapped** — season-in-review cards
- **Letterboxd review** — rate a game like a film
- **Airport departure board** — the slate as departures
- **Betting slip receipt** — the pick as a printed ticket
- **"POV:" cards** — first-person framing

### What requires Chuck (10 minutes, biggest visual unlock available)

Drop 5–10 images into `Inside the Number/stock/` and I composite our data over them.

**Sources with free commercial licenses:** Unsplash, Pexels, Pixabay.
**Search terms that don't look cheesy:** "stadium lights night", "empty stadium",
"football texture close up", "sports bar neon", "crowd silhouette", "turf macro".
**Avoid:** anything with visible faces, posed models, thumbs-up handshakes, or
"business people pointing at charts." That's the stock-photo look that reads as fake.
Dark, moody, textural, cropped tight — that matches our brand and looks expensive.

**What we do NOT use:** Getty/AP/team game photography, broadcast stills, or
reposted competitor graphics. Barstool and Bleacher Report post those because they
hold rights. We're about to apply to affiliate programs that ask about content
practices, and X removes posts on DMCA. Not worth it for a 20-follower account.

---

## 5. CADENCE — volume is the lever we never pulled

Action Network posts a templated best-bet for **every game on the board.** We posted
three times a day. That's the whole gap in surface area.

**Daily target:**
- **1 free pick** (~9am CT) — graphic attached, link in body
- **1 board card** (~11am CT on slate days) — the whole slate
- **3–6 per-game templated posts** — auto-generated, one per interesting number
- **1 personality post** — a joke, a reaction, no data required
- **1 meme-format card** — tier list, group chat, receipt
- **8–14 replies** — the hourly engagement task, unchanged in volume, upgraded in voice
- **1–2 plain reposts** — zero AI-tell risk, builds timeline texture

Skipped slots are free. A bad post costs credibility; an empty slot costs nothing.

---

## 6. LINKS

Link goes **in the body** of original posts. Chuck's call, Aug 29 2026, after a
two-post thread buried the link in a reply and he couldn't find it.

The reach cost of a body link is real but it's a rounding error at our size, and a
link nobody sees converts at zero. **Never split a post into a thread to hide a link.**

Replies carry no links. Ever.

---

## 7. HARD RULES (unchanged, still non-negotiable)

- **Never post about an event that has already started or finished.** Verify status
  live before every post. This burned us Aug 29 — we promoted odds on a UFC card
  that had ended eight hours earlier. Check the timestamp, not the calendar date.
- Never state a number you haven't verified **this hour**.
- Never claim a record, ROI, or units won. We don't publish one.
- Never say "lock", "guaranteed", "free money", "can't lose".
- Never mention the WNBA. Never say "vig", "juice", or "hold" — say "the book's cut".
- American spellings. 21+ framing where natural.
- Never expand a name from an initial without checking ("Colin" for Clay Holmes and
  "Wilmer" for Walbert Ureña both went out wrong).
- No betting jokes in threads about death, injury, tragedy, lawsuits, or politics.
- Do not take Ls publicly. When a pick loses, say nothing. The **only** exception is
  a plain factual error — fix or delete that immediately.
- No engagement bait, no follow-for-follow, no bought followers.

---

## 8. MEASUREMENT — the baseline to beat

As of Aug 29 2026: **20 followers. Posts averaging 5–17 views.** Site traffic
~320 visits/week. Newsletter: 2 subscribers.

Check weekly:
- Views per post (baseline: ~10)
- Follower delta
- Referral traffic to insidethenumber.com from X (Cloudflare analytics)
- Which format produced the top post that week — then do more of that

If a format produces nothing after two weeks, kill it. This document should be
rewritten again the moment the data says something different.

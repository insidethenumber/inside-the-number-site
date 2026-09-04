# Gemini graphics brief — Inside the Number

**How this works.** I write the caption and verify every number. You paste the
image prompt into Gemini, download the result, attach it to the post. Gemini is
better at pictures than anything I have; I am better at making sure the numbers
are real. Neither of us should do the other's job.

---

## PART 1 — THE STANDING ART DIRECTION

Give Gemini this once at the top of a chat, then paste individual prompts under
it. It keeps the look consistent across posts.

> You are making graphics for a sports-betting analysis brand called Inside the
> Number (@thenumberdesk). House style, applied to everything:
>
> - Near-black background (#07090d to #101521), subtle film grain, never pure flat black
> - ONE saturated accent per image. Our green is #00e08a. Amber #ffb020 for line movement, blue #1d9bf0 for slate/board posts
> - Typography is heavy condensed sans — Anton, Impact, Druk energy. Tight, tall, aggressive
> - The number is the hero. It should be the largest thing in the frame by a wide margin
> - Maximum three short lines of text total. Never a paragraph
> - Generous empty space. Crowded reads as amateur
> - 16:9 landscape, 2K
> - Sports broadcast graphic energy — think ESPN bumper, not infographic

### The five rules that stop it going wrong

1. **Never ask for a table, chart, stat grid, or leaderboard.** This is the big
   one. Ask for a table and the model invents rows of gibberish — we got
   "LIECIS", "BOLITARTS", "DODLIM" in a graphic that otherwise looked perfect.
2. **Keep total text under about eight words.** Short strings render correctly.
   Long ones garble.
3. **Spell out the exact text in quotes** — `reading exactly "COLORADO +6.5"`.
   Don't describe it, dictate it.
4. **For photography: no logos, no jerseys, no faces, no readable signage.**
   Say it explicitly in the prompt. Protects us on trademark and likeness, and
   stops the model inventing fake team marks.
5. **Ask for empty space where the caption goes** — "leave the lower third dark
   and uncluttered."

### If the text comes out garbled

Ask Gemini for the image with **no text at all**, then we add the words
ourselves. A clean photo with our type on top always beats a busy graphic with
one misspelled word in it.

---

## PART 2 — FOUR POSTS, READY TO GO

**All numbers verified against ESPN's live board at 3:35 PM CT, Thursday Sep 3.**
Lines move. If you post more than an hour from now, ping me and I'll re-check.

---

### POST 0 · PICK OF THE DAY — Colorado +6.5 at Georgia Tech

**This is the flagship post of the night.** Kickoff 8:00 PM ET. Numbers pulled
and posted on at 3:23 PM CT.

**The story:** Georgia Tech opened −7 and −290. It is −6.5 and −238 now. Neither
team has played a snap this season. The number moved *toward the underdog*
anyway. That is a real, checkable, differentiated observation — and it is the
reason for the pick, not decoration on top of it.

**Caption (this is the post text — copy it exactly):**
```
Georgia Tech opened -7 and -290 tonight.

It's -6.5 and -238 now.

Both teams are 0-0. Nobody has thrown a pass, missed a tackle or blown a coverage. The number moved anyway — and it moved toward the dog.

Colorado +6.5, 8:00 ET.
```

**Optional first reply, if you want the math in the thread:**
```
-238 and +195 add up to 104.3%. That extra 4.3% is the house, not a probability.

Strip it out and the market has Georgia Tech at 67.5% — not the 70.4% the price is charging you for.

Full number → insidethenumber.com
```

---

#### Graphic direction — what we're going for

The hero is **the move**, not the pick. Every capper on X tonight is posting a
side. Almost nobody is posting *the number changing shape before anyone played*.
So the image should be two numbers and an arrow, or a photograph of an empty
field — both say "nothing has happened yet and the price already moved."

Accent is **amber #ffb020**, not our green. Amber is our line-movement colour;
green is for the board. Using it correctly is how the account starts to look
like it has rules.

**Run both prompts below and pick.** They're cheap, and I'd rather you choose.

**Version A — the type card (bolder in a timeline, more likely to garble)**
```
A bold sports betting broadcast graphic on a near-black background, colour
#07090d, with subtle film grain. Centred in the frame, two pieces of
enormous heavy condensed sans-serif text side by side. On the left, "-7" in
dim grey with a thin horizontal strike-through line through it. On the
right, "-6.5" in bright amber, colour #ffb020, noticeably larger than the
grey number. Between the two numbers, a simple amber right-pointing arrow.
Above them, small white uppercase text reading exactly "NOBODY HAS PLAYED A
DOWN". Extreme scale contrast, generous empty space, very high contrast,
ESPN broadcast title-card energy. 16:9 landscape, 2K. No tables, no charts,
no logos, no other text or numbers anywhere in the image.
```

**Version B — the photograph (safer, more premium, my pick)**
```
Photorealistic cinematic photograph, no text anywhere in the image. An empty
college football stadium at dusk, shot low from the sideline looking across
untouched freshly painted turf. Stadium floodlights just coming on, long
shadows, heavy atmospheric haze, not a single person in frame, deep shadows
in the upper stands. Moody, quiet, anticipatory. Film grain, shallow depth
of field. Leave the lower third dark and uncluttered for a caption. 16:9
landscape, 2K. No logos, no jerseys, no faces, no readable signage.
```

**Why B is my pick:** an empty field *is* the argument. The caption says nobody
has played a down; the picture shows it. And a photo with no text in it cannot
misspell anything — which is the failure mode that ruined two graphics today.

**If you go with B**, send me the file and I'll run it through `hero.py stamp`
to lay "−7 → −6.5" and the footer over it in our type. That gets you Gemini's
photography with our numbers, which is the whole pipeline working as designed.

**If A comes back garbled**, don't try to fix it in Gemini — ask for the same
image with no text at all and I'll typeset it.

---

### POST 1 · THE NUMBER — two −100000s in one night

This is the strongest one. It is genuinely absurd and completely true.

**Caption:**
```
There are two -100000 moneylines on the board tonight.

Utah against Idaho. Delaware against Merrimack.

A hundred grand to win a dollar. Twice.

Delaware opened -8000 this morning. 👀
```

**Gemini prompt:**
```
A bold sports betting graphic on a near-black background with subtle film
grain. Enormous heavy condensed sans-serif text filling most of the frame,
in bright neon green, reading exactly "-100000". Beneath it, much smaller
white uppercase text reading exactly "TWICE. TONIGHT." At the very bottom
left, small grey text reading exactly "INSIDE THE NUMBER". Sports broadcast
title-card design, extreme scale contrast, generous empty space, high
contrast. No tables, no charts, no other text or numbers anywhere.
```

---

### POST 2 · MARKET MOVERS — same night, opposite directions

**Caption:**
```
Two games tonight, two lines running away from each other.

Wake Forest opened -22.5. It's -27.5 now.
Buffalo opened -24.5. It's -18.5 now.

Five points one way, six the other, same Thursday. Somebody's number was wrong at open.
```

**Gemini prompt:**
```
A bold sports betting graphic, near-black background with film grain, split
into two halves by a thin vertical amber line. On the left half, a large
white upward arrow. On the right half, a large white downward arrow. Above
them, small amber uppercase text reading exactly "SAME NIGHT". No other text
or numbers anywhere in the image. Minimal, graphic, high contrast, sports
broadcast design with lots of empty space.
```

---

### POST 3 · FOURTH QUARTER — the joke

Everyone is fading Colorado tonight; @br_betting had 69% of bets on Georgia
Tech and it's trending. This is the relatable version.

**Caption:**
```
college football is back which means it is once again time to watch a team you have never seen play, at a stadium you have never been to, for money you did not have to risk

see you at 8 💀
```

**Gemini prompt:**
```
Photorealistic cinematic photograph, no text anywhere in the image. A man in
his thirties sitting alone on a couch in a dark living room, lit only by the
glow of a television off-camera, leaning forward with his hands on his head
in an expression of pained anticipation. Late evening, warm TV light, moody
and slightly comedic, shallow depth of field. Leave the top third of the
frame dark and empty. No logos, no jerseys, no readable signage, no visible
screen content.
```

---

### POST 4 · SATURDAY TEASER — the traffic driver

Post this late tonight or first thing tomorrow. It's the one that should carry
the link.

**Caption:**
```
Sixty-eight college football games on Saturday.

Exactly one is ranked against ranked: Clemson at LSU, LSU -10.

The other sixty-seven are priced too, and most of them are not close.

Every game, every number → insidethenumber.com/games
```

**Gemini prompt:**
```
Photorealistic cinematic photograph, no text anywhere. A massive college
football stadium at night, packed to the top deck, seen from low behind one
end zone looking up into the stands. Heavy haze and smoke lit by floodlights,
purple and gold light washing across the crowd, enormous sense of scale, deep
shadows, film grain. Leave the bottom third darker and uncluttered for a
caption. No logos, no jerseys, no faces, no readable signage.
```

---

## PART 3 — WHY THESE FOUR

They are deliberately four different *kinds* of object, because four variations
of the same card is what made the account look automated:

| Post | Type | Job |
|---|---|---|
| 1 | Pure typography | Stop the scroll with an absurd real number |
| 2 | Abstract graphic | Show we watch movement nobody else reports |
| 3 | Real photography | Make the account feel human |
| 4 | Atmospheric photo + link | Drive traffic on the biggest day of the week |

Rough order tonight: **1 now** (people are on the board), **3 around 7:00**
(pre-kickoff, peak relatability), **2 late** if the lines move again, **4 last
thing or tomorrow morning**.

## What I will not write

No ticket or money percentages of our own — we don't have that data, and
quoting somebody else's is only OK when we credit them, as in the br_betting
reply. No claim about *who* moved a line. No record, ROI or units. Those are
the three ways this brand gets publicly embarrassed and they're not worth one
good post.

# X post pack — Thursday, September 3, 2026

**NOT POSTED.** X stays disabled until Chuck approves `docs/MARKETING_PLAN.md`
§4.6. This is a review set.

**Every number below was pulled from the live ESPN board this morning and
re-checked at 10:00 AM CT.** Lines moved between the two pulls (Wake Forest
-24.5 → -25.5, Rutgers -29.5 → -28.5, Delaware -28.5 → -30.5); the graphics
carry the later numbers. Nothing here is invented. That is the one thing we
do not copy from the Gemini and ChatGPT mockups, which both carried made-up
stats and said so in their own footnotes.

## How these were made — the new pipeline

1. **Gemini Pro** (Chuck's account, driven in Chrome) generates the hero
   photography. Prompted for no text, no logos, no faces, no jerseys, and a
   deliberately empty area for the caption.
2. **`scripts/hero.py`** lays ITN's data, franchise chip, typography and
   footer over the photo, with a gradient scrim so white type survives a
   bright crowd.
3. **`scripts/viz.py stack`** handles the colour-blocked list format, which
   needs no photography at all.

Backgrounds live in `assets/heroes/`. To add more, generate in Gemini, drop
the file in, and reference it with `--bg`.

---

## 1 · THE BOARD — the morning service post (carries the link)

Image: `1-board.jpg` — night stadium, teal and gold.

> Eleven games on the Thursday board.
> Ten of them are decided by kickoff.
> One is a football game. 🏈
>
> Georgia Tech -6.5, Colorado +195, total 50.5, 8:00 ET.
>
> Full board and the live number → insidethenumber.com/games

## 2 · THE NUMBER — the ugly price

Image: `2-number.jpg` — a pile of cash with one crumpled dollar on top.

> Utah's moneyline against Idaho opened at -50000 this morning.
>
> It's -100000 now.
>
> The price doubled in a day, on a game where you already needed a second
> mortgage to win lunch money. 💀

## 3 · THE BOARD — Saturday teaser (carries the link)

Image: `3-saturday.jpg` — purple and gold night bowl, smoke in the lights.

> Sixty-eight college football games on Saturday.
>
> Exactly one is ranked against ranked: Clemson at LSU, LSU -10.
>
> Every one of the other 67 is priced too. → insidethenumber.com/games

## 4 · THE PRICE IS THE POINT — the differentiator

Image: `4-price.jpg` — stadium, copy on the left third.

> Georgia Tech -238 and Colorado +195 add up to 104.3%.
>
> That extra 4.3% isn't rounding. It's the house.
>
> Strip it out and the market has Georgia Tech at 67.5% — not the 70.4%
> you're paying for.

## 5 · THURSDAY NIGHT, PRICED — the reference object

Image: `5-stack.png` — every game tonight, colour-blocked, closest first.

Modelled on the @Novig "gauntlet" post from Chuck's reference set: left block
one colour, right block the opponent's colour, marks alongside. Theirs shows
a schedule. Ours shows the same object **priced**, which is the whole account
in one graphic. This is the format most likely to get screenshotted.

> Every college football game tonight, sorted by how close the market thinks
> it is.
>
> One inside a touchdown. Nine coronations.
>
> Save this one. 👀

---

## What I would post, and when, if X were on

| Time | Post | Link |
|---|---|---|
| 9:00 AM | 5 · Thursday night, priced | no |
| 12:30 PM | 4 · The price is the point | no |
| 4:00 PM | 1 · The Board | yes |
| 6:30 PM | 2 · The Number (Utah) | no |
| 9:30 PM | 3 · Saturday teaser | yes |

Plus reply rounds off `docs/MONITOR_LIST.md` through the Colorado–Georgia
Tech window, which is where the strangers actually are. Two links across five
originals is inside the one-in-four rule in §4.2.

## Honest notes

- Two team logos are missing from the cache (West Georgia, Merrimack) —
  ESPN's team endpoint and its scoreboard disagree on those abbreviations.
  The colour block still carries the row; a fallback already handles the
  common mismatches (Buffalo BUF/BUFF, UAlbany UALB/ALB).
- The hero photos are AI-generated and generic by design: no real player, no
  real logo, no real venue. That keeps us clear of likeness and trademark
  problems and it is why the prompts say so explicitly.
- Team marks on the cards are the real ones, used to identify the teams in a
  factual sports context — the same use every account in the category makes.

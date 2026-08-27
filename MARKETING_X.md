# Inside the Number — X playbook

Internal. Excluded from the deployed site via `.assetsignore`.

House style carries over from the newsletter: **no "vig", "juice" or "hold"**.
American spellings only. Posts go out as the publication, not as Chuck.

---

## 1. Profile

**Handle:** @thenumberdesk — claimed Aug 23, 2026.

Chosen after `@insidethenumber` came back reserved and every close variant was
taken. Two of those are worth remembering: `@insidethenum` is an ACTIVE NFL
analytics account literally called "Inside The Numbers", and
`@theinsidenumber` is a dormant XFL betting account with the same name. The
name is crowded on X, which is why we went with the byline instead of a
near-miss of somebody else's handle.

**Display name:** see note below — "Inside the Number" is the brand,
"ITN Desk" is the byline. Display names are free to change; the handle isn't.

**Bio** (160 char limit — this is 148):

> Every game on the board, priced at what the market really thinks. Free pick
> daily. Line moves, true prices, and the numbers other sites don't publish. 21+

**Location:** Nashville, TN
**Link:** https://insidethenumber.com
**Avatar:** `social/itn-avatar.png`
**Header:** `social/itn-x-header.png`

### Pinned post

> Most betting accounts sell you a record.
>
> We don't publish one.
>
> What we publish: every game on the board with the book's margin stripped
> out, so you can see what the market actually thinks — and what you'd have
> to hit to break even at the posted price.
>
> Free, every day 👇
> insidethenumber.com

---

## 2. Why this works as content

The site already computes things nobody else publishes free. Each one is a
post that takes ten seconds to read and links back to a live page:

| Data we have | Post angle |
|---|---|
| Biggest line move on the board | "This number moved further than any other today" |
| Break-even vs our number | "You need 67% to break even. We make it 71%." |
| Starter's last 3 starts vs season ERA | "His ERA says 4.53. His last three say 1.45." |
| Hot/cold bats, last 15 games | "They're 4-1 — with their three best hitters ice cold." |
| Injury report (IL, ranked by impact) | "Atlanta is starting this game without both aces." |
| Predicted score from the run model | "We make it 3.81–4.14." |

**Voice add-on (Chuck, Aug 25 2026, night): positive and human.** A sharp
friend at the bar, not a brand. Punch up at prices and touts, never down at
fans or players. Celebrate wild finishes. Warmth wins followers.

**SUPERSEDED Aug 27 2026 — do NOT self-deprecate on losing picks.** The line
above used to end "self-deprecate on our Ls" and that is now wrong. Chuck's
call, Aug 27: *"quit taking Ls. Make the pick and move on. No reason ever to
look back. It shows weakness and that you were wrong."*

Make the call, publish the number, move to the next one. Do not post a
scoreboard update on a pick that is losing, do not write "we'll take the L",
do not say "consider us corrected", do not revisit a pick after the fact to
mark it down. This is not about hiding results — the site already publishes no
record at all, deliberately (see the Aug 22 change). It is that a running
public commentary on our own losses reads as weak and gives away the frame.

If a pick is losing and something on that game is genuinely interesting, post
the interesting thing without grading ourselves. Two examples of the same
situation, one wrong and one right:

> WRONG: "Our free pick was McIlroy +850. He's +1. We'll take the L on day one."
> RIGHT: "Hovland and Min Woo Lee at -6 with no cut and three rounds left. The
>         two shortest prices on the board are both behind them."

Same facts, same honesty, no self-flagellation.

**And never apologize for a pick that missed.** Chuck, Aug 27 2026: *"Never
apologize for a missed or wrong pick. If someone wants to fact check you
everything is there, posted already. Saying you are wrong in a post makes it
look like we don't know what we are doing."*

The receipts already exist. Every pick goes out with a stated side, a real
number and the reasoning, timestamped, before the game starts — anyone who
wants to grade us can, and we have never hidden a single one. An apology adds
no information a reader could not already get. What it does add is doubt about
whether we knew what we were doing when we made the call, which is the one
thing the whole brand rests on.

**The line to hold, because it is easy to get backwards:**

- BEFORE the result — full honesty, always. State the confidence level, state
  what beats the bet, say when a number is thin or when we could not meet our
  own selection rules. The "what beats it" paragraph on every pick is a
  feature and it stays. That is confidence, not hedging: it shows we already
  considered the other side.
- AFTER the result — nothing. No grade, no apology, no correction, no "as we
  said". The pick stands where it was published and speaks for itself.

Correcting a factual ERROR is different from apologizing for a losing PICK.
If we publish a wrong number, a wrong pitcher or a wrong date, fix it fast and
plainly — accuracy is the product. A pick that lost is not an error; it is a
priced opinion that did not come in, and those are not the same thing.

**Reply cadence — HOURLY, 9am-11pm (Chuck, Aug 25 2026, evening).** Upgraded
from 4-5 rounds a day after the first full day produced 3 -> 12 followers and
the site's first-ever X referrals. Now automated: the scheduled task
`itn-x-engagement-hourly` runs a round at :07 past each hour, 9am-11pm, on
Chuck's Mac. Quality gates volume — a round with no good target does nothing.

**Reply cadence — original note (Chuck, Aug 25 2026, morning).** Replies are doing
far more for us than original posts. Followers went 3 → 6 in the twelve hours
after the first reply round. Voice: one or two lines, playful, an emoji, and
one real number. Fun, not a lecture. "Si Woo's +2300 this week. Scheffler
+320. Diaper money is recoverable 🍼" is the target — a joke that happens to
contain two verified prices.

Two failure modes. First, running the same move every time: three break-even
calculations in one round starts reading like a bot with a calculator. Vary
the shape — a price, a coincidence, a joke, an observation about a player.
Second, forcing the count. Four good replies beat five with a misfire; skip
lawsuit stories, fan accounts, and anything where the only available reply is
generic.

**Length rule — keep them short (Chuck, Aug 25 2026).** Target roughly 150
characters, hard ceiling 200. The 280 limit is not a target. Three short lines
beat one paragraph: people read the first two lines in a timeline and scroll.
When a post runs long it is almost always because we explained the reasoning
instead of stating the number and stopping. State the number. Stop.

**The rule: every post contains a real number.** No hype, no "LOCK OF THE
DAY", no unit talk. The differentiator is that we sound like an analyst and
everyone else sounds like a tout.

---

## 3. Daily cadence

Three posts a day, all generated from the board:

- **~9:00 AM CT — The free pick.** Same play as the newsletter, with the
  reasoning compressed to two lines. Links to the game page.
- **~2:00 PM CT — Biggest line move.** Price journey, which way money is
  going, what it implies.
- **~5:30 PM CT — One number.** The sharpest single stat off tonight's board
  — a starter trending hard, a cold lineup, a total that moved.

Volume is deliberately low. Three good posts beat fifteen filler ones, and at
$0.20 per post with a link it also keeps the bill near $18/month.

---

## 4. Launch posts — real numbers from tonight's board (Aug 23)

These are live and verifiable. Use them or the equivalents on the day.

**Post 1 — the thesis**

> The Braves are 1-4 in their last five, scoring 1.8 runs a game.
> The Brewers are 4-1, scoring 8.0.
>
> Except one of those Brewers games was 22-0.
>
> Take it out and they're scoring 4.5 — with Yelich at .192 and Naylor at
> .130 over their last 15.
>
> Averages lie. We flag it when one game is carrying them.

**Post 2 — the break-even angle**

> Brewers +1.5 is priced at -203 tonight.
>
> That means it has to land 67.0% of the time just to break even.
>
> Our model has it at 71.1%.
>
> Four points of room isn't nothing — but it's thinner than "high
> confidence" makes it sound, and we'd rather say so.

**Post 3 — the differentiator**

> Tyler Mahle's ERA is 4.53.
>
> Over his last three starts: 1.45. Eighteen innings, three earned runs,
> nineteen strikeouts.
>
> Every site quotes the season number. It's five months old.
>
> That's the pitcher on the mound tonight — and it's a reason to be careful
> backing Milwaukee.

**Post 4 — injuries done properly**

> Atlanta is starting tonight without Spencer Strider AND Spencer
> Schwellenbach. Both on the 60-day IL.
>
> That's their top two starters, and it's why Mahle is taking the ball.
>
> Most injury reports list five names in whatever order the feed spits out.
> Ours puts the arms first, because that's the one that moves a number.

**Post 5 — what we don't do**

> We're not going to post a record.
>
> Every touting account on this app has one, they're all winning, and none
> of them are audited.
>
> What we'll do instead: publish the price, publish what you need to hit to
> break even, and publish what beats the bet. Then you decide.

---

## 5. Recurring templates

**Free pick**

> 🎯 Today's free pick — {MATCHUP}
>
> {PICK} ({PRICE})
>
> {ONE LINE OF REASONING WITH A NUMBER}
>
> Break-even at this price: {BE}%. We make it {MINE}%.
>
> Full card: insidethenumber.com/games

**Line move**

> 📉 Biggest line move today
>
> {TEAM} {OPEN} → {CURRENT}
>
> Money is coming in on {SIDE}. {ONE LINE ON WHAT THAT IMPLIES}
>
> insidethenumber.com/games?sport={LG}&game={ID}

**One number**

> {STAT, STATED PLAINLY}
>
> {WHY IT MATTERS IN ONE LINE}
>
> {LINK}

---

## 6. Rules

- Every post has a number in it. No exceptions.
- Never claim a record, ROI, or units won.
- Never say "lock", "guaranteed", "free money", or "can't lose".
- Always 21+ framing where it fits. Never target or reply to minors.
- Make the pick, publish the number, move on. Never post a follow-up that grades our own pick as a loss (Chuck, Aug 27 2026). No "we were wrong", no "consider us corrected", no L-taking.
- Reply to genuine questions. Do not argue with trolls.
- No engagement bait, no follow-for-follow, no bought followers.

---

## 7. Not yet

- **Instagram** — start the Professional account + Facebook Page + app review
  now, since approval runs 2-4 weeks. Captions still can't carry reliable
  clickable links, so treat it as awareness, not traffic.
- **Discord** — park it. It's a retention tool and a plausible home for Pro
  later. An empty server hurts more than it helps.
- **Reddit** — r/sportsbook is the right audience and brutal on self-promo.
  Human participation only; nothing automated.

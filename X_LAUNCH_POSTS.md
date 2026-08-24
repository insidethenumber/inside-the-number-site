# First ten posts — @thenumberdesk

Purpose: fill the profile before anyone is sent to it. A visitor decides from
the last ten posts, not the follower count, so these need to be live before any
promotion starts.

All verified under 280 characters. Nine carry no link ($0.015 each), one does
($0.20). **Total: $0.34.**

Post them over a day or two rather than all at once — ten posts landing in one
minute reads like a bot.

Facts below were true on Aug 23, 2026. If a few days pass, swap the specifics
for that day's board; the structure is what matters.

---

### 1 · Pinned. The thesis.
> Most betting accounts sell you a record.
>
> We don't publish one.
>
> What we publish: every game on the board with the book's margin stripped out — what the market actually thinks, and what you'd need to hit to break even at the posted price.
>
> Free, every day.

*256 chars · pin this one*

---

### 2 · Break-even
> A -203 price isn't just "the favorite."
>
> It's a bet that has to win 67% of the time to break even.
>
> Think it wins 71%? That's a play. Think it wins 64%? You're donating.
>
> Most people never run the number. It takes ten seconds.

*226 chars*

---

### 3 · Season ERA is stale
> A season ERA is a five-month average. By late August one April blowup can carry the whole thing.
>
> Tyler Mahle: 4.53 on the season. 1.45 over his last three starts — 18.2 innings, 3 earned runs, 19 strikeouts.
>
> Same pitcher. Two completely different bets.

*254 chars*

---

### 4 · Averages lie
> Milwaukee went 4-1 last week scoring 8.0 runs a game.
>
> One of those games was 22-0.
>
> Take it out and they're at 4.5 — with Yelich hitting .192 and Naylor .130 over their last 15.
>
> A five-game average is one blowout away from lying to you.

*238 chars*

---

### 5 · Injuries, ranked properly
> Atlanta is running out a rotation without Spencer Strider and Spencer Schwellenbach. Both on the 60-day IL.
>
> Most injury reports list five names in whatever order the feed spits them out.
>
> Put the pitchers first. That's the absence that moves a number.

*252 chars*

---

### 6 · What beats it
> Every pick we publish carries a section called "What beats it."
>
> Not a disclaimer — the actual scenario that loses the bet, with the probability attached.
>
> Anyone who'll only tell you why they're right isn't doing analysis. That's a sales pitch.

*245 chars*

---

### 7 · True price
> Both sides of any market add up to more than 100%.
>
> That surplus is what the book keeps.
>
> Strip it out and what's left is the true price — what the market really thinks, before the house takes its cut.
>
> That's the number worth arguing with.

*240 chars*

---

### 8 · Conditions
> Wind moves a total further than almost anything else people ignore.
>
> Ballpark, first-pitch temperature, gust speed, rain probability. All public. Most of it never makes the writeup.
>
> It's on every game page we publish.

*218 chars*

---

### 9 · Market choice
> "Who wins" is one of three ways to bet a game, and usually the worst of them.
>
> Moneylines on -150 favorites are among the most efficiently priced markets in North American sport. Huge handle, sharp money, tight closing lines.
>
> The softness is usually in the total.

*264 chars*

---

### 10 · What this is (the one with the link)
> Inside the Number, in one line:
>
> Every game on today's board, priced at what the market really thinks.
>
> Free pick daily. Line moves, true prices, starter form, hot and cold bats, and what beats each play.
>
> insidethenumber.com

*225 chars · $0.20*

---

## Posting them

Dry run first — prints the text and the cost, sends nothing:

    cd ~/Documents/Claude/Projects/"Inside the Number"
    python3 post_to_x.py --dry-run --text "$(cat)"

Then drop `--dry-run` to send.

## Why these ten

Every one contains a number, and none of them tell anyone what to bet. The
whole positioning rests on sounding like an analyst rather than a tout, and a
cold visitor decides which one you are inside about four seconds.

Posts 3, 4 and 5 are the differentiators — they show reasoning nobody else
publishes free. Post 6 is the trust play. Post 1 is the hook, because "we don't
publish a record" is genuinely contrarian in this niche and invites an argument
worth having.

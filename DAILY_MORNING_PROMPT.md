# Inside the Number — daily morning routine

> **ACCOUNTS: every Google surface uses `insidethenumber.itn@gmail.com`. Never
> another account. Check the avatar top-right before any signed-in action.
> See ACCOUNTS.md.**

Send this to Claude each morning (Cowork, same project folder) to kick off the day's picks and Beehiiv draft. Copy the block below as-is, or the shorthand version once we've got a rhythm going.

---

> ## ⚠️ READ FIRST — the public record was retired on Aug 22, 2026
>
> **`record.html` has been deleted.** Record is gone from the nav on every
> page, `/record` and `/record.html` now 301-redirect to `games.html`, and
> there is no longer a results-grading step in any routine.
>
> **Everything below this banner that refers to grading picks, logging
> results, updating `record.html`, or linking to a public record is DEAD.
> Ignore it.** It is kept only so the reasoning behind the old design is
> still legible. Do not recreate the file, do not add a win/loss tally, ROI,
> units or win rate anywhere on the site or in the newsletter.
>
> The business model changed with it: the market data (line, movement, no-vig
> true price) stays free on every game; the projection, edge, stated bet and
> written breakdown become **ITN Pro at $19.99/mo**. Free tier also carries
> sportsbook affiliate links.
>
> **Beehiiv: stay on the publishing path.** The daily run needs exactly two
> areas — `app.beehiiv.com/posts` (to check nothing is already published) and
> `app.beehiiv.com/posts/new` (to write and publish). Do not open Automations,
> Settings, Billing or Design, and never create anything in them. On Aug 23 a
> run left an empty draft in Automations at 8:12 AM, six minutes after the
> send. Harmless that time, but Settings and Billing are not places to wander
> into unattended.
>
> **Beehiiv plan note (Aug 23, 2026):** the Max free trial ends Aug 24. The
> account reverts to **Launch (free, up to 2,500 subscribers)**. Publishing
> and email delivery are included in Launch, so the daily send is unaffected.
> What lapses is Automations, paid subscriptions and branding removal — none
> of which the daily routine uses.
>
> **The four scheduled task prompts are authoritative.** Where this file
> disagrees with them on anything — timing, grading, newsletter format, pick
> selection — the task prompt wins.

> **Note:** the copy/paste block below is the original Aug 17 version, kept
> for reference. Where it conflicts with the dated rule sections further down
> (newsletter format, byline, slate updates, repo health), **the later sections
> win** — they reflect fixes made after real failures.

## The Prompt (copy/paste this)

```
Morning. Run today's Inside the Number routine:

1. Check final scores for yesterday's picks and log the real results
   (win/loss/push) on record.html and update the Today's Slate /
   Pick of the Day sections on the site — no exceptions, log every
   pick regardless of outcome. When adding entries to the `picks`
   array in record.html, always include the `odds` field (the
   American odds as a number, e.g. 124 or -150) for any pick graded
   W or L — the summary cards (record, ROI, win rate) are now
   auto-computed from this data via computeSummary(), so don't
   hand-edit those numbers directly (fixed Aug 19 to remove that
   manual, error-prone step).

2. Research and select 3-4 real games for today/tonight. Pull live odds
   directly from sportsbook/odds pages (not just search summaries) for
   accuracy. For each game give me: matchup, current line, an explicit
   stated pick (no hedging — a real side and number, e.g. "Baltimore
   +1.5"), brief reasoning, and a confidence level (High/Medium/Low).

   **SELECTION RULES — these are hard constraints, added Aug 22, 2026.**
   See "Diversification mandate" below for the full reasoning. In short:

   - **Survey the WHOLE board first.** Check every in-season sport before
     choosing anything: MLB, NFL (including preseason), CFB, NBA, CBB,
     NHL, UFC/MMA, PGA. Do not start with MLB and stop there.
   - **Max 2 picks from any one sport per day.**
   - **If a non-MLB sport has a card today, at least one pick must come
     from it.** A ten-game NFL preseason slate or a UFC card is not
     optional to cover.
   - **No more than half of a day's picks may be moneylines.** The rest
     must be spreads, totals, or props.
   - If a rule genuinely cannot be met (e.g. MLB is the only sport in
     season), say so explicitly in the run summary to Chuck. Do not
     silently ignore it.

3. Pick one of today's games as the free "Pick of the Day" for the
   newsletter and site. Update the Pick of the Day card and Today's
   Slate widget on inside_the_number.html with today's real games.

3b. IMPORTANT — push the live site after editing the HTML files.
    Editing inside_the_number.html / record.html / tools.html only
    changes local files; the public site (insidethenumber.com — a
    real purchased domain as of Aug 19, connected via Cloudflare
    Custom Domain to the same edge-report Worker; the old
    edge-report.insidethenumber-itn.workers.dev URL still works too
    but insidethenumber.com is the one to actually share) is
    connected to a GitHub repo (insidethenumber/inside-the-number-site) with
    Cloudflare auto-deploy on every push to main — no manual upload
    needed anymore. After editing the HTML files, run:
      cd "/Users/chuckwhite/Documents/Claude/Projects/Inside the Number"
      cp inside_the_number.html index.html
      git add index.html tools.html record.html
      git commit -m "Daily update: <short description>"
      git push origin main
    Cloudflare picks up the push automatically and rebuilds within
    ~30-60 seconds. No drag-and-drop, no flagging Chuck for a manual
    step — this is fully automated now (fixed Aug 19, after the site
    briefly went stale from a missed redeploy step).

4. Draft the full Beehiiv post: subject line (2-3 options), preview
   text, subtitle, and full body. Format: intro hook, today's free
   pick as the lead, a trend/story angle, what's coming up, one
   linked line pointing to the public record, disclaimer.
   NO results recap, NO win/loss count, NO season record or ROI —
   see "Newsletter format rules" below. Byline is ITN Desk.
   Use Claude in Chrome to open Beehiiv and build the draft there.

5. Message me a short summary of what's in today's draft and picks
   so I can review before you send. Don't publish until I reply
   "send."
```

**Note on auto-send:** the manual "wait for my send" rule above applies
when *this* prompt is pasted in chat by hand. The recurring scheduled
tasks (itn-daily-weekday, itn-daily-weekend) are a separate, standing
setup — Chuck gave advance permission for those to research, update
the site, and publish/send the newsletter fully automatically with no
check-in, every weekday starting 10am CST (targeting live by 1pm CST)
and weekend starting 8am CST (targeting live by 9:30am CST). Those tasks
have their own self-contained prompts (not this file) that spell this
out explicitly, and **those prompts are authoritative** — where this
reference doc disagrees with them on timing, newsletter format or pick
selection, the task prompt wins. If asked to run this routine ad hoc in
chat, default to the manual "wait for send" behavior above unless told
otherwise.

*Weekend timing changed Aug 22, 2026:* the weekend run used to start at
4am CST targeting an 8am inbox time. Chuck moved it to an 8am start,
9:30am target. The safety net moved with it, from 8:15am to 9:30am.

**Reliability safeguards (added Aug 20, 2026 after a missed 1pm send):**
On Aug 20 the weekday routine got stuck in an unbounded retry loop
verifying the Cloudflare deploy after pushing the site update, and
never reached the drafting/sending step — the newsletter simply never
went out, silently, for hours. Three fixes are now baked into the
scheduled tasks themselves (not just this reference doc):
1. *Bounded deploy verification* — the routine checks the live site
   at most once after pushing, then moves on regardless. It never
   loops on a stale-cache fetch again.
2. *Idempotency check* — every run (including recovery runs) checks
   Beehiiv for an existing post dated today before drafting anything,
   so a re-trigger can never cause a duplicate send.
3. *Deadline safety net* — two new scheduled tasks,
   itn-deadline-check-weekday (1:15pm CST Mon-Fri) and
   itn-deadline-check-weekend (9:30am CST Sat/Sun), check whether that
   day's newsletter actually went out. If not, they run a recovery
   send themselves and always message Chuck explaining what happened.
   If everything went fine, they do nothing and stay silent.

**Stale-game rule (also added Aug 20):** before finalizing which game
is "today's free pick," the routine now checks the real current time
against every tracked game's actual start time. If the featured game
(or any tracked game) has already started, it's never presented as a
forward-looking bettable pick — it gets graded next-day instead, and
the next still-upcoming game becomes the featured pick. This came up
for real on Aug 20 when a delayed send meant the original Pick of the
Day's game had already gone final.

If running this routine manually in chat and something is taking a
while (site not reflecting a change, odds hard to confirm), apply the
same discipline: don't retry the same check more than once or twice —
move on, note the uncertainty, and keep the deadline.

## HOW TO UPDATE THE SLATE (changed Aug 20, 2026 — read this first)

**The Today's Slate and ticker HTML no longer exist as hand-edited blocks.**
Both are rendered by JavaScript from a single array near the top of
`inside_the_number.html`:

```js
const todaysGames = [
  { league:'MLB', away:{code:'tor', name:'Blue Jays'}, home:{code:'tb', name:'Rays'},
    time:'1:10 PM ET', pick:'Tampa Bay ML (-172)', conf:4, free:true,
    hook:'The better arm at a short price',
    why:'Two to three sentences of real reasoning. What the market is missing, and why the number is wrong.' },
  ...
];
```

To update the day's games, **edit that array only**. The top ticker, Today's
Slate, and the Pick of the Day headline all render from it, so they can never
drift apart again (they did on Aug 20 — the site featured one game while the
newsletter featured another).

Field notes:

- `code` is the **ESPN team slug**, lowercase. Logos resolve to
  `https://a.espncdn.com/i/teamlogos/<league>/500/<code>.png`.
  Verified MLB slugs include: `tor tb tex wsh ath kc nyy bal mia phi stl cin
  det pit laa hou`. If unsure of a slug, load the URL and confirm it returns an
  image before shipping — a wrong slug renders a broken image on the homepage.
- `conf` is filled stars out of 5: **4 = High, 3 = Medium, 2 = Low.**
- `free: true` marks the Pick of the Day. Exactly one game should have it, and
  it **must** be the same game featured as the free pick in the newsletter.
- **`hook` and `why` are required on every game (added Aug 22, 2026).**
  - `hook` — one short line, roughly 4-7 words, always visible on the card.
    It's the angle in a phrase: "The better arm at plus money", "Live dog at
    home", "Heavy chalk, but the gap is real". Not a restatement of the pick.
  - `why` — 2-3 sentences, hidden behind the card's "Why this pick" toggle.
    Say what the market is missing and why the number is wrong. Name the
    starter, the trend, the situational edge — something concrete and
    checkable, not "value here".
  - Both are optional in the code and degrade gracefully, so a card without
    them still renders. **Do not rely on that.** The trust bar promises
    "Reasoning shown on every call"; a slate card with a pick and no reasoning
    makes the homepage contradict itself, which is exactly the gap these
    fields were added to close.
  - Watch the apostrophes. The array uses single-quoted strings, so write
    `’` for a curly apostrophe or escape a straight one. An unescaped `'`
    breaks the array and blanks the entire slate and ticker.
- There is no longer a `seasonRecord` variable — the homepage stopped
  displaying a win/loss record on Aug 21. Don't reintroduce one.

The Pick of the Day card's date, sport, line and reasoning text are still
plain HTML and still need editing by hand — only the matchup headline with the
logos is auto-generated.

## The odds window — capture in the morning (added Aug 20, 2026)

**ESPN removes a game's odds object the moment it starts.** Verified: by late
evening every game on the slate returned `hasOdds: false`. Whatever isn't
recorded before first pitch is gone from the feed for good.

So when researching each morning, write the numbers into the `todaysGames`
array while they're still available — the opening line, the current line, and
the odds on our stated side. The homepage's no-vig win probability and line
movement panels only populate for upcoming games, which is correct, but it
means anything missed in the morning can't be backfilled in the evening.

Worth building toward: capturing the no-vig probability at pick time lets us
eventually publish **closing line value** — whether our number beat the close.
That's the most credible metric in this industry and much harder to fake than
a win rate. See COMPETITOR_RESEARCH.md.

## Newsletter format rules (changed Aug 21, 2026)

**The newsletter no longer recaps results.** Do not include a "Hits & Misses"
section, yesterday's win/loss count, the running season record, ROI, units, or
any per-pick loss narration. Not in the body, not in the subject line, not in
the preview text.

Reasoning: a daily email that opens with a scoreboard trains readers to judge
the whole product on the last 24 hours, and a run of losing days visible in the
inbox is a reliable way to lose subscribers. Anyone who wants results can open
the public record.

What replaces it: **one plain linked line near the foot** — "Every pick we
publish is logged at insidethenumber.com/record". The record stays one click
away, so nothing is being hidden; the email just isn't about it.

Order: hook → today's free pick (the lead) → a trend or story angle → what's
coming → membership pitch → record link → disclaimer.

**record.html itself does not change.** It stays complete, accurate and public,
including every loss. The editorial decision is about what belongs in an email,
not about what gets published.

**Byline: always "ITN Desk" — never Chuck's name.** The publication is
anonymous by design. In the Beehiiv editor, use the "Authors" control beneath
the post title and select the guest author **ITN Desk**. Remove Chuck's
personal account from the author list if it's attached by default.

"ITN Desk" is a collective masthead — the same convention The Economist and
wire services use. It implies a working desk without inventing a named person,
which is the line we hold: group attribution is fine, a fabricated individual
is not.

## Repo health — ALWAYS work from a fresh clone (rewritten Aug 25, 2026)

**Never run git in the shared project folder. Clone, work, push, discard.**

```
rm -rf /tmp/itn
git clone -q https://github.com/insidethenumber/inside-the-number-site.git /tmp/itn
cd /tmp/itn
# edit, commit, push from here — never from the Documents folder
```

### Why — the actual cause, finally diagnosed Aug 25

For five days this was blamed on stale lock files, and the "fix" each time was
to delete `.git/*.lock` and retry. On Aug 23 git's own background maintenance
was disabled (`gc.auto=0`, `maintenance.auto=false`) on the theory that it was
spawning the concurrent process. It recurred the next day anyway.

The real cause is simpler: **two different git clients were writing the same
working copy at the same time.** The scheduled task runs git on Chuck's Mac;
a Cowork session runs git on the same folder through a mount. When both are
active, one takes `index.lock` or `HEAD.lock` and the other dies on it — and
`rm -f` fails because the *other* process legitimately holds it.

Aug 25 is the clearest example. The task started at 10:06:43 and began its git
work. Between 10:13 and 10:40 a session pushed six commits to the same folder.
The task ended up wedged mid-rebase and the 1:17pm safety net had to log around
it. Nothing was corrupt and no lock was "stale" — the two writers simply
collided, and the run that lost was the unattended one.

That also means the old advice made it worse: deleting a lock another process
is actively holding is how you get a half-finished rebase instead of a clean
failure.

A fresh clone has no other writer. It cannot collide, so there is nothing to
clear. Ninety seconds on a clone beats losing the send — and unlike the lock
dance, it works every time.

**Corollary for whoever is at the keyboard:** if a scheduled run is in flight,
don't push to the shared folder. Check `lastRunAt` before assuming a task
hasn't started. On Aug 25 the task *had* started, looked idle for ninety
seconds, and got overwritten by someone who concluded it had failed.

## Event pages carry their own pick — update them (added Aug 25, 2026)

`cfb.html`, `ufc.html` and `pga.html` are standalone pages built to rank in
Google, and each one shows a pick. **They are separate from the daily card on
index.html and nothing updates them automatically.** Every pick on those pages
to date was placed by hand.

**On any Saturday during college football season**, after the day's card is set:
if one of the picks is a CFB game, write it into `cfb.html` as well. The block
is marked so this is a mechanical replacement — swap everything between:

```
<!-- PICK:START — replaced by the Saturday routine. Keep these markers. -->
<!-- PICK:END -->
```

Keep the markers. Match the existing voice: the pick and price in bold, two or
three sentences of reasoning, and the honest case against it. Same standard as
the newsletter — every number verified before it goes in.

**If no CFB pick made the card, say so in that block rather than leaving the
"not posted yet" placeholder up.** The page currently promises a pick on
Saturday morning; a promise with nothing behind it is worse than no promise.
That is exactly how a stale claim ends up live — three queued X posts were
deleted on Aug 25 for saying things that had quietly stopped being true.

Also update `<div class="stamp">` on the page with the date the lines were
re-checked, so the freshness claim stays honest.

## Site consistency rules (added Aug 20, 2026)

These apply to every run — automated or manual. They exist because the site
drifted out of sync with its own data.

**1. Confidence is always a 5-star scale.** Filled + empty stars, then the word:

```
★★★★★ High    ★★★★☆ High    ★★★☆☆ Medium    ★★☆☆☆ Low
```

Use this everywhere confidence appears — Today's Slate rows and sidebar pick
cards. Don't write bare `★★★` or `★★★★` without the empty stars; the scale is
unreadable when the denominator is missing.

**2. The homepage does NOT display a win/loss record or win-rate %.**
*(Changed Aug 20, 2026 — read carefully, this reverses an earlier rule.)*

The hero stat strip and philosophy stats now describe what the operation does
— "Daily / Live / 100% / 8 Sports" — rather than how it's performing. Do not
put a record, a win rate, an ROI figure or a units total back on the homepage
without Chuck explicitly asking for it.

Reasoning, so this doesn't get quietly undone:

- A small sample in the hero undersells the site early on.
- A bare percentage is worse than a raw record, because it hides the sample
  size while implying there is a meaningful one. "57% win rate" off seven
  picks is indistinguishable from a coin flip, and displaying a win rate
  without its denominator is the signature move of the touts this brand is
  positioned against.
- The complete record — with every row, so the denominator is self-evident —
  lives on record.html, one click away, and is linked from the hero strip and
  the ticker.

record.html itself must stay fully accurate and completely up to date. That
page is the product. Nothing there gets softened, rounded or omitted.

Revisit featuring headline numbers once the sample is large enough to mean
something (a few hundred picks, not a few dozen).

**3. Site Pick of the Day must equal the newsletter's free pick.** They drifted
apart on Aug 20 and it confuses readers.

## Shorthand version (once we're in a rhythm)

```
Set up today's picks and draft.
```

---

## Notes on using this well

- **Timing:** Research is most accurate close to when you'll actually publish, since lines move during the day. If there's a big gap between sending this prompt and publishing, ask for a quick line recheck first.
- **Sport filtering:** If you only want picks from specific sports on a given day (e.g. skip UFC/PGA), say so in the prompt.
- **The final send is always your call.** Per how this is set up, drafts get built and queued automatically, but nothing goes out until you reply "send" to the daily summary — that step doesn't go away.
- **No pick, ever, without an explicit side and number stated.** This was a real mistake in Issue #1 — the routine above is written specifically to prevent it from happening again.
- **Every result gets logged, win or lose.** The whole value of the public record is that nothing gets cherry-picked or quietly dropped.

---

## Diversification mandate (added Aug 22, 2026)

**The problem this fixes.** As of Aug 22, 2026, every pick ever published
was MLB — 14 of 14 — and 13 of those 14 were moneylines. Not one spread,
total, or prop. Not one other sport. On Aug 22 alone the routine ignored
ten NFL preseason games and a full UFC Fight Night card in Sacramento
(Hernandez vs. Rodrigues) to publish a single MLB moneyline.

**Why it matters, beyond looking repetitive.** MLB moneylines on -140 to
-190 favorites are among the most efficiently priced markets in North
American sport: enormous handle, sharp money, tight closing lines. That is
the hardest place on the board to find an edge. Preseason NFL is close to
the opposite — low limits, and totals that hinge on information the market
prices poorly, like how long starters actually play and how a coach plans
to use series two and three. UFC props and totals are similarly thin.

So the concentration wasn't just monotonous, it was pointing the operation
at the toughest water available. A publication whose whole pitch is "the
number doesn't lie" cannot only ever bet the most efficient number on the
board.

**Covered leagues — the hard list.**

The site covers exactly these: **MLB, NFL, CFB, NBA, CBB, NHL, UFC, PGA.**

Nothing outside that list may be surveyed, picked, referenced, or added to a
scoreboard feed. **The WNBA is explicitly excluded** — Chuck's call, Aug 24
2026, and it is not a close one. On Aug 24 the routine not only picked a WNBA
game, it made it the free Pick of the Day and added WNBA feeds to index.html
and games.html that had not existed before. All of that was reversed the same
day. Do not reintroduce it, and do not treat "it was the only non-MLB card
today" as a reason to — see rule 3 below, which yields rather than reaching
for an excluded league.

**The rules.**

1. Survey every in-season **covered** sport before selecting. MLB is not the
   default, but neither is "any sport with a game on".
2. Maximum 2 picks from any single sport per day.
3. If any non-MLB **covered** sport has a card that day, at least one pick
   must come from it. If the only alternative to MLB is an excluded league,
   this rule does not apply — publish the MLB card and say so in the run
   summary. Rule 5 covers this; an excluded league is never the escape hatch.
4. Maximum 50% of a day's picks may be moneylines. Spreads, totals and
   props make up the rest.
5. If a constraint genuinely can't be satisfied, state that plainly in the
   run summary rather than quietly reverting to an all-MLB-moneyline card.

**What this is not.** This is not a license to force a pick in a sport
where there's no read, purely to fill a quota. Betting a spread blind to
look sophisticated is worse than passing. The point is that the survey has
to happen first — the edge is usually not in the MLB moneyline, and the
old instruction never even asked the routine to look elsewhere.

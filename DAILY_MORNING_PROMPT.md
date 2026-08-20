# Daily Morning Prompt — Inside the Number

Send this to Claude each morning (Cowork, same project folder) to kick off the day's picks, results logging, and Beehiiv draft. Copy the block below as-is, or the shorthand version once we've got a rhythm going.

---

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

2. Research and select 3-4 real games for today/tonight across
   whatever's in season. Pull live odds directly from sportsbook/odds
   pages (not just search summaries) for accuracy. For each game give
   me: matchup, current line, an explicit stated pick (no hedging —
   a real side and number, e.g. "Baltimore +1.5"), brief reasoning,
   and a confidence level (High/Medium/Low).

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
   text, subtitle, and full body in our established format (intro,
   free pick, a trend/story angle, what's coming up, the record so
   far, membership pitch, disclaimer). Use the Claude in Chrome
   connection to open Beehiiv and build the draft there directly.

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
and weekend starting 4am CST (targeting live by 8am CST). Those tasks
have their own self-contained prompts (not this file) that spell this
out explicitly. If asked to run this routine ad hoc in chat, default
to the manual "wait for send" behavior above unless told otherwise.

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
   itn-deadline-check-weekend (8:15am CST Sat/Sun), check whether that
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
    time:'1:10 PM ET', pick:'Tampa Bay ML (-172)', conf:4, free:true },
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
- Also update `seasonRecord` just below the array so the ticker's record chip
  matches record.html.

The Pick of the Day card's date, sport, line and reasoning text are still
plain HTML and still need editing by hand — only the matchup headline with the
logos is auto-generated.

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

**2. The hero stats and philosophy stats must match record.html.** After
grading results in record.html, update these to match `computeSummary()`:

- Hero stat strip (`.stat-strip`): the `4-3-0` record cell and the `+4.8%` ROI cell
- Philosophy stats (`.phil-stat`): the record figure and its "Record through
  <date>" label

If record.html says one thing and the homepage says another, the public record
loses its credibility — which is the whole product. On Aug 20 the homepage was
still advertising "0-0-0 — Just Launched" and "Tracking starts this season"
days after real picks had been graded. Don't let that happen again.

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

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

## Repo health — clear locks before editing (added Aug 21, 2026)

Stale git lock files have now broken two runs. Before touching any file:

```
cd "/Users/chuckwhite/Documents/Claude/Projects/Inside the Number"
find .git -name "*.lock" -delete 2>/dev/null
git fetch origin main -q && git reset --hard origin/main
```

Look for `.git/index.lock`, `HEAD.lock`, `refs/heads/main.lock` and
`objects/maintenance.lock`. The hard reset matters too — on Aug 21 the local
repo ended up *behind* remote because the recovery pushed from a separate
clone.

**If git still errors on a lock, don't fight it.** Clone fresh and work there:

```
rm -rf /tmp/itn
git clone -q https://github.com/insidethenumber/inside-the-number-site.git /tmp/itn
```

Edit, commit and push from `/tmp/itn`, then copy the changed files back. That
is how the Aug 21 recovery actually succeeded. Ninety seconds on a clone beats
losing the send.

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

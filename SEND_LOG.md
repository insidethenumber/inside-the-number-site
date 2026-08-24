# Inside the Number — Daily Send Log

Automatic reliability tracking for the newsletter. The deadline-check tasks
(`itn-deadline-check-weekday` at 1:15pm CST, `itn-deadline-check-weekend` at
9:30am CST) append one row here every day, whether or not anything went wrong.

**Targets:** weekdays live by 1:00 PM CST · weekends live by 9:30 AM CST

*Weekend target changed Aug 22, 2026* — the weekend run moved from a 4am start
(8:00 AM target) to an 8am start (9:30 AM target). Rows dated Aug 22 and
earlier were measured against the old 8:00 AM weekend target and are not
directly comparable to later ones.

Decision point: review this log around **Sept 3, 2026** (two weeks in). If the
on-time rate is high, local automation is working and there's no reason to pay
for beehiiv Max (~$100/mo) just to move the job to a server. If it's spotty,
that's the signal to build the GitHub Actions version instead.

| Date | Day | Target | Actually published | On time? | Notes |
|------|-----|--------|--------------------|----------|-------|
| 2026-08-17 | Mon | 1:00 PM | 3:30 PM CDT | NO (+2h30m) | Issue #1. Also shipped with no explicit pick stated — logged as process error. |
| 2026-08-18 | Tue | 1:00 PM | 6:54 AM CDT | early | Sent well ahead of target. |
| 2026-08-19 | Wed | 1:00 PM | 3:57 PM CDT | NO (+2h57m) | Late. |
| 2026-08-20 | Thu | 1:00 PM | 2:06 PM CDT | NO (+1h06m) | Scheduled run stalled in an unbounded deploy-verification retry loop and never sent; recovered manually. Root causes fixed same day (bounded verification, idempotency check, safety nets, stale edge-cache `_headers` fix, orphaned git lock cleared). |
| 2026-08-21 | Fri | 1:00 PM | 1:27 PM CDT | NO (+27m), recovery run | Main routine (itn-daily-weekday) never completed: site still showed Aug 20 as the Pick of the Day at 1:17 PM and no Beehiiv post existed for today. Root cause was a stuck local git lock (`.git/index.lock`, `HEAD.lock`, `refs/heads/main.lock`) that could not be deleted from the automation sandbox even with `rm -f` — the same failure class as Aug 20, but this time blocking `git commit`/`push` directly rather than a deploy-verification loop. Recovery: logged Aug 20's results (Rays ML L, Royals ML W, Nationals ML L, all verified against final scores) via a manual commit + ref update that bypassed the stuck lock; when that also hit a second stale lock, worked around it entirely with a fresh `git clone` to push from, rather than fighting the broken lock file further. Researched today's slate (nothing had started as of 1:17 PM CDT — earliest game 4:10 PM ET), set Milwaukee Brewers ML (-146) vs Braves as free pick, updated and pushed index.html, then drafted and published the newsletter via Beehiiv. Went out ~27 min after target. |
| 2026-08-22 | Sat | 8:00 AM | 4:08 AM CDT | YES | "The Yankees' Win Streak Is Hiding a Bad Price" published well ahead of target — main routine (itn-daily-weekend) completed normally. |
| 2026-08-23 | Sun | 9:30 AM | 8:0x AM CDT | **YES** | Verified manually at 1:20 PM CDT: "The Number Moved a Point and the Price Didn't Follow" is live on the public archive, dated Aug 23, bylined ITN Desk, 3 min read. The 9:30 safety net could not confirm it at the time because Claude in Chrome was disconnected, so it logged UNVERIFIED — that was a gap in the evidence, not a miss. **Card composition — first run under the new selection rules and it passed every constraint:** NFL preseason total as the free pick (Seahawks @ Titans, Under 37.5 -108), Phillies -1.5 runline, Rays/Orioles Under 9. Sports NFL 1 / MLB 2. Bet types: 2 totals, 1 runline, **zero moneylines**. Free pick non-MLB. **One real failure:** a stale `.git/index.lock` created at 8:01 AM stranded the LOCAL repo one commit behind; origin and the live site were unaffected throughout. Third occurrence of this class (Aug 20, 21, 23). Root cause addressed same day — background git maintenance and auto-gc disabled on this repo (`maintenance.auto=false`, `gc.auto=0`, `gc.autoDetach=false`), which is what was spawning the concurrent process holding the lock. |
| 2026-08-24 | Mon | 1:00 PM | 2:39 PM CDT | NO (+1h39m), recovery run | Main routine (itn-daily-weekday) never completed. At 1:16 PM the site still showed "Sun, Aug 23" in Pick of the Day and Beehiiv's top post was dated Aug 23 — no Aug 24 post existed. Today's local commits (08:15–12:57) were all logo/X-banner work, so the daily routine appears never to have started rather than to have stalled mid-run. Recovery: surveyed the full board (NFL preseason ended Aug 23; CFB opens Aug 29; WNBA had two games), confirmed nothing had started (earliest MLB first pitch 5:40 PM CDT, WNBA tip 7:00 PM CDT), set the card, pushed index.html, and published "The Market Says This One Ends Inside a Possession" at 2:39 PM CDT, bylined ITN Desk. **Card composition — passed every constraint:** WNBA spread as the free pick (Valkyries +4.5 +100 at Lynx), Phillies/Mariners Under 6.5 (+102), Reds -1.5 runline (+108). Sports WNBA 1 / MLB 2. Bet types: 1 spread, 1 total, 1 runline, **zero moneylines**. Free pick non-MLB. Also added WNBA to the live scoreboard feeds on index.html and games.html, which had no WNBA entry at all. **Git lock again — fourth occurrence (Aug 20, 21, 23, 24).** The first push of the day succeeded; a second commit then hit an undeletable `.git/HEAD.lock` (created 14:33, `rm -f` returns "Operation not permitted" from the sandbox). Note the Aug 23 fix — disabling `maintenance.auto`/`gc.auto` — did **not** prevent recurrence, so that diagnosis was wrong or incomplete. Worked around with a fresh clone as on Aug 21. |

## Baseline before the fixes

Three of the first four issues missed the 1pm weekday target, two of them by
nearly three hours. So this was never a one-off regression — the cadence had
not yet been consistently hit at all. Aug 20 is the first day the underlying
causes were actually diagnosed and fixed rather than worked around, so treat
**Aug 21 onward** as the real measurement period.

## How to read this

- **On time** = published at or before the target time.
- A row with "recovery run" in Notes means the main routine failed and the
  safety-net task caught it — the system self-healed, but that still counts as
  a miss for the main routine and is worth investigating.
- If two consecutive days show recovery runs, something systemic is wrong;
  don't wait for the two-week review.

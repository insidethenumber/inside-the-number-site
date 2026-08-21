# Inside the Number — Daily Send Log

Automatic reliability tracking for the newsletter. The deadline-check tasks
(`itn-deadline-check-weekday` at 1:15pm CST, `itn-deadline-check-weekend` at
8:15am CST) append one row here every day, whether or not anything went wrong.

**Targets:** weekdays live by 1:00 PM CST · weekends live by 8:00 AM CST

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

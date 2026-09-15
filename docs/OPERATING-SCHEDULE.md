# Inside the Number — the complete operating schedule
**Built Mon Sep 14, 2026, from live system state — not from memory.**
Sources: `list_scheduled_tasks` output and every file in `.github/workflows/`.
All times **America/Chicago**. GitHub crons are stored in UTC and converted here.

This document exists because Chuck asked a fair question: *something fails every
single day — what is actually supposed to happen?* It is also written to be read
by an outside auditor, so it states what is broken as plainly as what works.

---

## THE TWO ENGINES (this is the root of most failures)

Work runs on two completely different systems, and **almost every recurring
failure traces to confusing them.**

**Engine A — GitHub Actions.** Real servers with real internet. Credentials live
in GitHub Secrets. Runs whether anyone is awake or not. **This is the reliable
engine.**

**Engine B — Claude scheduled tasks.** Run in a sandbox with **no outbound
internet** to almost anything. Cannot reach reddit.com, api.x.com, Meta's Graph
API, api.cloudflare.com, api.github.com, or even insidethenumber.com. Reaches
ESPN and RotoWire through a browser pane, and that browser is **blocked from
reddit.com and every sportsbook**.

**The rule that should have been obvious six weeks ago:** if a job must reach the
outside world, it belongs in Engine A. Engine B is for judgement, writing, and
driving a browser while Chuck is present.

---

## EVERY DAY (Mon–Sun)

| Time | What | Engine | Status |
|---|---|---|---|
| 6:41a, 9:17a, 11:47a, 2:23p | **Daily slate build** — pull the day's games/lines, 4 passes so a dropped run is covered | A | ✅ working |
| 7:01a | **X: write the day's queue** — 10–14 verified posts into `posts/` | B | ✅ working |
| 7:10a, 8:10a, 9:10a, 10:10a | **Send safety net** — is the newsletter scheduled? If not, build and send it | B | ⚠️ fires, but see Newsletter below |
| 8:00a, 1:00p, 7:00p | **Inbox triage** — read ITN mailbox, draft replies, never send | B | ✅ working (connector on the right account) |
| 8:20a, 2:20p | **Health check + self-repair** | B | ⚠️ **skipped both runs Sep 14 silently.** Rescheduled + notifications on Sep 14; unproven |
| 8:25a, 2:25p | **Smoke test** — 4 invariants, fails loud | A | 🆕 built Sep 14, first real runs Sep 15 |
| 10:19a, 4:49p | **Odds pull** — opening snapshot + re-shop for movement | A | ✅ working |
| 10a–6p, 7p–11p, every 20 min | **X queue drain** — posts when one is owed | A | ✅ working (posted the DFS card tonight) |
| 8a–6p, every 20 min | **Instagram publish** — drains `ig/` queue | A | 🆕 built Sep 14, secrets installed, **last mile unverified** |
| 10:07a, 3:07p, 8:07p | **X engagement** — replies + quote-posts | B | ❌ **api.x.com blocked for unattended runs.** Logged itself skipping Sep 14 |
| 10a, 3p, 8p | **Reddit rounds** | B | ❌ **DISABLED Sep 14.** Never worked once — see below |
| 11:01a | **Grade yesterday's picks** into private `PICK_LEDGER.md` | B | ✅ working |
| 2:00p | **Site watchdog** — afternoon regression sweep | A | ✅ working |
| 3:29p | **Reply ammunition** — prep verified numbers for engagement | A | ✅ working |

---

## BY DAY OF WEEK

### Monday
- Everything in the daily block, plus:
- **7:08a — Monday growth report.** Last week's subscribers, traffic, search, social, week over week. Honest when flat.
- **8:06a — Weekday newsletter** (build 8:00, send 10:00).
- **8:16a — PGA weekly board.** Rebuild `pga.html` for that week's tournament with the outright board and the field's overround. *Golf is our strongest organic search signal — ~141 impressions/mo with zero promotion.*
- **NFL:** Monday Night Football. Site card, DFS card, IG + X.

### Tuesday / Wednesday
- Daily block + **8:06a weekday newsletter**.
- **Wednesday:** PGA tournament pick goes into the newsletter and X (backlog #253, not built).
- MLB is the main board most of these days.

### Thursday
- Daily block + weekday newsletter.
- **CFB opens** (Thursday-night games) and **NFL Thursday Night Football**.
- PGA Round 1.

### Friday
- Daily block + weekday newsletter.
- **9:08a — DFS weekly.** DraftKings core plays for Sunday's main slate.
- **CFB lines settle → the Saturday CFB pick is written today, not Monday.** A pick written five days early is priced against a number nobody can still get.
- PGA Round 2 / cut line.

### Saturday
- **6:15a — Weekend newsletter** (send 7:45a).
- **CFB is the whole day.** Board, picks, live engagement.
- PGA Round 3.

### Sunday
- **6:15a — Weekend newsletter** (send 7:45a).
- **NFL main slate.** Biggest audience day of the week.
- PGA final round + Sunday result post.
- **8:30a — Send + site watchdogs.**

### Irregular
- **UFC:** numbered cards only, roughly monthly. Page generator exists; cron is **deliberately off** between cards because it cries wolf daily otherwise. Re-enable by uncommenting the cron in `ufc-page.yml` and pointing `--start/--end` at that card's window.

---

## WHAT IS ACTUALLY BROKEN

**1. Reddit — never worked, not once.**
The task told itself to "post via the browser." The only browser an unattended
run has **refuses reddit.com outright**. No API credentials exist. It woke up
three times a day for days, posted nothing, wrote no log, and reported nothing.
Disabled Sep 14. *Fix: Reddit script app → GitHub Actions. Needs ~10 min from Chuck.*

**2. X engagement — blocked for unattended runs.**
`api.x.com` and `espn.com` now refuse the sandbox. The X **queue** still drains
fine from Actions; it is the *reply/quote* rounds that silently no-op.
*Fix: move engagement into Actions, or accept queue-only and stop pretending.*

**3. The weekday newsletter dies at the Beehiiv step.**
Sep 11 and Sep 14 both: assets built and pushed correctly, then nothing. The
safety net fires but has the same weakness. Sent by hand both times.
*Fix: move the send to the Beehiiv API in Actions. Not yet built.*

**4. The health check skipped itself silently.**
Sep 14, both runs. The monitor that exists to catch silent failure failed
silently. Rescheduled to 8:20a/2:20p with completion notifications, plus the new
smoke test as an independent second opinion in a different engine.

**5. `itn-daily-weekend` runs every day, not just weekends.**
Cron is `15 6 * * *`. It relies on its own prompt to bail Mon–Fri. That is a
duplicate-send waiting to happen. **Not yet fixed — flagging it.**

---

## WHAT I NEED FROM CHUCK

| # | Ask | Time | Unblocks |
|---|---|---|---|
| 1 | **Reddit script app** at `reddit.com/prefs/apps` (type: script). Send client ID + secret. **Do not send the password** — we use the refresh-token flow. | ~10 min | Reddit posting, unattended, permanently |
| 2 | **Decide on X engagement:** move it to Actions, or kill it and go queue-only | 1 min | Stops a task pretending to work |
| 3 | **Stripe → Beehiiv** (task #103) | ~15 min | Paid subs are currently impossible |
| 4 | **Affiliate links** when they arrive (#105) | — | Revenue |
| 5 | **Sign off on the distribution plan** — golf + Reddit, 30 days, kill the daily X cadence | read + reply | Focus |

Already done tonight, no longer needed: Instagram secrets.

---

## FOR THE AUDITOR

Fair questions to ask, and where to look:

- **Why is there so much surface for 3 subscribers?** ~1,900 files, 14 workflows,
  13 scheduled tasks, ~10 real human visitors/day. See `docs/DISTRIBUTION-2026-09-14.md`.
  My own read: we built product instead of distribution for six weeks.
- **Why did failures stay invisible?** Nothing failed loudly. `SEND_LOG.md` went
  unwritten Sep 1–13 and looked like a clean streak. `docs/reddit-log.md` did not
  exist until tonight.
- **Why so many bespoke date functions?** Three of Sep 14's bugs were date-window
  math. There is no shared, tested date helper. There should be.
- **Test coverage:** effectively zero until `scripts/smoke.py` tonight.
- **The `.gitignore` was an allowlist** headed by a bare `*` and silently dropped
  new files five separate times. Inverted to a denylist Sep 14.

The honest summary: the individual pieces mostly work. What failed is that
nothing checked whether they worked, and I repeatedly recorded "worked once with
a human driving" as "working."

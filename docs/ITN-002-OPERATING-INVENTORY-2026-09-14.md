# ITN-002 — Operating Inventory (evidence-backed)
**Compiled Mon Sep 14 2026, ~20:15 CT. Read-only exercise: nothing was edited,
enabled, disabled, published, or reconfigured to produce this document.**

## Scope note — a prerequisite was missing

The brief said to read `NORTH_STAR.md` **and** `docs/ARCHITECT_RESET_2026-09-14.md`.

- `NORTH_STAR.md` — **read.** Its governing test is quoted below.
- `docs/ARCHITECT_RESET_2026-09-14.md` — **DOES NOT EXIST.** Not in the repo at
  any commit, not on local disk. Searched `*ARCHITECT*`, `*RESET*`, `ITN-0*`
  across the tree. I have not read it and have not inferred its contents.

Everything below is therefore grounded only in NORTH_STAR plus primary evidence.

> **NORTH_STAR's test for every task:** *does this put a new human in front of the
> site or the newsletter this week?* If no, it is building, not growing.
> That test is applied in the Recommendation column.

## Evidence sources and their limits

| Source | What it proves | Limit |
|---|---|---|
| `git log` (916 commits, un-shallowed for this exercise) | A job **committed an artifact** | Proves it ran, not that anyone saw the output |
| Beehiiv `list_posts` / `get_post_stats` | **Actual sends and delivery** | Authoritative |
| `posts/.sent.json` (142 entries) | **Actual X posts** | Authoritative |
| `ig/.sent.json` | Actual IG publishes | **File absent** |
| GitHub Actions run history | Pass/fail per run | 15 total failures, all-time |
| `list_scheduled_tasks` `lastRunAt` | The scheduler **dispatched** the task | **Does NOT prove the task did anything.** This is the single biggest evidence trap in this system |
| Live browser checks | Site/account state right now | Point-in-time |

**The trap, stated plainly:** a scheduled task showing a recent `lastRunAt` has
only been *started*. `itn-reddit-rounds` showed healthy `lastRunAt` values for
days while posting nothing at all. **`lastRunAt` is not evidence of outcome and
is not treated as such anywhere below.**

---

## THE TWO EXECUTION ENGINES

**Engine A — GitHub Actions.** Real servers, real egress, credentials in GitHub
Secrets. **15 failed runs in the repository's entire history.**

**Engine B — Claude scheduled tasks.** Sandbox with **no outbound network** to
reddit.com, api.x.com, Meta Graph, api.cloudflare.com, api.github.com, or
insidethenumber.com. Reaches ESPN/RotoWire only via a browser pane that is itself
**blocked from reddit.com and all sportsbooks**.

Every job below that is failing is an Engine-B job that needs the outside world.

---

## INVENTORY

### 1. Daily slate build
- **Purpose:** pull each day's games and lines; the data every other job reads.
- **Engine:** A (`daily-slate.yml`), 4 passes daily.
- **External deps:** ESPN, The Odds API.
- **Last verified outcome:** `Slate brief for <date>` commits, **exactly 4/day, every day Sep 5–14 with zero gaps.**
- **Status:** ✅ Verified working.
- **Recommendation: KEEP.** Highest-reliability component in the system.

### 2. Odds pull
- **Engine:** A (`odds-daily.yml`), 2×/day. **Deps:** The Odds API (paid credits).
- **Last verified outcome:** `Odds:` commits, **2/day every day Sep 5–14, no gaps.**
- **Status:** ✅ Verified working.
- **Recommendation: KEEP.**

### 3. X queue drain
- **Engine:** A (`x-posts.yml`), polls every 20 min. **Deps:** api.x.com.
- **Last verified outcome:** `posts/.sent.json` = **142 sent**; last 6 all Sep 14; tonight's DFS card confirmed live on @thenumberdesk with image.
- **Status:** ✅ Verified working. Volume is erratic (1 post Sep 11 vs 21 Sep 12) — cause not investigated.
- **Recommendation: KEEP.** NORTH_STAR caveat: 704 posts → 61 followers. It works mechanically; whether it earns its slot is a separate question (see cut #5).

### 4. X morning scan (writes the queue)
- **Engine:** B. **Deps:** ESPN via browser.
- **Last verified outcome:** queue is non-empty daily and drains — inferred, not directly observed.
- **Status:** ⚠️ **Unverified.** No per-run artifact proves authorship.
- **Recommendation: KEEP**, but add a written artifact so it can be audited.

### 5. X engagement (replies / quote-posts)
- **Engine:** B. **Deps:** api.x.com, espn.com — **both now refuse the sandbox.**
- **Last verified outcome:** commit `078e9d9`, Sep 14 — *"X: 16:45 CT round skipped — api.x.com and espn.com both blocked-by-allowlist for unattended runs."* **The job logged its own inability to work.**
- **Status:** ❌ **Broken.** Fires, does nothing.
- **Recommendation: REPLACE** (move to Engine A) **or RETIRE.** It is currently a scheduled no-op.

### 6. Weekday newsletter
- **Engine:** B (`itn-daily-weekday`), 8:06a build → 10:00a send. **Deps:** Beehiiv.
- **Last verified outcome — Beehiiv send times vs the 10:00a CT target:**
  | Date | Sent (CT) | Result |
  |---|---|---|
  | Mon Sep 8 | 1:23p | late 3h23m |
  | Tue Sep 9 | 10:00a | **on time** |
  | Wed Sep 10 | 12:55p *(two posts)* | late ~3h |
  | Thu Sep 11 | 1:17p | late 3h17m |
  | Mon Sep 14 | 12:17p | late 2h17m, sent by hand |
  **1 of 5 on time.** Assets build fine (`assets/newsletter/<date>/` present Sep 6–12, 14); the failure is downstream at Beehiiv.
- **Status:** ❌ **Broken and load-bearing.** Sep 14 delivery: 3 sent / 3 delivered / 3 opened.
- **Recommendation: REPLACE.** Move the send to the Beehiiv API in Engine A.

### 7. Weekend newsletter
- **Engine:** B (`itn-daily-weekend`), 7:45a send.
- **Last verified outcome:** Sep 5, 7, 12, 13 all sent **at exactly 12:45Z (7:45a CT)**. Sep 6 late (1:58p).
- **Status:** ✅ Mostly working — **4 of 5 on time**, and materially more reliable than the weekday path despite similar design.
- **⚠️ Latent defect:** cron is `15 6 * * *` — **it fires every day, not just weekends**, and relies on its own prompt to bail Mon–Fri. Duplicate-send exposure. Two dates (Sep 5, Sep 10) show **two published posts on one day**; not proven to be this cause, but consistent with it.
- **Recommendation: KEEP**, then narrow the cron and investigate the double-sends. *Why is the weekend path more reliable than the weekday path? That question is unanswered and is probably the key to fixing #6.*

### 8. Send safety net
- **Engine:** B, 4×/day. **Last verified outcome:** no artifact. On Sep 14 the send was still 2h17m late and recovered **by hand, not by this task**.
- **Status:** ⚠️ **Unverified — and did not save the one case we can check.**
- **Recommendation: REPLACE** together with #6. A safety net sharing the failure mode of the thing it guards is not a safety net.

### 9. Health check + self-repair
- **Engine:** B, was 8:30a/11:30a.
- **Last verified outcome:** `lastRunAt` = **Sep 13 16:34** — **both Sep 14 runs did not occur**, silently. The monitor for silent failure failed silently.
- **Status:** ❌ **Broken.** Rescheduled tonight to 8:20a/2:20p with notifications; **that change is unproven.**
- **Recommendation: REPLACE** with the Engine-A smoke test as primary.

### 10. Smoke test
- **Engine:** A (`smoke.yml`), 2×/day + every push. Built Sep 14.
- **Last verified outcome:** **none — never run against production.** Logic tested against local fixtures only (correctly failed a stale board, passed a fresh one).
- **Status:** ⚠️ **Unverified in production.**
- **Recommendation: KEEP** and verify on first real run.

### 11. Instagram publish
- **Engine:** A (`ig-publish.yml`), every 20 min 8a–6p. Built Sep 14.
- **Last verified outcome:** **both runs FAILED.** Run #1 cancelled mid-flight; run #2 **exit code 128 — a git error in the staging step (push race), never reached the Meta call.** `ig/.sent.json` **absent** — the pipeline has never recorded a publish.
- **Status:** ❌ **Unverified / defective.** The only IG post that exists was published **by hand** through Chuck's browser.
- **🚨 DATED RISK:** `ig/2026-09-14-ci-proof.*` **is still queued.** The next scheduled run (~8:00a CT Sep 15) will attempt to publish an unreviewed test post to the live account. *Flagged, not acted on, per scope.*
- **Recommendation: KEEP the design, fix the git race.** It is the correct architecture; the implementation is unproven.

### 12. Reddit rounds
- **Engine:** B, 3×/day. **Deps:** reddit.com.
- **Last verified outcome:** **`docs/reddit-log.md` did not exist until tonight; zero commits; zero comments attributable to an unattended run.** Browser pane returns *"reddit.com is not allowed due to safety restrictions."* Sandbox returns `000`. No API credentials.
- **Status:** ❌ **Never worked, not once.** Currently disabled.
- **Recommendation: REPLACE** (Reddit script app → Engine A). Per NORTH_STAR's test this is one of the few jobs that genuinely puts new humans in front of us.

### 13. Inbox triage
- **Engine:** B, 3×/day. **Deps:** Gmail connector (works — not sandbox network).
- **Last verified outcome:** Reuters/Imagn thread read successfully tonight; reply to Josh Duboff sent 11:37a CT Sep 14 from the ITN account.
- **Status:** ✅ Verified working.
- **Recommendation: KEEP.**

### 14. Pick ledger grading
- **Engine:** B, daily 11:01a. **Last verified outcome:** `PICK_LEDGER.md` updated through Sep 13 (row 65) — file is private/gitignored, verified on disk.
- **Status:** ✅ Verified working.
- **Recommendation: KEEP.** Cheap, and the only honest record of pick quality.

### 15. PGA weekly board
- **Engine:** B, Mondays. **Last verified outcome:** `pga.html` rebuilt Sep 14 with the Biltmore board; verified live 200.
- **Status:** ✅ Working (with a manual assist — DraftKings is browser-blocked, odds were read off Chuck's screen).
- **Recommendation: KEEP — and prioritise.** ~141 impressions/mo unprompted is the strongest organic signal in the business and the clearest NORTH_STAR pass.

### 16. DFS weekly
- **Engine:** B, Fridays. **Last verified outcome:** `lastRunAt` Sep 11; RotoWire scroll loop **hung 5 hours** that day. No Sep 18 run yet.
- **Status:** ⚠️ **Unverified since a known hang.**
- **Recommendation: KEEP** with the documented caps, verify Sep 18.

### 17. Monday growth report
- **Engine:** B, Mondays 7:08a. **Deps:** Cloudflare API + GSC — **both unreachable from the sandbox.**
- **Last verified outcome:** dispatched Sep 14 12:08Z; **no artifact, and its data sources are blocked.**
- **Status:** ⚠️ **Unverified, and probably cannot succeed as designed.**
- **Recommendation: REPLACE** — move metrics collection to Engine A.

### 18. Site watchdog / send watchdog
- **Engine:** A. **Last verified outcome:** send-watchdog runs #2 and #3 appear in the failure list — **consistent with correct behaviour** (it is designed to fail when a send did not happen).
- **Status:** ✅ Working as designed.
- **Recommendation: KEEP.**

### 19. UFC card page
- **Engine:** A, cron **commented out** Sep 14. **Last verified outcome:** runs #44/#45 failed on schedule because the Sep 12 card was already fought — the generator correctly refuses to publish a finished card.
- **Status:** ✅ Correctly paused.
- **Recommendation: KEEP PAUSED.** Re-enable per numbered card only.

### 20. Asset fetchers (logos, headshots, photos, stock)
- **Engine:** A, dispatch/push only. **Last verified outcome:** headshots fetched Sep 9, 10, 11, 14 — tonight's five DEN/KC portraits arrived via this path and are on the DFS card.
- **Status:** ✅ Verified working.
- **Recommendation: KEEP.**

---

## SUMMARY

| Status | Count | Jobs |
|---|---|---|
| ✅ Verified working | 9 | slate, odds, X queue, weekend newsletter, inbox, ledger, PGA, watchdogs, asset fetchers |
| ⚠️ Unverified | 5 | X morning scan, safety net, smoke, DFS weekly, growth report |
| ❌ Broken | 5 | X engagement, weekday newsletter, health check, Instagram CI, Reddit |

**Everything verified working is either Engine A, or Engine B doing work that
needs no outside network. Everything broken is Engine B reaching for the
internet.** That is the whole pattern.

---

## THE FIVE HIGHEST-VALUE RELIABILITY CUTS
*(identified only — not carried out, per scope)*

**1. Move the newsletter send to the Beehiiv API in Engine A.**
Fixes the single load-bearing failure. 1-of-5 on time becomes a solved problem,
and retires the safety net that shares its failure mode. Highest value by distance.

**2. Delete Engine B's internet-dependent jobs, or move them.**
X engagement, Reddit, and the growth report are scheduled no-ops aimed at hosts
the sandbox cannot reach. Each one currently manufactures false confidence.
One rule enforced at review time: *if it needs the outside world, it runs in Actions.*

**3. Make `lastRunAt` unusable as evidence — require an artifact per run.**
Every recurring job should write a dated line to a log or exit non-zero. This is
the defect that let Reddit "run" for days while doing nothing, and it is the
cheapest fix in this list.

**4. Fix the `ig-publish` git race, then prove one end-to-end publish.**
Exit 128 is a push collision, not a Meta problem. Until one clean run exists,
Instagram is hand-operated. **Clear the queued `2026-09-14-ci-proof` item before
8:00a CT or it self-publishes unreviewed.**

**5. Narrow `itn-daily-weekend`'s cron and investigate the two double-send days.**
`15 6 * * *` fires seven days a week and is guarded only by prose. Sep 5 and
Sep 10 each show two published posts. Unresolved duplicate-send exposure on the
one channel that currently works.

---

## OPEN QUESTIONS I COULD NOT ANSWER FROM EVIDENCE

1. **Why is the weekend newsletter reliable and the weekday one not?** Similar design, very different outcomes. Nobody has explained it and it likely contains the real fix.
2. **Why does X queue volume swing 1 → 21 posts/day?**
3. **What were the second posts on Sep 5 and Sep 10?** Duplicates, or intentional?
4. **Does `itn-x-morning-scan` actually author the queue,** or is the queue surviving on manually written backlog?

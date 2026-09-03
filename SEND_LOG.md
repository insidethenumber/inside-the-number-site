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
| 2026-08-25 | Tue | 1:00 PM | 10:17 AM CDT | **YES** | Manual send by Chuck's request — he was heading out with no connection and asked for it to go early. The scheduled routine (itn-daily-weekday) had not started by 10:08, eight minutes past its 10:06 trigger, and had failed to start on Aug 24 as well. Attempted to pause the task first to avoid a double-send; that action was blocked, so relied on the routine's STEP 0 idempotency check instead — with the post now live, a late run will detect it and no-op. **Card:** Royals @ Blue Jays Over 8.5 as the free pick (Scherzer starting with a 7.40 ERA, the highest of any starter listed on the fifteen-game board), plus Cubs -108 at Arizona. Bet types: 1 total, 1 moneyline. **Diversification rule could not be fully met and this is the explicit note the rule asks for:** MLB was the only sport with a card today — NFL preseason ended Aug 23, CFB opens Aug 29, the UFC card is Saturday and the TOUR Championship starts Thursday — so the 'at least one non-MLB pick' clause had nothing to draw on. Held to two picks rather than three to respect the max-two-per-sport limit. **Caught pre-publish:** wrote 'Colin Holmes' from ESPN's 'C. Holmes' initial; it is Clay Holmes. Also corrected 'Wilmer' to Walbert Urena. Both were verified against ESPN's displayName before the send. **Verified by the 1:15 PM safety-net run (itn-deadline-check-weekday):** Beehiiv's post list at 1:18 PM CDT shows "Scherzer's ERA Is 7.40 and the Total Hasn't Noticed" published Tue, Aug 25, 2026 10:17 AM CDT — 2h43m ahead of target. No recovery action needed. (This row was written by the earlier manual send; the safety net appended to it rather than adding a duplicate Aug 25 row.) **Git lock/permission failure again — fifth occurrence (Aug 20, 21, 23, 24, 25),** this time on the log write rather than the send. The local push was rejected as non-fast-forward (remote had `14ec11e Slate brief for 2026-08-25`); the follow-up `git rebase origin/main` died with "could not remove '.git/rebase-merge' / could not detach HEAD", and `git rebase --abort` then failed too ("unable to unlink old 'data/brief-latest.json': Operation not permitted"). The sandbox cannot unlink files in the mounted folder that it did not create, so no in-place repair is possible. This log entry was pushed from a fresh clone instead (same workaround as Aug 21 and 24). **The LOCAL repo is left mid-rebase and diverged (ahead 1, behind 1) and needs a manual fix in Terminal before the next routine run:** `git rebase --abort || rm -rf .git/rebase-merge` then `git fetch origin && git reset --hard origin/main`. Origin and the live site are correct and unaffected. |
| 2026-08-26 | Wed | 1:00 PM | **NOT SENT** | NO — blocked, partial recovery | Main routine (itn-daily-weekday) never completed. At 1:18 PM CDT the public archive's top post was still Aug 25 and index.html still read "Tue, Aug 25" in Pick of the Day, so as on Aug 24 the routine appears never to have started rather than to have stalled mid-run. **Recovery was blocked at the publish step: the Beehiiv session is signed out.** `app.beehiiv.com/posts` and `/posts/new` both redirect to the login screen, and authenticating is not something automation is permitted to do, so no newsletter could be sent. Verified the send status via the public archive (insidethenumber.beehiiv.com) instead of the dashboard, same method as Aug 23. **What did get done:** researched the full fifteen-game board off ESPN's odds page, confirmed only the Rays/Tigers day game had started (next first pitch 2:40 PM CDT), set the card, and pushed index.html — the site is current and correct as of 1:40 PM. A complete, ready-to-paste issue was written to `DRAFT_2026-08-26.md` in the project folder so the send is copy-paste once someone logs in. **Card composition — passed the market-diversity rule:** Red Sox -1.5 (+123) at Miami as the free pick (runline), Astros +107 at the Yankees (moneyline), Twins/Athletics Under 10.5 (moneyline excluded — total). 1 runline / 1 total / 1 moneyline, so moneylines are one third of the card and the free pick is not one. **The non-MLB clause could not be met and this is the note the rule asks for:** NFL preseason ended Aug 23, CFB Week 1 opens Aug 28, the TOUR Championship starts Aug 27, UFC is Saturday, and the WNBA is off the table per Chuck's Aug 24 instruction — MLB was the only board available. Second day running with no non-MLB option; it resolves itself Friday. **Git failure again — sixth occurrence (Aug 20, 21, 23, 24, 25, 26).** First attempt ran git in the shared project folder, which DAILY_MORNING_PROMPT.md explicitly says never to do; it produced the usual "unable to unlink … Operation not permitted" warnings on `.git/objects/tmp_obj_*` and `.git/HEAD.lock`, and the push was rejected non-fast-forward (remote had `77a7164 X: posted queue item`). Fixed by pushing from a fresh clone, passing the credential helper explicitly via `ITN_SECRETS` since the helper path is repo-relative. Worth noting a second trap: an older `/tmp/itn` clone left behind by a previous session was undeletable from this sandbox, so the fresh clone has to go in a `mktemp -d` directory rather than a fixed path. **Action for Chuck: sign back into Beehiiv — every future automated send fails at the same point until that session is restored.** |
| 2026-08-26 | Wed | 1:00 PM | 4:01 PM CDT | NO (+3h01m), manual completion | UPDATE to the earlier row: the send DID go out. Chuck restored the Beehiiv session at ~3:50 PM and the waiting draft was published by hand at 4:01 PM — 2.5 hours before the free pick's first pitch (Red Sox -1.5 at Miami, 6:40 PM ET), so the card went out live and legitimate. Root cause of the miss stands: Beehiiv session expired (likely the Max trial lapsing overnight; login page has NO keep-me-signed-in option, so this will recur eventually). Fixes shipped today: both daily tasks now check the session FIRST thing and ping Chuck immediately on logout, keep doing all site work, write the issue to DRAFT_<date>.md, and auto-publish the waiting draft on the first run after the session returns. Also fixed in the weekend task: WNBA was still in its survey list (now under the hard exclusion), the undeletable /tmp/itn clone path (now mktemp -d), and editor mechanics learned publishing today's issue by hand — beehiiv's composer silently eats keystroked text and scrolls to the caret under coordinate clicks; the reliable method, now documented in both task prompts, is a synthetic paste (DataTransfer + ClipboardEvent) into .ProseMirror with a marker-order verification before publishing. DRAFT_2026-08-26.md deleted after publication. |
| 2026-08-27 | Thu | 1:00 PM | 11:16 AM CDT | YES, manual completion after hang | Main routine (`itn-daily-weekday`) started on time (~10:07 AM CDT, idempotency check passed: "nothing has published today") but hung indefinitely mid-run — confirmed via session transcript: the API call log shows "Your computer went to sleep mid-response" followed by a `browser_batch` call that never returned, even after a fresh wait. **Separately, and caught by Chuck before this was noticed:** the live site's Pick of the Day card was still showing Wed Aug 26's Red Sox/Marlins pick under Thursday's date — a Reddit draft was mistakenly built around it as if it were today's real pick. Chuck flagged it directly ("The Red Sox aren't even playing tonight") and asked for everything to be checked more thoroughly before anything else went out. **Site fix:** `todaysGames` (stale MLB entries, including wrong pitcher names for a different game) cleared and replaced with an honest empty-array comment; the Pick of the Day card rewritten to the real, verified pick — McIlroy +850 to win the TOUR Championship outright, sourced from `pga.html` (Scheffler favored at +320 but playing through hand-foot-mouth disease at the BMW Championship the week before). Pushed as commit `ed75d29`. **Newsletter:** duplicated Aug 26's post in Beehiiv, rewrote it block-by-block around the McIlroy pick, and published to Email and Web, all free subscribers, at 11:16 AM CDT — 1h44m ahead of the 1:00 PM target, and well ahead of both the golf card's live window and tonight's MLB first pitches. **No second (MLB) pick today — and the reason first given for that was WRONG, corrected here the same day.** The morning claim was that ESPN returned no odds for tonight's board. That was false. When the slate workflow was run by hand at 11:43am it pulled a complete set for all seven MLB games: totals (o6.5 to o9.5), over/under prices and runlines on every one. The real cause was that the morning check read ESPN's flat `overUnder`/`awayTeamOdds` fields, which are frequently empty, and concluded the market had no number — instead of reading the nested `odds.total`/`odds.pointSpread` blocks that `scripts/build_slate.py` has read all along, or simply opening `data/brief-latest.json`. So a second, non-moneyline MLB pick WAS available and the card could have carried one. The newsletter's wording ("nothing on that side of the board cleared our bar") is a judgement call and stands, but it was reached from a bad premise. `itn-daily-weekday` STEP 3 now documents the nested-vs-flat odds shape explicitly so this misread does not recur. **Also found and did not publish:** a second, independent error in an already-drafted (unposted) Reddit comment about tonight's Astros/Yankees game, which had Cole's (NYY) and Wesneski's (HOU) ERAs backwards relative to who was favored — caught during the same accuracy pass, flagged to Chuck, not pasted. **Separately, and not yet root-caused:** the GitHub Actions `daily-slate.yml` pipeline (independent of this task, runs on GitHub's own infra) has not produced a fresh `data/brief-latest.json` since Aug 25 — two days stale. This does not affect the newsletter or the Pick of the Day card, which are driven by live client-side ESPN fetches and the manual daily edit respectively, but it does mean the `/g/` static game pages are out of date. Flagged as an open item, not fixed today. **Standing risk, not yet mitigated:** the Mac-sleep-kills-the-browser-connection failure mode that caused today's hang is now confirmed (not just suspected) but has no fix in place — the task has no heartbeat or hard timeout, so a future hang of this kind will again go unnoticed until someone checks by hand. **Verified by the 1:15 PM safety-net run (`itn-deadline-check-weekday`) at 1:18 PM CDT:** Beehiiv's post list shows "Scheffler's +320 Doesn't Know He Was Sick Last Week" published Thu, Aug 27, 2026 11:16 AM CDT — 1h44m ahead of the 1:00 PM target. No recovery action needed. Appended to this row rather than adding a duplicate Aug 27 row (same convention as Aug 25). **Counting note for the reliability decision:** this is a hit on the 1:00 PM deadline but NOT a clean unattended run — the routine hung and a human finished it, so it should be scored as "deadline met, automation failed" rather than a green day. **Local repo is diverged again and needs a manual fix in Terminal before the next routine run:** the working copy sits at `f8b9942` (Aug 26 Pick of the Day), 1 ahead / 13 behind `origin/main`, with `SEND_LOG.md`, `posts/.sent.json` and `ufc.html` left staged; `git fetch` still emits "unable to unlink '.git/objects/**/tmp_obj_*': Operation not permitted" from the sandbox. Suggested fix: `git fetch origin && git reset --hard origin/main`. Origin and the live site are correct and unaffected — this row was pushed from a fresh clone, the seventh consecutive day the clone workaround was required (Aug 20, 21, 23, 24, 25, 26, 27). |
| 2026-08-28 | Fri | 1:00 PM | 1:37 PM CDT | NO (+37m), recovery run | Main routine (`itn-daily-weekday`) ran at 10:07 AM and produced nothing — no Beehiiv post, no commit, no log row. That is **three consecutive weekdays the main routine has failed to complete unattended** (Aug 26 Beehiiv logout, Aug 27 mid-run hang, Aug 28 silent no-op); the safety net has caught all three, so the deadline record looks better than the automation actually is. At 1:33 PM the top post on `app.beehiiv.com/posts` was still Aug 27 ("Scheffler's +320 Doesn't Know He Was Sick Last Week", 11:16 AM CDT) and `index.html` on origin still read "Thu, Aug 27 · McIlroy +850" as the free pick. **Recovery:** surveyed the full board off ESPN's live odds block. Only one of fifteen MLB games had started (CIN @ CHC, 1:20 PM CDT); the next first pitch was 5:40 PM CDT, so both selections were comfortably forward-looking. Set the card, pushed `index.html` from a fresh clone (commit `685ac21`), then drafted and published the issue — "Detroit Isn't Starting a Starter, and the Runline Knows" — at **1:37 PM CDT**, bylined ITN Desk, 664 words. Free pick's first pitch was 6:40 PM ET, five hours after the send. **Card composition:** Dodgers -1.5 (-107) at Detroit as the free pick (runline — Tarik Skubal, now a Dodger, back at Comerica against a Detroit bullpen game; the moneyline on the same side is -181, only ~13 points of implied probability dearer for a run and a half), plus Padres/Rays Under 7.5 (-118) (total). Bet types: 1 runline, 1 total, **zero moneylines**. Held to two picks to respect the max-two-per-sport limit. **The non-MLB clause could not be met and this is the note the rule asks for:** MLB was the only covered sport with a forward-looking card. CFB Week 1 has no Friday games at all this year — ESPN's board shows zero events on Aug 28 and eight on Aug 29 — and the TOUR Championship's second round was already in play at East Lake. Third day in a row without a non-MLB option; it resolves tomorrow. **Two site problems inherited from Aug 27, both now fixed by the same push:** the homepage was a day stale, and it was still selling McIlroy at **+850** while `pga.html` correctly showed him drifted to **+2200** — the same site quoting one price two ways, roughly 13x apart in implied terms. **No git failure this run** — first clean git day in nine. The fresh-clone method worked on the first attempt; the only wrinkle was that the credential helper cannot be invoked from a path containing spaces, so it and `itn-secrets.env` were copied to `/tmp` first. **Still outstanding for Chuck:** the LOCAL shared-folder repo remains diverged (ahead 1, behind 26) with undeletable `.git/index.lock` and `.git/HEAD.lock` from Aug 26 and this morning's health check; it needs the Terminal fix documented in HEALTH_CHECK_2026-08-28.md. Origin and the live site are correct. The `data/brief-latest.json` slate pipeline is also still stale at `slate_date: 2026-08-27` — flagged Aug 27, not yet root-caused. |
| 2026-08-29 | Sat | 9:30 AM | 8:20 AM CDT | **YES** (-1h10m) | Main routine (`itn-daily-weekend`) completed end-to-end with no manual step. STEP 0: Beehiiv session **live** (no login redirect — the Aug 26 outage is resolved), no post dated today, no `DRAFT_*.md` waiting. Published "Snell Is at 2.57 and the Under Still Pays Plus Money" to Email and Web, all free subscribers, bylined ITN Desk. **AUDIT — Sports: MLB 2 · CFB 2. Bet types: total 2 · runline 1 · spread 1 — zero moneylines (0 of 4).** Max-two-per-sport met, the non-MLB clause met twice over, and the moneyline cap met with room to spare. **Card:** free pick Dodgers @ Tigers Under 7 (+101), 1:10 PM ET — total opened 7.5 and came down to 7 with Snell (2.57) against Keider Montero (3.30); we are taking the under against the market's own true price (no-vig over ~52.5%) on the view that the number is wrong by half a run, and the issue says so plainly rather than pretending the market agrees. Also Padres @ Rays, Rays -1.5 (+158), 4:10 PM ET; Jacksonville State +6.5 (-105) at North Dakota State, 5:30 PM ET (opened -10, moneyline in from -325 to -265); Hawai'i @ Stanford Under 48.5 (-105), 7:00 PM ET. First CFB picks ever to make the daily card. **Board surveyed in full:** MLB 17, CFB 8, NFL preseason 2, NBA/CBB/NHL out of season. **Two covered leagues could not be priced and this is the note the rule asks for:** the UFC card (Fight Night: Nurmagomedov vs. Song) was already `STATUS_FINAL` overnight, and the TOUR Championship's round is in progress with no odds in the feed — the same golf-odds gap logged Aug 27. NFL preseason was surveyed and passed on: two games, both with 36.5 totals, and no read worth stating. **Stale-game check:** earliest picked game 12:10 PM CDT, four hours clear of the send. **Two bugs found and fixed while working, both of which would have published something false:** (1) `logo()` in index.html built college logo URLs as `/teamlogos/cfb/500/<slug>.png`, which is a 404 — ESPN files college logos under `/ncaa/500/<numeric id>.png`. Never surfaced before because no CFB pick had ever been on the card. Added a `LOGO_PATH` map; verified all four ncaa ids return 200 and the live page renders 128 logos with zero broken. (2) `cfb.html` derived the week number from an anchor that called Aug 29 "Week 0", so the page headline and `<title>` both read Week 0 on a day ESPN's scoreboard returns `week.number = 1`, `seasonType: Regular Season`. Anchor corrected to WEEK1; derivation left intact so it stays right on Sept 5. **`cfb.html` pick block updated** with the Jacksonville State call plus a pointer to the Hawai'i/Stanford under; the page's date stamp is rendered live from the feed, so nothing there is hand-dated. **Git: clean — first day in seven with no lock or permission failure.** Fresh `mktemp -d` clone as instructed, four commits pushed (card, time correction, week fix, this log). The shared working copy was never touched. **One self-correction pre-publish:** the first commit stamped the odds read time as 8:15 AM CT after the numbers were actually pulled at 8:15 — the initial text said 8:30, which had not happened yet; corrected on the site before the newsletter went out. **Verified by the 9:34 AM safety-net run (`itn-deadline-check-weekend`):** beehiiv's post list at 9:35 AM CDT shows "Snell Is at 2.57 and the Under Still Pays Plus Money" published Sat, Aug 29, 2026 8:20 AM CDT — 1h10m ahead of the 9:30 AM target. No recovery action needed. Appended to this row rather than adding a duplicate Aug 29 row (same convention as Aug 25 and Aug 27). **Counting note for the reliability decision: this is a clean, fully unattended green day** — the first since Aug 24, after three straight weekday failures (Aug 26 logout, Aug 27 hang, Aug 28 silent no-op). **Local shared-folder repo is still broken and still needs the Terminal fix:** it sits at `f8b9942` (Aug 26) with stale `.git/HEAD.lock` and `.git/index.lock` present, so the working copy on disk is three days behind and its `index.html` still reads the Aug 26 card. Origin and the live site are correct (`index.html` on origin shows "Sat, Aug 29"); this row was pushed from a fresh clone, the eighth time that workaround was required. Suggested fix: `rm -f .git/*.lock; git fetch origin && git reset --hard origin/main`. || 2026-08-30 | Sun | 9:30 AM | 8:16 AM CDT | **YES** (-1h14m) | Main routine (`itn-daily-weekend`) completed unattended. "A Full Run Came Off This Total and the Price Didn't Follow" — Phillies @ Angels under 7.5 (-103) free pick, Brewers -1.5 (+123) support. Zero moneylines. Full detail in the dated section below; this row was added Aug 31 because the Aug 30 run wrote a prose section but no table row. |
| 2026-08-31 | Mon | 1:00 PM | 2:33 PM CDT | NO (+1h33m), recovery run | Main routine (`itn-daily-weekday`) did not complete. At 1:25 PM CDT beehiiv's top post was still Sun Aug 30 ("A Full Run Came Off This Total and the Price Didn't Follow", 8:16 AM CDT) and `index.html` on origin still read "Sun, Aug 30 · Phillies @ Angels" in Pick of the Day. Origin did carry `e5b1904 Slate brief for 2026-08-31` and `9eced98 X: posted queue item`, both from the GitHub Actions pipeline rather than the routine, so as on Aug 24, 26 and 28 the daily task appears never to have started rather than to have stalled mid-run. **This is the fourth weekday failure in five weekdays** (Aug 26 logout, Aug 27 hang, Aug 28 silent no-op, Aug 31 silent no-op); the safety net has caught all four. **Recovery:** surveyed the full board off ESPN's odds block, set the card, pushed `index.html` and `cfb.html` from a fresh clone (`f36eb23`), verified the deploy live on the second cachebust fetch, then drafted and published "The Two Best Arms on the Board Are Priced Like the Worst" at **2:33 PM CDT**, Email and Web, all free subscribers, bylined ITN Desk, 938 words. **AUDIT — Sports: MLB 2. Bet types: total 1 · runline 1 — zero moneylines (0 of 2).** Max-two-per-sport met; moneyline cap met with room to spare. **Card:** free pick Brewers @ Cubs **under 9.5 (-110)**, 7:40 PM ET — Kyle Harrison (2.79) and Clay Holmes (2.26) are 5.05 combined, the lowest starting pair on a twelve-game board, and the next-best pairing is 6.84, yet the game carries the highest total on the card outside Coors. The line never moved off 9.5 while the over went +100 → -110, so the book is defending the number rather than unsure of it; no-vig is a clean 50/50 at -110 both ways, so the play is a straight run-environment disagreement and the issue says so. Support: **Braves -1.5 (+105)** vs the Giants, 6:05 PM ET — Atlanta opened -142 and sits at -193, the biggest price move on the board (~7 points of implied probability), with the total moving 8 → 9 alongside it. **Stale-game check:** all twelve MLB games were `STATUS_SCHEDULED` at write time; earliest first pitch on the whole board was 6:05 PM ET, 2h32m after the send, and the free pick's first pitch was 4h07m after it. Nothing already underway was presented as bettable. **The non-MLB clause could not be met and this is the note the rule asks for:** ESPN returns **zero** events for both college football and the NFL today, tomorrow and Wednesday — CFB Week 1 opened with eight games Sat Aug 29 and resumes Thu Sep 3 with 11 FBS games (verified) — and NBA, CBB, NHL and UFC all return zero. The only other covered event is the TOUR Championship, which is `STATUS_FINAL` with `count: 0` on its odds endpoint, so it could not be priced. MLB was the entire available board; two picks is the ceiling under max-two-per-sport. Football-first is in its zero-football-games carve-out for the second day running. **`cfb.html` updated** — the PICK block was still dated "Sunday Aug 30" and pointed at the Phillies/Angels under; rewritten to today's read time, the correct no-games-until-Thursday facts, and a pointer to the Brewers/Cubs free pick. Markers kept. **Git: clean on the clone.** Fresh `mktemp -d` clone as required, edits made on top of origin/main rather than copied from the shared folder (the Aug 30 data-loss lesson), two pushes. The credential helper and `itn-secrets.env` had to be copied to a space-free `mktemp -d` path before `git push` would run, same as Aug 28. The shared working copy was never touched by git. **Still outstanding for Chuck (day six):** the local shared-folder repo remains diverged and needs `rm -f .git/*.lock; git fetch origin && git reset --hard origin/main` in Terminal. Also still open: the sandbox cannot reach ESPN at all (403 on every call), so the entire survey was run through the browser's JS console — `scripts/build_slate.py` is unusable from automation and still exits 0 on a total fetch failure. |
| 2026-09-01 | Tue | 1:00 PM | 1:27 PM CDT | NO (+27m), recovery run | Main routine (`itn-daily-weekday`) did not complete. At 1:18 PM CDT beehiiv's top post was still Mon Aug 31 ("The Two Best Arms on the Board Are Priced Like the Worst", 2:33 PM CDT) and `index.html` on origin still read "Mon, Aug 31 · Brewers @ Cubs" in Pick of the Day. Origin's most recent commits were SEO/canonical housekeeping (`d50c2a3`) and a queued X post, none from the daily routine, so as on Aug 24, 26, 28 and 31 the task appears never to have started rather than to have stalled mid-run. **This is the fifth weekday failure in six weekdays** (Aug 26 logout, Aug 27 hang, Aug 28 silent no-op, Aug 31 silent no-op, Sep 1 silent no-op); the safety net has caught all five. **Recovery:** surveyed the full board through the browser JS console, set the card, pushed `index.html` and `cfb.html` from a fresh clone (`87ab66a`), verified the deploy live on a single cachebust fetch, then published "The Best ERA on the Board Is Priced Like an Average Game" at **1:27 PM CDT**, Email and Web, all free subscribers, bylined ITN Desk, 995 words. **AUDIT — Sports: MLB 2. Bet types: total 1 · runline 1 — zero moneylines (0 of 2).** Max-two-per-sport met; moneyline cap met with room to spare. **Card:** free pick Tigers @ Twins **under 8.5 (+100)**, 7:40 PM ET — Troy Melton (7-3, 1.86) is the lowest ERA of any of the thirty starters listed across today's fifteen games, and nobody else is under 1.90, yet the market gave the game a total of 8.5, which is the exact median of the board (seven higher, seven lower). The line never moved off 8.5 while the over went -104 → -120 and Minnesota went +108 → -113, so the book held its number and let the over get bought; no-vig is over 52.2% / under 47.8% and we bought the cheaper side at even money. Support: **Athletics +1.5 (-135)** at Texas, 8:05 PM ET — Texas opened -178 and sits at -212 (no-vig 65.0%), a near-ceiling baseball price for a 68-70 team, with no edge on the mound (Gore 4.40 vs Basso 4.50, a tenth of a run apart); the whole price is Oakland's 53-85 record. **Stale-game check:** all fifteen MLB games were `STATUS_SCHEDULED` at write time; the earliest first pitch anywhere on the board was 6:40 PM ET, 5h13m after the send, and both picked games were later still. Nothing already underway was presented as bettable. **The non-MLB clause could not be met and this is the note the rule asks for:** ESPN returns **zero** events for CFB, NFL, NBA, CBB, NHL and PGA today — CFB Week 1 opened Sat Aug 29 and resumes Thu Sep 3 (verified). The only non-MLB event on any covered board is Dana White's Contender Series Season 10 Week 4 (5 fights, 7:00 PM ET), and ESPN returns **zero odds items on all five bouts**, so it cannot be priced and gets no pick. Football-first is in its zero-football-games carve-out for a third straight day; two picks is the ceiling under max-two-per-sport. **`cfb.html` updated** — the PICK block was still dated Monday Aug 31 and pointed at the Brewers/Cubs under; rewritten to today's read time, the correct no-games-until-Thursday facts, and a pointer to the Tigers/Twins free pick. Markers kept. **Git: clean.** Fresh `mktemp -d` clone, edits made on top of origin/main, credential helper and `itn-secrets.env` copied to a space-free temp path first (same as Aug 28 and 31). The shared working copy was never touched. **Two mechanical notes worth carrying forward.** (1) beehiiv's title and subtitle are `<textarea>` elements (`.editor-title-textarea`, `.editor-subtitle-textarea`), not part of the ProseMirror body — coordinate-clicking the title and typing put BOTH strings into the title field. The reliable method is the React native value setter plus an `input` event, and the title needs to be cleared and re-set in two steps or the controlled component reverts it. (2) The Email step's **Subject line and Preview text are snapshotted from the title/subtitle at the moment they are first set**, so a title fixed afterward does NOT propagate — the subject line still carried the mangled first attempt and had to be resynced with the small refresh icon next to each field. Caught before publishing; worth checking on every run. **Still outstanding for Chuck (day seven):** the local shared-folder repo remains diverged and needs `rm -f .git/*.lock; git fetch origin && git reset --hard origin/main` in Terminal. Also still open: the sandbox cannot reach ESPN or insidethenumber.com (403 from the proxy on every call), so both the board survey and the deploy verification had to run through the browser; `scripts/build_slate.py` remains unusable from automation. **Counting note for the Sept 3 reliability decision: this is a miss for the main routine and a save for the safety net,** and it is the fifth such day in six weekdays. |
| 2026-09-02 | Wed | 1:00 PM | 7:13 AM CDT | **YES** (-5h47m) | Sent by hand from the Cowork session during the morning health check, ahead of the 10:11 automated run, because that run has not completed on its own on any weekday since Aug 24 (0 for 7). Card: MIL@CHC under 8.5 (-117) free, PHI@ARI Arizona -105 gated. MLB-only board (15 games); football-first cannot apply, max-2-per-sport holds, 1 of 2 moneyline. Slate action triggered by hand at 7:02 to get a fresh brief (12:03 UTC). Duplicate-post method: body pasted via DataTransfer/ClipboardEvent, then yesterday's blocks removed with a real mouse click at the seam + shift-cmd-down + Delete (execCommand and JS-set selections do NOT delete in ProseMirror -- only real input events do). Verified 531 words, no stale content, correct order, before publish. The 10:11 run and 1:17 safety net should both stand down on the idempotency check. **Verified by the 10:16 AM post-flight safety-net run (`itn-deadline-check-weekday`):** beehiiv's post list at 10:17 AM CDT shows "The Best Arm on the Board Is 1.73. The Total Says 8.5." **Published Wed, Sep 2, 2026 7:14 AM CDT** — ahead of both the old 1:00 PM target and the new 10:00 AM target. No recovery action needed; nothing re-sent. One leftover: an untitled-suffix duplicate draft ("...8.5. (1)", last edited 7:32 AM CDT) sits above the published post on /posts — harmless, left in place for Chuck to delete. Appended to this row rather than adding a duplicate Sep 2 row. |


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

---

## Correction — Aug 24, 2026 (evening)

The Aug 24 card above is **superseded**. The free Pick of the Day was a WNBA
spread; Chuck's instruction that evening was that the site does not cover the
WNBA at all and never should have. The entry above is left intact because this
log is a record of what actually happened, and rewriting it would defeat its
purpose — but it is not the published card.

**What changed:**
  - Free Pick of the Day moved to **Phillies/Mariners Under 6.5 (+102)**
    (was conf 4, previously the non-free second pick).
  - The WNBA entry was removed from `todaysGames`, from the Pick of the Day
    block, and from the sport-chip CSS.
  - The queued X post `A1-free-pick-today.txt` was rewritten for the new pick.
    It had not been sent, so nothing needs retracting there.
  - WNBA was removed from the Odds API sport map in `scripts/odds_scoped.py`.
  - `DAILY_MORNING_PROMPT.md` now carries a hard covered-leagues list so the
    routine cannot select it again, and rule 3 no longer treats an excluded
    league as a way to satisfy the non-MLB requirement.

**What could not be changed:** the newsletter published at 2:39 PM CDT on
Aug 24 went out with the WNBA game as the free pick. Sent email cannot be
recalled. That issue is the one remaining place the pick exists.

**Root cause worth noting:** the diversification mandate (rule 3) rewarded
picking *any* non-MLB sport with a card, and there was no list of which
leagues the site actually covers. The routine did what it was told. The fix is
the covered-leagues list, not more judgement at selection time.

---

## Thu Aug 27, 2026 — TOUR Championship page, post-Round-1 honesty pass

**What changed on `pga.html`:**
  - The odds stamp now says plainly that the DraftKings prices are a
    **snapshot read at 8:26 PM CT on Aug 27, not a live feed**, and tells the
    reader to check their own book before acting on any number on the page.
  - The Round 1 summary line was factually wrong. It read "all 30 through 18"
    and called Spaun "+4, the only man over par," which implied he finished.
    He did not — **J.J. Spaun withdrew after five holes with a shoulder
    injury**, so 29 players completed the round. The line now says that.
  - The removed claim "entire field inside 12 shots" was dropped rather than
    recalculated, because the tail of the leaderboard could not be verified
    this run and a made-up spread is worse than no spread.
  - Spaun's table row is now labeled "(withdrew, R1)" so the em dash in the
    odds column reads as a reason, not a gap.
  - No odds figures were added or altered. No pick language was touched.

**On live outright odds — still unavailable to automation here.** This was
re-checked. ESPN's golf odds endpoint for event 401811964 could not be
retrieved at all this run (the host is unreachable from the sandbox, and the
in-app browser refuses espn.com), and it returned an empty set when it was
last reachable — ESPN does not carry golf outrights. VegasInsider's futures
page is pre-tournament only. Updated in-tournament prices live inside
sportsbook apps, which we do not scrape and will not log into. The prices
currently on the page were **hand-entered by Chuck off the DraftKings board**,
and the page now says so with a timestamp attached.

**A second data note worth keeping.** ESPN's public scoreboard feed still
reported the TOUR Championship as `STATUS_SCHEDULED` with all 30 players at
"E" at 10 PM ET Thursday, hours after Round 1 finished. Round 1 results were
confirmed instead from Golfweek, CBS Sports and USA TODAY reporting. Do not
trust that ESPN endpoint as the sole round-status check for golf.

**Not done, deliberately:** no pick added or changed, no other page touched,
nothing posted to X or Reddit.

---

## Sun Aug 30, 2026 — sent 8:16 AM CDT (target 9:30 AM) — ON TIME, 74 min early

**Subject:** A Full Run Came Off This Total and the Price Didn't Follow
**Sent to:** all free subscribers, Email and Web. Byline ITN Desk (single author,
no personal account attached).

**Audit counts.**
  - Sports: **MLB 2**. That is the whole card.
  - Bet types: **total 1 · runline 1**. Moneylines **0 of 2 (0%)**, inside the
    50% cap.
  - Lead / free pick: **Phillies at Angels, under 7.5 (-103)**, 4:07 PM ET.
    Site Pick of the Day and newsletter free pick match.
  - Support: **Brewers -1.5 (+123)** vs Texas, 2:10 PM ET, confidence 3.

**FOOTBALL FIRST could not be applied, and the exception is why.** There are
**zero** football games today. ESPN returns 0 events for both
`football/college-football?dates=20260830` and `football/nfl?dates=20260830`.
CFB Week 1 opened with eight games on Sat Aug 29 — all final — and does not
resume until **Thu Sep 3** (11 FBS games, verified). The NFL opener is the
following week. This is precisely the "day with zero football games" carve-out,
not a judgement call, and the newsletter says so in the first two paragraphs
rather than quietly leading with baseball.

**Why only two picks, not three or four.** The only non-MLB event on the board
was the **TOUR Championship final round**. Event name was verified against the
feed before use (per the Aug 28 wrong-tournament caution) — it returns
"TOUR Championship", Round 3 play complete, which is correct for a Sunday.
But `sports.core.api.espn.com/.../golf/leagues/pga/events/401811964/.../odds`
returns **count: 0**. No price, so no pick — rule 3e over rule 3c. With golf
out and max-two-per-sport in force, two MLB picks is the ceiling. The
TOUR Championship still ran as the trend/story section, and the newsletter
states plainly that we have no pick on it because we could not read a number.

**The pick itself.** PHI/LAA is the only total on a fourteen-game board that
moved a **full run** (8.5 → 7.5); everything else that moved, moved half.
Philadelphia's true price barely budged across that move — 66.6% implied at
open, 65.2% now — when a falling total should have pulled a favorite in. And
after the move the under is still the *cheaper* side at -103 against -116 on
the over. Direction plus the better price.

**Stale-game check:** earliest first pitch on the board is 12:15 PM ET
(11:15 AM CT). Both picks (1:10 PM CT and 3:07 PM CT) were hours from starting
at send. Nothing already underway was presented as bettable.

**cfb.html:** no CFB pick made the card, so the PICK:START/PICK:END block was
rewritten to say there are no college football games today and to point at the
baseball free pick, rather than leaving Saturday's two plays sitting there as a
stale promise. Markers kept.

**Correction made after send.** The newsletter's disclaimer says the odds were
read at "8:35 AM CT". They were actually read between **8:08 and 8:15 AM CT** —
8:35 was a forward-guess written while drafting and it went out wrong. The
number itself is right; only the read-time stamp is off by twenty minutes.
index.html and cfb.html have been corrected to 8:15 AM CT. **Lesson: stamp the
read time from `date`, never from an estimate of when the send will land.**

**Infrastructure notes.**
  - `scripts/build_slate.py` produced **nothing** — every ESPN call from the
    sandbox failed with `Tunnel connection failed: 403 Forbidden`, and the
    script cheerfully wrote a 0-game brief.json and exited 0. The whole survey
    had to be re-done by hand through the browser's JS console against the same
    endpoints, which work fine from there. **The sandbox cannot reach ESPN.**
    build_slate.py should fail loudly on an all-sports fetch failure instead of
    reporting an empty board, which is indistinguishable from a real off-day.
  - Fresh `mktemp -d` clone, as required. No shared working copy touched.
  - Push needed `git -c credential.helper="$PWD/itn-git-credential.sh"` — a
    fresh clone carries no local credential.helper config, and `$HOME` in the
    sandbox is not the Mac home, so the documented
    `ITN_SECRETS="$HOME/Documents/..."` path does not resolve. Correct sandbox
    path is `/sessions/<id>/mnt/Projects/Inside the Number/itn-secrets.env`.
  - Deploy verified live on the first cachebust fetch. No stale-cache retry
    needed.

**Verified by the 9:34 AM safety-net run (`itn-deadline-check-weekend`).**
beehiiv's post list at 9:35 AM CDT shows "A Full Run Came Off This Total and
the Price Didn't Follow" published Sun, Aug 30, 2026 8:16 AM CDT — **1h14m
ahead of the 9:30 AM target**. No recovery action needed, and Chuck was not
messaged, per Step 3. Appended here rather than added as a duplicate Aug 30
row (same convention as Aug 25, 27 and 29). **Counting note for the Sept 3
reliability decision: a clean, fully unattended green day, the second in a
row** after Aug 29 — though see the build_slate.py note above, which means the
survey inside that run was not itself unattended.

**Git — ninth occurrence of the lock/permission failure (Aug 20, 21, 23, 24,
25, 26, 27, 29, 30).** This safety-net run hit it too: `.git/HEAD.lock` in the
shared folder is still undeletable from the sandbox ("Operation not permitted")
and `git commit` refused to run. Pushed from a fresh `mktemp -d` clone as usual.

**A real mistake by this run, caught and reverted — worth recording because the
next run can repeat it.** The first push (`11acf67`) copied SEND_LOG.md up from
the SHARED FOLDER working copy, which is stranded at an Aug 26 commit. That
overwrote origin's current log with a three-day-old version: it deleted this
entire Aug 30 section and the full Aug 29 audit row written by the main
routine, replacing them with two thin rows reconstructed from beehiiv
timestamps alone — 76 lines lost, including the FOOTBALL-FIRST exception
reasoning, the golf `count: 0` note and the read-time correction. Restored from
`6f1e669` in the same session; nothing was lost permanently and the live site
was never affected. **Root cause: the shared working copy is not a valid source
of file content while it is diverged.** The fresh-clone workaround was being
used for the *push* but not for the *read*. Any future run that edits a
repo-tracked file from the sandbox must edit it inside the fresh clone, on top
of origin/main — never copy the shared-folder version over origin's. The
underlying fix is still the one outstanding since Aug 26: the local repo needs
`rm -f .git/*.lock; git fetch origin && git reset --hard origin/main` run by
hand in Terminal. It is now four days stale and has caused an actual data loss
incident rather than just noise.


---

## Mon Aug 31, 2026 — recovery send at 2:33 PM CDT (target 1:00 PM) — MISSED by 1h33m

**Subject:** The Two Best Arms on the Board Are Priced Like the Worst
**Sent to:** all free subscribers, Email and Web. Byline ITN Desk.
**URL:** https://insidethenumber.beehiiv.com/p/the-two-best-arms-on-the-board-are-priced-like-the-worst

**What failed.** `itn-daily-weekday` produced no beehiiv post, no site commit and no
log row. Origin's two most recent commits before this run were both from the
GitHub Actions slate pipeline, not the routine, which points at a task that never
started rather than one that stalled. Same signature as Aug 24, Aug 26 and Aug 28.
**Four of the last five weekdays have now failed unattended.** The safety net has
caught every one of them, which means the deadline column in the table above is a
much rosier picture than the automation deserves — worth weighting heavily in the
Sept 3 decision.

**Audit counts.**
  - Sports: **MLB 2**. That is the whole card.
  - Bet types: **total 1 · runline 1**. Moneylines **0 of 2**.
  - Free pick: **Brewers at Cubs, under 9.5 (-110)**, 7:40 PM ET. Site Pick of the
    Day and newsletter free pick match.
  - Support: **Braves -1.5 (+105)** vs San Francisco, 6:05 PM ET, confidence 3.

**The pick.** Kyle Harrison (2.79) and Clay Holmes (2.26) are 5.05 combined — the
lowest starting-pitcher pair on a twelve-game board, with the next-best at 6.84.
That game is priced at 9.5, the highest total on the card outside Coors. Every
other game set at 9 or above has a starting pair at 6.84 or worse. The line has not
moved off 9.5 since open; the over has gone +100 → -110, so the book took money and
held the number. No-vig is a clean 50/50 at -110 apiece, so there is no price edge
on either side and this is purely a disagreement about the run environment. The
issue states the case against plainly — Wrigley with the wind out is the standard
way this profile dies.

**FOOTBALL FIRST could not be applied, and this is the carve-out, not a judgement
call.** ESPN returns 0 events for college football and 0 for the NFL on Aug 31,
Sep 1 and Sep 2. CFB resumes **Thu Sep 3 with 11 FBS games** (verified against the
scoreboard endpoint). NBA, CBB, NHL and UFC all return 0. The TOUR Championship is
`STATUS_FINAL` with `count: 0` on its odds endpoint — unpriceable, so no pick, per
the same golf-odds gap logged Aug 27, 29 and 30. MLB was the entire board.

**Stale-game check.** All twelve MLB games were `STATUS_SCHEDULED` at write time.
Earliest first pitch anywhere on the board was 6:05 PM ET, 2h32m after the send;
the free pick's was 7:40 PM ET, 4h07m after. Nothing in play was presented as
bettable.

**Infrastructure notes.**
  - **The sandbox still cannot reach ESPN** — every call returns
    `Tunnel connection failed: 403 Forbidden`, so the whole survey ran through the
    browser's JS console against the same endpoints, which work fine there. This is
    the second consecutive day this has been logged and `scripts/build_slate.py`
    still exits 0 on a total fetch failure, reporting an empty board that is
    indistinguishable from a real off-day. Unfixed.
  - Edits were made **inside the fresh clone on top of origin/main**, never copied
    up from the shared folder — the specific mistake that caused the Aug 30 data
    loss. No recurrence.
  - Push required copying `itn-git-credential.sh` and `itn-secrets.env` into a
    space-free `mktemp -d` directory first; the helper cannot be invoked from a
    path containing spaces. Same wrinkle as Aug 28.
  - Deploy verified live on the second cachebust fetch (the first was still serving
    the Aug 30 card). Bounded at two checks; no retry loop.
  - beehiiv session was live — no login redirect. The Aug 26 outage remains
    resolved.
  - Publishing mechanics: the composer body was filled with the documented
    synthetic-paste method (DataTransfer + ClipboardEvent into `.ProseMirror`) and
    verified by marker order before publishing. Title and subtitle accepted plain
    keystrokes. The publish control on the Review step is labeled **Schedule**, not
    Publish — clicking it opens a "When should this publish?" modal where
    **Publish now** is the fourth option. Worth documenting: a run looking for a
    button labeled "Publish" will not find one.

**Counting note for the Sept 3 reliability decision: this is a miss for the main
routine and a save for the safety net.** Weekday record since the safety net went
in is poor — the unattended weekday routine has completed on its own on very few of
the days it was supposed to. The weekend routine, by contrast, has been clean
(Aug 29 and Aug 30 both green and fully unattended). If the decision is framed as
"is local automation reliable enough," the honest answer from this log is that it
is reliable on weekends and unreliable on weekdays, and nobody has yet explained
why the weekday task specifically keeps failing to start.

**Schedule rewrite — Sep 2, 2026 (Chuck's request, 7:24 AM).** Targets changed and the send mechanism changed. Weekdays (non-holiday): task starts 8:00 AM CT and SCHEDULES the issue in Beehiiv for exactly 10:00 AM CT; safety net at 9:10 (pre-flight) and 10:10 (post-flight). Weekends and holidays: task fires 6:15 AM CT and schedules the issue for exactly 7:45 AM CT; safety net at 7:10 and 8:10. Rows dated Sep 3 or later are measured against these targets. Beehiiv's "Pick a specific time" scheduler was verified to parse "today at 10:00am" as 10:00 AM CDT.
| 2026-09-03 | Thu | 10:00 AM | 10:15 AM CDT | NO (+15m), recovery run | Main routine (`itn-daily-weekday`) did not complete under the new schedule. The 6:41 AM slate pass did not produce a fresh brief (the one that exists was generated 9:28 AM CT, the second pass), and the 8:00 AM task never updated `index.html` — `todaysGames` still carried Tue Sep 2's Brewers/Cubs card at 9:37 AM CDT, and nothing was scheduled or published in Beehiiv. **Pre-flight safety net (`itn-deadline-check-weekday`, ~9:37 AM run):** confirmed nothing scheduled/published, cloned fresh, surveyed the full board (`data/brief-latest.json`, generated 9:28 AM CT, plus live ESPN team-id lookups), and pushed the card to `index.html` at **10:08 AM** (commit `4e15e06`). By the time the card was set, real time had passed the 9:50 AM cutoff for scheduling, so the issue was drafted and **published immediately at 10:15 AM CDT** rather than scheduled for 10:00 — the 10:00 slot itself was missed by definition once the 8:00 AM task failed to run. **AUDIT — Sports: CFB 1 · MLB 1. Bet types: spread 1 · moneyline 1 (1 of 2, at the cap).** Max-two-per-sport met. Football-first applied: CFB led as the free pick since CFB had games today (first time this rule has actually applied — every prior weekday since Aug 24 had a zero-CFB/zero-NFL board). **Card:** free pick Colorado +6.5 at Georgia Tech, 8:00 PM ET — Georgia Tech opened -290 on the moneyline and -7 on the spread against a 0-0 opponent; both numbers have come in (-238, +6.5) with no in-season result to justify the move. Also Royals -118 vs Miami, 7:40 PM ET — Kansas City opened as a +106 home underdog to a 71-69 Miami team and is now a -118 favorite over a 62-78 team, a full moneyline flip overnight. Published "Georgia Tech Opened at -290. It's Already Down to -238." to Email and Web, all free subscribers, bylined ITN Desk, 493 words. **Stale-game check:** Colorado/Georgia Tech kicks 8:00 PM ET, Royals/Marlins 7:40 PM ET; both roughly 9-10 hours after the send. Nothing in play was presented as bettable. **Git:** fresh `mktemp -d` clone for both the card push and this log row, never the shared working copy; credential helper and `itn-secrets.env` copied to a space-free temp path first, same wrinkle as every prior recovery run. **Note on this row:** a concurrent session (`docs/sessions/2026-09-03.md`, commit `450a850`) logged the miss in narrative form at 10:14 AM while this recovery was still in progress and left the draft unpublished ("Chuck's standing pre-authorisation covers the scheduled tasks, not me in chat") — this safety-net run is the scheduled task and completed the publish at 10:15 AM. **Counting note for the reliability decision: this is the first weekday since the Sep 2 schedule rewrite, and it is a miss for the main routine (both the 6:41 AM slate pass and the 8:00 AM card/schedule task) and a save for the safety net.** The rewrite fixed the target time; it has not yet fixed the runner.

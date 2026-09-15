> ## ⚠️ PIVOT NOTICE — Sep 15, 2026, supersedes everything below
>
> Per `DECISION-ANONYMOUS-TOOLS-PIVOT-2026-09-14.md`, Inside the Number no
> longer sells picks. **There is no ITN Pro, no $17.99/mo tier, no paid
> picks product, and no daily "stated side and number."** The site's job is
> live odds, line movement, the no-vig true price, and the key numbers —
> free, on every game, on every board. The newsletter's job is the same
> thing in your inbox, not a pick.
>
> This also retires **record.html**, which the Aug 22 banner below already
> said was deleted — it still is (confirmed against the live repo tree,
> Sep 15). Every instruction below that references logging a result, a
> win/loss record, ROI, units, or linking to `/record` is dead. So is every
> reference to `inside_the_number.html` — that file does not exist in the
> live repo either; the live homepage is `index.html`, full stop.
>
> **What the daily routine is now:** research the board (all covered
> sports), make sure CFB and NFL are current and dated, write a no-vig/
> line-movement read of what's interesting today, and — only if Chuck has
> separately approved it — draft the newsletter around that. No forced
> side. No performance claims. See "The routine" below for the full
> replacement, and "Stale-content hard stop" for the check that keeps this
> from ever again showing yesterday's board on today's date.
>
> **Social posting stays paused** unless Chuck separately approves it in
> writing for that day. See the dedicated section near the end. This
> overrides anything below or in `x-posts.yml`/`ig-publish.yml`/
> `reply-ammo.yml` that assumes posting is on by default.

---

**READ NORTH_STAR.md FIRST.** The goal is traffic → subscribers → passive
income. Every task must put a new human in front of the site or newsletter;
building for its own sake waits.

**ANTI-HANG RULES — still in force, unchanged by the pivot. They bind every
scheduled task and outrank anything below that conflicts with them.**

1. **Run `date` at the start of EVERY numbered step.** A stalled run has no
   other way to notice it is late.
2. **No unbounded loops, ever.** Any scroll-to-accumulate, poll-until-ready,
   or retry loop needs both a hard iteration cap (12 is plenty) and a
   wall-clock deadline.
3. **Two strikes on any single check.** If a page, fetch, or script fails
   twice, stop, write down what is missing, and move on.
4. **A wedged browser tab is fixed by closing it, not by waiting.**
5. **Keep any single bash call small.** Clone → edit → verify → commit →
   push belongs in one call; the filesystem does not survive between calls.
6. **Shipping beats polish.** Past the deadline, stop building and publish
   what exists — accurate and dated beats complete.
7. **If a DRAFT_<today>.md exists in the repo, read it first.**

---

# Inside the Number — daily morning routine

> **ACCOUNTS: every Google surface uses `insidethenumber.itn@gmail.com`.
> Never another account. Check the avatar top-right before any signed-in
> action. See ACCOUNTS.md.**

> **Beehiiv: stay on the publishing path.** The daily run (when newsletter
> sending is separately approved — see "Social posting stays paused") needs
> exactly two areas — `app.beehiiv.com/posts` (check nothing is already
> published) and `app.beehiiv.com/posts/new` (write and publish). Do not
> open Automations, Settings, Billing, or Design.
>
> **Beehiiv plan:** Launch (free, up to 2,500 subscribers). Publishing and
> email delivery are included.

## The routine (copy/paste this)

```
Morning. Run today's Inside the Number board update:

1. Run `date`. Confirm today's actual date before doing anything else —
   every timestamp written to the site this run must match it.

2. Survey the whole board across every covered sport before writing
   anything: MLB, NFL, CFB, NBA, CBB, NHL, UFC, PGA. (The WNBA stays
   excluded — Chuck's call, unchanged by this pivot.) Pull live odds
   directly from sportsbook/odds pages, not just search summaries.

3. For CFB and NFL specifically (football-first priority while football
   traffic is active): confirm the current week/slate, the current lines,
   and which numbers have moved since they opened. Write this as
   board-reading, not a pick — the no-vig true price on each side, the
   key numbers (3, 7, 10 for football), and what a line move of a given
   size tends to mean. No stated side. No "our pick." No confidence
   rating.

4. Update `cfb.html` and `nfl.html` between their existing
   `<!-- PICK:START -->...<!-- PICK:END -->` markers (keep the markers —
   other tooling depends on them existing) with today's board read in the
   voice above. Every block you write must carry a visible, correct
   date/timestamp (the page's `<div class="stamp">` or equivalent) —
   never leave yesterday's date live under today's copy.

5. BEFORE pushing, run the stale-content check below. If it fails, STOP —
   do not push a page that still shows a prior day's date or slate in
   user-visible text.

6. Push the live site after editing. Editing files locally only changes
   local copies; the public site (insidethenumber.com, Cloudflare
   auto-deploy on push to `main`) is a separate step:

     rm -rf /tmp/itn && git clone -q https://github.com/insidethenumber/inside-the-number-site.git /tmp/itn
     cd /tmp/itn
     # edit index.html / cfb.html / nfl.html / games.html here — never in the shared Documents folder
     git add index.html cfb.html nfl.html games.html
     git commit -m "Board update: <short description>"
     git push origin main

   Cloudflare picks up the push automatically, rebuilds within ~30-60s.
   Never run git in the shared project folder — see "Repo health" below.

7. Newsletter draft is OPTIONAL and requires Chuck's standing or
   same-day approval — see "Social posting stays paused." If approved:
   draft a plain board-read email (today's most interesting line moves,
   the no-vig math on 2-3 games, what to watch) — no "today's free pick,"
   no membership pitch, no record link (record.html does not exist).
   Byline "ITN Desk." Message Chuck a short summary; do not send until he
   replies "send."
```

**Note on automation:** the scheduled tasks `itn-daily-weekday` /
`itn-daily-weekend` are a separate, standing setup with their own
self-contained prompts. **Those prompts are authoritative** where they
disagree with this reference doc — but as of this pivot, if those task
prompts still describe ITN Pro, a stated pick, or a record link, they are
themselves out of date and need the same correction described here before
they next run unattended. This patch does not edit those task prompts
directly (not in the repo `DAILY_MORNING_PROMPT.md` covers) — flagged in
the accompanying report as a follow-up.

## Stale-content hard stop (added Sep 15, 2026 — required, not optional)

Before any push in step 6 above, run this check. It exists because
`cfb.html` sat showing "updated Monday, Sep 14... No pick yet" through all
of Tuesday, Sep 15 — the routine simply hadn't run yet, and nothing caught
it before a visitor did.

```
for f in index.html cfb.html games.html nfl.html; do
  # 1. Extract whatever this page uses for its freshness timestamp
  #    (class="stamp", class="potd-date", or equivalent) and confirm it
  #    parses to TODAY's date, not any other day.
  # 2. Grep the page's user-visible board/pick region for weekday names
  #    or dates that do not match today (e.g. yesterday's or last
  #    Saturday's weekday name appearing where today's should be).
  # 3. If either check fails: STOP. Do not push. Write down exactly
  #    which file/section is stale and say so in the run summary to
  #    Chuck instead of pushing anyway.
done
```

Two strikes, same as the anti-hang rules: if a freshness check itself
can't be completed (page unreachable, markup changed shape), that also
counts as a failure — stop and report, don't assume it's fine and push.

This check is independent of `.github/workflows/site-watchdog.yml`, which
only verifies `index.html`'s `potd-date`. This step is the routine's own
responsibility for `cfb.html`, `nfl.html`, and `games.html` too, since the
watchdog does not cover them.

## Social posting stays paused

`x-posts.yml`, `ig-publish.yml`, and `reply-ammo.yml` exist in this repo
and may still run on their own schedules. **Per
`DECISION-ANONYMOUS-TOOLS-PIVOT-2026-09-14.md`, no automated public social
posting, content publishing, or site self-repair happens until Chuck gives
narrow, explicit, same-day (or clearly time-boxed) approval.** The daily
morning routine does not trigger, queue, or approve any social post as
a side effect of updating the board. If a scheduled social workflow fires
on its own, that is a separate compliance question from this routine, not
something this prompt authorizes.

## Repo health — ALWAYS work from a fresh clone (unchanged, still correct)

**Never run git in the shared project folder. Clone, work, push, discard.**

```
rm -rf /tmp/itn
git clone -q https://github.com/insidethenumber/inside-the-number-site.git /tmp/itn
cd /tmp/itn
# edit, commit, push from here — never from the Documents folder
```

Two different git clients writing the same working copy at once (a
scheduled task on Chuck's Mac, a Cowork session through a mount) is what
caused the Aug 25 lock collisions — not a stale lock file. A fresh clone
has no other writer and cannot collide. If a scheduled run is in flight,
don't push to the shared folder — check `lastRunAt` before assuming a task
has stalled.

## Reliability safeguards (unchanged by the pivot)

1. *Bounded deploy verification* — check the live site at most once after
   pushing, then move on regardless. Never loop on a stale-cache fetch.
2. *Idempotency check* — before drafting a newsletter (when approved),
   check Beehiiv for an existing post dated today, so a re-trigger can't
   cause a duplicate send.
3. *Deadline safety net* — scheduled check tasks confirm the board update
   actually happened and, separately, whether an approved newsletter went
   out; if not, they message Chuck rather than silently doing nothing.

## Event pages — cfb.html and nfl.html specifically

These are standalone pages built to rank in Google, and each carries a
board-read block between `<!-- PICK:START -->` / `<!-- PICK:END -->`
markers — **keep the markers**, other tooling (and this routine) depends
on them existing. Nothing updates these pages automatically; every update
to date has been placed by hand or by the routine above.

**Every time you touch one of these blocks:**
- Match the existing voice: the key number(s) in bold, the no-vig read,
  and what moved and why — never a stated side or a confidence rating.
- Update the page's date/timestamp element in the same edit. A dated
  freshness claim that's wrong is worse than no claim at all — that's
  exactly how "updated Monday" was still live Tuesday afternoon.
- If there's nothing new to say (bye weeks, no games), say that plainly
  with today's date attached, rather than leaving a prior day's text up
  unchanged.

## Site consistency rules (updated Sep 15, 2026 for the pivot)

**1. No confidence stars, no stated side, anywhere on the site.** The old
5-star confidence scale described a pick's conviction; there is no pick to
rate. If you find confidence stars anywhere, that's leftover picks-era
markup — flag it, don't reintroduce it.

**2. No win/loss record, win rate, ROI, or units anywhere on the site or
newsletter.** This was already the rule as of Aug 20, 2026, and remains
true for an added reason now: **record.html does not exist in the live
repo.** Do not link to `/record` or `insidethenumber.com/record` anywhere
— in the site, in the newsletter, or in social copy. If you find a link to
it, that's a dead link from before the pivot; flag it for removal in a
future site patch (this routine edits `cfb.html`/`nfl.html`/`index.html`
board content only, not link cleanup sitewide).

**3. Board content must be internally consistent.** If `index.html` and
`cfb.html`/`nfl.html` describe the same game differently (different line,
different date), that's the same class of bug as the old "site pick ≠
newsletter pick" drift — fix it before pushing, don't ship the
inconsistency.

## Newsletter format (when sending is separately approved — see "Social
posting stays paused")

Order: hook → today's most interesting board read (the lead, not "the
free pick") → a trend or line-movement story → what's coming → disclaimer.
**No results recap. No win/loss count. No season record, ROI, or units.
No membership pitch — there is no paid tier.** No link to `/record` — it
does not exist.

**Byline: always "ITN Desk" — never Chuck's name.** Use the "Authors"
control beneath the post title and select the guest author **ITN Desk**.
Remove Chuck's personal account from the author list if attached by
default.

## Diversification mandate — RETIRED (was Aug 22, 2026; no longer
applicable)

This section used to govern which sports a **pick** could come from and in
what mix (max 2 per sport, 50% moneyline cap, etc.). There is no pick
being selected anymore, so the mandate itself no longer applies. Kept here,
struck through in spirit, only so the sport-coverage list survives: **the
site still covers exactly MLB, NFL, CFB, NBA, CBB, NHL, UFC, PGA, and the
WNBA remains explicitly excluded** (Chuck's call, Aug 24 2026) — that part
of the old rule is about scope, not about picks, and still holds for what
the board-read may reference.

## Visuals — needs a follow-up pass, not covered by this patch

The pre-pivot newsletter visuals pipeline (`scripts/parlay_cards.py`,
`scripts/viz.py ticker`, the "THE FREE PICK" static card) is built around
a pick that no longer exists. **This patch does not rewrite the visuals
pipeline** — task scope here is the routine's picks-language and
stale-content problem, not the image scripts. If newsletter sending is
approved before the visuals pipeline is updated, either skip images for
that issue or adapt `viz.py ticker` to illustrate a line move without
"THE FREE PICK" framing. Flagged as a remaining risk in the report.

## Shorthand version (once we're in a rhythm)

```
Run today's board update. No pick, no ITN Pro, no record link.
```

---

## Notes on using this well

- **Timing:** research is most accurate close to when the board update
  actually goes live, since lines move during the day.
- **Sport filtering:** if you only want specific sports covered on a given
  day, say so in the prompt.
- **The final send (if newsletter sending is approved for that day) is
  always Chuck's call.** Nothing goes out until he replies "send."
- **No forced side, ever.** If the board doesn't justify saying anything
  interesting about a game, say that plainly instead of manufacturing a
  take.
- **The stale-content check is not optional.** Skipping it to save time is
  exactly how the Sep 15 incident happened.

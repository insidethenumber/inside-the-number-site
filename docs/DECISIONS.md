# DECISIONS.md — the things Chuck should never have to repeat

**Read this at the start of every session. Before telling Chuck something is
"ready", "working", or "done", check it against this file.**

Created Sep 2, 2026 after Chuck had to remind me, in one evening, that the
Caesars form was already known-broken, that BetMGM's verification had already
failed, and that the Reddit account he actually owns is not the one the
automation was checking. Each of those was already written down somewhere. The
problem was that nothing forced me to read it. This file is that force.

Format: one entry per decision or fact. Date, the fact, why it matters, and
what NOT to do. Newest at the top of each section. Never delete — strike
through and date the reversal.

---

## Standing orders (Chuck's calls)

- **2026-09-02 · X is OFF until new rules are written.** `itn-x-engagement-hourly`
  disabled; `x-posts.yml` schedule removed (manual-only). Do not post, reply,
  quote, repost or follow from @thenumberdesk until Chuck approves a written
  ruleset. Re-enable BOTH when he does.
- **2026-09-02 · Log every session** to `docs/sessions/YYYY-MM-DD.md`. What
  was done, what broke, what was fixed, what is unverified. Chuck should never
  have to check for inaccuracies himself.
- **2026-09-02 · The marketing punch list lives at `docs/MARKETING_PUNCHLIST.md`.**
  Every Monday the `itn-monday-growth-report` task sends Chuck the open items.
- **2026-09-02 · External strategy docs go in `docs/inputs/`.** Chuck will keep
  sending them. File each one, then extract the actionable items into the
  punch list with a source reference.
- **2026-09-02 · Goal is traffic → subscribers → passive income.** Nothing else.
  Building for its own sake waits. See NORTH_STAR.md.
- **2026-09-02 · X voice is BOTH meme and data.** "Everyone on X aren't robots,
  they are humans who love memes and relatable content." Emoji allowed on X
  as visual bullets. No-emoji rule is newsletter and site copy only.
- **2026-09-01 · The `free` flag gates the homepage.** Exactly one pick shows
  in full; the rest are "In today's newsletter". The newsletter must carry
  every pick on the card.
- **2026-08-29 · Football first.** When CFB or NFL has games, the lead pick is
  football.
- **2026-08-27 · Don't take Ls in public.** Losing picks are not acknowledged
  on X. Only plain factual errors get corrected or deleted.
- **2026-08-24 · WNBA is excluded.** Not close.
- **2026-08-22 · The public record is retired.** No W/L, ROI, units anywhere
  public. `PICK_LEDGER.md` is private grading only.
- **2026-08 · Not charging anyone yet.** $17.99/mo is the listed founding
  price; Pro stays a waitlist until there are real subscribers.

## Things that are BROKEN or DEAD — do not send Chuck to them

- **2026-09-02 · Caesars affiliate signup is broken ON THEIR END.** Submitting
  returns "result storage capacity has been reached for this form." Confirmed
  Aug 29 AND Sep 2. A form that renders is not a form that works. Support email
  unanswered. Do not send Chuck to fill it out again.
- **2026-09-02 · BetMGM Partners is UNVERIFIED end-to-end.** Registration wizard
  renders (4 steps). Last attempt the verification email never arrived; support
  email unanswered. Worth one attempt; never describe it as "working".
- **2026-09-01 · u/RockyTopEdge is BANNED sitewide on Reddit.** Dead. Do not
  check it, do not recreate it (ban evasion). Every Reddit doc before Sep 2
  said "you need a working account" — wrong, see next entry.
- **2026-08-31 · bet365 Partners rejected us** at the pre-questionnaire on
  traffic volume. Retry only once traffic is real.
- **2026-08-29 · FanDuel affiliate portal is dead** (`tba@tba.com` on its
  contact page). Abandoned.
- **2026-09-01 · Hard Rock affiliate declined** — demands bank details before
  approval. Chuck's call.
- **Sandbox network:** cannot reach ESPN (403), a.espncdn.com, fonts.gstatic.com,
  jsDelivr, unpkg, raw.githubusercontent.com. CAN reach github.com and pypi.
  Read ESPN through a browser tab. Fonts and logos get cached by CI
  (`cache-logos.yml`), never fetched from the sandbox.
- **Claude in Chrome cannot attach files to X posts** (`file_upload`
  unavailable). Images post via the API path: `post_to_x.py --image`.

## Accounts — which is which

- **Reddit: u/kceza1 is Chuck's personal account** ("Chuck | Nashville", years
  of history, good standing, verified Sep 2). The ammo pack is written for
  HIM to post from it. I do not post from it — an agent posting scheduled ITN
  comments from his real account is the pattern that got RockyTopEdge banned.
- **X: @thenumberdesk**, verified. Bio rewritten Sep 2. 33 followers.
- **Google surfaces: insidethenumber.itn@gmail.com** only.
- **Beehiiv:** Launch (free) plan, 4/2,500 subs, all four are Chuck's own
  addresses. Boosts (paid recommendations) require the Scale plan.
- **Gmail connector is chef@chefchuck.com** — not the ITN gmail.

## Things I got wrong and must not repeat

- **2026-09-02 · Told Chuck Caesars was "live again" because the page loaded.**
  Rule: never mark anything "ready for Chuck" on a page load. Carry it to a
  submit confirmation or call it UNVERIFIED.
- **2026-09-02 · Moved the newsletter build to 8:00 AM and broke its data
  dependency** (slate built at 9:17). Fixed same day: slate now builds 6:41.
  Rule: when moving a schedule, list what it consumes and check those times.
- **2026-09-02 · Said the Beehiiv test draft was deleted; I had clicked
  Cancel.** Deleted later, verified. Rule: verify destructive actions by
  re-reading state, not by remembering the click.
- **2026-09-02 · Let "you need a working Reddit account" stand for two days**
  while kceza1 sat there fine. Rule: when a doc says a resource is missing,
  check whether the OTHER account exists before repeating it.
- **2026-09-02 · Four rounds of X graphics Chuck didn't like.** Data tables
  in a feed that rewards five words of huge type. Rule: at thumbnail size,
  nobody reads a table. Rule: scroll our own timeline before designing.
- **2026-09-02 · Built infrastructure when Chuck asked for growth, repeatedly.**
  Rule: "does this put a new human in front of the site this week?" If no,
  it waits.
- **2026-09-02 (night) · Two silent data losses found while doing other work.**
  (a) The game-page generator never carried the `rel="me"` X link, so the
  link I "added to 179 pages" that morning was being stripped from 152 of
  them on every rebuild. (b) The slate builder read ESPN's opening lines and
  threw them away, so MARKET MOVERS — the franchise I called "genuinely
  real" — had no data behind it. Both fixed. Rule: a change made by editing
  generated files is not a change until it is in the generator. Rule: before
  calling a data franchise "real", open the JSON and find the field.
- **2026-09-02 (night) · The logo-cache job failed on its first run** (bot
  User-Agent, ESPN 403). Caught because I checked the run instead of
  assuming a green button meant a green job. Rule stands: verify the run.

## Honesty rules for content (non-negotiable)

- **No ticket/money splits.** We do not have that data (Action Network does).
- **No claimed model edge.** Our model de-vigs DraftKings against itself and
  cannot beat DraftKings. Private record 12-18 as of Sep 2. Any "market X% /
  ITN Y% / Z% edge" is fabricated.
- **No public record.** Retired Aug 22.
- **No "sharps moved it".** We can see that a number moved, not who moved it.
- **Every number verified this run** from a live feed or a page just loaded.
- **Never expand a name from an initial without checking** ("Colin" for Clay
  Holmes shipped wrong).
- **No "vig/juice/hold"** in newsletter or site copy — "the book's cut".
- **American spellings.**

## Timing (as of Sep 2)

- Weekday newsletter: builds 8:00 AM CT, scheduled to send 10:00 AM CT.
  Safety net 9:10 / 10:10. First real run Sep 3 — UNVERIFIED until then.
- Weekend/holiday newsletter: builds 6:15 AM CT, sends 7:45 AM CT. Safety net
  7:10 / 8:10. Chuck must keep the Mac awake at 6:15.
- Slate data: GitHub Action at 6:41 / 9:17 / 11:47 AM / 2:23 PM CT.
- Holidays are listed in the task prompts; the weekend task owns them.

## Sep 4, 2026 — /parlay page, and results on the CFB board

**Parlay of the Day page (`/parlay`).** Chuck asked whether it was a good idea.
Yes, with one condition, and the condition is the whole product: the cost leads.
Our pitch is that we tell people what a price actually costs them, and a parlay
is the worst-priced thing on the board. Three legs and a payout would make us
the thing we criticise. So the page prints the break-even the ticket needs, the
chance three independent bets actually land, and the gap between them, above the
fold, every day.

Built as `scripts/build_parlay_page.py`, fed by the SAME spec JSON that renders
the slip card in `scripts/parlay_cards.py` — one source of truth, so the graphic
on X and the page it links to cannot disagree. Archive in `data/parlays.json`
accumulates under the fold, which is what gives the page depth instead of it
being thin on day one.

Kickoff guard: every leg carries its start time and the browser marks it
STARTED/FINAL and locks the card once all three are away. A dated page still
presenting a game that kicked off three hours ago as bettable is the fastest way
to lose a reader, and it is the failure mode this page was always going to have.

Honest expectation on SEO: we will not rank for "parlay of the day" — Action
Network, Covers and Pickswise own it. The value is a real landing page for the X
post and internal support for `/parlay-calculator`, which is the page that can
actually rank.

**Results on the CFB board.** Chuck: "there should be results from yesterday's
games. Please always do this in the evening or live." Built as live reads rather
than an evening job, because a job that has to run is a job that can be missed:

- The board window now always reaches back to include yesterday (it used to jump
  forward to the next Saturday on Tuesday and drop the weekend entirely).
- Final games show the score, who covered, and the total result. In-progress
  games show a live clock and score. The page re-reads the feed every minute
  while anything is live, every ten otherwise, and not at all in a hidden tab.
- ESPN strips the odds block from a game once it is final, so the board would
  know the score but not the number to grade it against. Finals therefore pull
  the closing spread and total from the summary endpoint (pickcenter), once
  each, after the board has already painted.

Day headers now read e.g. "11 games · 5 of 11 favorites covered". That is a fact
about the market, not a record of ours — the no-W/L rule is untouched.

## Sep 4, 2026 — the nav was dead on every page but two

Chuck, on the CFB page: clicking the ITN logo or HOME just reloaded CFB. It was
not a CFB bug. Fourteen pages shipped `<a class="nav-brand" href="">` and
`<a href="">Home</a>`. An empty href resolves to the current URL, so every logo
and every Home link on the site reloaded the page you were already on. Only
index.html (which used `#top`) and ufc.html (`index.html`) were unaffected, which
is why it survived earlier nav checks — those checks confirmed the links existed
and were styled, not that they went anywhere.

Fixed: 40 links across 14 pages, all now `href="/"`, desktop nav and mobile menu
both. Verified by clicking, live, not by reading markup — from /cfb and /tools
the logo and Home both land on the homepage.

Also swept every internal href and src on every page for dead targets. Clean:
the only unresolved matches are JS template literals (`${g.a.logo}`) and the
tel:/sms: helpline links on the responsible-gambling page.

**Standing rule going forward: a link is not fixed until it has been clicked.**
Grepping for `href=` proves a link is present. It does not prove it works. Every
nav audit from here clicks through at least one page per template.

## Sep 5, 2026 — Newsletter visuals are built by script, never by hand
The Sep 5 7:45 issue shipped with zero images because the task prompt said text/plain and never mentioned images. From now on: `scripts/newsletter_assets.py --issue issue.json` produces every image AND the paste-ready `issue.html` in one run; the task pastes that file as text/html and refuses to schedule with fewer than 3 `.ProseMirror img` (one fresh-duplicate retry, then fall back and report). The task prompt is authoritative over DAILY_MORNING_PROMPT.md, so mechanics changes must land in the task prompt itself, not only in the docs.

## Sep 5, 2026 — Mockups from other sessions get re-verified against the live board before use
x-posts-preview-2026-09-05.html carried 46/68 (live: 47), LSU -375 (live: -380), and named Clemson +10 as the free pick while the site said Tulane +7.5. Concepts are reusable; numbers are re-pulled the day of.

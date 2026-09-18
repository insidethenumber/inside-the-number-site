# Market Board — specification and current state

**The Market Board is `/games`.** It already existed as the cross-sport board and is the most-linked page on the site. This sprint improved it; it did not build a second one. `/nfl` and `/cfb` are sport-specific boards built on the same feed and remain the deep views for football.

**Live URL:** `https://insidethenumber.com/games` (`?sport=NFL|CFB|MLB|UFC|PGA|CBB|NBA|NHL`)

## Field coverage — what a visitor sees

| Required field | Where it appears | State before this sprint | Now |
|---|---|---|---|
| Sport | League rail + card badge | ✅ | ✅ |
| Matchup / event | Card | ✅ | ✅ |
| Market type | Expanded card: moneyline, spread, total | ✅ | ✅ |
| Current line / price | Card + expanded rows | ✅ | ✅ |
| Implied probability | Expanded card ("true price", vig removed) | ✅ | ✅ |
| **Source** | `#board-stamp` — "Lines via ESPN (DraftKings prices)" | ❌ not stated | ✅ |
| **Timestamp** | `#board-stamp` — "read 9:02 PM CT" | ❌ none | ✅ |
| Opening vs current | Expanded card ("since the number opened") | ✅ | ✅ |
| Movement amount | Expanded card | ✅ | ✅ |
| Plain-English movement explanation | Expanded card + "How to read" bullet 3 | ✅ / ➕ | ✅ |
| **Stale-data warning** | `#board-stamp.warn` — "Feed not reached — nothing on this page is current" | ❌ silent | ✅ |
| **Source link** | "ESPN" in the stamp → ESPN's public scoreboard for the selected league | ❌ | ✅ |
| **How to read this board** | Static section under the board | ❌ | ✅ |
| Prediction-market comparison | Static line: "not shown", with the condition for showing it | ❌ | ✅ honest unavailable state |

## The four states, and what each shows

| State | Stamp | Board | Verified |
|---|---|---|---|
| **Valid feed** | `Lines via ESPN (DraftKings prices) · read 9:02 PM CT · 12 games on the feed · prices move — recheck before you use one` | Cards, counts in the rail | 390 + 1280, Sep 18 |
| **Empty feed / outage** (every league fetch fails) | Amber: `Feed not reached — nothing on this page is current. Try again in a minute.` | Rail shows `—` for every league; the empty-league view | 390 + 1280, Sep 18 |
| **Stale** (page left open) | The read time is visible and does not advance. Bullet 4 tells the visitor that time is the only one that counts | Unchanged | By design — no cached prices exist to go stale silently |
| **Market closed** (game started/finished) | Normal stamp | `—` in place of a price; bullet 5 explains why | Live tonight: all 9 MLB games |

The stamp is written by the same fetch that fills the board. It cannot show a time the feed did not answer at, and it never carries a hard-coded date.

## What was deliberately not built

- No new route, template or nav item.
- No client-side price cache — a cache is exactly what turns "stale" into "silently wrong".
- No prediction-market column (see `DATA-SOURCES-AND-LICENSING.md`).
- No NBA / NHL / CBB content. The leagues exist in the rail with an honest empty state; building them out is future expansion, contingent on a real user need and valid data.
- No change to `/nfl`, `/cfb`, `/mlb-playoffs`, `/ufc-331-odds` — they already carry source, stamp or snapshot date, and explainers.

## Code change

`games.html` only — 68 insertions, 0 deletions, two commits (`8ae8c0f`, `dd7ce1b`). Additions: a `#board-stamp` element with scoped CSS, a `feedOk` flag set when any league returns 200, `stampBoard()` called after `route()`, a per-league public-source href set inside `rail()`, and one static `<section>`.

## QA

Rebuilt in the browser from live HTML with index-addressed chunks and SHA-256-matched to `8ae8c0f` (`2149653f…`). Four renders: valid×390, valid×1280, outage×390, outage×1280. Overflow 0 in all four. Ten anchors past the 390px edge were all inside the pre-existing horizontally-scrolling `#rail` and `#tick`; zero unexplained. Per-league source href verified for NFL, CFB, MLB, UFC. Signup embed present in all four. All four "how to read" links resolve to existing routes.

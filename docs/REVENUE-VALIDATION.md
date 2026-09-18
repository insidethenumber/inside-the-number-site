# Revenue validation — the business path, without billing

**Nothing is charged this weekend. No payment system exists. No paid tier is created.** This documents the path and the evidence required before any of it is built.

## Free, today

Public Market Board (`/games`, `/nfl`, `/cfb`) · the guides (`/football-line-movement`, `/mlb-playoffs`, `/ufc-331-odds`) · ten calculators · the free Beehiiv signup with the No-Vig Cheat Sheet.

## Possible paid offer, later

| Tier | Price | What it sells |
|---|---|---|
| **Daily Market Note** | $7 / month | Five minutes each morning: what moved overnight, which sport, what the price implies, why it matters. **Sells time and clarity, not outcomes** |
| **Deeper reports + alerts** | $12–15 / month | Sport-specific briefings, movement alerts on a chosen slate, historical open-to-close views |

**What it must never promise:** winning bets, picks, a record, an edge, or "sharp" information. The pitch is *understand the number before you act on it*, and the product is the reader's time back. That constraint is a feature — it is the one thing the picks-sellers cannot copy.

## Evidence required before adding billing — all of it, not some

| # | Evidence | Why it gates billing |
|---|---|---|
| 1 | **≥ 100 active free subscribers** with an open rate above 40% across at least four sends | Three subscribers cannot validate a price point. A paid tier on top of three is theater |
| 2 | **Returning visitors ≥ 20% of visits** over a 21-day window (Cloudflare) | A Market Note is a habit product; no return visits means no habit |
| 3 | **≥ 5 unsolicited replies or DMs** asking for more, faster, or deeper | Demand has to be expressed, not inferred |
| 4 | **A free "Market Note" sent for 14 consecutive days** without a missed morning | Proves the operating cadence exists before anyone pays for it |
| 5 | **Legal review** of (a) ESPN/DraftKings price display and (b) whether the Note is advice in target states | See `DATA-SOURCES-AND-LICENSING.md` |
| 6 | **Beehiiv description fixed** — it still says "one free pick every morning" | Cannot sell "no picks" while the signup page promises one |

## Other revenue lines — documented, not pursued this sprint

- **Referral partnerships:** only with licensed operators, only where the state permits affiliate marketing, only with the required disclosures on every page carrying a link. Earlier applications (bet365 Partners, Underdog) are on file. Not activated.
- **Sponsorship:** a single "presented by" line in the Market Note. Requires the subscriber base above first.
- **Data licensing:** *inbound* — the site licenses nothing out and has nothing proprietary to license.

## What kills the paid idea

If the 21-day scorecard shows no returning visitors and no subscriber growth from content pages, the Note has no audience, and the right move is to stop — not to add a paywall to a page nobody returns to.

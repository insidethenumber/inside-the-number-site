# Data sources and licensing

Honest inventory of every number the site shows, where it comes from, and what is and is not licensed.

## Sources in use

| Data | Source | Access | Used on | Licensing status |
|---|---|---|---|---|
| Scores, schedules, status | ESPN public site API (`site.api.espn.com`) | Unauthenticated public endpoint, fetched client-side | All boards | **Unlicensed public endpoint.** ESPN publishes no terms for it and could restrict it at any time. Treated as best-effort; every page fails honestly if it stops answering |
| Sportsbook prices (spread, total, moneyline) | The `odds` object on the same ESPN payload, attributed by ESPN to **DraftKings** | Same | All boards, guides | **Same status.** We display ESPN's attribution and link to ESPN's public page. We do not scrape DraftKings and hold no agreement with either |
| UFC prices | `sports.core.api.espn.com` odds endpoint | Same | `/ufc-331-odds`, `/games?sport=UFC` | Same. Paired by athlete ID, not array position |
| MLB standings, probables | ESPN + `statsapi.mlb.com` | Public | `/games` MLB view | Same status |
| Daily slate brief | `data/brief-*.json`, built by `daily-slate.yml` from the above | Repo | Homepage ticker | Derived from the above |
| Email metrics | Beehiiv API | Authenticated (owner's account) | Docs only | Licensed to the account |

**What is not used:** no paid odds API, no screen-scraping of any sportsbook, no broadcast footage, no licensed team logos in social assets (team logos on the board are ESPN-hosted images loaded from ESPN's CDN under the same best-effort status).

## Prediction markets — not shown, and why

| Platform | Public API | Licensed to ITN | Shown |
|---|---|---|---|
| Kalshi | Has a documented API with terms; sports contracts subject to state-by-state regulatory status | **No** | No |
| Polymarket | Has a public API; US access restrictions apply | **No** | No |
| Novig | No documented public data API | **No** | No — and the brief explicitly forbids scraping it |

**Requirement before a comparison column ships:** a documented API or data agreement whose terms permit display on a third-party site, with attribution; a per-quote timestamp; a bid/ask where the platform exposes one; and a link to the platform's own terms. Until then the board says "not shown" rather than "coming soon" or a guessed number.

## Legal posture

Inside the Number is not a sportsbook, exchange, operator or adviser. It takes no funds, matches no trades, holds no positions and sells no picks. The footer disclaimer and `/responsible-gambling` are on every page. **Two items require a lawyer, not Claude:** (1) whether continued display of ESPN-attributed DraftKings prices needs a data agreement at any traffic level, and (2) whether any future paid Market Note constitutes advice in the states it is sold in. Both are listed in `REVENUE-VALIDATION.md` as blockers to billing.

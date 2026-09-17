# SEO implementation report

**Branch:** `sprint-m27` · **Base:** `origin/main` `dd29053` · **Date:** Sep 17, 2026
Only high-confidence, clearly justified fixes. No keyword pages, no thin articles, no new sports.

---

## The eight priority routes, before and after

| Route | Title | Desc | Body inbound | `h2` | Schema | Signup |
|---|---|---|---|---|---|---|
| `/nfl` | 78 → **44** | 178 → **149** | 13 | 1 → **1** *(now a real `h2`)* | Breadcrumb → **+Organization, +WebPage** | ✅ |
| `/cfb` | 91 → **50** | 186 → **139** | 12 | **0 → 1** | unchanged | ✅ |
| `/games` | 81 → **49** | 172 → **139** | 24 | 0 | unchanged | ✅ |
| `/football-line-movement` | 58 | 175 → **141** | **4 → 7** | 11 | Article+FAQPage | ✅ |
| `/mlb-playoffs` | 48 | 140 | **5 → 8** | 11 | Article+FAQPage | ✅ |
| `/ufc-331-odds` | 62 | 205 → **149** | **2 → 5** | 9 | Article+FAQPage | ✅ |
| `/no-vig-calculator` | 72 → **48** | 147 | 23 | 7 | FAQPage | ✅ |
| `/tools` | 78 → **51** | 223 → **143** | 14 | 11 | SoftwareApplication+ItemList | ✅ |

---

## Change 1 — internal link equity *(the highest-value fix in this report)*

**Before.** Counting body links only, with nav and footer excluded:

```
/ufc-331-odds             2        /games               24
/football-line-movement   4        /no-vig-calculator   23
/mlb-playoffs             5
```

Ten calculator pages all linked to `/games` and `/no-vig-calculator` and to nothing else. Every bit of internal authority pooled in two pages with low informational search intent, while the three pages carrying `Article` + `FAQPage` schema — the only ones structurally capable of ranking for a question — were the most orphaned on the site.

**After.** A "Read next" block on `/nfl`, `/cfb`, `/games` and `/no-vig-calculator`:

```
/ufc-331-odds             5   (+150%)
/football-line-movement   7   (+75%)
/mlb-playoffs             8   (+60%)
```

**Why it matters.** Internal links are the one ranking input entirely under our control. With no external backlinks, internal structure *is* the site's authority signal, and it was pointed at the wrong pages.

## Change 2 — heading structure on the two seasonal pages

`/cfb` had **zero** `<h2>` elements. `/nfl` had one. On both, "How to read this board" was a `<div class="pick-tag">` — the heading of that section, rendered as a 9.5px mono eyebrow.

Now `<h2 class="pick-tag">` with a one-line margin reset, so it renders identically. **Why it matters:** heading level is semantic and size is presentational; a page targeting "college football odds" with no subheading gives a crawler no structure to read.

**Deliberately not done:** padding `/nfl` (484 words) and `/cfb` (334 words). They are live boards. Adding prose to reach a word count is the thin-content move this brief rules out — the seven articles in `seo-content-map.md` take the informational queries instead.

## Change 3 — schema parity on `/nfl`

`/nfl` was the only priority page carrying `BreadcrumbList` and `ListItem` and nothing else. Added `WebPage` + `Organization` matching `/cfb`. All JSON-LD on every changed page validates.

## Change 4 — titles and descriptions

19 titles and 11 descriptions brought inside Google's cut across M25–M27. Worst offenders: `/mlb-playoff-odds-explained` 96 → 47 chars; `/learn` description 211 → 149. In every case the part removed was the ` | Inside the Number` suffix, which was being truncated away anyway.

Two were stale, not merely long:
- **`/games`** advertised *"across MLB, NFL, CFB, **NBA, NHL**"* — both 404.
- **`/cfb`** described a sort order the page stopped using when it was rebuilt time-ordered.

## Change 5 — signup coverage

`/odds-converter` was the last of 17 priority and tool pages with no email capture — only an outbound hop, the pattern `index.html` retired on Aug 29 2026 after analytics showed people dying on the hop. **All 17 now carry the inline form.**

## Change 6 — indexing hygiene *(M25, in this branch)*

`/parlay` ("Today's parlay: None", dated Sep 14, 0 inbound links) and `/dfs` (title contains "Paused") set to `noindex,follow` and removed from the sitemap. Neither deleted; both still reachable and still passing link signal. Sitemap 28 → **29**, with the three guides added.

---

## Verified

```
29 sitemap entries — all resolve, all canonical to the extensionless URL
 0 noindexed pages in the sitemap
 0 forbidden routes (/nba /nhl /cbb /mlb /positive-ev-calculator)
 0 sitemap pages blocked by robots.txt
 0 titles over 62 chars · 0 descriptions over 155
all JSON-LD parses on every page
robots.txt does NOT block /parlay or /dfs — required, or Google never reads the noindex
```

---

## Owner checklist — Search Console

I cannot submit these. Exact steps, in order, **after the release deploys**:

1. Search Console → Sitemaps → **resubmit `https://insidethenumber.com/sitemap.xml`**. The live file still has 28 entries and omits all three guides.
2. URL Inspection → **Request indexing** for, in this order:
   - `https://insidethenumber.com/ufc-331-odds` *(time-critical — the card is Saturday)*
   - `https://insidethenumber.com/football-line-movement`
   - `https://insidethenumber.com/mlb-playoffs`
3. Record today's baseline: total clicks, impressions, average position.
4. Record per-page impressions for all eight priority routes. Expect several zeros.
5. Coverage report → confirm `/parlay` and `/dfs` move to **"Excluded by 'noindex' tag"**.
6. Confirm no priority route is reported as blocked, excluded or "Discovered – currently not indexed".

**Nothing above has been done.** Steps 1 and 2 are blocked on the deploy.

---

## What this report does not claim

No ranking is promised. The competitive analysis in `PRODUCT-PROOF-REPORT.md` found at least nine free no-vig calculators from stronger domains and five established line-movement products, so **ranking for head terms is not a realistic 90-day outcome.** These fixes make the site technically correct and internally coherent. They do not manufacture authority, and no amount of on-page work will.

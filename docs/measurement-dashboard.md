# Measurement dashboard

**Window:** Thu Sep 17 → Wed Sep 23, 2026. Free tools only: Cloudflare Web Analytics, Google Search Console, Beehiiv.

---

## UTM convention

One format, never varied. Lowercase, no spaces.

```
?utm_source=<channel>&utm_medium=social&utm_campaign=sprint1&utm_content=<day>-<topic>
```

| Channel | `utm_source` |
|---|---|
| X | `x` |
| Reddit | `reddit` |
| Instagram (bio link) | `instagram` |

**The seven tagged links — copy these exactly**

```
Thu  https://insidethenumber.com/no-vig-calculator?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d1-novig
Fri  https://insidethenumber.com/cfb?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d2-nomoneyline
Sat  https://insidethenumber.com/ufc-331-odds?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d3-ufc331
Sun  https://insidethenumber.com/football-line-movement?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d4-keynumbers
Mon  https://insidethenumber.com/break-even-calculator?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d5-breakeven
Tue  https://insidethenumber.com/mlb-playoffs?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d6-series
Wed  https://insidethenumber.com/parlay-calculator?utm_source=x&utm_medium=social&utm_campaign=sprint1&utm_content=d7-parlay
```

Swap `utm_source=x` for `reddit` or `instagram` as needed; change nothing else.

**Two cautions.** Reddit strips or flags tracking parameters in some subs — if a mod objects, post the bare URL and attribute that visit by referrer instead. Instagram allows one bio link: rotate it daily to the day's page, tagged `utm_source=instagram`.

### Landing page per campaign

No new landing pages. **The article is the landing page.** Building seven landing pages for a campaign that has never produced a subscriber would be exactly the polishing this sprint exists to stop. If a day earns traffic and no signups, *then* that page gets a dedicated treatment.

---

## The six fields

| Field | Source | Lag |
|---|---|---|
| Page visits | Cloudflare Web Analytics, per URL, previous 24h | same day |
| Search impressions | Search Console, per page | **2–3 days** |
| Search clicks | Search Console, per page | **2–3 days** |
| Signup form starts | Beehiiv, form views vs submissions | same day |
| Confirmed subscribers | Beehiiv active count (double opt-in) | same day |
| Referring source | Cloudflare top referrers | same day |

**Exclude your own traffic.** Open the site once in every browser you use with `?itn_internal=1`. This has been outstanding across seven audits and it silently corrupts every number below.

---

## Search Console checklist — do once, Thursday

- [ ] Property verified for `insidethenumber.com`
- [ ] **Submit the updated `sitemap.xml`** once the release deploys — the live one has 28 entries and omits all three guides
- [ ] Request indexing: `/football-line-movement`, `/mlb-playoffs`, `/ufc-331-odds`
- [ ] Record today's totals as the baseline: clicks, impressions, average position
- [ ] Record per-page impressions for all eight priority pages (expect several zeros)
- [ ] Coverage report: confirm `/parlay` and `/dfs` move to "Excluded by noindex" after deploy
- [ ] Confirm no priority page is reported as blocked or excluded

## Beehiiv checklist — do once, Thursday

- [ ] Record the baseline: **3 active, 10 all-time, 7 churned, 0 new in 7 days**
- [ ] Confirm double opt-in still on
- [ ] Confirm the confirmation email is arriving (send yourself one)
- [ ] **Change the publication description** — it still reads *"one free pick every morning"* while the homepage says "0 — Picks. Ever."
- [ ] Note which form each signup came from, daily

---

## Daily table

| Date | Page promoted | Source | Visits | Impr. | Clicks | Form starts | Subs | Notes |
|---|---|---|---|---|---|---|---|---|
| Thu 9/17 | `/no-vig-calculator` | x | | | | | | baseline day · sitemap deployed? |
| Fri 9/18 | `/cfb` | x + reddit | | | | | | vs last Friday |
| Sat 9/19 | `/ufc-331-odds` | x + reddit + ig | | | | | | biggest event of the week |
| Sun 9/20 | `/football-line-movement` | x + reddit | | | | | | guide vs board |
| Mon 9/21 | `/break-even-calculator` | x + reddit | | | | | | weekly Search Console read |
| Tue 9/22 | `/mlb-playoffs` | x + reddit | | | | | | Beehiiv delta vs 3 |
| Wed 9/23 | `/parlay-calculator` | x + reddit | | | | | | build the scorecard |

---

## The four-step question this sprint actually answers

The objective is not traffic. It is whether a stranger completes this chain:

```
1. FIND     a useful page          → Search impressions, or a tagged visit
2. CLICK    to a second page       → Cloudflare: >1 page in a session
3. SUBSCRIBE to the Morning Board  → Beehiiv, attributed to a non-homepage page
4. RETURN   for a different sport  → a second visit, different topic
```

Most sites die at step 2. **Step 3 has never once happened from a guide page.**

---

## Thresholds

### Minimum viable — the sprint was worth running

| # | Threshold | Why this number |
|---|---|---|
| 1 | **≥100 total visits** across the seven promoted pages | ~14/day. Below this nothing else is interpretable |
| 2 | **≥1 visit from each of x, reddit, instagram** | Proves each channel can move one human |
| 3 | **≥1 Search Console impression** on `/football-line-movement`, `/mlb-playoffs` or `/ufc-331-odds` | Proves the sitemap fix worked. **Fails automatically if the release is not deployed** |
| 4 | **≥10 sessions viewing 2+ pages** | Step 2 of the chain |
| 5 | **≥1 subscriber from a non-homepage page** | Step 3. Has never happened |

### Success — do it again, bigger

- ≥250 visits · ≥3 subscribers, at least one from a guide · ≥25 impressions on a new guide · one page clearly ahead of the others

### Failure — stop and pivot

**All four true on Wednesday:**
- <50 visits across seven days
- 0 subscribers from any source
- 0 impressions on any new guide **despite the sitemap being live**
- No channel produced more than 2 visits

That is not a page-quality problem. It is a distribution problem, and the pivot is a different channel — not another redesign.

### The ambiguous middle — most likely outcome

Traffic arrives, nobody subscribes. **The diagnosis is step 2 vs step 3:**

| Pattern | Reading | Next |
|---|---|---|
| Visits, but almost all single-page | The page answers the question and ends. Content problem | Strengthen "Read next" on the winning page |
| Multi-page sessions, no signups | They will read but not trade an address. Offer problem | The Morning Board promise, or the cheat sheet, is not worth an email yet |
| One page has most of the traffic | Format works, topic matters | Write two more like it. Stop writing the others |

---

## The scorecard — fill Wednesday 5 PM

| Page | Day | Visits | Impr. | Clicks | 2+ page sessions | Subs | Top referrer | Rank |
|---|---|---|---|---|---|---|---|---|
| `/no-vig-calculator` | Thu | | | | | | | |
| `/cfb` | Fri | | | | | | | |
| `/ufc-331-odds` | Sat | | | | | | | |
| `/football-line-movement` | Sun | | | | | | | |
| `/break-even-calculator` | Mon | | | | | | | |
| `/mlb-playoffs` | Tue | | | | | | | |
| `/parlay-calculator` | Wed | | | | | | | |

**How to act:** top two by visits get promoted again. Bottom two get **left alone, not rewritten** — one week of data on a page nothing linked to until Wednesday is a verdict on its distribution, not on the page.

---

## Three ways these numbers will lie

1. **The release is not deployed.** Threshold 3 fails for a reason unrelated to content, and Thursday/Monday/Wednesday measure nothing. Check this before blaming anything else.
2. **Your own browsing is counted.** Use `?itn_internal=1`. A handful of your own views is a large fraction of this week's traffic.
3. **Saturday distorts the week.** UFC 331 is the only genuine traffic event in the window. Expect `/ufc-331-odds` to win, and do not conclude event pages beat evergreen guides from one data point — the guides will still be earning impressions in December when that card is history.

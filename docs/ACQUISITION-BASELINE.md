# Acquisition baseline — read Thu Sep 17, 2026

**Purpose:** the numbers the 7-day proof sprint is measured against. Everything below is either **[MEASURED]** (pulled from a live source in this session, with the source named) or **[UNAVAILABLE]** (no access — stated plainly, never estimated). Nothing here is inferred.

**Production commit at baseline:** `0eb6995072a62d9a3e5965fa649d2689fd01b494`

---

## 1. Email — Beehiiv [MEASURED]

Pulled from the Beehiiv API at 01:30 UTC, Sep 18, 2026 (publication `pub_bf5cf688`).

| Metric | All time | Last 7 days |
|---|---|---|
| Active subscribers | **3** | 3 (no change) |
| New subscribers | 10 | **0** |
| Churned | 7 | 0 |
| Net | 3 | 0 |
| Open rate | 78.22% | 100.0% |
| Click rate | 1.27% | **0.0%** |
| Earnings | $0.00 | $0.00 |

**Acquisition sources, all time — this is the whole list:**

```
embed: direct / (none)      2
website: direct / (none)    1
```

Three attributed subscribers, both sources "direct", zero from search, social or referral. **Seven of the ten people who ever subscribed have left.** A 78% open rate across three addresses is one person opening an email; it is not a benchmark and will not survive contact with real subscribers.

**Signup form:** one inline form, id `3c7a1727-e42d-4d8c-b16e-d693bf3aff4f`, created Aug 29. It is embedded on every content page (verified below).

**Known contradiction, owner-only to fix:** the Beehiiv publication description still reads *"…and one free pick every morning."* The site says "0 — Picks. Ever." One of the two is lying to a prospective subscriber at the moment of signup. Claude does not modify Beehiiv publication settings.

---

## 2. Site traffic — Cloudflare Web Analytics [UNAVAILABLE]

No Cloudflare API credential is present in this environment (`CF_API_TOKEN`, `CLOUDFLARE_API_TOKEN`, `CF_ZONE_ID` all unset). A read-only token was created in an earlier session but is not reachable from here.

**Therefore: visits, top pages and referrers could not be read, and are not estimated anywhere in this document.**

The beacon *is* installed and firing — verified on all 23 HTML routes (exactly once each), so the data exists in the dashboard; only Claude's access to it is missing.

**What Chuck must connect:** either read the dashboard manually and paste the four numbers into §6 of `7-DAY-ACQUISITION-EXPERIMENT.md`, or expose a read-only Cloudflare Analytics token to the session. The sprint is fully executable without it — it just means Chuck reads traffic instead of Claude.

## 3. Search — Google Search Console [UNAVAILABLE]

No GSC credential in this environment and no MCP connector for it. Impressions, clicks, average position and indexed-page count could not be read and are not estimated.

**What Chuck must connect:** nothing installable for free that Claude can reach. Chuck reads Search Console directly; the daily action list tells him exactly which two numbers to record.

---

## 4. Funnel audit — live, all [MEASURED]

Every route fetched from production at 01:35 UTC, Sep 18.

| Route | HTTP | Title | Desc | Canonical | JSON-LD | Signup |
|---|---|---|---|---|---|---|
| `/` | 200 | 57 | 143 | self | 2, parse | 3 |
| `/games` | 200 | 53 | 139 | self | 2, parse | 2 |
| `/cfb` | 200 | 50 | 139 | self | 2, parse | 2 |
| `/nfl` | 200 | 44 | 149 | self | 2, parse | 2 |
| `/mlb-playoffs` | 200 | 48 | 140 | self | 3, parse | 2 |
| `/ufc-331-odds` | 200 | 58 | 149 | self | 3, parse | 2 |
| `/no-vig-calculator` | 200 | 52 | 147 | self | 2, parse | 2 |
| `/tools` | 200 | 51 | 143 | self | 3, parse | 2 |
| `/football-line-movement` | 200 | 58 | 141 | self | 3, parse | 2 |

**Result: no high-impact funnel defect found.** Every title is inside Google's ~60-character render width, every description inside ~155, every canonical self-referential, every JSON-LD block parses, and every page carries a real signup embed. There were no broken links, no dead ends and no missing metadata to fix.

**Smoke invariants, re-run through the browser** (the repo's `scripts/smoke.py` cannot run from Claude's sandbox — the proxy returns 403 for insidethenumber.com, an environment limit, not a site failure; the same script runs fine in GitHub Actions):

- 25 / 25 routes return 200 — **pass**
- Analytics beacon loads exactly once on all 23 HTML pages — **pass**
- Sitemap: 29 entries — **pass**
- `#potd-date` present — **pass**
- Homepage board stamp is today's date — **FAIL**, serves `Wed, Sep 16`

**That last one is the single real defect on the live site, and it is already fixed** in the validated M29 hotfix (`4c7b51a`), which is built, QA'd and waiting on an owner push. It is not re-fixed here.

---

## 5. What is already measured, and where [MEASURED]

The first-party measurement helper on every page (added Sep 15, Block S3) is better than the baseline numbers suggest. It is cookie-free, sends nothing to third parties, and does three things:

| # | Mechanism | Where it lands |
|---|---|---|
| 1 | **Internal-traffic flag.** `?itn_internal=1` marks the browser as the owner's; `?itn_internal=0` clears it. The Cloudflare beacon is then skipped entirely for that browser | Keeps Chuck's own visits out of every count |
| 2 | **First-touch UTM capture**, kept 30 days, so a signup on a later page still credits how the visitor first arrived | `localStorage.itn_utm` |
| 3 | **Source passthrough into Beehiiv** — the captured UTM is appended to the subscribe iframe `src` and the hosted subscribe link | Beehiiv → subscriber → Acquisition Details |

So **signup completion is already attributable end to end**, for free, with no work needed this sprint. That is the event that matters most and it is live.

### Measurement gaps, stated honestly

| Event | Status | Why |
|---|---|---|
| Signup **completion** + source | ✅ working | Beehiiv acquisition sources, fed by the UTM passthrough |
| Page visits + referrer | ✅ collected | Cloudflare beacon — Chuck can read it, Claude cannot |
| **Signup start** (focus/typing in the form) | ❌ **not measurable for free** | The Beehiiv form is a cross-origin iframe. The parent page cannot observe focus or keystrokes inside it — that is the browser's security model, not a gap in our code. Measuring it needs Beehiiv's own form analytics or a paid events product |
| **Board click** as a distinct event | ⚠️ partially covered | Cloudflare Web Analytics free tier is pageview-only, no custom events. Board clicks that navigate to another ITN route already appear as a pageview of the destination. Clicks that expand a row in place are not counted |

**No tracking code was added this sprint.** Everything feasible for free is already in place, and the two gaps above cannot be closed without a paid product — which this sprint explicitly excludes. Inventing a proxy metric would be worse than recording the gap.

---

## 6. The honest starting line

```
Active subscribers        3
Subscribers from search   0
Subscribers from social   0
Social posts published    0
Revenue                   $0.00
Site traffic              collected, not readable by Claude
Search impressions        unknown — no GSC access
```

Anything this sprint produces is measured against those numbers. They are small enough that a single subscriber from a non-homepage source is a real, legible signal.

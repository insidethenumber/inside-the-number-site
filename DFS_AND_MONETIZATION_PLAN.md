# DFS Section + Affiliate Monetization — Research & Plan

Researched Aug 21, 2026. Two separate initiatives, written up together because
they share a compliance surface.

---

# PART 1 — NFL DFS SECTION

## The structural problem with DFS, stated plainly

A leaked **betting pick** costs almost nothing. The line might move a point;
the pick still stands on its own merit.

A leaked **DFS lineup** is different, because DFS is a *zero-sum contest
against other entrants*. Every person playing your lineup for free is directly
competing against the subscribers who paid for it. Worse, duplicated rosters
cluster — if the lineup hits, the prize pool splits more ways and everyone's
payout shrinks. The product actively degrades in proportion to how much it
leaks. That isn't true of anything else on the site.

Chuck already flagged this instinct. It's correct, and it should shape the
design rather than kill the idea.

## Recommended model: core plays, not full lineups

Publish **the players we're building around and why** — not a locked
9-player roster.

| | Full lineup | Core plays |
|---|---|---|
| Value to subscriber | High | High — arguably higher, they still build |
| Value to leaker | Total | Partial |
| Roster duplication | Severe | Minimal |
| Single-outcome blame risk | Everyone loses together | Spread across builds |
| Teaches the method | No | Yes — fits ITN's whole positioning |

Core plays also fit the brand better. ITN's entire pitch is *"we show the
reasoning, not just the pick."* A bare lineup is the opposite of that.

## Proposed structure

**Free tier (public, drives signups)**
- 2–3 **core plays** for the week's main slate, with reasoning
- One "fade" — a popular chalk play we're avoiding, and why
- Published Thursday or Friday for the Sunday slate

**Paid tier (Member)**
- Full core build: 5–6 players with salary context and ownership read
- Leverage/contrarian plays for GPPs
- Cash-game vs tournament split
- Late-swap notes Sunday morning

**Cadence:** NFL only, once weekly. Confirmed as the right call — one build
per week, fixed slate, fits the existing weekend routine. Daily MLB DFS would
multiply operational load for a fraction of the audience.

## The obligation this creates

ITN's identity is *every result logged*. Adding DFS creates a duty to grade
DFS too — finish position, cash rate, ROI on the core plays. Publishing DFS
picks without grading them would directly undercut the thing the rest of the
site is built on.

**Do not launch this unless we're committed to grading it as rigorously as
the betting picks.** That means a DFS section on record.html, its own results
table, and a line in the weekly routine.

## Build checklist (when we're ready)

- [ ] `dfs.html` page, or a section on the homepage during NFL season
- [ ] Player data source — check whether ESPN's feed carries DFS salaries
      (it likely does not; may need a separate source)
- [ ] DFS results table on record.html, separate from betting picks so the
      two records never get conflated
- [ ] Weekly scheduled task (Thu or Fri) mirroring the daily routine
- [ ] Free/paid gating — currently no paywall mechanism exists at all
- [ ] Ownership projections are the hard part; may not be feasible free

**Timing:** NFL season is close. Better to build it properly in the next few
weeks than rush a half-version.

---

# PART 2 — AFFILIATE MONETIZATION

## How it actually works

Sportsbooks pay affiliates for referred depositing customers, via:

- **CPA** — flat fee per qualified new depositor (commonly $50–$500 depending
  on state and operator)
- **Revenue share** — percentage of the book's net revenue from that customer,
  often ongoing
- **Hybrid** — smaller CPA plus a smaller rev-share

FanDuel pays monthly with a **$50 minimum** threshold. DraftKings reviews
applications in "a few days" and offers CPA and hybrid deals. Both restrict
promotion to **regulated US states where they hold licenses**.

## The blunt reality check

Both DraftKings and FanDuel screen applicants on **traffic quality standards**
and want to know about your audience. With 2 newsletter subscribers and a site
that's days old, an application today would very likely be declined — and a
declined application is worth avoiding, since re-applying later from a
stronger position is easier than reversing a rejection.

**Traffic has to come first.** This is a "build the audience, then monetize"
sequence, not the reverse. Realistic path:

1. Grow to consistent organic traffic (SEO via the tools + record pages)
2. Grow the newsletter list
3. Apply to one or two programs with real numbers to show
4. Add links only where they genuinely serve the reader

## ⚠️ Bovada — do not do this

Chuck listed Bovada alongside DraftKings and ESPN Bet. They are not the same
category and this distinction matters a lot.

**Bovada is an offshore operator, not licensed by any US state regulator.**
Several state regulators treat it as operating illegally in their
jurisdictions.

Two concrete consequences:

1. **Legal exposure.** Promoting an unlicensed operator to US residents is a
   materially different risk profile from promoting a state-licensed book.
2. **It poisons the legitimate path.** Licensed operators' affiliate
   agreements commonly prohibit affiliates from *also* promoting unregulated
   or black-market sites. Linking to Bovada can disqualify ITN from
   DraftKings, FanDuel, BetMGM and Caesars — the programs actually worth
   having.

Recommendation: **licensed US operators only.** DraftKings, FanDuel, BetMGM,
Caesars, ESPN Bet, bet365, Fanatics. Leave the offshore books alone entirely.

## State licensing — affiliates often need their own registration

This surprises people. In several states the *affiliate* must be licensed or
registered, not just the sportsbook:

| State | Affiliate requirement | Fee |
|---|---|---|
| Washington DC | License required | ~$10,000 |
| Illinois | License required | ~$10,000 |
| Pennsylvania | License required | ~$2,000–2,500 |
| New Jersey | License required | ~$2,000–2,500 |
| Arizona | License required | $1,500 initial / $500 renewal |
| Indiana | License + letter of intent from an operator | ~$500 |
| Colorado | License required (two types) | Varies |

**Tennessee — good news.** Chuck is Nashville-based, and Tennessee does **not**
require CPA affiliates to be licensed. TN's vendor registration (the $150,000
one) applies to payment processors, odds providers and platform developers —
not affiliate marketers. So operating from TN, on a CPA basis, is the clean
starting point.

*This is a summary of research, not legal advice. Before taking affiliate
revenue, confirm current requirements with a gaming attorney — these rules
change often and vary by deal structure.*

## Compliance the site must carry before any affiliate link goes live

Non-negotiable, and mostly missing today:

- [ ] **FTC affiliate disclosure** — clear statement that we earn commission
      on referrals. FTC Endorsement Guides are actively enforced.
- [ ] **21+ age statement** on any page carrying betting links
- [ ] **Responsible gambling messaging** + **1-800-GAMBLER**
- [ ] **State availability** — links must only surface where that book is
      licensed, or carry clear "where legal" language
- [ ] **Privacy policy** and **terms of use** pages — the site has neither
- [ ] Existing footer disclaimer is a good start but not sufficient on its own

## What good looks like on competitor sites

- Covers and Action Network run a **"Top-Rated Sportsbooks"** module: book
  logo, star rating, headline offer, promo code, "Claim" CTA, and a dense
  block of state-by-state terms and helpline numbers underneath.
- Vegas Insider runs a persistent sidebar of **"Best Betting Sites"** promo
  code links.
- Every one of them carries the 1-800-GAMBLER line and state restrictions
  directly adjacent to the offer.

The pattern is consistent: the offer is prominent, the compliance text is
immediately beneath it, never buried.

## Suggested sequencing

1. **Now:** add privacy policy, terms, and a responsible-gambling page.
   Needed regardless of affiliates, and they're table stakes for looking
   legitimate.
2. **Now:** keep building traffic — tools and record pages are the SEO assets.
3. **Later, at real traffic:** apply to one licensed operator, TN-based, CPA.
4. **Then:** build a sportsbook module modeled on Covers, compliance-first.
5. **Never:** offshore books.

## An honest note on fit

Affiliate revenue creates a structural tension worth naming up front. ITN's
value proposition is *independent, documented analysis*. Affiliate income means
getting paid when readers deposit at a sportsbook. Those incentives are not
perfectly aligned, and readers notice.

The sites that handle this well keep the two clearly separated — the analysis
never bends toward the sponsor, and the commercial relationship is disclosed
plainly. Worth deciding early how firmly to hold that line, because it's much
harder to walk back later.

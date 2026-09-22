# Inside the Number: Acquisition Diagnosis

Date: 2026-09-22

## What the live data says

Cloudflare RUM, filtered to non-bot traffic for the last seven days, recorded 351 page loads. That is not an audience: 249 were internal navigation after a page had already loaded, and 97 new arrivals had no referrer. Those direct/unknown arrivals include owner browsing and cannot be treated as acquired visitors.

Only five arrivals identify a distribution source:

| Source | Arrivals | Landing page |
| --- | ---: | --- |
| X (`t.co`) | 3 | `/` |
| Facebook mobile | 2 | `/` |
| Google / Reddit / newsletter referral | 0 traceable | none |

The previous seven days had ten traceable X arrivals and no other named referral source. This is not a conversion-rate diagnosis. There is not enough qualified traffic at the signup form to judge conversion.

Search is indexed, not absent. The most recent Search Console baseline recorded 170 impressions, zero clicks, and average position 60.6. The only query families with signal were `no vig calculator`, `kelly criterion calculator`, and `kelly calculator`. Search snippets were stale and promoted expired event content; that was corrected in commits `752b7ac` and `fc7095e`.

## Why traffic is not funneling

1. There is no repeatable acquisition channel. Five named referrals in a week cannot create subscribers.
2. Search visibility is on page six or later, where impressions do not turn into visits. Metadata was not the only problem; the domain has no authority or relevant external links yet.
3. Previous distribution concentrated on timely sports graphics. Those can earn impressions, but they expire and mostly send people to the generic homepage instead of a utility page with a matching intent.
4. The business has not yet tested a credible referral channel: relevant newsletter recommendations, one-to-one newsletter swaps, calculator/resource listings, or useful community answers.
5. Paid ads are not the shortcut. Sports betting advertising is restricted, and the site has not proved a visitor-to-subscriber conversion rate. Buying traffic before that would only buy an expensive ambiguity.

## 14-day acquisition experiment

The objective is not followers. It is 25 attributable visits to a useful page and one confirmed, non-direct subscriber.

### Track A: Google discovery

- Submit `https://insidethenumber.com/sitemap.xml` in Search Console.
- Request indexing only for `/no-vig-calculator`, `/kelly-calculator`, `/football-line-movement`, `/mlb-playoffs`, and `/`.
- Track impressions and clicks weekly, not daily. The first decision comes after 14 days.
- Next build: one automatically generated, crawlable weekly NFL/CFB hub. Do not recreate per-game pages; the prior approach produced thin, orphaned URLs.

### Track B: utility-led referrals

- Offer the No-Vig Calculator and Kelly Calculator to relevant betting-math/resource directories and small analytics newsletters. The pitch is the free tool, not a generic request for promotion.
- Set up reciprocal Beehiiv recommendations with adjacent, non-picks newsletters. Free Recommendations are available on the current plan; do not buy boosts yet.
- Each outreach URL uses: `?utm_source=partner&utm_medium=referral&utm_campaign=utility_launch&utm_content=<partner-name>`.

### Track C: community distribution

- Publish three useful, rules-compliant answers each week in relevant betting/math communities. Link only when a calculator directly answers the question. No game picks, no generic "visit my site" posts, no link dumping.
- Use one specific URL per answer, for example: `https://insidethenumber.com/no-vig-calculator?utm_source=reddit&utm_medium=community&utm_campaign=utility_launch&utm_content=novig_answer`.
- Success is a referred visit first, not upvotes.

### Track D: social, but not social volume

- One sports post should point to one matching page: a line-movement visual goes to `/football-line-movement`; a probability visual goes to `/no-vig-calculator`; a bankroll question goes to `/kelly-calculator`.
- Do not send every post to the homepage. Use the existing UTM handoff on all public pages so Beehiiv preserves the source after a visitor subscribes.
- Pause Instagram as an acquisition priority until a Reel produces a tracked site visit. It may still be useful for brand proof, but it is not a traffic engine until the numbers say otherwise.

## Decision rules

- If a channel produces 10+ attributable visits but zero signup-form starts, improve the page/offer before adding volume.
- If a page gets search impressions but no clicks, improve its search title and snippet based on the actual query.
- If 14 days produce fewer than 25 attributable visits and no non-direct subscriber, stop expanding the content calendar and reassess the product wedge before spending on ads.

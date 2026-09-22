# Inside the Number: Slate and SEO Audit

Date: 2026-09-22

## Live product check

- College football: 71 contests in the seven-day board. The board filters render for All Games, Top 25, Power 4, and Featured Games. Cards show moneyline, spread, total, no-vig probability, and a full-analysis path.
- MLB: 16 games on today's board with moneyline, run line, total, probable pitchers, and no-vig probabilities.
- NFL: all 16 Week 3 games render with moneyline, spread, total, no-vig probabilities, and full analysis.
- UFC: the Sep. 26 Rosas Jr. vs. Barcelos Fight Night card renders with 12 bouts. The page correctly labels that ESPN supplies no UFC prices, rather than inventing odds.
- Production smoke test: 20 of 20 monitored pages returned HTTP 200; analytics beacon loaded once on 18 measured pages.

## Search evidence

The September 7 Search Console report recorded 170 impressions, zero clicks, and an average position of 60.6 over seven days. The only meaningful early query signals were calculator intent: "no vig calculator" (20 impressions), "kelly criterion calculator" (16), and "kelly calculator" (11).

Google currently has the domain indexed, but its public snippets were stale and still surfaced expired UFC 331 / Morning Board language. The old sitemap also promoted expired UFC, PGA, and UFC 331 pages while the current live sports boards were elsewhere.

## Changes deployed today

Commit `752b7ac`:

- Retired expired UFC/PGA event pages from the sitemap and marked them `noindex,follow`.
- Marked the obsolete, dated "Parlay of the Day" page `noindex,follow`; the evergreen parlay calculator remains indexable.
- Redirected active site CTAs from expired UFC 331 content to the live UFC board.
- Updated changed sitemap dates so crawlers can prioritize the current discovery layer.
- Reframed the Kelly calculator title and description around the full, half, and quarter Kelly outputs that the tool visibly provides and the queries already indicate.

## Remaining constraint

The interactive game board is client-rendered. It is excellent for people who arrive, but Google initially sees its loading shell rather than a full weekly slate. Do not create dozens of thin game pages. The next technical SEO build should be one generated, crawlable weekly NFL/CFB hub with verified current matchups, a visible timestamp, and links into the live board.

## Priority order

1. In Search Console, submit the sitemap and request indexing only for `/`, `/no-vig-calculator`, `/kelly-calculator`, `/football-line-movement`, and `/mlb-playoffs`.
2. Build the one crawlable weekly NFL/CFB hub described above, generated from the existing source feed so it cannot go stale by hand.
3. Measure search impressions, clicks, and signup conversion weekly. Do not buy ads until analytics identify a page and message that convert.

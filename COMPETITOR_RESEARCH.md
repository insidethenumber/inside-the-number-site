# Competitive Benchmark — the five sites in our business

Researched Aug 22, 2026. Internal doc, not served publicly.

The question this answers: what do the best sites in this category actually
ship, where does ITN already match them, and what would it take to be as good.

---

## The five

**1. Action Network** — the category leader
Owned by Better Collective, who paid **$240M** for it in 2021. Commercial data
partnerships with BetMGM, DraftKings, FanDuel and PointsBet, which is where its
betting-percentage data comes from — not a public feed.
Pricing: **$19.99/mo, $99.99/yr**. (We launched at $17.99/mo as a founding
rate, $2 under Action's price, with $149/yr — roughly half their annual rate.
Note added Aug 31 2026: this doc originally read "the same monthly price
we're proposing" when the plan was still $19.99; changed after Chuck's call
to undercut instead.)
Ships: public betting % **split into bets vs money** (the valuable version),
odds from real books, projections on moneyline/spread/total, PRO Report signals,
bet tracking via BetSync, QuickSlip bet placement, custom betting systems.

**2. Dimers** — the model-first play
Pricing: **$29.99/mo, $199.99/yr**.
Ships: Monte Carlo simulations per game, **22,000+ games a year**, Best Bets,
Best Props, "Dimebot" AI assistant, iOS and Android apps. Breadth is the whole
product — every game in every league, every day.

**3. SportsLine (CBS)** — distribution as the moat
Proprietary model, **10,000 simulations per game**, across MLB, NFL and PGA.
The model is ordinary; being embedded in CBS Sports is not. Traffic comes free.

**4. Wunderdog** — the closest analogue to what we're building
**410,000+ subscribers.** Gives computer picks away free — predicted score and
win probability on every game, across eight sports — plus free public consensus.
Sells human handicapping with a money-back guarantee. Publishes **85,000+ picks
with wins and losses**, searchable, as its central trust claim.
Their own page says it plainly: computer picks are the starting point, finding
real edges takes a human. Worth internalising — the model is the lead magnet,
not the product.

**5. Pickswise** — the free/affiliate model
**No paid tier at all.** Every pick, every sport, plus parlays, entirely free.
Monetised through sportsbook affiliate commissions. Proof that the whole picks
product can be a traffic funnel rather than a subscription business.

**Adjacent, and increasingly the real competition:** OddsJam (+EV line
shopping), Oddspedia (line movement context), ProfitDuel (odds screener feeding
calculators), Oddschecker (best free comparison). These matter because the
clearest edge we found by hand tonight — a UFC main event priced −185 at one
book and −222 at another — is *their* core feature, not ours.

---

## Where ITN stands

| | ITN today | Best in class |
|---|---|---|
| Free board, every game | **yes** | Pickswise, Wunderdog |
| True price per market, shown plainly | **yes** | rare — genuine differentiator |
| Predicted score model | **MLB only** | Wunderdog (8 sports), Dimers, SportsLine |
| All three markets graded per game | **yes** | Dimers |
| Line movement | single book | Oddspedia, Action |
| Multi-book / best available price | **no** | OddsJam, ProfitDuel, Action |
| Public betting % (bets vs money) | **no** | Action, Wunderdog |
| Player props | **no** | Dimers, Action |
| Bet tracker | **no** | Action (BetSync) |
| Mobile app | **no** | all four paid competitors |
| Betting calculators | **10, all verified correct** | ProfitDuel, SportyTrader |
| Documented pick record | **retired** | Wunderdog (85k, searchable) |
| Daily newsletter | **yes** | Wunderdog (410k subscribers) |
| UFC / PGA depth | partial | almost nobody does this well |

---

## Honest read

**Three things we already do as well as anyone.** The true price on every
market, stated plainly rather than buried. Reasoning attached to every call.
Ten calculators that are actually correct — all ten were verified against
hand-computed values on Aug 22.

**Three real gaps, in order of leverage.**

1. **Multi-book odds — $99/mo, The Odds API.** The highest-return spend
   available. It gets Pinnacle (which sharpens every true price we compute),
   enables a best-available-price feature on every game, and that feature
   points straight at affiliate links. Improves the product and earns at the
   same time. Nothing else on this list has that profile.
2. **Model breadth.** Wunderdog runs computer picks in eight sports; we run one.
   The Poisson approach doesn't transfer to football or basketball — those need
   a margin-distribution model — so this is real work, not a config change.
3. **Audience.** Wunderdog has 410,000 subscribers. Action Network had $240M
   spent on it. We have a six-issue newsletter. This is the actual gap, and no
   feature closes it.

**One strategic conclusion.** Every serious competitor treats model output as
free. Action, Wunderdog and Pickswise all give picks or projections away and
monetise elsewhere — subscriptions on top, affiliate underneath, or both. If
ITN Pro is sold on projections alone it is selling the thing the category gives
away. The defensible paid product is the hand-written work: the staked daily
picks, UFC card-by-card, the PGA Tuesday preview and post-cut re-price. Those
are the things a model can't produce and the big sites mostly don't bother with.

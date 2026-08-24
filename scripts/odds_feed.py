#!/usr/bin/env python3
"""
Inside the Number — multi-book odds feed.

ESPN carries one price, from one book, and carries nothing at all for MMA or
golf outrights. This pulls from The Odds API, which normalizes ~50 books
(BetMGM, DraftKings, FanDuel, Caesars and others) behind one endpoint.

Why an aggregator and not the books directly: BetMGM and DraftKings publish no
public API, and pulling from their internal endpoints means scraping against
their terms. Action Network's terms — read during this project — enumerate
betting data as protected content and prohibit scraping outright. An
aggregator licenses the data properly, so nothing here can get the site pulled.

Two things this unlocks that ESPN cannot do at all:

  1. MMA prices. ESPN has none. The Odds API includes MMA on every plan
     INCLUDING the free tier, so Saturday's UFC card costs nothing to cover.
  2. Best price across books. With one book you report a number. With fifty
     you can say "DraftKings has this at -118 and BetMGM at -105", which is
     real money to a reader and something no free site publishes well.

Credits, not requests: one call costs roughly (regions x markets) credits.
Query one region and one market and it is 1 credit. The free tier's 500/month
is plenty for a UFC card; daily multi-sport coverage wants the $29 plan.

    export ODDS_API_KEY=...          # or put it in itn-secrets.env
    python3 scripts/odds_feed.py --sport mma_mixed_martial_arts
    python3 scripts/odds_feed.py --list
"""

import argparse, json, os, sys, urllib.parse, urllib.request, urllib.error

BASE = "https://api.the-odds-api.com/v4"
SECRETS = os.environ.get(
    "ITN_SECRETS", os.path.expanduser("~/Documents/Claude/Projects/itn-secrets.env"))


def api_key():
    """Env var wins; otherwise read the same secrets file the X poster uses."""
    k = os.environ.get("ODDS_API_KEY")
    if k:
        return k
    if os.path.exists(SECRETS):
        for line in open(SECRETS):
            if line.strip().startswith("ODDS_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("ERROR: no ODDS_API_KEY. Add it to itn-secrets.env as:\n"
             "  ODDS_API_KEY=your_key_here")


def call(path, **params):
    params["apiKey"] = api_key()
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            data = json.loads(r.read().decode())
            # These headers are the whole budget story — always surface them.
            used = r.headers.get("x-requests-used")
            left = r.headers.get("x-requests-remaining")
            if left is not None:
                print(f"  [credits used {used}, remaining {left}]", file=sys.stderr)
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        if e.code == 401:
            sys.exit("ERROR: key rejected (401). Check ODDS_API_KEY.")
        if e.code == 422:
            sys.exit(f"ERROR: bad request (422) — sport key or market wrong.\n{body}")
        if e.code == 429:
            sys.exit("ERROR: out of credits (429). Free tier is 500/month.")
        sys.exit(f"ERROR: HTTP {e.code}\n{body}")


def implied(american):
    v = float(american)
    return 100.0 / (v + 100.0) if v > 0 else abs(v) / (abs(v) + 100.0)


def best_prices(event, market="h2h"):
    """
    Best available price per outcome across every book, plus the no-vig line
    computed from the best of each side.

    Shopping the best number on both sides is the single highest-return habit
    in betting and it is invisible if you only ever look at one book.
    """
    best = {}
    for bk in event.get("bookmakers", []):
        for mk in bk.get("markets", []):
            if mk.get("key") != market:
                continue
            for oc in mk.get("outcomes", []):
                name, price = oc.get("name"), oc.get("price")
                if price is None:
                    continue
                cur = best.get(name)
                if cur is None or price > cur["price"]:
                    best[name] = {"price": price, "book": bk.get("title")}
    if len(best) == 2:
        (a, ad), (b, bd) = best.items()
        ia, ib = implied(ad["price"]), implied(bd["price"])
        tot = ia + ib
        if tot > 0:
            ad["true"] = round(ia / tot * 100, 1)
            bd["true"] = round(ib / tot * 100, 1)
            # Below 100% across the best of both sides means the books
            # disagree enough that no margin survives shopping.
            for d in (ad, bd):
                d["field_total"] = round(tot * 100, 1)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sport", default="mma_mixed_martial_arts")
    ap.add_argument("--markets", default="h2h")
    ap.add_argument("--regions", default="us")
    ap.add_argument("--list", action="store_true", help="list available sports and exit")
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.list:
        for s in call("/sports"):
            if s.get("active"):
                print(f"  {s['key']:<38} {s['title']}")
        return

    events = call(f"/sports/{a.sport}/odds",
                  regions=a.regions, markets=a.markets, oddsFormat="american")
    if not events:
        print(f"No priced events for {a.sport} right now.")
        return

    print(f"\n{len(events)} event(s) — {a.sport}\n")
    for ev in events:
        print(f"{ev.get('away_team')} vs {ev.get('home_team')}   {ev.get('commence_time')}")
        best = best_prices(ev, a.markets.split(",")[0])
        for name, d in best.items():
            true = f"  true {d['true']}%" if "true" in d else ""
            print(f"   {name:<26} {d['price']:>+5}  (best: {d['book']}){true}")
        if best:
            ft = next((d.get("field_total") for d in best.values() if d.get("field_total")), None)
            if ft:
                keep = ft - 100
                print(f"   {'':<26} shopping the best of both sides leaves "
                      f"{keep:+.1f}% to the house")
        print(f"   books quoted: {len(ev.get('bookmakers', []))}\n")

    if a.out:
        json.dump(events, open(a.out, "w"), indent=1)
        print(f"wrote {a.out}")


if __name__ == "__main__":
    main()

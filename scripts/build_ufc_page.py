#!/usr/bin/env python3
"""
Inside the Number — UFC card page generator.

Produces ufc.html: a STATIC page with every fight on the upcoming card, the
best available price on each corner across ~50 books, each fighter's win
chance in plain English, their record and weight class from ESPN, and a
human-written note on the fights people actually care about.

Two data sources, merged by name:
  The Odds API  — prices (ESPN carries zero MMA odds; this is the scarce part)
  ESPN          — records and weight classes (free, no odds, but good bios)

Language rules, learned the hard way on Aug 24 (Chuck: "no one knows what
house edge and true are"): no "hold", no "house edge", no "true probability"
on the page. Odds, win chance, and sentences a person would say. The math
underneath is unchanged — only the words changed.

Hand-written fight notes live in NOTES below. They are editorial and survive
regeneration untouched; everything else is derived from the data so a refresh
cannot invent opinions. Notes must only contain facts that do not go stale
(who a fighter is, how they fight) — records and prices stay machine-side.

Runs in GitHub Actions (the local sandbox cannot reach either API).
One Odds API credit per run.

    python3 scripts/build_ufc_page.py --start 2026-08-29 --end 2026-08-30 \
        --title "UFC Fight Night Shanghai" --venue "Shanghai, China"
"""

import argparse, html, json, os, re, sys, unicodedata, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "https://api.the-odds-api.com/v4"
# ESPN answers curl and refuses urllib's default UA — see build_slate.py.
UA = {"User-Agent": "curl/8.5.0", "Accept": "*/*"}

# ── hand-written fight notes ───────────────────────────────────────────────
# Keyed by frozenset of the two LAST names, lowercased. Time-safe facts only:
# who a fighter is and how they fight. No records, no prices — those are
# derived fresh each run and would go stale here.
NOTES = {
    frozenset({"yadong", "nurmagomedov"}):
        "Umar is the latest product of the famous Dagestani wrestling pipeline — "
        "Khabib's cousin — and fights like it: forward pressure, chain wrestling, "
        "nothing wasted. Song Yadong is the kind of one-punch bantamweight who can "
        "end a round he's losing. The whole fight is one question: does it stay "
        "standing long enough for that power to matter? The books say almost "
        "certainly not.",
    frozenset({"xiaonan", "gomes"}):
        "Yan Xiaonan has shared the cage with the very best at strawweight — she's "
        "challenged for the title — and this card is built around Chinese stars, so "
        "the moment won't rattle her. Denise Gomes is younger and walks forward for "
        "fifteen minutes straight. The books making the veteran only a modest "
        "favorite tells you how much they respect that pace.",
    frozenset({"asakura", "qileng"}):
        "Kai Asakura came over from Japan's RIZIN as a genuine star and has already "
        "fought for a UFC flyweight title. Aori Qileng is durable and will happily "
        "make it ugly, but the books see a class gap here — and it's hard to argue.",
    frozenset({"perez", "mudaerji"}):
        "Alex Perez has fought for a UFC flyweight title, and that experience is "
        "most of the case for him. Su Mudaerji is the faster, flashier striker with "
        "the home crowd behind him — the books lean his way and the atmosphere will "
        "too.",
    # ── Noche UFC: Silva vs. Delgado, Sept 12 2026 ──
    frozenset({"silva", "delgado"}):
        "Jean Silva arrived with the Fighting Nerds camp and fights like the room "
        "he trains in — creative, violent, and completely unbothered. Jose Miguel "
        "Delgado is the Mexican prospect this card was built to showcase, a "
        "featherweight who hunts finishes. Noche UFC is the Mexican Independence "
        "Day card, and the main event is the story of the night in one fight.",
    frozenset({"moreno", "morales"}):
        "Brandon Moreno was the first Mexican-born champion in UFC history, and on "
        "this card that matters as much as the matchup. Joseph Morales is unbeaten "
        "in the UFC's eyes for years off injury layoffs and rebuilds. A former "
        "champ against a flyweight trying to restart — experience against hunger.",
    frozenset({"grasso", "fiorot"}):
        "Quietly the best fight on the card. Alexa Grasso has held the women's "
        "flyweight title; Manon Fiorot has been the division's most consistent "
        "contender for years. Neither is in a title fight here, which tells you "
        "how deep this division runs — and this one could decide who challenges "
        "next.",
    frozenset({"blaydes", "acosta"}):
        "Curtis Blaydes is the most decorated heavyweight name on the card, a "
        "wrestler who has been one win from a title shot more than once. Waldo "
        "Cortes Acosta hits like a heavyweight and has been busy while Blaydes "
        "sat. Classic heavyweight question: timing and takedowns, or the punch?",
}


def api_key():
    k = os.environ.get("ODDS_API_KEY")
    if k:
        return k
    p = os.path.join(ROOT, "itn-secrets.env")
    if os.path.exists(p):
        for line in open(p):
            if line.strip().startswith("ODDS_API_KEY="):
                v = line.split("=", 1)[1].strip()
                if v:
                    return v
    sys.exit("ERROR: no ODDS_API_KEY")


def implied(american):
    v = float(american)
    return 100.0 / (v + 100.0) if v > 0 else abs(v) / (abs(v) + 100.0)


def fetch_odds(start, end):
    q = urllib.parse.urlencode({
        "apiKey": api_key(), "regions": "us", "markets": "h2h",
        "oddsFormat": "american",
        "commenceTimeFrom": start + "T00:00:00Z",
        "commenceTimeTo": end + "T00:00:00Z",
    })
    url = f"{BASE}/sports/mma_mixed_martial_arts/odds?{q}"
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            print(f"odds credits remaining: {r.headers.get('x-requests-remaining')}",
                  file=sys.stderr)
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: odds HTTP {e.code} {e.read().decode()[:200]}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: cannot reach the Odds API ({e.reason}). Run in CI.")


def date_range(start, end):
    """YYYYMMDD strings from start to end inclusive.

    ESPN's scoreboard is queried per-date. The old code only ever asked for
    --start, so a card that begins late UTC (every US evening card) had its
    bouts sitting on the NEXT ESPN date and came back empty.
    """
    d0 = datetime.strptime(start, "%Y-%m-%d").date()
    d1 = datetime.strptime(end, "%Y-%m-%d").date()
    out, d = [], d0
    while d <= d1:
        out.append(d.strftime("%Y%m%d"))
        d += timedelta(days=1)
    return out


def fetch_espn(ymds):
    """The card roster: records, weight classes, bout format and card status.

    Returns (bouts, cards). Each bout carries `periods` — 5 for the main
    event, 3 for everything else — which is how the main event is identified.
    Each card carries ESPN's status so we can refuse to publish a finished one.

    Best-effort for the bio fields, but the roster itself is now load-bearing:
    priced fights that do not appear here are discarded (see on-card filter).
    """
    bouts, cards = [], []
    for ymd in ymds:
        url = ("https://site.api.espn.com/apis/site/v2/sports/mma/ufc/scoreboard"
               f"?dates={ymd}")
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=UA), timeout=25) as r:
                data = json.loads(r.read().decode())
        except Exception as e:
            print(f"WARN: ESPN unavailable for {ymd} ({e})", file=sys.stderr)
            continue
        for ev in data.get("events", []):
            status = (((ev.get("status") or {}).get("type") or {})
                      .get("name") or "")
            cards.append({"name": ev.get("name") or "",
                          "date": ev.get("date") or "",
                          "status": status})
            for c_ in ev.get("competitions", []):
                names, recs = [], []
                for comp in c_.get("competitors", []):
                    a = comp.get("athlete") or {}
                    names.append(a.get("displayName") or a.get("shortName") or "")
                    rec = ""
                    for rblock in (comp.get("records") or []):
                        if rblock.get("summary"):
                            rec = rblock["summary"]
                            break
                    recs.append(rec)
                weight = ((c_.get("type") or {}).get("text")
                          or (c_.get("type") or {}).get("abbreviation") or "")
                weight = re.sub(r"\s*-?\s*(Main|Co-Main).*$", "", weight).strip()
                periods = (((c_.get("format") or {}).get("regulation") or {})
                           .get("periods"))
                if len(names) == 2:
                    bouts.append({"names": names, "recs": recs,
                                  "weight": weight, "periods": periods,
                                  "card": ev.get("name") or "",
                                  "status": status,
                                  # ESPN dates each bout with the START of its
                                  # card segment (prelims / main card). That is
                                  # the only trustworthy time we have; the odds
                                  # feed's commence_time was wrong by hours on
                                  # Noche UFC (Sep 5, 2026 — Chuck caught it).
                                  "date": c_.get("date") or ev.get("date") or ""})
    print(f"ESPN: {len(bouts)} bouts across {len(cards)} card(s)", file=sys.stderr)
    return bouts, cards


def fold(n):
    """Lowercase and strip accents: 'Edgar Chairez' -> 'edgar chairez'.

    Sep 5 2026: ESPN spells the Noche UFC flyweight 'Edgar Chairez' and the
    odds feed spells him 'Edgar Chairez' with acutes. Without folding, the
    accented letters were being replaced by spaces, which shredded the name
    into 'dgar ch irez' and the two feeds stopped agreeing that he was one
    person -- so a priced bout was thrown off the card.
    """
    d = unicodedata.normalize("NFKD", n or "")
    return "".join(c for c in d if not unicodedata.combining(c)).lower()


def last(n):
    return re.sub(r"[^a-z]", "", fold(n).split()[-1]) if n else ""


def toks(n):
    """Every word of a name, lowercased, folded and stripped of punctuation."""
    return frozenset(re.sub(r"[^a-z ]", " ", fold(n)).split())


def squash(n):
    """A name with every space and mark removed: 'Su Mudaerji' -> 'sumudaerji'."""
    return re.sub(r"[^a-z]", "", fold(n))


def squash_sorted(n):
    """Space-stripped name with its words alphabetised.

    Handles spacing and word order at once: ESPN 'Rongzhu' and the odds feed's
    'Zhu Rong' both reduce to 'rongzhu'. squash() alone could not, because it
    preserved order.
    """
    return "".join(sorted(toks(n)))


def same_person(x, y):
    """Is this the same fighter, spelled two ways by two feeds?

    Three real disagreements observed on the Shanghai card alone:
      order      ESPN "Ding Meng"    vs odds "Meng Ding"
      suffix     ESPN "Levi Rodrigues Jr." vs odds "Levi Rodrigues"
      spacing    ESPN "Sumudaerji"   vs odds "Su Mudaerji"
    A shared word handles the first two; comparing the space-stripped form
    handles the third.
    """
    if toks(x) & toks(y):
        return True
    sx, sy = squash(x), squash(y)
    if sx and sx == sy:
        return True
    ax, ay = squash_sorted(x), squash_sorted(y)
    return bool(ax) and ax == ay


# Divisions as we want them rendered. ESPN is inconsistent about case —
# it returned "flyweight" on some bouts and "Flyweight" on others in the
# same payload, which showed up on the live page as mismatched cards.
_DIVISIONS = ("Strawweight", "Flyweight", "Bantamweight", "Featherweight",
              "Lightweight", "Welterweight", "Middleweight", "Light Heavyweight",
              "Heavyweight", "Catchweight")


def tidy_weight(w):
    """Normalise ESPN's division string. It arrives as type.abbreviation and
    is inconsistently cased; women's bouts come through as "W Strawweight"."""
    if not w:
        return ""
    low = w.lower()
    womens = low.startswith("w ") or "women" in low
    for d in _DIVISIONS:
        if d.lower() in low:
            return ("Women's " + d) if womens else d
    return w.strip()


def enrich(fight, bouts):
    """Attach record + weight class where ESPN has this bout.

    Matching used to compare last names only. That silently failed on every
    Chinese and Mongolian fighter on the Shanghai card — Su Mudaerji, Aori
    Qileng, Meng Ding, Long Xiao, Liu Ce — because the two feeds disagree on
    which token is the family name, so "Ding Meng" and "Meng Ding" looked
    like different people. Five of thirteen fights shipped with no records
    and no weight class as a result.

    Now we compare whole-name token sets in both orders. A corner matches if
    it shares any word with an ESPN corner, which is plenty to identify one
    person inside a single card. If two bouts both match we take neither —
    a wrong record is worse than a missing one.

    Returns the matched ESPN bout (or None). The caller uses that both to read
    the bout format and to decide whether the fight belongs on this card at all.
    """
    na, nb = fight["a"]["name"], fight["b"]["name"]
    hits = []
    for b in bouts:
        e0, e1 = b["names"][0], b["names"][1]
        if same_person(na, e0) and same_person(nb, e1):
            hits.append((b, False))
        elif same_person(na, e1) and same_person(nb, e0):
            hits.append((b, True))

    if len(hits) == 1:
        b, swapped = hits[0]
        fight["weight"] = tidy_weight(b["weight"])
        order = ("b", "a") if swapped else ("a", "b")
        for idx, side in enumerate(order):
            fight[side]["record"] = b["recs"][idx] if idx < len(b["recs"]) else ""
        return b

    if len(hits) > 1:
        print(f"WARN: {fight['a']['name']} vs {fight['b']['name']} matched "
              f"{len(hits)} ESPN bouts — leaving blank rather than guessing",
              file=sys.stderr)
    fight["weight"] = ""
    fight["a"]["record"] = fight["b"]["record"] = ""
    return None


def best_both(ev):
    best = {}
    for bk in ev.get("bookmakers", []):
        for mk in bk.get("markets", []):
            if mk.get("key") != "h2h":
                continue
            for oc in mk.get("outcomes", []):
                n, p = oc.get("name"), oc.get("price")
                if p is None:
                    continue
                if n not in best or p > best[n]["price"]:
                    best[n] = {"price": p, "book": bk.get("title")}
    if len(best) != 2:
        return None
    (a, da), (b, db) = best.items()
    ia, ib = implied(da["price"]), implied(db["price"])
    tot = ia + ib
    da["chance"], db["chance"] = ia / tot * 100, ib / tot * 100
    return {"a": {"name": a, **da}, "b": {"name": b, **db},
            "sum": tot, "books": len(ev.get("bookmakers", []))}


def read_for(f):
    """One human sentence per fight, price-derived. NOTES override these."""
    note = NOTES.get(frozenset({last(f["a"]["name"]), last(f["b"]["name"])}))
    if note:
        return note
    fav = f["a"] if f["a"]["chance"] >= f["b"]["chance"] else f["b"]
    dog = f["b"] if fav is f["a"] else f["a"]
    gap = abs(f["a"]["chance"] - f["b"]["chance"])
    if f["sum"] < 1:
        return ("Worth knowing: the books disagree on this one so much that the "
                "best price on each corner actually adds up in your favor. That "
                "almost never happens.")
    if gap < 5:
        return ("The books can barely split these two — whichever corner you "
                "like, you're getting close to even money. Fights like this are "
                "where actually having an opinion pays.")
    if fav["chance"] >= 80:
        risk = abs(fav["price"]) if fav["price"] < 0 else 100
        pay = round(dog["price"] / 100) if dog["price"] > 0 else 1
        return (f"{fav['name']} is heavy chalk — you're risking ${risk} to win "
                f"$100. {dog['name']} at {dog['price']:+d} pays about {pay}-to-1 "
                "for anyone who thinks this fight is closer than the number.")
    pay = dog["price"] / 100 if dog["price"] > 0 else 1
    return (f"The books lean {fav['name']}, roughly {fav['chance']:.0f} times "
            f"out of 100. {dog['name']} at {dog['price']:+d} pays about "
            f"{pay:.1f}-to-1 on the upset.")


def fmt_time(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (dt - timedelta(hours=5)).strftime("%-I:%M %p CT")   # summer CT


NAV = """<nav>
  <a class="nav-brand" href="index.html">
    <div class="nav-logo-mark">
      <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="navLine" gradientUnits="userSpaceOnUse" x1="106.5" y1="84" x2="106.5" y2="26">
            <stop offset="0%" stop-color="var(--white)"/><stop offset="35%" stop-color="var(--white)"/><stop offset="100%" stop-color="var(--green-deep)"/>
          </linearGradient>
        </defs>
        <rect x="1" y="1" width="118" height="118" rx="18" fill="var(--black)" stroke="var(--border-lit)" stroke-width="2"/><g transform="translate(-7.75,-1)">
        <rect x="24" y="38" width="10" height="46" fill="var(--white)"/>
        <rect x="42" y="38" width="30" height="10" fill="var(--white)"/>
        <rect x="52" y="38" width="10" height="46" fill="var(--white)"/>
        <rect x="80" y="38" width="10" height="46" fill="var(--white)"/>
        <polygon points="80,38 90,38 111.5,84 101.5,84" fill="var(--white)"/>
        <rect x="101.5" y="34" width="10" height="50" fill="url(#navLine)"/>
        <polygon points="106.5,26 114.5,34 98.5,34" fill="url(#navLine)"/></g>
      </svg>
    </div>
    <span class="nav-name">Inside <span>the</span> Number</span>
  </a>
    <ul class="nav-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="index.html#analysis">Analysis</a></li>
      <li><a href="index.html#slate">Picks</a></li>
      <li><a href="games.html">Games</a></li>
      <li><a href="dfs.html">DFS</a></li>
      <li><a href="tools.html">Tools</a></li>
      <li><a href="index.html#pricing" class="nav-cta">Get Pro</a></li>
    </ul>
  <button class="nav-hamburger" id="navHamburger" aria-label="Menu" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</nav>
<div class="mobile-menu" id="mobileMenu">
    <a href="index.html">Home</a>
    <a href="index.html#analysis">Analysis</a>
    <a href="index.html#slate">Picks</a>
    <a href="games.html">Games</a>
    <a href="dfs.html">DFS</a>
    <a href="tools.html">Tools</a>
    <a href="index.html#pricing" class="nav-cta">Get Pro</a>
  </div>"""

NAV_JS = """<script>
  (function(){
    const b=document.getElementById('navHamburger'), m=document.getElementById('mobileMenu');
    if(!b||!m) return;
    const c=()=>{b.classList.remove('open');m.classList.remove('open');document.body.classList.remove('menu-open');b.setAttribute('aria-expanded','false');};
    b.addEventListener('click',()=>{const o=b.classList.toggle('open');m.classList.toggle('open',o);document.body.classList.toggle('menu-open',o);b.setAttribute('aria-expanded',o?'true':'false');});
    m.querySelectorAll('a').forEach(a=>a.addEventListener('click',c));
  })();
</script>"""

NAV_CSS = """
  .nav-logo-mark { width:44px; height:44px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
  .nav-logo-mark svg { width:100%; height:100%; display:block; }
  .nav-links a.nav-cta { color:var(--green); }
  .nav-hamburger { display:none; width:40px; height:40px; background:none; border:none; cursor:pointer; flex-direction:column; justify-content:center; align-items:center; gap:5px; z-index:200; padding:0; }
  .nav-hamburger span { display:block; width:24px; height:2px; background:var(--white); transition:transform .25s,opacity .25s; }
  .nav-hamburger.open span:nth-child(1){transform:translateY(7px) rotate(45deg);}
  .nav-hamburger.open span:nth-child(2){opacity:0;}
  .nav-hamburger.open span:nth-child(3){transform:translateY(-7px) rotate(-45deg);}
  .mobile-menu { position:fixed; inset:0; background:rgba(5,6,8,0.98); backdrop-filter:blur(20px); z-index:150; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:24px; opacity:0; pointer-events:none; transform:translateY(-12px); transition:opacity .25s,transform .25s; }
  .mobile-menu.open { opacity:1; pointer-events:auto; transform:translateY(0); }
  .mobile-menu a { color:var(--white); text-decoration:none; font-family:'Barlow Condensed',sans-serif; font-size:25px; font-weight:700; text-transform:uppercase; letter-spacing:0.04em; }
  body.menu-open { overflow:hidden; }
"""


def preview_fights(bouts):
    """Build the fight list straight from ESPN's roster, no odds.

    Used when the card is confirmed and upcoming but no book has posted lines
    yet — typically until 7-10 days out. Publishing the verified card early
    earns search traffic for the event name while it is being searched; the
    odds bolt on automatically the first run after books price the card,
    because the priced path takes precedence in main().

    ESPN lists prelims first and the main event last, so display order is the
    reverse of feed order (headliner first, walk-outs backwards).
    """
    fights = []
    for b in reversed(bouts):
        if len(b.get("names", [])) != 2 or not all(b["names"]):
            continue
        recs = b.get("recs") or ["", ""]
        f = {"a": {"name": b["names"][0], "record": recs[0] if len(recs) > 0 else ""},
             "b": {"name": b["names"][1], "record": recs[1] if len(recs) > 1 else ""},
             "weight": tidy_weight(b.get("weight", "")),
             "periods": b.get("periods"),
             "read": NOTES.get(frozenset({last(b["names"][0]),
                                          last(b["names"][1])}), "")}
        fights.append(f)
    return fights


def order_main_first(fights):
    """Headliner to the top, identified by the five-round format."""
    five = [f for f in fights if f.get("periods") == 5]
    if len(five) == 1:
        main = five[0]
    elif len(five) > 1:
        print(f"WARN: {len(five)} five-round bouts; keeping feed order",
              file=sys.stderr)
        main = five[0]
    else:
        print("WARN: no five-round bout reported — first fight in feed order "
              "treated as main. VERIFY THE HEADLINER BEFORE POSTING.",
              file=sys.stderr)
        main = fights[0]
    return [main] + [f for f in fights if f is not main]


def assert_card_is_upcoming(cards, allow_finished=False):
    """Refuse to publish a card that has already happened.

    On Aug 29 2026 this page sat live promoting odds on a UFC card that had
    finished eight hours earlier, and an automated X post drove traffic to it.
    A stale page is worse than no page: it is visibly wrong to anyone who
    watched the fights, and it is the kind of error that costs the account
    its credibility permanently.

    ESPN reports STATUS_SCHEDULED until the first bout starts. Anything else
    (in progress, final) means we must not write a pre-fight odds page.
    """
    if not cards:
        sys.exit("ERROR: ESPN returned no card for this window — refusing to "
                 "publish. A page with no verifiable card behind it is exactly "
                 "how the Aug 29 2026 incident happened.")
    live = [c for c in cards if c["status"] != "STATUS_SCHEDULED"]
    if live and not allow_finished:
        detail = "; ".join(f"{c['name']}: {c['status']}" for c in live)
        sys.exit(f"ERROR: card is not upcoming ({detail}). Refusing to publish "
                 f"pre-fight odds for a card that has started or finished. "
                 f"Pass --allow-finished only to build a results page.")
    if live:
        print(f"WARN: --allow-finished set; {len(live)} card(s) already under "
              f"way or complete", file=sys.stderr)


def build(events, bouts, title, venue, datestr, preview=False):
    """Assemble the page from priced events, keeping only this card's fights.

    Two failures on Aug 29 2026 that this function is now written against:

    1. The odds feed returns EVERY mma_mixed_martial_arts event inside the
       --start/--end window, which on a busy weekend means other promotions
       entirely. Those were merged straight onto the UFC page. Fights are now
       kept only if they appear on the ESPN roster for this card.

    2. The main event was taken as fights[0] after a reverse sort on
       commence_time. The odds feed gives every bout on a card the same
       commence_time (the card's start), so that sort is arbitrary and the
       page headlined the wrong fight. The main event is the only bout
       scheduled for five rounds — that is what we key on now.

    With preview=True the odds feed is ignored entirely and the page is built
    from ESPN's roster: fighters, records, weight classes and the hand-written
    notes, with an honest "lines not posted yet" in place of prices.
    """
    if preview:
        fights = preview_fights(bouts)
        if not fights:
            sys.exit("ERROR: preview requested but ESPN returned no usable "
                     "bouts — nothing to publish.")
        for f in fights:
            f["time"] = ""
            f["iso"] = ""
        return render(order_main_first(fights), title, venue, datestr,
                      preview=True)

    fights, off_card, unpriced = [], [], []
    for ev in sorted(events, key=lambda e: e.get("commence_time", ""), reverse=True):
        f = best_both(ev)
        if not f:
            # Event exists in the feed but no book has posted a two-way price
            # yet. Normal well ahead of a card; worth naming so the operator can
            # tell "not priced yet" apart from "wrong window".
            unpriced.append(" vs ".join(
                str(x) for x in (ev.get("home_team"), ev.get("away_team"))
                if x) or ev.get("id", "?"))
            continue
        f["time"] = fmt_time(ev["commence_time"])
        f["iso"] = ev["commence_time"]
        matched = enrich(f, bouts)
        if matched is None:
            off_card.append(f"{f['a']['name']} vs {f['b']['name']}")
            continue
        # Trust ESPN for WHEN. Segment = earliest ESPN bout date on the card is
        # the prelims; anything later is the main card.
        if matched.get("date"):
            seg_dates = sorted({b["date"] for b in bouts if b.get("date")})
            seg = "Prelims" if matched["date"] == seg_dates[0] else "Main card"
            f["time"] = f"{seg} · {fmt_time(matched['date'])}"
            f["iso"] = matched["date"]
        f["periods"] = matched.get("periods")
        f["read"] = read_for(f)
        fights.append(f)

    # Every bout ESPN lists but no book has priced still belongs on the page —
    # Chuck, Sep 5 2026: "put all fights ... for the Sept 12th fights". They
    # render with records and segment time and an honest "lines not posted yet".
    def _key(names):
        return frozenset(last(n).lower() for n in names if n)
    priced_keys = {_key([f["a"]["name"], f["b"]["name"]]) for f in fights}
    seg_dates = sorted({b["date"] for b in bouts if b.get("date")})
    extras = []
    for b in reversed(bouts):
        names = b.get("names") or []
        if len(names) != 2 or not all(names):
            continue
        if _key(names) in priced_keys:
            continue
        recs = b.get("recs") or ["", ""]
        seg = ""
        if b.get("date") and seg_dates:
            seg = ("Prelims" if b["date"] == seg_dates[0] else "Main card")
            seg = f"{seg} · {fmt_time(b['date'])}"
        extras.append({
            "a": {"name": names[0], "record": recs[0] if len(recs) > 0 else ""},
            "b": {"name": names[1], "record": recs[1] if len(recs) > 1 else ""},
            "weight": tidy_weight(b.get("weight", "")),
            "periods": b.get("periods"),
            "time": seg, "iso": b.get("date") or "",
            "unpriced": True, "books": 0,
            "read": NOTES.get(frozenset({last(names[0]), last(names[1])}), ""),
        })
    if extras:
        print(f"{len(extras)} bout(s) on the ESPN card with no book price yet — "
              "published without odds: "
              + "; ".join(f"{x['a']['name']} vs {x['b']['name']}" for x in extras),
              file=sys.stderr)
        fights += extras

    if off_card:
        print(f"filtered {len(off_card)} priced event(s) not on this ESPN card: "
              + "; ".join(off_card), file=sys.stderr)
    if unpriced:
        print(f"{len(unpriced)} event(s) in the feed with no book price yet: "
              + "; ".join(unpriced), file=sys.stderr)
    if not fights:
        if unpriced and not off_card:
            sys.exit(
                f"ERROR: the card is on ESPN but no book has priced it yet "
                f"({len(unpriced)} event(s) returned with no odds). This is "
                f"normal well before fight week — retry closer to the card. "
                f"Refusing to publish a card page with no real prices on it.")
        sys.exit("ERROR: no priced fights matched this card — refusing to write "
                 "a page. Check --start/--end and that ESPN lists the card.")

    # If nothing on the card is priced yet, everything here came from the
    # unpriced-extras pass -- that is the roster preview, not an odds page.
    any_priced = any(not f.get("unpriced") for f in fights)
    return render(order_main_first(fights), title, venue, datestr,
                  preview=not any_priced)


def render(fights, title, venue, datestr, preview):
    main = fights[0]
    stamp = datetime.now(timezone.utc).strftime("%b %-d, %Y %H:%M UTC")
    e = html.escape

    # Unpriced bouts (on the ESPN card, no book price yet) carry no win
    # chance, so every stat in the summary strip is computed over the priced
    # subset only. Sep 5 2026: forgetting this crashed the build with a
    # KeyError on "chance" the first time unpriced bouts were published.
    priced = [f for f in fights if not f.get("unpriced")]
    if not preview:
        closest = min(priced, key=lambda f: abs(f["a"]["chance"] - f["b"]["chance"]))
        heaviest = max(priced, key=lambda f: max(f["a"]["chance"], f["b"]["chance"]))
        hfav = heaviest["a"] if heaviest["a"]["chance"] > heaviest["b"]["chance"] else heaviest["b"]
        by_time = sorted((f for f in fights if f.get("iso")), key=lambda f: f["iso"])
        first_t = (by_time[0]["time"] if by_time else fights[-1]["time"])
        main_t = main["time"]

    def corner(x, bare=False):
        # bare=True: this bout is on the card but no book has posted a two-way
        # price yet (Sep 5 2026 — three Noche prelims). Showing the fighters
        # with an honest blank beats hiding a fight that is on the card.
        rec = f'<div class="f-rec">{e(x["record"])}</div>' if x.get("record") else ""
        if preview or bare:
            return f"""<div class="corner"><div class="f-name">{e(x['name'])}</div>{rec}</div>"""
        return f"""<div class="corner"><div class="f-name">{e(x['name'])}</div>{rec}
            <div class="f-price">{x['price']:+d}</div>
            <div class="f-book">best price: {e(x['book'])}</div>
            <div class="f-true">win chance {x['chance']:.0f}%</div></div>"""

    def frow(f, feature=False):
        cls = "fight feature" if feature else "fight"
        wt = e(f["weight"]) if f.get("weight") else ""
        label = "Main event · " + wt if feature and wt else (
                "Main event" if feature else wt)
        left = e(f['time']) + (f" · {wt}" if f.get('time') and wt else
                               ("" if f.get('time') else label))
        bare = bool(f.get("unpriced"))
        hold = ("lines not posted yet" if (preview or bare)
                else f"{f['books']} books quoted")
        read = f'<div class="f-read">{e(f["read"])}</div>' if f.get("read") else ""
        return f"""
      <div class="{cls}">
        <div class="f-top"><span class="f-time">{left}</span>
          <span class="f-hold">{hold}</span></div>
        <div class="f-grid">{corner(f['a'], bare)}<div class="vs">vs</div>{corner(f['b'], bare)}</div>
        {read}
      </div>"""

    rows = frow(main, True) + "".join(frow(f) for f in fights[1:])

    ld = {"@context": "https://schema.org", "@type": "SportsEvent",
          "name": title, "sport": "Mixed Martial Arts",
          **({"startDate": min(f["iso"] for f in fights if f.get("iso"))}
             if not preview and any(f.get("iso") for f in fights) else {}),
          "location": {"@type": "Place", "name": venue},
          "description": (f"Every fight on the {title} card: records and "
                          "weight classes, with odds added as books post them."
                          if preview else
                          f"Every fight on the {title} card: records, weight "
                          "classes, the best moneyline across major sportsbooks "
                          "and each fighter's win chance in plain English."),
          "organizer": {"@type": "Organization", "name": "UFC"}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home",
                   "item": "https://insidethenumber.com/"},
                  {"@type": "ListItem", "position": 2, "name": "UFC",
                   "item": "https://insidethenumber.com/ufc.html"}]}

    if preview:
        desc = (f"{title} card preview — every announced fight with records "
                "and weight classes, plus what actually matters on this card. "
                "Odds added automatically as soon as books post them.")
        page_title = f"{title} — Full Card & Fight Preview | Inside the Number"
        og_title = f"{title} — the full card, before the lines drop"
    else:
        desc = (f"{title} card — every fight with records, the best price across "
                "major sportsbooks on both corners, and each fighter's win chance "
                "in plain English.")
        page_title = f"{title} Odds — Best Price on Every Fight | Inside the Number"
        og_title = f"{title} — every fight, every price"

    if preview:
        tagline = "the full card, before the lines drop."
        sub = ("Every announced fight with records and weight classes, and the "
               "story on the ones that matter. As soon as sportsbooks post "
               "lines for this card, the best price on both corners and each "
               "fighter's win chance appear here automatically.")
        stamp_line = f"Card checked {stamp} · odds not posted yet"
        early_html = ('<div class="early">Books usually price a card 7–10 days '
                      'out. This page rebuilds itself daily and the numbers '
                      'appear the morning they exist.</div>')
        co = fights[1] if len(fights) > 1 else None
        chips = [
            ('Main event',
             f"{e(main['a']['name'].split()[-1])} vs {e(main['b']['name'].split()[-1])}",
             e(main.get('weight') or 'headliner') + ' · 5 rounds')]
        if co:
            chips.append(('Co-main',
                          f"{e(co['a']['name'].split()[-1])} vs {e(co['b']['name'].split()[-1])}",
                          e(co.get('weight') or '')))
        chips.append(('Fights announced', str(len(fights)), e(datestr)))
        strip_html = "".join(
            f'    <div class="chip"><div class="l">{l}</div>'
            f'<div class="v">{v}</div><div class="s">{s}</div></div>\n'
            for l, v, s in chips)
        expl_html = ('<p class="expl"><b>Why no odds yet?</b> Sportsbooks '
                     'don\'t price full UFC cards until fight week gets close. '
                     'Rather than show you stale or invented numbers, this page '
                     'shows the verified card now and adds the real prices the '
                     'day they post.</p>')
    else:
        tagline = "every fight, every price."
        sub = ("The best moneyline on both corners across major sportsbooks, "
               "records, and each fighter's win chance in plain English. ESPN "
               "doesn't carry MMA odds. We do.")
        nbooks = max(f['books'] for f in fights)
        # "best of 1 books" was both ungrammatical and misleading -- "best of"
        # implies we shopped several books. Only claim shopping when we did.
        stamp_line = (f"Prices updated {stamp} · "
                      + (f"best of {nbooks} books" if nbooks > 1
                         else "one book, not shopped"))
        segs = sorted({f["iso"] for f in fights if f.get("iso")})
        if len(segs) >= 2:
            early_html = (f'<div class="early">Prelims {e(fmt_time(segs[0]))} · '
                          f'Main card {e(fmt_time(segs[-1]))}. Times are card starts; '
                          f'the main event is last.</div>')
        else:
            early_html = (f'<div class="early">Card starts {e(fmt_time(segs[0]))}.</div>'
                          if segs else '')
        strip_html = f"""    <div class="chip"><div class="l">Main event</div>
      <div class="v">{e(main['a']['name'].split()[-1])} vs {e(main['b']['name'].split()[-1])}</div>
      <div class="s">{e(main.get('weight') or 'headliner')} · closes the main card</div></div>
    <div class="chip"><div class="l">Closest fight</div>
      <div class="v">{e(closest['a']['name'].split()[-1])} / {e(closest['b']['name'].split()[-1])}</div>
      <div class="s">near even money both ways — pick a side</div></div>
    <div class="chip"><div class="l">Biggest favorite</div>
      <div class="v">{e(hfav['name'])}</div>
      <div class="s">the books give him {hfav['chance']:.0f} in 100 — priced {hfav['price']:+d}</div></div>"""
        expl_html = ('<p class="expl"><b>How to read this.</b> The price shown '
                     'is the best any major book is offering on that corner '
                     'right now — always take the best number on your side; '
                     'over a season it\'s the difference between winning and '
                     'breaking even. Win chance is what the market honestly '
                     'gives each fighter once the bookmaker\'s cut is stripped '
                     'out — both corners add up to 100.</p>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{e(page_title)}</title>
<meta name="description" content="{e(desc)}"/>
<link rel="canonical" href="https://insidethenumber.com/ufc.html"/>
<meta name="theme-color" content="#050608"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"/>
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="Inside the Number"/>
<meta property="og:url" content="https://insidethenumber.com/ufc.html"/>
<meta property="og:title" content="{e(og_title)}"/>
<meta property="og:description" content="{e(desc)}"/>
<meta property="og:image" content="https://insidethenumber.com/og-image.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="https://insidethenumber.com/og-image.png"/>
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(crumbs)}</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=Barlow:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
  :root {{
    --black:#050608; --border:#1c2129; --border-lit:#2a2f3a;
    --surface-1:#0e1116; --surface-2:#141821;
    --green:#00d084; --green-deep:#007a4d; --green-dim:rgba(0,208,132,0.12);
    --blue:#3ba7ff; --red:#ff5c5c; --gold:#f0b429;
    --white:#f0f2f5; --muted:#6b7280; --mid:#9ca3af;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Barlow',sans-serif; background:var(--black); color:var(--white); line-height:1.6; }}
  body::before {{ content:''; position:fixed; inset:0; z-index:-1; pointer-events:none;
    background:
      linear-gradient(rgba(255,255,255,0.11) 1px, transparent 1px) 0 0 / 100% 64px,
      linear-gradient(90deg, rgba(255,255,255,0.11) 1px, transparent 1px) 0 0 / 64px 100%,
      radial-gradient(ellipse 65% 28% at 8% 10%, rgba(0,208,132,0.38) 0%, transparent 62%),
      radial-gradient(ellipse 58% 24% at 94% 32%, rgba(59,167,255,0.34) 0%, transparent 60%); }}
  nav {{ background:rgba(5,6,8,0.9); backdrop-filter:blur(14px); border-bottom:1px solid var(--border);
    padding:0 48px; display:flex; align-items:center; justify-content:space-between; height:60px;
    position:sticky; top:0; z-index:100; }}
  .nav-brand {{ display:flex; align-items:center; gap:10px; text-decoration:none; }}
  .nav-name {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:20px;
    letter-spacing:0.04em; text-transform:uppercase; color:var(--white); }}
  .nav-name span {{ color:var(--green); }}
  .nav-links {{ display:flex; align-items:center; gap:26px; list-style:none; }}
  .nav-links a {{ color:#b6bdc8; text-decoration:none; font-size:13px; font-weight:500;
    letter-spacing:0.06em; text-transform:uppercase; }}
  .nav-links a:hover {{ color:var(--green); }}
{NAV_CSS}
  .wrap {{ max-width:860px; margin:0 auto; padding:44px 24px 60px; }}
  .eyebrow {{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--green);
    letter-spacing:0.18em; text-transform:uppercase; margin-bottom:10px; }}
  h1 {{ font-family:'Barlow Condensed',sans-serif; font-size:clamp(34px,5vw,56px); font-weight:900;
    text-transform:uppercase; line-height:0.98; }}
  h1 span {{ background:linear-gradient(100deg,var(--green),var(--blue));
    -webkit-background-clip:text; background-clip:text; color:transparent; }}
  .sub {{ color:var(--mid); font-weight:300; margin:14px 0 6px; max-width:660px; }}
  .stamp {{ font-family:'IBM Plex Mono',monospace; font-size:10.5px; color:var(--muted); margin-bottom:6px; }}
  .early {{ font-family:'IBM Plex Mono',monospace; font-size:10.5px; color:var(--gold); margin-bottom:24px; }}
  .strip {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:22px 0 30px; }}
  .chip {{ background:var(--surface-1); border:1px solid var(--border); border-radius:12px; padding:13px 15px; }}
  .chip .l {{ font-family:'IBM Plex Mono',monospace; font-size:8.5px; color:var(--muted);
    letter-spacing:0.13em; text-transform:uppercase; margin-bottom:5px; }}
  .chip .v {{ font-family:'Barlow Condensed',sans-serif; font-size:17px; font-weight:800; }}
  .chip .s {{ font-size:11.5px; color:var(--mid); }}
  .fight {{ background:var(--surface-1); border:1px solid var(--border); border-radius:14px;
    padding:18px 20px; margin-bottom:14px; }}
  .fight.feature {{ border-top:3px solid var(--green); background:var(--surface-2); }}
  .f-top {{ display:flex; justify-content:space-between; margin-bottom:12px; }}
  .f-time {{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--blue); letter-spacing:0.1em; }}
  .f-hold {{ font-family:'IBM Plex Mono',monospace; font-size:9.5px; color:var(--muted);
    letter-spacing:0.06em; text-transform:uppercase; }}
  .f-grid {{ display:grid; grid-template-columns:1fr auto 1fr; gap:14px; align-items:center; }}
  .corner {{ text-align:center; }}
  .f-name {{ font-family:'Barlow Condensed',sans-serif; font-size:19px; font-weight:800;
    text-transform:uppercase; letter-spacing:0.02em; }}
  .f-rec {{ font-family:'IBM Plex Mono',monospace; font-size:10.5px; color:var(--muted); }}
  .f-price {{ font-family:'IBM Plex Mono',monospace; font-size:22px; font-weight:600;
    color:var(--green); margin:2px 0; }}
  .f-book {{ font-size:11px; color:var(--muted); }}
  .f-true {{ font-family:'IBM Plex Mono',monospace; font-size:11.5px; color:var(--mid); margin-top:3px; }}
  .vs {{ font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--muted); }}
  .f-read {{ border-top:1px solid var(--border); margin-top:13px; padding-top:11px;
    font-size:13.5px; color:var(--mid); font-weight:300; }}
  .expl {{ border-top:1px solid var(--border); margin-top:26px; padding-top:18px;
    font-size:13px; color:var(--mid); font-weight:300; }}
  .cta {{ background:var(--green-dim); border:1px solid var(--green); border-radius:14px;
    padding:20px 22px; margin-top:26px; }}
  .cta a {{ color:var(--green); font-weight:600; text-decoration:none; }}
  footer {{ border-top:1px solid var(--border); padding:26px 24px 34px; text-align:center; }}
  .foot-d {{ font-size:11px; color:var(--muted); max-width:640px; margin:0 auto 8px; }}
  .foot-c {{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--muted); }}
  @media (max-width:640px) {{
    nav {{ padding:0 18px; }} .nav-links {{ display:none; }} .nav-hamburger {{ display:flex; }}
    .strip {{ grid-template-columns:1fr; }}
    .f-grid {{ gap:8px; }} .f-name {{ font-size:16px; }} .f-price {{ font-size:18px; }}
  }}
</style>
<style id="nav-fit">
/* NAV FIT (Aug 31 2026) - the nav links need ~770px but this page only swapped
   to the hamburger at 640px, so between ~640px and ~770px they crowded the logo
   and ran off the right edge. Compact tier + one shared 900px hamburger
   breakpoint gives ~320px of slack instead of none. Keep this in sync with the
   identical block in the hand-maintained pages (index.html, games.html, etc). */
@media (max-width:1150px){{
  nav{{padding-left:20px !important;padding-right:20px !important}}
  .nav-links{{gap:16px !important}}
  .nav-links a{{font-size:11.5px !important;letter-spacing:.04em !important}}
  .nav-name{{font-size:17px !important}}
  .nav-logo-mark{{width:34px !important;height:34px !important}}
}}
@media (max-width:900px){{
  .nav-links{{display:none !important}}
  .nav-hamburger{{display:flex !important}}
}}
</style>
</head>
<body>
{NAV}
<div class="wrap">
  <div class="eyebrow">// UFC · {e(datestr)} · {e(venue)}</div>
  <h1>{e(title)}<br/><span>{tagline}</span></h1>
  <p class="sub">{sub}</p>
  <div class="stamp">{stamp_line}</div>
  {early_html}
  <div class="strip">
{strip_html}
  </div>
{rows}
  {expl_html}
  <div class="cta"><b>One free pick every day, with the reasoning shown.</b><br/>
    <a href="https://insidethenumber.beehiiv.com/subscribe" target="_blank" rel="noopener">
    Get it in your inbox →</a></div>
</div>
<footer>
  <div class="foot-d">For entertainment purposes only. Inside the Number does not facilitate
    gambling. Odds shown are from licensed data feeds and may differ from your book.
    Please gamble responsibly.</div>
  <div class="foot-c">© 2026 ITN · Nashville, TN</div>
</footer>
{NAV_JS}
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--title", default="UFC Fight Night Shanghai")
    ap.add_argument("--venue", default="Shanghai, China")
    ap.add_argument("--datestr", default="Sat, Aug 29")
    ap.add_argument("--out", default=os.path.join(ROOT, "ufc.html"))
    ap.add_argument("--allow-finished", action="store_true",
                    help="Publish even if ESPN says the card has started or "
                         "finished. Off by default: the Aug 29 2026 incident "
                         "was a live page promoting odds on a finished card.")
    ap.add_argument("--max-age-hours", type=float, default=None,
                    help="Skip the rebuild if the existing page's price stamp "
                         "is younger than this. Lets the workflow poll often "
                         "without burning an Odds API credit every time.")
    a = ap.parse_args()

    # Same problem as the X queue: GitHub's scheduled trigger for this job had
    # never once fired on time. The answer there was to poll every 20 minutes
    # instead of trusting one cron. Here a poll costs an Odds API credit, and
    # the free tier is 500 a month — so the age of the stamp already on the
    # page decides whether this run does any work. Dropped triggers get covered
    # by the next poll; credits stay at roughly one refresh per max-age window.
    if a.max_age_hours is not None and os.path.exists(a.out):
        existing = open(a.out).read()
        if "Card checked" in existing:
            # Preview page: always rebuild. The whole point of polling is to
            # notice the morning the books post lines.
            m = None
            print("existing page is a roster preview — rebuilding to check "
                  "for freshly posted lines.", file=sys.stderr)
        else:
            m = re.search(
                r"Prices updated ([A-Z][a-z]{2} \d{1,2}, \d{4} \d{2}:\d{2}) UTC",
                existing)
        if m:
            import datetime as _dt
            try:
                stamped = _dt.datetime.strptime(m.group(1), "%b %d, %Y %H:%M").replace(
                    tzinfo=_dt.timezone.utc)
                age = (_dt.datetime.now(_dt.timezone.utc) - stamped).total_seconds() / 3600
                if age < a.max_age_hours:
                    print(f"page is {age:.1f}h old (< {a.max_age_hours}h) — "
                          f"skipping, no credit spent.")
                    return
                print(f"page is {age:.1f}h old — refreshing.", file=sys.stderr)
            except ValueError as e:
                print(f"WARN: could not read price stamp ({e}) — rebuilding.",
                      file=sys.stderr)

    # ESPN first: it is the authority on what is actually ON this card and
    # whether the card has already happened. If the guard trips we exit before
    # spending an Odds API credit.
    bouts, cards = fetch_espn(date_range(a.start, a.end))
    assert_card_is_upcoming(cards, a.allow_finished)

    events = fetch_odds(a.start, a.end)
    print(f"{len(events)} priced events in window", file=sys.stderr)
    # If any event carries a real two-way price we build the priced page;
    # otherwise fall back to the roster preview. The check mirrors best_both()
    # so the decision and the build cannot disagree.
    have_prices = any(best_both(ev) for ev in events)
    if not have_prices:
        print("no book has priced this card yet — building the roster "
              "preview; prices bolt on automatically once they exist.",
              file=sys.stderr)
    page = build(events, bouts, a.title, a.venue, a.datestr,
                 preview=not have_prices)
    with open(a.out, "w") as fh:
        fh.write(page)
    print(f"wrote {a.out} ({len(page):,} bytes)")


if __name__ == "__main__":
    main()

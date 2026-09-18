#!/usr/bin/env python3
"""
Full Board scope + no-silent-redirects — Phase 1 (Sep 18 2026)
==============================================================

Three defects in games.html, all reported by the owner and all confirmed:

  1. "The Full Board only shows MLB." Not a filter bug. The board fetched all
     eight leagues for today's ET date and then auto-selected firstWith() —
     the first league in a hard-coded array with any games. MLB is first in
     that array and plays daily in September, so MLB won every time. In
     February the same code would have opened on basketball. Fixed by
     selecting the league with the most games priced, and by saying on the
     page why that league was chosen.

  2. Three of the eight league chips left the board. CFB, UFC and PGA each ran
     location.replace(), so a control that looks like a filter behaved like an
     exit — losing the rail, the read-time stamp and the detail shell. All
     three now render in place.

  3. The board only ever fetched TODAY. On a Friday the CFB chip showed three
     games while seventy-odd were already priced for Saturday. Football now
     defaults to a seven-day window, baseball and the indoor sports stay on
     today, and every board states which window it is showing.

Nothing here invents a number. Golf still has no two-way market and says so;
UFC shows only bouts the feed actually carries. Loading, empty and
feed-not-reached states are preserved and extended, not removed.

Usage:  python3 scripts/build_board_scope.py [--check]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "games.html"

SENTINEL = "/* ITN-BOARD-SCOPE */"

# ── 1. Pull the team-event parser out of load() so the week fetch can reuse
#       it verbatim. Previously the only full parse lived inside load()'s
#       Promise.all, which is why the range fetch (upcoming()) had to use a
#       thinner one with no records and no opening lines. ─────────────────────
P1_OLD = """      D[label]=(d.events||[]).map(ev=>{
        const c=ev.competitions?.[0];if(!c)return null;
        const h=c.competitors.find(x=>x.homeAway==='home'),a=c.competitors.find(x=>x.homeAway==='away');"""
P1_NEW = """      D[label]=parseTeam(d,label);
      TODAY_N[label]=D[label].length;
    }catch(e){D[label]=[]}
  }));
  ready=true; route();
  stampBoard();
}

/* The full team-event parse, lifted out of load() unchanged so the week
   window gets exactly the same card data as today does — records, splits,
   probable starters, opening lines and all. */
function parseTeam(d,label){
  return (d.events||[]).map(ev=>{
        const c=ev.competitions?.[0];if(!c)return null;
        const h=c.competitors.find(x=>x.homeAway==='home'),a=c.competitors.find(x=>x.homeAway==='away');"""

P2_OLD = """          a:side(a),h:side(h),o,ours:OURS[key]||null};
      }).filter(Boolean);
    }catch(e){D[label]=[]}
  }));
  ready=true; route();
  stampBoard();
}"""
P2_NEW = """          date:ev.date||'',
          a:side(a),h:side(h),o,ours:OURS[key]||null};
  }).filter(Boolean);
}"""

# ── 2. CFB needs group 80 (FBS) or the Saturday slate arrives partial. ──────
P3_OLD = ("      const r=await fetch(`https://site.api.espn.com/apis/site/v2/sports/"
          "${path}/scoreboard?dates=${eDate()}`);")
P3_NEW = ("      const r=await fetch(`https://site.api.espn.com/apis/site/v2/sports/"
          "${path}/scoreboard?dates=${eDate()}${GROUPS(label)}`);")

# ── 3. Scope machinery, replacing the array-order default. ─────────────────
P4_OLD = """const total=()=>LEAGUES.reduce((t,[l])=>t+(D[l]||[]).length,0);
const firstWith=()=>(LEAGUES.find(([l])=>(D[l]||[]).length)||['MLB'])[0];"""

P4_NEW = SENTINEL + """
const total=()=>LEAGUES.reduce((t,[l])=>t+(D[l]||[]).length,0);

/* Games priced today, snapshotted at load. The rail keeps showing these even
   when the visitor is looking at a week window, so the counts never quietly
   change meaning under them; the scope note below the rail says as much. */
const TODAY_N={};

/* Which league the board opens on when the URL does not name one.

   It used to be "the first league in LEAGUES that has anything on". MLB is
   first in that array and plays every day from April to October, so the Full
   Board opened on baseball all season no matter what else was happening —
   which is exactly what "the Full Board only shows MLB" was. Now it opens on
   whichever league has the most games priced right now, ties broken by the
   array order so the choice is stable inside a page session, and the page
   says why it chose. */
function defaultLeague(){
  let best=null,n=0;
  for(const [l] of LEAGUES){const c=(D[l]||[]).length; if(c>n){n=c;best=l}}
  return best||'MLB';
}
/* Kept as the old name because the in-flight guard further down still calls
   it; both now mean the same thing. */
const firstWith=defaultLeague;

/* ESPN's college-football scoreboard returns a partial slate unless you ask
   for a group. 80 is FBS, which is what a board should show. */
const GROUPS=s=>s==='CFB'?'&groups=80':'';

/* ── BOARD SCOPE ──────────────────────────────────────────────────────────
   "Today" is the honest window for a sport that plays daily. It is the wrong
   window for football, which plays on two or three days a week: on a Friday
   the CFB feed has a handful of games while most of the week's board is
   already priced for Saturday. Showing the handful without saying so reads
   as a thin week rather than the wrong window. So football opens on the week,
   everything else opens on today, and both say which one they are showing. */
const SCOPE_DEFAULT={MLB:'today',NBA:'today',NHL:'today',CBB:'today',NFL:'week',CFB:'week'};
const SCOPE_CHOICE=['today','week'];
const WEEK_DAYS=7;
const W={};   // week window per league; null means the feed refused

function scopeOf(sport){
  const q=(new URLSearchParams(location.search).get('scope')||'').toLowerCase();
  if(SCOPE_CHOICE.indexOf(q)>=0 && SCOPE_DEFAULT[sport]) return q;
  return SCOPE_DEFAULT[sport]||'event';
}
function weekEnds(){return [new Date(), new Date(Date.now()+(WEEK_DAYS-1)*864e5)]}
function ymd(d){return `${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}`}

async function loadWeek(sport){
  if(W[sport]!==undefined) return W[sport];
  const path=(LEAGUES.find(([l])=>l===sport)||[])[1];
  if(!path){W[sport]=[];return W[sport]}
  const [d0,d1]=weekEnds();
  try{
    const r=await fetch(`https://site.api.espn.com/apis/site/v2/sports/${path}`
      +`/scoreboard?dates=${ymd(d0)}-${ymd(d1)}${GROUPS(sport)}&limit=300`);
    if(!r.ok){W[sport]=null;return W[sport]}
    W[sport]=parseTeam(await r.json(),sport)
      .sort((a,b)=>new Date(a.date||0)-new Date(b.date||0));
  }catch(e){W[sport]=null}
  return W[sport];
}

/* The scope control. Visible, not a URL trick: a visitor who wants today's
   three football games instead of the week's seventy can have them, and the
   note underneath always states the window and the date range it covers. */
function scopeBar(sport,scope,count){
  const el=document.getElementById('board-scope'); if(!el) return;
  if(!SCOPE_DEFAULT[sport]){el.innerHTML='';el.style.display='none';return}
  el.style.display='';
  const [d0,d1]=weekEnds();
  const day=d=>`${MO[d.getMonth()]} ${d.getDate()}`;
  const btn=(v,label)=>`<a href="?sport=${sport}&scope=${v}"${v===scope?' aria-current="page"':''}>${label}</a>`;
  const window_=scope==='week'?`${day(d0)} \\u2013 ${day(d1)}`:day(d0);
  const n=count==null?'reading the feed\\u2026'
        :count?`${count} ${count===1?'game':'games'} priced`:'nothing priced in this window';
  el.innerHTML=
    `<div class="bs-row"><span class="bs-lab">Showing</span>${btn('today','Today')}${btn('week','This week')}</div>`+
    `<div class="bs-note">${sport} \\u00b7 ${scope==='week'?'the next 7 days':'today only'} \\u00b7 ${window_} \\u00b7 ${n}`+
    `${scope==='week'?' \\u00b7 counts on the bar above are today\\u2019s games':''}</div>`;
}
"""

# ── 4. listView: no redirects, honour the scope, state it, keep the honest
#       empty and feed-not-reached states. ────────────────────────────────────
P5_OLD = """async function listView(sport){
  /* PGA: the tab IS the tournament page. ESPN's golf feed carries no odds at
     all (verified — the odds endpoint returns empty), so the board could only
     ever show a bare event graphic. On Aug 24 that meant a stale BMW
     Championship card, which Chuck flagged; pga.html carries the current
     event with the full field priced and our pick. Unconditional, unlike the
     UFC redirect, because golf never has two-way prices for a live board. */
  if(sport==='PGA'){ location.replace('pga.html'); return; }
  if(sport==='CFB'){ location.replace('cfb.html'); return; }
  rail(sport);
  const g=D[sport]||[];
  const view=document.getElementById('view');
  if(g.length){"""

P5_NEW = """/* Golf has no two-way market. ESPN's golf feed carries no prices at all
   (verified — the odds endpoint returns empty), so there is no spread, total
   or fair price to read here and inventing one is out of the question. The
   board used to location.replace() to pga.html, which made a filter chip
   behave like an exit. It now renders the tournament in place and offers the
   outrights board as a visible, labelled link. */
function pgaView(){
  const view=document.getElementById('view');
  const g=D.PGA||[];
  ticker('PGA',null);
  const head=`<div class="crumb"><a href="/">Home</a> \\u203a <a href="?sport=PGA">PGA</a> \\u203a <span>This week</span></div>
    <h1>PGA \\u2014 This Week's Event</h1>
    <p class="lead">Golf is priced as outrights \\u2014 one field, one winner \\u2014 not as a two-way
    market, so there is no spread, total or fair-price read on this board. The full field with
    prices is on the <a href="/pga" style="color:var(--green)">PGA board</a>.</p>`;
  view.innerHTML = g.length
    ? head+`<div class="list">${g.map(card).join('')}</div>`
    : head+`<div class="off-hero">
        <div class="off-tag">PGA \\u00b7 nothing on the feed today</div>
        <div class="off-h">No round on the feed right now</div>
        <div class="off-when"><a href="/pga" style="color:var(--green)">Open this week's PGA board \\u2192</a></div>
        ${liveChips('PGA')}</div>`;
}

/* A fight is a two-way market with no spread and no total, so the UFC view is
   the card itself: bout order, weight class, records, and the moneyline pair
   wherever the feed carries one. Nothing is shown that the feed did not
   return. This also used to location.replace() to an archived card page. */
function ufcView(){
  const view=document.getElementById('view');
  const f=D.UFC||[];
  ticker('UFC',null);
  const crumb=`<div class="crumb"><a href="/">Home</a> \\u203a <a href="?sport=UFC">UFC</a> \\u203a <span>Current card</span></div>`;
  if(f.length){
    const name=(f.find(x=>x.card)||{}).card||'';
    view.innerHTML=crumb+`<h1>UFC \\u2014 ${name||'Current Card'}</h1>
      <p class="lead">Every bout ESPN has on this card, in order. A fight carries no spread and no
      total, so the market read is the two-way price and the margin sitting inside it. The full card
      priced across the books is on the <a href="/ufc-331-odds" style="color:var(--green)">UFC page</a>.</p>
      <div class="list">${f.map(card).join('')}</div>`;
    return;
  }
  view.innerHTML=crumb+`<h1>UFC \\u2014 No Bouts On The Feed</h1>
    <p class="lead">ESPN's MMA feed has no bouts for today. That is the state of the feed, not a
    claim that nothing is scheduled this week.</p>
    <div class="off-hero">
      <div class="off-tag">UFC \\u00b7 nothing on the feed today</div>
      <div class="off-h">The current numbered card has its own page</div>
      <div class="off-when"><a href="/ufc-331-odds" style="color:var(--green)">Open the current UFC card \\u2192</a></div>
      ${liveChips('UFC')}
    </div>`;
}

async function listView(sport){
  rail(sport);
  const view=document.getElementById('view');
  const scope=scopeOf(sport);

  /* Event-shaped sports get their own view rather than a silent jump to
     another page. Neither invents a price. */
  if(sport==='PGA'){ scopeBar(sport,scope,null); return pgaView(); }
  if(sport==='UFC'){ scopeBar(sport,scope,null); return ufcView(); }

  let g=D[sport]||[];
  if(scope==='week'){
    scopeBar(sport,scope,null);
    view.innerHTML=`<div class="empty view-loading">Reading the ${sport} board for the next 7 days\\u2026</div>`;
    const w=await loadWeek(sport);
    /* the visitor may have moved on while that was in flight */
    const now=(new URLSearchParams(location.search).get('sport')||'').toUpperCase();
    if(now && now!==sport) return;
    if(w===null){
      scopeBar(sport,scope,null);
      view.innerHTML=`<div class="off-hero">
        <div class="off-tag">${sport} \\u00b7 feed not reached</div>
        <div class="off-h">Could not read the ${sport} week</div>
        <div class="off-when">ESPN did not answer for this window. Nothing is shown rather than
        something stale.</div>
        <div class="off-out"><a href="?sport=${sport}&scope=today" style="color:var(--green)">Try today's board instead \\u2192</a></div>
        ${liveChips(sport)}</div>`;
      return;
    }
    /* Merged into D so the ticker and the game detail can find a game the
       visitor opened from the week board. TODAY_N keeps the rail honest. */
    const seen={}; (D[sport]||[]).forEach(x=>seen[x.id]=1);
    D[sport]=(D[sport]||[]).concat(w.filter(x=>!seen[x.id]));
    g=w;
  }
  scopeBar(sport,scope,g.length);
  if(g.length){"""

# The h1 / lead line, now scope-aware and with the "why this league" note.
P6_OLD = """      <div class="crumb"><a href="/">Home</a> › <span>${sport}</span></div>
      <h1>${sport} — ${sport==='UFC'?"Tonight's Card":sport==='PGA'?'This Week':"Today's Board"}</h1>
      <p class="lead">${sport==='UFC'?`Every fight on tonight's ${sport} card, with records and bout order. Full Shanghai card with best prices across the books is <a href="ufc" style="color:var(--green)">right here</a>.`:sport==='PGA'?`This week's ${sport} field. Golf is priced as outrights rather than a two-way market, so it's covered in the newsletter rather than on this board.`:`Every ${sport} game on the board today. Each one opens the full market — moneyline, spread and total — with each side's real win chance and the move since the number opened.`}</p>"""

P6_NEW = """      <div class="crumb"><a href="/">Home</a> \\u203a <span>${sport}</span></div>
      <h1>${sport} \\u2014 ${scope==='week'?"This Week's Board":"Today's Board"}</h1>
      ${!(new URLSearchParams(location.search).get('sport'))?`<p class="lead" style="color:var(--muted);font-size:13.5px">Opened on ${sport} because it has the most games priced right now. Every league is on the bar above \\u2014 they all stay on this page.</p>`:''}
      <p class="lead">Every ${sport} game priced ${scope==='week'?'over the next seven days':'today'}. Each one opens the full market \\u2014 moneyline, spread and total \\u2014 with each side's real win chance and the move since the number opened.</p>"""

# The empty branch: the UFC redirect goes, and the copy stops assuming "today".
P7_OLD = """    /* UFC: the tab IS the card page. When ESPN has no live fights today, send
       the visitor straight to ufc.html — the static page with every upcoming
       fight priced across the books. The old empty state said "No UFC games
       on the board" and "out of season", both false with a fully priced card
       five days out; Chuck's call (Aug 24) was to stop apologizing and show
       the page. On fight day ESPN has events, this branch never runs, and the
       live board renders as before. */
    if(sport==='UFC'){ location.replace('ufc.html'); return; }
    ticker(sport,null);
    view.innerHTML=`
      <div class="off-hero">
        <div class="off-tag">${sport} · off today</div>
        <div class="off-h">No ${sport} games on the board</div>"""

P7_NEW = """    ticker(sport,null);
    view.innerHTML=`
      <div class="off-hero">
        <div class="off-tag">${sport} \\u00b7 ${scope==='week'?'nothing in the next 7 days':'off today'}</div>
        <div class="off-h">No ${sport} games ${scope==='week'?'priced this week':'on the board today'}</div>
        ${scope==='today'?`<div class="off-out" style="margin-bottom:8px"><a href="?sport=${sport}&scope=week" style="color:var(--green)">Look at the next 7 days \\u2192</a></div>`:''}"""

# ── 5. The scope control's markup and styling. ─────────────────────────────
P8_OLD = '<div class="tick" id="tick"></div>'
P8_NEW = """<div class="tick" id="tick"></div>

<!-- Board scope. Written by JS so it can never state a window the feed was
     not actually asked for. Hidden for the event-shaped sports (UFC, PGA),
     which have no today-versus-week choice to offer. -->
<style>
  #board-scope{max-width:1100px;margin:12px auto 0;padding:0 16px}
  #board-scope .bs-row{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
  #board-scope .bs-lab{font-family:'IBM Plex Mono',monospace;font-size:9.5px;
    letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-right:2px}
  #board-scope .bs-row a{display:inline-block;padding:5px 12px;border-radius:999px;
    border:1px solid var(--border-lit);background:rgba(255,255,255,.02);color:#c9cfd8;
    text-decoration:none;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.06em}
  #board-scope .bs-row a:hover{color:var(--white);border-color:#39424f}
  #board-scope .bs-row a[aria-current="page"]{color:var(--green);
    border-color:rgba(0,208,132,.5);background:rgba(0,208,132,.07)}
  #board-scope .bs-row a:focus-visible{outline:2px solid var(--green);outline-offset:3px}
  #board-scope .bs-note{margin-top:7px;font-family:'IBM Plex Mono',monospace;
    font-size:10.5px;color:var(--muted);letter-spacing:.04em}
  @media(max-width:900px){#board-scope{padding:0 20px}}
</style>
<div id="board-scope"></div>"""

# ── 6. A game detail is one game, not a window, so the scope control has
#       nothing to say there. Hidden rather than left showing the last board's
#       window, which would be a false statement about what is on screen. ────
P9_OLD = """function gameView(sport,id){
  rail(sport);
  ticker(sport,id);"""
P9_NEW = """function gameView(sport,id){
  rail(sport);
  const sb=document.getElementById('board-scope');
  if(sb){sb.innerHTML='';sb.style.display='none';}
  ticker(sport,id);"""

PATCHES = [
    ("extract parseTeam (head)", P1_OLD, P1_NEW, 1),
    ("extract parseTeam (tail)", P2_OLD, P2_NEW, 1),
    ("CFB group 80 on the today fetch", P3_OLD, P3_NEW, 1),
    ("scope machinery + most-games default", P4_OLD, P4_NEW, 1),
    ("listView: no redirects, scope-aware", P5_OLD, P5_NEW, 1),
    ("board heading states the window", P6_OLD, P6_NEW, 1),
    ("empty state drops the UFC redirect", P7_OLD, P7_NEW, 1),
    ("scope control markup", P8_OLD, P8_NEW, 1),
    ("game detail hides the scope control", P9_OLD, P9_NEW, 1),
]


def main():
    check = "--check" in sys.argv
    html = TARGET.read_text(encoding="utf-8")

    if SENTINEL in html:
        print("games.html already carries the board-scope patch — nothing to do.")
        return 0
    if check:
        for label, old, _new, n in PATCHES:
            found = html.count(old)
            print("%-42s %s" % (label, "ok" if found == n else "ANCHOR MISS (%d)" % found))
        return 0

    for label, old, new, n in PATCHES:
        found = html.count(old)
        if found != n:
            print("STOP. Anchor for '%s' matched %d times, expected %d. "
                  "Nothing written." % (label, found, n))
            return 1
        html = html.replace(old, new, n)

    # No board control may navigate away silently. Matched with the opening
    # quote so the comments above, which name the old behaviour, do not trip it.
    if "location.replace('" in html or 'location.replace("' in html:
        print("STOP. A location.replace() survived the patch. Nothing written.")
        return 1

    TARGET.write_text(html, encoding="utf-8")
    print("games.html patched: %d anchors, no silent redirects remain." % len(PATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())

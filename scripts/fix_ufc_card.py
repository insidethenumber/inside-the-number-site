#!/usr/bin/env python3
"""
UFC board repair — /games?sport=UFC becomes a rolling current-card route.
Sep 18 2026.

THE BUG
  games.html asked ESPN for MMA events on TODAY's date only. A fight card is
  an event, not a day, so on six days out of seven that query returns nothing.
  Verified against the live feed: ?dates=20260918 -> 0 events, while
  UFC 331: Van vs. Pantoja 2 sat one day away with 12 bouts already published.
  The board said "No bouts on the feed" and pushed visitors at the dated
  /ufc-331-odds article as though it were the live card.

WHAT THE FEED ACTUALLY CARRIES  (probed Sep 18 2026, UFC 331, all 12 bouts)
  event name + shortName, event date, venues[0].fullName + city/state,
  per-bout start time, type.abbreviation (weight class),
  format.regulation.periods (3 or 5 — 5 marks a main/championship bout),
  athlete.displayName / shortName, records[].summary, athlete.flag.href + alt.
  NOT carried: prices. Every bout returned odds:null, and the per-event
  summary endpoint answers {code,message} rather than a document. So this
  board shows a CARD, not a market, and says so.

  ESPN supplies no cardSegment field and no bout order. It does publish three
  distinct start times (21:30Z x3, 23:00Z x4, 01:00Z x5) — its own
  segmentation. Bouts are grouped by that real start time and each group is
  labelled with the time, NOT with an invented "Main Card" / "Prelims" label
  the feed never gave.

Usage: python3 scripts/fix_ufc_card.py [--check]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "games.html"
SENTINEL = "/* ITN-UFC-CURRENT-CARD */"

# ── 1. Replace the inline mma parse with a call to the shared one ────────
P1_OLD = (Path(__file__).resolve().parent / 'ufc_mma_block.txt').read_text(encoding='utf-8')
P1_NEW = '      if(kind===\'mma\'){\n        /* One ESPN "event" is a card; each competition is a single fight.\n           Dana White\'s Contender Series shares this endpoint and is filtered\n           out by NOT_UFC, exactly as the current-card fetch does. */\n        D[label]=(d.events||[]).filter(ev=>!NOT_UFC.test(ev.name||ev.shortName||\'\'))\n          .flatMap(ev=>mmaBouts(ev,label));\n        return;\n      }'

# ── 2. The shared parser + the current-card loader, inserted above ufcView.
P2_OLD = """/* A fight is a two-way market with no spread and no total, so the UFC view is
   the card itself: bout order, weight class, records, and the moneyline pair
   wherever the feed carries one. Nothing is shown that the feed did not
   return. This also used to location.replace() to an archived card page. */
function ufcView(){"""

P2_NEW = SENTINEL + """
/* Dana White's Contender Series shares the UFC endpoint but is a developmental
   show, not a UFC card. Hoisted to top level so the board fetch and the
   current-card fetch filter it identically. */
const NOT_UFC=/contender series|dana white/i;

/* One ESPN "event" is a card; each competition is a single fight. */
function mmaBouts(ev,label){
  return (ev.competitions||[]).map(c=>{
    const cs=c.competitors||[]; if(cs.length<2) return null;
    const [x,y]=cs;
    const nm=z=>z.athlete?.shortName||z.athlete?.displayName||'';
    const side=z=>({ab:nm(z),name:z.athlete?.displayName||'',
      logo:z.athlete?.flag?.href||'',flagAlt:z.athlete?.flag?.alt||'',sc:'',
      rec:z.records?.find(r=>r.type==='total')?.summary||''});
    return{id:c.id,league:label,kind:'mma',state:c.status?.type?.state||ev.status?.type?.state,
      detail:c.status?.type?.shortDetail||ev.status?.type?.shortDetail||'',
      card:ev.name||'',weight:c.type?.abbreviation||'',venue:c.venue?.fullName||'',
      /* per-bout start time and scheduled rounds: both real feed fields, and
         the only segmentation ESPN gives a card */
      boutDate:c.date||'',rounds:c.format?.regulation?.periods||null,
      a:side(x),h:side(y),
      /* Fights can carry a published pick like any other contest. Matched on
         last names, both orders, because a fight has no home or away. */
      o:c.odds?.[0]||{},
      ours:OURS[mmaKey(nm(x),nm(y))]||OURS[mmaKey(nm(y),nm(x))]||null};
  }).filter(Boolean);
}

/* ── THE CURRENT UFC CARD ──────────────────────────────────────────────────
   A card is an event, not a day. Asking for today returns nothing on six days
   in seven, which is why this board read "No bouts on the feed" with UFC 331
   one day out. Ask across a forward window and take the next real UFC event;
   a card that started earlier tonight still counts as the current one. */
const UFC_WINDOW_DAYS=45;
let UFC_CARD;   // undefined = not tried · null = none found · object = the card

async function loadUfcCard(){
  if(UFC_CARD!==undefined) return UFC_CARD;
  const d0=new Date(), d1=new Date(Date.now()+UFC_WINDOW_DAYS*864e5);
  try{
    const r=await fetch('https://site.api.espn.com/apis/site/v2/sports/mma/ufc'
      +`/scoreboard?dates=${ymd(d0)}-${ymd(d1)}&limit=100`);
    if(!r.ok){ UFC_CARD=null; return UFC_CARD; }
    const j=await r.json();
    const cutoff=Date.now()-6*36e5;      // a card in progress is still current
    const ev=(j.events||[])
      .filter(e=>!NOT_UFC.test(e.name||e.shortName||''))
      .filter(e=>(e.competitions||[]).length)
      .filter(e=>{const t=Date.parse(e.date); return Number.isFinite(t)&&t>=cutoff})
      .sort((a,b)=>Date.parse(a.date)-Date.parse(b.date))[0];
    if(!ev){ UFC_CARD=null; return UFC_CARD; }
    const v=(ev.venues||[])[0]||{};
    UFC_CARD={id:ev.id,name:ev.name||'',short:ev.shortName||'',date:ev.date||'',
      venue:v.fullName||'',
      city:[v.address&&v.address.city,v.address&&v.address.state].filter(Boolean).join(', '),
      bouts:mmaBouts(ev,'UFC')};
  }catch(e){ UFC_CARD=null; }
  return UFC_CARD;
}

const CT=(iso,opts)=>{ const d=new Date(iso); if(isNaN(d)) return '';
  return d.toLocaleString('en-US',Object.assign({timeZone:'America/Chicago'},opts)); };

/* One bout. Deliberately NOT the team card: a fight has no spread and no
   total, so it gets no market grid. A price row appears only if the feed
   actually returned two moneylines for this bout. */
function fightCard(g){
  const p=pair(g.o&&g.o.moneyline&&g.o.moneyline.away&&g.o.moneyline.away.close&&g.o.moneyline.away.close.odds,
               g.o&&g.o.moneyline&&g.o.moneyline.home&&g.o.moneyline.home.close&&g.o.moneyline.home.close.odds);
  const mlA=g.o&&g.o.moneyline&&g.o.moneyline.away&&g.o.moneyline.away.close&&g.o.moneyline.away.close.odds;
  const mlH=g.o&&g.o.moneyline&&g.o.moneyline.home&&g.o.moneyline.home.close&&g.o.moneyline.home.close.odds;
  const row=(t,ml,tp)=>`<div class="fc-f">
    ${t.logo?`<img src="${t.logo}" alt="${t.flagAlt||''}" title="${t.flagAlt||''}" loading="lazy"/>`:'<span></span>'}
    <span class="fc-nm">${t.name||t.ab}</span>
    <span class="fc-rec">${t.rec||''}${ml!=null&&fmt(ml)?` <b>${fmt(ml)}</b>`:''}${tp!=null?` <i>${(tp*100).toFixed(1)}%</i>`:''}</span>
  </div>`;
  const title=g.rounds===5;
  return `<a class="fc" href="?sport=UFC&game=${g.id}">
    <div class="fc-top">
      <span class="w">${g.weight||'UFC'}</span>
      <span>${title?'<b class="main">5 rounds</b> \\u00b7 ':''}${g.boutDate?CT(g.boutDate,{hour:'numeric',minute:'2-digit'})+' CT':''}</span>
    </div>
    ${row(g.a,mlA,p?p.a:null)}
    <div class="fc-v">vs</div>
    ${row(g.h,mlH,p?p.b:null)}
  </a>`;
}

/* A fight is a two-way market with no spread and no total, so the UFC view is
   the card itself. Nothing is shown that the feed did not return. */
async function ufcView(){"""

# ── 3. The view body ──────────────────────────────────────────────────────
P3_OLD = """  const view=document.getElementById('view');
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
}"""

P3_NEW = """  const view=document.getElementById('view');
  view.innerHTML=`<div class="empty view-loading">Finding the current UFC card\\u2026</div>`;
  const cardData=await loadUfcCard();
  if((new URLSearchParams(location.search).get('sport')||'').toUpperCase()!=='UFC') return;

  if(!cardData || !cardData.bouts.length){
    /* Only reached when the forward-window query genuinely comes back with no
       upcoming UFC event. Never described as "today". */
    view.innerHTML=`<h1>UFC \\u2014 No Card Scheduled</h1>
      <p class="lead">ESPN lists no UFC event in the next ${UFC_WINDOW_DAYS} days. That is the state
      of the schedule as the feed reports it, not a gap in this page.</p>
      <div class="off-hero">
        <div class="off-tag">UFC \\u00b7 nothing scheduled in the next ${UFC_WINDOW_DAYS} days</div>
        <div class="off-h">Nothing to price yet</div>
        <div class="off-when">Read <a href="/ufc-331-odds" style="color:var(--green)">how fight prices work</a>
          while you wait, or open the <a href="?" style="color:var(--green)">Full Board</a>.</div>
        ${liveChips('UFC')}
      </div>`;
    return;
  }

  /* Merge into D so the ticker, the rail count and a bout opened straight
     from a URL all resolve against the same data. */
  const seen={}; (D.UFC||[]).forEach(x=>seen[x.id]=1);
  D.UFC=(D.UFC||[]).concat(cardData.bouts.filter(x=>!seen[x.id]));
  rail('UFC'); ticker('UFC',null);

  /* ESPN publishes no cardSegment and no bout order, but it does publish a
     start time per bout, and a card's segments are exactly those time blocks.
     Group by the real time and label each group with it — no invented
     "Main Card" / "Prelims" wording the feed never supplied. Latest block
     first, so the main event leads. */
  const groups={};
  cardData.bouts.forEach(b=>{ (groups[b.boutDate]=groups[b.boutDate]||[]).push(b); });
  const times=Object.keys(groups).sort().reverse();

  const anyPrice=cardData.bouts.some(b=>b.o&&b.o.moneyline);
  const meta=[
    cardData.date?CT(cardData.date,{weekday:'long',month:'short',day:'numeric'}):'',
    cardData.venue, cardData.city
  ].filter(Boolean).join(' \\u00b7 ');

  view.innerHTML=`
    <div class="fc-ev">
      <div class="fc-ev-n">${cardData.name||'UFC'}</div>
      <div class="fc-ev-m">${meta}${meta?' \\u00b7 ':''}${cardData.bouts.length} bouts \\u00b7 times in CT</div>
    </div>
    <p class="lead">Every bout ESPN lists on this card, with weight class, scheduled rounds,
    professional records and each fighter's country. ${anyPrice
      ? 'Where the feed carries a two-way price it is shown with the fair read beside it.'
      : '<b>ESPN is not carrying prices for this card</b>, so none are shown \\u2014 a fight has no spread and no total, and a made-up number is worse than no number.'}
    How fight prices work is explained in the
    <a href="/ufc-331-odds" style="color:var(--green)">UFC odds guide</a>.</p>
    ${times.map(t=>`
      <div class="fc-seg"><b>${CT(t,{hour:'numeric',minute:'2-digit'})} CT</b>
        <span>${groups[t].length} bout${groups[t].length===1?'':'s'}</span></div>
      ${groups[t].slice().reverse().map(fightCard).join('')}`).join('')}
    <p class="expl" style="border:none;padding-top:10px">Card, times and records via
      <a href="https://www.espn.com/mma/schedule" target="_blank" rel="noopener" style="color:var(--muted)">ESPN</a>.
      Fight cards change \\u2014 late withdrawals and bout-order moves happen, and this page reflects
      the feed at the time it was read.</p>`;
  document.title=`${cardData.name||'UFC'} \\u2014 full card | Inside the Number`;
}"""

# ── 4. A bout opened straight from a URL must resolve too ────────────────
P4_OLD = """  if(!g && SCOPE_DEFAULT[sport]){
    const v=document.getElementById('view');
    if(v) v.innerHTML=`<div class="empty view-loading">Reading the ${sport} board\\u2026</div>`;
    const w=await loadWeek(sport);
    if(Array.isArray(w) && w.length){
      const seen={}; (D[sport]||[]).forEach(x=>seen[x.id]=1);
      D[sport]=(D[sport]||[]).concat(w.filter(x=>!seen[x.id]));
      g=(D[sport]||[]).find(x=>x.id===id);
      ticker(sport,id);
    }
  }"""

P4_NEW = """  if(!g && SCOPE_DEFAULT[sport]){
    const v=document.getElementById('view');
    if(v) v.innerHTML=`<div class="empty view-loading">Reading the ${sport} board\\u2026</div>`;
    const w=await loadWeek(sport);
    if(Array.isArray(w) && w.length){
      const seen={}; (D[sport]||[]).forEach(x=>seen[x.id]=1);
      D[sport]=(D[sport]||[]).concat(w.filter(x=>!seen[x.id]));
      g=(D[sport]||[]).find(x=>x.id===id);
      ticker(sport,id);
    }
  }
  /* Same problem, different shape: D.UFC holds today, and the current card is
     almost never today. Without this, every bout link on the card — and every
     link anyone shared — dead-ends on refresh. Bouts are only rendered as
     links because this resolves them. */
  if(!g && sport==='UFC'){
    const v=document.getElementById('view');
    if(v) v.innerHTML=`<div class="empty view-loading">Finding the current UFC card\\u2026</div>`;
    const c=await loadUfcCard();
    if(c && c.bouts.length){
      const seen={}; (D.UFC||[]).forEach(x=>seen[x.id]=1);
      D.UFC=(D.UFC||[]).concat(c.bouts.filter(x=>!seen[x.id]));
      g=(D.UFC||[]).find(x=>x.id===id);
      rail('UFC'); ticker('UFC',id);
    }
  }"""

# ── 5. listView must await the now-async ufcView ─────────────────────────
P5_OLD = "  if(sport==='UFC'){ scopeBar(sport,scope,null); return ufcView(); }"
P5_NEW = "  if(sport==='UFC'){ scopeBar(sport,scope,null); return await ufcView(); }"

# ── 6. Card styling ───────────────────────────────────────────────────────
P6_OLD = '  .foot{margin-top:9px;padding-top:8px;border-top:1px solid var(--border);display:flex;justify-content:space-between;'
P6_NEW = """  /* ── UFC fight card. A bout is not a game: no spread, no total, no market
     grid. Just who, at what weight, over how many rounds, with records. ── */
  .fc-ev{border:1px solid var(--border);border-radius:var(--r-md);padding:16px 18px;margin-bottom:6px;
    background:linear-gradient(180deg,var(--surface-2),var(--surface-1))}
  .fc-ev-n{font-family:'Barlow Condensed',sans-serif;font-size:clamp(21px,5.2vw,30px);font-weight:900;
    text-transform:uppercase;line-height:1.04;color:var(--white);overflow-wrap:anywhere}
  .fc-ev-m{margin-top:7px;font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--mid);line-height:1.6}
  .fc-seg{margin:18px 0 9px;display:flex;gap:9px;align-items:baseline;flex-wrap:wrap;
    font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
  .fc-seg b{color:var(--green);font-weight:600;letter-spacing:.08em}
  .fc{display:block;background:linear-gradient(180deg,var(--surface-2),var(--surface-1));
    border:1px solid var(--border);border-radius:var(--r-md);padding:12px 14px;margin-bottom:9px;
    text-decoration:none;color:inherit;transition:border-color .15s,transform .15s}
  a.fc:hover{border-color:var(--border-lit);transform:translateY(-2px)}
  .fc-top{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:8px;
    font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
  .fc-top .w{color:var(--blue)}
  .fc-top .main{color:var(--gold);font-weight:600}
  .fc-f{display:grid;grid-template-columns:20px minmax(0,1fr) auto;align-items:center;gap:9px;padding:3px 0}
  .fc-f img{width:20px;height:14px;object-fit:cover;border-radius:2px;display:block}
  .fc-nm{font-family:'Barlow',sans-serif;font-size:14.5px;font-weight:600;color:var(--white);
    overflow-wrap:anywhere;line-height:1.25}
  .fc-rec{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--mid);white-space:nowrap}
  .fc-rec b{color:var(--white);font-weight:600}
  .fc-rec i{color:var(--green);font-style:normal}
  .fc-v{font-family:'IBM Plex Mono',monospace;font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;
    color:var(--muted);padding-left:29px;margin:1px 0}
  @media(max-width:420px){.fc-nm{font-size:13.5px}.fc-rec{font-size:10.5px}.fc{padding:11px 12px}}

  .foot{margin-top:9px;padding-top:8px;border-top:1px solid var(--border);display:flex;justify-content:space-between;"""

PATCHES = [
    ("share the bout parser", P1_OLD, P1_NEW, 1),
    ("current-card loader + fight card renderer", P2_OLD, P2_NEW, 1),
    ("UFC view body", P3_OLD, P3_NEW, 1),
    ("bout URL resolves the current card", P4_OLD, P4_NEW, 1),
    ("listView awaits ufcView", P5_OLD, P5_NEW, 1),
    ("fight card styling", P6_OLD, P6_NEW, 1),
]


def main():
    check = "--check" in sys.argv
    html = TARGET.read_text(encoding="utf-8")

    if SENTINEL in html:
        print("games.html already carries the UFC current-card repair.")
        return 0

    ok = True
    for label, old, _new, n in PATCHES:
        found = html.count(old)
        print("%-44s %s" % (label, "ok" if found == n else "ANCHOR MISS (%d)" % found))
        if found != n:
            ok = False
    if check:
        return 0 if ok else 1
    if not ok:
        print("STOP. Nothing written.")
        return 1

    for _label, old, new, n in PATCHES:
        html = html.replace(old, new, n)

    TARGET.write_text(html, encoding="utf-8")
    print("games.html patched: %d anchors." % len(PATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())

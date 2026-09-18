#!/usr/bin/env python3
"""
Two narrow fixes found in the 390px mobile audit, Sep 18 2026.

A. BLOCKER — a game opened by URL dead-ends.
   gameView() looks the game up in D[sport], which only ever holds TODAY. The
   week window is merged into D by listView(), so a game reached by clicking a
   card works — but a shared link, a refresh, a back-forward or a search result
   never runs listView and lands on "That game isn't on today's board".
   Measured live at 390px on /games?sport=NFL&scope=week&game=401872937.
   Since NFL and CFB now DEFAULT to the week, this breaks the normal path for
   both football boards. Fix: pull the week once and look again before giving
   up, reusing the existing loadWeek() and the same merge listView() does.

B. Duplicate module — two breadcrumbs stacked on every board list view.
   The header carries "Home > Full Board" (60px) and the view printed a second
   "Home > CFB" (17px) 366px below it, saying something different. The H1
   directly underneath already names the sport and the window. Drop the
   in-view copy on list views only; the game-detail crumb stays because it
   carries the matchup, which the header crumb cannot.

Nothing else is touched: no analysis, no guide copy, no market maths.

Usage: python3 scripts/fix_mobile_2026-09-18.py [--check]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "games.html"
SENTINEL = "/* ITN-MOBILE-FIX-2026-09-18 */"

# ── A ─────────────────────────────────────────────────────────────────────
A_OLD = """function gameView(sport,id){
  rail(sport);
  const sb=document.getElementById('board-scope');
  if(sb){sb.innerHTML='';sb.style.display='none';}
  ticker(sport,id);
  const g=(D[sport]||[]).find(x=>x.id===id);
  if(!g){document.getElementById('view').innerHTML=
    `<div class="crumb"><a href="/">Home</a> › <a href="?sport=${sport}">${sport}</a> › <span>Game</span></div>
     <div class="empty">That game isn't on today's board. <a href="?sport=${sport}" style="color:var(--green)">Back to ${sport} →</a></div>`;return}"""

A_NEW = """async function gameView(sport,id){
  """ + SENTINEL + """
  rail(sport);
  const sb=document.getElementById('board-scope');
  if(sb){sb.innerHTML='';sb.style.display='none';}
  ticker(sport,id);
  let g=(D[sport]||[]).find(x=>x.id===id);
  /* D holds today only. A game reached by clicking a card is fine, because
     listView() merged the week in first — but a shared link, a refresh or a
     search result comes straight here, and NFL and CFB now default to the
     week. Without this, every link to a Saturday game answered "that game
     isn't on today's board". Pull the week once and look again. */
  if(!g && SCOPE_DEFAULT[sport]){
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
  if(!g){document.getElementById('view').innerHTML=
    `<div class="crumb"><a href="/">Home</a> › <a href="?sport=${sport}">${sport}</a> › <span>Game</span></div>
     <div class="empty">That game isn't on the ${sport} board right now \\u2014 it may have finished, or the feed may not carry it. <a href="?sport=${sport}" style="color:var(--green)">Back to ${sport} →</a></div>`;return}"""

# ── B ─────────────────────────────────────────────────────────────────────
# The separators live in the file as the literal six characters backslash-u-2-0-3-a
# inside a JS template literal, not as the character itself. Built from chr(92)
# so no editor or quoting layer can silently turn one into the other.
BS = chr(92)
B_OLD = ('      <div class="crumb"><a href="/">Home</a> ' + BS + 'u203a <span>${sport}</span></div>\n'
         '      <h1>${sport} ' + BS + 'u2014 ${scope===\'week\'?"This Week\'s Board":"Today\'s Board"}</h1>')
B_NEW = ('      <h1>${sport} ' + BS + 'u2014 ${scope===\'week\'?"This Week\'s Board":"Today\'s Board"}</h1>')

PATCHES = [
    ("A: game detail falls back to the week window", A_OLD, A_NEW, 1),
    ("B: drop the second breadcrumb on list views", B_OLD, B_NEW, 1),
]


def main():
    check = "--check" in sys.argv
    html = TARGET.read_text(encoding="utf-8")

    if SENTINEL in html:
        print("games.html already carries these fixes — nothing to do.")
        return 0

    for label, old, _new, n in PATCHES:
        found = html.count(old)
        print("%-46s %s" % (label, "ok" if found == n else "ANCHOR MISS (%d)" % found))
        if found != n and not check:
            print("STOP. Nothing written.")
            return 1
    if check:
        return 0

    for _label, old, new, n in PATCHES:
        html = html.replace(old, new, n)

    # gameView is now async; route() must not assume it returns synchronously.
    if "if(game && LEAGUES.some(([l])=>l===sport)) gameView(sport,game);" not in html:
        print("STOP. route() dispatch not in the expected shape. Nothing written.")
        return 1

    TARGET.write_text(html, encoding="utf-8")
    print("games.html patched: %d anchors." % len(PATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())

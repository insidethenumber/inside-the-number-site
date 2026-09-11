# DFS — the weekly build (set Sep 11, 2026)

**Cadence:** every **Friday**, for the **Sunday main slate only**. Site: **DraftKings**.
Chuck's call, Sep 11: one site not two, DK over FD, light push on X + newsletter.
`dfs.html` publicly promises "Published Thursday or Friday, ahead of the Sunday slate" —
this task is what keeps that promise.

## Why DraftKings and not both
DK and FD are different products and a lineup cannot be ported between them:
DK is full PPR with yardage bonuses on a $50,000 cap; FD is half-PPR, no bonuses,
$60,000 cap. Same nine spots (QB, 2 RB, 3 WR, TE, FLEX, DST). Their salary
algorithms are tuned to their own scoring, so pass-catching backs and slot
receivers carry more value on DK, touchdown-dependent players more on FD.
Two cards doubles the build AND the verification pass for no extra readers.

## Where the salaries come from — DK and FD are BLOCKED
DraftKings and FanDuel cannot be reached from this environment by any route:
the sandbox proxy blocks them, and the browser refuses both as gambling sites.
Do not waste a run rediscovering this.

**Use RotoWire's DK optimizer instead** — reachable in the browser, and it carries
salary, position, team, opponent, value AND projected ownership in one table:

    https://www.rotowire.com/daily/nfl/optimizer.php?site=DraftKings

### The extraction, which is not obvious
The player table is **virtualised** — only ~33 rows exist in the DOM at a time, so a
single read returns a tiny, QB-heavy subset and looks like the whole pool. You must
scroll the table's own scroll container and accumulate:

```js
function grab(){return [...document.querySelectorAll('tr')].slice(1).map(r=>{
  const c=[...r.querySelectorAll('td')].map(x=>x.innerText.trim());
  return c.length>10?{n:c[0],pos:c[4],tm:c[5],opp:c[6],sal:c[7],val:c[9],own:c[12]}:null;
}).filter(Boolean);}
// walk up from the table to the ancestor that actually scrolls
let p=document.querySelector('table'),sc=null;
while(p&&p!==document.body){const s=getComputedStyle(p);
  if((s.overflowY==='auto'||s.overflowY==='scroll')&&p.scrollHeight>p.clientHeight+50){sc=p;break;}
  p=p.parentElement;}
const map=new Map(); sc.scrollTop=0; grab().forEach(r=>map.set(r.n+r.tm,r));
for(let i=0;i<60;i++){sc.scrollTop+=sc.clientHeight*0.8;
  await new Promise(r=>setTimeout(r,200)); grab().forEach(r=>map.set(r.n+r.tm,r));}
```
That yields ~420 players. Columns are positional: 0 name, 4 pos, 5 team, 6 opp,
7 salary, 9 value, 12 projected ownership %.

### Filtering to the Sunday main slate
RotoWire defaults to the full-week slate ("Wed-Mon", 16 games). The DK **main slate**
is the **1:00 PM and 4:25 PM ET Sunday windows only** — it excludes Thursday night,
Sunday night and Monday night. Read the game times off the slate strip on the page and
keep only those teams. Week 1 that was 12 games / 24 teams / 319 players.

Salaries are DK's real numbers. They are locked once a slate posts, so if a salary is
wrong the lineup will not fit the cap — verify the total against $50,000 before shipping.

## The ITN angle — do not try to out-project Stokastic
They have projection models, ownership data, optimisers and staff. We do not and will
not. What we have that they do not lead with is **the market**: implied team totals from
the odds we already pull four times a day, plus the ownership column above.

Lead with **where the field is**, not with a projection. Week 1's story wrote itself:
Jahmyr Gibbs was on **62.6%** of lineups, with the next highest at 21.7% — a 3x gap.
That is a fact about the field, it is verifiable, and it is the same editorial voice as
every other number on the site.

## Format (already promised on dfs.html — do not invent a new one)
- 3–4 **core plays** with the reasoning
- the **fades** — popular chalk we are avoiding, and why
- **salary context** and an **ownership read**
- **cash vs GPP** split: which plays travel to which format
Free. Pro adds full builds, leverage and ownership depth.

## Headshots — use them, Chuck asked for this Sep 11
The card must carry player faces, not just names. Pipeline already exists:
`data/headshot_manifest.json` (top-level key per league, e.g. `"nfl"`, array of
`{id,name,team,pos}` where `id` is the ESPN athlete id) → committing a manifest change
auto-triggers `.github/workflows/fetch-headshots.yml` → `assets/headshots/nfl/<id>.png`.
Then build with `python3 scripts/cards.py lineup --league nfl ...` which reads them off disk.
CI-routed because the sandbox cannot reach ESPN's CDN.

**Doctrine limit:** a player's face never appears on a graphic carrying a price, a promo
code, an affiliate link or the word "premium". DFS salaries are facts about the contest
and are fine. Our subscription price next to a face is not.

## Push
Light. One X post with the card image, and a short block in the newsletter. Not a
campaign — DFS is a weekly feature, not the main product.

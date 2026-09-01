#!/usr/bin/env python3
"""
Generate the standalone SEO pages for the five calculators that only lived
inside tools.html.

Why a generator rather than five hand-written files: the pages are identical
apart from a handful of fields, and the ones we already ship
(no-vig / kelly / expected-value) drifted from each other over time. Keeping
the chrome in one place means a nav or footer change is one edit, not five.

The calculator maths here is copied deliberately, function for function, from
the implementations in tools.html. If a formula changes there it has to change
here too -- these pages are a second front door to the same tool, not a
reimplementation with its own opinions.

Run: python3 scripts/build_calc_pages.py
"""

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://insidethenumber.com"

# ---------------------------------------------------------------- shared CSS
# Lifted verbatim from no-vig-calculator.html so the five new pages are
# visually indistinguishable from the three that already exist. The only
# additions are .out.one (single-result layout), .n.pos/.n.neg (the coloured
# result states tools.html uses) and .out .s (the explanatory line under a
# result) -- none of which the two-result no-vig page needed.
CSS = """:root{--bg:#050608;--s1:#0e1116;--s2:#141821;--bd:#1c2129;--green:#00d084;--blue:#3ba7ff;--red:#ff5c5c;--gold:#f0b429;--white:#f0f2f5;--mid:#9ca3af;--muted:#6b7280}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Barlow',system-ui,sans-serif;background:var(--bg);color:var(--white);line-height:1.6}
nav{border-bottom:1px solid var(--bd);padding:0 24px;height:56px;display:flex;align-items:center;justify-content:space-between}
nav a{color:var(--white);text-decoration:none;font-weight:800;font-size:18px;letter-spacing:.04em;text-transform:uppercase}
nav a span{color:var(--green)}
nav .r a{font-size:12px;color:#b6bdc8;font-weight:500;margin-left:18px;letter-spacing:.08em}
.wrap{max-width:680px;margin:0 auto;padding:36px 20px 56px}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--green);letter-spacing:.18em;text-transform:uppercase;margin-bottom:10px}
h1{font-family:'Barlow Condensed',sans-serif;font-size:clamp(30px,5vw,44px);font-weight:900;text-transform:uppercase;line-height:1.02;margin-bottom:8px}
h1 span{color:var(--green)}
.sub{color:var(--mid);font-weight:300;margin-bottom:24px;max-width:58ch}
.tool{background:var(--s1);border:1px solid var(--bd);border-radius:14px;padding:22px;margin-bottom:26px}
label{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--muted);letter-spacing:.12em;text-transform:uppercase;margin:12px 0 5px}
input{width:100%;background:var(--s2);border:1px solid var(--bd);border-radius:8px;color:var(--white);font-family:'IBM Plex Mono',monospace;font-size:16px;padding:10px 12px}
input:focus{outline:none;border-color:var(--green)}
.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.out{background:var(--s2);border:1px solid var(--bd);border-radius:10px;padding:14px;margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:10px;text-align:center}
.out.one{grid-template-columns:1fr}
.out .n{font-family:'IBM Plex Mono',monospace;font-size:22px;color:var(--green);font-weight:600}
.out .n.pos{color:var(--green)}
.out .n.neg{color:var(--red)}
.out .l{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin-top:3px}
.out .s{grid-column:1/-1;font-size:12.5px;color:var(--mid);font-weight:300;line-height:1.5;margin-top:6px;text-align:left}
h2{font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;text-transform:uppercase;margin:26px 0 8px}
p.x{font-size:14px;color:var(--mid);font-weight:300;margin:10px 0;max-width:60ch}
p.x b{color:var(--white)}
p.x a{color:var(--green);text-decoration:none}
.foot{border-top:1px solid var(--bd);margin-top:34px;padding-top:16px;font-size:12px;color:var(--muted)}
.foot a{color:var(--green);text-decoration:none}
@media(max-width:560px){.row{grid-template-columns:1fr}}"""

# Odds helpers, matching tools.html exactly.
HELPERS = """function toDec(am){am=+am;return am>0?1+am/100:1+100/(-am)}
function toProb(am){am=+am;return am>0?100/(am+100):(-am)/((-am)+100)}
function toAm(d){return d>=2?Math.round((d-1)*100):Math.round(-100/(d-1))}
function probToAm(p){return p>=0.5?Math.round(-100*p/(1-p)):Math.round(100*(1-p)/p)}
function sign(n){return n>0?'+'+n:''+n}
function pct(p){return (p*100).toFixed(1)+'%'}
function money(v){return (v<0?'-$':'$')+Math.abs(v).toFixed(2)}
function ok(am){am=+am;return isFinite(am)&&(am<=-100||am>=100)}
function set(id,v){document.getElementById(id).textContent=v}
function setn(id,v,cls){const e=document.getElementById(id);e.textContent=v;e.className='n'+(cls?' '+cls:'')}"""


PAGES = [
    # ------------------------------------------------------------------ vig
    {
        "slug": "vig-calculator",
        "eyebrow": "Tools · Vig & hold",
        "h1_lead": "Vig &amp; Hold",
        "h1_tail": "Calculator",
        "breadcrumb": "Vig & Hold Calculator",
        "title": "Vig Calculator — Work Out the Hold on Any Betting Market | Inside the Number",
        "desc": "Free vig calculator: enter both sides of a market and see exactly what the sportsbook is charging you. Standard two-way markets hold 4-5%.",
        "sub": "Enter both sides of a market. Out comes the sportsbook's cut — the fee you pay on every bet, whether you win or lose.",
        "body": """
    <div class="row">
      <div><label>Side A odds (American)</label><input type="number" id="a" value="-110" step="1"/></div>
      <div><label>Side B odds (American)</label><input type="number" id="b" value="-110" step="1"/></div>
    </div>
    <div class="out one">
      <div><div class="n" id="hold">—</div><div class="l">Book hold on this market</div></div>
      <div class="s" id="note"></div>
    </div>""",
        "js": """function calc(){
  const a=document.getElementById('a').value,b=document.getElementById('b').value;
  if(!ok(a)||!ok(b))return;
  const h=(toProb(a)+toProb(b)-1)*100;
  setn('hold',h.toFixed(2)+'%',h>6?'neg':h<3?'pos':'');
  set('note',h<3?'Sharp price — unusually low margin. Books price this thin when they are confident in the number.'
    :h>6?'Expensive. You are paying well over the standard rate; shop this market elsewhere.'
    :'Around the normal rate for a two-way market.');
}""",
        "copy": [
            ("What the hold actually is",
             "Convert both sides of a market to implied probability and add them up. "
             "A fair market would total 100%. A real one totals more — usually 104-105% "
             "on a two-way line. That surplus is the <b>hold</b>, also called the vig or "
             "juice: the sportsbook's fee, priced into the odds rather than charged as a "
             "commission."),
            ("Why a point or two matters more than it sounds",
             "At -110 on both sides the hold is 4.76%, and you need to win 52.4% of your "
             "bets to break even. Find the same game at -105 and the hold drops to 2.44% "
             "and break-even falls to 51.2%. That 1.2-point difference is larger than the "
             "edge most bettors ever manage to find through handicapping. Paying less is "
             "the most reliable edge available."),
            ("Where to go next",
             "Once you know the hold, strip it out with the "
             "<a href=\"/no-vig-calculator\">no-vig calculator</a> to see the market's "
             "honest price, then check what win rate you actually need with the "
             "<a href=\"/break-even-calculator\">break-even calculator</a>."),
        ],
        "faq": [
            ("What is vig in sports betting?",
             "Vig — also called juice or hold — is the sportsbook's built-in margin: the "
             "amount by which both sides' implied probabilities exceed 100%. At -110/-110 "
             "the two sides total 104.76%, so the hold is 4.76%."),
            ("What is a normal hold percentage?",
             "Standard two-way markets such as sides and totals run about 4-5%. Under 3% is "
             "a sharp price. Over 6% is expensive. Player props and futures are often far "
             "higher, sometimes 15-20% or more."),
            ("How do you calculate the hold on a market?",
             "Convert each side's American odds to implied probability, add them together, "
             "and subtract 100%. For -110 and -110: 52.38% + 52.38% = 104.76%, so the hold "
             "is 4.76% before rounding."),
        ],
    },
    # ----------------------------------------------------------- break-even
    {
        "slug": "break-even-calculator",
        "eyebrow": "Tools · Break-even",
        "h1_lead": "Break-Even",
        "h1_tail": "Win Rate",
        "breadcrumb": "Break-Even Win Rate Calculator",
        "title": "Break-Even Win Rate Calculator — What You Need to Hit | Inside the Number",
        "desc": "Free break-even calculator: enter any American odds and see the win rate you need just to stop losing money. At -110 it's 52.4%.",
        "sub": "Enter a price. Out comes the win rate you need just to break even — the bar every bet has to clear before it makes you a dollar.",
        "body": """
    <label>American odds</label>
    <input type="number" id="o" value="-110" step="1"/>
    <div class="out one">
      <div><div class="n" id="be">—</div><div class="l">Required win rate to break even</div></div>
      <div class="s" id="note"></div>
    </div>""",
        "js": """function calc(){
  const o=document.getElementById('o').value;
  if(!ok(o))return;
  const p=toProb(o);
  set('be',pct(p));
  set('note',`At ${sign(+o)}, you need to win more than ${pct(p)} of these for the bet to be profitable. `
    +`Over 100 bets that is ${(p*100).toFixed(0)} wins just to stand still.`);
}""",
        "copy": [
            ("The number every bet has to clear",
             "Break-even win rate is the implied probability of the price you're taking. "
             "At -110 it's 52.4%. At -150 it's 60%. At +200 it's 33.3%. Below that rate "
             "you lose money over time no matter how good any individual bet felt."),
            ("Why 52.4% is the number people quote",
             "-110 is the standard price on point spreads and totals, so 52.4% became the "
             "benchmark for whether someone can actually bet. It sounds close to a coin "
             "flip, and that's the trap: the gap between 50% and 52.4% is the entire "
             "business model of a sportsbook. Long-term winners typically land in the "
             "53-55% range — a couple of points above break-even, not double digits."),
            ("Reading it the other way",
             "This calculator also answers the reverse question. If you think a team wins "
             "58% of the time, any price with a break-even below 58% is a bet worth making. "
             "That comparison is exactly what the "
             "<a href=\"/edge-calculator\">edge calculator</a> automates, and what "
             "<a href=\"/expected-value-calculator\">expected value</a> turns into dollars."),
        ],
        "faq": [
            ("What win rate do you need to break even at -110?",
             "52.38%. That is the implied probability of -110, so anything below it loses "
             "money over a large enough sample even though it looks like close to a coin flip."),
            ("How do you calculate break-even win rate?",
             "Convert the American odds to implied probability. For negative odds: "
             "odds / (odds + 100). For positive odds: 100 / (odds + 100). The result is the "
             "share of bets you must win to break even."),
            ("Is a 55% win rate good in sports betting?",
             "Yes. At standard -110 pricing, break-even is 52.4%, so 55% is a real and "
             "sustainable edge. Very few bettors hold above 55% over thousands of bets."),
        ],
    },
    # ----------------------------------------------------------------- edge
    {
        "slug": "edge-calculator",
        "eyebrow": "Tools · Edge",
        "h1_lead": "Edge vs the",
        "h1_tail": "Market",
        "breadcrumb": "Edge vs the Market Calculator",
        "title": "Betting Edge Calculator — Your Number vs the True Price | Inside the Number",
        "desc": "Free edge calculator: compare your own win probability against the no-vig market price and see how many points of edge you actually have.",
        "sub": "Enter both sides of the market and your own number. Out comes the gap between what you think and what the market thinks, with the fee stripped out.",
        "body": """
    <div class="row">
      <div><label>Side A odds (American)</label><input type="number" id="a" value="-138" step="1"/></div>
      <div><label>Side B odds (American)</label><input type="number" id="b" value="116" step="1"/></div>
    </div>
    <label>Your probability for side A (%)</label>
    <input type="number" id="p" value="58" step="0.1"/>
    <div class="out one">
      <div><div class="n" id="edge">—</div><div class="l">Your edge over the true price</div></div>
      <div class="s" id="note"></div>
    </div>""",
        "js": """function calc(){
  const a=document.getElementById('a').value,b=document.getElementById('b').value;
  const mine=Number(document.getElementById('p').value)/100;
  if(!ok(a)||!ok(b)||!(mine>=0&&mine<=1))return;
  const ra=toProb(a),rb=toProb(b),s=ra+rb;
  if(!(s>0))return;
  const fair=ra/s,d=mine-fair;
  setn('edge',(d>=0?'+':'')+(d*100).toFixed(1)+' pts',d>=0?'pos':'neg');
  set('note',`Market's true price on A is ${pct(fair)} (${sign(probToAm(fair))}). You have it at ${pct(mine)}. `
    +(d>0?'That gap is your edge — if your number is right.'
         :'No edge here. The market is pricing A higher than you are.'));
}""",
        "copy": [
            ("Compare against the fair price, not the posted one",
             "The mistake that quietly ruins otherwise good handicapping is measuring your "
             "edge against the number on the screen. That number includes the sportsbook's "
             "fee. Beating it by a hair means you're roughly breaking even. This calculator "
             "removes the margin from both sides first, then compares your estimate against "
             "what's left — the market's actual opinion."),
            ("How big an edge is realistic",
             "One to three points is a genuine, workable edge. Five or more usually means "
             "you've found a stale line, or that your model is missing something the market "
             "already knows — an injury, a lineup change, weather. A number far off the "
             "market is a reason to double-check your inputs before it's a reason to bet."),
            ("Edge is only half the decision",
             "Knowing you have an edge doesn't tell you how much to risk. Feed the same "
             "numbers into the <a href=\"/kelly-calculator\">Kelly calculator</a> for "
             "a stake size scaled to the size of the edge, and see the dollar value with "
             "<a href=\"/expected-value-calculator\">expected value</a>."),
        ],
        "faq": [
            ("How do you calculate your edge in sports betting?",
             "Remove the margin from the market by converting both sides to implied "
             "probability and dividing each by their total. Then subtract that fair "
             "probability from your own estimate. The difference, in percentage points, "
             "is your edge."),
            ("What is a good edge in sports betting?",
             "One to three percentage points against the no-vig price is a real edge and "
             "enough to be profitable long term. Anything above five points is more often "
             "a modelling error or stale line than a genuine opportunity."),
            ("Why compare against the no-vig price instead of the posted odds?",
             "The posted price includes the sportsbook's fee, so beating it slightly is not "
             "actually an edge. The no-vig price is the market's honest estimate, which is "
             "the only fair benchmark for your own number."),
        ],
    },
    # ---------------------------------------------------------------- hedge
    {
        "slug": "hedge-calculator",
        "eyebrow": "Tools · Hedge",
        "h1_lead": "Hedge",
        "h1_tail": "Calculator",
        "breadcrumb": "Hedge Calculator",
        "title": "Hedge Calculator — Lock In Profit on a Live Bet | Inside the Number",
        "desc": "Free hedge calculator: enter your original stake and odds plus the current price on the other side to see exactly how much to lay to lock in a result.",
        "sub": "You're holding a live ticket and want to guarantee the outcome. This is how much to put on the other side, and what you keep either way.",
        "body": """
    <div class="row">
      <div><label>Original stake ($)</label><input type="number" id="s" value="100" step="1"/></div>
      <div><label>Original odds</label><input type="number" id="o" value="400" step="1"/></div>
    </div>
    <label>Current odds on the other side</label>
    <input type="number" id="h" value="-200" step="1"/>
    <div class="out">
      <div><div class="n" id="amt">—</div><div class="l">Hedge stake</div></div>
      <div><div class="n" id="profit">—</div><div class="l">Locked either way</div></div>
      <div class="s" id="note"></div>
    </div>""",
        "js": """function calc(){
  const stake=Number(document.getElementById('s').value);
  const o=document.getElementById('o').value,h=document.getElementById('h').value;
  if(!ok(o)||!ok(h)||!isFinite(stake)||stake<=0)return;
  const ret=stake*toDec(o),hd=toDec(h);
  const amt=ret/hd,profit=ret-stake-amt;
  set('amt',money(amt));
  setn('profit',money(profit),profit>=0?'pos':'neg');
  set('note',`Original ticket returns ${money(ret)} if it wins. Staking ${money(amt)} on the other side returns `
    +`${money(amt*hd)}. Either way you finish with ${money(ret-amt)} against ${money(stake+amt)} risked`
    +(profit<0?' — this hedge locks in a loss, it just caps the damage.':'.'));
}""",
        "copy": [
            ("What hedging actually costs you",
             "Hedging converts an uncertain outcome into a certain one, and you pay for that "
             "certainty. The guaranteed amount is always less than the expected value of "
             "simply letting the original bet ride. That isn't an argument against hedging — "
             "it's the price of removing variance, and sometimes that's worth paying."),
            ("When it makes sense",
             "Hedge when the outstanding amount is large relative to your bankroll, when the "
             "other side has moved far enough that the lock is genuinely good, or when losing "
             "the ticket outright would change your behaviour on the next twenty bets. Don't "
             "hedge a small futures ticket purely because watching it is uncomfortable."),
            ("Partial hedges",
             "You don't have to lock the whole thing. Staking half the calculated amount "
             "removes half the variance and keeps half the upside. Run the number here, then "
             "decide how much certainty you actually want to buy — and check the "
             "<a href=\"/bankroll-drawdown-calculator\">drawdown calculator</a> if the "
             "answer depends on what a loss would do to your bankroll."),
        ],
        "faq": [
            ("How do you calculate a hedge bet?",
             "Work out the total return on the original ticket if it wins, then divide that "
             "figure by the decimal odds on the opposite side. The result is the stake that "
             "returns the same amount whichever way the event goes."),
            ("Is hedging a bet always a good idea?",
             "No. Hedging always costs expected value in exchange for certainty. It is worth "
             "it when the amount at stake is large relative to your bankroll, and usually not "
             "worth it on small tickets where the variance does not matter."),
            ("Can you hedge and still lose money?",
             "Yes. If the price on the other side has moved against you, the guaranteed "
             "figure can be less than your total risk. The hedge then caps the loss rather "
             "than locking in a profit."),
        ],
    },
    # ------------------------------------------------------------- drawdown
    {
        "slug": "bankroll-drawdown-calculator",
        "eyebrow": "Tools · Drawdown",
        "h1_lead": "Bankroll",
        "h1_tail": "Drawdown",
        "breadcrumb": "Bankroll Drawdown Calculator",
        "title": "Bankroll Drawdown Calculator — Survive a Losing Streak | Inside the Number",
        "desc": "Free bankroll drawdown calculator: see how far a normal losing run takes your bankroll at any unit size. A 10-bet losing streak is routine.",
        "sub": "Flat staking at a given unit size. This is how far a normal losing run takes you down — and normal is further than most people plan for.",
        "body": """
    <div class="row">
      <div><label>Bankroll ($)</label><input type="number" id="b" value="1000" step="1"/></div>
      <div><label>Unit size (%)</label><input type="number" id="u" value="2" step="0.1"/></div>
    </div>
    <label>Losing streak length</label>
    <input type="number" id="n" value="10" step="1"/>
    <div class="out">
      <div><div class="n" id="left">—</div><div class="l">Bankroll after</div></div>
      <div><div class="n" id="down">—</div><div class="l">Drawdown</div></div>
      <div class="s" id="note"></div>
    </div>""",
        "js": """function calc(){
  const bank=Number(document.getElementById('b').value);
  const unit=Number(document.getElementById('u').value)/100;
  const n=Number(document.getElementById('n').value);
  if(!isFinite(bank)||bank<=0||!(unit>0&&unit<1)||!(n>=0))return;
  const left=bank*Math.pow(1-unit,n);
  set('left',money(left));
  setn('down','-'+((1-left/bank)*100).toFixed(1)+'%','neg');
  set('note',`${n} straight losses at ${(unit*100).toFixed(1)}% of bankroll leaves ${money(left)} of ${money(bank)}. `
    +`A run this long is routine even for a bettor winning 55% long term.`);
}""",
        "copy": [
            ("Losing streaks are longer than people expect",
             "A bettor hitting 55% — a genuinely strong long-term rate — still has better "
             "than a coin-flip chance of dropping ten in a row at some point across a "
             "season. Eight and nine-bet losing runs are unremarkable. The question isn't "
             "whether one arrives, it's whether your unit size lets you still be betting "
             "when it ends."),
            ("Why unit size is the whole game",
             "At 2% units a ten-bet losing run costs about 18% of your bankroll — "
             "unpleasant, survivable. At 10% units the same run costs about 65%, and now "
             "you need to roughly triple what's left just to get back to even. Same "
             "handicapping, same losing streak, completely different outcome. Most bettors "
             "who go broke were right often enough and simply bet too big."),
            ("Sizing to survive",
             "One to three percent per bet is the standard range, and there's nothing "
             "clever about it — it's chosen so that a bad month is a dent rather than the "
             "end. If you'd rather size to the edge on each individual bet, the "
             "<a href=\"/kelly-calculator\">Kelly calculator</a> does that, and "
             "quarter-Kelly usually lands in this same 1-3% neighbourhood."),
        ],
        "faq": [
            ("How long can a losing streak last in sports betting?",
             "Longer than most bettors plan for. Even at a 55% win rate, runs of eight to "
             "ten straight losses occur regularly across a full season. They are variance, "
             "not evidence that a method has stopped working."),
            ("What percentage of bankroll should you bet per game?",
             "One to three percent of your bankroll per bet is the standard range. It is "
             "chosen so that a normal losing streak is survivable rather than fatal."),
            ("How much does a 10-bet losing streak cost?",
             "At 2% units, about 18% of your bankroll. At 5% units, about 40%. At 10% "
             "units, about 65% — which then requires nearly tripling the remainder just to "
             "get back to even."),
        ],
    },
]


def render(p):
    # Extensionless: Cloudflare serves /slug and 301s /slug.html, so the
    # .html form can never be indexed. Advertise what returns 200.
    url = f"{SITE}/{p['slug']}"

    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in p["faq"]
        ],
    }
    # Plain-text names only. The existing no-vig page carries literal <span>
    # tags inside its breadcrumb name, which is invalid for structured data --
    # not repeating that here.
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Tools", "item": f"{SITE}/tools"},
            {"@type": "ListItem", "position": 3, "name": p["breadcrumb"], "item": url},
        ],
    }

    copy = "\n".join(
        f'  <h2>{h}</h2>\n  <p class="x">{body}</p>' for h, body in p["copy"]
    )

    desc = html.escape(p["desc"], quote=True)
    title = html.escape(p["title"], quote=True)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{url}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:site_name" content="Inside the Number"/>
<meta property="og:image" content="{SITE}/og-image.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<script type="application/ld+json">{json.dumps(faq, separators=(', ', ': '))}</script>
<script type="application/ld+json">{json.dumps(crumbs, separators=(', ', ': '))}</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@800;900&family=Barlow:wght@300;400;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
{CSS}
</style>
</head>
<body>
<nav><a href="/">Inside <span>the</span> Number</a>
  <div class="r"><a href="/tools">All tools</a><a href="/games">Today's board</a></div></nav>
<div class="wrap">
  <div class="eyebrow">// {p['eyebrow']}</div>
  <h1>{p['h1_lead']} <span>{p['h1_tail']}</span></h1>
  <p class="sub">{p['sub']}</p>
  <div class="tool">{p['body']}
  </div>
{copy}
  <p class="x">We run these numbers on
  <a href="/games">every game on the board</a>, every day — or see
  <a href="/tools">all ten calculators</a> on one page.</p>
  <div class="foot">Inside the Number · every game priced at what the market really
  thinks · <a href="/">free pick daily</a> · 21+ only. If gambling stops being fun,
  call 1-800-GAMBLER.</div>
</div>
<script>
{HELPERS}
{p['js']}
document.addEventListener('input',calc);calc();
</script>
</body>
</html>
"""


def main():
    for p in PAGES:
        out = ROOT / f"{p['slug']}.html"
        out.write_text(render(p), encoding="utf-8")
        print(f"wrote {out.name} ({len(out.read_text(encoding='utf-8').splitlines())} lines)")


if __name__ == "__main__":
    main()

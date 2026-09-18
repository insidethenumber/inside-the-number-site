#!/usr/bin/env python3
"""
ITN global navigation builder — Phase 1 (Sep 18 2026)
=====================================================

One source of truth for the site header, the mobile menu, the Home > parent >
current context bar, and the board switcher. Run it and every page in PAGES
gets the identical component, rendered into the HTML (not injected at runtime)
so it is crawlable and works with JavaScript off.

Why a build step instead of a runtime include
---------------------------------------------
The site is a set of static files on Cloudflare Pages with no template layer.
Before this, each page carried its own hand-copied <nav>, which is how three
labels drifted into pointing at pages they did not describe. Generating the
markup means the next label change is one edit here, not twelve.

What it rewrites, per page
--------------------------
  1. the contents of the first <nav> ... </nav>          -> generated links
  2. <div class="mobile-page-context"> ... </div>         -> generated crumb
  3. <div class="mobile-menu"> / <div class="compact-mobile-menu">
                                                          -> generated panel
  4. the inline hamburger <script>                        -> shared asset
  5. adds the shared CSS/JS <link>/<script> before </head>

It does NOT touch page copy, board logic, calculators, SEO tags, JSON-LD,
the signup embeds, or the measurement helper.

Usage
-----
    python3 scripts/build_nav.py            # rewrite every page in PAGES
    python3 scripts/build_nav.py --check    # report drift, change nothing
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── The information architecture. This block is the product decision. ──────
# BOARDS  = live market boards. A board label must reach a board.
# LEARN   = explainers. A guide label must reach a guide.
# TOOLS   = the calculators, and the cheat sheet that lives inside one.
BOARDS = [
    ("/games",            "Full Board",       "Every league on one page"),
    ("/games?sport=NFL&scope=week", "NFL", "This week's NFL slate"),
    ("/games?sport=CFB&scope=week", "College Football", "This week's CFB slate"),
    ("/games?sport=MLB&scope=today", "MLB", "Today's MLB board"),
    ("/games?sport=UFC",  "UFC",              "The current card"),
]
LEARN = [
    ("/learn",                     "How to Read the Board", "Start here"),
    ("/football-line-movement",    "Football Guide",        "Why football lines move"),
    ("/mlb-playoffs",              "MLB Playoff Odds",      "Reading October prices"),
    ("/glossary",                  "Glossary",              "Plain-English definitions"),
]
TOOLS = [
    ("/tools",                            "All Calculators", "Ten of them"),
    ("/no-vig-calculator",                "No-Vig Calculator", "Strip out the book's cut"),
    ("/parlay-calculator",                "Parlay Calculator", "What the legs really pay"),
    ("/no-vig-calculator#cheat-sheet",    "No-Vig Cheat Sheet", "The printable one"),
]

# The single call to action. Bare URL on purpose: the site-wide measurement
# helper decorates this exact href with the visitor's first-touch source, so
# adding our own utm_ parameters here would fight it.
CTA_HREF = "https://insidethenumber.beehiiv.com/subscribe"
CTA_TEXT = "Morning Board"
CTA_LONG = "Get the free Morning Board"

# The board switcher, shown on boards and game detail views.
SWITCH = [
    ("/games",           "Full Board"),
    ("/games?sport=NFL&scope=week", "NFL"),
    ("/games?sport=CFB&scope=week", "CFB"),
    ("/games?sport=MLB&scope=today", "MLB"),
    ("/games?sport=UFC", "UFC"),
]

# ── Per-page context. (parent_href, parent_label, current_label) ───────────
# parent_href None means the page sits directly under Home.
PAGES = {
    "index.html": dict(
        route="/", section=None, crumb=None, switcher=False),
    # games.html carries its own league rail, which IS the board switcher.
    "games.html": dict(
        route="/games", section="boards", crumb=(None, None, "Full Board"), switcher=False),
    "nfl.html": dict(
        route="/nfl", section="boards", crumb=("/games", "Full Board", "NFL"), switcher=True),
    "cfb.html": dict(
        route="/cfb", section="boards", crumb=("/games", "Full Board", "College Football"), switcher=True),
    "ufc-331-odds.html": dict(
        route="/ufc-331-odds", section="boards", crumb=("/games", "Full Board", "UFC"), switcher=True),
    # ufc.html is an archived card. Its parent is the current UFC page, not Home,
    # so a visitor who lands on the archive has a route to the live one.
    "ufc.html": dict(
        route="", section="boards", crumb=("/ufc-331-odds", "UFC", "Past Card"), switcher=True),
    "mlb-playoffs.html": dict(
        route="/mlb-playoffs", section="learn", crumb=("/learn", "Learn", "MLB Playoff Odds"), switcher=False),
    # The reported defect: this guide had only "Home" and no parent, while every
    # sibling guide already returned to /learn.
    "football-line-movement.html": dict(
        route="/football-line-movement", section="learn", crumb=("/learn", "Learn", "Football Guide"), switcher=False),
    "learn.html": dict(
        route="/learn", section="learn", crumb=(None, None, "Learn"), switcher=False),
    "tools.html": dict(
        route="/tools", section="tools", crumb=(None, None, "Tools"), switcher=False),
    "no-vig-calculator.html": dict(
        route="/no-vig-calculator", section="tools", crumb=("/tools", "Tools", "No-Vig Calculator"), switcher=False),
    "parlay-calculator.html": dict(
        route="/parlay-calculator", section="tools", crumb=("/tools", "Tools", "Parlay Calculator"), switcher=False),
}

# Which nav item should read as "you are here".
SECTION_LABEL = {"boards": "Boards", "learn": "Learn", "tools": "Tools"}

# ── Truthful labels in page copy ──────────────────────────────────────────
# The nav is only half the problem: body copy called /games "the scores page"
# too. A board is a board. Each entry asserts its own hit count, so a miss is
# loud rather than silent.
#   (filename, old, new, expected occurrences)
LABEL_FIXES = [
    ("index.html",
     '<a href="games" style="color:inherit;text-decoration:underline">scores page</a>',
     '<a href="games" style="color:inherit;text-decoration:underline">Full Board</a>', 2),
    ("index.html", '<a href="games">scores page</a>', '<a href="games">Full Board</a>', 2),
    ("nfl.html",
     'The live multi-sport board is on the <a href="games">scores page</a>.',
     'Every other league is on the <a href="games">Full Board</a>.', 2),
    # Every other page links the brand to "/". This one pointed at a filename,
    # which breaks the moment the route is served without the extension.
    ("ufc.html", '<a class="nav-brand" href="index.html">', '<a class="nav-brand" href="/">', 1),
    # The reported guide defect, in the body as well as the crumb: every sibling
    # explainer ends with a link back to /learn; this one was built outside that
    # family and never got one, so the only way out was Home.
    ("football-line-movement.html",
     '<p class="standfirst">A line is a price,',
     '<p class="standfirst" style="margin-top:2px;font-size:12px;opacity:.7">'
     '<a class="inline" href="learn">&larr; Back to the basics</a></p>\n'
     '    <p class="standfirst">A line is a price,', 1),
]

START = "<!--ITN-NAV:START  generated by scripts/build_nav.py — edit there, not here-->"
END = "<!--ITN-NAV:END-->"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def group_markup(gid, label, items, section, current_section, route):
    here = ' itn-here' if section == current_section else ''
    rows = []
    for href, text, sub in items:
        cur = ' aria-current="page"' if href == route else ''
        rows.append(
            '        <li><a href="%s"%s>%s<span class="itn-sub">%s</span></a></li>'
            % (href, cur, esc(text), esc(sub))
        )
    return (
        '    <li class="itn-group">\n'
        '      <button class="itn-top%s" id="itn-%s-btn" aria-expanded="false" '
        'aria-controls="itn-%s-menu" aria-haspopup="true">%s<span class="itn-chev" aria-hidden="true"></span></button>\n'
        '      <ul class="itn-menu" id="itn-%s-menu" aria-labelledby="itn-%s-btn" hidden>\n'
        '%s\n'
        '      </ul>\n'
        '    </li>'
        % (here, gid, gid, esc(label), gid, gid, "\n".join(rows))
    )


def desktop_links(current_section, route):
    return (
        '  <ul class="itn-links">\n'
        + group_markup("boards", "Boards", BOARDS, "boards", current_section, route) + "\n"
        + group_markup("learn", "Learn", LEARN, "learn", current_section, route) + "\n"
        + group_markup("tools", "Tools", TOOLS, "tools", current_section, route) + "\n"
        + '    <li><a class="itn-cta" href="%s">%s</a></li>\n' % (CTA_HREF, esc(CTA_TEXT))
        + '  </ul>'
    )


def mobile_panel(route):
    def block(head, items):
        rows = []
        for href, text, sub in items:
            cur = ' aria-current="page"' if href == route else ''
            rows.append('      <a href="%s"%s>%s<span class="itn-sub">%s</span></a>'
                        % (href, cur, esc(text), esc(sub)))
        return ('    <div class="itn-m-group">\n'
                '      <div class="itn-m-head">%s</div>\n%s\n    </div>'
                % (esc(head), "\n".join(rows)))

    return (
        '<div class="itn-mobile" id="itnMobileMenu">\n'
        + block("Boards", BOARDS) + "\n"
        + block("Learn", LEARN) + "\n"
        + block("Tools", TOOLS) + "\n"
        + '    <a class="itn-m-cta" href="%s">%s</a>\n' % (CTA_HREF, esc(CTA_LONG))
        + '</div>'
    )


def context_bar(crumb):
    if not crumb:
        return ""
    parent_href, parent_label, current = crumb
    items = ['    <li><a href="/">Home</a></li>']
    if parent_href:
        items.append('    <li><a href="%s">%s</a></li>' % (parent_href, esc(parent_label)))
    items.append('    <li aria-current="page">%s</li>' % esc(current))
    return ('<nav class="itn-ctx" aria-label="Breadcrumb">\n  <ol>\n%s\n  </ol>\n</nav>'
            % "\n".join(items))


def switcher(current_href):
    rows = []
    for href, label in SWITCH:
        cur = ' aria-current="page"' if href == current_href else ''
        rows.append('  <a href="%s"%s>%s</a>' % (href, cur, esc(label)))
    return ('<nav class="itn-switch" aria-label="Switch board">\n'
            '  <span class="itn-switch-lab">Boards</span>\n%s\n</nav>' % "\n".join(rows))


HAMBURGER = (
    '  <button class="nav-hamburger" id="itnMenuButton" aria-label="Menu" '
    'aria-expanded="false" aria-controls="itnMobileMenu">\n'
    '    <span></span><span></span><span></span>\n'
    '  </button>'
)
HAMBURGER_COMPACT = (
    '  <button class="menu-button" id="itnMenuButton" aria-label="Menu" '
    'aria-expanded="false" aria-controls="itnMobileMenu">\n'
    '    <span></span><span></span><span></span>\n'
    '  </button>'
)

HEAD_ASSETS = (
    '<link rel="stylesheet" href="/assets/nav/itn-nav.css">\n'
    '<script defer src="/assets/nav/itn-nav.js"></script>\n'
)

# Which board href each page should mark as current in the switcher.
SWITCH_CURRENT = {
    "nfl.html": "/games?sport=NFL&scope=week",
    "cfb.html": "/games?sport=CFB&scope=week",
    "ufc-331-odds.html": "/games?sport=UFC",
    "ufc.html": "/games?sport=UFC",
}


def rewrite(path: Path, cfg: dict) -> str:
    html = path.read_text(encoding="utf-8")
    original = html
    name = path.name
    section = cfg["section"]
    route = cfg["route"]
    compact = 'class="compact-nav"' in html

    # 0 ── idempotency: a previously generated block is removed first, so the
    #      script can be re-run after a label change without stacking navs.
    html = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\s*', "",
                  html, flags=re.S)
    html = re.sub(r'\s*<ul class="itn-links">.*?</ul>\s*<button [^>]*id="itnMenuButton".*?</button>',
                  "", html, count=1, flags=re.S)

    # 1 ── the link row inside the existing <nav> shell ────────────────────
    #     The brand block and the bar's own styling are left exactly alone.
    links = desktop_links(section, route)
    ham = HAMBURGER_COMPACT if compact else HAMBURGER

    payload = "\n" + links + "\n" + ham + "\n"
    if compact:
        html, n = re.subn(
            r'<div class="desktop-links">.*?</div>\s*<button class="menu-button".*?</button>\s*',
            lambda m: payload, html, count=1, flags=re.S)
    else:
        html, n = re.subn(
            r'\s*<ul class="nav-links">.*?</ul>\s*<button class="nav-hamburger".*?</button>\s*',
            lambda m: payload, html, count=1, flags=re.S)
    if not n:
        # Already converted on a previous run: step 0 stripped the old row, so
        # put the fresh one back in the same place, just inside the nav shell.
        html = re.sub(r'</nav>', lambda m: payload + '</nav>', html, count=1)

    # 2 ── the old mobile-only context strip -> generated crumb ────────────
    crumb = context_bar(cfg["crumb"])
    sw = switcher(SWITCH_CURRENT.get(name, "")) if cfg["switcher"] else ""
    block = "\n".join(x for x in [START, crumb, sw, mobile_panel(route), END] if x)

    html = re.sub(r'<div class="mobile-page-context">.*?</div>\s*', "", html, flags=re.S)

    # 3 ── the old mobile menus ────────────────────────────────────────────
    html = re.sub(r'<div class="mobile-menu" id="mobileMenu">.*?</div>\s*', "",
                  html, flags=re.S)
    html = re.sub(r'<div class="compact-mobile-menu" id="compactMobileMenu">.*?</div>\s*', "",
                  html, flags=re.S)

    # 4 ── the inline hamburger scripts ────────────────────────────────────
    html = re.sub(r'<script>(?:(?!</script>).)*?navHamburger(?:(?!</script>).)*?</script>\s*',
                  "", html, flags=re.S)
    html = re.sub(r'<script>(?:(?!</script>).)*?compactMenuButton(?:(?!</script>).)*?</script>\s*',
                  "", html, flags=re.S)

    # 5 ── drop the generated block straight after the nav bar ─────────────
    #     A lambda, not a replacement string: the block contains ampersands,
    #     backslashes and \g-looking sequences that re would try to expand.
    html = re.sub(r'</nav>', lambda m: '</nav>\n' + block, html, count=1)

    # 6 ── shared assets in <head> ─────────────────────────────────────────
    if "/assets/nav/itn-nav.css" not in html:
        html = html.replace("</head>", HEAD_ASSETS + "</head>", 1)

    if html != original:
        path.write_text(html, encoding="utf-8")
    return "changed" if html != original else "unchanged"


def apply_label_fixes():
    """Relabel visible links whose text did not describe their destination."""
    for name, old, new, expected in LABEL_FIXES:
        p = ROOT / name
        if not p.exists():
            print("  LABEL  %-26s MISSING FILE" % name)
            continue
        html = p.read_text(encoding="utf-8")
        found = html.count(old)
        if found == 0 and html.count(new):
            print("  LABEL  %-26s already applied" % name)
            continue
        if found != expected:
            print("  LABEL  %-26s EXPECTED %d, FOUND %d — skipped, fix by hand"
                  % (name, expected, found))
            continue
        p.write_text(html.replace(old, new), encoding="utf-8")
        print("  LABEL  %-26s %d replaced" % (name, found))


def main():
    check = "--check" in sys.argv
    for name, cfg in PAGES.items():
        p = ROOT / name
        if not p.exists():
            print("MISSING %s" % name)
            continue
        if check:
            html = p.read_text(encoding="utf-8")
            ok = START in html and "/assets/nav/itn-nav.css" in html
            print("%-32s %s" % (name, "ok" if ok else "NOT BUILT"))
        else:
            print("%-32s %s" % (name, rewrite(p, cfg)))
    if not check:
        apply_label_fixes()


if __name__ == "__main__":
    main()

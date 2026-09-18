#!/usr/bin/env python3
"""
Repoint active "current UFC card" links from the dated /ufc-331-odds route to
the rolling /games?sport=UFC board. Sep 18 2026.

/ufc-331-odds is a good explainer and STAYS — it keeps its page, its content
and its place under Learn. What it must stop doing is impersonating the live
card. Two kinds of link are changed:

  1. Twenty-two pages still carry the pre-Phase-1 nav, where the bare label
     "UFC" (and "UFC 331" in the mobile drawer) points at the dated article.
     A visitor reading that nav has no way to know the card is over. Only the
     UFC entry is touched here; rebuilding those navs wholesale is a separate
     job and is not attempted in a focused UFC repair.
  2. ufc.html's own "Next card:" pointer, which is the single most explicit
     "this is what's on next" claim on the site.

Left alone on purpose — these describe the article as an article:
  index.html "UFC 331 odds explained" guide card,
  tools.html and no-vig-calculator.html body references,
  games.html's related-reading strip,
  the page's own canonical/OG/JSON-LD.

Usage: python3 scripts/fix_ufc_links.py [--check]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOARD = "/games?sport=UFC"

# (old, new, why) applied to every page that still carries the legacy nav
NAV_SWAPS = [
    ('<a href="ufc-331-odds">UFC</a>', '<a href="%s">UFC</a>' % BOARD),
    ('<a href="/ufc-331-odds">UFC</a>', '<a href="%s">UFC</a>' % BOARD),
    ('<a href="ufc-331-odds">UFC 331</a>', '<a href="%s">UFC</a>' % BOARD),
    ('<a href="/ufc-331-odds">UFC 331</a>', '<a href="%s">UFC</a>' % BOARD),
]

# One-off links whose text claims the dated page is what is on next.
ONE_OFFS = [
    ("ufc.html",
     '<div class="stamp" style="border-left:3px solid #00d084;padding-left:12px">'
     '<b style="color:#f0f2f5">Next card:</b> <a href="ufc-331-odds">UFC 331 odds '
     '&mdash; how to read Van vs Pantoja 2</a>.</div>',
     '<div class="stamp" style="border-left:3px solid #00d084;padding-left:12px">'
     '<b style="color:#f0f2f5">Next card:</b> <a href="%s">the current UFC card, '
     'live from the schedule</a> &middot; <a href="ufc-331-odds">how to read fight '
     'prices</a>.</div>' % BOARD),
]


def main():
    check = "--check" in sys.argv
    changed = total = 0

    for p in sorted(ROOT.glob("*.html")):
        if " 2.html" in p.name or " 3.html" in p.name:
            continue                      # never touch the user's copies
        if p.name == "ufc-331-odds.html":
            continue                      # the article keeps its own links
        html = p.read_text(encoding="utf-8")
        orig = html
        for old, new in NAV_SWAPS:
            if old in html:
                total += html.count(old)
                html = html.replace(old, new)
        for name, old, new in ONE_OFFS:
            if p.name == name and old in html:
                total += 1
                html = html.replace(old, new, 1)
        if html != orig:
            changed += 1
            print("  %-34s %s" % (p.name, "would change" if check else "updated"))
            if not check:
                p.write_text(html, encoding="utf-8")

    print("%d page(s), %d link(s)%s" % (changed, total, " — check only" if check else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

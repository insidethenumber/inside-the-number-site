#!/usr/bin/env python3
"""
Align every URL we publish with the URL the site actually serves.

The problem this fixes
----------------------
Cloudflare Workers static assets serve /page for /page.html and 301-redirect
/page.html -> /page. That is Cloudflare's default html_handling and it is fine
on its own -- but every canonical tag, og:url, JSON-LD item and sitemap entry
on this site pointed at the .html form.

So Google would read sitemap.xml, request /tools.html, receive a 301, and file
the URL under "Page with redirect" rather than indexing it. Search Console
showed 183 not-indexed pages, of which 97 were "Page with redirect" and 72
"Alternate page with proper canonical tag" -- 169 of 183 explained by this one
mismatch.

The fix is to advertise the URL that actually returns 200: the extensionless
one. Nothing about the server changes; only what we claim our URLs are.

Scope: canonical, og:url, JSON-LD "item", internal hrefs, and both sitemaps.
index.html is special-cased to "/" rather than "/index".

Run: python3 scripts/fix_canonical_urls.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://insidethenumber.com"


def strip_ext(path: str) -> str:
    """/tools.html -> /tools ; /index.html -> / ; leaves everything else alone."""
    if not path.endswith(".html"):
        return path
    base = path[: -len(".html")]
    if base.endswith("/index") or base == "/index":
        return base[: -len("index")] or "/"
    return base


def fix_absolute(text: str) -> str:
    """Rewrite https://insidethenumber.com/....html in any attribute or JSON value."""
    def repl(m):
        return SITE + strip_ext(m.group(1))
    return re.sub(re.escape(SITE) + r"(/[^\s\"'<>]*?\.html)", repl, text)


def fix_hrefs(text: str) -> str:
    """Rewrite href="/foo.html" and href="foo.html" (relative, same-site only)."""
    def repl(m):
        quote, url = m.group(1), m.group(2)
        if url.startswith(("http://", "https://", "//", "mailto:", "#")):
            return m.group(0)
        # Relative links inside /g/ point at siblings; strip_ext wants a leading
        # slash to reason about index.html, so normalise then put it back.
        lead = "" if url.startswith("/") else "REL"
        norm = url if url.startswith("/") else "/" + url
        out = strip_ext(norm)
        if lead == "REL":
            out = out.lstrip("/")
        return f'href={quote}{out}{quote}'
    return re.sub(r'href=(["\'])([^"\']*?\.html)\1', repl, text)


def main():
    changed = []

    # ---- HTML files: root + per-game pages -------------------------------
    for f in sorted(list(ROOT.glob("*.html")) + list((ROOT / "g").glob("*.html"))):
        s = orig = f.read_text(encoding="utf-8")
        s = fix_absolute(s)
        s = fix_hrefs(s)
        if s != orig:
            f.write_text(s, encoding="utf-8")
            changed.append(f.relative_to(ROOT).as_posix())

    # ---- Sitemaps --------------------------------------------------------
    for name in ["sitemap.xml", "g/sitemap-games.xml"]:
        p = ROOT / name
        if not p.exists():
            continue
        s = orig = p.read_text(encoding="utf-8")
        s = fix_absolute(s)
        if s != orig:
            p.write_text(s, encoding="utf-8")
            changed.append(name)

    print(f"rewrote {len(changed)} files")
    for c in changed[:12]:
        print("  ", c)
    if len(changed) > 12:
        print(f"   ... and {len(changed)-12} more")


if __name__ == "__main__":
    main()

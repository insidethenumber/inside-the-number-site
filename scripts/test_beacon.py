#!/usr/bin/env python3
"""Offline guard for the Cloudflare Web Analytics beacon.

Why this exists, separately from smoke.py:

smoke.py already checks the beacon, but only against the LIVE site, which means
it can only fail *after* a bad deploy. On Sep 25 2026 build_ufc_page.py
regenerated ufc.html without the beacon; UFC traffic went uncounted for three
days. A second page, weekly-football-odds.html, had never carried the beacon at
all and was not even in smoke.py's PAGES list, so nothing was watching it.

Both failure modes are visible in the repo without a network call. This test
catches them at commit time:

  1. Every route in sitemap.xml resolves to a file carrying the beacon exactly
     once. Miss it, or duplicate it, and this fails.
  2. build_ufc_page.py -- which writes a whole page from scratch -- emits the
     beacon into its template. A generated page silently drops anything the
     generator does not know to include, so the generator is checked directly
     rather than its output.

Run: python3 scripts/test_beacon.py
Exits non-zero with a specific message on failure.
"""
from __future__ import annotations

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEACON_SRC = "static.cloudflareinsights.com/beacon.min.js"
BEACON_TOKEN = "bfd50abb734b41edb7863a58e69fbfd8"
# First-touch source capture. A page without this is invisible to UTM
# attribution even though its beacon reports the pageview -- so social and
# search traffic to it cannot be told apart. Guarded for the same reason as
# the beacon: the generated pages lose it on every rebuild otherwise.
UTM_HELPER = "itn_utm"

# Generated pages: checked at the generator, not the artifact, because the
# artifact on disk may be stale or absent between builds.
# generator source -> (artifact it writes, placeholder its template must use)
#
# Checking only that the beacon string appears somewhere in the generator is
# NOT enough: the constant can still be defined while the template stops
# interpolating it, which is a silent regression that looks identical on disk.
# So we assert the placeholder is actually present in the emitted template too.
GENERATORS = {
    "scripts/build_ufc_page.py": ("ufc.html", "{ANALYTICS_BEACON}"),
    "scripts/build_weekly_hub.py": ("weekly-football-odds.html", "{ANALYTICS_BEACON}"),
}


def read(path):
    with io.open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def sitemap_routes():
    xml = read("sitemap.xml")
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    return [u.replace("https://insidethenumber.com", "") or "/" for u in locs]


def route_to_file(route):
    """Map a public route to the file that serves it."""
    if route == "/":
        return "index.html"
    name = route.strip("/")
    for candidate in (name + ".html", os.path.join(name, "index.html")):
        if os.path.exists(os.path.join(ROOT, candidate)):
            return candidate
    return None


def main():
    failures = []
    checked = 0
    generated = set(GENERATORS.values())

    for route in sitemap_routes():
        path = route_to_file(route)
        if path is None:
            failures.append("[route] %s has no file behind it" % route)
            continue
        if path in generated:
            # Covered by the generator check below; the on-disk copy may be
            # stale between builds and a false failure here teaches nothing.
            continue
        page = read(path)
        n = page.count(BEACON_SRC)
        checked += 1
        if UTM_HELPER not in page:
            failures.append(
                "[utm] %s (%s) has no first-touch source helper -- tagged "
                "traffic to this page cannot be attributed" % (path, route))
        if n == 0:
            failures.append(
                "[beacon] %s (%s) has no Cloudflare beacon -- traffic to this "
                "page is not being counted" % (path, route))
        elif n > 1:
            failures.append(
                "[beacon] %s (%s) loads the beacon %dx -- page views will be "
                "double counted" % (path, route, n))

    for gen, (artifact, placeholder) in GENERATORS.items():
        src = read(gen)
        if placeholder not in src:
            failures.append(
                "[generator] %s no longer interpolates %s into its template, "
                "so %s will be written without the beacon even though the "
                "constant is still defined" % (gen, placeholder, artifact))
        if BEACON_SRC not in src:
            failures.append(
                "[generator] %s does not emit the beacon, so every rebuild of "
                "%s drops it (this is exactly what happened Sep 25)"
                % (gen, artifact))
        if UTM_HELPER not in src:
            failures.append(
                "[utm] %s does not emit the first-touch source helper, so "
                "%s loses UTM attribution on every rebuild" % (gen, artifact))
        if BEACON_TOKEN not in src:
            failures.append(
                "[generator] %s does not carry the analytics token %s -- the "
                "beacon it emits would not report to us" % (gen, BEACON_TOKEN))
        checked += 1

    if failures:
        print("FAIL -- %d problem(s) across %d checks:" % (len(failures), checked))
        for f in failures:
            print("  %s" % f)
        return 1

    print("ok -- beacon present exactly once across %d checks" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Canonical ITN mark renderer.

Single source of truth for the badge so every raster asset comes from the same
geometry as the inline SVG in the site's nav. The coordinates below match the
SVG's 120x120 viewBox exactly.

Colour scheme is variant D, chosen Aug 24 2026: the N's upstroke runs white
from the base and turns deep green (#007a4d) toward the arrowhead. It replaces
a version whose base was --red (#ff5c5c), which read as pink at small sizes.
"""

from PIL import Image, ImageDraw

BLACK      = (5, 6, 8)
BORDER_LIT = (46, 52, 62)
WHITE      = (240, 242, 245)
GREEN_DEEP = (0, 122, 77)          # --green-deep

# Gradient along the upstroke: 0 = bottom (y=84), 1 = top (y=26)
STOPS = [(0.00, WHITE), (0.35, WHITE), (1.00, GREEN_DEEP)]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _grad_at(t):
    t = max(0.0, min(1.0, t))
    for i in range(len(STOPS) - 1):
        o0, c0 = STOPS[i]
        o1, c1 = STOPS[i + 1]
        if o0 <= t <= o1:
            return _lerp(c0, c1, (t - o0) / ((o1 - o0) or 1e-9))
    return STOPS[-1][1]


# Optical centring, on the LETTERFORMS rather than the full ink bounding box.
#
# First attempt centred the bbox including the arrowhead. Because the arrow
# projects up and to the right, that pushed the heavy ITN letters down and to
# the left — measured on the live X avatar as 4px left and 16px low at 400px.
# The eye centres on the letter mass, not on a thin accent, so the block
# x 24..111.5 / y 38..84 is what gets centred and the arrowhead overhangs.
DX, DY = -7.75, -1.0


def render_badge(px, supersample=4):
    """Return an RGB image of the badge, px by px, rendered with antialiasing."""
    S = px * supersample
    K = S / 120.0
    def X(v): return (v + DX) * K
    def Y(v): return (v + DY) * K

    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)

    # Badge frame is NOT offset — only the glyphs move inside it.
    d.rounded_rectangle([1 * K, 1 * K, 119 * K, 119 * K], radius=18 * K,
                        fill=BLACK, outline=BORDER_LIT, width=max(1, int(2 * K)))

    # I, T, and the N's left stroke and diagonal — solid white
    d.rectangle([X(24), Y(38), X(34), Y(84)], fill=WHITE)
    d.rectangle([X(42), Y(38), X(72), Y(48)], fill=WHITE)
    d.rectangle([X(52), Y(38), X(62), Y(84)], fill=WHITE)
    d.rectangle([X(80), Y(38), X(90), Y(84)], fill=WHITE)
    d.polygon([(X(80), Y(38)), (X(90), Y(38)),
               (X(111.5), Y(84)), (X(101.5), Y(84))], fill=WHITE)

    # Upstroke + arrowhead share one continuous gradient, as in the SVG
    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([X(101.5), Y(34), X(111.5), Y(84)], fill=255)
    md.polygon([(X(106.5), Y(26)), (X(114.5), Y(34)), (X(98.5), Y(34))], fill=255)

    grad = Image.new("RGB", (S, S))
    gd = ImageDraw.Draw(grad)
    y0, y1 = Y(84), Y(26)
    for py in range(S):
        gd.line([(0, py), (S, py)], fill=_grad_at((y0 - py) / (y0 - y1)))
    img.paste(grad, (0, 0), mask)

    return img.resize((px, px), Image.LANCZOS)


if __name__ == "__main__":
    render_badge(512).save("/tmp/itn-badge-preview.png")
    print("wrote /tmp/itn-badge-preview.png")

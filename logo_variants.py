#!/usr/bin/env python3
"""
ITN mark — colour variants for review.

Reproduces the SVG geometry from index.html exactly (same coordinates on a
120x120 viewBox) so a mockup is a true preview of what the site would render,
not a redraw. Only the gradient on the N's upstroke and arrowhead changes.

The current mark runs red at the bottom of that stroke. At small sizes and on
a dark field it reads pink rather than red, which is the complaint.

    python3 logo_variants.py     # writes social/logo-variants/
"""

import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "social", "logo-variants")

S = 1024                    # render size; viewBox is 120x120
K = S / 120.0               # scale factor

BLACK      = (5, 6, 8)
BORDER_LIT = (46, 52, 62)
WHITE      = (240, 242, 245)

# Candidate greens, light to deep
GREEN_STD  = (0, 208, 132)  # --green, current
GREEN_MID  = (0, 179, 113)
GREEN_DARK = (0, 145, 92)
GREEN_DEEP = (0, 122, 77)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grad_at(stops, t):
    """stops: [(offset 0..1, colour)] where 0 = bottom of the stroke."""
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        o0, c0 = stops[i]
        o1, c1 = stops[i + 1]
        if o0 <= t <= o1:
            span = (o1 - o0) or 1e-9
            return lerp(c0, c1, (t - o0) / span)
    return stops[-1][1]


def draw_gradient_shapes(img, shapes, stops, y_bottom=84.0, y_top=26.0):
    """
    Paint `shapes` with a vertical gradient mapped to the SVG's own gradient
    axis: y=84 is offset 0, y=26 is offset 1. Done by building a mask of the
    shapes and compositing a gradient image through it, so the gradient runs
    continuously across the stroke AND the arrowhead — as it does in the SVG.
    """
    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    for kind, pts in shapes:
        scaled = [(x * K, y * K) for x, y in pts]
        if kind == "rect":
            md.rectangle([scaled[0], scaled[1]], fill=255)
        else:
            md.polygon(scaled, fill=255)

    grad = Image.new("RGB", (S, S))
    gd = ImageDraw.Draw(grad)
    y0, y1 = y_bottom * K, y_top * K
    for py in range(S):
        t = (y0 - py) / (y0 - y1)
        gd.line([(0, py), (S, py)], fill=grad_at(stops, t))

    img.paste(grad, (0, 0), mask)


def render(stops, arrow_solid=None):
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)

    # Rounded panel + lit border
    d.rounded_rectangle([1 * K, 1 * K, 119 * K, 119 * K], radius=18 * K,
                        fill=BLACK, outline=BORDER_LIT, width=max(2, int(2 * K)))

    # I, T, and the N's left stroke + diagonal — always solid white
    d.rectangle([24 * K, 38 * K, 34 * K, 84 * K], fill=WHITE)          # I
    d.rectangle([42 * K, 38 * K, 72 * K, 48 * K], fill=WHITE)          # T bar
    d.rectangle([52 * K, 38 * K, 62 * K, 84 * K], fill=WHITE)          # T stem
    d.rectangle([80 * K, 38 * K, 90 * K, 84 * K], fill=WHITE)          # N left
    d.polygon([(80 * K, 38 * K), (90 * K, 38 * K),
               (111.5 * K, 84 * K), (101.5 * K, 84 * K)], fill=WHITE)  # N diagonal

    upstroke = [("rect", [(101.5, 34), (111.5, 84)])]
    head     = [("poly", [(106.5, 26), (114.5, 34), (98.5, 34)])]

    if arrow_solid:
        # Stroke stays white; only the arrowhead carries colour.
        d.rectangle([101.5 * K, 34 * K, 111.5 * K, 84 * K], fill=WHITE)
        d.polygon([(106.5 * K, 26 * K), (114.5 * K, 34 * K), (98.5 * K, 34 * K)],
                  fill=arrow_solid)
    else:
        draw_gradient_shapes(img, upstroke + head, stops)

    return img


VARIANTS = [
    ("A-current",
     "Current — red at the base",
     [(0.00, (255, 92, 92)), (0.15, WHITE), (0.60, WHITE), (1.00, GREEN_STD)], None),

    ("B-white-base-std-green",
     "White base, standard green tip",
     [(0.00, WHITE), (0.55, WHITE), (1.00, GREEN_STD)], None),

    ("C-white-base-dark-green",
     "White base, darker green tip",
     [(0.00, WHITE), (0.55, WHITE), (1.00, GREEN_DARK)], None),

    ("D-white-base-deep-green",
     "White base, deep green, more coverage",
     [(0.00, WHITE), (0.35, WHITE), (1.00, GREEN_DEEP)], None),

    ("E-hard-two-tone",
     "Hard split — white then solid green, no blend",
     [(0.00, WHITE), (0.62, WHITE), (0.63, GREEN_MID), (1.00, GREEN_MID)], None),

    ("F-green-head-only",
     "White stroke, solid green arrowhead only",
     None, GREEN_MID),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, _label, stops, solid in VARIANTS:
        img = render(stops, solid)
        img.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, name + ".png"),
                                                   "PNG", optimize=True)
        print("wrote", name + ".png")

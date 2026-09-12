#!/usr/bin/env python3
"""
Phone-first Reels generator.

WHY THIS EXISTS (Sep 12, 2026). Our first four Reels were desktop information
graphics rendered vertically: odds tables, salary grids, small type, several
ideas per frame. On a muted feed at thumb-scrolling speed none of it is legible
in the half-second you get. Account sat at 2 followers.

The fix is not "nicer design". It is a different unit of content:

  ONE number, enormous, legible at arm's length in under a second.
  Motion in frame one, because a static frame reads as an ad and gets flicked.
  Three beats, six to eight seconds, then stop.
  Nothing inside Instagram's UI overlay — bottom 330px, right 150px.

Usage:
  python3 scripts/reels.py --spec reel.json --out posts/860-name.mp4
"""
import argparse, json, os, subprocess, tempfile, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
SAFE_BOTTOM, SAFE_RIGHT = 330, 150      # Instagram chrome
BG, INK, GREEN, DIM, RED = "#05070a", "#ffffff", "#1dd682", "#8a93a0", "#ff5b5b"
FONTS = "assets/fonts"

def f(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

def center(d, y, text, font, fill, max_w=W - 120):
    """Draw horizontally centred, shrinking to fit. Returns bottom y."""
    size = font.size
    while size > 24:
        ft = ImageFont.truetype(font.path, size)
        w = d.textbbox((0, 0), text, font=ft)[2]
        if w <= max_w:
            break
        size -= 6
    ft = ImageFont.truetype(font.path, size)
    b = d.textbbox((0, 0), text, font=ft)
    d.text(((W - b[2]) / 2, y), text, font=ft, fill=fill)
    return y + b[3] + 10

def wrap(d, y, text, font, fill, max_w=W - 150, lead=1.25):
    words, line = text.split(), ""
    for word in words:
        trial = (line + " " + word).strip()
        if d.textbbox((0, 0), trial, font=font)[2] > max_w and line:
            y = center(d, y, line, font, fill); y += int(font.size * (lead - 1))
            line = word
        else:
            line = trial
    if line:
        y = center(d, y, line, font, fill)
    return y

def ease(t):                       # easeOutCubic
    return 1 - (1 - t) ** 3

def frame(beat, p, spec):
    """p is 0..1 progress within this beat."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    top = 300                                     # clear of the top UI

    # a thin brand rule, always
    d.rectangle([0, 0, W, 10], fill=GREEN)
    center(d, 120, spec.get("kicker", "INSIDE THE NUMBER"), f("BarlowCondensed-Bold.ttf", 44), DIM)

    if beat == 0:
        # THE NUMBER. Counts up, then holds. This is the whole hook.
        target = spec["number"]
        shown = spec.get("number_from", target)
        try:
            a, b = float(str(shown).lstrip("+-")), float(str(target).lstrip("+-"))
            cur = a + (b - a) * ease(min(p * 1.8, 1))
            sign = "-" if str(target).startswith("-") else ("+" if str(target).startswith("+") else "")
            txt = f"{sign}{cur:.1f}".rstrip("0").rstrip(".") if "." in str(target) else f"{sign}{cur:.0f}"
        except ValueError:
            txt = str(target)
        y = center(d, top + 120, txt, f("Anton-Regular.ttf", 520), GREEN)
        if p > 0.55:
            wrap(d, y + 60, spec["number_label"], f("BarlowCondensed-Bold.ttf", 92), INK)

    elif beat == 1:
        y = center(d, top, spec["turn_top"], f("BarlowCondensed-Bold.ttf", 84), DIM)
        y = center(d, y + 40, spec["turn_big"], f("Anton-Regular.ttf", 300),
                   RED if spec.get("turn_bad") else GREEN)
        if p > 0.35:
            wrap(d, y + 50, spec["turn_body"], f("BarlowCondensed-SemiBold.ttf", 78), INK)

    else:
        y = wrap(d, top + 80, spec["payoff"], f("BarlowCondensed-Bold.ttf", 104), INK)
        if p > 0.4:
            center(d, y + 90, "insidethenumber.com", f("BarlowCondensed-Bold.ttf", 66), GREEN)

    return img

def build(spec, out):
    beats = spec.get("beats", [2.6, 2.6, 2.4])
    with tempfile.TemporaryDirectory() as tmp:
        n = 0
        for i, secs in enumerate(beats):
            total = int(secs * FPS)
            for k in range(total):
                frame(i, k / max(total - 1, 1), spec).save(f"{tmp}/{n:05d}.png")
                n += 1
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
             "-i", f"{tmp}/%05d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-profile:v", "high", "-crf", "20", "-movflags", "+faststart", out],
            check=True)
    dur = sum(beats)
    print(f"OK  {out}  {dur:.1f}s  {os.path.getsize(out)/1024:.0f}KB")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    build(json.load(open(a.spec)), a.out)

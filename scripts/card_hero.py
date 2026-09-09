"""
Answer to "why can't you do that in 45 seconds" — the layout, built the honest way.

Same composition as the Gemini mock: a real photograph, a title band, four glass
panels of numbers, a footer with the handle. The difference is that every number
on this one came from ESPN this morning and the photo is a licensed file we can
legally publish, so nothing here has to be walked back later.
"""
import sys, os, json
sys.path.insert(0, "/tmp/w4/scripts")
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import cards as C

W, H = 1600, 900
ROOT = "/tmp/w4"
PH = os.path.join(ROOT, "assets", "photos")

# --- background: real photo, darkened so type reads -------------------------
bg = Image.open(os.path.join(PH, "lumen-field-seahawk-stadium.jpg")).convert("RGB")
r = max(W / bg.width, H / bg.height)
bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1), Image.LANCZOS)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2,
              (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
bg = ImageEnhance.Color(bg).enhance(0.72)
bg = bg.filter(ImageFilter.GaussianBlur(2.5))
dark = Image.new("RGB", (W, H), "#05070b")
bg = Image.blend(bg, dark, 0.62)

img = bg
d = ImageDraw.Draw(img, "RGBA")


def panel(x, y, w, h, radius=18, fill=(10, 13, 19, 214), border=(58, 68, 84, 255)):
    d.rounded_rectangle([x, y, x + w, y + h], radius, fill=fill, outline=border, width=2)


def txt(x, y, s, font, fill, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


# --- title band -------------------------------------------------------------
d.rectangle([0, 0, W, 104], fill=(5, 7, 11, 232))
txt(W // 2, 30, "PATRIOTS AT SEAHAWKS: INSIDE THE NUMBER", C.D(52), C.WHITE, "ma")
d.rectangle([0, 102, W, 105], fill=C.GREEN)

# --- centre: the pick -------------------------------------------------------
CX = W // 2
panel(CX - 250, 300, 500, 300, radius=22, fill=(6, 9, 14, 232), border=(0, 208, 132, 255))
txt(CX, 328, "THE PICK", C.B(24), C.GREEN, "ma")
txt(CX, 372, "NEW ENGLAND", C.D(64), C.WHITE, "ma")
txt(CX, 444, "+3", C.D(118), C.GREEN, "ma")
txt(CX, 566, "-110  ·  opened +3.5", C.M(24), C.DIM, "ma")

# team logos flanking the pick
try:
    C.paste_logo(img, C.logo("nfl", "NE", 132), CX - 400, 450)
    C.paste_logo(img, C.logo("nfl", "SEA", 132), CX + 268, 450)
except Exception as e:
    print("logo:", e)

# --- four number panels -----------------------------------------------------
PW, PH_ = 400, 176
cells = [
    (36,        150, "SPREAD MOVE",    "+3.5 → +3",  C.GREEN,
     "Half a point off. At exactly 3", "you push instead of losing."),
    (W-PW-36,   150, "MONEYLINE MOVE", "+160 → +142", C.BLUE,
     "The price moved further than", "the spread did."),
    (36,        640, "TOTAL",          "44.5",        C.AMBER,
     "Has not moved a half point", "since it opened."),
    (W-PW-36,   640, "TRUE WIN CHANCE","40%",         C.WHITE,
     "New England, after stripping out", "what the book keeps."),
]
for x, y, label, big, colour, l1, l2 in cells:
    panel(x, y, PW, PH_)
    d.rectangle([x, y, x + 6, y + PH_], fill=colour)
    txt(x + 26, y + 20, label, C.B(21), C.MUTED)
    txt(x + 26, y + 50, big, C.D(62), colour)
    txt(x + 26, y + 118, l1, C.M(19), C.DIM)
    txt(x + 26, y + 143, l2, C.M(19), C.DIM)

# --- footer -----------------------------------------------------------------
d.rectangle([0, H - 76, W, H], fill=(5, 7, 11, 240))
d.rectangle([0, H - 78, W, H - 76], fill=C.GREEN)
txt(36, H - 52, "@thenumberdesk  ·  insidethenumber.com", C.B(26), C.WHITE)
txt(W - 36, H - 50, "Wed Sep 9 · 8:20 PM ET · NBC  ·  21+", C.M(22), C.MUTED, "ra")

out = "/tmp/gem/itn-real-numbers.png"
img.save(out)
print("wrote", out, img.size)

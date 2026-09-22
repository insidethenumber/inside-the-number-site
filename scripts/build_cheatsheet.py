#!/usr/bin/env python3
"""
The No-Vig Cheat Sheet — the lead magnet delivered on thanks.html at confirm.

CHANGES FROM v1 (Sep 13):
  - Adds "HOW TO USE THE BOARD" — v1 taught the math but never told the reader
    what to do with it on the site. That was the missing half of the promise.
  - Footer cadence line now names The Market Brief and says "weekday mornings"
    instead of "every morning", so the PDF cannot outrun the send schedule.
  - Tightened leading in two blocks to buy room for the new section.

Output: assets/downloads/no-vig-cheat-sheet.pdf  (one page, US Letter)
Run from repo root.
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import os

F = "assets/fonts"
for name, fn in [("Anton","Anton-Regular.ttf"),("BarBold","BarlowCondensed-Bold.ttf"),
                 ("BarSemi","BarlowCondensed-SemiBold.ttf"),("Bar","Barlow-Medium.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, fn)))

BG, INK, GREEN, DIM, LINE = (HexColor('#05070a'), HexColor('#ffffff'),
                             HexColor('#1dd682'), HexColor('#8a93a0'), HexColor('#222833'))
W, H = letter
OUT = 'assets/downloads/no-vig-cheat-sheet.pdf'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("The No-Vig Cheat Sheet — Inside the Number")
c.setAuthor("Inside the Number")
c.setSubject("Turn any two-sided price into the market's true probability.")

c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(GREEN); c.rect(0, H-9, W, 9, fill=1, stroke=0)

def rule(y):
    c.setStrokeColor(LINE); c.setLineWidth(1); c.line(46, y, W-46, y)

def head(y, text):
    c.setFillColor(GREEN); c.setFont('BarBold', 14); c.drawString(46, y, text)
    rule(y-7); return y-24

y = H-52
c.setFillColor(GREEN); c.setFont('BarBold', 12); c.drawString(46, y, "INSIDE THE NUMBER")
c.setFillColor(DIM); c.drawRightString(W-46, y, "insidethenumber.com")
y -= 38
c.setFillColor(INK); c.setFont('Anton', 35); c.drawString(46, y, "THE NO-VIG CHEAT SHEET")
y -= 20
c.setFillColor(DIM); c.setFont('Bar', 10.5)
c.drawString(46, y, "Every two-sided price tells you two things: what the book charges, and what the market actually thinks.")
y -= 13
c.drawString(46, y, "They are not the same number. This is how you get from one to the other.")

# ---- formulas ----
y = head(y-26, "THE ONLY TWO FORMULAS YOU NEED")
c.setFillColor(INK); c.setFont('BarSemi', 11.5); c.drawString(46, y, "1.  American price  to implied %")
y -= 14; c.setFillColor(DIM); c.setFont('Bar', 10)
c.drawString(60, y, "Negative:   imp = –odds ÷ (–odds + 100)          –110  →  110 ÷ 210  =  52.4%")
y -= 12
c.drawString(60, y, "Positive:   imp = 100 ÷ (odds + 100)              +150  →  100 ÷ 250  =  40.0%")
y -= 19
c.setFillColor(INK); c.setFont('BarSemi', 11.5); c.drawString(46, y, "2.  Strip the cut  to the true number")
y -= 14; c.setFillColor(DIM); c.setFont('Bar', 10)
c.drawString(60, y, "fair % = your side's implied %  ÷  (both sides' implied % added together)")
y -= 12
c.drawString(60, y, "Both sides –110:  52.4 + 52.4 = 104.8.   52.4 ÷ 104.8 = 50.0%.  A coin flip, priced as 52.4%.")

# ---- price table ----
y = head(y-24, "WHAT THE COMMON PRICES REALLY COST")
cols = [52, 156, 272, 396]
c.setFillColor(DIM); c.setFont('BarBold', 9.5)
for x, t in zip(cols, ["PRICE", "BREAK-EVEN %", "FAIR % vs –110", "THE BOOK'S CUT"]):
    c.drawString(x, y, t)
y -= 6; rule(y)
for p, be, fair, cut in [("–105","51.2%","50.0%","2.4 cents"),
                         ("–110","52.4%","50.0%","4.8 cents"),
                         ("–115","53.5%","50.0%","7.0 cents"),
                         ("–120","54.5%","50.0%","9.1 cents"),
                         ("+100","50.0%","48.8%","—"),
                         ("–200","66.7%","64.5%","—")]:
    y -= 15.5
    c.setFillColor(INK);   c.drawString(cols[0], y, p)
    c.setFillColor(DIM);   c.setFont('Bar', 10.5); c.drawString(cols[1], y, be)
    c.setFillColor(GREEN); c.drawString(cols[2], y, fair)
    c.setFillColor(DIM);   c.drawString(cols[3], y, cut)
    c.setFont('Bar', 10.5)

# ---- key numbers ----
y = head(y-22, "KEY NUMBERS — WHY HALF A POINT MATTERS")
c.setFillColor(DIM); c.setFont('Bar', 10)
for ln in ["NFL margins land on 3 and 7 more than any other number. Buying off 3 to 2.5, or 7 to 6.5, is worth far more",
           "than the same half point anywhere else. College spreads the distribution wider, but 3, 7, 10 and 14 still cluster.",
           "+3.5 and +3 look almost identical on a board. Then the favorite wins by exactly three — one ticket cashes,",
           "the other pushes. That is the whole argument for watching the number instead of the team."]:
    c.drawString(46, y, ln); y -= 12.5

# ---- line moves ----
y = head(y-14, "READING A LINE MOVE IN FOUR CASES")
for h, b in [("Number moves toward a side AND that side's price rises",
              "Money and the number agree. The strongest read you get."),
             ("Number moves toward a side but that side gets cheaper",
              "The number outran the money that pushed it. A fade setup."),
             ("Number frozen, price on one side keeps climbing",
              "The market is out of room on the number, so it moves the price instead."),
             ("Both sides juiced (–118 / –118)",
              "The book does not want either side at this number.")]:
    c.setFillColor(INK); c.setFont('BarSemi', 10.5); c.drawString(46, y, h); y -= 11.5
    c.setFillColor(DIM); c.setFont('Bar', 9.5);  c.drawString(58, y, b); y -= 12.5

# ---- NEW: how to use the board (two columns) ----
y = head(y-12, "HOW TO USE THE BOARD")
steps = [("1", "Open the board, not the matchup.",
          "Every game, every league, one page."),
         ("2", "Read OPEN before NOW.",
          "Where a number started says more than where it sits."),
         ("3", "Compare true price to posted price.",
          "The gap between them is the book's cut."),
         ("4", "Respect a number sitting on 3 or 7.",
          "Those two carry most of the weight in football.")]
colx = [46, 310]
for row in range(2):
    ytop = y
    for col in range(2):
        n, h, b = steps[row*2 + col]
        x = colx[col]
        c.setFillColor(GREEN); c.setFont('BarBold', 10.5); c.drawString(x, ytop, n)
        c.setFillColor(INK);   c.setFont('BarSemi', 10.5); c.drawString(x+13, ytop, h)
        c.setFillColor(DIM);   c.setFont('Bar', 9.5);      c.drawString(x+13, ytop-11.5, b)
    y = ytop - 28

rule(70)
c.setFillColor(GREEN); c.setFont('BarBold', 11.5)
c.drawString(46, 54, "We run this math on every game on the board — free, no account.")
c.setFillColor(DIM); c.setFont('Bar', 9.5)
c.drawString(46, 41, "The Market Brief · weekday mornings · insidethenumber.com · no picks, no fake records, no units.")
c.drawRightString(W-46, 41, "21+  ·  1-800-GAMBLER")
c.showPage(); c.save()
print("built", OUT, os.path.getsize(OUT)//1024, "KB")

#!/usr/bin/env python3
"""
The No-Vig Cheat Sheet — the lead magnet.

WHY IT EXISTS. Until Sep 13 2026 the only ask on the site was "subscribe for
our picks". That asks a stranger for trust we have not earned, and it converted
at roughly nothing. A reference card asks for nothing — it is a thing they keep.
The calculator search traffic proves people want the tool, not the tout.

Output: assets/downloads/no-vig-cheat-sheet.pdf  (one page, US Letter)
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
y -= 40
c.setFillColor(INK); c.setFont('Anton', 37); c.drawString(46, y, "THE NO-VIG CHEAT SHEET")
y -= 21
c.setFillColor(DIM); c.setFont('Bar', 10.5)
c.drawString(46, y, "Every two-sided price tells you two things: what the book charges, and what the market actually thinks.")
y -= 14
c.drawString(46, y, "They are not the same number. This is how you get from one to the other.")

y = head(y-30, "THE ONLY TWO FORMULAS YOU NEED")
c.setFillColor(INK); c.setFont('BarSemi', 11.5); c.drawString(46, y, "1.  American price  to implied %")
y -= 15; c.setFillColor(DIM); c.setFont('Bar', 10)
c.drawString(60, y, "Negative:   imp = –odds ÷ (–odds + 100)          –110  →  110 ÷ 210  =  52.4%")
y -= 13
c.drawString(60, y, "Positive:   imp = 100 ÷ (odds + 100)              +150  →  100 ÷ 250  =  40.0%")
y -= 22
c.setFillColor(INK); c.setFont('BarSemi', 11.5); c.drawString(46, y, "2.  Strip the cut  to the true number")
y -= 15; c.setFillColor(DIM); c.setFont('Bar', 10)
c.drawString(60, y, "fair % = your side's implied %  ÷  (both sides' implied % added together)")
y -= 13
c.drawString(60, y, "Both sides –110:  52.4 + 52.4 = 104.8.   52.4 ÷ 104.8 = 50.0%.  A coin flip, priced as 52.4%.")

y = head(y-28, "WHAT THE COMMON PRICES REALLY COST")
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
    y -= 17
    c.setFillColor(INK);   c.drawString(cols[0], y, p)
    c.setFillColor(DIM);   c.setFont('Bar', 10.5); c.drawString(cols[1], y, be)
    c.setFillColor(GREEN); c.drawString(cols[2], y, fair)
    c.setFillColor(DIM);   c.drawString(cols[3], y, cut)
    c.setFont('Bar', 10.5)

y = head(y-26, "KEY NUMBERS — WHY HALF A POINT MATTERS")
c.setFillColor(DIM); c.setFont('Bar', 10)
for ln in ["NFL margins land on 3 and 7 more than any other number. Buying off 3 to 2.5, or 7 to 6.5, is worth far more",
           "than the same half point anywhere else. College spreads the distribution wider, but 3, 7, 10 and 14 still cluster.",
           "",
           "+3.5 and +3 look almost identical on a board. Then the favorite wins by exactly three — one ticket cashes,",
           "the other pushes. That is the whole argument for watching the number instead of the team."]:
    c.drawString(46, y, ln); y -= 13

y = head(y-16, "READING A LINE MOVE IN FOUR CASES")
for h, b in [("Number moves toward a side AND that side's price rises",
              "Money and the number agree. The strongest read you get."),
             ("Number moves toward a side but that side gets cheaper",
              "The number outran the money that pushed it. A fade setup."),
             ("Number frozen, price on one side keeps climbing",
              "The market is out of room on the number, so it moves the price instead."),
             ("Both sides juiced (–118 / –118)",
              "The book does not want either side at this number.")]:
    c.setFillColor(INK); c.setFont('BarSemi', 10.5); c.drawString(46, y, h); y -= 12
    c.setFillColor(DIM); c.setFont('Bar', 9.5);  c.drawString(58, y, b); y -= 16

rule(70)
c.setFillColor(GREEN); c.setFont('BarBold', 11.5)
c.drawString(46, 54, "We run this math on every game, every morning — free.")
c.setFillColor(DIM); c.setFont('Bar', 9.5)
c.drawString(46, 41, "insidethenumber.com   ·   no picks-only pitch, no fake records, no units.")
c.drawRightString(W-46, 41, "21+  ·  1-800-GAMBLER")
c.showPage(); c.save()
print("built", OUT, os.path.getsize(OUT)//1024, "KB")

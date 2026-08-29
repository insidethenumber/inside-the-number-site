#!/usr/bin/env python3
"""
Inside the Number — social card generator.

Builds branded PNG/GIF cards for X from live odds data. Every format here was
designed against engagement data scraped from competitor accounts on Aug 29 2026
(see MARKETING_X.md and X_TEARDOWN_AUG29.md).

DESIGN RULE: the graphic supports the post, it never carries it. The first line of
the tweet still has to do the work. A great card under a boring line still dies.

Usage:
    python3 scripts/build_social_card.py divergence --out card.png \
        --matchup "Hawai'i at Stanford" --when "Today 6:00 PM CT" \
        --spread-from -3 --spread-to -4.5 --total-from 50.5 --total-to 48.5

    python3 scripts/build_social_card.py tierlist --out tiers.png --json tiers.json
    python3 scripts/build_social_card.py bignumber --out big.png \
        --team USC --number -37.5 --translation "win by five touchdowns."
    python3 scripts/build_social_card.py linemove-gif --out move.gif ...

Fonts: Poppins (bundled on most systems via google-fonts). Falls back to DejaVu.
"""
import argparse, json, os, random, sys
from PIL import Image, ImageDraw, ImageFont

# ---------- brand ----------
BG=(5,6,8); GREEN=(0,208,132); BLUE=(56,152,255); WHITE=(240,243,247)
MUTED=(120,132,148); CARD=(13,16,21); LINE=(30,36,45); RED=(255,86,86); AMBER=(255,184,77)

FONT_DIRS=["/usr/share/fonts/truetype/google-fonts/","/System/Library/Fonts/Supplemental/",
           "/usr/share/fonts/truetype/dejavu/"]
def F(name,size):
    for d in FONT_DIRS:
        p=os.path.join(d,name)
        if os.path.exists(p):
            return ImageFont.truetype(p,size)
    for d in FONT_DIRS:
        for fb in ("DejaVuSans-Bold.ttf","DejaVuSans.ttf"):
            p=os.path.join(d,fb)
            if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
BOLD="Poppins-Bold.ttf"; MED="Poppins-Medium.ttf"; REG="Poppins-Regular.ttf"; LIGHT="Poppins-Light.ttf"

def canvas(w,h):
    img=Image.new("RGB",(w,h),BG); d=ImageDraw.Draw(img)
    for k in range(6): d.line([(0,k),(w,k)],fill=(0,208-k*12,132-k*6))
    return img,d

def footer(d,w,h):
    d.text((48,h-58),"INSIDE THE NUMBER",font=F(BOLD,22),fill=WHITE)
    d.text((285,h-54),"insidethenumber.com",font=F(MED,18),fill=MUTED)
    d.text((w-190,h-54),"21+ · itn",font=F(MED,18),fill=MUTED)

def arrow(d,x,y,up,color,size=48):
    if up: d.polygon([(x,y-size//2),(x-size//2,y+size//3),(x+size//2,y+size//3)],fill=color)
    else:  d.polygon([(x,y+size//2),(x-size//2,y-size//3),(x+size//2,y-size//3)],fill=color)

def fmt(v):
    s=f"{v:g}"
    return s.replace("-","−")

# ---------- formats ----------
def divergence(a):
    w,h=1200,675; img,d=canvas(w,h)
    d.text((48,44),"THE MARKET DISAGREES WITH ITSELF",font=F(BOLD,24),fill=GREEN)
    d.text((48,80),a.matchup,font=F(BOLD,58),fill=WHITE)
    d.text((48,152),a.when,font=F(MED,22),fill=MUTED)
    panels=[("SPREAD",a.spread_from,a.spread_to,a.spread_to<a.spread_from,GREEN,"MARKET MORE CONFIDENT"),
            ("TOTAL", a.total_from, a.total_to, a.total_to>a.total_from, RED,"EXPECTS FEWER POINTS")]
    for i,(lab,fr,to,up,col,sub) in enumerate(panels):
        x=48+i*566; y=214
        d.rounded_rectangle([x,y,x+520,y+250],radius=18,fill=CARD,outline=LINE,width=2)
        d.text((x+34,y+28),lab,font=F(BOLD,22),fill=MUTED)
        d.text((x+34,y+78),fmt(fr),font=F(MED,46),fill=MUTED)
        arrow(d,x+250,y+108,up,col)
        d.text((x+310,y+70),fmt(to),font=F(BOLD,60),fill=col)
        d.text((x+34,y+178),sub,font=F(BOLD,20),fill=col)
    d.rounded_rectangle([48,496,w-48,566],radius=14,fill=(10,26,20),outline=GREEN,width=2)
    d.text((72,516),a.verdict,font=F(BOLD,28),fill=WHITE)
    footer(d,w,h); img.save(a.out); return a.out

def bignumber(a):
    w,h=1200,675; img,d=canvas(w,h)
    d.text((48,60),a.label,font=F(BOLD,24),fill=GREEN)
    d.text((48,120),a.team,font=F(BOLD,70),fill=WHITE)
    d.text((48,200),fmt(a.number),font=F(BOLD,190),fill=GREEN)
    d.text((620,232),"The market is saying",font=F(MED,30),fill=MUTED)
    words=a.translation.split()
    mid=len(words)//2 or 1
    d.text((620,278)," ".join(words[:mid]),font=F(BOLD,52),fill=WHITE)
    d.text((620,336)," ".join(words[mid:]),font=F(BOLD,52),fill=WHITE)
    if a.kicker:
        d.rounded_rectangle([620,410,w-48,486],radius=14,fill=(26,14,10),outline=AMBER,width=2)
        d.text((646,432),a.kicker,font=F(BOLD,26),fill=AMBER)
    d.text((48,470),a.sub,font=F(MED,24),fill=MUTED)
    footer(d,w,h); img.save(a.out); return a.out

def tierlist(a):
    tiers=json.load(open(a.json))
    rows=sum(max(1,len(v)) for _,v in tiers)
    w,h=1200,240+rows*62+130; img,d=canvas(w,h)
    d.text((44,40),a.label,font=F(BOLD,24),fill=GREEN)
    d.text((44,76),a.headline,font=F(BOLD,44),fill=WHITE)
    palette=[RED,AMBER,GREEN,(90,100,115),(120,132,148)]
    y=170
    for i,(letter,items) in enumerate(tiers):
        col=palette[min(i,len(palette)-1)]
        bh=max(112,len(items)*46+30)
        d.rounded_rectangle([44,y,150,y+bh],radius=12,fill=col)
        d.text((78,y+bh//2-34),letter,font=F(BOLD,62),fill=BG)
        d.rounded_rectangle([160,y,w-44,y+bh],radius=12,fill=CARD,outline=LINE,width=1)
        ty=y+(bh-len(items)*44)//2
        for it in items:
            d.text((188,ty),it,font=F(MED,34),fill=WHITE); ty+=44
        y+=bh+12
    if a.sub: d.text((44,y+6),a.sub,font=F(MED,26),fill=MUTED)
    footer(d,w,h); img.save(a.out); return a.out

def linemove_gif(a):
    W,H=1000,560; frames=[]; TOTAL=54; HS,HE=8,14
    ease=lambda t:t*t*(3-2*t)
    for i in range(TOTAL):
        img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
        for k in range(5): d.line([(0,k),(W,k)],fill=(0,208-k*14,132-k*8))
        p = 0.0 if i<HS else (1.0 if i>TOTAL-HE else ease((i-HS)/(TOTAL-HE-HS)))
        sp=a.spread_from+(a.spread_to-a.spread_from)*p
        to=a.total_from +(a.total_to -a.total_from )*p
        d.text((44,38),a.label,font=F(BOLD,22),fill=GREEN)
        d.text((44,72),a.matchup,font=F(BOLD,48),fill=WHITE)
        for j,(lab,val,col) in enumerate([("SPREAD",sp,GREEN),("TOTAL",to,RED)]):
            x=44+j*468
            d.rounded_rectangle([x,150,x+444,352],radius=16,fill=CARD,outline=LINE,width=2)
            d.text((x+28,174),lab,font=F(BOLD,20),fill=MUTED)
            d.text((x+28,212),fmt(round(val,1)),font=F(BOLD,92),fill=col)
            d.rounded_rectangle([x+28,318,x+28+max(int(340*p),4),326],radius=4,fill=col)
        if p>0.92:
            d.rounded_rectangle([44,392,W-44,462],radius=14,fill=(10,26,20),outline=GREEN,width=2)
            d.text((70,412),a.verdict,font=F(BOLD,30),fill=WHITE)
        d.text((44,H-46),"INSIDE THE NUMBER",font=F(BOLD,20),fill=WHITE)
        d.text((262,H-43),"insidethenumber.com",font=F(MED,17),fill=MUTED)
        frames.append(img)
    frames[0].save(a.out,save_all=True,append_images=frames[1:],duration=66,loop=0,optimize=True)
    return a.out

FORMATS={"divergence":divergence,"bignumber":bignumber,"tierlist":tierlist,"linemove-gif":linemove_gif}

def main():
    p=argparse.ArgumentParser(description="ITN social card generator")
    p.add_argument("format",choices=FORMATS.keys())
    p.add_argument("--out",required=True)
    p.add_argument("--matchup",default=""); p.add_argument("--when",default="")
    p.add_argument("--spread-from",type=float,default=0); p.add_argument("--spread-to",type=float,default=0)
    p.add_argument("--total-from",type=float,default=0);  p.add_argument("--total-to",type=float,default=0)
    p.add_argument("--verdict",default=""); p.add_argument("--team",default="")
    p.add_argument("--number",type=float,default=0); p.add_argument("--translation",default="")
    p.add_argument("--kicker",default=""); p.add_argument("--sub",default="")
    p.add_argument("--label",default="LINE MOVE"); p.add_argument("--headline",default="")
    p.add_argument("--json",default="")
    a=p.parse_args()
    out=FORMATS[a.format](a)
    print(out)

if __name__=="__main__":
    main()

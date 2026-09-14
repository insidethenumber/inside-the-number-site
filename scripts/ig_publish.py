#!/usr/bin/env python3
"""
Inside the Number — Instagram publishing queue.

WHY THIS EXISTS (written Sep 14, 2026)
--------------------------------------
The Meta setup was finished Sep 13: professional account, linked Facebook Page,
developer app, tester role, long-lived token good through Nov 12. It worked —
a real post went out through the API that night.

Then on Sep 14 it failed, and the reason had nothing to do with any of that.
The token lives in a local file on a machine with NO network route to Meta.
The only way to use it was to hand it to a browser and let the browser make the
call. That hand-off is exactly the pattern a credential-safety check exists to
stop, so one day it worked and the next day it didn't. Instagram then had to be
posted by hand, through a login screen, on a deadline.

X has never had this problem. Its credentials live in GitHub Secrets and a
GitHub runner does the posting, so it posts whether anyone is at a desk or not.
This script gives Instagram the same shape. Nothing about the Meta setup is
redone: same token, same app, same Page. It just moves somewhere that can
actually reach Meta, and where no credential passes through a browser.

HOW IT WORKS
------------
Queue lives in ig/ and mirrors posts/ :

    ig/<slug>.txt   the caption
    ig/<slug>.png   the image (or .jpg)
    ig/.sent.json   state, committed back so a fresh checkout never double-posts

Publishing is Meta's two-step flow:

    1. POST /{ig-user-id}/media          -> returns a container id
    2. poll  /{container-id}?fields=status_code  until FINISHED
    3. POST /{ig-user-id}/media_publish  -> returns the live media id

The image must be at a PUBLIC URL Meta can fetch; it cannot be uploaded as
bytes. So the image is served off insidethenumber.com, and this script refuses
to publish until that URL actually returns 200 — the Cloudflare deploy lags the
push by a minute or two and publishing early gets a container that never
finishes.

    python3 scripts/ig_publish.py --dry-run   # show what's next, send nothing
    python3 scripts/ig_publish.py             # publish one
    python3 scripts/ig_publish.py --status    # queue health

Credentials come from env vars in CI (GitHub Secrets) or itn-secrets.env
locally: IG_ACCESS_TOKEN, IG_BUSINESS_ACCOUNT_ID.
"""

import argparse, glob, json, os, sys, time, datetime
import urllib.request, urllib.parse, urllib.error

HERE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(HERE)
QUEUE = os.path.join(ROOT, "ig")
STATE = os.path.join(QUEUE, ".sent.json")

API_BASE = os.environ.get("IG_API_BASE", "https://graph.instagram.com")
API_VER  = os.environ.get("IG_API_VERSION", "v21.0")
SITE     = "https://insidethenumber.com"
# Where the workflow copies queue images so they get a public URL.
PUBLIC_DIR = "assets/ig"

IMAGE_EXTS = (".png", ".jpg", ".jpeg")
CAPTION_MAX = 2200
# Instagram rejects anything outside this range outright. 1080x1350 == 0.8.
AR_MIN, AR_MAX = 0.8, 1.91


# ----------------------------------------------------------------- creds
def creds():
    tok = os.environ.get("IG_ACCESS_TOKEN")
    uid = os.environ.get("IG_BUSINESS_ACCOUNT_ID")
    if tok and uid:
        return tok, uid
    path = os.path.join(ROOT, "itn-secrets.env")
    if os.path.exists(path):
        vals = {}
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                vals[k.strip()] = v.strip()
        tok = tok or vals.get("IG_ACCESS_TOKEN")
        uid = uid or vals.get("IG_BUSINESS_ACCOUNT_ID")
    if not tok or not uid:
        sys.exit("ERROR: IG_ACCESS_TOKEN and IG_BUSINESS_ACCOUNT_ID are not set. "
                 "In CI these come from GitHub Secrets; locally from itn-secrets.env.")
    return tok, uid


# ----------------------------------------------------------------- http
def _api(path, params, method="GET", timeout=45):
    url = f"{API_BASE}/{API_VER}/{path.lstrip('/')}"
    data = None
    if method == "POST":
        data = urllib.parse.urlencode(params).encode()
    else:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"ERROR: Meta returned {e.code} for {method} {path}\n{body}")


def url_is_live(url, tries=12, wait=15):
    """Meta fetches the image itself, so it must be reachable BEFORE we publish."""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status == 200:
                    print(f"  image live after {i+1} check(s)")
                    return True
        except Exception:
            pass
        if i < tries - 1:
            time.sleep(wait)
    return False


# ----------------------------------------------------------------- state
def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"sent": [], "history": []}


def save_state(st):
    os.makedirs(QUEUE, exist_ok=True)
    json.dump(st, open(STATE, "w"), indent=2)


def next_item(st):
    for txt in sorted(glob.glob(os.path.join(QUEUE, "*.txt"))):
        slug = os.path.splitext(os.path.basename(txt))[0]
        if slug in st["sent"]:
            continue
        img = None
        for ext in IMAGE_EXTS:
            cand = os.path.join(QUEUE, slug + ext)
            if os.path.exists(cand):
                img = cand
                break
        return slug, txt, img
    return None, None, None


# ----------------------------------------------------------------- checks
def check(slug, txt, img):
    problems = []
    caption = open(txt).read().rstrip()
    if not caption:
        problems.append("caption is empty")
    if len(caption) > CAPTION_MAX:
        problems.append(f"caption is {len(caption)} chars, over the {CAPTION_MAX} limit")
    if not img:
        problems.append("no image beside the caption (Instagram will not take a text-only post)")
    else:
        try:
            from PIL import Image
            w, h = Image.open(img).size
            ar = w / h
            if not (AR_MIN - 1e-6 <= ar <= AR_MAX + 1e-6):
                problems.append(
                    f"aspect ratio {ar:.4f} ({w}x{h}) is outside Instagram's "
                    f"{AR_MIN}-{AR_MAX}. Pad the canvas; do not crop the content.")
        except ImportError:
            print("  note: Pillow missing, skipping aspect-ratio check")
    return caption, problems


# ----------------------------------------------------------------- publish
def publish(slug, caption, image_url, token, uid):
    print(f"  creating container for {image_url}")
    c = _api(f"{uid}/media",
             {"image_url": image_url, "caption": caption, "access_token": token},
             method="POST")
    cid = c.get("id")
    if not cid:
        raise SystemExit(f"ERROR: no container id returned: {c}")
    print(f"  container {cid}")

    for i in range(30):
        s = _api(cid, {"fields": "status_code,status", "access_token": token})
        code = s.get("status_code")
        if code == "FINISHED":
            print(f"  container FINISHED after {i+1} poll(s)")
            break
        if code == "ERROR":
            raise SystemExit(f"ERROR: container failed: {s}")
        time.sleep(5)
    else:
        raise SystemExit("ERROR: container never reached FINISHED after 150s")

    r = _api(f"{uid}/media_publish",
             {"creation_id": cid, "access_token": token}, method="POST")
    mid = r.get("id")
    if not mid:
        raise SystemExit(f"ERROR: publish returned no media id: {r}")

    perma = ""
    try:
        perma = _api(mid, {"fields": "permalink", "access_token": token}).get("permalink", "")
    except SystemExit:
        pass
    return mid, perma


# ----------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dry-run", action="store_true", help="show what's next, publish nothing")
    p.add_argument("--status", action="store_true", help="queue health")
    p.add_argument("--public-base", default=SITE,
                   help="origin the image is served from (default insidethenumber.com)")
    a = p.parse_args()

    st = load_state()
    slug, txt, img = next_item(st)

    if a.status:
        total = len(glob.glob(os.path.join(QUEUE, "*.txt")))
        print(f"sent: {len(st['sent'])}   pending: {total - len(st['sent'])}")
        print(f"   next: {os.path.basename(txt) if txt else '(queue empty)'}")
        if total - len(st["sent"]) == 0:
            print("\nWARNING: Instagram queue is empty. Add ig/<slug>.txt + ig/<slug>.png.")
        return

    if not slug:
        print("Nothing to publish — Instagram queue is empty.")
        return

    caption, problems = check(slug, txt, img)
    ext = os.path.splitext(img)[1] if img else ""
    image_url = f"{a.public_base.rstrip('/')}/{PUBLIC_DIR}/{slug}{ext}"

    print(f"--- next: {slug} ({len(caption)} chars, "
          f"{'image' if img else 'NO IMAGE'}) ---")
    print(caption)
    print("-" * 50)
    print(f"image_url: {image_url}")

    if problems:
        for pr in problems:
            print(f"ERROR: {pr}")
        sys.exit(1)

    if a.dry_run:
        print("(dry run — nothing published)")
        return

    token, uid = creds()

    if not url_is_live(image_url):
        sys.exit(f"ERROR: {image_url} is not reachable. Meta fetches the image "
                 f"itself, so publishing now would create a container that never "
                 f"finishes. Is the deploy done?")

    mid, perma = publish(slug, caption, image_url, token, uid)
    print(f"PUBLISHED {mid} {perma}")

    st["sent"].append(slug)
    st["history"].append({
        "slug": slug,
        "media_id": mid,
        "permalink": perma,
        "image_url": image_url,
        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    })
    save_state(st)
    print(f"state written: {len(st['sent'])} sent")


if __name__ == "__main__":
    main()

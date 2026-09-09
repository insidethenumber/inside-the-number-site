#!/usr/bin/env python3
"""
Build the ITN photo library from data/photo_manifest.json.

Runs in GitHub Actions, not locally: the sandbox has no egress to any image
host (images.unsplash.com, upload.wikimedia.org and every mirror return 403
through the proxy). CI has open network, so CI downloads and commits the files
back, and everything else in the pipeline reads them out of the repo.

Two sources, and the difference matters legally:

  Unsplash    Unsplash License. Commercial use allowed, no attribution legally
              required. We use it ONLY for photos with no identifiable athlete
              and no team mark - turf, lights, goalposts, a ball. Those are safe
              anywhere, including on a graphic that promotes the newsletter.

  Commons     Wikimedia Commons. This is where real game photography comes from.
              Licenses vary per file, so this script reads each file's actual
              license from the API and REFUSES anything non-commercial (NC) or
              no-derivatives (ND). A photo we cannot crop or overlay is useless
              to us, and one we cannot use commercially is a lawsuit waiting on
              the day we put an affiliate link under it.

Every accepted file gets a row in assets/photos/CREDITS.json with the
photographer, the licence and the source URL, so attribution is never guesswork
at posting time.

    python3 scripts/fetch_photos.py            # fetch anything missing
    python3 scripts/fetch_photos.py --force    # re-fetch everything
"""

import argparse, json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "photos")
MANIFEST = os.path.join(ROOT, "data", "photo_manifest.json")
CREDITS = os.path.join(OUT, "CREDITS.json")

UA = "InsideTheNumber/1.0 (https://insidethenumber.com; desk@insidethenumber.com)"
COMMONS = "https://commons.wikimedia.org/w/api.php"

# Licences we will not touch. NC forbids commercial use; ND forbids the crops
# and overlays that every card we build depends on. Rejecting them here is
# cheaper than discovering it after a graphic is live.
BANNED = re.compile(r"\b(NC|ND|noncommercial|no-?deriv|fair ?use|non-free)\b", re.I)
# Anything not on this list gets rejected too - unknown means unknown, and an
# unknown licence on a betting account is not a risk worth taking.
ALLOWED = re.compile(
    r"^(cc[- ]?by([- ]sa)?([- ]\d(\.\d)?)?|cc0|public ?domain|pd([- ].*)?|"
    r"attribution([- ]sharealike)?)", re.I)

# Big enough to crop into a 1080x1920 Reel without softening.
MIN_W, MIN_H = 1200, 800


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except Exception as e:
            if i == tries - 1:
                raise
            print(f"   retry {i+1} after {e}")
            time.sleep(2 * (i + 1))


def slugify(s):
    s = re.sub(r"\.[A-Za-z0-9]+$", "", s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:60]


def commons_query(params):
    params = dict(params, format="json", formatversion="2")
    return json.loads(get(COMMONS + "?" + urllib.parse.urlencode(params)))


def licence_of(info):
    """Pull the licence short name out of extmetadata, tolerating its shapes."""
    meta = (info.get("extmetadata") or {})
    for key in ("LicenseShortName", "License", "UsageTerms"):
        v = meta.get(key, {}).get("value")
        if v:
            return re.sub(r"<[^>]+>", "", str(v)).strip()
    return ""


def artist_of(info):
    v = (info.get("extmetadata") or {}).get("Artist", {}).get("value", "")
    v = re.sub(r"<[^>]+>", " ", str(v))
    return re.sub(r"\s+", " ", v).strip() or "Unknown"


def fetch_commons(search, credits, force):
    """Search Commons, keep only commercially reusable, modifiable images."""
    kept, seen = 0, set()
    want = search["limit"]
    res = commons_query({
        "action": "query", "generator": "search",
        "gsrsearch": f'filetype:bitmap {search["query"]}',
        "gsrnamespace": "6", "gsrlimit": str(want * 5),
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata|mime",
        "iiurlwidth": "1800",
    })
    pages = (res.get("query") or {}).get("pages") or []
    for p in pages:
        if kept >= want:
            break
        info = (p.get("imageinfo") or [{}])[0]
        if not info:
            continue
        title = p.get("title", "").removeprefix("File:")
        if title in seen:
            continue
        seen.add(title)

        lic = licence_of(info)
        if not lic or BANNED.search(lic) or not ALLOWED.match(lic):
            print(f"   skip (licence '{lic or 'unknown'}'): {title}")
            continue
        if (info.get("mime") or "") not in ("image/jpeg", "image/png"):
            continue
        if info.get("width", 0) < MIN_W or info.get("height", 0) < MIN_H:
            print(f"   skip (too small {info.get('width')}x{info.get('height')}): {title}")
            continue

        name = f'{search["slug"]}-{slugify(title)}.jpg'
        dest = os.path.join(OUT, name)
        if os.path.exists(dest) and not force:
            kept += 1
            continue
        url = info.get("thumburl") or info.get("url")
        try:
            data = get(url)
        except Exception as e:
            print(f"   FAILED {title}: {e}")
            continue
        with open(dest, "wb") as f:
            f.write(data)
        credits[name] = {
            "source": "wikimedia-commons",
            "title": title,
            "photographer": artist_of(info),
            "licence": lic,
            "page": info.get("descriptionurl"),
            "use": "editorial",
        }
        print(f"   ok  {name}  [{lic}]  {len(data)//1024}KB")
        kept += 1
    if kept == 0:
        print(f"   WARNING: nothing usable for '{search['query']}'")
    return kept


def fetch_unsplash(item, credits, force):
    name = f'unsplash-{item["slug"]}.jpg'
    dest = os.path.join(OUT, name)
    if os.path.exists(dest) and not force:
        return 0
    url = (f'https://images.unsplash.com/{item["path"]}'
           f'?fm=jpg&q=85&w=2400&fit=max&cs=tinysrgb')
    data = get(url)
    with open(dest, "wb") as f:
        f.write(data)
    credits[name] = {
        "source": "unsplash",
        "photographer": item["credit"],
        "profile": f'https://unsplash.com/@{item["user"]}',
        "licence": "Unsplash License",
        "page": f'https://unsplash.com/photos/{item["id"]}',
        "use": "commercial-ok",
    }
    print(f'   ok  {name}  {len(data)//1024}KB')
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    man = json.load(open(MANIFEST))
    credits = json.load(open(CREDITS)) if os.path.exists(CREDITS) else {}

    print("Unsplash (conceptual, commercial-safe)")
    n = 0
    for item in man.get("unsplash", []):
        try:
            n += fetch_unsplash(item, credits, a.force)
        except Exception as e:
            print(f'   FAILED {item["slug"]}: {e}')

    print("\nWikimedia Commons (editorial, licence-checked)")
    for s in man.get("commons_searches", []):
        print(f'  {s["slug"]}: {s["query"]}')
        n += fetch_commons(s, credits, a.force)

    # Drop rows for files someone deleted, so CREDITS never claims a photo we
    # no longer ship.
    for name in [k for k in credits if not os.path.exists(os.path.join(OUT, k))]:
        del credits[name]

    with open(CREDITS, "w") as f:
        json.dump(dict(sorted(credits.items())), f, indent=1)

    have = len([f for f in os.listdir(OUT) if f.lower().endswith((".jpg", ".png"))])
    print(f"\n{n} new, {have} photos in the library, {len(credits)} credited.")
    if have == 0:
        sys.exit("No photos downloaded — something is wrong with the network or the manifest.")


if __name__ == "__main__":
    main()

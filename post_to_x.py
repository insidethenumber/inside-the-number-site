#!/usr/bin/env python3
"""
Inside the Number — X poster.

Reads credentials from a file OUTSIDE this repo (this repo is public), signs an
OAuth 1.0a request by hand and posts to the X API v2.

Standard library only — no pip install, so a scheduled task can't break because
a dependency moved.

Usage
-----
    python3 post_to_x.py --verify                 # confirm the keys work (a read, ~$0.005)
    python3 post_to_x.py --dry-run --text "..."   # print what would go out, send nothing
    python3 post_to_x.py --text "..."             # actually post

Costs, as of Aug 2026: $0.015 per post, $0.20 if the post contains a link.

Every failure mode is reported distinctly, because "it didn't work" is useless
at 6am. Auth problems, billing problems, rate limits and duplicate text all
look different and need different fixes.
"""

import argparse, re, base64, hashlib, hmac, json, os, sys, time, urllib.parse, urllib.request, urllib.error, secrets as _secrets

def _find_secrets():
    """
    Locate itn-secrets.env.

    Order matters. ITN_SECRETS wins so CI or a one-off run can point elsewhere.
    Otherwise look next to this file first — the secrets live in the repo folder,
    excluded by a deny-by-default .gitignore — then the older sibling-of-repo
    location, which is where an earlier version of this script expected it.
    """
    env = os.environ.get("ITN_SECRETS")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, "itn-secrets.env"),
                 os.path.join(os.path.dirname(here), "itn-secrets.env"),
                 os.path.expanduser("~/Documents/Claude/Projects/itn-secrets.env")):
        if os.path.exists(cand):
            return cand
    return os.path.join(here, "itn-secrets.env")


SECRETS = _find_secrets()
API_POST = "https://api.x.com/2/tweets"
API_ME   = "https://api.x.com/2/users/me"


def load_secrets(path=SECRETS):
    """Parse a KEY=value file. Missing file is a clear error, not a traceback."""
    if not os.path.exists(path):
        sys.exit(f"ERROR: credentials file not found at {path}")
    out = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    needed = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET"]
    missing = [k for k in needed if not out.get(k)]
    if missing:
        sys.exit("ERROR: missing or empty in itn-secrets.env: " + ", ".join(missing))
    return out


def _q(s):
    """Percent-encoding per RFC 5849 — stricter than the urllib default."""
    return urllib.parse.quote(str(s), safe="~")


def oauth_header(method, url, creds, query=None):
    """
    Build an OAuth 1.0a Authorization header.

    Note: a JSON request body is deliberately NOT part of the signature base
    string. Only oauth_* parameters and any URL query parameters are signed.
    Including the body is the classic reason a hand-rolled signer returns 401.
    """
    p = {
        "oauth_consumer_key": creds["X_API_KEY"],
        "oauth_nonce": _secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": creds["X_ACCESS_TOKEN"],
        "oauth_version": "1.0",
    }
    sig_params = dict(p)
    if query:
        sig_params.update(query)

    joined = "&".join(f"{_q(k)}={_q(sig_params[k])}" for k in sorted(sig_params))
    base = "&".join([method.upper(), _q(url), _q(joined)])
    key = f'{_q(creds["X_API_SECRET"])}&{_q(creds["X_ACCESS_SECRET"])}'
    p["oauth_signature"] = base64.b64encode(
        hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()
    ).decode()

    return "OAuth " + ", ".join(f'{_q(k)}="{_q(v)}"' for k, v in sorted(p.items()))


def call(method, url, creds, body=None):
    """Returns (status, parsed_json_or_text)."""
    headers = {"Authorization": oauth_header(method, url, creds)}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, raw
    except Exception as e:
        return 0, str(e)


API_MEDIA = "https://upload.twitter.com/1.1/media/upload.json"


def upload_media(path, creds):
    """Upload an image and return its media_id_string.

    v1.1 simple upload: one multipart POST, images only, under 5MB. The OAuth
    signature base string deliberately excludes multipart body fields — only
    the oauth_* params are signed — which is why oauth_header() works here
    unchanged. Getting that wrong is the classic 401 on this endpoint.
    """
    if not os.path.exists(path):
        raise SystemExit(f"ERROR: no such image: {path}")
    size = os.path.getsize(path)
    if size > 5 * 1024 * 1024:
        raise SystemExit(f"ERROR: {path} is {size/1e6:.1f}MB, over X's 5MB image limit.")

    boundary = "----itn" + _secrets.token_hex(12)
    fname = os.path.basename(path)
    ext = os.path.splitext(fname)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".webp": "image/webp"}.get(ext, "image/png")

    body = b"".join([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="media"; filename="{fname}"\r\n'.encode(),
        f"Content-Type: {mime}\r\n\r\n".encode(),
        open(path, "rb").read(),
        f"\r\n--{boundary}--\r\n".encode(),
    ])
    headers = {
        "Authorization": oauth_header("POST", API_MEDIA, creds),
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    req = urllib.request.Request(API_MEDIA, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            payload = json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"MEDIA UPLOAD FAILED (HTTP {e.code}): {e.read().decode()[:300]}")
    mid = payload.get("media_id_string")
    if not mid:
        raise SystemExit(f"MEDIA UPLOAD FAILED: no media_id in {str(payload)[:200]}")
    print(f"uploaded {fname} ({size/1024:.0f}KB) -> media_id {mid}")
    return mid


API_RT   = "https://api.x.com/2/users/{uid}/retweets"

# Video needs CHUNKED upload: INIT -> APPEND(n) -> FINALIZE -> poll STATUS.
# The simple one-shot upload above is images only. Added Sep 12, 2026 so the
# 1080x1920 reels we already render can go to X, where video outreaches a
# static card by a wide margin.
#
# OAUTH GOTCHA, and it is the whole reason this is fiddly: OAuth 1.0a signs
# URL QUERY parameters but NOT multipart body fields. So every control param
# (command, media_id, segment_index) goes in the QUERY STRING where it gets
# signed, and only the raw bytes ride in the multipart body. Putting command
# in the body instead is the classic 401 here.

CHUNK = 4 * 1024 * 1024          # 4MB — X's per-APPEND ceiling is 5MB
VIDEO_MAX = 512 * 1024 * 1024


def _media_call(creds, query, body=None, content_type=None, method="POST"):
    url = API_MEDIA + "?" + urllib.parse.urlencode(query)
    headers = {"Authorization": oauth_header(method, API_MEDIA, creds, query=query)}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode() or "{}"
            return r.status, (json.loads(raw) if raw.strip().startswith("{") else raw)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"MEDIA {query.get('command')} FAILED (HTTP {e.code}): {e.read().decode()[:300]}")


def upload_video(path, creds, media_category="tweet_video"):
    """Chunked-upload a video (or big GIF) and return its media_id_string."""
    if not os.path.exists(path):
        raise SystemExit(f"ERROR: no such video: {path}")
    size = os.path.getsize(path)
    if size > VIDEO_MAX:
        raise SystemExit(f"ERROR: {path} is {size/1e6:.0f}MB, over X's 512MB video limit.")
    ext = os.path.splitext(path)[1].lower()
    mime = {".mp4": "video/mp4", ".mov": "video/quicktime", ".gif": "image/gif"}.get(ext)
    if not mime:
        raise SystemExit(f"ERROR: {ext} is not a video type X accepts (use .mp4/.mov).")
    if ext == ".gif":
        media_category = "tweet_gif"

    _, init = _media_call(creds, {"command": "INIT", "total_bytes": str(size),
                                  "media_type": mime, "media_category": media_category})
    mid = init.get("media_id_string")
    if not mid:
        raise SystemExit(f"INIT gave no media_id: {str(init)[:200]}")
    print(f"INIT {os.path.basename(path)} ({size/1e6:.1f}MB, {media_category}) -> {mid}")

    with open(path, "rb") as fh:
        seg = 0
        while True:
            chunk = fh.read(CHUNK)
            if not chunk:
                break
            boundary = "----itn" + _secrets.token_hex(12)
            body = b"".join([
                f"--{boundary}\r\n".encode(),
                b'Content-Disposition: form-data; name="media"; filename="blob"\r\n',
                b"Content-Type: application/octet-stream\r\n\r\n",
                chunk,
                f"\r\n--{boundary}--\r\n".encode(),
            ])
            _media_call(creds,
                        {"command": "APPEND", "media_id": mid, "segment_index": str(seg)},
                        body=body,
                        content_type=f"multipart/form-data; boundary={boundary}")
            print(f"  APPEND segment {seg} ({len(chunk)/1e6:.1f}MB)")
            seg += 1

    _, fin = _media_call(creds, {"command": "FINALIZE", "media_id": mid})

    # X transcodes asynchronously. Poll until it says succeeded, or give up —
    # bounded, per the anti-hang rules in DAILY_MORNING_PROMPT.md.
    info = fin.get("processing_info")
    waited = 0
    while info and info.get("state") in ("pending", "in_progress"):
        secs = min(int(info.get("check_after_secs", 5)), 15)
        if waited + secs > 180:
            raise SystemExit(f"ERROR: {path} still transcoding after 180s. Not posting.")
        time.sleep(secs); waited += secs
        _, st = _media_call(creds, {"command": "STATUS", "media_id": mid}, method="GET")
        info = st.get("processing_info")
        print(f"  transcoding... {info.get('state') if info else 'done'} ({waited}s)")
    if info and info.get("state") == "failed":
        raise SystemExit(f"TRANSCODE FAILED: {str(info.get('error'))[:200]}")
    print(f"video ready -> media_id {mid}")
    return mid


def upload_any(path, creds):
    """Route to the right uploader by extension and size."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".mp4", ".mov"):
        return upload_video(path, creds)
    if ext == ".gif" and os.path.getsize(path) > 5 * 1024 * 1024:
        return upload_video(path, creds, "tweet_gif")
    return upload_media(path, creds)


def my_user_id(creds):
    st, me = call("GET", API_ME, creds)
    uid = (me or {}).get("data", {}).get("id")
    if not uid:
        raise SystemExit(f"could not read own user id (HTTP {st}): {str(me)[:200]}")
    return uid


def retweet(tweet_id, creds):
    """Plain repost, no comment. For a quote-post use --quote instead."""
    uid = my_user_id(creds)
    st, out = call("POST", API_RT.format(uid=uid), creds, {"tweet_id": reply_id(tweet_id)})
    if st == 200 and (out or {}).get("data", {}).get("retweeted"):
        print(f"reposted {reply_id(tweet_id)}")
        return True
    if st == 403 and "already" in str(out).lower():
        print("already reposted — nothing to do")
        return True
    raise SystemExit(f"REPOST FAILED (HTTP {st}): {str(out)[:300]}")


def explain(status, payload):
    """Turn an HTTP status into something actionable at a glance."""
    if status in (401,):
        return ("AUTH FAILED — the four keys are wrong, or the access token was "
                "issued before permissions were set to Read and Write. Regenerate "
                "the access token and update itn-secrets.env.")
    if status == 403:
        return ("FORBIDDEN — keys are valid but this app isn't allowed to post. "
                "Check App permissions = Read and Write, then REGENERATE the "
                "access token (changing the setting alone doesn't upgrade an "
                "existing token).")
    if status in (402,):
        return ("BILLING — credentials are fine. The account is out of credits. "
                "Top up at console.x.com → Billing → Credits.")
    if status == 429:
        return "RATE LIMITED — too many requests. Wait and retry."
    if status == 400 and "duplicate" in str(payload).lower():
        return "DUPLICATE — X rejects identical text posted twice. Vary the wording."
    return None


def reply_id(s):
    """
    Accept either a bare tweet id or the URL you copied out of the browser.

    Nobody has the numeric id to hand -- you have the link. Taking both removes
    the one step where this gets fumbled at 11pm.
    """
    s = str(s).strip()
    m = re.search(r"/status/(\d+)", s)
    if m:
        return m.group(1)
    if s.isdigit():
        return s
    sys.exit(f"ERROR: can't read a tweet id out of {s!r}. "
             "Pass the numeric id or the full https://x.com/.../status/... URL.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", help="post body")
    ap.add_argument("--file", help="read the post body from a text file")
    ap.add_argument("--image", metavar="PATH",
                    help="attach an image (PNG/JPG/GIF, under 5MB)")
    ap.add_argument("--video", metavar="PATH",
                    help="attach an .mp4/.mov (chunked upload, transcode wait)")
    ap.add_argument("--quote", metavar="TWEET_ID_OR_URL",
                    help="quote-post that tweet with your text as the comment")
    ap.add_argument("--retweet", metavar="TWEET_ID_OR_URL",
                    help="plain repost, no comment. Ignores --text.")
    ap.add_argument("--reply-to", metavar="TWEET_ID_OR_URL",
                    help="post this as a reply to that tweet")
    ap.add_argument("--dry-run", action="store_true", help="print, don't send")
    ap.add_argument("--verify", action="store_true", help="check credentials only")
    a = ap.parse_args()

    creds = load_secrets()

    if a.retweet:
        retweet(a.retweet, creds)
        return

    if a.verify:
        status, payload = call("GET", API_ME, creds)
        if status == 200:
            u = payload.get("data", {})
            print(f"OK — authenticated as @{u.get('username')} ({u.get('name')})")
            print("Credentials are valid and the token has account access.")
            return
        msg = explain(status, payload)
        print(f"FAILED (HTTP {status})")
        print(msg or json.dumps(payload)[:400])
        sys.exit(1)

    """Reading from a file avoids shell quoting entirely — several posts contain
       apostrophes, which break single-quoted shell strings."""
    text = a.text
    if a.file:
        if not os.path.exists(a.file):
            sys.exit(f"ERROR: no such file: {a.file}")
        text = open(a.file).read().strip()
    if not text:
        sys.exit("ERROR: --text or --file is required (or use --verify)")
    a.text = text

    n = len(a.text)
    has_link = "http://" in a.text or "https://" in a.text
    print(f"--- post ({n} chars, {'with' if has_link else 'no'} link, "
          f"est. ${'0.20' if has_link else '0.015'}) ---")
    print(a.text)
    print("-" * 40)

    if n > 280:
        sys.exit(f"ERROR: {n} characters — over the 280 limit by {n-280}.")

    if a.image:
        print(f"with image: {a.image}")
    if a.reply_to:
        print(f"as a REPLY to {reply_id(a.reply_to)}")

    if a.dry_run:
        print("DRY RUN — nothing was sent.")
        return

    body = {"text": a.text}
    if a.image:
        body["media"] = {"media_ids": [upload_any(a.image, creds)]}
    if a.video:
        body["media"] = {"media_ids": [upload_video(a.video, creds)]}
    if a.quote:
        body["quote_tweet_id"] = reply_id(a.quote)
    if a.reply_to:
        body["reply"] = {"in_reply_to_tweet_id": reply_id(a.reply_to)}

    status, payload = call("POST", API_POST, creds, body)
    if status in (200, 201):
        tid = payload.get("data", {}).get("id")
        print(f"POSTED — https://x.com/thenumberdesk/status/{tid}")
        return
    msg = explain(status, payload)
    print(f"FAILED (HTTP {status})")
    print(msg or json.dumps(payload)[:400])
    sys.exit(1)


if __name__ == "__main__":
    main()

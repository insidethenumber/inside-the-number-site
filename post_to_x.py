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

import argparse, base64, hashlib, hmac, json, os, sys, time, urllib.parse, urllib.request, urllib.error, secrets as _secrets

SECRETS = os.environ.get("ITN_SECRETS", os.path.expanduser("~/Documents/Claude/Projects/itn-secrets.env"))
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", help="post body")
    ap.add_argument("--dry-run", action="store_true", help="print, don't send")
    ap.add_argument("--verify", action="store_true", help="check credentials only")
    a = ap.parse_args()

    creds = load_secrets()

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

    if not a.text:
        sys.exit("ERROR: --text is required (or use --verify)")

    n = len(a.text)
    has_link = "http://" in a.text or "https://" in a.text
    print(f"--- post ({n} chars, {'with' if has_link else 'no'} link, "
          f"est. ${'0.20' if has_link else '0.015'}) ---")
    print(a.text)
    print("-" * 40)

    if n > 280:
        sys.exit(f"ERROR: {n} characters — over the 280 limit by {n-280}.")

    if a.dry_run:
        print("DRY RUN — nothing was sent.")
        return

    status, payload = call("POST", API_POST, creds, {"text": a.text})
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

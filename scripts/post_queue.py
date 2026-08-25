#!/usr/bin/env python3
"""
Inside the Number — X posting queue.

Posts the next unsent item from posts/ to @thenumberdesk, then records what
went out. Designed to run in GitHub Actions several times a day.

Why a queue and not a generator: the posts are written and fact-checked ahead
of time. Every number that goes out has been verified once by a human or by a
run that could check it. Generating copy at post time would mean publishing
claims nobody had looked at, and this account's whole position is that it
checks its numbers.

State lives in posts/.sent.json, committed back to the repo, so the queue
survives a fresh checkout and never double-posts.

    python3 scripts/post_queue.py --dry-run     # show what's next, send nothing
    python3 scripts/post_queue.py               # send one
    python3 scripts/post_queue.py --status      # queue health

Credentials come from environment variables in CI (GitHub Secrets) or from
itn-secrets.env locally — same four OAuth 1.0a values post_to_x.py uses.
"""

import argparse, json, os, sys, glob, datetime
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
POSTS = os.path.join(ROOT, "posts")
STATE = os.path.join(POSTS, ".sent.json")

# Reuse the signing and posting code rather than duplicating OAuth.
spec = importlib.util.spec_from_file_location("poster", os.path.join(ROOT, "post_to_x.py"))
poster = importlib.util.module_from_spec(spec)
spec.loader.exec_module(poster)


def creds():
    """CI passes secrets as env vars; locally fall back to the secrets file."""
    keys = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET"]
    if all(os.environ.get(k) for k in keys):
        return {k: os.environ[k] for k in keys}
    return poster.load_secrets()


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"sent": [], "history": []}


def save_state(st):
    json.dump(st, open(STATE, "w"), indent=1)


def queue(st):
    """Unsent posts, in filename order. Numbered prefixes control sequence."""
    everything = sorted(os.path.basename(p) for p in glob.glob(os.path.join(POSTS, "*.txt")))
    return [f for f in everything if f not in st["sent"]]


# Target posting times, Central. These are intentions, not triggers — see
# --if-due below.
SLOTS_CT = [(9, 15), (12, 15), (16, 40)]


def central_now():
    from zoneinfo import ZoneInfo
    return datetime.datetime.now(ZoneInfo("America/Chicago"))


def slots_passed(now_ct):
    """How many of today's posting windows have opened."""
    return sum(1 for h, m in SLOTS_CT if (now_ct.hour, now_ct.minute) >= (h, m))


def sent_today(st, now_ct):
    from zoneinfo import ZoneInfo
    ct = ZoneInfo("America/Chicago")
    n = 0
    for h in st.get("history", []):
        at = h.get("at")
        if not at:
            continue
        try:
            dt = datetime.datetime.fromisoformat(at)
        except ValueError:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        if dt.astimezone(ct).date() == now_ct.date():
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--if-due", action="store_true",
                    help="Post only if fewer posts have gone out today than "
                         "windows have opened. Safe to call every few minutes.")
    a = ap.parse_args()

    st = load_state()
    pending = queue(st)

    # GitHub's scheduled triggers are best-effort: on Aug 24-25 the 9am slot
    # never fired, the 4pm slot ran 57 minutes late and the 8pm slot 2h36m
    # late. Rather than trust one cron to land, the workflow now wakes up
    # every 20 minutes and asks this question instead: have fewer posts gone
    # out today than windows have opened? If a trigger is dropped, the next
    # one covers for it. Posting stays capped at len(SLOTS_CT) a day because
    # the count, not the clock, is what gates it.
    if a.if_due:
        now_ct = central_now()
        due, already = slots_passed(now_ct), sent_today(st, now_ct)
        stamp = now_ct.strftime("%H:%M %Z")
        if already >= due:
            print(f"{stamp}: not due — {already} sent today, {due} window(s) open.")
            return
        print(f"{stamp}: due — {already} sent today, {due} window(s) open. Posting one.")

    if a.status:
        print(f"sent: {len(st['sent'])}   pending: {len(pending)}")
        for f in pending[:8]:
            print(f"   next: {f}")
        if len(pending) <= 3:
            print("\nWARNING: queue is nearly empty. Refill posts/ before it runs dry.",
                  file=sys.stderr)
        return

    if not pending:
        # Not an error — just nothing to say today. Exit clean so CI stays green.
        print("Queue is empty. Nothing to post.")
        print("::warning title=X queue empty::Refill posts/ with new content.")
        return

    name = pending[0]
    text = open(os.path.join(POSTS, name)).read().strip()

    n = len(text)
    has_link = "http://" in text or "https://" in text
    cost = 0.20 if has_link else 0.015
    print(f"--- next: {name} ({n} chars, {'link' if has_link else 'no link'}, "
          f"est ${cost:.3f}) ---")
    print(text)
    print("-" * 50)

    if n > 280:
        sys.exit(f"ERROR: {name} is {n} chars — over the 280 limit. Fix it and rerun.")

    if a.dry_run:
        print("DRY RUN — nothing sent.")
        return

    status, payload = poster.call("POST", poster.API_POST, creds(), {"text": text})
    if status in (200, 201):
        tid = payload.get("data", {}).get("id")
        url = f"https://x.com/thenumberdesk/status/{tid}"
        print(f"POSTED — {url}")
        st["sent"].append(name)
        st["history"].append({
            "file": name,
            "id": tid,
            "url": url,
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "chars": n,
            "had_link": has_link,
            "est_cost": cost,
        })
        save_state(st)
        spent = sum(h.get("est_cost", 0) for h in st["history"])
        print(f"queue: {len(queue(st))} remaining   est. spent to date: ${spent:.2f}")
        return

    msg = poster.explain(status, payload)
    print(f"FAILED (HTTP {status})")
    print(msg or json.dumps(payload)[:400])
    # A duplicate means the text already went out — burn it and move on rather
    # than wedging the queue on the same item forever.
    if status == 400 and "duplicate" in str(payload).lower():
        st["sent"].append(name)
        save_state(st)
        print(f"marked {name} as sent so the queue advances.")
        return
    sys.exit(1)


if __name__ == "__main__":
    main()

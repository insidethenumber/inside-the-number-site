# Cloudflare — how this site is actually served, and the traps

**The site is a Worker, not Pages.** Project `edge-report`, account
`f653b2b50f7a215f80b8f816367e0ca7`, deployed from `insidethenumber/inside-the-number-site`
on every push to `main` via `npx wrangler deploy`. There is no build command; the repo
root is uploaded as static assets.

## Trap 1 — `_redirects` only accepts RELATIVE paths

Cloudflare Workers static assets validate `_redirects` at DEPLOY time. Two things are
rejected outright, and a rejection fails the whole deploy:

- **Absolute URLs as the source.** `https://www.example.com/* ...` → *"Only relative
  URLs are allowed."* Sources must start with `/`.
- **Netlify's force suffix `!`.** `301!` parses as status `0` → *"Valid status codes are
  200, 301, 302, 303, 307, or 308. Got 0."*

**This bit us on Sep 8, 2026.** Three absolute-URL host rules with `301!` were added to
consolidate the four URL variants GSC was reporting. Every deploy from ~12:00 CT failed.
The site silently served stale content for ~90 minutes — the newsletter images 404'd and
the issue would have gone out text-only if it hadn't been routed around. **Nothing warns
you.** The push succeeds, GitHub Actions stays green, and only the Cloudflare build fails.

## Trap 2 — a failing deploy is invisible from the repo side

GitHub Actions being green says nothing about whether the site updated. **After any push
that must appear on the live site, verify the file with a real `fetch()`** — not a page
load, which can be served from cache. If it 404s, check
`dash.cloudflare.com → Workers & Pages → edge-report → Deployments` for a red build.

## Host canonicalisation lives in a Redirect Rule, not in the repo

`www` → root is a **zone-level Redirect Rule** named **"Canonical host: www to root (301)"**,
created Sep 8 2026 from Cloudflare's "Redirect from WWW to root" template:
wildcard `https://www.*` → `https://${1}`, 301, **preserve query string ON**.
Verified live: `https://www.insidethenumber.com/tools?utm_test=1` → `https://insidethenumber.com/tools?utm_test=1`.

Cloudflare warns at deploy time that `www` may not be a proxied DNS record. It deployed
and works anyway, but if www ever stops redirecting, check DNS for a proxied www record first.

**Do not try to do host redirects in `_redirects`. It cannot do them and it will break every deploy.**

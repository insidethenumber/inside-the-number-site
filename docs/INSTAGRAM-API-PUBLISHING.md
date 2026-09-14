# Instagram publishing — the API path
**Written Sep 14, 2026. This is the path to use for still images.**
(`docs/INSTAGRAM-POSTING.md` still applies to Reels, which the API path here
does not cover.)

## The short version

Drop two files in `ig/` and push. CI publishes.

    ig/<slug>.txt    the caption
    ig/<slug>.png    the image, aspect ratio between 0.8 and 1.91

Nobody logs into anything.

## Why this exists

The Meta setup finished Sep 13 — professional account, linked Page, developer
app, tester role, long-lived token through **Nov 12, 2026**. It worked; a real
post went out that night.

It failed the next day anyway, for a reason that had nothing to do with the
setup. **The token lived in a local file on a machine with no network route to
Meta.** The only way to use it was to hand it to a browser and let the browser
call the API — and that hand-off is exactly what a credential-safety check is
built to stop. One day it went through, the next it didn't, and Instagram had to
be posted by hand through a login screen on a deadline.

X never had this problem: its credentials are in GitHub Secrets and a GitHub
runner posts. This gives Instagram the same shape. Same token, same app, same
Page — moved somewhere that can reach Meta.

## The two gotchas, both now enforced in code

**1. Meta fetches the image itself.** You cannot upload bytes. The image must
sit at a public URL first, which is why the workflow copies `ig/<slug>.png` into
`assets/ig/` and pushes *before* publishing. Cloudflare's deploy lags the push
by a minute or two, so `ig_publish.py` blocks until the URL returns 200.
Publishing early yields a container that never reaches FINISHED.

**2. Aspect ratio must be 0.8–1.91.** The DFS card on Sep 14 rendered at
1080x1360 = **0.7941**, just under the floor, and would have been rejected.
`ig_publish.py` now fails the run with the measured ratio rather than letting it
reach Meta. **Pad the canvas to fix it; never crop the content** — 1360 x 0.8 =
1088, so padding 1080 to 1088 lands exactly on the floor.

## Publishing is three calls, not one

1. `POST /{ig-user-id}/media` with `image_url` + `caption` → container id
2. poll `GET /{container-id}?fields=status_code` until `FINISHED`
3. `POST /{ig-user-id}/media_publish` with `creation_id` → live media id

Skipping the poll is the classic failure: publish immediately after step 1 and
the container isn't ready.

## Operating it

    python3 scripts/ig_publish.py --status    # queue health
    python3 scripts/ig_publish.py --dry-run   # validate, publish nothing
    python3 scripts/ig_publish.py             # publish one

State lives in `ig/.sent.json`, committed back, so a fresh checkout never
double-posts. The workflow polls every 20 minutes rather than trusting one cron
to land — the lesson `x-posts.yml` learned in August.

## One-time setup (Chuck)

**Settings → Secrets and variables → Actions → New repository secret**, twice:

| Name | Value |
|---|---|
| `IG_ACCESS_TOKEN` | the long-lived token in `itn-secrets.env` |
| `IG_BUSINESS_ACCOUNT_ID` | `17841452852830364` |

I can't add these myself — the GitHub API isn't reachable from my sandbox, and
installing your own credential is the right division of labour anyway. Until
they exist the workflow fails loudly with a message naming exactly what's
missing, which is the correct behaviour: no silent skips.

## Token expiry

**Nov 12, 2026.** Refresh with:

    GET /refresh_access_token?grant_type=ig_refresh_token&access_token=<current>

Then update the GitHub Secret. Worth a calendar reminder around Nov 5.

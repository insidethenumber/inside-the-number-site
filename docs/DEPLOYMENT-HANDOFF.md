# Deployment handoff — M28 revalidated release

**Status: BLOCKED on owner authentication. Nothing has been pushed or deployed.**

| | |
|---|---|
| **Production now** | `dd29053` — "Slate brief for 2026-09-17", ITN Desk, Sep 17 19:32 UTC |
| **Production before** | `fab7551` |
| **Release branch** | `release-m28`, rebased onto `dd29053`, linear, 20 commits ahead, 0 behind, clean tree |
| **Release head** | see `RELEASE-HEAD.txt` beside this file — the guarded script checks it for you |
| **Superseded** | `cc9bb25` / `sprint-m27`. The old bundle's base was `fab7551`; do not use `deploy-m26.sh` |

---

## Why the previous deployment stopped, and why that was correct

`deploy-m26.sh` compared `origin/main` against its expected base `fab7551`, found `dd29053`, and exited before touching anything. That guard did its job. Production had advanced by one commit — the automated slate brief — and merging a release tested against an older base without re-checking is exactly the failure the guard exists to prevent.

## What actually changed in production between the two commits

```
$ git diff --name-status fab7551 dd29053
M  data/brief-2026-09-17.json
M  data/brief-latest.json
A  data/snapshots/2026-09-17-1932.json
```

**Three files, all under `data/`. Zero non-data paths.** Author `ITN Desk <desk@insidethenumber.com>`, message "Slate brief for 2026-09-17" — the automated pipeline, nothing else. Nothing in the release needed to be reconsidered on the merits; it needed to be re-based and re-tested, which is what this release is.

## Slate data preservation — verified, not assumed

```
$ git diff --name-only dd29053 release-m28 -- data/
(empty)
```

`data/` on the release branch is **byte-identical to production**. `brief-latest.json` still carries `slate_date: 2026-09-17`, and `data/snapshots/2026-09-17-1932.json` — the file production added — is present and untouched. `.github/`, `scripts/` and `wrangler.jsonc` are also byte-identical; this release changes site HTML and `sitemap.xml` only.

The rebase applied 19 commits onto `dd29053` with **zero conflicts**, so no content decision — stale-versus-current — ever had to be made.

---

## How the release was verified against *this* base

Live production was fetched and hashed route by route: all eight priority pages matched their `dd29053` blobs exactly, confirming the deployed site is current `main`. Each release page was then rebuilt in the browser from that live HTML using index-addressed chunks and SHA-256 compared against the committed file.

| Route | Rebuild = committed bytes |
|---|---|
| `/` `/nfl` `/cfb` `/games` `/mlb-playoffs` `/ufc-331-odds` `/no-vig-calculator` `/tools` | **8 / 8 exact** |

So every render below exercised the exact bytes in the release commit, not an approximation of them.

---

## Owner action — one command

```bash
chmod +x ~/Documents/Claude/Projects/"Inside the Number"/docs/deploy-m28.sh
~/Documents/Claude/Projects/"Inside the Number"/docs/deploy-m28.sh
```

It clones fresh (your project folder is **not** a git checkout — its `.git` was renamed to `.git-DETACHED-2026-09-10`), refuses to run if `origin/main` has moved off `dd29053`, refuses if the bundle head is not the expected commit, refuses if the diff touches `data/`, asks before pushing, and never forces. If production has advanced again, it will stop — that is the guard working, and the fix is another rebase, not a flag.

## Why Claude still cannot push

```
$ git push --dry-run origin release-m28:main
fatal: could not read Username for 'https://github.com'

GITHUB_TOKEN / GH_TOKEN  unset      gh cli  absent
credential.helper  none             ~/.netrc, ~/.ssh  absent
$ git ls-remote origin -h refs/heads/main   ->   dd29053...   (read works)
```

Read succeeds, write does not: an authentication gap, not a network one. A browser session signs in the GitHub web UI, which has no mechanism to accept a commit produced elsewhere. Rebuilding 35 files through the web editor would create different commits and discard tested history, so it was not attempted, and no alternate path was improvised.

## After it deploys

1. Wait 1–3 minutes for Cloudflare (`wrangler.jsonc`, Workers static assets — it builds from the repo on its own).
2. Check `https://insidethenumber.com/sitemap.xml` shows **29** entries.
3. Check the homepage board stamp reads **today**, with no "not from today" note.
4. Tell Claude it is live; it will run the post-deploy verification before anything is called done.
5. Search Console: resubmit the sitemap, request indexing for the three guides.
6. Beehiiv: the publication description still says "one free pick every morning" while the site says "0 — Picks. Ever." Replacement copy is in `PRODUCT-PROOF-REPORT.md`. Owner-only; Claude has not touched Beehiiv settings.

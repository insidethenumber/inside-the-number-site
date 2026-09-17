# Deployment handoff

**Status: BLOCKED.** Production is `fab7551`. The tested release is `cc9bb25`; this sprint's work sits on top at `2c8dc65`.

## What is waiting

| Branch | Commit | Contents |
|---|---|---|
| `sprint-m27` | **`2c8dc65`** | 13 commits on top of `origin/main` — the full M24–M26 release plus the M27 acquisition fixes |

The release is a clean fast-forward: `origin/main` is an ancestor, 0 commits behind, and nothing under `data/` is touched.

## Why Claude cannot push

```
$ git push --dry-run origin HEAD:refs/heads/main
fatal: could not read Username for 'https://github.com': No such device or address   (exit 128)

GITHUB_TOKEN / GH_TOKEN / GITHUB_PAT ... unset
gh cli ......... absent      credential.helper ... none
~/.git-credentials / ~/.netrc / ~/.ssh ... absent
```

`git fetch` and `git ls-remote` succeed, so this is an authentication gap, not a network one. Chuck **is** signed into github.com in Chrome as `insidethenumber` — but a browser session authenticates the web UI, not git, and GitHub's web interface has no way to receive a commit from elsewhere. Reconstructing 35 files by hand through the web editor would produce a different commit and discard the tested history, so it was not attempted.

## Owner action

Run on the Mac:

```bash
# if git asks for a login — browser flow, nothing typed into chat
brew install gh && gh auth login        # GitHub.com → HTTPS → Login with a web browser

cd ~/Desktop
git clone https://github.com/insidethenumber/inside-the-number-site.git itn-deploy && cd itn-deploy
git fetch "/Users/chuckwhite/Documents/Claude/Projects/Inside the Number/docs/ITN-M26-release.bundle" m24-front-door:rc
git log --oneline main..rc     # expect 12 commits ending cc9bb25
git merge --ff-only rc
git push origin main
```

`docs/deploy-m26.sh` in the project folder does exactly this with guardrails: it refuses if production moved, refuses if anything under `data/` would change, and asks once before pushing.

**The M27 sprint commit `2c8dc65` is not in that bundle** — it was created after it. Either re-export from the sandbox, or apply `docs/ITN-M27-SPRINT.patch`.

## Verify after deploying

| URL | Expect |
|---|---|
| `/` | H1 "Every Line, Explained" · board date = today · no "not from today" warning |
| `/nfl` | Read-next block · `h2` present |
| `/cfb` | Read-next block · first `h2` on the page |
| `/mlb-playoffs` · `/ufc-331-odds` | 200, context row at 390px |
| `/no-vig-calculator` | mobile row `← HOME / TOOLS / NO-VIG` · Read-next block |
| `/sitemap.xml` | **29 entries**, including all three guides |
| `/parlay` · `/dfs` | 200, and `noindex,follow` in the head |

## What this blocks

Threshold 3 of the sprint — any Search Console impression on a new guide — **cannot pass while the live sitemap omits those three pages.** Days 1, 5 and 7 of the measurement plan read zero for a reason unrelated to the content.

UFC 331 is Saturday. `/ufc-331-odds` is finished, tested and live, and Google has still never been told it exists.

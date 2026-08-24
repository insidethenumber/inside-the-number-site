#!/bin/sh
# Inside the Number — git credential helper.
#
# Why this exists: the PAT used to be embedded in the remote URL, which meant
# any innocuous `git remote -v` printed it in full. That is exactly how the
# previous token got exposed on Aug 24. Now the remote URL is clean and the
# token is read from itn-secrets.env at push time only.
#
# itn-secrets.env lives OUTSIDE the repo and is never committed.
[ "$1" = "get" ] || exit 0
SECRETS="${ITN_SECRETS:-$(dirname "$0")/itn-secrets.env}"
[ -f "$SECRETS" ] || exit 0
TOK=$(sed -n 's/^GITHUB_PAT=//p' "$SECRETS" | tr -d '\r\n" ')
[ -n "$TOK" ] || exit 0
echo "username=insidethenumber"
echo "password=$TOK"

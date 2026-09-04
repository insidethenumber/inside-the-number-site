# Newsletter visuals — spec and rationale (Sep 4, 2026)

Chuck: "can we incorporate GIFs or Graphics in the newsletter going forward?"
Yes. The operational rules live in `DAILY_MORNING_PROMPT.md`, which both
newsletter tasks read on every run. This file is the why.

## Why the ticker GIF is the right first move

We already built `scripts/viz.py ticker` on Sep 3 and never shipped it. It
animates a number sliding from where it opened to where it sits now. That is
literally the brand — the whole site exists to show what a price did — and it is
the only asset we own that no competitor's newsletter has. It also costs nothing
per issue: one command, about 190 KB, generated from numbers the routine already
pulled.

## The Outlook constraint drove the design

Outlook on Windows shows only the first frame of an animated GIF, and Outlook is
a large share of any email list. So frame one of the ticker is a complete
message on its own: headline, the opening number, and OPEN / NOW labelled at
both ends of the track. Readers on Gmail and Apple Mail see the number travel;
readers on Outlook see a clean static card. Nobody sees a broken half-idea.

## Why we host on our own domain

`assets/newsletter/<date>/` in the repo, served by Cloudflare at
insidethenumber.com. Free, permanent, on-brand, and immune to a third-party
image host expiring a link two months from now — which is exactly what happened
to the Canva export URLs used for the Sep 3 X cards, which died the same night.

## Honest note on priority

The list is 4 subscribers, all Chuck's own addresses. Images will not grow it —
distribution will (see ACQUISITION_PLAN_2026-09-04.md). This was cheap to build
and makes the issue more forwardable, which is worth something once real people
are on the list. It is not a growth lever and should not be treated as one.

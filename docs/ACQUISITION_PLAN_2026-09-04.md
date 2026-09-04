# The distribution problem — Sep 4, 2026

Written after Chuck asked two questions: do we have subscribers beyond the
four, and how is traffic. The answers are no and thin. This is what I think we
should do about it, with the part that needs Chuck's hours separated from the
part I can run alone.

---

## 1. What the numbers actually say

Pulled live Sep 4, 2026.

| Metric | Value | Source |
|---|---|---|
| Newsletter subscribers | **4** — all Chuck's own addresses | Beehiiv |
| Real outside subscribers | **0** | Beehiiv |
| Site visits, 30 days | 490 (780 page views) | Cloudflare |
| Site visits, last 24h | 23 (42 views) | Cloudflare |
| X followers | **37** | x.com |
| Views on a typical ITN original post | **26–188** | x.com |
| Views on today's Parlay of the Day post | **70** | x.com |
| Views on threads we replied into today | 9.6K, 11K, 22K, 32K, 97K | x.com |
| Pages indexed by Google | ~30–40 | site: query |
| Rank for a real long-tail term | **not in top 12** | Google |
| Rank for "inside the number betting" | 1 | Google |

### The finding that matters

**Our original posts reach nobody. Our replies reach everybody.**

A post we spend an hour building — verified numbers, custom graphic, tested
caption — goes out to 37 followers and gets 70 views. A reply that takes four
minutes lands under a post being read by 97,000 people.

That is a ~1000x difference in reach per unit of effort, and we have been
spending our effort on the wrong side of it. Ten mockups is not the problem;
the problem is that whichever mockup we pick gets shown to 70 people.

### The second finding — CORRECTED Sep 4, after Chuck pushed back

I originally wrote that 490 visits producing 0 signups proved a conversion
problem on top of a traffic problem. Chuck's response: "all of the traffic is
you, pinging the page." He is right, and I should have checked before drawing a
conclusion from it.

The evidence he is right:

- **`/record` is in the 30-day top-URL list.** That page was deleted weeks ago.
  Nobody outside this project has a link to it. Those loads are ours.
- **`/top2-preview` is in the list.** A preview page that was never linked from
  anywhere public. That is purely internal.
- **Today: 42 page views.** In this session alone I loaded /cfb four times,
  /parlay three times, plus the homepage, /tools and /games while verifying
  fixes. That is most of today's number by itself.

So the 490 is largely me verifying my own work, and a smaller amount of Chuck
checking pages. **Real outside traffic is a small fraction of it — plausibly
tens of visits a month, not hundreds.**

**What this changes:** the "0% conversion" claim is unsupported. You cannot
diagnose an offer from traffic that is mostly your own browser. There is one
problem, not two: **almost nobody has ever seen this site.** The offer might be
weak, and I still think leading with the honest-price angle is right on the
merits — but it is untested, and I should not have presented it as diagnosed.

**Process fix, so the number becomes trustworthy:**

1. *My side, effective immediately:* verify with `fetch()` rather than real
   browser page loads. Fetch does not execute page JavaScript, so the analytics
   beacon never fires. Browser loads only when I genuinely need to see rendering.
2. *Site side:* Web Analytics is on "Automatic setup", so Cloudflare injects the
   beacon at the edge and there is no script tag to guard. Switching to manual
   setup would let us wrap it in a `localStorage.itn_internal` check, so Chuck's
   own browsing stops counting too. Worth doing before we make any decision off
   these numbers again.
3. *Until then:* treat all historical traffic figures in this project as
   contaminated. Do not cite the 490.

---

## 2. Why the offer isn't converting

Our headline promise is "one free pick every day with the reasoning shown."

Every tout site on the internet offers a free daily pick. The reader has no way
to tell us apart from the 10,000 accounts promising the same thing, and their
prior on all of them — correctly — is that it is noise. We are asking for an
email address in exchange for a thing they already believe is worthless.

Meanwhile the actually differentiated thing we do is buried: **we tell people
what a price costs them.** The break-even math, the de-vigged fair number, the
"what beats it" line, the parlay gap. Nobody else publishes that, because it
makes their product look bad. It is the only reason a stranger would trust us
over a capper with a bigger following.

**The offer should lead with that and stop competing on picks.** Something like:
*"The number, before the noise. Every day: what the line actually implies, what
it costs you, and what beats it."* Then the free pick is a bonus, not the pitch.

That is a copy change, and I can make it, but I want Chuck's read first because
it changes what the brand is selling.

---

## 3. What produces strangers, ranked by yield per hour of Chuck's time

Zero budget assumed. Ordered by what I actually expect to work at our size.

### Tier 1 — needs Chuck, highest yield

**Reddit.** r/sportsbook's daily threads are read by tens of thousands of people
who are *already* arguing about numbers. A comment that de-vigs a price and
shows the break-even is native content there, not marketing. This is the single
best fit for what we do, and it has been blocked for weeks: item #101 on the
punch list, pending since August. The old account was banned; a real account
with genuine comment history is required, and Reddit is aggressive about
detecting automation, so **this has to be Chuck, by hand, no links for the
first two weeks.** 20 minutes a day. I write the comments, Chuck posts them.

**Betting Discords and group chats.** Same logic, smaller rooms, warmer. A human
who shows up with a real number every day becomes the person people ask. Cannot
be automated, cannot be faked. 15 minutes a day.

### Tier 2 — I can run this alone, starting now

**X replies at 5x volume.** This is the one channel I can operate without Chuck.
Today I did 6 replies. The ceiling is 40–60 a day into threads with 10K+ views,
one per account, always with a verified number. Expected: this is how we go from
37 followers to a few hundred. It will not produce subscribers directly — it
produces the audience that later clicks a link.

**Cut originals to 2–3 a day.** They are for credibility and the record, not
reach. The effort saved goes into replies. This inverts what we have been doing.

### Tier 3 — real ceiling, real cost

**Short-form video.** The parlay slip card is already 80% of a 30-second clip:
"here's what this parlay actually costs you." TikTok and YouTube Shorts have
discovery that X and Google do not — a zero-follower account can reach 50,000
people. This is the only channel on the list with a genuine shot at step-change
growth. Cost: Chuck on camera or a voiceover, 30–45 min per clip. Worth testing
three before committing.

### Tier 4 — keep doing, expect nothing soon

**SEO.** The site is indexed, fast and structured correctly. It will not rank
for anything competitive for 6–12 months at this domain age, and never for
"parlay of the day" or similar head terms — those belong to Action Network and
Covers. Long-tail calculator pages are the realistic target. Keep publishing,
do not count on it this season.

**Beehiiv recommendation network.** Already enabled. It trades subscribers with
other newsletters, so it does nothing until we have subscribers to trade. It is
a flywheel that cannot start from 4.

**Paid ads.** Not until the funnel converts. Paying to send people into a 0%
conversion page burns money to prove something we already know.

---

## 4. The honest arithmetic

At a 1% visit-to-subscriber rate — optimistic for cold traffic — 100 subscribers
needs ~10,000 visits. We are at *tens* of real visits a month once our own
loads come out. That is not a 20x gap, it is closer to 100x, and no amount of
site polish closes it.

Which means: **the next month should be almost entirely distribution, and the
site should be treated as done.** It works, it is fast, the numbers on it are
right, and as of today the navigation finally works. Every further hour spent on
features is an hour not spent finding readers.

---

## 5. What I recommend, concretely

**This weekend (CFB Saturday is the biggest traffic day of the year):**
- I run X replies hard — 40+ a day, football-first, every one carrying a real
  number. Originals drop to 2.
- Chuck sets up the Reddit account properly and starts commenting. I write them.
- We rewrite the homepage offer to lead with the price/cost angle, not "free pick"
  — on the merits, not because the data proved it. The data proves nothing yet.

**Next two weeks:**
- Reddit daily, 20 minutes, Chuck.
- Test three short-form videos off the parlay cards.
- Hold all new site features unless they directly serve conversion.

**Measurement, so this is not vibes:** check subscribers, visits and followers
every Monday. If four weeks of this produces fewer than 25 real subscribers, the
offer is wrong, not the effort — and we change the offer, not the volume.

## 6. What I need from Chuck

1. **A decision on the offer rewrite** — lead with the honest-price angle?
2. **The Reddit account**, working, this weekend. This is the biggest unblock.
3. **Search Console access** — Chrome is signed in as ccwhite1101@gmail.com; the
   property is under another Google account. Impressions data would tell us which
   terms we are close on instead of guessing.
4. **A yes/no on short-form video**, because it needs him, not me.

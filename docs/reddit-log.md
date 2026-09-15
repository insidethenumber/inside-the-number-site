# Reddit log — u/kceza1

One line per comment. Started Sep 14, 2026.

**Why this file was empty until now.** The `itn-reddit-rounds` task has required
this log since it was written, and it never produced a single line. On Sep 14 we
found out why: the task told itself to "post via the browser", and the only
browser an unattended run has **refuses reddit.com outright** ("not allowed due
to safety restrictions"). The sandbox has no network route to Reddit either, and
no Reddit API credentials exist. So it woke up three times a day, hit a wall, and
exited without saying anything. Days of that. Nobody knew because nothing failed
loudly and this file was never checked.

Task is disabled until posting moves to GitHub Actions with a Reddit script app,
the same fix applied to Instagram the same night.

| Date | Sub | Thread | Survived | Notes |
|---|---|---|---|---|
| Sep 14 2026 | r/nfl | NFL Week One Underreactions | yes | CHI/CAR total: opened 44.5 (-110/-110), closed 47.5 (over -105 / under -115), final 96. Posted via Chuck's Chrome with him present. Confirmed live in-thread at `?sort=new`; the profile page was cached and lagged several minutes — **check the thread, not the profile.** |

## Lessons already paid for

- **Profile pages lie for a few minutes.** `/user/<name>/comments` is cached. To
  confirm a comment stuck, open the thread with `?sort=new`.
- **Reddit uses single-key shortcuts.** Clicking the comment box then typing
  immediately sent `s` (save) and `h` (hide) to the page instead of the field.
  Click, confirm focus is in the field, then type.
- **Don't force the number into the wrong thread.** Sep 14: had a verified
  Houston/Texas Tech move (opened TTU -12.5, now -7.5, total posted OFF) but the
  only r/CFB thread on that game was about the marching band. Skipped it. A
  line-move take in a band thread is spam, and on an 18-karma account spam gets
  you filtered. Posting fewer is correct.
- **Voice, per Chuck Sep 14:** "pretty lengthy and pretty nerdy. Be a little more
  funny and less wordy." Four sentences max, one number, lead with the funny part.

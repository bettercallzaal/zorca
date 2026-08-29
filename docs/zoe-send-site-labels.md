# Send-site labels for the zero-reply ZOE types

**For:** the send-budget lane, which tagged four of the zero-reply types from
code and correctly refused to guess the rest.
**Evidence:** the ZOE chat export, 9,627 bot messages, 2026-03-28 to
2026-08-27, plus a string search of the ZOE bot source tree on this machine.
**Companion:** `zoe-analysis-2026-08-27.md` (volume, bands, reply rates).

## How to match

**Normalise whitespace before matching anything.** The export writes
inline-keyboard button labels separated by newlines and runs of spaces, so
`POST REGEN SKIP` is not a contiguous string in the raw text. Matching it
literally misfiled 329 social drafts in the first pass of the analysis - as
conversational answers, work reports and event promos. Collapse `\s+` to a
single space, then match.

Every matcher below is anchored to the **first line** of the normalised text
unless stated otherwise. Counts are over the full 151-day window.

## Two of the five types are not what the name suggests

Before wiring anything, note that two of the labels handed to me do not
survive contact with the messages:

- **`event promo` is 2 messages, not 28.** The fractal and Monday-cobuild
  promos carry POST/REGEN/SKIP approval buttons - they are social drafts
  awaiting a tap, and they belong to the draft budget, not a promo budget.
  Only two announcements ("Lunch stream today...", "Lunch stream 11:30am ET.
  Come hang.") are genuine one-way promos.
- **`recurring status report` is four independent senders**, not one type. A
  single budget rule over the group would throttle them together when their
  schedules, volumes and owners differ. They are split out below.

## The labels

### 1. `fleet report` - 103 messages, Jun-Aug, ZERO replies

Three distinct emitters share this label. Match any of, on the first line:

| Matcher (first line, normalised) | N | Send time |
|---|--:|---|
| `Fleet health <MM>-<DD>:` | 55 | 06:00 daily |
| `=== ZAO FLEET <MM>-<DD> <HH>:<MM> UTC ===` | 24 | 08:45 daily |
| `FLEET OUTPUT - <N>` | 23 | 08:00 daily |

Regex: `^(Fleet health \d{2}-\d{2}:|=== ZAO FLEET .* UTC ===|FLEET OUTPUT - \d+)`

**Send site:** `bot/src/zoe/fleet-health.ts` exists and builds fleet-health
text, but its own comment scopes it to the morning brief, and none of the
three literals above appear anywhere in the bot source. The standalone 06:00
/ 08:00 / 08:45 sends are **UNMAPPED** - VPS-side, not in this git history.
Same drift pattern as the heartbeats.

### 2. `ecosystem watch` - 60 messages, Jun-Aug, ZERO replies

Matcher: first line starts `Ecosystem watch - ` followed by a weekday and
date (`Ecosystem watch - Tue Jul 21`).
Regex: `^Ecosystem watch - `
Send time: **09:00 daily**, no exceptions in the record.
Stable body field: `<N> repos, <N> open PRs total`.

**Send site: UNMAPPED.** The string does not appear in the bot source tree.

### 3. `build-candidate approval` - 129 messages, ZERO replies

All 129 were sent on **a single day, 2026-08-04**, between 04:45 and 14:42 -
roughly one every four minutes for ten hours. 120 distinct titles.

Matcher: first line starts `BUILD CANDIDATE #` followed by a numeric id.
Regex: `^BUILD CANDIDATE #\d+:`
Stable fields in the body: ` why: `, ` draft: `, ` approve: `.
The id in the first line is the same id used by the approve path.

**Send site: SPLIT.**
- *Confirmed:* `bot/src/zoe/build-candidate.ts` owns the tap-to-approve
  inline buttons, and `bot/src/zoe/index.ts` handles the callbacks
  `bc:approve:<id>` and `bc:skip:<id>`. That is the answer half.
- *UNMAPPED:* the literal `BUILD CANDIDATE #` text is composed upstream by
  the fleet escalation path (a loop draft handed to an escalate step), which
  is not in this repo. **The budget must be applied at the escalation
  producer, not at the button module** - throttling the button module would
  suppress the approval UI while the sends kept coming.

### 4. `bot activity log` - 42 messages, Jul-Aug, ZERO replies

Matcher: first line starts `ZOL followed `.
Regex: `^ZOL followed \d+/\d+ today \(mirroring @[a-z]+'s follows\)( \[DRY RUN\])?:`
Send time: **15:01 daily** (41 of 42; the one outlier is the single
`[DRY RUN]` message on 2026-07-13 at 16:15).
Only two shapes exist in 151 days - live and dry-run.

**Send site: UNMAPPED.** `bot/src/zoe/zol-queue.ts` exists but contains none
of these literals; the follow-mirroring job is not in this repo.

### 5. `affirmation prose` - 48 messages, Aug only, ZERO replies

Two fixed texts, alternating, never varied in 24 days each:

| Matcher (first line prefix) | N | Send time |
|---|--:|---|
| `I know who I am and I own the path I've chosen.` | 24 | 06:00 daily |
| `As the night settles, I reflect with gratitude` | 24 | 23:00 daily |

Regex: `^(I know who I am and I own|As the night settles, I reflect)`

**Send site: UNMAPPED.** The two texts are stored on this machine in a
private wellness-affirmations note dated 2026-08-18, so the *content source*
is identified, but nothing in the bot source reads it or sends it. The 06:00
and 23:00 cron that emits them is not in this repo.

Worth flagging to whoever owns it: these two strings are the purest case in
the whole record - 48 identical messages, zero replies, and they bracket
Zaal's day at 06:00 and 23:00, inside the 22:00-07:00 window the analysis
flags as 21% of all traffic.

### 6. `team tracker` - 1 message, Jun, ZERO replies

Matcher: `^Team tracker - \d+ open:`
**Send site: CONFIRMED - `bot/src/zoe/team-tracker.ts`**, registered from
`bot/src/zoe/index.ts`. One send in 151 days; a budget rule here buys
nothing, but the label is exact.

### 7. `event promo` - 2 messages, ZERO replies (see caveat above)

Matcher for the two genuine promos: `^Lunch stream`.

The 26 messages previously carrying this label are **social drafts** - match
them with the draft matcher (whitespace-normalised `post regen skip`), not
here.
**Send sites for those, CONFIRMED:** `bot/src/zoe/posts/fractal-promo.ts`
(the 18 `fractal tomorrow 6pm EST` drafts, 15:00) and
`bot/src/zoe/posts/drafters.ts` (the 8 `monday cobuild` drafts).

## Types the lane did not name but that also drew zero replies

Same window, same attribution. Listed so the budget covers the whole set
rather than the five that were asked about.

| Type | N | Matcher (first line) | Send site |
|---|--:|---|---|
| watchdog/restart | 266 | contains `watchdog` or `froze -> restarted` | UNMAPPED |
| provider limit / credits | 99 | `FLEET BRAIN DOWN (NO_CREDITS)`, or body matches `hit your (weekly\|monthly) limit` | UNMAPPED |
| agent-bus relay | 75 | `^BUS from `, `^BUS coordinator `, or `bus: <N> new message(s):` | UNMAPPED |
| cost report | 24 | `^Cost-of-pass \d{4}-\d{2}-\d{2}:` | UNMAPPED |
| cockpit digest | 5 | `Cockpit - <date>` (may be prefixed `(N/N)`) | UNMAPPED |

## Where the cron lives, for the ones that are in the repo

`bot/src/zoe/scheduler.ts` is the node-cron host for the scheduled nudges
that *are* in this repo. It is named here as the place to add a budget gate
for those, **not** as the send site of any UNMAPPED type above - none of
their literals appear in it, and attributing them there would be the guess
this file exists to avoid.

## What UNMAPPED means here

Nine of the twelve zero-reply types have no emitter in the bot source tree on
this machine. That is consistent with the known drift in this estate: jobs
get stood up directly on the box and never land in git. **A send budget
implemented only in the bot repo would not throttle them.** The budget needs
a chokepoint at the Telegram send call itself, or these types keep sending at
full volume regardless of what the repo says.

---

*Note on paths: this file names repo-relative source modules, which the
sibling analysis deliberately avoids. They are module names, not hosts, keys
or accounts, and the file is useless to the send-budget lane without them.
Strip section-by-section if this repo's public status makes that the wrong
trade - the matchers stand on their own.*

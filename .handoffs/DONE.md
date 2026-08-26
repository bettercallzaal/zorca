# DONE - stage 1, Mac half built and tested (task_a6082d860006)

Nothing pushed. Nothing running. No pane was ever created during this build -
every test ran against a stub `orca` in a sandboxed HOME.

## Built

| Path | What |
|---|---|
| `bin/zorca-actuator` | The Mac-side drain. Config-driven, preflighted, exactly-once, TTL-enforcing, reaper on start, pane readback before success. |
| `bin/zorca-lane-enqueue` | The VPS-side append. Also the executable definition of the queue record, so the two halves cannot drift. |
| `bin/zorca-actuator-test` | 16 cases, all passing. Stub `orca`, sandboxed HOME, no paid session possible. |
| `docs/DESIGN-bridge.md` | v3. Live plan is section 12. |

`./bin/zorca-actuator-test` -> **16 passed, 0 failed.**
`--check` against the real `orca` and the real GUI on 7777 -> **preflight ok.**

## The four instructions, and where each is enforced

- **Port from config, no default, fails loudly.** `config()` lists every
  missing key at once and exits 2; `preflight()` refuses to start if the
  configured port does not answer `/api/state`. There is no fallback port
  anywhere in the file. Tested: unset, and set-but-unreachable.
- **TTL at build time.** A record with a past `expiresAt` **or none at all**
  is refused and reported `expired` - no pane. Tested both.
- **Reaper at build time.** Any row left `claimed` by a dead process is
  closed as an error on the next start, so nothing sits invisible. Tested.
- **run-use first, `dispatch --inject` always, readback before success.**
  All three asserted in the suite; the readback case proves an unbriefed
  pane reports ERROR rather than DONE.

## One hazard the tests found, and the fix

Exactly-once originally rested on a single local state file. Destroy it and
every unexpired request re-runs - a second paid pane per request. The queue
is append-only and already carries a result record per handled request, so
the drain now treats **the queue as the durable evidence and state as a
cache**. Tested by deleting the state file: no duplicate.

## Deliberately NOT done

- **Not wired into `zorca up`.** It spawns paid panes, no config exists yet,
  and the SSH direction is unratified. Starting it automatically would be
  wrong on all three counts. It also avoids editing `bin/zorca`, which the
  `zorca-gui2` lane is actively changing.
- **`zorca-gui2` untouched**, as instructed. Note both 7777 and 7778 answer
  `/api/state` right now, so the double-actuator question in section 12 is
  live, not hypothetical.
- **Stage 1a/1b (webhook + `/lane` conversation) are ZOE-side**, in ZAOOS,
  and are not this repo's to deploy. `zorca-lane-enqueue` is the contract
  they call; the ZOE change is small and unambiguous because of it.

## Needs Zaal before this can run

1. **The SSH direction.** Config supports both (`queue.mode`), and neither is
   defaulted. The measured position is unchanged: VPS-to-Mac push cannot work
   today - `tailscale status` reports stopped and nothing listens on 22 - so
   `mode: "ssh"` (Mac dials out, queue file on the VPS) is the only variant
   that runs now and the only one that literally keeps zero inbound ports.
2. **A config file** at `~/.zao/zorca-actuator.json`. None was created; the
   real path is untouched.

## Flag: a mid-turn instruction arrived truncated

Received: *"e delete call stay Zaal's - do not touch either."* The head is
missing, so **two** things are named as Zaal's and I can only see the second.
I have not pushed, deleted, or removed anything, and I touched no file
outside the three new `bin/` scripts plus this handoff and the design doc, so
the instruction is satisfied under any reading - but I am not guessing which
two things it named. Please re-send the head.
- 2026-08-26 grill fix VERIFIED, not applied by this lane - it had already landed as `zaal-dotfiles a979b96` (Zaal, 13:06), parsing the timestamp instead of the string compare this lane proposed, which was wrong on garbage dates in both directions. Deployed `~/bin/zao-status-refresh` is byte-identical to that commit. Ran the refresh: `grill` 200, `grill_queued` 380 - two distinct quantities now, which is the proof the 12h window clause is live (both read 381 before). Backup at `~/.zao/archive/zao-status-refresh.2026-08-26-prefix.bak`. Detail: `.handoffs/grill-jammed-381-rootcause.md`.
- 2026-08-26 OPEN, UNRESOLVED - needs a live answer to settle: **zero grill verdicts recorded since 2026-08-24** while ~190 cards/day were sent. This is now causing a real jam, not a reported one: windowed outstanding hit the 200 ceiling and the gate has sent nothing since 18:02 UTC (2h53m silent). Last `verdict-synced` in the journal is Aug 24 14:22; no grill errors since. Cannot be settled from state alone - it needs one live card answered from Telegram to see whether `answered` gains a key, which separates "Zaal stopped tapping" from "the verdict-write path broke on the 24th". Store: `/home/zaal/.zao/zoe/backlog-grill-state.json`.
- 2026-08-26 cycle 1 - :7778 SINCE YOU LAST LOOKED surface. Two new sources merged into one time-ordered feed: the vault daily log (`~/zao-vault/daily/<today>.md`, `## HH:MM` headings plus their first bullet) and last-commit-per-live-worktree (`git -C <pane cwd> log -1`, proof of work rather than pane text). NEW marks come from a per-browser last-look stamp in localStorage, read once per load so polling cannot erase it mid-session. Every stat cell now names where its number lives. Timestamps are parsed, not string-compared (a979b96): an event whose time will not parse renders `??:??`, is never counted new, and is never dropped. Phone 390: counter 53px, feed 371px, action list header on the first screen; no horizontal scroll at 390/768/1280. Screenshot `/tmp/zorca-7778-phone-since.png`. File `gui/zorca-gui2`.
- 2026-08-26 cycle 2a - :7778 STUCK surface, stale-claim detection. A lane at rank 3-4 that has held its state past 45 min with no commit landed in its worktree since the claim began. orca-board reports state but not since-when, so zorca observes it: state per handle written to `~/.zao/zorca-claims.json` every refresh, timestamp moves only on a real state change. A pane first seen already working reports "at least Nm" - a duration not observed is never reported as one that was. Excluded by design: rank<=2 (blocked on Zaal, that is rail 1's job), rank 5-6, and any cwd that is not a git repo (cannot measure, so no judgement). Count also rides the lanes strip cell so the glance catches it without scrolling. Screenshot `/tmp/zorca-7778-phone-stuck.png`. File `gui/zorca-gui2`.
- 2026-08-26 cycle 2b - :7778 CLAIMS OUTLIVING THEIR LANE. Rows in `~/zao-vault/handoffs/IN-FLIGHT.md` whose lane has no live pane: 24 of them right now, oldest 8 shown, oldest first. Newest row per lane; lane-to-pane matching is containment on the alphanumerics of both (fractal runs in ZAOfractal), stated on the surface rather than hidden. Rows that say the lane closed are excluded - an accurate record is not an outliving claim. Dates parsed, not compared (a979b96): an unparseable date renders "date unreadable - shown anyway" and is never dropped, since an undateable claim is the kind that has sat longest. Not tappable: there is no pane to focus and the fix is a human closing the row. Cost the feed one phone row (4 -> 3) to keep the action list above the fold at 390x844 - firstAction 739. Screenshot `/tmp/zorca-7778-phone-stuck.png`. File `gui/zorca-gui2`.
- 2026-08-26 cycle 3a - :7778 ESTATE AT RISK stat. Nothing persists a mac-estate sweep - `~/bin/repo-cleanup` prints and exits - so this measures it: `git status --porcelain` and `git rev-list --count @{u}..HEAD` across the live worktrees on the board, scoped there on purpose because the full 48-clone estate would cost more than it tells you every 20s. Live right now: 6 dirty, 7 unpushed, 4 no remote across 15 worktrees. A repo that cannot be read counts as `unreadable`, never as clean - `sh2()` was added so a git crash is distinguishable from a clean tree. A blank board returns unknown, not a reassuring zero. Full-estate sweep date parsed from `~/zao-vault/notes/repo-estate.md` (2026-08-25) and stated in the fold. Paid for the height by folding the feed on phone: the count stays visible at top, the rows sit one tap down; firstAction 584, above the fold. New "Where these numbers live" block in the reference fold states complete provenance for all eight surfaces. Screenshot `/tmp/zorca-7778-phone-estate.png`. File `gui/zorca-gui2`.
- 2026-08-26 cycle 3b - :7778 OLDEST DRAFT stat. `~/.zao/orca-drafts.json` read directly instead of through `queue_read()`, which returns [] on any failure and so cannot tell an empty queue from an unreadable one - the same collapse `sh()` made. Four states, all distinct on screen: "none queued" (nil), "Nm waiting - N queued" (ok/gold/warn past 1h/6h), "age unknown - N queued" when every item lacks a usable ts, and "unknown" when the file will not parse. A draft with no usable ts is counted `undated` and never assumed fresh. Fixture-tested per branch: missing file, empty list, bad JSON, JSON that is not a list, oldest-not-newest, mixed dated/undated, all-undated. Live: 4m waiting, 4 queued. Strip is now 6 cells at 2/3/6 columns for 390/768/1280; firstAction 584, above the fold. Screenshot `/tmp/zorca-7778-phone-strip.png`. File `gui/zorca-gui2`.
- 2026-08-26 cycle 4 - :7778 trend on every strip stat, against the reading from before your last look. Server keeps a bounded observation history in `~/.zao/zorca-trend.json` (24h at one sample per refresh) and serves it decimated to one sample per 10 min, max 150 points. A stat that could not be measured is recorded as null, never zero - a zero would read as a real observation and a later comparison would invent a trend out of a failed scrape. Five outcomes stay distinct on screen and were each fixture-tested: "first look on this browser - no baseline yet" (no mark), "nothing measured before your last look" (no sample at or before the mark), "no observations recorded yet" (empty history), "waiting unchanged since 6:39 PM" (equal reading), and a signed delta coloured by whether up is good for that stat. A single reading never yields a direction. Watcher declares itself out: "freshness, not a stock - no trend". Signed numbers rather than glyphs, per the no-decorative-symbols rule. firstAction 689, above the fold. Screenshot `/tmp/zorca-7778-phone-trend.png`. File `gui/zorca-gui2`.


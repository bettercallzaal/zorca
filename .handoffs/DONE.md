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

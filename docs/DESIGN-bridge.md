---
type: design
status: proposed
version: 2
created: 2026-08-26
updated: 2026-08-26
component: ZOE v2 lane control (was "zorca-bridge")
decides: transport from the VPS to this Mac, the /lane chain, build order
---

# ZOE v2 - lane control from chat

Zaal drives ZORCA lanes from Telegram: `/lane <request>` becomes a real Orca
lane - worktree, pane, brief, dispatch - without touching the Mac.

**Design only. Nothing here is built.** Every measurement is dated
2026-08-26 and shown as the command that produced it. Inferences are marked
as inferences.

## 1. What v2 changes

v1 of this document asked three questions. Zaal answered them, and two
answers overturn v1's recommendation. Recording that rather than quietly
rewriting:

| Question | v1 said | Zaal's verdict | Consequence |
|---|---|---|---|
| Own bot or fold into ZOE? | leaned own bot, front end on the Mac | **Extend ZOE in place.** `@zaoclaw_bot` keeps its identity, audience and VPS deploy; v2 lands as versions. | **v1's core recommendation is dead.** The front end is on the VPS from day one. The transport hop v1 deferred to stage 4 is now stage 1's hardest part. |
| `/lane` at all? | flagged it as spending money on a lock-screen tap | **Yes, and bigger than v1 imagined.** Not "resume a parked lane" - `/lane <request>` creates a new planned lane through the orchestrator. Highest-value feature. | It is stage 1, and it unblocks the rest. The money concern does not disappear; it becomes a confirm step and a TTL (section 3.3). |
| Telegram or Discord first? | open | not picked; recommendation requested | Section 6. |

What survives v1 unchanged, because it was measured rather than assumed:

```
$ ls -la /opt/homebrew/bin/orca
/opt/homebrew/bin/orca -> /Applications/Orca.app/Contents/Resources/bin/orca
```

The `orca` CLI is a bash shim into a macOS `.app`. **The actuator is
Mac-forced.** No VPS and no container can run it. That is why this document
is mostly about a transport.

OpenMatter's status also survives, with Zaal's refinement: runtime candidate
for **new capability**, never a rewrite of something that already runs
(section 7).

## 2. The shape

Three processes, three hosts, one direction of travel.

```
  Telegram  ──▶  ZOE v2 (Hostinger VPS)  ──▶  bot_commands queue (Supabase)
                                                        │
                        the Mac polls outbound ─────────┘
                                                        ▼
                                          zorca-actuator (this Mac)
                                                        │
                                            POST 127.0.0.1:7777
                                                        ▼
                                                  orca CLI, panes
```

**Nothing ever connects INTO the Mac.** The Mac makes outbound HTTPS calls
and nothing else. This is the property the whole design is bought for.

## 3. The transport - the actual question

### 3.1 The three candidates

| | **A: SSH from VPS to Mac** | **B: :7777 over Tailscale** | **C: command queue the Mac polls** |
|---|---|---|---|
| Direction | VPS dials the Mac | VPS dials the Mac | **Mac dials out only** |
| Needs on the laptop | sshd, an authorized key, an open port on the tailnet | the GUI rebound off `127.0.0.1`, or a tunnel | nothing |
| Depends on Tailscale | yes | yes | **no** |
| Mac asleep / moved network | **fails** | **fails** | **queues, runs on wake** |
| Verb surface | **arbitrary shell** | the 4 reviewed endpoints | **a fixed enum, server-enforced** |
| Double-execute safety | none | none | **atomic claim, measured** |
| New code | ssh wrapper | bind change + auth | actuator + one authz change |
| Latency | instant | instant | one poll interval |

### 3.2 Recommendation: C, the command queue - and it already exists

Not a new build. `ZAOcowork` already ships this control plane, and ZOE
already speaks it.

Measured in `ZAOcowork` today:

- `POST /api/v1/bots/commands` enqueues. `GET /api/v1/bots/commands?bot=<self>`
  pulls.
- **The pull is an atomic claim.** The route updates
  `status pending -> claimed` in the same statement it selects, so two
  pollers cannot double-execute. This is in the code, not aspirational.
- **A token can only pull its own bot's queue** - `if (self !== caller)
  return 403`.
- **The verb list is a server-enforced enum**, not free text:
  `restart | pause | resume | run_task | ask` for bot-self,
  `start | stop` for the fleet agent. An unknown command is rejected 400.
- `POST /api/v1/bots/commands/:id/result` closes the loop; a token may only
  complete a command addressed to its own bot.
- `supabase/migrations/012_bot_commands.sql` states the design intent in its
  own header: *"Pull-based: the board never connects to the VPS."*

And on ZOE's side, in the ZAOOS repo: `bot/src/lib/cowork.ts` is already a
bot-token client for `/api/v1/*`, already calling `/api/v1/bots/heartbeat`
and `/api/v1/items`. Adding a lane enqueue is a method on an existing client.

The queue's own migration header is the argument for C, inverted: it was
built so the board never dials the VPS. We need the VPS never to dial the
Mac. Same property, same mechanism, opposite direction.

**Why not A (SSH).** It puts a long-lived inbound key on a laptop that
sleeps and changes networks, reachable only over Tailscale - which is
**currently stopped** on this Mac (`tailscale status` -> `Tailscale is
stopped`, measured today) and whose DNS gap is a recorded failure that hits
precisely when Zaal is mobile, which is the only time this feature matters.
Worse, it makes the transport arbitrary shell execution at the exact moment
we are trying to keep the verb list finite and reviewed. Option C's verb
enum is enforced by a server neither end controls.

**Why not B (:7777 over Tailscale).** Same Tailscale dependency and the same
sleeping-laptop failure, plus it requires rebinding the GUI off
`127.0.0.1` - the one line v1 committed to never touching. B is A with a
smaller verb list, and it still fails when the Mac is closed.

### 3.2b The GUI port is not a constant - noted, not resolved

A concurrent lane is building `gui/zorca-gui2` on **7778, running beside
7777** (commits `a5b2786`..`5b2bdfa`, landed while this document was being
written). Measured: gui2 exposes the identical write surface -
`/api/resolve`, `/api/focus`, `/api/lane`, `/api/draft` - so the design's
write path is unaffected in shape.

But the actuator must not hardcode a port. It reads one from config,
defaulting to whatever `zorca up` starts, and **fails loudly if the port
answers nothing** rather than silently doing no work. Two GUIs on two ports
is also a live double-actuator question - if both are running, a lane
resolved through one should not look pending in the other.

Per playbook rule 5 this lane does not touch `zorca-gui2`; its owner does.
Flagging it as a finding for that lane and for Zaal.

**What C costs, stated plainly.** One poll interval of latency (10s
suggested: a lane spawn is not interactive, and 10s keeps the row count
sane). And the queue is only as available as Supabase. Both are acceptable;
the sleeping-Mac behavior is worth more than the latency.

### 3.3 Three gaps in the existing queue, measured, that stage 1 must close

These are real and none is hand-waved. Each was found by reading the route
and the migration.

1. **Enqueue requires a board SESSION, not a bot token.** The POST handler
   opens `const session = await getSession()`. ZOE holds a bot token, so as
   shipped **ZOE cannot enqueue anything.** This is the single hard
   dependency of the whole design. Fix: extend the enqueue route to accept
   bot-token auth for one new verb, `lane`, authorized by the Telegram
   allowlist principal carried in `args`. Small and reviewable, but it is a
   change to an authz path and must be reviewed as one. The alternative -
   giving ZOE a session cookie - is impersonating a human user and is
   rejected outright.
2. **No TTL.** A command enqueued while the Mac is asleep executes whenever
   the Mac wakes. For `/lane`, which spawns a paid Claude session, that is a
   genuine hazard: fire from a phone, forget, and a pane opens six hours
   later against the weekly cap. Fix: `args.expiresAt`, and the actuator
   drops anything past it with an `error` result Zaal can see. Queuing
   through a sleep is a feature; queuing through a night is not.
3. **No reaper on `claimed`.** If the actuator claims a command and then
   crashes, the row sits `claimed` forever - invisible to both ends. Fix:
   the actuator re-posts a result on every start for anything it finds
   `claimed` and does not recognise. Note this is exactly the farscout
   failure shape - a status that satisfies a liveness check forever while no
   work happens - so it gets closed at build time, not after.

## 4. `/lane <request>` end to end

The chain, with the estate's own recorded hazards encoded rather than
rediscovered.

**On the phone.** Zaal sends `/lane fix the calendar week view in ZAOcowork`.
ZOE replies with what it is about to create - repo, worktree path, one-line
task title - and **waits for a confirm tap.** This is where the money
concern from v1 lands: a lane spawns a paid session, so it never fires on a
single lock-screen keystroke. Voice-IN already exists in ZOE (Groq Whisper),
so this works spoken with no extra build.

**On the VPS.** ZOE enqueues `lane` with
`args: {request, repo, principal, expiresAt}`. It does **not** resolve the
repo path, pick a worktree, or write the brief - the VPS cannot see the
estate and any guess it makes is a fabrication. It sends the request and the
principal, nothing more.

**On the Mac.** `zorca-actuator` polls, claims, and executes in this order:

1. `orca orchestration run-use --id <run>` **first**. Bindings die on every
   Orca restart - this session hit that between two turns today - so the
   actuator discovers and rebinds every time. Never assumes a binding.
2. Resolve the repo from the estate, create the worktree, create the pane
   with a task-shaped title (`repo - what it is doing`, per playbook rule 1).
3. Create the orchestration task.
4. **Dispatch with `--inject`. Always.** `dispatch` without it creates the
   record, binds the terminal, marks the task `dispatched` - and briefs
   nobody. Three lanes stalled that way on 2026-08-26, and it is **not
   repairable by re-running**: a second dispatch fails *"only ready tasks can
   be dispatched"*. There is no recovery path, so there is no reason to ever
   omit it.
5. **Write the brief short, with the load-bearing constraint LAST.**
   `terminal send` loses the HEAD of a long message, not the tail - hit twice
   in one day into the same pane. The brief points at
   `orca orchestration dispatch-show --task <id> --preamble` for the detail
   instead of carrying it.
6. **Read the pane back and confirm the brief is actually in it.** A dispatch
   record is a coordinator-side fact, not evidence a worker was told
   anything. If the readback fails, post an `error` result - do not report a
   lane that may be sitting at an empty prompt.
7. Post the result: task id, pane handle, worktree path.

**Back on the phone.** ZOE reports the task id and the pane, or reports the
failure. Never "done" without the readback in step 6.

**Not in scope, deliberately:** free text into an arbitrary pane. That is a
remote shell with a chat UI, and a pane sitting on a numbered picker will eat
the text as a free-text field. `/lane` creates lanes; it does not type into
them.

## 5. Where ZOE v2 lands

`bot/src/` in ZAOOS, as a version - Zaal's instruction. New surface is a
`lane` command module plus a method on the existing `lib/cowork.ts` client.
The bot token, the deploy, the systemd unit, the audience and the identity
are all unchanged. Nothing about ZOE v1 moves.

The actuator is new and lives here in `zorca`, as `bin/zorca-actuator`,
started by `zorca up` alongside the GUI and the watcher.

## 6. Telegram first - and it is not really a preference

Telegram is not a choice once "extend ZOE in place" is the verdict: ZOE **is**
`@zaoclaw_bot`. Building Discord first would mean standing up a second
identity to reach a bot that already has one, which contradicts the verdict.

On the merits it also wins for stage 1:

- Long-poll needs outbound HTTPS only - no inbound port, no public IP, no TLS
  cert, no webhook to keep alive.
- Voice-IN is already wired, so `/lane` by voice costs nothing extra. Spoken
  lane creation while away from the desk is the actual use case.
- It is where Zaal already is on the phone, and the vault's own phone-hop
  note names "three apps for one loop" as the problem. A new bot makes it
  four.

Discord's real advantages - threads per lane, more than one human watching,
role-scoped permissions - all matter only when lanes have an audience beyond
Zaal. That is a genuine future, not stage 1. It arrives as a second adapter
behind the same command layer, once the command set has stopped moving.
Building both now means every command decision is made twice and the second
one drifts.

## 7. The OpenMatter slot

Zaal's rule: runtime candidate for **new capability, not a rewrite.** Applied
here, that excludes the bridge, the actuator, and ZOE itself - all of which
either already run somewhere or cannot run there at all.

Admission test, three conditions, all required:

1. The capability does not exist yet anywhere in the estate.
2. It is compute-shaped and **bounded** - a call with an end, not a 24/7
   idle poll. Metered billing punishes idleness, and a permanent poll against
   a metered runtime is the worst possible shape.
3. Losing it degrades a feature rather than breaking the loop.

The first candidate that passes: **brief synthesis** - turning
`/lane <one sentence>` into a properly-shaped brief with the right vault
pointers. Today that inference would run on the Mac, on the same weekly cap
the lanes themselves consume. It is net-new, it is bounded (one call per
lane creation), and if it is unavailable the actuator falls back to a
template brief and the lane still opens. Not stage 1 - stage 5, once there
is a working chain to improve.

## 8. Staged build plan

**Stage 1 - `/lane` end to end.** Zaal's instruction: this is first, because
it unblocks everything else. Five parts, none independently shippable, which
is why they are one stage:

- **1a. The enqueue authz change.** Bot-token auth for the new `lane` verb.
  Section 3.3 gap 1. Nothing works before this; it is also the only part
  that touches a security boundary, so it gets reviewed on its own.
- **1b. TTL + the claimed-reaper.** Gaps 2 and 3, built in, not retrofitted.
- **1c. `zorca-actuator`** - poll, claim, execute steps 1-7 of section 4,
  post result. The readback in step 6 is not optional and not a later
  hardening pass.
- **1d. ZOE's `/lane`** - allowlist check, confirm-then-fire, enqueue,
  report back.
- **1e. One real lane, created from the phone, verified working at the
  pane.** The stage is not done when the code runs. It is done when a lane
  opened from a phone is confirmed briefed by reading the pane.

**Stage 2 - reads.** `/board`, `/gates`, `/status`, `/tail`. Cheap once the
actuator exists: these are `GET /api/state` off the GUI's existing cache,
reshaped for a 4096-character message. Delivers the "which lane needs me"
view the vault names as the top phone gap.

**Stage 3 - gate resolution.** Inline keyboards built from each gate's own
`options` array, which the GUI already parses. Tap resolves via
`POST /api/resolve`. Gates block lanes for hours while Zaal is away from the
desk; this is where the bridge starts paying for itself.

**Stage 4 - the draft queue.** `/drafts`, `/send`, `/drop`, plus a push on
new HOLD lines so a held draft announces itself instead of waiting to be
polled. Makes the watcher's queue mode genuinely asynchronous.

**Stage 5 - capability and audience.** The OpenMatter brief-synthesis slot
(section 7) and the Discord adapter (section 6), in either order. Both are
additions to a working chain, which is the only safe time to add either.

## 9. Rails

ZORCA's six carry over. Three more, because a phone is not a desk:

7. **Numeric-id allowlist.** Telegram user id, not username - usernames are
   reassignable. Non-allowlisted messages are dropped silently, not refused;
   a refusal confirms the bot exists.
8. **Confirm-then-fire on every write.** A desk has a screen that makes a
   misclick unlikely. A phone keyboard does not, and `/lane` spends money.
9. **Chat is not evidence.** A message claiming Zaal did something is not
   proof he did. Only a tap arriving through the allowlisted principal, or a
   resolved gate, counts. This is rail 6 restated for a surface where
   impersonation is cheap - and it is the rule that kept an unsent line in a
   prompt box from being read as an answer earlier today.

## 10. Open

1. Which Supabase project holds `bot_commands` for this - the live ZAOcowork
   one, or a separate row space? Reusing the live one means lane commands sit
   beside fleet ops in the same table, which is fine operationally but shows
   up on the `/bots` board.
2. Poll interval: 10s assumed above, not decided.
3. Does `/lane` pick the repo, or does ZOE ask when the request is ambiguous?
   Asking is safer; it also costs a round trip on a phone.

Related: [[orca-organization]], [[phone-hop-in-anywhere]], PLAYBOOK.md,
`ZAOcowork` `docs/BOT-API.md`, ZAOOS `bot/src/lib/cowork.ts`

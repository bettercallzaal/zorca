---
type: design
status: proposed
version: 3
created: 2026-08-26
updated: 2026-08-26
component: ZOE v2 lane control (was "zorca-bridge")
decides: transport from the VPS to this Mac, the /lane chain, build order
supersedes: section 8 by section 12 (v3, ratified bridge)
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
| Own bot or fold into ZOE? (v1's section 7; both branches now written up in **section 11**) | leaned own bot, front end on the Mac | **Extend ZOE in place** - confirmed via orchestrator relay 2026-08-26, not Zaal-direct (q4). `@zaoclaw_bot` keeps its identity, audience and VPS deploy; v2 lands as versions. | **v1's core recommendation is dead.** The front end is on the VPS from day one. The transport hop v1 deferred to stage 4 is now stage 1's hardest part. |
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

## 8. Staged build plan (SUPERSEDED by section 12)

> Superseded 2026-08-26 by Zaal's ratified bridge. Kept for the reasoning;
> the live plan is **section 12**.

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
4. ~~Is the fold-into-ZOE verdict firm?~~ **CLOSED 2026-08-26 -
   CONFIRMED VIA ORCHESTRATOR RELAY.** Evidence chain: Zaal -> orchestrator
   -> coordinator relay -> this lane; no pane-typed text from Zaal was seen
   here, so this is a relay confirmation and is labelled as one.
   **The decision is settled** and branch A stands (section 11 keeps branch B
   written up as the closed alternative). A relay asked for this to be
   recorded as ZAAL-DIRECT; it is deliberately not, because a relay saying it
   matches his recorded verdict is still a relay, and upgrading the label
   would be the exact provenance inflation this question was raised to catch.
5. ~~Does Telegram retain undelivered `getUpdates` for ~24h?~~
   **CLOSED 2026-08-26, deliberately unmeasured.** See section 13.
6. ~~One instruction is unread.~~ **CLOSED 2026-08-26.** A mid-turn message
   arrived head-truncated, surviving only as *"e delete call stay Zaal's - do
   not touch either."* The head was **not** reconstructed and nothing was
   inferred from it - a sentence whose visible half concerns a delete call is
   the worst possible place to guess the missing half. The coordinator has
   since confirmed the two things named were **issue template placement** and
   **the delete call**, and that neither was touched. Nothing was pushed and
   nothing was deleted at any point.

   **The finding that outlived the incident:** this route truncated the head
   of four inbound messages and preserved the tail every time, while both
   messages carrying their instruction at the tail arrived intact and
   actionable. That is measurement, not hypothesis. On this channel
   **constraint-last is the rule, not a guideline** - the truncated message
   was ~2KB with its corrections at the head, which is precisely what the
   playbook entry warns against.

Related: [[orca-organization]], [[phone-hop-in-anywhere]], PLAYBOOK.md,
`ZAOcowork` `docs/BOT-API.md`, ZAOOS `bot/src/lib/cowork.ts`

## 11. Appendix A - the two branches, documented

**Why this section exists, stated plainly.** Section 1 records "extend ZOE in
place" as a Zaal verdict, relayed by the coordinator. A later orchestrator
relay asked for both branches documented anyway, and repeated that the unsent
prompt-line text is not an answer. Those two things are in tension: if the
verdict is real, this section is contingency; if the verdict was contaminated
by the unsent text - which read "fold it into ZOE, telegram first" and
overlaps the verdict on exactly the ZOE half - then the question is open and
section 1 is overstated.

**Resolved 2026-08-26, and labelled precisely.** The verdict is confirmed
**via orchestrator relay**, not as Zaal-direct - see open question 4 for the
chain and for why the stronger label was declined. Branch A stands; branch B
below is kept as the documented closed alternative, not a live option.

(Pointer for stale references: this was **v1's section 7**. In v2 that number
is the OpenMatter slot.)

### 11.1 The asymmetry that drives everything

The two branches are not two skins on one design. They differ in **how many
hosts sit between the phone and the pane**, and that number decides whether
section 3 of this document is needed at all.

| | **Branch A: fold into ZOE** | **Branch B: own bot** |
|---|---|---|
| Hosts in the path | 3 - phone, VPS, Mac | **2 - phone, Mac** |
| Transport problem | the whole of section 3 | **does not exist** |
| Queue, TTL, reaper | all required | **none required** |
| Enqueue authz change | **required** (section 3.3 gap 1) | not required |
| VPS hop | **stage 0/1** | stage 4, or never |
| Latency | one poll interval | instant |
| New identity | none | a second bot |
| Phone apps for one loop | 3 | **4** |

Branch B deletes sections 2, 3, and 3.3 outright. That is the single largest
fact about this choice and it is easy to miss while reading a document that
is mostly about a transport.

### 11.2 Branch A - fold into ZOE (the recorded verdict)

`@zaoclaw_bot` gains a `/lane` command. Identity, audience, token, systemd
unit and deploy are unchanged; v2 lands as versions in ZAOOS `bot/src/`.

**`/lane` consequence.** The full chain of section 4: phone to VPS to
`bot_commands` to a Mac actuator to `orca`. ZOE cannot see the estate, so it
sends the request and the principal and resolves nothing - repo, worktree and
brief are all the actuator's job. Every design decision in sections 2, 3 and
4 exists to serve this branch.

**VPS hop: stage 0.** It is not deferrable. The front end is already on the
VPS on day one, so the transport is the first thing built, and the enqueue
authz change (gap 1) is the first thing reviewed. Stage 1 cannot start
without touching a security boundary.

**What it buys.** One identity and one audience. Voice-IN already wired, so
spoken `/lane` costs nothing. ZOE's existing auth and deploy are reused. And
the queue genuinely survives a sleeping Mac - the command waits and runs on
wake, bounded by the TTL from gap 2.

**What it costs.** Three hosts in the path for every command, so three places
to be wrong and three to instrument. A live bot with real users gains a
feature that can regress it. A security-boundary change lands in week one,
before any of the design has been proven end to end. Two of the three gaps in
section 3.3 (TTL, reaper) exist *only* because this branch has a queue.

### 11.3 Branch B - own bot, front end on the Mac

A separate Telegram bot whose long-poll loop runs on this Mac, beside the GUI
and the watcher, started by `zorca up`.

**`/lane` consequence.** Phone to Mac. One process reads the update, checks
the allowlist, and runs the section 4 chain locally - `run-use`, worktree,
pane, `dispatch --inject`, short brief, pane readback. **No queue, no
transport, no enqueue change, no TTL, no reaper.** The three gaps in section
3.3 are not fixed by this branch; they are not encountered.

**VPS hop: stage 4, or never.** It only arrives if "survives a sleeping Mac"
turns out to be a real, frequent failure rather than a hypothetical - and if
it does arrive, it arrives against a chain already proven working, which is
the safest possible time to add a hop.

**One point that needs checking before this branch is costed.** Telegram's
`getUpdates` is believed to retain undelivered updates server-side for about
24 hours, which would mean a `/lane` sent to a sleeping Mac is delivered on
wake rather than lost - substantially weakening branch A's headline
advantage, and re-introducing gap 2's stale-command hazard on this side of
the fence instead. **I have not verified this and it should not be relied on
until someone does.** It is the single measurement that would most change the
comparison.

**What it buys.** The simplest chain that can work, and the only one with no
new authz surface. Instant rather than poll-bounded. ZOE v1 cannot regress
because ZOE v1 is not touched.

**What it costs.** A second bot identity for an audience that already knows
`@zaoclaw_bot`, and a fourth app in a loop the vault's own phone-hop note
already criticises at three. Voice-IN would have to be rebuilt rather than
inherited. And if the Telegram retention point above turns out false, a
closed laptop simply drops the request.

### 11.4 What each branch would change in this document

| Section | Under A | Under B |
|---|---|---|
| 2 - the shape | as written | replaced by a two-box diagram |
| 3 - transport | as written | **deleted** |
| 3.3 - three gaps | as written | **deleted** (not encountered) |
| 4 - `/lane` chain | as written | unchanged, minus the queue hops |
| 5 - where it lands | ZAOOS `bot/src/` | `zorca`, beside the actuator |
| 6 - Telegram first | implied by the verdict | a real choice, still Telegram |
| 8 - stages | 1a-1e as written | 1a and 1b drop out |

Section 4 surviving both branches is worth noticing: the `/lane` chain and
its hazards are the durable part of this design. The transport is the part
under dispute.

### 11.5 Not a recommendation

Branch A is what Zaal is recorded as choosing and it is what sections 2
through 8 are written for. Branch B is materially simpler and this section
should not be read as pretending otherwise - but "simpler" is not the only
axis, and the identity and audience arguments that decided it are Zaal's to
weigh, not measurable from here.

## 12. v3 - the ratified bridge and the live build plan

Both open questions are answered and a transport is ratified, **confirmed via
orchestrator relay 2026-08-26** (chain: Zaal -> orchestrator -> coordinator
relay -> this lane; not observed as Zaal's own typed text). The decision is
settled at that evidence level - see open question 4. This section supersedes
section 8 and settles sections 3 and 11.

**What is now decided:**

- **q4:** ZOE v2 runs on **OpenMatter**, with the **VPS warm as fallback**.
  Both, not either. This also settles section 11 - there is a ZOE v2, so
  **branch A is confirmed** and branch B is closed.
- **q5:** the Telegram retention question is not answered, it is **removed**.
  A **webhook** to the VPS has no retention dependency at all. That is the
  right kind of answer to an unverified fact: delete the dependency rather
  than measure it.
- **Transport:** Telegram webhook to the VPS; the VPS puts each `/lane`
  request into a **queue file**; the orchestrator on the Mac **polls the
  queue**. Not the `bot_commands` plane, not Tailscale-to-`:7777`.

The queue-file design keeps the property that matters and that both earlier
candidates fought over: **if the Mac sleeps, the queue waits.**

### 12.1 One measured blocker, and the one-word fix

The spec says the VPS writes the queue file *on the Mac over SSH*, and in the
same breath that the *Mac keeps zero inbound ports*. Those cannot both hold:
an inbound `ssh` is an inbound port.

Measured on this Mac, today:

```
$ tailscale status
Tailscale is stopped.
$ lsof -nP -iTCP:22 -sTCP:LISTEN
(no output - nothing is listening on 22)
```

So VPS-to-Mac SSH is not merely a security tradeoff, it **cannot work today**:
there is no route (Tailscale down, laptop behind NAT with no static address)
and no listener (Remote Login off). Enabling both is exactly the inbound
surface the spec says it avoids.

**The fix is the direction, and nothing else. Invert the SSH.**

> The **queue file lives on the VPS.** The webhook appends to it. The Mac
> polls it by **SSHing outbound** to the VPS and draining it.

Everything Zaal specified survives intact - webhook so there is no retention
risk, a queue file rather than a cloud table, SSH rather than an exposed
port, the orchestrator polling the queue, and the queue waiting through a
sleep. What changes is who dials. The Mac dials out. And this variant:

- needs **zero** inbound ports on the Mac, literally rather than nearly;
- works **today**, with no Tailscale and no Remote Login;
- keeps the VPS as the only machine with a public face, which it already is;
- survives the Mac changing networks, which a laptop does constantly.

Stage 1 below is written against this variant. If Zaal wants VPS-to-Mac push
specifically, the cost is: Tailscale back up on both ends, Remote Login on,
a key installed, and the DNS-gap failure mode that hits exactly when he is
mobile. That is a real option and it is his call - but it is not free, and it
is not what the "zero inbound ports" clause describes.

### 12.2 The queue file

A line-delimited JSON append log on the VPS - one record per `/lane`, append
only, never edited in place:

```
{"id","ts","expiresAt","principal","request","status"}
```

Append-only because two writers (webhook) and one reader (Mac) on a file are
safe if nobody rewrites, and because a crashed drain must never lose a
request. The Mac drains by reading, acting, then appending a **result
record** rather than mutating the original - the same claim-and-report shape
as `bot_commands`, in a file.

Carried over from section 3.3, because a file does not fix them:

- **TTL (`expiresAt`) is required.** A `/lane` fired at a sleeping Mac must
  not spawn a paid pane six hours later. Queuing through a sleep is a
  feature; queuing through a night is not.
- **A restart reaper is required.** Anything the Mac finds claimed-but-not-
  reported on startup gets an error result, so no request can sit invisible
  forever. This is the farscout shape and it gets closed at build time.

The `getSession()` enqueue gap from section 3.3 **disappears** - there is no
`/api/v1` call in this path at all.

### 12.3 Stage 1 - `/lane` end to end on this bridge

Done when a lane opened from Zaal's phone is confirmed briefed by reading the
pane. Not when the code runs.

- **1a. Webhook receiver on the VPS.** `setWebhook` against the existing
  `@zaoclaw_bot` token, TLS on the VPS's public name, numeric-id allowlist
  as the first check, non-allowlisted updates dropped silently. Replaces
  ZOE's long-poll for this route only.
- **1b. `/lane` conversation + the append.** Echo back the parsed request and
  wait for a confirm tap - a lane spends money and a phone keyboard has no
  hover. On confirm, append the record with `expiresAt`.
- **1c. Mac-side drain (`zorca-actuator`).** Outbound SSH to the VPS on an
  interval, pull new records, honour TTL, run the section 4 chain per
  record, append the result. Restart reaper included, not deferred.
- **1d. The section 4 chain, unchanged.** `run-use` first - bindings died
  three times during the writing of this document, so rebinding is
  unconditional, never error recovery. `dispatch --inject` always; omitting
  it briefs nobody and cannot be repaired by re-running. Brief short with
  the load-bearing constraint last, pointing at `dispatch-show --preamble`.
  **Pane readback before reporting success.**
- **1e. Report back.** ZOE reads the result record and tells Zaal the task id
  and pane, or the failure. Never "done" without 1d's readback.

Section 4 is the durable part of this design: it survived branch A, branch B,
and now a third transport, unchanged.

### 12.4 Stage 2 - OpenMatter runtime, VPS warm fallback

Move ZOE v2's runtime to OpenMatter; keep the VPS instance warm.

**Three things to settle first. Each is measured or structural, not a
preference.**

1. **Telegram allows exactly one webhook URL per bot token.** OpenMatter and
   the VPS cannot both receive updates for `@zaoclaw_bot` at the same time.
   So "warm fallback" is **not** passive standby - failing over means an
   active health check plus a `setWebhook` repoint, and a decision about who
   is allowed to fire that repoint. Build the repoint as an explicit,
   idempotent operation with a manual override, or the fallback is a comfort
   rather than a mechanism.
2. **A webhook does not reduce metered cost if billing is by container
   uptime.** The container must be running to receive an update. On the only
   rate datum that exists - derived ~0.837 Cr/hr against a ~12 Cr balance -
   a permanently-up instance is under a day of runway. Before cutover,
   measure whether OpenMatter bills uptime or invocation. If uptime, this
   stage needs a topped-up grant or an explicit budget, not an assumption.
3. **The grant's purpose.** The credits were a partner grant for an agreed
   newsletter-agent beta. Running ZOE's lane control on them is a different
   use. Zaal's call, but it should be made deliberately rather than
   discovered at the balance.

Also inherited: the Hermes template's dashboard and API server are the
subject of an active exposure campaign. A bot token on that host raises the
blast radius of a compromise from "an agent" to "the bot that can open
lanes." The allowlist and the confirm step are what stand between a
compromised host and a spawned pane, so neither is optional at any stage.

**Sequence:** deploy beside the VPS instance and run it dark first (no
webhook), verify it can drain and act, then repoint `setWebhook`, keep the
VPS warm, and rehearse the failback once before trusting it.

### 12.5 Stages 3+

Unchanged from section 8: reads (`/board`, `/gates`, `/status`, `/tail`),
then gate resolution from chat, then the draft queue with HOLD push, then
the Discord adapter and the OpenMatter brief-synthesis slot. All are
additions to a working chain, which is the only safe time to add any of them.

## 13. One belief left unmeasured, on purpose

Open question 5 asked whether Telegram retains undelivered `getUpdates` for
about 24 hours. It is closed **without being measured**, and this section
records why so nobody re-opens it as an oversight.

**It no longer decides anything.**

1. It was only ever load-bearing for the **branch comparison**. Its whole
   weight was that if Telegram retains updates, branch B keeps most of
   branch A's sleeping-Mac advantage without the VPS hop (section 11.3).
   **Branch A stands** - Zaal confirmed ZOE v2 - so the comparison it fed is
   settled and the answer changes no decision.
2. The ratified transport **removed the dependency outright**. Stage 1 is a
   **webhook**, not `getUpdates`. Retention is a property of a polling API
   this design no longer uses. Even under branch B the question would now be
   moot.

**And measuring it costs more than it returns.** There is no documentation
substitute for the real behaviour of a real token, so a genuine test means
taking `@zaoclaw_bot` off updates, letting real messages accumulate, and
observing what arrives on reconnect. That bot is a live surface Zaal uses
daily. The price is deliberately not answering his actual messages for hours
to settle a question that gates nothing - a live degradation bought with
nothing.

**The rule this is an instance of.** An unverified belief is only worth
measuring while something still rests on it. When the design moves and
nothing does, the honest move is to mark it unmeasured and say so - not to
quietly assert it, and not to spend real cost proving a fact that has stopped
mattering. It stays written down as a belief, never cited as a finding, and
if a future design puts weight back on it, it gets measured then.

Related: section 11.3 (where it mattered), section 12 (which removed it).

## 14. Handoff - lane closed 2026-08-26

Everything below is recoverable from this file alone. Scrollback is not
required and should not be trusted; that is the whole reason this document
carries the state rather than the pane.

### Where the work is

**All local. `origin` is untouched** and still sits at `9b64e28`, the commit
it held before this lane started - so the diff for this lane is exactly
`git log 9b64e28..HEAD`. Push is gated and was never performed. Nothing was
deleted at any point.

| What | Where |
|---|---|
| The design, v3 | `docs/DESIGN-bridge.md` - live plan is **section 12** ( section 8 superseded) |
| Mac-side drain | `bin/zorca-actuator` |
| VPS-side append + record contract | `bin/zorca-lane-enqueue` |
| Test suite, 16 cases | `bin/zorca-actuator-test` - run it first, it needs no Orca |
| Task report | `.handoffs/DONE.md` |

### Before anything runs - two things, both Zaal's

1. **The SSH direction.** `queue.mode` supports `ssh` and `local` and
   **defaults to neither**. The measured position: VPS-to-Mac push cannot
   work today - Tailscale reports stopped and nothing listens on 22 - so
   `ssh` (Mac dials out, queue file on the VPS) is the only variant that runs
   now and the only one that literally keeps zero inbound ports on the Mac.
2. **The config file** at `~/.zao/zorca-actuator.json`. It does not exist.
   The actuator refuses to start without it and names every missing key at
   once. There is no default port: **7777 and 7778 both answer**, so guessing
   was never available.

The actuator is deliberately **not** wired into `zorca up`. It spends money,
has no config, and the direction is unratified - three independent reasons.

### The channel rule, which is measurement not preference

This route truncated the **head** of four inbound messages and preserved the
**tail** every time. Both messages that carried their instruction at the tail
arrived intact and actionable; the ~2KB message with its corrections at the
head lost them. On this channel **constraint-last is the rule**. It is the
`terminal send` head-loss the playbook already records, and it is reliable
here rather than intermittent.

Corollary worth keeping: every truncation was recoverable because this
document held the state. A pane that loses its brief can re-read a committed
file. One that only had the message is finished.

### Untouched, on instruction - do not assume otherwise

`zorca-gui2` and its files. `bin/zorca`. The delete call. Issue template
placement. Each was left alone deliberately, not overlooked.

### Open, and closed-with-a-label

Section 10 carries all six. Two are closed at a narrower evidence level than
was asked for, and that is the point of them: **q4** is confirmed via
orchestrator relay, **not** Zaal-direct; **q5** is closed deliberately
unmeasured because nothing rests on it any more (section 13).

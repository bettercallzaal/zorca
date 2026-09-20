# ZORCA

**ZORCA is the layer that makes many coding agents one operation, and the
boundary through which that operation talks to the outside world.**

It has two jobs. Inside, it organises agents running in [Orca](https://orca.stably.ai)
into lanes with conventions, a ranked board and hard safety rails. Outside, it
is the adapter: the place where internal work is translated into a public
contract, so a partner system can ask for something without being handed the
keys to the estate.

Orca itself is closed source and unaffiliated. ZORCA only drives its public CLI
(`orca terminal ...`, `orca host ...`, `orca environment ...`). Nothing here
patches or redistributes the app, and that is deliberate: **the adapter must not
depend on anything Orca-specific, or swapping the cockpit out breaks the
boundary rather than just the window.**

## Status, honestly

This repo was retired to a pointer on 2026-09-06 because it held nine tools
against the layer's hundred-plus, two of them stale and one a broken copy of a
safety tool. That reasoning was right and is preserved below. What changed is
that the repo now has a job the pointer could not do.

**Today: `PLAYBOOK.md` is the real content, and it is the thing worth reading.**
The rest of this README describes what belongs here and what does not, so the
refill happens deliberately rather than by drift back to nine stale copies.

## What lives here

Things that are true regardless of one machine's filesystem, and safe in public.

| | |
|---|---|
| **`PLAYBOOK.md`** | The operating conventions, the supervision rules, and every hazard that actually happened. This is the seed of the whole layer. |
| **`gui/`** | The board UI - `zorca-gui` (:7777) and `zorca-gui2` (:7778, the doc-2420 redesign), plus `contrast-check.py` and `field-audit.py`. |
| **`docs/DESIGN-bridge.md`** | ZOE v2 lane control: a `/lane` request from chat becoming a real lane, over a polled command queue rather than SSH. **Proposed, not built.** |
| **`ZOE-CENTER.md`**, **`zoe-analysis-2026-08-27.md`** | Design and the evidence behind it. Design only; nothing built. |
| **`LICENSE`** | MIT. |
| *(planned)* **the federation contract** | The Capability Card and envelope mapping. Named, not started - see below. |

## What does NOT live here, and why

**Every executable tool in the layer lives in `zaal-dotfiles/bin`, which is
private and unlicensed.** That is roughly 109 tools: the board and lane
machinery (`zj`, `zao-lanes`, `orca-board`, `lane-send`), the single-seat lock
(`zorca-lock`), briefing (`zorca-brief` - briefs are FILES, because
`orca terminal send` drops the head of long messages), sensing (`zao-tick`,
`zao-selftest`), handing back (`zao-reap`, `zorca-bundle`), and the ZOE v2 lane
control pair (`zorca-actuator`, `zorca-lane-enqueue`).

They are not here for one reason, and it is a rule rather than an accident:

> **A public copy of a tool that is not the copy that runs is worse than no
> copy at all.**

That is not theoretical. Before the 2026-09-06 retirement this repo shipped
`zorca-brief` at 18 lines while the version actually in use was 113 - a public,
broken copy of a safety tool, under the layer's own name. Anyone cloning got the
broken one.

So: **making a tool public is a deliberate extraction with a licence decision
attached, not a side effect of where a file sits.** If a tool is extracted, it
is extracted as the canonical copy, with its tests, and the private one becomes
the pointer - never the other way round, and never by copying.

## The safety rails

Each one was bought with a real failure. They are documented here because they
are the layer's actual design, and because a partner system asking what proof
this estate requires is asking exactly this question.

1. **Danger words** - drafts and pane text matching license/publish/delete/
   archive/push/merge/rotate/credential are HELD for the human, never sent.
2. **Draft screening** - the draft is screened, not just the pane. A stalled
   pane with an innocent question can still get a dangerous draft.
3. **No fabrication** - the drafter writes as the orchestrator, never as the
   human. It may decide between offered options, never assert world-facts
   (payments, approvals, access). Real-world actions exit as NEEDS-HUMAN.
4. **Provenance** - every auto-sent message is prefixed `[auto-draft]`, so the
   receiving agent can discount its factual claims.
5. **Receipt checks** - a send is not a delivery. The watcher confirms the pane
   actually holds the text; compaction and restarts eat briefs.
6. **Evidence rule** - only the human's own typed text or a resolved decision
   gate proves a human action. Anything else claiming one is held.

The general form, from `PLAYBOOK.md`: **agents under pressure to be decisive
will assert state they cannot measure.** Give every loop an honest "I cannot
know this" exit and make provenance visible, or decisiveness becomes fabrication.

## The federation boundary

Named, not started. Recorded here so the shape is public before anything is
built against it.

ZORCA is the adapter between internal work and a public federation contract.
Internally the unit of work is a packet: id, mission, owner agent, machine,
stage, evidence, blocked-on, plus the authorized context that crossed the
boundary and the receipt that proves what happened. Externally a partner sees
only a capability card and an envelope: mission id, sender, recipient or
capability, payload hash, requested effect, expiry, idempotency key.

The rule that governs the translation:

> **Normalize at the boundary, preserve each system's internal ontology behind
> it.**

A partner asks "who can perform capability X" and never learns which component
does it. Owner-agent and machine do not cross. The payload hash crosses; the
payload does not. And the completion criterion is the strict one: **neither side
can report success unless the other side can independently observe the intended
effect.** No repository access in either direction - that is the actual proof
that the boundary is real.

Nothing is built. No contract has been read. See `docs/REPO-LAYOUT.md` for what
would land where when it is.

## Orca itself - the measured picture

ZORCA drives Orca's public CLI, so what that CLI can actually do is part of this
layer's ground truth. The ZAO research library holds it, measured rather than
recalled. Read these before writing a new Orca call:

| Doc | What it establishes |
|---|---|
| [**2513 - Orca: what the ADE actually provides, what we use, and how to use it well**](https://github.com/bettercallzaal/ZAOOS/tree/main/research/dev-workflows/2513-orca-ade-capabilities) | Orca 1.4.204's whole command surface against what this estate invokes: **19 of 234 commands used, 215 untouched**. The high-value unused ones were run, not read from help text - including a control pair showing `terminal wait --for tui-idle` returns rc 0 on an idle pane in 0.11s and rc 1 on a working one at timeout. Ends in eight best practices. |
| [**2407 - Orca and the Wall are blind in the same way**](https://github.com/bettercallzaal/ZAOOS/tree/main/research/dev-workflows/2407-orca-tmux-lane-integration) | Why **Orca is the viewer and tmux is the substrate**, and why the lane system was deliberately not migrated into it. |
| [**2497 - Managing zorca: what to upgrade**](https://github.com/bettercallzaal/ZAOOS/tree/main/research/agents/2497-zorca-upgrades) | The audit of this layer's own tooling - the hand-written line count, and the supervisor that turned out not to have been running. |

### The four rules that cost the most to learn

1. **Read the schema before writing the call.** `orca agent-context --json`
   prints all 234 commands. Flags are not guessable: it is `--terminal <handle>`,
   never `--id`.
2. **Wait, do not poll.** `orca terminal wait --for tui-idle` exits 0 when
   satisfied and 1 on timeout. Deriving "idle" from pane text reads interface
   chrome as intent - it has reported a confirm dialog's highlighted default as
   something a person typed.
3. **A decision owed to a human belongs in a gate, not a pane.**
   `orca orchestration gate-create` takes `--task`. A picker sitting open in a
   pane appears in no list, and the pane cannot receive while it is open, so a
   message queue can build behind it unseen.
4. **Never point a long-running process at a path inside a shared checkout.** A
   tree that lanes switch branches in will make the file vanish under a running
   daemon. Keep daemons on a path that does not move.

## Requires

- Orca installed with its CLI on PATH (`orca status` works)
- python3, and the `claude` CLI for the drafter
- `gh` for the estate auditor's GitHub passes

## History

Extracted 2026-08-25 from a live 13-pane session. Retired to a pointer
2026-09-06, for the reasons kept above. Refilled deliberately from
`PLAYBOOK.md`, which is what the pointer README itself said the extraction would
start from. APIs are Orca's public CLI surface and may shift under app updates.

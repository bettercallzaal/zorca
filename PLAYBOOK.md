---
type: playbook
status: active
created: 2026-08-25
updated: 2026-09-01
tags: [orca, orchestration, workflow]
source: manual
confidence: high
routed: unrouted
---

# How Orca gets organized

State as of 2026-08-25 evening: 9 live panes, 65 registered worktrees, 63
registered repos, 3 project groups, 0 automations, 0 orchestration runs. The
CLI can do runs/tasks/gates/workers; none of it is in use. The gap is not
tooling, it is convention.

## The operating loop (running now)

- `orca-board` - ranked board of every pane: ctx-critical > choice-prompt >
  asked-question > waiting > idle-done > bare-shell.
- `orca-board --auto 90` - the watcher. Drafts the next step for any stalled
  pane and sends it. HOLDS anything matching the irreversible-word list
  (license, publish, delete, archive, push, merge, rotate, credential...) and
  logs to `~/.zao/orca-board.log`. Zaal reads HOLD lines, decides those.
- `orca-board --tail <repo>` - follow one pane live.
- `orca-board --draft` - dry-run the replies without sending.

Division of labor: the watcher keeps lanes moving; Zaal (or the orchestrator
session) decides everything irreversible; pane titles carry the task so the
sidebar reads as a status board.

## The division of labor (Zaal, 2026-08-26 - the standing rule)

"The orchestrator here is in charge of Obsidian; any other requests go to a
specific planned Orca channel / lane."

| Surface | Writer | Never |
|---|---|---|
| The vault (notes, TOC, IN-FLIGHT, grill queue, daily, playbook) | The orchestrator session, directly | Dispatched to a lane |
| Repo work (code, docs, research, builds) | A planned Orca lane per repo/topic | Done inline by the orchestrator |
| A lane's own `.handoffs/` + repo-committed reports | That lane | - |
| Dispatch bookkeeping, worker_done verification | The coordinator pane | Resolved gates it did not verify |
| Gates (irreversibles, money, public, identity) | Zaal | Anyone else |

Flow: request arrives at the orchestrator -> vault-shaped work happens here;
everything else gets worktree + pane + brief (carrying vault *pointers*, not
copies) + orchestration dispatch -> lane reports -> coordinator verifies ->
orchestrator writes the vault record. One writer for the picture, many for
the repos - the four-surfaces drift problem is prevented by construction,
not by sync scripts.

## Supervising a lane (set by Zaal, 2026-08-31; extended 2026-09-01)

The rules above say who writes what. These say how one terminal watches another,
and they exist because on the day they were written **a lane and its supervisor
were each wrong three times, and each caught the other.** Neither was reliably
right, so the rules are built around that rather than around seniority.

### 1. What reaches the human

**Only what changes his next action.** Four categories:

- a decision the lane needs from him
- a contradiction with something he currently believes
- anything with a deadline
- anything about to be sent, published or merged outward

Everything else is held and folded into a summary when he asks. Measured against
one real day, that is about five messages instead of twenty.

The failure mode to avoid is **narrating a working system**. If the lane is doing
well, that is not news. "Reserved a doc number", "running the tests", "PRs
changed: none" - none of those reach him.

### 2. Intervening mid-action

**Message the lane directly, tell the human after.** Speed matters when it is
mid-write; a correction that arrives after the commit is archaeology.

This is granted knowing the supervisor will sometimes be wrong. The cost of a
wrong intervention is one message and a correction. The cost of a late one is a
merged commit or a sent email.

### 3. When the two disagree

**Neither wins by rank.** Zaal, 2026-08-31: *"I'd like both to tell the other why
they think one way and then come to a solution. If it can't, ask Zaal."*

1. **Say why, not just what.** "This is wrong" is not a position. "This is wrong
   because I grepped the string and found eight files" is.
2. **The other side answers the reasoning**, not the conclusion.
3. **Converge.** Usually one side has measured and the other has remembered, and
   that resolves it without anyone conceding anything.
4. **Only if it will not converge does it go to the human** - with both positions
   stated, not one position and a complaint.

**Converging on "we do not know" is a successful outcome**, not a failure to
decide. On the day this was written, two terminals stopped on an ambiguous name,
neither had evidence, nobody guessed, and it went up unresolved. That was the
right ending.

This appears to be an original: the published multi-agent literature covers
orchestrator-to-worker delegation and says nothing about two peers disagreeing on
a fact.

### 4. Ask what the lane has already measured before asserting a limit on it

Added 2026-09-01, after the supervisor did the thing this whole file is about.

It measured that no configured MCP server could reach a particular database -
true, and re-checked - and told the lane it **could not read** that database,
raising a gate on that basis. The lane had read it hours earlier by another
route, and said so.

The measurement was correct. The conclusion did not follow. *"No configured MCP
reaches it"* is a fact about the supervisor's instruments; it was silently
promoted into a fact about the lane's capabilities.

The lane's framing, which is better than the rule:

> **"A board that only sees menus and a peer that only sees its own probes fail
> the same way. Measure the lane, not the surface."**

So: before telling a lane what it cannot do, ask it what it has already done. A
supervisor's probes describe the supervisor.

### 5. Continuity

Supervision is a job, so it transfers like one. When a supervising session runs
low on context it hands the watch on explicitly, in the handoff, rather than
letting it die quietly. **A lane that believes it is being watched and is not is
worse than one that knows it is alone.**

Concretely: the watcher process dies with the session that started it. Re-arming
it is the first thing a successor does, before any other work.

### The shape underneath all five

The recurring failure is **something asserted without being measured**. Every
rule above is a way of catching that in something other than yourself.

So the supervisor's real job is not correctness. It is being the second place a
claim has to survive.

## Conventions to adopt

1. **One pane per lane, titled by task.** `repo - what it is doing`, renamed
   when the task changes (`orca terminal rename`). Never the auto-title.
2. **Close panes when the lane ends.** A bare shell with no assignment is
   noise. Recreate takes one command
   (`orca terminal create --worktree path:<p> --command claude`).
3. **ctx above 85% means handoff, not new work.** Write `.handoffs/`, commit,
   `/clear`, reassign. The watcher flags these as ctx-critical.
4. **Worktree hygiene.** 65 registered worktrees for 9 live panes. After the
   branch-prune pass, remove dead ones with `orca worktree rm` (it deletes the
   git worktree too - only after its branch is merged or pushed).
5. **File ownership when panes overlap.** Two panes nearly edited
   sync-projects.js the same hour. Rule: the pane whose repo owns the file
   makes the change; the other reports findings and stands by.
6. **Multi-agent state lives in the vault, not scrollback.** Findings land as
   committed docs (repo-local) plus a short vault note linking [[repo-estate]].
   Scrollback dies at compaction; the vault does not.

## Standing policy - what counts as a disclosure

Set by Zaal 2026-08-26, resolving `gate_283ff11d6f72`. It generalises; apply it
rather than re-deciding each case.

- **Aggregating already-public information is fine.** Republishing on-chain
  addresses, balances, ENS names and other self-published facts in a convenient
  table is not a disclosure. Convenience is not exposure.
- **Genuinely-new private linkage still gates.** Binding a public identifier to
  something only ZAO's own systems know - a `users` row, a Discord export, an
  internal tier - is a disclosure and must be raised before publishing.

The practical test: could a stranger derive this from public sources alone? If
yes, publish. If it takes ZAO's private data to make the connection, gate it.

Corollary learned the same day: **do not restate redacted content in the commit
message or the report.** Describing precisely what was removed republishes it,
which is the one way a redaction pass makes things worse.

## Known hazards (all hit today)

- **settings.json wholesale rewrite**: a stale Claude session rewrites
  `~/.claude/settings.json` from memory on any toggle, silently reverting
  external edits (wiped dotfiles PR #31 on Aug 18; likely mechanism for the
  CLAUDE.md glossary regression of 2026-08-20). After adding permissions,
  restart other long-lived sessions or expect reversion.
- **Agent committed unredacted handoffs to a public repo's main**
  (`1b805eb`, zaostock, caught before push). Rule 5 exists because of this -
  and the watcher's HOLD list is the second line of defense.
- **Auto-drafts fabricate under decisiveness pressure** (2026-08-25: a
  draft told the zolbot pane "doing the $10 top-up now, Tailscale up" -
  actions Zaal never took). Root cause: "write as Zaal" + "always decide" +
  no escape hatch. The four-layer fix, in order of trust:
  1. Identity - the drafter writes as the orchestrator, never as Zaal.
  2. Claim classes - decisions between offered options are allowed;
     world-facts (payments, access, approvals) are forbidden and route to
     NEEDS-ZAAL.
  3. Provenance - every auto-sent message carries an [auto-draft] prefix so
     receiving panes can discount its factual claims.
  4. Evidence rule (coordinator-enforced) - only Zaal's own typed text or a
     resolved gate proves a Zaal action; any other claim of one is held and
     escalated, never propagated.
  The general form: agents under pressure to be decisive will assert state
  they cannot measure. Give every loop an honest "I cannot know this" exit
  and make provenance visible, or decisiveness becomes fabrication.
- **Inference filed as measurement** (coordinator self-audit, 2026-08-26):
  three of six gates were wrong at filing - a stale queue item read as "LLC
  not formed", "unreferenced" read as "dead", a risk overstated. The
  measurement was right each time; the conclusion drawn from it was filed as
  if it were the measurement. Gate-writing rule: state what was measured,
  state the inference separately, and let the human own the leap.
- **`dispatch` without `--inject` silently briefs nobody** (2026-08-26): the
  record is created, the terminal is bound, the task reads `dispatched` - and the
  pane sits at an empty prompt with no idea it has work. All three morning lanes
  stalled this way. It is not repairable through the same command: re-running
  dispatch with `--inject` fails *"only ready tasks can be dispatched"*. Recover
  by briefing the pane with `orca terminal send`, pointing it at
  `orca orchestration dispatch-show --task <id> --preamble` for the protocol, and
  always leading with `run-use --id <run>`. General form: a dispatch record is a
  coordinator-side fact, not evidence a worker was told anything. Verify the pane
  moved, the same way you verify a `worker_done`.
- **`terminal send` loses the HEAD of a long message, not the tail** (2026-08-26,
  hit twice into the same pane): a multi-paragraph brief arrived with only the
  last three sentences intact the first time and only the last paragraph the
  second. Both times the pane had recently crossed a compaction boundary. The
  lane recovered by inferring the task from its title, then from the vault daily
  note - and both times it SAID the brief was truncated instead of guessing
  quietly, which is the only reason it was caught. Mitigations: put the
  load-bearing constraint LAST, not first; keep briefs short and point the pane
  at a file or command for the detail (`dispatch-show --preamble`, a vault note);
  and read the pane back after sending anything that matters. A resolved gate
  recorded in `daily/` is a durable second source a truncated worker can recover
  from - which is an argument for writing decisions down the same hour they land.
- **Pickers eat text**: a pane sitting on a numbered picker sends any text
  into a free-text field. The board detects choice-prompt; answer with arrow
  keys + Enter, verify cursor with a read first.

## Dated snapshots below this line - not current state

Everything from here down is a **snapshot of one moment**, kept because the
reasoning in it is still useful. Run ids, lane lists, cap status and "still
unadopted" claims were true on the date in their heading and are almost
certainly false now.

Read them as history. If you need current state, measure it: `zao-lanes`,
`orca orchestration task-list`, `orca worktree ps`. A playbook that presents a
stale snapshot as the present is the exact defect the rest of this file warns
about.

## Adopted 2026-08-25 late evening: orchestration runs/tasks/gates

Zaal: "let's combine everything." One Run - `run_a4892c0a5cdc`, the ZAO
operating run - holds every lane as a task. Four dispatched to live panes
(dashboard-data-layer, hypersnap-research, zol-revival, drift-audit-skill),
three ready (ledger-reconciliation, signer-committee, frapp-gh-phase1),
three blocked on Zaal gates (zid-allocation tier size, facilitator names,
archive-the-14). Inspect: `orca orchestration task-list` /
`orca orchestration gate-list` / `orca worktree ps`. Panes report with
`orca orchestration send --type worker_done`; the coordinator inbox is
`orca orchestration inbox`.
- Automations (cron) still unadopted: first candidate is the follow-graph audit in
  [[../inbox/queue-2026-08-25|the queue]], second is a nightly
  `repo-cleanup audit` snapshot.

Related: [[repo-estate]], [[obsidian-second-brain]]

## Stack snapshot - 2026-08-26 early morning (the agentic workflow update)

Eight lanes live or queued under run_a4892c0a5cdc: fractal (Orca-native
worktree, v0.2 pass, push held for Zaal's branch review), frapp-gh (day-1
async game), ZID policy (tier 1000), estate PII pass, bonfire lane (fractgram
indexing + dvl mojo search, outbound replies draft-only), dashboard-UI
research + Obsidian X-post research (one pane, sequential), coordinator
(verify + dispatch owner). Grill running here in the orchestrator via
quick-grill batches; verdicts recorded same-tick. ZORCA public (MIT), GUI at
:7777, watcher in queue mode, zorca up/down/status launcher. Orca itself
turned out to be MIT open source - fork-with-upstream-sync chosen by Zaal
over overlay-only (mechanism: gh repo fork + scheduled gh repo sync).
Weekly cap: fumes until Wed 6am; Zaal accepts plan-move if it runs dry.

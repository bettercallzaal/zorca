---
type: playbook
status: active
created: 2026-08-25
updated: 2026-08-25
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
- **Pickers eat text**: a pane sitting on a numbered picker sends any text
  into a free-text field. The board detects choice-prompt; answer with arrow
  keys + Enter, verify cursor with a read first.

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

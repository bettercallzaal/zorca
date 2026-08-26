# ZORCA

The ZAO orchestration layer for [Orca](https://orca.stably.ai). Orca gives you
many terminal panes running coding agents; ZORCA makes them one operation - a
ranked board, an auto-continue watcher with hard safety rails, an estate
auditor, and the operating conventions that survived a real multi-agent day.

Orca itself is closed source and unaffiliated. ZORCA only drives its public
CLI (`orca terminal ...`, `orca orchestration ...`) - nothing here patches or
redistributes the app.

## What is in here

| Piece | What it does |
|---|---|
| `bin/orca-board` | Ranked board of every live pane (`ctx-critical` > `choice-prompt` > `asked-question` > `waiting` > `idle-done` > `bare-shell`). `--auto` drafts and sends next steps to stalled panes; `--draft` dry-runs; `--tail <repo>` follows one pane; `--json` for machines. |
| `bin/repo-cleanup` | Estate auditor: uncommitted vs unbacked vs stray work, duplicate clones, archive candidates, license gaps. Every mutating subcommand is dry-run without `--apply`. |
| `PLAYBOOK.md` | The operating conventions: one pane per lane, ctx>85% means handoff, file ownership between panes, the hazards that actually happened and the rules they produced. |

## The safety rails (each one bought with a real failure)

1. **Danger words** - drafts and pane text matching license/publish/delete/
   archive/push/merge/rotate/credential are HELD for the human, never sent.
2. **Draft screening** - the draft itself is screened, not just the pane; a
   stalled pane with an innocent question can still get a dangerous draft.
3. **No fabrication** - the drafter writes as the orchestrator, never as the
   human; it may decide between offered options, never assert world-facts
   (payments, approvals, access). Real-world actions exit as NEEDS-HUMAN.
4. **Provenance** - every auto-sent message is prefixed `[auto-draft]` so the
   receiving agent can discount its factual claims.
5. **Receipt checks** - a send is not a delivery; the watcher confirms the
   pane actually holds the text (compaction and restarts eat briefs).
6. **Evidence rule** - only the human's own typed text or a resolved
   decision gate proves a human action. Anything else claiming one is held.

## Requires

- Orca installed with its CLI on PATH (`orca status` works)
- python3, `claude` CLI for the drafter
- `gh` for the estate auditor's GitHub passes

## Status

Extracted 2026-08-25 from a live 13-pane session run by The ZAO. APIs are
Orca's public CLI surface and may shift under app updates.

# ZORCA - retired to a pointer, 2026-09-06

**The ZAO orchestration layer does not live here any more. It lives in
`zaal-dotfiles/bin`.**

This repo was public, MIT, and named "the ZAO orchestration layer" while holding
9 of the layer's 114 tools - two of them stale, one of them a broken copy of a
safety tool. That was worse than holding none, because anyone cloning it got the
broken version. It is now a pointer.

## Where the layer actually is

`zaal-dotfiles/bin`, 105 tools before this move and 109 after. `~/bin` **is**
that directory. Everything the layer does is there:

| | |
|---|---|
| Board and lanes | `zj`, `zao-lanes`, `zao-lane-boot`, `zao-lane-health`, `zao-lane-watch`, `orca-board` |
| One seat at a time | `zorca-lock` (claim / heartbeat / check / release) |
| Briefing | `zorca-brief` - briefs are FILES, because `orca terminal send` drops the head of long messages |
| Sensing | `zao-tick`, `zao-selftest`, `zao-morning` |
| Handing back | `zao-reap`, `zao-bundle-unbacked`, `zorca-bundle` |
| Messaging | `lane-send` |
| ZOE v2 lane control | `zorca-actuator`, `zorca-lane-enqueue` |

## What moved out of here, and where it went

All four tools that existed **only** in this repo were absorbed into
`zaal-dotfiles` in PR #103 before this retirement, so nothing was dropped:
`zorca-actuator` (439 lines), `zorca-actuator-test` (100), `zorca-gui-test`
(231), `zorca-lane-enqueue` (75).

The rest were already in dotfiles - `repo-cleanup`, `zorca`, `zorca-bundle` and
`zorca-lock` byte-identical, and `orca-board` and `zorca-brief` in *newer*
versions there (585 vs 505 lines, and 113 vs 18).

Nothing is deleted. Git history holds every version, and the canonical copies are
live in dotfiles.

## Why the layer is not public

`zaal-dotfiles` is private and unlicensed. Making the orchestration layer public
is a deliberate extraction with a licence decision attached, not a side effect of
where files happen to sit. This repo had 0 stars, so nothing depended on it.

If that extraction ever happens, it starts here, from `PLAYBOOK.md`.

## What is still worth reading here

- **`PLAYBOOK.md`** - the operating conventions that survived a real multi-agent
  day. Its sibling is `zao-vault/notes/orca-organization.md` (12 conventions and
  every hazard that actually happened) and
  `zao-vault/notes/lane-supervision-playbook.md`. All three describe the same
  job; the vault ones are the maintained copies.
- **`ZOE-CENTER.md`** and `docs/DESIGN-bridge.md` - design notes.
- **`LICENSE`** - MIT, unchanged.

## Context

Orca itself is closed source and unaffiliated. Nothing here ever patched or
redistributed the app; it drove the public CLI.

The reasoning for this retirement, and the two other consolidation jobs it is
part of, is in `zao-vault/notes/zao-orchestrator-2026-09-05.md`.

---
type: design
status: proposed
created: 2026-09-09
component: zorca repo layout
decides: what lives in this public repo, what stays a pointer to private dotfiles
---

# Repo layout - what lives here and what does not

**Proposal. No code was moved to write this.** It exists so the refill of this
repo happens on a rule rather than by drift, because the last time this repo
held tools it drifted into shipping stale copies of them.

## The rule

> **A public copy of a tool that is not the copy that runs is worse than no copy
> at all.**

Everything below follows from that one line. It is not a style preference; it is
the finding that caused the 2026-09-06 retirement, and the evidence was a public
`zorca-brief` at 18 lines against the 113-line version actually in use - a broken
copy of a safety tool, published under the layer's own name.

The test for any file: **if this copy went stale, would anyone find out?** If the
answer is no, it does not belong in a public repo.

## Three categories

### 1. Lives here - things that cannot go stale silently

Documents whose truth does not depend on one machine's filesystem, and which a
reader can check against their own experience rather than against a private
directory.

| Path | What | Why it is safe here |
|---|---|---|
| `PLAYBOOK.md` | Operating conventions, supervision rules, hazards | Conventions, not code. A reader can disagree with it; they cannot get a broken binary from it |
| `README.md` | What the layer is, and this boundary | Same |
| `docs/REPO-LAYOUT.md` | This file | Same |
| `docs/DESIGN-bridge.md` | ZOE v2 lane control design | Marked proposed and not built, so there is nothing to drift from |
| `ZOE-CENTER.md`, `zoe-analysis-2026-08-27.md` | Design plus its evidence | Design only. Already written with no hostnames, paths, keys or account identifiers - components are named by role |
| `gui/` | The board UI: `zorca-gui`, `zorca-gui2`, `contrast-check.py`, `field-audit.py` | **The exception, and it is deliberate - see below** |
| `LICENSE` | MIT | |
| `docs/drafts/issue-templates/` | Issue templates | Drafts, unadopted |

### 2. Stays a pointer - the whole executable layer

Roughly 109 tools in `zaal-dotfiles/bin`, which is **private and unlicensed**.
Named here by role so a reader knows what exists, with no copy to go stale:

| Role | Tools |
|---|---|
| Board and lanes | `zj`, `zao-lanes`, `zao-lane-boot`, `zao-lane-health`, `zao-lane-watch`, `orca-board` |
| One seat at a time | `zorca-lock` (claim / heartbeat / check / release) |
| Briefing | `zorca-brief` - briefs are FILES, because `orca terminal send` drops the head of long messages |
| Sensing | `zao-tick`, `zao-selftest`, `zao-morning` |
| Handing back | `zao-reap`, `zao-bundle-unbacked`, `zorca-bundle` |
| Messaging | `lane-send` |
| ZOE v2 lane control | `zorca-actuator`, `zorca-lane-enqueue` |
| Launcher | `zorca` (up / down / status) |

**Extraction, if it ever happens, is one-directional and deliberate.** The
public copy becomes canonical, with its tests, and the private one becomes the
pointer. Never a copy in both places, and never a copy made because a file
happened to be convenient to move.

### 3. Named, not started - the federation contract

Nothing exists yet and nothing should be built until the public contract it must
match has actually been read. When it is, it lands here, because a capability
card that is not public is not a capability card:

| Planned path | What |
|---|---|
| `federation/capability-card.json` | civilization id, protocol versions, public key, capabilities, accepted work packet types, transport endpoints, proof requirements, credential requirements, payment methods, data egress policy, max delegation, callback endpoints |
| `federation/envelope.md` | The mapping: internal packet to public envelope, and the receipt chain back |
| `federation/README.md` | What crosses the boundary and what does not |

**Blocking, and it is one question:** the public federation contract and the
receipt format have not been read by anyone here. No envelope can be specified
against a contract nobody has seen, so no code is written until that is
resolved. Recorded rather than guessed.

Two constraints that are already settled and should survive into whatever is
built:

- **Owner-agent and machine do not cross the boundary.** A partner asks for a
  capability and never learns which component provides it. That is what
  "normalize at the boundary, preserve internal ontology behind it" means in
  practice.
- **Identity lives above the machine.** If a host dies, the agent resumes
  elsewhere. Machine is body, model is brain, identity is the agent. That makes
  identity a repo-and-vault concern, not a per-machine one.

## The `gui/` exception, and the open question in it

`gui/` holds runnable Python, which looks like a contradiction of the rule. It
is here on purpose: it is a self-contained UI with no private counterpart, so
there is no second copy for it to drift from. It is also the only part of this
repo that has ever had a security bug - the :7777 injection holes, closed by
`4a5de63` (index-based handlers, a validated manifest, an origin guard).

**Open question for this PR:** the private launcher `zorca` starts the GUI from
a hardcoded path inside a checkout of this public repo. That makes a private
tool depend on a public working copy being present and current - which is the
same coupling this layout exists to prevent, pointing the other way. It was
measured tonight: the pull that closed the injection holes also deleted the
launcher, and for four minutes `zorca` was off PATH estate-wide. Restoring it
took one command; the coupling that made it possible has not been decided.

Three options, not chosen here:

1. **Leave it.** The GUI is public, the launcher is private, and the launcher
   knows where the checkout is. Simplest, and the coupling is real but small.
2. **Move `gui/` into dotfiles.** Removes the coupling and takes the UI private.
   Costs the one piece of running code this repo has.
3. **Make the launcher's GUI path configurable**, defaulting to the checkout and
   failing loudly when it is absent, rather than silently starting nothing.

Option 3 is the smallest change that removes the silent-failure mode, which is
the part that actually bit. It is a decision about a private file, so it is not
made here.

## What this layout does not settle

- Whether this repo is the right home for the capability card, or whether it
  gets its own public repo. That is a decision with a licence attached.
- Whether the ZOE v2 lane control pair are dead code or the head start on the
  adapter. They implement a queue record, a mandatory expiry, an idempotency-
  shaped id and a refusal path across a trust boundary, which is most of the
  envelope shape - but neither has ever run.
- What the layer is called in public if any of it is extracted.

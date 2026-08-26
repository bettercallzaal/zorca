---
type: design
status: proposed
created: 2026-08-26
component: zorca-bridge
decides: where it runs, how it reaches the orchestrator, what it is allowed to do
---

# ZORCA Bridge - design

A chat front end for ZORCA, so the operating loop that today needs a Mac
keyboard can be driven from Telegram or Discord: read the ranked board, read
pending gates, resolve a gate, approve or drop a queued draft, tail a lane,
wake a parked lane.

**Design only.** Nothing in this document is built. Every number below was
measured on 2026-08-26 unless marked derived.

## 0. Brief provenance

The brief that produced this document arrived head-truncated in the pane -
the failure mode PLAYBOOK.md already records (`terminal send` loses the HEAD
of a long message, not the tail). What survived was: where it runs (VPS vs
OpenMatter container vs both), the Telegram/Discord bridge, how it reaches
the orchestrator (orca CLI over SSH / orchestration DB / ZORCA GUI API at
:7777), staged build plan, design only, worker_done when committed.

The scope below is reconstructed from ZORCA's own code plus the vault, not
guessed silently. The component name `zorca-bridge` is this lane's choice and
is the one thing Zaal may want to overrule.

## 1. The measurement that settles "where it runs"

```
$ ls -la /opt/homebrew/bin/orca
/opt/homebrew/bin/orca -> /Applications/Orca.app/Contents/Resources/bin/orca
$ file /opt/homebrew/bin/orca
Bourne-Again shell script text executable
```

The `orca` CLI is a shim into a macOS `.app`. It is not a daemon, not a
static binary, and not portable. The orchestration DB it reads lives at
`~/Library/Application Support/orca/orchestration.db`. The panes it drives are
windows in a running Mac GUI app.

So the question "VPS vs OpenMatter container vs both" has a forced answer and
it is neither of the two on offer:

**The hands must be on the Mac. Only the mouth can move.**

Nothing on a Linux VPS or in a Hermes container can run `orca terminal send`,
create a pane, or resolve a gate. Any design that puts the actuator off-Mac
is designing a thing that cannot exist.

That leaves a genuine split, and this is the real decision:

| Half | What it does | Where it can run |
|---|---|---|
| **Actuator** | `orca` CLI calls, orchestration DB reads, pane scraping | Mac only. Forced. |
| **Front end** | Telegram/Discord long-poll or gateway, auth, formatting | Mac, VPS, or container. Free choice. |

### Recommendation: both halves on the Mac, for v1

The front end is a long-poll loop against Telegram's API. It needs outbound
HTTPS and nothing else - no inbound port, no public IP, no webhook, no TLS
cert. The Mac already has outbound HTTPS. Putting the front end on the VPS
buys one thing (it survives the Mac sleeping) and costs a transport hop, a
second secret store, a second deploy target, and a new class of failure where
the front end is up and cheerfully answering while the actuator is
unreachable, which is the exact "service-pulse is not run-heartbeat" trap
that let farscout zombie for two months.

Run both on the Mac under one launchd agent. Revisit only if Stage 4's
survives-a-sleeping-Mac requirement becomes real.

### Why not the OpenMatter container

Ruled out on its own terms, not by preference:

1. It cannot run `orca` (section 1).
2. Credits are metered. The bridge is an idle long-poll that must run 24/7 -
   the worst possible shape for per-hour billing. Derived rate 0.837 Cr/hr
   against a ~12 Cr grant balance is under a day of continuous uptime.
3. The credits are a partner grant earmarked for a newsletter-agent beta.
   Spending them on infrastructure Zaal already owns is a cost regression and
   a misuse of the grant's stated purpose.
4. The container in question is Nous' Hermes Agent template, whose dashboard
   and API server are the subject of an active exposure campaign. Adding a
   bot token to that blast radius is a downgrade.

OpenMatter stays WATCH as infra and live as a relationship. It is not the
home for this.

## 2. How the bridge reaches the orchestrator

Three candidate paths were named. They are not alternatives - they are three
layers, and the right answer uses two of them.

| Path | Reads | Writes | Verdict |
|---|---|---|---|
| **Orchestration DB direct** (`sqlite3 file:...?mode=ro`) | tasks, specs, gates - instant, no subprocess | never | **Adopt for reads.** Already the GUI's primary path with a CLI text-parse fallback when the schema shifts. Reuse both, including the fallback. |
| **ZORCA GUI API at :7777** | `GET /api/state` - the whole cached board in one call | `POST /api/resolve`, `/api/focus`, `/api/lane`, `/api/draft` | **Adopt as the only write path.** |
| **orca CLI over SSH** | anything | anything | **Reject for v1.** |

### Why the GUI API and not the CLI

The GUI already solved the two hard problems and solved them once:

- **The pane scrape costs about 1 second per pane.** The GUI refreshes in a
  background thread and serves a cache instantly. A bridge shelling out to
  `orca-board --json` per message would make a 13-pane board a 13-second
  reply, and would race the watcher for the same panes.
- **Every mutation already has an audited shape.** `/api/draft` with
  `action:send` deliberately omits the `[auto-draft]` prefix because a human
  tapped it, and the code says so at the call site. `/api/lane` spawns a paid
  session and the button says so. Re-implementing these in a second process
  means re-deciding those calls, and one of them will be decided differently.

One actuator, two front ends (browser and chat). Not two actuators.

### Why not SSH

SSH from a VPS into the Mac means a long-lived inbound key on a laptop, over
Tailscale, whose DNS gap is a known failure that hits precisely when Zaal is
on the move - which is the only time the bridge matters. It also re-opens
arbitrary command execution as the transport, when the whole point of the
GUI API is that the verb list is finite and each verb is reviewed. If Stage 4
ever moves the front end to the VPS, the transport is a Tailscale-scoped HTTP
call to :7777, not a shell.

**Required change:** the GUI binds `127.0.0.1` only. Keep it that way. The
bridge is a localhost client. It never widens that bind.

## 3. Command surface

Read verbs, anyone on the allowlist:

| Command | Backed by |
|---|---|
| `/board` | `GET /api/state` -> panes, ranked, one line each |
| `/gates` | cached pending gates, with options |
| `/drafts` | the HOLD/QUEUE trail, `~/.zao/orca-drafts.json` |
| `/tail <lane>` | pane text from cached state |
| `/status` | the `zorca status` four lines |

Write verbs, Zaal only, each an explicit tap:

| Command | Backed by | Note |
|---|---|---|
| `/gate <id> <resolution>` | `POST /api/resolve` | resolution echoed back before it fires |
| `/send <draft-id>` | `POST /api/draft action:send` | carries Zaal's authority, no `[auto-draft]` prefix |
| `/drop <draft-id>` | `POST /api/draft` | queue drop only |
| `/focus <handle>` | `POST /api/focus` | |
| `/lane <n>` | `POST /api/lane` | **spawns a paid session.** Must say so in the confirm. |

Not in v1, deliberately: free-text into a pane. A bridge that can type
anything into any pane is a remote shell with a chat UI, and the pane it
types into may be sitting on a numbered picker that eats text as a free-text
field. If free-text is wanted later it goes through the draft queue like
everything else, so it inherits danger-word screening.

## 4. Safety rails

The bridge inherits ZORCA's six rails unchanged and adds three that are
specific to being reachable from a phone.

7. **Single-principal allowlist.** A hardcoded numeric Telegram user id (and
   Discord user id + guild id). Not a username - usernames are reassignable.
   Any message from anyone else is dropped silently, not answered with a
   refusal, because a refusal confirms the bot exists.
8. **Write verbs are confirm-then-fire.** Every mutating command echoes what
   it is about to do and waits for a second tap. The Mac GUI has a screen to
   make an accidental click unlikely; a phone keyboard does not.
9. **Chat is not evidence.** A message in Telegram claiming a human did
   something is not proof a human did it. Only a tap that arrives through the
   allowlisted principal and produces a resolved gate counts. This is the
   evidence rule (rail 6) restated for a surface where impersonation is
   cheaper.

Danger-word screening stays where it is - in the watcher, on the draft. The
bridge does not re-implement it; it displays HOLD lines so Zaal can decide
them, which is the whole point.

## 5. Secrets

Bot token in `~/.zao/zao.env`, never in the repo, never in a transcript.
Entered via `/secret`. If Stage 4 moves the front end to the VPS the token
moves with it and the Mac keeps none - one token, one host, never both.

## 6. Staged build plan

Each stage is shippable and useful alone. No stage requires the next.

**Stage 0 - read-only Telegram, one command.** Long-poll loop, allowlist
check, `/board` only, rendered from `GET /api/state`. Proves the transport,
the auth, and the formatting budget (Telegram's 4096-char message limit
against a 13-pane board) before anything can mutate state. Half a day.

**Stage 1 - the rest of the read verbs.** `/gates`, `/drafts`, `/tail`,
`/status`. Still zero write paths. At this point the bridge already delivers
the thing the vault's phone-hop note names as the top gap: a one-tap "which
lane needs me" view that is not terminal-only.

**Stage 2 - gates, the highest-value write.** `/gates` renders inline
keyboard buttons from the gate's own `options` array, which the GUI already
parses. Tap resolves via `POST /api/resolve`. Gates are the thing that blocks
lanes for hours while Zaal is away from the desk, so this stage is where the
bridge starts paying for itself. Confirm-then-fire from the first commit.

**Stage 3 - the draft queue.** `/drafts`, `/send`, `/drop`. Push
notification on new HOLD lines so Zaal learns of a held draft instead of
polling for one. This is the stage that makes the watcher's queue mode
genuinely asynchronous.

**Stage 4 - lane control and the survives-a-sleeping-Mac question.**
`/focus`, `/lane`. Only here does the front-end-on-VPS question become real,
and only if the Mac sleeping in the middle of a run turns out to be a
frequent failure rather than a hypothetical. If it does: front end to the
VPS, Tailscale-scoped HTTP to :7777, token moves off the Mac, and the
bridge reports actuator-unreachable explicitly rather than going quiet.

**Discord** is deliberately not a stage. It is a second adapter behind the
same command layer, worth building only once the Telegram command set has
stopped changing. Building both at once means every command decision gets
made twice and the second one drifts.

## 7. Open for Zaal

1. Name: `zorca-bridge`, or fold it into ZOE (`@zaoclaw_bot`) as a command
   group? ZOE already owns the phone surface and the vault note argues for
   fewer apps, not more. Against: ZOE runs on the VPS and cannot reach the
   Mac's `orca`, so folding in means the VPS-front-end hop at Stage 0 rather
   than Stage 4.
2. Does `/lane` belong in the bridge at all, given it spends money on a tap
   from a lock screen?
3. Telegram first, or Discord first?

Related: [[orca-organization]], [[phone-hop-in-anywhere]], PLAYBOOK.md

# ZOE at the center

> Mandate, Zaal 2026-08-27: *"improve our orchestrator being the ZOE at the
> center and find how we can put things together more."*

**Design only. Nothing here is built.** This repo is public, so no hostnames,
paths, keys or account identifiers appear below - components are named by
role.

## 0. The constraint that shapes everything

**Evidence lives in [`zoe-analysis-2026-08-27.md`](zoe-analysis-2026-08-27.md).
One writer per fact: that lane owns the numbers, the categories and the
quotes. This document cites them and carries design only.**

An earlier revision of this section carried my own measurements of the export.
They are **withdrawn** in favour of that doc, which decomposes the traffic far
further than mine did - my classifier dropped 89.5% of messages into an
undifferentiated bucket, and theirs opens it.

**One of my withdrawn conclusions was wrong, not merely coarser**, and it is
worth naming rather than quietly deleting: I measured failure notices at a low
reply rate and concluded they were noise Zaal ignores. The analysis lane
measures the opposite - **breakage is the one thing he reliably answers**,
at many times the rate of a decision card. My number was a substring artifact
over a different window. **Any design that suppresses failure reporting to cut
volume would have been built on my error.** Cut the feed, not the alarms.

### What this constrains, in design terms

Taking that doc's findings as given, four things follow for this design. Three
of them contradict what I proposed in the first draft.

1. **The command-surface framing is wrong.** Sections 5 and 9 assumed verbs
   like `/lane` and `/board`. He overwhelmingly writes prose, not commands.
   **Natural language is the front door; commands are the accelerator.**
2. **An ask queue that ADDS messages fails by arithmetic.** His replies are
   the scarce resource and the budget is tiny. The queue must **displace**
   output, not add to it.
3. **Grill cards are the specific thing not to ship into this channel.**
   Build step 2 proposed exactly that. The analysis lane measures enumerated
   decision cards as both the largest class of ZOE's traffic and its
   worst-answered - a queue enumerated into a chat window. That is a direct
   refutation of my own step, on far better evidence than the eight cards my
   pass saw.
4. **Bounded questions still work - they are drowning, not failing.** Gates
   and completions answer far above baseline. The ask-queue idea survives; the
   volume it would arrive in does not.

**The corrected goal: v2 sends less and answers more.** Not "ZOE reaches more
surfaces" - it already reaches him constantly and is mostly skipped.
Centering the estate on that channel without cutting its volume routes
everything into a firehose he has learned to ignore.

## 1. What changes

`docs/DESIGN-bridge.md` treats ZOE as a **bridge**: a chat front end bolted
onto ZORCA so lanes can be opened from a phone. That framing is too small,
and it is the wrong way round.

**ZOE is the front door. The orchestrator and the Orca lanes are ZOE's
hands.** Every input arrives at ZOE; ZOE decides what it is and who should
touch it; the hands do the work; the answer comes back out through ZOE.

The bridge design is not wasted - it is one limb (section 5). But `/lane`
stops being *the* feature and becomes one verb among several.

## 2. The thesis, in one paragraph

The estate does not lack surfaces. It has too many, and they are already
doing the same three things: **take an input, ask a human a bounded
question, hand work to a lane.** Meetings do it in Phase 3.5. The
orchestrator does it with gates. The grill does it with tap-to-answer
cards. ZOL does it with human-gated drafts. The board does it with the HOLD
queue. Five implementations of two verbs. Putting things together means
collapsing them onto one front door, not adding a sixth.

## 3. The one unification that matters

**Every one of these is a bounded question with options, waiting for a tap:**

| Today | Where it lives | Reachable from a phone? |
|---|---|---|
| Orchestration gate | orchestration DB, `gate-list` | no |
| `quick-grill` batch | `AskUserQuestion`, a local TUI | **no, and it cannot be** |
| ZOE grill card | ZOE, Telegram | yes |
| Held auto-draft | the watcher's HOLD queue | no |
| ZOL draft awaiting approval | drafts on the Pi | no |
| Phase 3.5 lane weigh-in | packet files in a worktree | no |

Four of six are unreachable from the one surface Zaal actually carries.

Worse, `AskUserQuestion` is not merely inconvenient - it is **structurally
unanswerable** by anything but a human at that terminal. The Orca dispatch
preamble says so in its own words, forbidding it outright for dispatched
workers and routing them to `orchestration ask` instead; the meeting skill
records the same constraint. So the grill, today, can only be run by someone
sitting at the Mac.

**The unification: one `ask` type, one queue, one renderer.** A bounded
question - text, options, an owner, a deadline - is a single record. ZOE
renders it as a Telegram inline keyboard. The tap resolves it at source,
whatever the source was. Gates, grill cards, HOLD decisions, ZOL drafts and
weigh-in requests stop being five things.

This is the highest-value item in this document, and it is not `/lane`.

## 4. The map

```
   INPUTS                    ZOE  (the front door)              HANDS
   ------                    -----------------------            -----
   Telegram msg  ─┐          ┌──────────────────┐          ┌─ Orca lane
   Discord       ─┤          │ classify         │          │  (worktree,
   Farcaster     ─┼────────▶ │ authorize        │ ───────▶ ├─  pane, brief,
   /meeting      ─┤          │ ask if unclear   │          │   dispatch)
   grill answer  ─┤          │ route            │          ├─ orchestrator
   chat export   ─┘          └──────────────────┘          │  (vault, docs)
                                     ▲    │                 ├─ ZOL (Farcaster)
                                     │    ▼                 └─ Bonfire (memory)
                                 ┌───────────────┐
                                 │  ask queue    │  one record type,
                                 │  (bounded     │  one renderer,
                                 │   questions)  │  taps resolve at source
                                 └───────────────┘
```

Two rules keep this honest:

- **ZOE classifies and routes. ZOE does not resolve.** It cannot see the
  estate - it runs off-Mac - so any repo path, worktree or lane identity it
  produced would be a guess. It forwards the request and the principal.
- **Everything irreversible is a tap, never an inference.** Unchanged from
  the rails that already exist.

## 5. What connects to what

| Input | State today | Folding it in means |
|---|---|---|
| **`/lane`** (`bin/zorca-lane-enqueue`, `bin/zorca-actuator`) | **Built and tested this session**, Mac half only. 16 tests green. | ZOE-side command + confirm tap. The contract is already executable, so this is small. See `docs/DESIGN-bridge.md` s12. |
| **Meetings, Phase 3.5** | **Built and battle-scarred.** Classifies lanes, sends packets, bounded 10-minute wait, then fans out. Refuses bare shells and panes on pickers; ranks by pane title; clears its own trust gate. | Its weigh-in request becomes an **ask-queue record**, so a lane's silence is visible on the phone instead of only in a directory. Phase 3.5 is the reference implementation of the whole pattern - do not redesign it, generalise it. |
| **Grill** | `AskUserQuestion`, Mac-terminal only. | Becomes ask-queue records rendered as inline keyboards. This is the single biggest reachability win and it needs no new concepts. |
| **ZOL** | Live daemon on the Pi. Farcaster identity with its own signer. Posts human-gated, **no spend capability by design**. Already described as *a child of ZOE* - the hierarchy exists on paper and not in code. | Outbound already works. What is missing is **inbound**: replies and mentions do not reach the orchestrator, so ZOL is a mouth without an ear. Route mentions in as ask-queue records ("reply to this?"), never as auto-posts. |
| **Chat export** | **Landed 2026-08-27**: `~/.zao/telegram-exports/zoe/result.json`, 7.0 MB, 10,142 messages. A separate ZOE-analysis lane in this repo is mining it. | Already producing section 0. The ingest slot below points at that path. |
| **Discord** | Not built. | A second adapter behind the same command layer. Deliberately last - see section 8. |

## 6. Telecast is the shape

`99darwin/telecast` - a Farcaster micro-client inside Telegram, TypeScript,
small. Read for structure, not for code.

**What it proves.** A Telegram bot is a perfectly good universal client for
a network it has no native relationship with. Its command table is flat and
verb-shaped - feed, cast, replies, channel cast - and the network's identity
lives behind a signer the bot holds. That is exactly the ZOE-center claim:
the front door does not need to *be* the system, it needs to hold a
credential per system and speak a verb per action.

**What to copy.** One command group per network. Feed in, post out, replies
surfaced. State keyed per user rather than global.

**What to avoid, and its author says so first.** Its README warns that the
signer-management commands are sensitive and should be removed or
authenticated after setup. Telecast is single-user hobby scale; ZOE would be
holding a signer for a live Farcaster identity, a bot token, and the ability
to open paid lanes. **Signer and credential management must never be chat
commands in ZOE.** Ever. The pattern to take is the client; the pattern to
reject is administering the keys from the same surface that uses them.

## 7. The chat-export ingest slot

Zaal is exporting his real ZOE Telegram chat. That export is the highest-
value corpus in the estate for one specific question: *what does he actually
ask ZOE for?* Every command surface above is a guess about that until the
export is read.

**The file.** `~/.zao/telegram-exports/zoe/result.json` - 7.0 MB, single-chat
export shape, 10,142 messages. **It stays there.** It is private data about
other people as well as Zaal; it does not enter this repo or any repo, and the
ingester reads it in place.

**Reuse, do not rebuild.** `zabalgamez` branch `ws/bonfire-lane` carries
`scripts/telegram-export-to-bonfire.mjs` (370 lines, commit `fe384eb`),
which already:

- handles **both** Telegram Desktop export shapes (single-chat root, and the
  multi-chat `chats.list` form);
- segments messages into conversation units by **quiet gap** rather than by
  message, because one chat line is rarely one idea;
- floors on minimum length, truncates long bodies, supports `--since`,
  `--limit`, `--chat`, `--out`;
- is **dry-run by default** and posts only on an explicit `--post`.

That dry-run default is the reason to reuse it rather than write a fresh
one: an ingester whose safe mode is the default has already made the
decision that matters.

**The slot.** Ingest is a ZOE input like any other, but batch and offline:

1. **Extract, do not post.** Run it with `--out` only. Produce segments.
2. **Classify before anything is written anywhere.** What fraction of
   segments are captures, tasks, questions, decisions, or chatter? That
   histogram *is* the command-surface spec - it tells you which verbs ZOE
   needs, ranked by real frequency rather than by what seemed likely.
3. **PII gate before any post.** This is Zaal's own chat: it contains other
   people, and the estate has been burned twice this month by publishing a
   name-to-identifier linkage. Nothing from the export reaches Bonfire or a
   repo until that pass runs and Zaal accepts it. **Blocking, not advisory.**
4. **Then, optionally, memory.** Segments that are genuinely decisions can
   become Bonfire episodes with `--post`.

**Two prerequisites, both real.** The script is on an **unmerged branch in a
different repo** - so either merge it there or vendor it deliberately, but do
not fork it silently into a third copy. And the export itself is private
data: it belongs off-repo, like the other private transcripts already are.

## 8. Gaps, measured

1. **The ask queue does not exist.** Five question surfaces, no common
   record. Everything in section 3 depends on this.
2. **`AskUserQuestion` cannot be answered remotely** - structural, recorded
   in both the Orca preamble and the meeting skill. The grill is Mac-bound
   until it moves onto the ask queue.
3. **ZOL has no inbound path.** It posts and replies on its own daemon;
   nothing routes a mention to the orchestrator or to Zaal.
4. **ZOE cannot enqueue against the cowork control plane.** The enqueue
   route opens a board session, and ZOE holds a bot token, not a session.
   Known and costed in `docs/DESIGN-bridge.md` s3.3.
5. **One webhook URL per bot token.** Telegram permits exactly one. Every
   additional input - Discord, Farcaster, export - must arrive by a
   *different* mechanism, not a second webhook on the same bot. This
   constrains section 4 more than it looks.
6. **The export ingester is on an unmerged branch in another repo.**
7. **ZOE cannot see the estate.** Not a defect - it is why ZOE classifies
   and the Mac resolves - but it means every path-shaped decision must be
   deferred to a hand, and any design that forgets this produces fabrication.

## 9. Build order

Ordered so each step is useful alone and unblocks the next.

**0. Cut ZOE's output first.** Nothing else in this list survives contact
with the ratio the analysis doc measures. That doc's traffic table names the
targets and ranks them; use it rather than guessing. Set a daily budget, batch
the rest into one digest, drop the classes that measure near zero - **and
leave failure reporting alone**, because it is the class he actually answers.
Measurable before and after, from the same export.

**1. The ask queue - as a REPLACEMENT for volume, not an addition.** One
record type: question, options, owner, deadline,
source, resolution. ZOE renders inline keyboards; a tap writes back to the
source. Migrate **orchestration gates first** - they already carry an
`options` array the GUI parses, so they are the cheapest real proof. This
is first because it is what makes every later step answerable from a phone.

**2. Grill off `AskUserQuestion` - but NOT into the chat feed.** Removing that
dependency is still right: today the grill needs a human at the Mac. But the
analysis doc shows enumerated decision cards are the single worst-performing
thing ZOE has ever done, so the destination is a **surface he opens**, not a
message stream he scrolls past. Send a small batch, measure against the rate
gates achieve, and migrate only if it clears.

**3. `/lane` end to end.** The Mac half exists and is tested; add ZOE's
command, the confirm tap, and the result report. Per `docs/DESIGN-bridge.md`
s12.3, on the queue-file transport.

**4. The export ingest.** Extract, classify, PII-gate. Its output **reorders
everything after this point**, so it lands before the remaining verbs are
designed - building more commands before reading what he actually asks for
is guessing with extra steps.

**5. Phase 3.5 generalised.** Its weigh-in becomes an ask-queue record. Then
any input, not just a meeting, can ask the lanes that own it before fanning
out. This is the step where "put things together" is actually finished.

**6. ZOL inbound.** Mentions and replies arrive as ask-queue records.
Outbound stays human-gated and ZOL keeps no spend capability.

**7. Discord.** A second adapter behind a command layer that has stopped
moving. Last, deliberately: building it earlier means every command decision
is made twice and the second one drifts.

## 10. Open, for Zaal

1. **Where does the ask queue live?** The cowork Supabase (already has a bot
   control plane and a board that could render it) or the orchestration DB
   (already holds gates, but is Mac-local and invisible to ZOE)? Neither is
   obviously right and it is the load-bearing choice in this document.
2. **Does ZOE ever get to answer for you?** Everything above assumes no -
   ZOE asks, Zaal taps. A "ZOE may resolve questions below confidence X"
   rule would change the character of the system and is not proposed here.
3. **Merge or vendor the export ingester?**
4. **Are the export aggregates publishable at all?** This repo is public,
   and they are behavioural data derived from a private chat that a stranger
   could not derive. Moving them out of this document does **not** settle it -
   they now live in `zoe-analysis-2026-08-27.md` in the same public repo. Same
   shape as open question 7 in `docs/DESIGN-bridge.md`, same answer: **Zaal's
   call.** Raised once here rather than twice; that doc's lane owns the
   content, so any redaction is theirs to apply and his to decide.
5. Open question 7 in `docs/DESIGN-bridge.md` is unrelated and still open.

Related: `docs/DESIGN-bridge.md`, `PLAYBOOK.md`, `README.md`

# ZOE v1, measured: what the record says v2 must do differently

**Date:** 2026-08-27
**Source:** the full ZOE personal chat export, 10,142 messages, 2026-03-28 to
2026-08-27 (151 days). Two participants: Zaal and the bot. No third party
appears in it.
**Method:** counts below are computed from the export, not estimated. Reply
rate means "a Zaal message followed within 30 minutes."
**Scope note:** this repo is public. Quotes are Zaal's own words to his own
bot. Paths, hostnames, keys, invite links and account identifiers have been
stripped from every quote.

---

## The headline

**ZOE did not lose Zaal by being wrong. It lost him by volume.**

| Month | Zaal | ZOE | ZOE per Zaal reply |
|---|---|---|---|
| Mar (partial) | 123 | 168 | 1.4 |
| Apr | 184 | 690 | 3.8 |
| May | 83 | 897 | 10.8 |
| Jun | 53 | 890 | 16.8 |
| Jul | 60 | 2,273 | 37.9 |
| **Aug** | **12** | **4,709** | **392.4** |

Zaal engaged most in April. From April to August his messages fell **93%**
while ZOE's output rose **6.8x** (and **28x** from March). Over the whole
record ZOE sent **9,627** messages against Zaal's **515** - a ratio of
**18.7:1**, and **392:1** by August.

Total sent to him: **5,525,545 characters, roughly 1.1 million words.** Mean
message 574 chars, median 514, p90 1,146.

**Only 8.6% of ZOE's messages ever drew a reply.**

---

## What ZOE actually says: the real taxonomy

The first pass classified by substring and dropped most traffic into `other`.
That bucket was read - 300 messages sampled evenly across all 151 days - and
the categories below were derived from what is in it, not guessed. All 9,627
bot messages are then classified. The residual type, `conversational answer`,
is a genuine category (ZOE replying in prose to something Zaal said), not a
leftover pile.

Reply rate here is stricter than the 8.6% headline figure: a message counts
as replied-to only if it was the **last** bot message before a Zaal message
within 30 minutes. 405 of Zaal's 505 messages attribute to a preceding ZOE
message this way; the other 100 he opened cold.

| Type | N | % | Mar | Apr | May | Jun | Jul | Aug | Reply rate |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| grill decision card | 2,977 | 30.9% | 0 | 0 | 0 | 0 | 0 | 2,977 | **0.03%** |
| conversational answer | 1,220 | 12.7% | 119 | 264 | 225 | 262 | 226 | 124 | **21.07%** |
| idle-session nag | 1,144 | 11.9% | 4 | 6 | 0 | 165 | 956 | 13 | 1.57% |
| research deliverable | 998 | 10.4% | 0 | 0 | 0 | 92 | 505 | 401 | 0.60% |
| social draft approval | 413 | 4.3% | 0 | 0 | 198 | 88 | 31 | 96 | 0.24% |
| watchdog/restart | 266 | 2.8% | 0 | 1 | 0 | 0 | 0 | 265 | 0.00% |
| usage tip | 219 | 2.3% | 0 | 0 | 219 | 0 | 0 | 0 | 4.57% |
| progress filler | 211 | 2.2% | 4 | 4 | 38 | 76 | 82 | 7 | 2.84% |
| failure report | 205 | 2.1% | 10 | 23 | 0 | 3 | 96 | 73 | **9.76%** |
| grill / decision question | 195 | 2.0% | 0 | 0 | 0 | 0 | 71 | 124 | 3.59% |
| test-script broadcast | 194 | 2.0% | 0 | 169 | 25 | 0 | 0 | 0 | 2.06% |
| research push (ZOE TIP) | 174 | 1.8% | 0 | 174 | 0 | 0 | 0 | 0 | 2.30% |
| recurring status report | 164 | 1.7% | 0 | 0 | 0 | 4 | 60 | 100 | 0.00% |
| work report | 151 | 1.6% | 27 | 12 | 76 | 16 | 18 | 2 | **21.85%** |
| build-candidate approval | 129 | 1.3% | 0 | 0 | 0 | 0 | 0 | 129 | 0.00% |
| scheduled brief | 128 | 1.3% | 0 | 30 | 62 | 29 | 7 | 0 | 2.34% |
| evening reflection | 104 | 1.1% | 0 | 0 | 28 | 33 | 26 | 17 | 6.73% |
| provider limit / credits | 99 | 1.0% | 0 | 1 | 0 | 0 | 2 | 96 | 0.00% |
| teammate mention relay | 84 | 0.9% | 0 | 0 | 0 | 0 | 64 | 20 | 1.19% |
| loop status | 80 | 0.8% | 0 | 0 | 0 | 80 | 0 | 0 | 3.75% |
| agent-bus relay | 75 | 0.8% | 0 | 0 | 0 | 0 | 0 | 75 | 0.00% |
| grill answer receipt | 72 | 0.7% | 0 | 0 | 0 | 0 | 68 | 4 | 12.50% |
| ritual nudge | 62 | 0.6% | 0 | 0 | 0 | 0 | 0 | 62 | 1.61% |
| subtask lifecycle | 56 | 0.6% | 0 | 0 | 4 | 26 | 26 | 0 | 3.57% |
| affirmation prose | 48 | 0.5% | 0 | 0 | 0 | 0 | 0 | 48 | 0.00% |
| bot activity log | 42 | 0.4% | 0 | 0 | 0 | 0 | 19 | 23 | 0.00% |
| event promo | 28 | 0.3% | 0 | 0 | 10 | 10 | 4 | 4 | 0.00% |
| cost report | 24 | 0.2% | 0 | 0 | 0 | 0 | 0 | 24 | 0.00% |
| stall/stale nag | 22 | 0.2% | 0 | 0 | 0 | 3 | 0 | 19 | 4.55% |
| capture ack | 14 | 0.1% | 0 | 0 | 0 | 1 | 8 | 5 | **21.43%** |
| empty/noise | 12 | 0.1% | 0 | 0 | 12 | 0 | 0 | 0 | 0.00% |
| system error | 10 | 0.1% | 4 | 6 | 0 | 0 | 0 | 0 | **70.00%** |
| cockpit digest | 5 | 0.1% | 0 | 0 | 0 | 0 | 4 | 1 | 0.00% |
| self-throttle notice | 2 | 0.0% | 0 | 0 | 0 | 2 | 0 | 0 | 50.00% |
| **TOTAL** | **9,627** | 100% | 168 | 690 | 897 | 890 | 2,273 | 4,709 | **4.21%** |

## What this attribution can and cannot say

**Every reply rate in this document, and in any document that cites it, is a
ceiling. It is not a measurement that a message worked.**

A rate is computed by crediting the **last** ZOE message before a Zaal reply.
But ZOE rarely sends one message. The 405 attributed replies arrived after
**2,064 ZOE messages** standing in their 30-minute windows - mean 5.1 per
reply, median 3, maximum 28. Only one message in each window can have been
the one that worked, so **1,659 messages (80.4%) sat inside a window that
produced a reply and cannot be shown to have earned any of it.** One reply
marks a whole burst answered.

Re-running every figure with the opposite rule - split each reply's credit
evenly across all messages in its window - moves the bands and does not move
the conclusion:

| Band | ceiling (last-message) | floor (split-credit) |
|---|--:|--:|
| ANSWER | 17.64% | 16.45% |
| ASK | 0.58% | 0.89% |
| BROADCAST | 1.97% | 2.18% |

Note the direction: split-credit *raises* ASK and BROADCAST, because credit
bleeds onto the bursty classes that happened to be nearby. Neither method is
the truth. The defensible claim is the ordering and its magnitude - **ANSWER
outperforms ASK by 20-30x under either rule** - and per-type rates should be
read as upper bounds, most inflated for the classes that arrive in bursts.

## The one line the table is saying

Every type divides into three bands: ZOE **answering** him, ZOE **asking**
him for a tap, and ZOE **broadcasting** at him unprompted.

| Band | N | % | Mar | Apr | May | Jun | Jul | Aug | Reply rate |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ANSWER (responds to him) | 1,814 | 18.8% | 154 | 286 | 343 | 461 | 428 | 142 | **17.64%** |
| ASK (wants a tap) | 4,964 | 51.6% | 4 | 6 | 198 | 256 | 1,122 | 3,378 | **0.58%** |
| BROADCAST (unsolicited) | 2,849 | 29.6% | 10 | 398 | 356 | 173 | 723 | 1,189 | **1.97%** |

**Answering is 30x more likely to get a reply than asking. ZOE went from
91.7% answering to 3.0% answering.**

| Month | ANSWER messages | total | answer share |
|---|--:|--:|--:|
| Mar | 154 | 168 | **91.7%** |
| Apr | 286 | 690 | 41.4% |
| May | 343 | 897 | 38.2% |
| Jun | 461 | 890 | 51.8% |
| Jul | 428 | 2,273 | 18.8% |
| Aug | 142 | 4,709 | **3.0%** |

The absolute number of answering messages barely moved - 154 in March, 142 in
August. **ZOE never got better or worse at answering. It buried the answers
under 4,567 other messages.** More than half of everything it has ever sent
(51.6%) is a request for a tap that lands 0.58% of the time.

## Reading the table

- **The grill card is the single largest thing ZOE does** - 30.9% of its
  entire life, all of it in one month, at a 0.03% reply rate. 22 sweep runs,
  largest 372 cards, queues up to 573 items, and in 2,415 cards the index had
  already overrun the total (cards reading "364/363"): the backlog grew
  faster than the sweep drained it and ZOE kept counting.
- **The types Zaal answers are the ones where ZOE has something of his in
  hand**: system errors (70%), work reports (21.85%), capture
  acknowledgements (21.43%), conversational answers (21.07%), failure
  reports (9.76%). Every one is ZOE responding to a thing Zaal started.
- **The types he never answers are the scheduled ones**: watchdog restarts,
  recurring status reports, build-candidate approvals, cost reports, bot
  activity logs, agent-bus relays, event promos, affirmation prose - **1,116
  messages at a combined 0.00%.** Not one reply, ever.
- **Research is the most expensive thing that nobody reads**: 998
  deliverables, 0.60% reply rate. **18.5% of them (185) contain no research
  at all** - they are quota or auth failures wearing a research header
  ("You've hit your weekly limit", "no output - check claude auth"). A
  further 10.2% are verbatim repeats of an earlier identical deliverable; the
  same five topic lines were re-sent 30 or more times each.
- **The nag migrated rather than stopped**: idle-session nags peaked at 956
  in July, then near-vanished in August (13) - replaced one-for-one by the
  grill card. Volume was never fixed, only relabelled.
- **ZOE noticed once.** In June it sent: *"I've sent 3 things you haven't
  replied to. I'll dial back - raising my bar so I only ping when it really
  matters."* Two such messages exist in 151 days. Traffic tripled afterwards.

## The classes that work, over the full window

The August-only view invites a wrong conclusion: that the fix is composition,
shift the mix back toward answers and the replies return. The full Mar-Aug
record says otherwise. **The classes that work did not merely shrink - their
reply rates collapsed too, while they were still being sent.**

| Class | Mar | Apr | May | Jun | Jul | Aug |
|---|--:|--:|--:|--:|--:|--:|
| conversational answer | **56.3%** (67/119) | 39.4% (104/264) | 22.7% (51/225) | 6.1% (16/262) | 7.5% (17/226) | **1.6%** (2/124) |
| work report | **70.4%** (19/27) | 25.0% (3/12) | 9.2% (7/76) | 25.0% (4/16) | 0% (0/18) | 0% (0/2) |
| failure report | 50.0% (5/10) | 52.2% (12/23) | - | 0% (0/3) | 1.0% (1/96) | 2.7% (2/73) |
| **ANSWER band** | **59.1%** (91/154) | 39.2% (112/286) | 17.8% (61/343) | 5.4% (25/461) | 6.5% (28/428) | **2.1%** (3/142) |

ZOE still sent 124 conversational answers in August. Two were answered. In
March the same class ran at 56.3%.

| Month | replies earned | messages sent |
|---|--:|--:|
| Mar | 100 | 168 |
| Apr | 135 | 690 |
| May | 73 | 897 |
| Jun | 39 | 890 |
| Jul | 47 | 2,273 |
| Aug | **11** | **4,709** |

**Replies earned fell from 100 to 11 while messages sent rose from 168 to
4,709 - a 28x rise in output bought a 9x fall in return.** Volume did not
just crowd out the good classes; it poisoned them. A v2 that only rebalances
the mix, without cutting absolute volume, is building the March message set
inside the August channel and should expect the August rate.

**On gates:** a parallel lane reports roughly 19 gates over five months at
about 47% answered. That does not appear in this record and this document
does not carry it. The nearest thing here is `Decision needed` - **194
messages, Jul-Aug only, 3.6% answered**. Orchestration gates live in the
orchestration DB, a surface Zaal cannot reach from his phone (that is
`ZOE-CENTER.md` section 3's own point). Their answer rate is evidence about
that surface, not about this one, and the two must not be averaged.

## What he asked for, in his own words

His demand vocabulary across all 505 non-empty messages is work and status,
not narrative: research (125), build (85), next (45), api (44), status (42),
agent/agents (82), check (33), error (29), test (28), docs (27), tasks (27),
plus tool names.

**On cadence** - 2026-04-05, the instruction that defines the failure:

> "1 but give me updates 6-12 hours on important things but 1 at a time so
> it's not a list"

Requested: 2-4 messages a day, one item at a time. Delivered over the 143
days that followed: **9,271 messages, 65 per day - 22x the ceiling he set**,
and delivered as lists.

**On channel** - twelve minutes earlier, same day:

> "Can we send these as emails or something instead so they don't break flow
> on a Convo"

Messages sent to Telegram after that request: **9,273.**

**On bursts** - 2026-04-03:

> "Why did all 3 send at same time"

Bursts recorded after that: 1,299.

**On assumptions** - 2026-04-02:

> "Your biggest weakness right now is making assumptions and fabricating
> APIs. The fix isn't to stop coding - it's to ASK MORE QUESTIONS before
> acting."

**On role** - 2026-04-02:

> "lets be an overall orchestrator of the codebase stop trying to make fixes
> but improve workflw"

**On autonomy and escalation** - 2026-07-15:

> "we need to be more autonomous and check in with me and risky things like
> we spent $25"

**On cost** - 2026-06-26:

> "research this why are you spending so much"

**On acknowledgement** - 2026-03-28, the very first instruction he ever gave
it:

> "From now on, always acknowledge messages immediately with 'Got it -
> working on [task]' before doing any work. Never leave me waiting with no
> response."

That one it kept. See "What to keep" below.

---

## Ranked: what ZOE v2 must do differently

Ranked by weight of evidence and by how much each would move the 392:1 ratio.

**1. A hard send budget, enforced in code, not in a prompt.**
392 messages per reply is the whole failure. v2 gets a daily message
allowance measured against the cadence he actually stated (2-4/day). When the
budget is spent, everything else queues or goes to a surface he pulls from.
A prompt instruction was given on 2026-04-05 and violated 22x for 143
straight days - so the ceiling must live in the sender, not the model. The
budget is spent on the answer band first: it is 18.8% of traffic and 79% of
all replies ZOE ever earned.

**2. Never enumerate a queue into the chat.**
2,977 cards, 0.37% answered, index overrunning the total 2,415 times. One
open ask at a time, and the next card does not send until the current one is
resolved or expires. If a queue has 573 items, that is a dashboard, and the
chat gets one line: how many, and the single most important one.

**3. Answer, do not report - and cut volume anyway, because answers stop
working too.**
Answering draws a reply **17.64%** of the time; asking for a tap draws
**0.58%** - a 30x gap. ZOE's answering share fell from **91.7% to 3.0%**
while its absolute answering volume held flat (154 messages in March, 142 in
August). It did not get worse at answering; it buried the answers. v2's
default is silence plus breakage, and the answer band is the only band that
grows. Status is pulled (he types "status" - one of his top terms), never
pushed. The 1,116 messages across watchdog restarts, recurring status
reports, build-candidate approvals, cost reports, bot activity logs,
agent-bus relays, event promos and affirmation prose drew **zero replies in
151 days** and should not exist in the chat at all. But rebalancing alone
will not work: the ANSWER band itself fell from **59.1% to 2.1%** answered
across the same window. At August volume Zaal ignores answers too, so the
budget in rank 1 is not optional trim around this fix - it is the
precondition for it.

**4. Every ask carries an owner, a deadline and an expiry.**
The ask band is **51.6% of everything ZOE has ever sent and lands 0.58% of
the time**; 65 of 66 resends died at "resend 3/3". An ask that goes unanswered past its deadline must take its default
action and say so in one line, not re-send. Resends taught him the messages
were ignorable.

**5. Route by urgency to a channel, not everything to the one channel.**
He asked for this on 2026-04-05 and was ignored 9,273 times. v2 has three
lanes: interrupt (breakage, money, risk - Telegram now), digest (one
scheduled roll-up), and pull (a surface he opens when he wants it). Default
is digest.

**6. Deduplicate and collapse before sending, and never ship a failure
wearing a success header.**
34.4% duplicate rate overall, one string 339 times, 138 identical failure
reports. Worst case is research: **18.5% of 998 deliverables contained no
research**, only a quota or auth error under a research headline, and a
further 10.2% were verbatim repeats. A blocked job must report as blocked,
once, in the interrupt lane - not as 185 fake deliverables.
Identical or near-identical messages collapse into one with a count. Repeat
alarms escalate in severity or go quiet - they never simply repeat.

**7. Respect the clock.**
2,059 messages between 22:00 and 07:00, from a bot that itself sent him a
nightly "hard stop on AI, start winding down" message. Only the interrupt
lane may fire at night, and only for breakage, money or risk.

**8. Escalate cost and risk; suppress routine.**
"why are you spending so much" and "check in with me and risky things like we
spent $25" are both explicit. Credits exhaustion and spend belong in the
interrupt lane at first occurrence and must then go quiet - 57 identical
FLEET BRAIN DOWN alarms trained him to scroll past the one class of message
he said he wanted.

**9. Never send a burst.**
1,299 bursts, max 31 messages in 60 seconds, and he complained about it in
April. A minimum inter-message interval, with anything that arrives inside
the window merged into the next send.

**10. Ask before assuming, and stay the orchestrator.**
His two role corrections - ask more questions before acting, and orchestrate
rather than patch - are the only content-level failures in the record. They
rank last here not because they are unimportant but because at 12 messages a
month he is no longer present for ZOE to be wrong in front of. Fix the volume
first; these become measurable again afterwards.

---

## What to keep

**Immediate acknowledgement works and is the one instruction ZOE never
broke.** 86 "Got it - working on this one, reply incoming" messages, median
**16 seconds** to the next message, and only **3%** were followed by more
filler instead of real work. This is the interaction pattern v2 should
generalise: fast, short, and followed by an actual answer.

---

## The constraint this sets on ZOE-CENTER

`ZOE-CENTER.md` argues for one front door, one ask type, one queue, one
renderer. This record adds the constraint that decides whether that front
door survives contact:

> **A unified ask queue that renders every gate, grill card, HOLD decision
> and draft into Telegram is the August failure with better plumbing.** The
> unification is right. It is only safe if it ships with a send budget, a
> one-open-ask-at-a-time rule, an expiry-with-default on every ask, and a
> digest lane that is the default destination.

v2 must send less and answer more. Everything else in the design is
downstream of that.

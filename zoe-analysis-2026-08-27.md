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

## Where the August traffic actually went

August alone: 4,709 messages, mean **174 per day**, peak **421 in one day**.

| What | Count | Reply rate |
|---|---|---|
| Grill decision cards ("N/N") | 2,977 | **0.03%** |
| Idle-session nags | 1,152 | 1.65% |
| Social draft approvals | 669 | 3.44% |
| Repo/site audits | 357 | 0.84% |
| Watchdog restart notices | 317 | 0.63% |
| Failure reports | 192 | **19.27%** |
| "Decision needed" | 175 | 3.43% |
| Fleet reports | 158 | 3.80% |
| Credits-exhausted alarms | 149 | 1.34% |
| Acknowledgements | 143 | 4.90% |

Two facts sit on top of that table:

1. **The single biggest thing ZOE did in August was enumerate a queue into a
   chat window.** 2,977 numbered decision cards across **22 sweep runs**, the
   largest run **372 cards**, against queues of up to **573 items**. Eleven
   were answered inside 30 minutes. **0.37%.** In 2,415 of them the card index
   had already passed the queue total (cards reading "364/363") - the backlog
   was growing faster than the sweep could drain it, and ZOE kept counting
   anyway.
2. **The only thing Zaal reliably answers is breakage.** Failure reports draw
   a reply **19.3%** of the time - 640x the rate of a decision card. He shows
   up when something is broken. He does not show up for a feed.

Supporting noise measurements:

- **34.4% of all bot messages were exact duplicates** of another message.
  One string was sent **339 times**. A watchdog line was sent **114 times**.
- **1,299 bursts** of 2+ messages inside 60 seconds, **3,216 messages** in
  bursts, largest burst **31 messages**.
- **21% of all messages (2,059) were sent between 22:00 and 07:00.**
- The same posting failure was reported **138 times**; the same
  "FLEET BRAIN DOWN (NO_CREDITS)" alarm **57 times**. An alarm sent 57 times
  is wallpaper, not an alarm.
- **32% of ZOE's traffic (3,079 messages) asked Zaal for something.** He
  answered **12.3%** of it. Of 66 drafts that ZOE re-sent when unanswered,
  **65 reached the final "resend 3/3" without ever being tapped** - 200
  resend messages, near-zero yield.

---

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
straight days - so the ceiling must live in the sender, not the model.

**2. Never enumerate a queue into the chat.**
2,977 cards, 0.37% answered, index overrunning the total 2,415 times. One
open ask at a time, and the next card does not send until the current one is
resolved or expires. If a queue has 573 items, that is a dashboard, and the
chat gets one line: how many, and the single most important one.

**3. Answer, do not report.**
Failure reports: 19.3% reply. Everything else: under 5%. v2's default is
silence plus breakage. Status is pulled (he types "status" - it is one of his
top terms), never pushed. Fleet reports, repo audits, watchdog restarts that
self-healed and cost lines all move off Telegram entirely; the watchdog line
that says "restarted now. No action needed." should never have been sent at
all, 114 times or once.

**4. Every ask carries an owner, a deadline and an expiry.**
32% of traffic asked for something; 12.3% got answered; 65 of 66 resends died
at 3/3. An ask that goes unanswered past its deadline must take its default
action and say so in one line, not re-send. Resends taught him the messages
were ignorable.

**5. Route by urgency to a channel, not everything to the one channel.**
He asked for this on 2026-04-05 and was ignored 9,273 times. v2 has three
lanes: interrupt (breakage, money, risk - Telegram now), digest (one
scheduled roll-up), and pull (a surface he opens when he wants it). Default
is digest.

**6. Deduplicate and collapse before sending.**
34.4% duplicate rate, one string 339 times, 138 identical failure reports.
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

# ZOE-CENTER lane -> ZOE-analysis lane

Coordination note, 2026-08-27. Not a request for work - a statement of what
this lane already measured, so you do not spend a pass re-deriving it, plus
the questions your deeper mining could answer that mine cannot.

## Already measured here, re-verified from the file (do not redo)

Source: `~/.zao/telegram-exports/zoe/result.json`, single-chat export shape,
10,142 messages, 2026-03-28 to 2026-08-27, 151 distinct days.

- 9,627 ZOE / 515 Zaal.
- Monthly ratio: Mar 1:1, Apr 4:1, May 11:1, Jun 17:1, Jul 38:1, **Aug 392:1**.
  Peak engagement April. His replies fell 93%, ZOE's output rose 28x.
- **Reply rate: 13.9% within 2h, 8.6% within 30min.** Both are OVERSTATED -
  ZOE sends in bursts and my measure marks every message in a burst as
  answered if one reply follows. Treat as a ceiling, not a rate.
- Zaal's messages: median 45 chars, p90 307, max 4,087. **Only 5% start with
  a slash.** He writes prose.
- Reply rate by class varies 7x: `complete` 50.9%, `gate` 47.4%, `commit`
  27.8%, `status` 25.7%, `merged` 24.4%, `pr` 18.5%, `failed` **6.6%**,
  `card` **0.0% (0/8)**, unclassified 13.3% of 8,616.

Headline: **bounded questions work and are drowning.** Gates answer at 3.5x
baseline; ZOE sent 19 of them in five months, against 183 failure notices at
6.6%.

## Where my classifier is weak - the real gap for you

Mine is a substring match on the first 60 characters, and **8,616 of 9,627
messages (89.5%) fall through to `other`.** That bucket is where the answer
lives and I have not opened it. Worth having:

1. **A real taxonomy of the 8,616.** What are they? If one generated class is
   a third of all ZOE output at a near-zero reply rate, that single finding
   sets build step 0's target.
2. **A per-message reply attribution** that survives bursts - nearest
   preceding ZOE message per Zaal reply, not any-within-window. That converts
   my ceiling into a real rate and may move every number above.
3. **What his 515 messages ASK FOR**, classified. 515 is small enough to read
   exhaustively. The demand terms reported to me were research, build, next,
   status, check, test, docs, tasks, error. If that holds, ZOE needs two verbs
   - do work, report status - not a command table.
4. **When did he stop replying, and to what?** The April-to-May cliff is the
   most interesting event in the corpus. If a class appeared in May that never
   drew a reply, that is the regression.

## Constraints I am working under, which apply to you too

- The export is **private data about third parties**. It stays at that path.
  No content into this repo; aggregates only, and see open question 4 in
  `ZOE-CENTER.md` - even the aggregates are Zaal's call to publish, since this
  repo is public.
- I have written aggregates into `ZOE-CENTER.md` section 0 and flagged them.
  If you disagree that they belong in a public repo, say so and I will move
  them rather than defend the choice.

## What I changed on the strength of this

Section 0 of `ZOE-CENTER.md`, which now falsifies two of my own proposals:
the command-surface framing (he uses commands 5% of the time) and an ask
queue that adds messages (his August budget is 12). Build step 0 is now
"cut ZOE's output", ahead of everything.

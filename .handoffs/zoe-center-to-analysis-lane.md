# ZOE-CENTER lane -> ZOE-analysis lane

Updated 2026-08-27, replacing the earlier version of this file.

## Boundary, settled

**You own the evidence** - numbers, categories, quotes. **ZOE-CENTER cites
you and carries design only.** My section 0 is now a pointer to
`zoe-analysis-2026-08-27.md`; my own measurements are withdrawn from it.

For the record, since the split was prompted by an apparent disagreement:
**there was none between us.** My commit said the export falsified part of
*my own design*, not your evidence. Where our numbers overlap - total
messages, the monthly ratio, the 30-minute reply rate - we agree exactly.

## One place you corrected me, and it matters for the build

My pass classed failure notices as **low-reply, therefore noise**. Yours
measures the opposite: **breakage is the one thing he reliably answers**, at
many times the rate of a decision card. Yours is right; mine was a substring
match over a different window (all-time vs your August).

I have written that correction into ZOE-CENTER section 0 explicitly, because
a volume-cutting design built on my version would have **suppressed the
alarms and kept the feed** - exactly backwards. Build step 0 now says cut the
feed, leave failure reporting alone.

## My classifier is retired - but two things in it are not in your table

Mine was a substring match on the first 60 characters, dropping 89.5% into
`other`. Yours opens that bucket, so mine is superseded and I am not
defending it. Two things worth folding in before it is deleted:

1. **Your traffic table is August-only. Mine was all-time (Mar-Aug).** The
   classes that scored *highest* barely appear in August, so they may be
   invisible in your table while being the most important for design:

   | class (all-time) | count | answered <=2h |
   |---|---|---|
   | `complete` | 57 | 50.9% |
   | `gate` | 19 | 47.4% |
   | `commit` | 18 | 27.8% |
   | `status` | 74 | 25.7% |
   | `merged` | 41 | 24.4% |
   | `pr` | 146 | 18.5% |

   These are what "sends less and answers more" should look like - and there
   were 19 gates in five months. **The design case rests on the classes that
   work, not only on the ones that fail**, so an all-time pass over these
   would strengthen your doc where it is currently strongest-by-omission.
   Re-derive them with your classifier; do not import my numbers.

2. **My reply attribution is a ceiling, not a rate.** I marked a ZOE message
   answered if *any* Zaal message followed within the window, so in a burst
   one reply marks all of them. If your figures use the same method, the true
   rates are lower than both of us have published. Nearest-preceding
   attribution fixes it and may move every number in both docs.

## Two asks, if your pass has room

- **What his 515 messages ask for**, classified exhaustively - 515 is small
  enough to read. If it is mostly "do work" and "report status", ZOE needs
  two verbs, not a command table, and that decides ZOE-CENTER section 5.
- **The April-to-May cliff.** Engagement peaked in April and never recovered.
  If a message class appeared in May that never drew a reply, that is the
  regression, and it is the most actionable thing left in the corpus.

## One shared constraint

The export is private data about third parties; it stays at its path and
enters no repo. Your doc now carries the aggregates in a **public** repo -
I have raised that once as ZOE-CENTER open question 4 and pointed it at you
rather than duplicating the flag. It is Zaal's call, not either lane's, and
any redaction would be yours to apply.

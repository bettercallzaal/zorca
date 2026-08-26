# grill JAMMED 381 - root cause

Investigated 2026-08-26. Nothing was rewritten and nothing was cleared.
Both state files archived first:

- VPS: `/home/zaal/.zao/zoe/archive/backlog-grill-state.2026-08-26-investigation.json`
- Mac: `~/.zao/archive/status.2026-08-26-investigation.json`

## The headline

**Batches never stopped firing.** The grill sent 190 cards today, 294
yesterday, 281 the day before. The gate held exactly twice in four days.
`JAMMED` is a false alarm.

Gate outcomes from the bot's own journal (`journalctl --user -u zoe-bot`):

| day | sent | held |
|---|---|---|
| Aug 23 | 153 | 0 |
| Aug 24 | 281 | 0 |
| Aug 25 | 294 | 2 |
| Aug 26 | 190 | 0 |

## The store

`/home/zaal/.zao/zoe/backlog-grill-state.json` on the VPS - `asked` 572,
`answered` 191, `activeTaskId`, `lastSentMs`, `pinnedOldestMessageId`.
It is read over SSH by `~/bin/zao-status-refresh`, cached to
`~/.zao/status.json`, and rendered by `~/bin/zao-statusline`.

`lastSentMs` was 112 seconds old at the time of measurement. The store is
live, not stalled.

## Root cause

`~/bin/zao-status-refresh` reproduces `outstandingCount()` inline rather
than calling it, and the copy drifted from the original **again**:

```python
out=len([i for i in a if i not in n and not a[i].get("requeuedAt")])
```

The real gate, `outstandingCount()` in
`bot/src/zoe/backlog-grill-runner.ts:114`, has a third clause the copy never
got - `now - sentAt < capWindowMs`, a 12-hour window added 2026-08-14:

```ts
if (s.answered[id] || s.asked[id].requeuedAt) return false;
const sentAt = Date.parse(s.asked[id].at);
if (!Number.isFinite(sentAt)) return true;
return now - sentAt < capWindowMs;   // <- missing from the statusline copy
```

So the two numbers are different quantities:

| quantity | value now |
|---|---|
| statusline: every card ever asked and never answered | **381** |
| gate: unanswered **within the last 12h** | **140** |
| deployed ceiling (`ZOE_GRILL_MAX_OUTSTANDING`, `~/zao-bot-live/bot/.env`) | 200 |

381 is compared against 200 and paints JAMMED. 140 is compared against 200
and sends. The bar has been reporting a jam that the gate is not having.

This is the exact failure the window was introduced to end. From the
runner's own comment:

> That last one is the 2026-08-09 jam. [...] A backpressure signal that
> cannot fall on its own is not backpressure, it is a latch - and
> `grill JAMMED 20/20` printed unchanged on every lane until nobody read it.

And from `zao-status-refresh` itself, three lines above the broken copy:

> If that clause changes there, change it here in the same commit.

It changed there. It was not changed here. Same latch, one layer up:
all-time-unanswered can only fall when Zaal answers, so it cannot fall on
its own, and it has been pinned for two days.

## One-line fix

`at` is ISO-8601 UTC, so a lexicographic compare is exact and needs no
parsing. In `~/bin/zao-status-refresh`, inside the SSH python block:

```python
cut=time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time()-12*3600))
out=len([i for i in a if i not in n and not a[i].get("requeuedAt") and (not a[i].get("at") or str(a[i]["at"])[:19] >= cut)])
```

The `not a[i].get("at")` half preserves the gate's deliberate safe error: an
undateable card counts, because holding a slot beats flooding him. There are
zero undateable cards today, but the copy should match the original or it
will drift a third time.

Applied against the live store this returns 140, and the bar reads
`grill 140/200 NEARING` - true, and able to fall.

**Superseded - and the string compare was wrong.** The fix landed as
`zaal-dotfiles a979b96` at 13:06, authored by Zaal, before this lane was
told to apply it. It parses the value instead of sorting it, and the commit
carries the reason my one-liner should not have shipped:

> A string compare looks exact - `at` really is ISO-8601 UTC - but it gets
> the safe-error path wrong in both directions: "not-a-date" sorts ABOVE the
> cutoff and counts by ASCII accident, while "0000-bad" sorts below it and is
> silently dropped. Same class of garbage, opposite answers, and one of them
> loses a card from the count.

The shipped version:

```python
def inwindow(v, now, w=12*3600):
    try:
        t=calendar.timegm(time.strptime(str(v)[:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return True
    return now-t < w
```

That is the gate's rule exactly - cannot date it, count it. `~/bin/zao-status-refresh`
is byte-identical to `a979b96:bin/zao-status-refresh`; nothing was applied by
this lane.

## Verified after the fix, 2026-08-26 20:55 UTC

```
cache before   grill 200  queued 380
zao-status-refresh  exit 0
cache after    grill 200  queued 380  err_vps 0
bar renders    grill JAMMED 200 open/380 queued quiet 2h
```

**The two numbers are now different quantities, which is the proof the window
clause is live** - before the fix `grill` and `grill_queued` both read 381.

The bar does not read `140/200 NEARING`, and it should not. 140 was the
windowed count at 15:39 UTC. Five more hours of sending took it to 200, and
on the VPS right now:

```
windowed outstanding 200      <- at the deployed ceiling
lifetime unanswered  380
lastSentMs           18:02 UTC     now 20:55 UTC   -> 2h53m of silence
```

So the grill **is** jammed now, genuinely, for the first time in this
investigation - and the bar is saying so truthfully instead of by accident.
The cause is the open item below: nothing has been answered since Aug 24, so
the windowed count climbed to the cap and the gate stopped.

## The thing that is actually wrong, and the bar is not saying it

`answered` per day, from the same store:

```
2026-08-19  23      2026-08-22   4
2026-08-20  13      2026-08-24   8
2026-08-21   1      2026-08-25   0
                    2026-08-26   0
```

Asks per day over the same window: 191 on the 25th, 190 on the 26th.

**Zero answers have been recorded for two days while ~190 cards a day go
out.** Whether Zaal stopped tapping or the verdict-write path broke on the
24th is the open question - the last `verdict-synced` line in the journal is
Aug 24 14:22, and there are no grill errors since. That is worth a look on
its own; the JAMMED label is not what has been telling you about it.

Suggested next probe: send one card, answer it from Telegram, and check
whether `answered` gains a key. That separates "not tapping" from "taps not
recording" in one round trip.

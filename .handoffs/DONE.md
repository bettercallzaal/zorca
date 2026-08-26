# DONE

Coordinator reads this. One line per shipped cycle, newest last.

- 2026-08-26 grill JAMMED 381 root cause - false alarm, metric drift in `~/bin/zao-status-refresh` (missing the 12h `capWindowMs` clause). Not applied, reported. Full writeup + one-line fix: `.handoffs/grill-jammed-381-rootcause.md`. State archived at `/home/zaal/.zao/zoe/archive/backlog-grill-state.2026-08-26-investigation.json` and `~/.zao/archive/status.2026-08-26-investigation.json`. Separate real issue surfaced: zero grill answers recorded since 2026-08-24 while ~190 cards/day are sent.

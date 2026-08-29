#!/usr/bin/env python3
"""Field-to-reader audit for gui/zorca-gui2.

Run against a live board:  python3 gui/field-audit.py [url]

Forward direction, and it is SOUND: a key the server puts in the payload
whose name appears nowhere in the page as `.key` is definitely unread. It
over-approximates readership, so anything it flags is real.

Reverse direction is deliberately NOT attempted here by name matching -
`e`, `d`, `g` and `r` are each bound to four different things in the page
and any such check is noise. Do it with the Proxy recipe in the docstring
below, which is sound because it observes actual property access.

    // in the page's console, before load():
    window.__undef = [];
    // wrap fetch("/api/state") so the parsed body is a deep Proxy that
    // records every miss, then call load() and read window.__undef.
    // Misses on s.acks[<key>] are expected - an unacked item is a miss.

Exit code 1 if anything is definitely unread, so it can gate a commit.
"""
import json
import re
import sys
import urllib.request

# detail=1 on purpose: the lean payload omits tasks and resolved, and a
# field that is never served is also never audited.
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:7778/api/state?detail=1"
SRC = "gui/zorca-gui2"

page = open(SRC).read().split('PAGE = r"""', 1)[1].rsplit('"""', 1)[0]
live = json.load(urllib.request.urlopen(URL))

# Fields the server keeps for its own use and never means to send to the
# page. Listed rather than silently tolerated, so adding one is a decision.
SERVER_ONLY = {
    ("stuck[]", "cwd"), ("gitlog[]", "cwd"), ("panes[]", "cwd"),
    ("estate.ahead[]", "cwd"), ("orphans[]", "when"), ("lanes[]", "cmd"),
    ("panes[]", "title"),
    # served only when the fold asks for them; the strip reads the counts
    ("payload", "resolved_count"),
}

def audit(label, keys):
    out = []
    for k in sorted(keys):
        if (label, k) in SERVER_ONLY:
            continue
        if not re.search(r"\.%s\b" % re.escape(k), page):
            out.append(k)
    mark = "unread: %s" % out if out else "ok"
    print("  %-18s %2d keys  %s" % (label, len(keys), mark))
    return out

print("field audit against", URL)
bad = []
bad += audit("payload", set(live))
for name in ("estate", "drafts_age", "grill"):
    bad += audit(name, set(live.get(name) or {}))
for name in ("stuck", "orphans", "daily", "gitlog", "panes", "tasks", "lanes"):
    rows = live.get(name) or []
    if rows:
        bad += audit(name + "[]", set(rows[0]))
ahead = ((live.get("estate") or {}).get("ahead") or [])
if ahead:
    bad += audit("estate.ahead[]", set(ahead[0]))

raw = urllib.request.urlopen(URL).read()
lean = urllib.request.urlopen(URL.split("?")[0]).read()
print("\n  polled payload %.1f KB every 15s; with detail=1 %.1f KB, fetched "
      "only when the reference fold opens" % (len(lean) / 1024, len(raw) / 1024))
print("\n%s" % ("FAIL - fields above are served and never read" if bad else "PASS"))
sys.exit(1 if bad else 0)

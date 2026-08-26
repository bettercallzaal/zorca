#!/usr/bin/env python3
"""WCAG 2.2 relative luminance / contrast over the shipped :root block."""
import re, sys
src = open(sys.argv[1] if len(sys.argv) > 1 else "gui/zorca-gui2").read()
block = src.split(":root {", 1)[1].split("}", 1)[0]
tok = dict(re.findall(r"--([a-z-]+)\s*:\s*(#[0-9a-fA-F]{6})", block))

def lum(h):
    c = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

navy, panel = tok["navy"], tok["panel"]
TEXT = ["text", "dim", "gold", "ok", "warn", "info"]
NONTEXT = ["line-interactive", "panel"]
print("%-18s %-9s %8s %8s  %s" % ("token", "hex", "on navy", "on panel", "verdict"))
fail = 0
for name in TEXT + NONTEXT:
    hexv = tok[name]
    on_navy = ratio(hexv, navy)
    on_panel = ratio(hexv, panel) if name != "panel" else float("nan")
    need = 4.5 if name in TEXT else 3.0
    if name == "panel":
        ok = on_navy >= 1.2   # surface separation, not a WCAG threshold
        verdict = "surface %.2f:1 vs navy (>=1.20)" % on_navy
    else:
        ok = on_navy >= need and on_panel >= need
        verdict = ("pass" if ok else "FAIL") + " (needs %.1f)" % need
    if not ok:
        fail += 1
    print("%-18s %-9s %8.2f %8s  %s" % (
        "--" + name, hexv, on_navy,
        "-" if name == "panel" else "%.2f" % on_panel, verdict))
print("\ntoast .bad: --navy on --warn = %.2f:1" % ratio(navy, tok["warn"]))
print("panel-raised on panel      = %.2f:1" % ratio(tok["panel-raised"], panel))
print("\n%d failing" % fail)
sys.exit(1 if fail else 0)

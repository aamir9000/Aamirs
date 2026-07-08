#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scoped L+M verification for one concept in a Master-Depth-style file.
Usage: python3 _tools/verify_lm.py "<path>" <N>
Extracts region "## CONCEPT N" .. "## CONCEPT N+1" and reports residue + structure.
"""
import re, sys

path = sys.argv[1]
n = int(sys.argv[2])
text = open(path, encoding="utf-8").read()
m = re.search(rf"#+ CONCEPT 0*{n}\b.*", text)
start = m.start()
nxt = re.search(rf"#+ CONCEPT 0*{n+1}\b", text[start+5:])
end = (start+5+nxt.start()) if nxt else len(text)
region = text[start:end]

residue = [
    "locked START", "locked END", "interpolate strictly", "Camera distance",
    "Transform-anchor distance", "suspended build", "macro build beat",
    "radiant reveal", "transform resolved", "cause building to effect",
    "clearly imminent", "mid-sweep", "mid-wrap", "mid-bloom", "mid-burst",
    "mid-flip", "mid-draw", "mid-roll", "mid-ripple", "mid-wave",
    "signature impossible beat",
]
fails = []
for p in residue:
    c = region.count(p)
    if c:
        fails.append(f"  RESIDUE {c}x: {p}")

beat1 = len(re.findall(r"^- \[00:00\u201300:02\] (?:Cut to|Match-cut)", region, re.M))
sb = region.count("SHOT BREAKDOWN (timed")
vp = region.count("\u2014 VIDEO PROMPT")
ip = region.count("\u2014 IMAGE PROMPT")
orient = region.count("ORIENTATION LOCK")
idlock = region.count("IDENTITY (locked):")
dur_bad = len([l for l in region.splitlines() if l.startswith("DURATION:") and "6 seconds" not in l])
fr_bad = len([l for l in region.splitlines() if l.startswith("FRAME RATE") and "no slow-motion" not in l])
# non-negated slow-mo outside NEGATIVE lines and headers
slow = 0
for l in region.splitlines():
    ll = l.lower()
    if ("slow-mo" in ll or "slow motion" in ll):
        if l.startswith("NEGATIVE") or "no slow-motion" in ll or "never slow-motion" in ll:
            continue
        slow += 1
        fails.append(f"  SLOWMO: {l[:90]}")

print(f"CONCEPT {n}: beat1(Cut/Match)={beat1} SB={sb} VP={vp} IP={ip} orient={orient} idlock={idlock} dur_bad={dur_bad} fr_bad={fr_bad} slow={slow}")
if sb != vp or beat1 != sb:
    fails.append(f"  STRUCT mismatch: SB={sb} VP={vp} beat1={beat1}")
if fails:
    print("FAIL:")
    print("\n".join(fails))
else:
    print("PASS")

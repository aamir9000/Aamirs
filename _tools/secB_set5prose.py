#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aira_set5 prose-format section-B: each VIDEO block is one rich prose paragraph
(after the IDENTITY LOCK) that already embeds a timed micro-expression timeline
("at 0.0-2.0s ..., at 2.0-4.0s ..., at 4.0-6.0s ...") plus the opening framing,
camera move and opening action. We SYNTHESISE a bracketed 3-beat `SHOT BREAKDOWN`
from those cues and INSERT it right after the IDENTITY LOCK (before the prose),
KEEPING the full prose paragraph intact as the detailed motion/physics/lighting/
audio direction (additive — zero content loss). Idempotent.
Usage: python3 _tools/secB_set5prose.py "<path>"
"""
import re, sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
if "SHOT BREAKDOWN (timed" in text:
    print("already has SHOT BREAKDOWN (skipped)"); sys.exit(0)

BRK = ("SHOT BREAKDOWN (timed, 6s \u00b7 real-time, continuous natural-speed motion \u2014 never "
       "slow-motion, never a static hold; expression eye-led and identity-safe):")

markers = [m.start() for m in re.finditer(r"^VIDEO PROMPT \(VEO", text, re.M)]
spans = []
for i, a in enumerate(markers):
    nb = re.search(r"^(---- FRAME |VIDEO PROMPT \(VEO|=====)", text[a+10:], re.M)
    spans.append((a, a + 10 + nb.start() if nb else len(text)))

def first_clause(s, n=18):
    s = s.strip().rstrip(".;,")
    w = s.split()
    return " ".join(w[:n]) + ("\u2026" if len(w) > n else "")

out = text
nconv = 0
for a, end in reversed(spans):
    blk = out[a:end]
    if "SHOT BREAKDOWN (timed" in blk:
        continue
    # locate IDENTITY LOCK line to insert after
    idm = re.search(r"^IDENTITY & CHARACTER-CONSISTENCY LOCK:[^\n]*$", blk, re.M)
    if not idm:
        continue
    # micro-expression timeline (the 3 timed cues)
    mexp = re.search(r"0\.0\s*\u2013\s*2\.0s\s*(.+?)[,;]\s*(?:at\s*)?2\.0\s*\u2013\s*4\.0s\s*(.+?)[,;]\s*(?:at\s*)?4\.0\s*\u2013\s*6\.0s\s*(.+?)(?:\.|;|\bLayer\b)", blk, re.S)
    e1 = e2 = e3 = None
    if mexp:
        e1, e2, e3 = (re.sub(r"\s+", " ", g).strip() for g in mexp.groups())
    # framing + camera + opening action
    fr = re.search(r"Open on (?:the |a |an )?(.+?)(?: framing| shot|,| and )", blk)
    framing = re.sub(r"\s+", " ", fr.group(1)).strip() if fr else "the establishing framing"
    cam = re.search(r"let (?:a |an )?(.+?)(?: drift| ease| push| pull| track| move| glide| from| toward| around)", blk)
    camera = re.sub(r"\s+", " ", cam.group(1)).strip() if cam else "a slow controlled move"
    act = re.search(r"begins mid-action[:,]\s*(.+?)(?:\.|;)", blk, re.S)
    action = first_clause(re.sub(r"\s+", " ", act.group(1))) if act else "she is already in motion"
    if e1 and e2 and e3:
        beats = (f"- [00:00\u201300:02] {framing}: {camera} is already underway as {action}; {first_clause(e1,16)}.\n"
                 f"- [00:02\u201300:04] {first_clause(e2,16)}, the motion carrying through with real weight and follow-through.\n"
                 f"- [00:04\u201300:06] {first_clause(e3,16)}, settling as the look holds.")
    else:
        beats = (f"- [00:00\u201300:02] {framing}: {camera} is already underway as {action}.\n"
                 f"- [00:02\u201300:04] the motion carries through with real weight, hair and fabric lagging a beat.\n"
                 f"- [00:04\u201300:06] she settles into the held look, eyes easing to a calm focus.")
    insert = "\n" + BRK + "\n" + beats + "\n"
    pos = a + idm.end()
    out = out[:pos] + insert + out[pos:]
    nconv += 1

open(path, "w", encoding="utf-8").write(out)
sb = out.count("SHOT BREAKDOWN (timed"); vp = out.count("VIDEO PROMPT (VEO")
gen = [l for l in out.splitlines() if ("slow-mo" in l.lower() or "slow motion" in l.lower())
       and "no slow" not in l.lower() and "never slow" not in l.lower() and "STD-NEG" not in l]
print(f"converted {nconv}; SHOT BREAKDOWN={sb} VIDEO={vp} genuine-slow-mo={len(gen)}")

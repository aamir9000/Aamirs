#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Format-B section-B engine for the Travel-Scenic plain-text files aira_set4.txt /
aira_set5.txt. These are already 6s, fixed-skeleton identity-locked, with timed
3-phase action and SUBJECT FRAMING + ORIENTATION LOCK present (K.3 travel/scenic
realism already baked in). The only PASS-1 delta is structural: convert the
`CHOREOGRAPHY & SUBJECT ACTION (timed, fluid): 0.0-2.0s ...; 2.0-4.0s ...; 4.0-6.0s ...`
line into a bracketed 3-beat `SHOT BREAKDOWN` (folding SHOT TYPE/ANGLE + CAMERA
MOVEMENT into beat 1), drop the now-duplicated standalone `CAMERA MOVEMENT:` line,
and normalise the combined `DURATION: 6.0s. FPS + MOTION BLUR: ...` line to the
standard DURATION + FRAME RATE strings. All other rich sections preserved.

Processes the WHOLE file (all video blocks). Idempotent.
Usage: python3 _tools/secB_fb.py "<path>"
"""
import re, sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
if "SHOT BREAKDOWN (timed" in text and "CHOREOGRAPHY & SUBJECT ACTION (timed" not in text:
    print("already converted (skipped)"); sys.exit(0)

BRK_HDR = ("SHOT BREAKDOWN (timed, 6s \u00b7 real-time, continuous energetic motion \u2014 never "
           "slow-motion, never a static hold; expression eye-led and identity-safe):")
DUR_STD = ("DURATION: 6 seconds (the clip plays the full 6s at real-time natural speed). "
           "FRAME RATE + MOTION BLUR: 24fps, real-time playback at natural speed (no slow-motion), "
           "180\u00b0 shutter, natural motion blur.")

# split into video blocks by the VEO video header; process each up to the next frame/concept marker
markers = [mm.start() for mm in re.finditer(r"^VIDEO PROMPT \(VEO", text, re.M)]
bounds = []
for i, a in enumerate(markers):
    nb = re.search(r"^(--- FRAME |=====|CONCEPT |## |MASTER AUDIO)", text[a+10:], re.M)
    end = a + 10 + nb.start() if nb else len(text)
    bounds.append((a, end))

def group3(ph):
    if len(ph) >= 3:
        n = len(ph); a = n // 3; b = 2 * n // 3
        return ("; ".join(ph[:max(a,1)]), "; ".join(ph[max(a,1):max(b,a+1)]) or "the motion carries through",
                "; ".join(ph[max(b,a+1):]) or "she settles and holds")
    if len(ph) == 2: return (ph[0], ph[1], "she settles the beat and holds, eyes alive")
    if len(ph) == 1: return (ph[0], "the motion carries through with real momentum", "she settles and holds")
    return ("she holds, alive and breathing", "a slow micro-shift keeps it alive", "she settles, eyes direct")

out = text
# process from last block to first so indices stay valid
nconv = 0
for a, end in reversed(bounds):
    blk = out[a:end]
    shotm = re.search(r"^SHOT TYPE / ANGLE:\s*(.+)$", blk, re.M)
    camm = re.search(r"^CAMERA MOVEMENT:\s*(.+)$", blk, re.M)
    chm = re.search(r"^CHOREOGRAPHY & SUBJECT ACTION[^\n:]*:\s*(.+)$", blk, re.M)
    if not chm:
        continue
    shot = shotm.group(1).strip().rstrip(".") if shotm else "the shot"
    cam = re.split(r"[,;\u2014]", camm.group(1).strip())[0].strip() if camm else None
    ph = []
    for p in re.split(r";\s*", chm.group(1).strip()):
        p = re.sub(r"^\s*[\d.]+\s*\u2013\s*[\d.]+s\s*", "", p).strip()
        if p: ph.append(p.rstrip("."))
    b1, b2, b3 = group3(ph)
    camlead = f"{cam} is already underway" if cam else "the move is already underway"
    beats = (f"- [00:00\u201300:02] {shot}: {camlead} \u2014 {b1}.\n"
             f"- [00:02\u201300:04] {b2}.\n"
             f"- [00:04\u201300:06] {b3}.")
    blk = re.sub(r"^CHOREOGRAPHY & SUBJECT ACTION[^\n:]*:[^\n]*$", lambda _: BRK_HDR + "\n" + beats, blk, count=1, flags=re.M)
    blk = re.sub(r"^CAMERA MOVEMENT:[^\n]*\n", "", blk, count=1, flags=re.M)
    blk = re.sub(r"^DURATION:[^\n]*$", lambda _: DUR_STD, blk, count=1, flags=re.M)
    out = out[:a] + blk + out[end:]
    nconv += 1

open(path, "w", encoding="utf-8").write(out)
sb = out.count("SHOT BREAKDOWN (timed"); vp = out.count("VIDEO PROMPT (VEO")
left = out.count("CHOREOGRAPHY & SUBJECT ACTION (timed")
cam_left = len(re.findall(r"^CAMERA MOVEMENT:", out, re.M))
gen = [l for l in out.splitlines() if ("slow-mo" in l.lower() or "slow motion" in l.lower())
       and "no slow-motion" not in l.lower() and "never slow-motion" not in l.lower()
       and not l.startswith(("NEGATIVE", "FRAME RATE"))]
print(f"converted {nconv} blocks; SHOT BREAKDOWN={sb} VIDEO={vp} leftover-choreo={left} standalone-CAM={cam_left} genuine-slow-mo={len(gen)}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic section-B + section-K engine for NON-TRANSFORMATION concepts (no couture
A->B wardrobe swap; wardrobe is continuity-locked). Used for the surreal/world,
product and action-single files that still use the OLD `SUBJECT ACTION WITH TIMING`
+ standalone `CAMERA MOVEMENT` format.

Per concept:
  * VIDEO (every present frame): drop the standalone `CAMERA MOVEMENT:` line,
    convert `SUBJECT ACTION WITH TIMING:` -> a timed 3-beat `SHOT BREAKDOWN`
    (synthesised from the action phases + the camera move folded into beat 1,
    re-timed to 0-2 / 2-4 / 4-6), reset `DURATION:` and `FRAME RATE + MOTION BLUR:`
    to the 6s standard. All other sections (PHYSICS / LIGHTING / AUDIO / NEGATIVE /
    identity lock / image fields) are preserved.
  * IMAGE: neutralise old multi-frame keyframe residue in any inline
    `TRANSFORM KEYFRAME NOTE` (locked START/END keyframe / locked hold / interpolate
    strictly -> continuity-locked phrasing) so the magical beat reads as one
    grounded, believable, match-cut beat (section-K), wardrobe untouched.
  * brief: append a section-K believability + match-cut continuity note.
Idempotent. Usage: python3 _tools/secB_lm.py "<path>" <concept_number> [conceptHeaderRegex]
The optional 3rd arg overrides the concept-header pattern (default '# CONCEPT N').
"""
import re, sys
path = sys.argv[1]; N = int(sys.argv[2])
hdr_pat = sys.argv[3] if len(sys.argv) > 3 else rf"# CONCEPT {N}\b"
text = open(path, encoding="utf-8").read()
m = re.search(rf"^#+ ?{hdr_pat}.*$", text, re.M) or re.search(rf"^.*CONCEPT {N}\b.*$", text, re.M)
if not m:
    sys.exit(f"concept {N} not found")
# region = from this header to the next top-level concept header
after = text[m.end():]
nm = re.search(rf"^#+ ?CONCEPT {N+1}\b", after, re.M) or re.search(rf"^# CONCEPT \d", after, re.M)
r0 = m.start(); r1 = m.end() + nm.start() if nm else len(text)
region = text[r0:r1]
if "SHOT BREAKDOWN (timed" in region and "SUBJECT ACTION WITH TIMING" not in region:
    print(f"CONCEPT {N}: already section-B (skipped)"); sys.exit(0)

BRK_HDR = ("SHOT BREAKDOWN (timed, 6s \u00b7 real-time, continuous energetic motion \u2014 never "
           "slow-motion, never a static hold; expression eye-led and identity-safe):")
FR_STD = ("FRAME RATE + MOTION BLUR: 24fps, real-time playback at natural speed (no slow-motion), "
          "180\u00b0 shutter, natural motion blur.")
DUR_STD = "DURATION: 6 seconds (the clip plays the full 6s at real-time natural speed)."

fm = re.search(r"## Frame 1 of (\d+) \u2014 IMAGE PROMPT", region)
if not fm:
    sys.exit(f"concept {N}: no standard frame headers")
F = int(fm.group(1))
present = [k for k in range(1, F + 1) if f"## Frame {k} of {F} \u2014 IMAGE PROMPT" in region]

def vid_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT")
    later = [kk for kk in present if kk > k]
    if later:
        b = region.index(f"## Frame {later[0]} of {F} \u2014 IMAGE PROMPT", a)
    else:
        nb = re.search(r"\n### |\n#+ ?CONCEPT ", region[a:]); b = a + nb.start() if nb else len(region)
    return a, b

def shot_of(va, vb):
    sm = re.search(r"^SHOT TYPE:\s*(.+)$", region[va:vb], re.M)
    return sm.group(1).strip().rstrip(".") if sm else "the shot"
def cam_of(va, vb):
    cm = re.search(r"^CAMERA MOVEMENT:\s*(.+)$", region[va:vb], re.M)
    if not cm: return None
    return re.split(r"[,;\u2014]", cm.group(1).strip())[0].strip()
def phases_of(va, vb):
    am = re.search(r"^SUBJECT ACTION WITH TIMING[^\n:]*:\s*(.+)$", region[va:vb], re.M)
    if not am: return []
    out = []
    for p in re.split(r";\s*", am.group(1).strip()):
        # strip leading timing prefix: "0:00.0–0:00.8 — ", "0.0–3.0s — ", or "0.0–1.8s " (no dash)
        p = re.sub(r"^\s*\d+:\d+(?:\.\d+)?\s*\u2013\s*\d+:\d+(?:\.\d+)?\s*(?:\u2014\s*)?", "", p)
        p = re.sub(r"^\s*[\d.]+\s*\u2013\s*[\d.]+s\s*(?:\u2014\s*)?", "", p).strip()
        p = re.sub(r"\s*(?:One clean subject action[^.]*|Clean cause[^.]*|real physics throughout|real physics except[^.]*)\.?\s*$", "", p).strip()
        if p: out.append(p.rstrip("."))
    return out

def group3(ph):
    if not ph:
        return ("she holds the beat, alive and breathing", "a slow micro-shift keeps it alive", "she settles, eyes direct to lens")
    if len(ph) == 1:
        return (ph[0], "the motion carries through with real momentum and follow-through", "she settles and holds, eyes direct")
    if len(ph) == 2:
        return (ph[0], ph[1], "she settles the beat and holds, eyes alive and direct to lens")
    # 3+ phases -> three roughly-equal groups
    n = len(ph); a = n // 3; b = 2 * n // 3
    g1 = "; ".join(ph[:max(a,1)]); g2 = "; ".join(ph[max(a,1):max(b,a+1)]); g3 = "; ".join(ph[max(b,a+1):])
    return (g1, g2 or "the motion carries through", g3 or "she settles and holds, eyes direct")

for k in present:
    va, vb = vid_span(k); vblk = region[va:vb]
    shot = shot_of(va, vb); cam = cam_of(va, vb); ph = phases_of(va, vb)
    camlead = (f"{cam} is already underway" if cam else "the move is already underway")
    b1, b2, b3 = group3(ph)
    beats = (f"- [00:00\u201300:02] {shot}: {camlead} \u2014 {b1}.\n"
             f"- [00:02\u201300:04] {b2}.\n"
             f"- [00:04\u201300:06] {b3}.")
    vblk = re.sub(r"^CAMERA MOVEMENT:[^\n]*\n\n?", "", vblk, count=1, flags=re.M)
    vblk = re.sub(r"^SUBJECT ACTION WITH TIMING[^\n:]*:[^\n]*$", lambda _: BRK_HDR + "\n" + beats, vblk, count=1, flags=re.M)
    vblk = re.sub(r"^DURATION:[^\n]*$", lambda _: DUR_STD, vblk, count=1, flags=re.M)
    vblk = re.sub(r"^FRAME RATE \+ MOTION BLUR:[^\n]*$", lambda _: FR_STD, vblk, count=1, flags=re.M)
    region = region[:va] + vblk + region[vb:]

# neutralise old keyframe residue in image notes (wardrobe continuity-locked, magical beat grounded)
region = region.replace("locked START keyframe", "continuity-locked START")
region = region.replace("locked END keyframe", "continuity-locked resolution")
region = region.replace("locked hold", "continuity-locked hold")
region = region.replace("interpolate strictly", "carry continuity smoothly")

# brief: append section-K believability + continuity note (Movement line, else Wardrobe line)
if "grounded in real physics" not in region:
    add = (" Believability/realism layer (section K): every element is real and clearly described; the one "
           "magical beat is surreal yet grounded in real physics and premium execution \u2014 no cheap sparkles, "
           "no floaty/plasticky CGI; scale and 3D placement stay believable; her single self, face and wardrobe "
           "stay continuity-locked; frame joins are hard match-cuts to new angles.")
    if re.search(r"^Movement:\s*.+$", region, re.M):
        mv = re.search(r"^Movement:\s*(.+)$", region, re.M); base = mv.group(1).rstrip()
        base += "" if base.endswith(('.', '!')) else "."
        region = re.sub(r"^Movement:\s*.+$", lambda _: "Movement: " + base + add, region, count=1, flags=re.M)
    elif re.search(r"^Wardrobe:\s*.+$", region, re.M):
        wv = re.search(r"^Wardrobe:\s*(.+)$", region, re.M); base = wv.group(1).rstrip()
        base += "" if base.endswith(('.', '!')) else "."
        region = re.sub(r"^Wardrobe:\s*.+$", lambda _: "Wardrobe: " + base + add, region, count=1, flags=re.M)

text = text[:r0] + region + text[r1:]
open(path, "w", encoding="utf-8").write(text)
sb = region.count("SHOT BREAKDOWN (timed"); vp = region.count("\u2014 VIDEO PROMPT")
sa = region.count("SUBJECT ACTION WITH TIMING"); cm = len(re.findall(r"^CAMERA MOVEMENT:", region, re.M))
res = [p for p in ("locked START keyframe", "locked END keyframe", "interpolate strictly") if p in region]
dur_bad = len([l for l in region.splitlines() if l.startswith("DURATION:") and "6 seconds" not in l])
print(f"CONCEPT {N}: F={F} present={len(present)} SB={sb} VP={vp} leftover-SA={sa} standalone-CAM={cm} dur_bad={dur_bad} residue={res or 'none'}")

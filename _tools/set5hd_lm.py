#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Concepts 91-95 "FULL Heavy-Detail" engine — OLD-format three-look liquid-material
couture reels (SILENT). Each is 6 frames: F1 HOOK/LOOK A, F2 CHANGE 1 (A->B),
F3 LOOK B, F4 CHANGE 2 (B->C, MAGIC), F5 LOOK C, F6 PERFECT-LOOP CLOSE (C->A re-pour).

Does THREE things at once:
  1. section-B video conversion on EVERY frame: delete the standalone
     `CAMERA MOVEMENT:` line, convert `SUBJECT ACTION WITH TIMING:` -> a timed
     3-beat `SHOT BREAKDOWN (timed, 6s ...)` (folding the camera move into beat 1
     and re-timing to 0-2 / 2-4 / 4-6), reset `DURATION:` and `FRAME RATE + MOTION
     BLUR:` to the 6s standard strings. PHYSICS & REALISM / LIGHTING / AUDIO /
     NEGATIVE / identity lock kept intact (K.1 believability already lives in PHYSICS).
  2. L+M chained on the transform frames (F2, F4, F6): flip the (MID-CHANGE/MID-MAGIC)
     image to the clean OPENING look (reuse the prior LOOK frame's wardrobe + stable
     look fields), rewrite the CHANGE KEYFRAME NOTE to the contained-MID-CLIP /
     HELD-angle / Veo-first-last / match-cut model, beats = hold-open / change-begins /
     resolve-to-next-look.
  3. brief Movement + Identity-safety -> L+M.
Idempotent. Usage: python3 _tools/set5hd_lm.py "<path>" <concept_number>
"""
import re, sys
path = sys.argv[1]; N = int(sys.argv[2])
text = open(path, encoding="utf-8").read()
m = re.search(rf"^# CONCEPT {N} \u2014.*$", text, re.M)
nxt = re.search(rf"^# CONCEPT {N+1} \u2014", text[m.end():], re.M)
r0 = m.start(); r1 = m.end() + nxt.start() if nxt else len(text)
region = text[r0:r1]
if "contained MID-CLIP" in region:
    print(f"CONCEPT {N}: already L+M (skipped)"); sys.exit(0)

F = int(re.search(r"## Frame 1 of (\d+) \u2014 IMAGE PROMPT", region).group(1))
present = [k for k in range(1, F + 1) if f"## Frame {k} of {F} \u2014 IMAGE PROMPT" in region]
BRK_HDR = ("SHOT BREAKDOWN (timed, 6s \u00b7 real-time, continuous energetic motion \u2014 never "
           "slow-motion, never a static hold; expression eye-led and identity-safe):")
FR_STD = ("FRAME RATE + MOTION BLUR: 24fps, real-time playback at natural speed (no slow-motion), "
          "180\u00b0 shutter, natural motion blur.")
DUR_STD = "DURATION: 6 seconds (the clip plays the full 6s at real-time natural speed)."

def img_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT")
    b = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT", a)
    return a, b
def vid_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT")
    later = [kk for kk in present if kk > k]
    if later:
        b = region.index(f"## Frame {later[0]} of {F} \u2014 IMAGE PROMPT", a)
    else:
        nb = re.search(r"\n### |\n# CONCEPT ", region[a:]); b = a + nb.start() if nb else len(region)
    return a, b
def header(k):
    i = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT"); return region[i:region.index(chr(10), i)]
def ward_line(k):
    a, b = img_span(k); mm = re.search(r"^WARDROBE[^\n]*$", region[a:b], re.M); return mm.group(0) if mm else ""
def look_name(k):
    mm = re.search(r"WARDROBE \(LOOK . \u2014 ([^)]+)\)", ward_line(k)); return mm.group(1).strip() if mm else None
def stable_fields(k):
    a, b = img_span(k); out = {}
    for line in region[a:b].splitlines():
        for lab in ("FOOTWEAR", "ACCESSORIES", "HAIR", "MAKEUP", "EYE COLOUR", "KINETIC STILLNESS",
                    "SPATIAL LOGIC", "LIGHTING", "TEXTURE & MICRO-DETAIL", "COLOR GRADE"):
            if line.startswith(lab): out.setdefault(lab, line); break
    return out
def shot_of(k):
    va, vb = vid_span(k); sm = re.search(r"^SHOT TYPE:\s*(.+)$", region[va:vb], re.M)
    return sm.group(1).strip().rstrip(".") if sm else "the hero"
def cam_of(k):
    va, vb = vid_span(k); cm = re.search(r"^CAMERA MOVEMENT:\s*(.+)$", region[va:vb], re.M)
    if not cm: return None
    c = cm.group(1).strip(); c = re.split(r"[,;\u2014]", c)[0].strip(); return c
def action_phases(k):
    va, vb = vid_span(k); am = re.search(r"^SUBJECT ACTION WITH TIMING:\s*(.+)$", region[va:vb], re.M)
    if not am: return []
    txt = am.group(1).strip()
    parts = re.split(r";\s*", txt)
    cleaned = []
    for p in parts:
        p = re.sub(r"^\s*\d+\.\d+\s*\u2013\s*\d+\.\d+s\s*\u2014\s*", "", p).strip()
        # strip trailing meta-commentary clauses that aren't action
        p = re.sub(r"\s*(?:One clean subject action[^.]*|Clean cause\u2192effect[^.]*|Clean cause.effect[^.]*|real physics throughout|real physics except the permitted[^.]*)\.?\s*$", "", p).strip()
        if p: cleaned.append(p.rstrip("."))
    return cleaned

# transform frames: header has "CHANGE n" or "RE-POUR"/"RE-WASH" (loop close)
tfs = []
loopf = None
for k in present:
    h = header(k)
    if re.search(r"\(CHANGE \d", h): tfs.append(k)
    if "PERFECT-LOOP CLOSE" in h: loopf = k
if loopf and loopf not in tfs:
    tfs.append(loopf)

def donor_next(KT):
    earlier = [k for k in present if k < KT]
    donor = earlier[-1] if earlier else None
    if KT == loopf:
        nxtf = 1 if 1 in present else None
    else:
        later = [k for k in present if k > KT]
        nxtf = later[0] if later else None
    return donor, nxtf

def next_name(KT, nxtf):
    if nxtf:
        nm = look_name(nxtf)
        if nm: return nm
    hm = re.search(r"\u2192 LOOK \w(?: ([A-Z][A-Za-z0-9 \-]+?))?\)", header(KT))
    if hm and hm.group(1): return hm.group(1).strip().title()
    return "the next look"

# ---- process every frame's VIDEO (section-B) ----
for k in present:
    va, vb = vid_span(k); vblk = region[va:vb]
    shot = shot_of(k); cam = cam_of(k)
    if k in tfs:
        donor, nxtf = donor_next(k)
        openName = (look_name(donor) if donor else None) or "the opening look"
        nextName = next_name(k, nxtf)
        hm = re.search(r"\(CHANGE \d \u2014 (.+?) \u00b7 LOOK", header(k))
        mech = (hm.group(1).strip().title() if hm else ("Re-Pour" if k == loopf else "the change"))
        resolve = (f"settles fully into the {nextName} of the Veo last-frame still (Frame {nxtf}'s image)"
                   if nxtf else f"settles fully into the {nextName} the next clip opens on (Veo's last frame)")
        beats = (
            f"- [00:00\u201300:02] Cut to {shot} \u2014 HELD angle (Veo first frame = the clean {openName} still): "
            f"she is already in motion in the {openName} look \u2014 the change NOT yet begun, the angle fixed for "
            f"the whole clip; coiling into the change.\n"
            f"- [00:02\u201300:04] The change BEGINS here, mid-clip: a clean {mech} re-tones the {openName} look into "
            f"the {nextName} look in one continuous sweep \u2014 motivated and crisp, never a muddy blend (angle "
            f"held, identity locked).\n"
            f"- [00:04\u201300:06] The change completes and the look {resolve}, resolved and held; she lands a "
            f"confident beat, eyes alight."
        )
    else:
        ph = action_phases(k)
        camlead = (f"{cam} is already underway" if cam else "the move is already underway")
        if len(ph) >= 3:
            b1, b2, b3 = ph[0], ph[1], " ".join(ph[2:])
        elif len(ph) == 2:
            b1, b2, b3 = ph[0], ph[1], "she settles the beat and holds, eyes alive and direct to lens"
        elif len(ph) == 1:
            b1, b2, b3 = ph[0], "the motion carries through with real momentum and follow-through", "she settles and holds the look, eyes direct"
        else:
            b1, b2, b3 = "she holds the look, alive and breathing", "a slow micro-shift keeps the beat alive", "she settles, eyes direct to lens"
        beats = (
            f"- [00:00\u201300:02] {shot}: {camlead} as {b1}.\n"
            f"- [00:02\u201300:04] {b2}.\n"
            f"- [00:04\u201300:06] {b3}."
        )
    # delete standalone CAMERA MOVEMENT line
    vblk = re.sub(r"^CAMERA MOVEMENT:[^\n]*\n\n?", "", vblk, count=1, flags=re.M)
    # replace SUBJECT ACTION WITH TIMING block with SHOT BREAKDOWN
    vblk = re.sub(r"^SUBJECT ACTION WITH TIMING:[^\n]*$", lambda _: BRK_HDR + "\n" + beats, vblk, count=1, flags=re.M)
    # reset DURATION + FRAME RATE
    vblk = re.sub(r"^DURATION:[^\n]*$", lambda _: DUR_STD, vblk, count=1, flags=re.M)
    vblk = re.sub(r"^FRAME RATE \+ MOTION BLUR:[^\n]*$", lambda _: FR_STD, vblk, count=1, flags=re.M)
    region = region[:va] + vblk + region[vb:]

# ---- L+M image flip on transform frames ----
for KT in tfs:
    donor, nxtf = donor_next(KT)
    openName = (look_name(donor) if donor else None) or "the opening look"
    nextName = next_name(KT, nxtf)
    hm = re.search(r"\(CHANGE \d \u2014 (.+?) \u00b7 LOOK", header(KT))
    mech = (hm.group(1).strip().title() if hm else ("Re-Pour" if KT == loopf else "the change"))
    is_magic = "MAGIC" in header(KT)
    a, b = img_span(KT); blk = region[a:b]
    magictag = " \u2014 the magical change-beat" if is_magic else ""
    resolve = (f"settling into Frame {nxtf}'s {nextName} image (Veo's LAST frame)"
               if nxtf else f"settling into the {nextName} the next clip opens on (Veo's LAST frame)")
    note = (f"CHANGE KEYFRAME NOTE: the {mech} ({openName} \u2192 {nextName}){magictag} \u2014 contained MID-CLIP "
            f"inside this one frame at a HELD angle. This is the START frame of the transform CLIP \u2014 render her "
            f"fully in the clean {openName} look (the exact still the Frame-{KT} video opens on, and Veo's FIRST "
            f"frame), the change NOT yet begun. The change happens MID-CLIP at this same held angle \u2014 a clean "
            f"{mech} re-tones the {openName} look into the {nextName} look in one continuous sweep \u2014 {resolve}; "
            f"the camera may travel with her but never rotates its angle through the change. Face, bone structure "
            f"and eye colour stay 100% locked. Do NOT depict the change in this still and do NOT invent a second "
            f"Aira, a new face or new hands.")
    if re.search(r"^CHANGE KEYFRAME NOTE:", blk, re.M):
        blk = re.sub(r"^CHANGE KEYFRAME NOTE:[^\n]*$", lambda _: note, blk, count=1, flags=re.M)
    elif re.search(r"^LOOP[^\n]*KEYFRAME NOTE:|^LOOP NOTE", blk, re.M):
        blk = re.sub(r"^(LOOP[^\n]*NOTE[^\n]*)$", lambda _: note, blk, count=1, flags=re.M)
    # flip WARDROBE to clean opening look (reuse donor wardrobe) if donor exists
    if donor:
        ow = ward_line(donor)
        ow = re.sub(r"^WARDROBE \(LOOK \w \u2014 ([^)]+)\):",
                    lambda mm: f"WARDROBE (clean {mm.group(1)} \u2014 intact, change not yet begun):", ow)
        blk = re.sub(r"^WARDROBE[^\n]*$", lambda _: ow, blk, count=1, flags=re.M)
        for lab, val in stable_fields(donor).items():
            blk = re.sub(rf"^{lab}[^\n]*$", lambda _ , v=val: v, blk, count=1, flags=re.M)
    blk = re.sub(r"^COMPOSITION REFERENCE:[^\n]*$",
                 lambda _: f"COMPOSITION REFERENCE: the held beat before the {mech} \u2014 the clean {openName} "
                           f"look, the change about to fire on the cut.", blk, count=1, flags=re.M)
    blk = re.sub(r"^ATMOSPHERE:[^\n]*$",
                 lambda _: f"ATMOSPHERE: charged, metallic, alive \u2014 the instant before {openName} re-pours into "
                           f"{nextName}.", blk, count=1, flags=re.M)
    region = region[:a] + blk + region[b:]

# ---- brief ----
add = (" Each look-change is contained MID-CLIP at a HELD angle (Veo first/last-frame: the clean opening look -> "
       "the resolved next look), never an instant snap across a cut; every frame join is a hard match-cut to a new "
       "angle, and face/identity stays locked through every change.")
mv = re.search(r"^Movement:\s*(.+)$", region, re.M)
if mv:
    base = mv.group(1).rstrip(); base += "" if base.endswith(('.', '!')) else "."
    region = re.sub(r"^Movement:\s*.+$", lambda _: "Movement: " + base + add, region, count=1, flags=re.M)
region = re.sub(r"^(Identity safety:[^\n]*?)$",
                lambda mm: mm.group(1) + (" every look-change is contained inside one clip at a held angle and "
                "resolves smoothly by clip-end; her single self and face are never duplicated or covered."),
                region, count=1, flags=re.M)

text = text[:r0] + region + text[r1:]
open(path, "w", encoding="utf-8").write(text)
sb = region.count("SHOT BREAKDOWN (timed"); vp = region.count("\u2014 VIDEO PROMPT")
sa = region.count("SUBJECT ACTION WITH TIMING"); cm = len(re.findall(r"^CAMERA MOVEMENT:", region, re.M))
dur_bad = len([l for l in region.splitlines() if l.startswith("DURATION:") and "6 seconds" not in l])
print(f"CONCEPT {N}: F={F} transforms={tfs} loop={loopf} SB={sb} VP={vp} leftover-SA={sa} standalone-CAM={cm} dur_bad={dur_bad}")

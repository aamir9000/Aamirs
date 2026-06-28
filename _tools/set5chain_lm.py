#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Set-5 CHAINED multi-look L+M engine (clothes-change concepts 83, 84).

These concepts cycle several looks (A->B->C->D) with a transform frame between
each held look: headers like
  "## Frame 2 of 8 - IMAGE PROMPT (CHANGE 1 - SPIN-BLUR SNAP-CHANGE - LOOK A -> LOOK B)".
Each transform frame opens on the PRIOR look (the frame before it, a clean
"LOOK X" hold) and resolves to the NEXT look (the frame after it). L+M model:
each change is contained MID-CLIP at a HELD angle, Veo first = this frame's image
(the clean opening look = the prior LOOK frame's look), Veo last = the next LOOK
frame's image; every join is a hard match-cut.

Per transform frame: rewrite the TRANSFORM KEYFRAME NOTE to L+M, flip the
"(mid-change)" WARDROBE to the clean opening look (reuse the prior LOOK frame's
WARDROBE + stable look fields), rewrite the 3 SHOT BREAKDOWN beats to
hold-openLook / change-begins-mid-clip / resolve-to-nextLook. Brief Movement +
Identity-safety -> L+M. Idempotent.
Usage: python3 _tools/set5chain_lm.py "<path>" <concept_number>
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

def img_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT")
    b = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT", a)
    return a, b
def vid_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT")
    if k < F: b = region.index(f"## Frame {k+1} of {F} \u2014 IMAGE PROMPT", a)
    else:
        nb = re.search(r"\n### |\n# CONCEPT ", region[a:]); b = a + nb.start() if nb else len(region)
    return a, b
def header(k):
    i = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT")
    return region[i:region.index(chr(10), i)]
def wardrobe_line(k):
    a, b = img_span(k)
    mm = re.search(r"^WARDROBE[^\n]*$", region[a:b], re.M)
    return mm.group(0) if mm else ""
def look_name(k):
    mm = re.search(r"WARDROBE \(LOOK . \u2014 ([^)]+)\)", wardrobe_line(k))
    return mm.group(1).strip() if mm else None
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

# transform frames = headers with "CHANGE n"
tfs = [k for k in range(1, F + 1) if re.search(r"\(CHANGE \d", header(k))]

for KT in tfs:
    hdr = header(KT)
    hm = re.search(r"\(CHANGE \d \u2014 (.+?) \u2014 LOOK (\w) \u2192 LOOK (\w)\)", hdr)
    mechanism = hm.group(1).strip().title() if hm else "the snap-change"
    donor = KT - 1            # the clean opening-look frame
    nxtf = KT + 1             # the resolved next-look frame
    openName = look_name(donor) or f"Look {hm.group(2) if hm else 'A'}"
    nextName = look_name(nxtf) or f"Look {hm.group(3) if hm else 'B'}"
    is_magic = "(MAGIC BEAT)" in hdr or "MAGIC" in hdr
    magictag = " \u2014 the magical change-beat" if is_magic else ""
    a, b = img_span(KT); blk = region[a:b]
    note = (f"TRANSFORM KEYFRAME NOTE: the {mechanism} ({openName} \u2192 {nextName})"
            f"{magictag} \u2014 contained MID-CLIP inside this one "
            f"frame at a HELD angle. This is the START frame of the transform CLIP \u2014 render her fully in the "
            f"clean {openName} look (the exact still the Frame-{KT} video opens on, and Veo's FIRST frame), the "
            f"change NOT yet begun. The change happens MID-CLIP at this same held angle \u2014 a clean {mechanism} "
            f"flips the {openName} look to the {nextName} look in one continuous motion \u2014 settling into Frame "
            f"{nxtf}'s {nextName} image (Veo's LAST frame); the camera may travel with her but never rotates its "
            f"angle through the change. Face, bone-structure, eye colour and hair stay locked to the reference. Do "
            f"NOT depict the change in this still and do NOT invent a second Aira, a new face or new hands.")
    blk = re.sub(r"^TRANSFORM KEYFRAME NOTE:[^\n]*$", lambda _: note, blk, count=1, flags=re.M)
    # flip WARDROBE (mid-change) -> the clean opening look (reuse donor wardrobe)
    open_ward = wardrobe_line(donor)
    open_ward = re.sub(r"^WARDROBE \(LOOK \w \u2014 ([^)]+)\):",
                       lambda mm: f"WARDROBE (clean {mm.group(1)} \u2014 intact, the change not yet begun):",
                       open_ward)
    blk = re.sub(r"^WARDROBE[^\n]*$", lambda _: open_ward, blk, count=1, flags=re.M)
    # reuse donor stable look fields
    sf = stable_fields(donor)
    for lab, val in sf.items():
        blk = re.sub(rf"^{lab}[^\n]*$", lambda _ , v=val: v, blk, count=1, flags=re.M)
    blk = re.sub(r"^COMPOSITION REFERENCE:[^\n]*$",
                 lambda _: f"COMPOSITION REFERENCE: the held beat before the {mechanism} \u2014 the clean {openName} "
                           f"look, the change about to fire on the cut.", blk, count=1, flags=re.M)
    blk = re.sub(r"^ATMOSPHERE:[^\n]*$",
                 lambda _: f"ATMOSPHERE: charged, kinetic, pop \u2014 the on-beat instant before {openName} flips to "
                           f"{nextName}.", blk, count=1, flags=re.M)
    region = region[:a] + blk + region[b:]
    # beats
    va, vb = vid_span(KT); vblk = region[va:vb]; shot = shot_of(KT)
    beats = (
        f"- [00:00\u201300:02] Cut to {shot} \u2014 HELD angle (Veo first frame = the clean {openName} still): she "
        f"is already in motion in the {openName} look \u2014 the change NOT yet begun, the angle fixed for the whole "
        f"clip; coiling into the on-beat change.\n"
        f"- [00:02\u201300:04] The change BEGINS here, mid-clip: a clean {mechanism} flips the {openName} look to the "
        f"{nextName} look in one continuous motion \u2014 crisp and motivated, never a muddy blend (angle held, "
        f"identity locked).\n"
        f"- [00:04\u201300:06] The change completes and the look settles fully into the {nextName} of the Veo "
        f"last-frame still (Frame {nxtf}'s image), resolved and held; she lands a confident on-beat pose, eyes alight."
    )
    vblk = re.sub(r"(SHOT BREAKDOWN \(timed[^\n]*\):\n)(?:- \[00:00[^\n]*\n- \[00:02[^\n]*\n- \[00:04[^\n]*)",
                  lambda mm: mm.group(1) + beats, vblk, count=1)
    region = region[:va] + vblk + region[vb:]

# brief
add = (" Each look-change is contained MID-CLIP at a HELD angle (Veo first/last-frame: the clean opening look -> "
       "the resolved next look) \u2014 never an instant snap across a cut; every frame join is a hard match-cut to "
       "a new angle, and identity stays locked through every change.")
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
cut = len(re.findall(r"\[00:00\u201300:02\] Cut to", region))
res = [p for p in ("(mid-change)", "blur-peak the tangerine", "this is the first change-beat", "this is the second change-beat", "this is the third") if p in region]
print(f"CONCEPT {N}: F={F} transform-frames={tfs} SB={sb} VP={vp} Cut-to={cut}; residue={res or 'none'}")

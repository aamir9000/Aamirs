#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Set-5 CONTINUATION L+M engine (concepts 79-82 in the (cont)/(cont 2) files).

These share a uniform structure: a Frame-2 transform frame tagged
"## Frame 2 of N - IMAGE PROMPT (TRANSFORM)" with a "TRANSFORM KEYFRAME NOTE:
this is the signature change-beat. ... KEYFRAME-LOCK : ... Cause -> effect ..."
note, and a "(MAGIC BEAT)" frame carrying a "MAGIC NOTE:" line (look unchanged,
only the optical effect animates). Frame 1 is the clean opening look.

Per concept (data table CONT below):
  * SWAP (79 liquid-chrome->prism, 80 cobalt->marigold colour-shift): the
    transform frame's image is flipped to the clean Look A (reusing Frame 1's
    look fields), L+M note, hold-A / change-begins-mid-clip / resolve-to-LookB beats.
  * ASSEMBLY (81 blobs, 82 plasma-filaments): the transform frame opens on the
    pre-form material (gown NOT yet formed), assembling mid-clip into the gown.
  * MAGIC BEAT frame: the MAGIC NOTE is reframed to contained-MID-CLIP at a HELD
    angle, this still = the kindle opening, single self/face/look locked & uncovered,
    believable optical physics, settle, match-cut; beat 1 opens "Cut to ... HELD angle".
Brief Movement + Identity-safety -> L+M. Idempotent.
Usage: python3 _tools/set5cont_lm.py "<path>" <concept_number>
"""
import re, sys

path = sys.argv[1]
N = int(sys.argv[2])
text = open(path, encoding="utf-8").read()

m = re.search(rf"^# CONCEPT {N} \u2014.*$", text, re.M)
if not m:
    sys.exit(f"concept {N} not found")
nxt = re.search(rf"^# CONCEPT {N+1} \u2014", text[m.end():], re.M)
r0 = m.start(); r1 = m.end() + nxt.start() if nxt else len(text)
region = text[r0:r1]
if "contained MID-CLIP" in region:
    print(f"CONCEPT {N}: already L+M (skipped)"); sys.exit(0)

CONT = {
    79: dict(mode="swap", lookA="sleek liquid-chrome column gown", lookB="faceted holographic prism gown",
             essence="a ribbon of iridescent oil-slick liquid-foil pours down and swirls around her, then sets and facets"),
    80: dict(mode="swap", lookA="cobalt-blue sculptural one-shoulder column gown", lookB="marigold sculptural column gown",
             essence="a warm radiant heat-bloom wave sweeps diagonally and triggers a thermochromic colour-shift, cobalt igniting into marigold along a clean travelling boundary"),
    81: dict(mode="assembly", material="glossy candy lava-lamp blobs", lookB="magenta liquid-latex blob-form gown",
             essence="glossy candy lava-lamp blobs rise from the floor, float up around her and merge into a single sheet"),
    82: dict(mode="assembly", material="crackling magenta-cyan plasma filaments", lookB="liquid-chrome plasma-filament gown",
             essence="crackling plasma filaments arc out from the orb and the floor, race up around her in glowing electric threads and weave"),
}
d = CONT.get(N)
if not d:
    sys.exit(f"concept {N}: not in CONT table")

fm = re.search(r"## Frame 1 of (\d+) \u2014 IMAGE PROMPT", region)
F = int(fm.group(1))

def img_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT")
    b = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT", a)
    return a, b

def vid_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT")
    if k < F:
        b = region.index(f"## Frame {k+1} of {F} \u2014 IMAGE PROMPT", a)
    else:
        nb = re.search(r"\n### |\n# CONCEPT ", region[a:]); b = a + nb.start() if nb else len(region)
    return a, b

# detect KT (TRANSFORM) and KM (MAGIC BEAT) by header
KT = KM = None
for k in range(1, F + 1):
    hdr_i = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT")
    hdr = region[hdr_i:region.index(chr(10), hdr_i)]
    if "(TRANSFORM)" in hdr:
        KT = k
    if "(MAGIC BEAT)" in hdr:
        KM = k

def fields(blk):
    out = {}
    for line in blk.splitlines():
        for lab in ("WARDROBE", "FOOTWEAR", "ACCESSORIES", "HAIR", "MAKEUP", "EYE COLOUR",
                    "KINETIC STILLNESS", "SPATIAL LOGIC", "LIGHTING", "COLOR GRADE",
                    "TEXTURE & MICRO-DETAIL"):
            if line.startswith(lab):
                out.setdefault(lab, line); break
    return out

a1, b1 = img_span(1); f1 = fields(region[a1:b1])

def shot_of(k):
    va, vb = vid_span(k)
    sm = re.search(r"^SHOT TYPE:\s*(.+)$", region[va:vb], re.M)
    return sm.group(1).strip().rstrip(".") if sm else "the hero"

# ---------- KT (transform) ----------
if KT:
    a, b = img_span(KT); blk = region[a:b]
    if d["mode"] == "swap":
        la, lb = d["lookA"], d["lookB"]
        note = (f"TRANSFORM KEYFRAME NOTE: the look change \u2014 contained MID-CLIP inside this one frame at a "
                f"HELD angle. This is the START frame of the transform CLIP \u2014 render her fully in the {la} "
                f"Look A (the exact still the Frame-{KT} video opens on, and Veo's FIRST frame): the {la} fully "
                f"intact, the change NOT yet begun. The change happens MID-CLIP at this same held angle \u2014 "
                f"{d['essence']} into the {lb} \u2014 settling into Frame {KT+1}'s {lb} image (Veo's LAST frame); "
                f"the camera may travel or crane with her but never rotates its angle through the change. Face, "
                f"hairline, eye position and skin texture stay identical to Frame 1. Do NOT depict the morph in "
                f"this still and do NOT invent a second Aira, a new face or new hands.")
        ward = f"WARDROBE: (Look A, intact) \u2014 the {la}, fully intact and unchanged, the change NOT yet begun; fabric pristine with zero wrinkles, lint or stray threads."
        b2 = (f"the {la} re-forming into the {lb}")
    else:  # assembly
        mat, lb = d["material"], d["lookB"]
        note = (f"TRANSFORM KEYFRAME NOTE: the material-assembly change \u2014 contained MID-CLIP inside this one "
                f"frame at a HELD angle. This is the START frame of the transform CLIP (Veo's FIRST frame): {mat} "
                f"just beginning to gather, the {lb} NOT yet formed. The change happens MID-CLIP at this same held "
                f"angle \u2014 {d['essence']} and set into the {lb} \u2014 settling into Frame {KT+1}'s fully-formed "
                f"image (Veo's LAST frame); the camera may travel or crane with her but never rotates its angle "
                f"through the change. Face, hairline, eye position and skin texture stay identical to Frame 1. Do "
                f"NOT depict the formed gown in this still and do NOT invent a second Aira, a new face or new hands.")
        ward = f"WARDROBE: (start of assembly) \u2014 the {lb} NOT yet formed; {mat} just beginning to gather and rise, only the first elements starting to settle; no formed gown yet, no floating debris."
        b2 = (f"the {mat} assembling and setting into the {lb}")
    blk = re.sub(r"^TRANSFORM KEYFRAME NOTE:[^\n]*$", lambda _: note, blk, count=1, flags=re.M)
    blk = re.sub(r"^WARDROBE[^\n]*$", lambda _: ward, blk, count=1, flags=re.M)
    # reuse Frame 1 stable look fields
    for lab in ("FOOTWEAR", "ACCESSORIES", "HAIR", "MAKEUP", "EYE COLOUR", "KINETIC STILLNESS",
                "SPATIAL LOGIC", "LIGHTING", "TEXTURE & MICRO-DETAIL"):
        if lab in f1:
            blk = re.sub(rf"^{lab}[^\n]*$", lambda _ , v=f1[lab]: v, blk, count=1, flags=re.M)
    # clean transform phrasing in the kept FRAMING/SUBJECT/BODY/FACIAL
    blk = blk.replace("caught mid-transform", "poised before the change")
    blk = blk.replace("mid-transform but balanced", "poised and balanced before the change")
    blk = re.sub(r"^COMPOSITION REFERENCE:[^\n]*$",
                 lambda _: "COMPOSITION REFERENCE: the held breath before the signature change \u2014 the clean "
                           "opening look, the single impossible move about to begin.", blk, count=1, flags=re.M)
    blk = re.sub(r"^ATMOSPHERE:[^\n]*$",
                 lambda _: "ATMOSPHERE: anticipatory, electric, futuristic \u2014 the instant before the change "
                           "sweeps across her.", blk, count=1, flags=re.M)
    region = region[:a] + blk + region[b:]
    # beats
    va, vb = vid_span(KT); vblk = region[va:vb]; shot = shot_of(KT)
    looklabel = d.get("lookA") or d.get("lookB")
    beats = (
        f"- [00:00\u201300:02] Cut to {shot} \u2014 HELD angle (Veo first frame = the clean opening still): she is "
        f"already in motion in the intact opening look \u2014 the change NOT yet begun, the angle fixed for the "
        f"whole clip; gaze beginning to track the coming change.\n"
        f"- [00:02\u201300:04] The change BEGINS here, mid-clip: {b2} in one continuous motion \u2014 gradual and "
        f"motivated, never a snap; a wondering breath, brows lifting (angle held, identity locked).\n"
        f"- [00:04\u201300:06] The change completes and the look settles smoothly and fully into the {d.get('lookB','new look')} "
        f"of the Veo last-frame still (Frame {KT+1}'s image), resolved and held; she lands a confident finished beat, eyes alight."
    )
    vblk = re.sub(r"(SHOT BREAKDOWN \(timed[^\n]*\):\n)(?:- \[00:00[^\n]*\n- \[00:02[^\n]*\n- \[00:04[^\n]*)",
                  lambda mm: mm.group(1) + beats, vblk, count=1)
    region = region[:va] + vblk + region[vb:]

# ---------- KM (magic beat) ----------
if KM:
    a, b = img_span(KM); blk = region[a:b]
    knote = ("MAGIC NOTE: the optical magic beat \u2014 contained MID-CLIP at a HELD angle. This still is the KINDLE "
             "opening (Veo's FIRST frame): the effect only just beginning, her look otherwise calm and fully "
             "resolved. The burst happens MID-CLIP at this same held angle, blooms to its peak and SETTLES to a "
             "sustained halo (Veo's LAST frame); the camera may orbit or push but never rotates its angle through "
             "it. Her SINGLE self, face, hair and wardrobe stay locked and uncovered throughout \u2014 only the "
             "light/effect animates. Real optical physics; no melting, no second subject, no blown highlights; "
             "frame joins are hard match-cuts to new angles.")
    if re.search(r"^MAGIC NOTE:", blk, re.M):
        blk = re.sub(r"^MAGIC NOTE:[^\n]*$", lambda _: knote, blk, count=1, flags=re.M)
    region = region[:a] + blk + region[b:]
    va, vb = vid_span(KM); vblk = region[va:vb]; shot = shot_of(KM)
    b1 = (f"- [00:00\u201300:02] Cut to {shot} \u2014 HELD angle (Veo first frame = the kindle still): the effect is "
          f"only just beginning, her look calm and fully resolved; gaze drawn to it (her single self held, the angle fixed).")
    vblk = re.sub(r"- \[00:00\u201300:02\][^\n]*", lambda _: b1, vblk, count=1)
    region = region[:va] + vblk + region[vb:]

# ---------- brief ----------
add = (" The look change is contained MID-CLIP at a HELD angle (Veo first/last-frame: clean Look A -> resolved "
       "Look B) and the optical magic beat is contained mid-clip too (her single resolved look held, the effect "
       "kindles -> blooms -> settles to a halo); every frame join is a hard match-cut to a new angle.")
mv = re.search(r"^Movement:\s*(.+)$", region, re.M)
if mv:
    base = mv.group(1).rstrip(); base += "" if base.endswith(('.', '!')) else "."
    region = re.sub(r"^Movement:\s*.+$", lambda _: "Movement: " + base + add, region, count=1, flags=re.M)
region = re.sub(r"^(Identity safety:[^\n]*?)$",
                lambda mm: mm.group(1) + (" each impossible beat is contained inside one clip at a held angle and "
                "resolves smoothly by clip-end; her single self and face are never duplicated or covered."),
                region, count=1, flags=re.M)

text = text[:r0] + region + text[r1:]
open(path, "w", encoding="utf-8").write(text)

sb = region.count("SHOT BREAKDOWN (timed"); vp = region.count("\u2014 VIDEO PROMPT")
cut = len(re.findall(r"\[00:00\u201300:02\] Cut to", region))
res = [p for p in ("(mid-transform)", "transitions from the", "KEYFRAME-LOCK :", "signature change-beat") if p in region]
print(f"CONCEPT {N}: mode={d['mode']} F={F} KT={KT} KM={KM} SB={sb} VP={vp} Cut-to={cut}; residue={res or 'none'}")

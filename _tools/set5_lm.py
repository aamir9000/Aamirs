#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Set-5 L+M retrofit engine (assembly-type couture + VFX-burst concepts 72-79).

Each Set-5 concept has TWO impossible beats:
  * KT = the material-assembly transform frame (base -> couture; note "START
    keyframe of the <change> transform"). Handled like Set 4 but the START state
    is the PRE-FORM material (the gown not yet formed), since Frame 1 already
    shows the formed gown. -> rewrite NOTE to L+M, flip WARDROBE to the pre-form
    START, clean SUBJECT/COMP/ATMOSPHERE, rewrite the 3 SHOT BREAKDOWN beats to
    hold-pre-form / assemble-mid-clip / resolve-to-formed.
  * KM = the VFX "magic burst" frame (look unchanged, only the effect animates;
    note "owns the magic beat" / "PEAK keyframe" / a "MAGIC EFFECT" block).
    -> reframe the NOTE to contained-MID-CLIP at a HELD angle, this still = the
    KINDLE opening, single self/face/look locked & uncovered, believable physics,
    settle-to-halo, match-cut joins; open beat 1 with "Cut to ... HELD angle".
Plus the brief Movement + Identity-safety lines -> L+M.

Idempotent. Usage: python3 _tools/set5_lm.py "<path>" <concept_number>
"""
import re, sys

path = sys.argv[1]
N = int(sys.argv[2])
text = open(path, encoding="utf-8").read()

m = re.search(rf"^# CONCEPT {N} \u2014.*$", text, re.M)
if not m:
    sys.exit(f"concept {N} not found")
nxt = re.search(rf"^# CONCEPT {N+1} \u2014", text[m.end():], re.M)
r0 = m.start()
r1 = m.end() + nxt.start() if nxt else len(text)
region = text[r0:r1]

if "contained MID-CLIP" in region:
    print(f"CONCEPT {N}: already L+M (skipped)")
    sys.exit(0)

MAT = {
    72: "candy-bright terrazzo chips",
    73: "glowing woven-rattan strands",
    74: "sweeping clouds of vivid pastel chalk-dust",
    75: "thousands of colour-flipping sequins",
    76: "glossy jewel-tone liquid enamel",
    77: "flat sheets of vivid kirigami paper",
    78: "flat candy-chrome mylar foil",
    79: "iridescent prism mirror-foil panels",
}
material = MAT.get(N, "its forming material")

fm = re.search(r"## Frame 1 of (\d+) \u2014 IMAGE PROMPT", region)
F = int(fm.group(1))

def frame_img_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT")
    b = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT", a)
    return a, b

def frame_vid_span(k):
    a = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT")
    if k < F:
        b = region.index(f"## Frame {k+1} of {F} \u2014 IMAGE PROMPT", a)
    else:
        nb = re.search(r"\n### |\n# CONCEPT ", region[a:])
        b = a + nb.start() if nb else len(region)
    return a, b

# locate KT (assembly transform) and KM (magic burst)
KT = KM = None
for k in range(1, F + 1):
    a, b = frame_img_span(k)
    blk = region[a:b]
    if re.search(r"START keyframe of the .+? transform", blk):
        KT = k
    if ("owns the magic beat" in blk) or ("PEAK keyframe" in blk) or ("MAGIC EFFECT \u2014" in blk):
        KM = k
if KT is None and KM is None:
    sys.exit(f"concept {N}: no transform/magic frame found (corrupt?)")

# brief Wardrobe -> gownB
wm = re.search(r"^Wardrobe:\s*(.+)$", region, re.M)
gownB = wm.group(1).strip() if wm else "the couture gown"
if "\u2192" in gownB:
    gownB = gownB.split("\u2192")[-1].strip()
gownB = re.sub(r"^(a |an |the )", "", gownB, flags=re.I)

def shot_of(k):
    va, vb = frame_vid_span(k)
    sm = re.search(r"^SHOT TYPE:\s*(.+)$", region[va:vb], re.M)
    return (sm.group(1).strip().rstrip(".") if sm else "the hero")

def replace_line(blk, prefix, newline):
    return re.sub(rf"^{re.escape(prefix)}[^\n]*$", lambda _: newline, blk, count=1, flags=re.M)

def replace_beats(vblk, beats):
    return re.sub(r"(SHOT BREAKDOWN \(timed[^\n]*\):\n)(?:- \[00:00[^\n]*\n- \[00:02[^\n]*\n- \[00:04[^\n]*)",
                  lambda mm: mm.group(1) + beats, vblk, count=1)

# ---- KT (assembly transform) ----
if KT is not None:
    a, b = frame_img_span(KT)
    blk = region[a:b]
    change_m = re.search(r"START keyframe of the (.+?) transform", blk)
    change = change_m.group(1).strip() if change_m else "material-assembly"
    note = (f"TRANSFORM KEYFRAME NOTE: the {change} transform \u2014 contained MID-CLIP inside this one "
            f"frame at a HELD angle. This is the START frame of the transform CLIP (Veo's FIRST frame): "
            f"{material} just beginning to sweep in from the frame edges toward the seam lines, the {gownB} "
            f"NOT yet formed. The change happens MID-CLIP at this same held angle \u2014 the {material} "
            f"assembling and locking into the {gownB} \u2014 settling into Frame {KT+1}'s fully-formed image "
            f"(Veo's LAST frame); the camera may travel or crane with her but never rotates its angle through "
            f"the change. Face, hair and identity stay fixed throughout. Do NOT depict the formed gown in this "
            f"still and do NOT invent a second Aira, a new face or new hands.")
    blk = re.sub(r"^TRANSFORM KEYFRAME NOTE:[^\n]*$", lambda _: note, blk, count=1, flags=re.M)
    ward = (f"WARDROBE: (start of assembly) \u2014 the {gownB} NOT yet formed; {material} just beginning to "
            f"sweep in from the frame edges toward the seam lines, only the first elements starting to lock, "
            f"surfaces clean and edges sharpening; no formed gown yet, no floating debris.")
    blk = re.sub(r"^WARDROBE[^\n]*$", lambda _: ward, blk, count=1, flags=re.M)
    blk = blk.replace("the transform climbing the figure", "the look held in its pre-form moment")
    blk = blk.replace("widening to take in the building couture", "holding the pre-form START before it builds")
    blk = re.sub(r"^COMPOSITION REFERENCE:[^\n]*$",
                 lambda _: f"COMPOSITION REFERENCE: the held breath before the {change} assembly \u2014 "
                           f"kinetic, graphic, the single impossible build about to begin.", blk, count=1, flags=re.M)
    blk = re.sub(r"^ATMOSPHERE:[^\n]*$",
                 lambda _: f"ATMOSPHERE: anticipatory, electric, magical \u2014 the instant before the look "
                           f"builds around her from {material}.", blk, count=1, flags=re.M)
    region = region[:a] + blk + region[b:]
    # beats
    va, vb = frame_vid_span(KT)
    vblk = region[va:vb]
    shot = shot_of(KT)
    beats = (
        f"- [00:00\u201300:02] Cut to {shot} \u2014 HELD angle (Veo first frame = the pre-form START still): "
        f"{material} already sweeping in from the frame edges as she opens to present \u2014 the {gownB} NOT "
        f"yet formed, the angle fixed for the whole clip; gaze tracking the incoming material.\n"
        f"- [00:02\u201300:04] The change BEGINS here, mid-clip: the {material} assembling and locking along the "
        f"seam lines into the {gownB} in one continuous build \u2014 gradual and motivated, never a snap; a "
        f"delighted breath, brows lifting in wonder (angle held, identity locked).\n"
        f"- [00:04\u201300:06] The build completes and the look settles smoothly and fully into the {gownB} of "
        f"the Veo last-frame still (Frame {KT+1}'s image), resolved and held; a confident finished beat, eyes alight."
    )
    vblk = replace_beats(vblk, beats)
    region = region[:va] + vblk + region[vb:]

# ---- KM (VFX magic burst) ----
if KM is not None:
    a, b = frame_img_span(KM)
    blk = region[a:b]
    eff = None
    for pat in (r"owns the magic beat \u2014 (?:a |an )?(.+?)[.(]",
                r"PEAK keyframe of the (.+?) (?:magic|burst|bloom)",
                r"MAGIC EFFECT \u2014 (.+?) \("):
        em = re.search(pat, blk)
        if em:
            eff = em.group(1).strip(); break
    eff = eff or "the magic burst"
    knote = (f"TRANSFORM KEYFRAME NOTE: the {eff} \u2014 the single impossible move, contained MID-CLIP at a "
             f"HELD angle. This still is the KINDLE opening (Veo's FIRST frame): the {eff} only just beginning, "
             f"tight at its source, her look otherwise calm and fully resolved. The burst happens MID-CLIP at "
             f"this same held angle and radiates then SETTLES to a sustained halo (Veo's LAST frame); the camera "
             f"may push or orbit but never rotates its angle through it. Her SINGLE self, face, hair and wardrobe "
             f"stay locked and uncovered throughout \u2014 only the effect animates. Believable real physics; no "
             f"double-Aira, no blown highlights; frame joins are hard match-cuts to new angles.")
    if re.search(r"^TRANSFORM KEYFRAME NOTE:", blk, re.M):
        blk = re.sub(r"^TRANSFORM KEYFRAME NOTE:[^\n]*$", lambda _: knote, blk, count=1, flags=re.M)
    elif re.search(r"^MAGIC EFFECT \u2014[^\n]*$", blk, re.M):
        blk = re.sub(r"^MAGIC EFFECT \u2014[^\n]*$", lambda _: knote, blk, count=1, flags=re.M)
    region = region[:a] + blk + region[b:]
    # beat 1 -> Cut to / HELD / kindle
    va, vb = frame_vid_span(KM)
    vblk = region[va:vb]
    shot = shot_of(KM)
    b1 = (f"- [00:00\u201300:02] Cut to {shot} \u2014 HELD angle (Veo first frame = the kindle still): the {eff} "
          f"is only just beginning, tight at its source, her look calm and fully resolved; gaze drawn to it "
          f"(her single self held, the angle fixed).")
    vblk = re.sub(r"- \[00:00\u201300:02\][^\n]*", lambda _: b1, vblk, count=1)
    region = region[:va] + vblk + region[vb:]

# ---- brief Movement + Identity safety ----
mv = re.search(r"^Movement:\s*(.+)$", region, re.M)
if mv:
    base = mv.group(1).rstrip()
    add = (" Both impossible beats are contained MID-CLIP at a HELD angle \u2014 the material-assembly transform "
           "inside the transform frame (Veo first/last-frame: pre-form START -> resolved gown) and the VFX burst "
           "inside the magic frame (her single resolved look held, the effect kindles -> radiates -> settles to a "
           "halo); every frame join is a hard match-cut to a new angle.")
    if not base.endswith(('.', '!')):
        base += "."
    region = re.sub(r"^Movement:\s*.+$", lambda _: "Movement: " + base + add, region, count=1, flags=re.M)

region = re.sub(r"^(Identity safety:[^\n]*?)$",
                lambda mm: mm.group(1) + (" each impossible beat is contained inside one clip at a held angle and "
                "resolves smoothly by clip-end; her single self and face are never duplicated or covered."),
                region, count=1, flags=re.M)

text = text[:r0] + region + text[r1:]
open(path, "w", encoding="utf-8").write(text)

sb = region.count("SHOT BREAKDOWN (timed")
vp = region.count("\u2014 VIDEO PROMPT")
cut = len(re.findall(r"\[00:00\u201300:02\] Cut to", region))
res = [p for p in ("is 60% formed", "(mid-transform)", "(transforming)", "START keyframe =",
                   "the transform climbing the figure") if p in region]
print(f"CONCEPT {N}: F={F} KT={KT} KM={KM} change-material={material!r} effect-detected; "
      f"SB={sb} VP={vp} Cut-to={cut}; residue={res or 'none'}; gownB={gownB[:42]!r}")

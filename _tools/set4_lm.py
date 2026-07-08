#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Set-4-family L+M retrofit engine (steering sections L + M, surgical method).

Scope: the couture mid-clip A->B transform files whose transform lives on ONE
frame as a `TRANSFORM KEYFRAME NOTE` (Set 4 51-70 and the structurally-identical
Set 5 / continuation files). Per concept it:
  1. parses the brief `Wardrobe:` line -> (LookA, change, LookB);
  2. appends the L+M continuity sentence to the `Movement:` line (idempotent);
  3. rewrites the `Identity safety:` line to the contained-mid-clip model;
  4. rebuilds the transform-frame IMAGE as the CLEAN Look A: it reuses that
     concept's OWN clean Frame-1 look/world fields (WARDROBE/HAIR/MAKEUP/HANDS/
     FACIAL/KINETIC/SPATIAL/LIGHTING/COLOR GRADE/TEXTURE) so there is zero morph
     residue, while KEEPING the transform frame's distinct angle (BODY POSTURE /
     FRAMING / SUBJECT FRAMING / LENS, cleaned of morph phrasing) and inserting a
     generated L+M TRANSFORM KEYFRAME NOTE + anticipation COMP/ATMOSPHERE;
  5. rewrites the transform-frame VIDEO `SHOT BREAKDOWN` 3 beats to the L+M
     hold-A / morph-begins-mid-clip / resolve-to-LookB model (Veo first=this
     frame's Look A still, last=next frame's Look B still).
The transform frame is detected dynamically (the frame whose IMAGE block holds
`TRANSFORM KEYFRAME NOTE`); the next frame's image is the Look B / Veo last frame.
Idempotent. Usage: python3 _tools/set4_lm.py "<path>" <concept_number>
"""
import re
import sys

path = sys.argv[1]
N = int(sys.argv[2])
text = open(path, encoding="utf-8").read()

# ---- isolate the concept region -------------------------------------------
m = re.search(rf"^# CONCEPT {N} \u2014.*$", text, re.M)
if not m:
    sys.exit(f"concept {N} not found")
nxt = re.search(rf"^# CONCEPT {N+1} \u2014", text[m.end():], re.M)
r_start = m.start()
r_end = m.end() + nxt.start() if nxt else len(text)
region = text[r_start:r_end]
orig_region = region

if "contained MID-CLIP inside" in region:
    print(f"CONCEPT {N}: already L+M (skipped)")
    sys.exit(0)

# ---- parse the brief Wardrobe line ----------------------------------------
wm = re.search(r"^Wardrobe:\s*(.+?)\s*\(start\)\s*\u2192\s*transforms via\s*(.+?)\s*into\s*(.+)$",
               region, re.M)
if not wm:
    sys.exit(f"concept {N}: could not parse Wardrobe line")
lookA = wm.group(1).strip().rstrip(".")
change = wm.group(2).strip().rstrip(".")
lookB = wm.group(3).strip().rstrip(".")
# tidy leading article duplication for prose
def noart(s):
    return re.sub(r"^(a |an |the )", "", s, flags=re.I)

# ---- frame count + transform frame index ----------------------------------
fm = re.search(r"## Frame 1 of (\d+) \u2014 IMAGE PROMPT", region)
F = int(fm.group(1))

def img_block(k):
    a = region.index(f"## Frame {k} of {F} \u2014 IMAGE PROMPT")
    b = region.index(f"## Frame {k} of {F} \u2014 VIDEO PROMPT", a)
    return a, b

# find transform frame
K = None
for k in range(1, F + 1):
    a, b = img_block(k)
    if "TRANSFORM KEYFRAME NOTE" in region[a:b]:
        K = k
        break
if K is None:
    sys.exit(f"concept {N}: no TRANSFORM KEYFRAME NOTE frame found")

# ---- helper: split an image block into label->line ------------------------
def parse_fields(block):
    d = {}
    for line in block.splitlines():
        for lab in ("WARDROBE:", "HAIR (", "MAKEUP (", "HANDS & NAILS:",
                    "FACIAL MICRO-DYNAMICS:", "KINETIC STILLNESS",
                    "SPATIAL LOGIC:", "LIGHTING:", "COLOR GRADE:",
                    "TEXTURE & MICRO-DETAIL:", "BODY POSTURE & WEIGHT:",
                    "FRAMING:", "SUBJECT FRAMING & POSITION:",
                    "LENS + DOF + BOKEH:", "NEGATIVE:",
                    "COMPOSITION REFERENCE:", "ATMOSPHERE:"):
            if line.startswith(lab):
                key = lab.split(" (")[0].rstrip(":")
                d[key] = line
                break
    return d

a1, b1 = img_block(1)
f1 = parse_fields(region[a1:b1])
aK, bK = img_block(K)
fK = parse_fields(region[aK:bK])

la = noart(lookA)
lb = noart(lookB)
# world noun: prefer the SPATIAL BACKGROUND location, then framing fallbacks
world = "set"
bgm = re.search(r"BACKGROUND \u2014 (?:a |an |the )?(.+?)[,;]", f1.get("SPATIAL LOGIC", ""))
if bgm:
    world = bgm.group(1).strip()
else:
    wm2 = re.search(r"complete figure in frame in the (.+?),", fK.get("SUBJECT FRAMING & POSITION", ""))
    if wm2:
        world = wm2.group(1).strip()

# ---- build the new transform-frame IMAGE block ----------------------------
note = (
    f"TRANSFORM KEYFRAME NOTE: the {change} transform \u2014 contained MID-CLIP inside this one "
    f"frame at a HELD angle. This is the START frame of the transform CLIP \u2014 render her fully "
    f"in the {la} Look A (the exact still the Frame-{K} video opens on, and Veo's FIRST frame): "
    f"the {la} fully intact, face fully recognizable, caught at the instant before the "
    f"{change} begins (the change NOT yet begun). The change happens MID-CLIP at this same HELD "
    f"angle \u2014 {change} sweeps smoothly across her in one continuous wavefront and the "
    f"{la} re-forms into the {lb} \u2014 settling into Frame {K+1}'s finished "
    f"Look B image (Veo's LAST frame); the camera may travel or crane with her but never rotates "
    f"its angle through the change. Identity, bone structure and hair colour ride through untouched. "
    f"Do NOT depict the morph in this still and do NOT invent a new face, new hands or new bone structure."
)

# clean transform-frame pose fields
body = re.sub(r"\s+as (?:the |a )?[\w\- ]+? (?:forms|assembles|sets|blooms|grows|weaves|knits|builds|sculpts|spins up|crystall(?:ises|izes)|takes shape|wicks in|laces (?:up|in))\b",
              "", fK["BODY POSTURE & WEIGHT"])
framing = fK["FRAMING"]
framing = re.sub(r"the [^,;]+? leading the eye(?: inwards?| outward)?", f"the {world} leading the eye", framing)
subj = fK["SUBJECT FRAMING & POSITION"]
subj = re.sub(r"the diagonal transform-line of the .+? leading the eye",
              f"the {world} leading the eye", subj)
subj = subj.replace("one arm beginning the transform gesture", "one arm easing out from the body")

comp = (f"COMPOSITION REFERENCE: the held breath before the signature transform \u2014 a single "
        f"elegant impossible {change} crossing about to begin, cinematic and share-worthy.")
atmo = (f"ATMOSPHERE: anticipation, magical-but-believable \u2014 the instant before the {change} "
        f"re-dresses her.")

new_img_lines = [
    f"## Frame {K} of {F} \u2014 IMAGE PROMPT",
    "",
    "IDENTITY LOCK: Aira [paste identity-lock reference sheet here].",
    "",
    note,
    "",
    f1["WARDROBE"] + "  The look is fully intact \u2014 no transform yet.",
    "",
    f1["HAIR"],
    "",
    f1["MAKEUP"],
    "",
    f1["HANDS & NAILS"],
    "",
    f1["FACIAL MICRO-DYNAMICS"],
    "",
    body,
    "",
    f1["KINETIC STILLNESS"],
    "",
    f1["SPATIAL LOGIC"],
    "",
    f1["LIGHTING"],
    "",
    framing,
    subj,
    "",
    fK["LENS + DOF + BOKEH"],
    "",
    comp,
    "",
    atmo,
    "",
    f1["COLOR GRADE"],
    "",
    f1["TEXTURE & MICRO-DETAIL"],
    "",
    fK["NEGATIVE"],
    "",
]
new_img = "\n".join(new_img_lines)

region = region[:aK] + new_img + region[bK:]

# ---- rewrite the transform-frame VIDEO SHOT BREAKDOWN beats ----------------
# locate the video block for frame K
va = region.index(f"## Frame {K} of {F} \u2014 VIDEO PROMPT")
vb = region.index(f"## Frame {K+1} of {F} \u2014 IMAGE PROMPT", va) if K < F else len(region)
vblock = region[va:vb]
shot_m = re.search(r"^SHOT TYPE:\s*(.+)$", vblock, re.M)
shot = shot_m.group(1).strip().rstrip(".") if shot_m else "the transform hero"

beats = (
    f"- [00:00\u201300:02] Cut to {shot} \u2014 HELD angle (Veo first frame = the {la} Look A "
    f"still): a gentle push-with is already travelling with her in the {la} \u2014 the look "
    f"fully intact, NO change yet, the angle fixed for the whole clip; gaze easing into the beat.\n"
    f"- [00:02\u201300:04] The change BEGINS here, mid-clip: {change} sweeps smoothly across her in one "
    f"continuous wavefront, the {la} re-forming into the {lb} exactly where it "
    f"passes \u2014 gradual and motivated, never a snap; a soft awe rising in her eyes (angle held, "
    f"identity locked).\n"
    f"- [00:04\u201300:06] The wavefront completes and the look settles smoothly and fully into the "
    f"{lb} Look B of the Veo last-frame still (Frame {K+1}'s image), resolved and held; a "
    f"luminous expression landing."
)
# replace the three beat lines under the SHOT BREAKDOWN header in this video block
vblock_new = re.sub(
    r"(SHOT BREAKDOWN \(timed[^\n]*\):\n)(?:- \[00:00[^\n]*\n- \[00:02[^\n]*\n- \[00:04[^\n]*)",
    lambda mm: mm.group(1) + beats, vblock, count=1)
region = region[:va] + vblock_new + region[vb:]

# ---- brief Movement + Identity safety -------------------------------------
lm_sentence = (f" The Look A\u2192Look B change ({la} \u2192 {lb}) is contained MID-CLIP inside Frame {K} "
               f"at a HELD angle \u2014 Veo first/last-frame continuity (Frame {K} image = Look A = first "
               f"frame, Frame {K+1} image = Look B = last frame); every frame join is a hard match-cut to "
               f"a new angle.")
region = re.sub(r"(^Movement:[^\n]*?)(\s*)$",
                lambda mm: mm.group(1) + ("" if mm.group(1).rstrip().endswith(('.', '!')) else ".") + lm_sentence,
                region, count=1, flags=re.M)

ident = (f"Identity safety: the change is contained inside the single Frame-{K} transform clip \u2014 it "
         f"OPENS on the recognizable pre-transform face + {la} (Look A) and RESOLVES smoothly "
         f"to the {lb} (Look B, new AND clearly her) by clip-end; the {change} covers only the "
         f"mid-clip crossing at a held angle; only the named transform is impossible, all light and "
         f"fabric obey real physics.")
region = re.sub(r"^Identity safety:[^\n]*$", lambda _ : ident, region, count=1, flags=re.M)

# ---- write back ------------------------------------------------------------
text = text[:r_start] + region + text[r_end:]
open(path, "w", encoding="utf-8").write(text)

# ---- report ----------------------------------------------------------------
sb = region.count("SHOT BREAKDOWN (timed")
vp = region.count("\u2014 VIDEO PROMPT")
cut1 = region.count("Cut to ")
residue = [p for p in ("START KEYFRAME (locked)", "END KEYFRAME (locked)", "mid-transform",
                       "the diagonal pour-line", "light-seam dividing", "beginning the transform gesture")
           if p in region]
print(f"CONCEPT {N}: transform frame F{K}/{F}; SB={sb} VP={vp} 'Cut to'={cut1}; "
      f"residue={residue if residue else 'none'}")
print(f"  LookA={lookA[:40]!r} change={change!r} LookB={lookB[:40]!r} world={world!r}")

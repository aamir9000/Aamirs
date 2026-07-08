#!/usr/bin/env python3
"""Mechanically convert one frame of one concept into a PURE-ENVIRONMENT / no-subject
frame. Scoped by concept header + frame header so the many non-unique lines
(IDENTITY, NEGATIVE, LIP-SYNC ...) are handled safely by position.

It only does the *mechanical* removals/neutralisations that are identical for
every concept. The concept-specific narrative lines (SCENE NOTE, VISUAL-LEAD,
FRAMING, SHOT TYPE, SHOT BREAKDOWN, SPATIAL LOGIC, KINETIC, MICRO-MAGIC, TEXTURE,
PHYSICS, CONTINUITY, AUDIO) are left for hand editing afterwards.

Usage: python3 _tools/subject_free.py <concept_num> <frame_num>
"""
import re
import sys

FILE = "CONCEPTS/Surreal/NEW Reel Concepts (131\u2013150) .txt"

SUBJECT_LABELS = (
    "WARDROBE:", "FOOTWEAR:", "ACCESSORIES:", "HAIR:", "MAKEUP:",
    "EYE COLOUR:", "HANDS & NAILS:", "FACIAL MICRO-DYNAMICS:",
    "BODY POSTURE & WEIGHT:",
)

DIRECTIVE = ("PURE ENVIRONMENT \u2014 NO SUBJECT IN FRAME: this is a world-only shot; "
            "Aira does NOT appear (no person, no figure, no silhouette, no body, no hands). "
            "Render only the environment, its objects and the magic cue. "
            "Disregard any subject/wardrobe/pose wording elsewhere.")

VIDEO_NOSUBJ = ("NO SUBJECT (locked): this is a pure-environment frame \u2014 no person, no figure, "
                "no silhouette, no body, hands or face appear; render the world and its objects only. "
                "Identity lock is N/A because Aira is absent from this shot.")

def main():
    concept = int(sys.argv[1])
    frame = int(sys.argv[2])
    with open(FILE, encoding="utf-8") as fh:
        lines = fh.readlines()

    # concept block
    cstart = None
    cend = len(lines)
    for i, ln in enumerate(lines):
        if ln.startswith(f"# CONCEPT {concept} "):
            cstart = i
            break
    if cstart is None:
        sys.exit(f"concept {concept} not found")
    for i in range(cstart + 1, len(lines)):
        if lines[i].startswith("# CONCEPT "):
            cend = i
            break

    img_hdr = re.compile(rf"^## Frame {frame} of \d+ \u2014 IMAGE PROMPT")
    vid_hdr = re.compile(rf"^## Frame {frame} of \d+ \u2014 VIDEO PROMPT")
    nxt_hdr = re.compile(r"^## Frame \d+ of \d+ \u2014 ")

    img_s = vid_s = blk_e = None
    for i in range(cstart, cend):
        if img_hdr.match(lines[i]):
            img_s = i
        elif vid_s is None and img_s is not None and vid_hdr.match(lines[i]):
            vid_s = i
        elif vid_s is not None and nxt_hdr.match(lines[i]):
            blk_e = i
            break
    if img_s is None or vid_s is None:
        sys.exit(f"frame {frame} blocks not found in concept {concept}")
    if blk_e is None:
        blk_e = cend

    out = []
    for i, ln in enumerate(lines):
        # ---- IMAGE block ----
        if img_s < i < vid_s:
            stripped = ln.strip()
            if any(stripped.startswith(lbl) for lbl in SUBJECT_LABELS):
                continue  # drop subject-only field line
            if stripped.startswith("IDENTITY LOCK: Aira ["):
                out.append("IDENTITY LOCK: N/A \u2014 no person in this frame (pure environment); no reference sheet applies.\n")
                out.append("\n")
                out.append(DIRECTIVE + "\n")
                continue
        # ---- VIDEO block ----
        if vid_s < i < blk_e:
            stripped = ln.strip()
            if stripped.startswith("IDENTITY (locked): Aira "):
                out.append(VIDEO_NOSUBJ + "\n")
                continue
            if stripped.startswith("LIP-SYNC:"):
                out.append("LIP-SYNC: N/A \u2014 no person, mouth or voice in this pure-environment frame.\n")
                continue
            if stripped.startswith("FACIAL CONSISTENCY / IDENTITY LOCK:"):
                out.append("FACIAL CONSISTENCY / IDENTITY LOCK: N/A \u2014 no person, face or eyes in this pure-environment frame.\n")
                continue
            if stripped.startswith("NEGATIVE:"):
                out.append("NEGATIVE: any person, figure, human silhouette, body, hands or face; identity drift; "
                           "mirrored/flipped frame; slow-motion; watermark; empty white or flat background; blown highlights; plasticky CGI.\n")
                continue
        out.append(ln)

    with open(FILE, "w", encoding="utf-8") as fh:
        fh.writelines(out)
    print(f"concept {concept} frame {frame}: mechanical subject-free done "
          f"(img {img_s+1}-{vid_s}, vid {vid_s+1}-{blk_e})")

if __name__ == "__main__":
    main()

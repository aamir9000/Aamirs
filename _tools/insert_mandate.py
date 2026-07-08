#!/usr/bin/env python3
"""
insert_mandate.py — insert the STRICT COLOUR & RENDER MANDATE at the top of every prompt block.

Auto-detects format per file:
  * If the file uses 'Image Prompt' / 'Video Prompt' headers  -> insert after each such header
    (one mandate per image prompt and per video prompt = every prompt).
  * Else (set4 / action '--- FRAME k ---' style)              -> insert after each FRAME header
    (one mandate per frame, covering its image+video).

The mandate reinforces render QUALITY only (crisp/fresh/clean colour, rich sky, deep sea-blue
water, clean blacks, natural skin, clean composition, honour intended coverage / no unwanted
revealed edges, no AI artifacts). It explicitly does NOT override the composition / camera /
lens / wardrobe / action / identity coded in the fields — it never contradicts a coded value.

Idempotent: if the mandate already follows an anchor, it is not inserted again.
Usage: python3 _tools/insert_mandate.py "<file>"
"""
import sys, io, re

SIG = "STRICT COLOUR & RENDER MANDATE"
MANDATE = (
 "STRICT COLOUR & RENDER MANDATE (must be followed exactly; this governs render QUALITY only and "
 "must NOT change the composition, camera, lens, framing, wardrobe, action or identity specified "
 "above): render the colours already specified at their richest, freshest, cleanest and most "
 "premium — crisp, vivid and luminous with elegant, controlled saturation; never dull, faded, "
 "washed-out, muddy, grey or flat. Hold deep-but-clean blacks, luminous full mid-tones and "
 "beautiful highlight roll-off with high dynamic range and no blown highlights. Wherever sky is "
 "visible, render it richly graded and cinematic — never empty, white or overexposed. Wherever "
 "water is visible, render it crystal-clear with deep sea-blue and turquoise gradients, clean "
 "caustics and sparkling reflections — never grey or murky (unless the concept explicitly "
 "specifies dark / ink / obsidian water, which stays deep, glassy and clean). Protect natural, "
 "true skin tone; never push saturation onto the face. Keep the image immaculately clean and "
 "premium with clear figure-to-ground separation so the hero reads first; honour the concept's "
 "intended dominant surface and full-frame coverage, and do NOT reveal unwanted structural edges, "
 "seams, side-walls or empty dead space that break the intended composition. Photoreal, "
 "award-winning editorial finish — no AI artifacts, plastic or waxy skin, dead eyes, malformed "
 "hands or unfinished backgrounds."
)

HEADER = re.compile(r"\b(?:image|video)\s+prompt\b", re.I)
FRAME  = re.compile(r"^\s*(?:-{2,}|—|#{1,6})\s*frame\b", re.I)

def process(path):
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    use_headers = any(HEADER.search(l) for l in lines)
    nl = "\n"
    out, n = [], 0
    for idx, ln in enumerate(lines):
        out.append(ln)
        anchor = HEADER.search(ln) if use_headers else FRAME.match(ln)
        if not anchor:
            continue
        j = idx + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and SIG in lines[j]:
            continue                       # already present -> idempotent
        out.append(MANDATE + nl)
        n += 1
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print(f"{path}: inserted {n} mandate lines ({'header' if use_headers else 'frame'} mode)")

def main():
    if len(sys.argv) != 2:
        print("usage: insert_mandate.py <file>"); sys.exit(2)
    process(sys.argv[1])

if __name__ == "__main__":
    main()

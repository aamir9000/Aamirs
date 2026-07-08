#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEAN-STRIP engine — Veo-optimised the VIDEO prompts only (image prompts untouched).
Per steering decision: the start still already carries wardrobe/lighting/spatial/identity,
so the video prompt should be lean — motion + camera + transform + expression + audio.

Within each VIDEO-PROMPT block this:
  1. replaces the long `IDENTITY & CHARACTER-CONSISTENCY LOCK:` paragraph with a SHORT identity line,
  2. removes the standalone `LIGHTING:` line (static — the image prompt carries it),
  3. removes the `ENVIRONMENT:` line (static — the image prompt carries it),
  4. trims the long video `NEGATIVE:` line to a few Veo-friendly terms.
IMAGE-PROMPT blocks (FRAMING/SUBJECT FRAMING/LIGHTING/NEGATIVE etc.) are LEFT FULLY INTACT.

Scoped strictly to lines inside a `... VIDEO PROMPT` section (until the next ###/##/---/MASTER
header). Files without these fields are passed through unchanged. Idempotent.

Usage:  python3 _tools/lean_strip.py "<path>"
"""
import re
import sys

SHORT_IDENTITY = (
    "IDENTITY (locked): Aira \u2014 same person every frame; face, bone structure, eye shape "
    "+ colour, nose, lips, skin texture and hair strictly locked to reference; ONLY expression, "
    "gaze and head move; no identity drift, no face/anatomy warp, no second or duplicate person."
)
SHORT_NEGATIVE = (
    "NEGATIVE: identity drift, face or hand warp, extra or fused fingers, duplicate person, "
    "mirrored/flipped frame, slow-motion, watermark."
)


def is_video_header(line):
    return bool(re.match(r"#+ .*VIDEO PROMPT", line))


def is_boundary(line):
    return (
        line.startswith("### ")
        or line.startswith("## ")
        or line.startswith("---")
        or line.startswith("MASTER TRACK")
        or line.startswith("MASTER AUDIO")
    )


def process(text):
    lines = text.split("\n")
    out = []
    in_video = False
    n_id = n_lt = n_env = n_neg = 0
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if is_video_header(line):
            in_video = True
            out.append(line)
            i += 1
            continue
        if in_video and is_boundary(line):
            in_video = False  # this boundary line is appended normally below
        if in_video:
            if line.startswith("IDENTITY & CHARACTER-CONSISTENCY LOCK:"):
                out.append(SHORT_IDENTITY)
                n_id += 1
                i += 1
                continue
            if line.startswith("LIGHTING:"):
                n_lt += 1
                i += 1
                if i < n and lines[i].strip() == "":
                    i += 1
                continue
            if line.startswith("ENVIRONMENT:"):
                n_env += 1
                i += 1
                if i < n and lines[i].strip() == "":
                    i += 1
                continue
            if line.startswith("NEGATIVE:"):
                out.append(SHORT_NEGATIVE)
                n_neg += 1
                i += 1
                continue
        out.append(line)
        i += 1
    return "\n".join(out), (n_id, n_lt, n_env, n_neg)


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    text, (n_id, n_lt, n_env, n_neg) = process(text)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(
        f"{path}: shortened {n_id} identity locks, removed {n_lt} LIGHTING + {n_env} "
        f"ENVIRONMENT lines, trimmed {n_neg} video NEGATIVE lines"
    )


if __name__ == "__main__":
    main()

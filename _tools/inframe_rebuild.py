#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild the AIRA Special-Concept volumes into the new IN-FRAME layout.

OLD per concept:
  ## INGREDIENTS + LOCKS  (@subject / @object / THE PLACE / ELEMENT / TRICK / HERO / Footing)  [meta, outside frames]
  ### FRAME n
    **Frame angle:** ...
    **ENVIRONMENT still (the only per-frame ingredient):** ... *(Animate ...)*
    **VIDEO PROMPT:**
      - *Facial consistency + expression (identity-safe):* ...
      - *Animation:* ...
      - *AUDIO (in-frame):* ...

NEW per concept (everything operative lives INSIDE the frame prompts):
  ### FRAME 1
    **Subject prompt** (generate once ...): <@subject body>
    **Object prompt**  (generate once ...): <@object body>          # only if a 2nd @-ingredient exists
    **Environment prompt:** <env body, scene only>
    **Video prompt:** <facial> <animation incl physics+9:16+framing> Sound (diegetic): <audio>
  ### FRAME 2+  -> Environment prompt + Video prompt only (subject/object stated once in F1)

The INGREDIENTS meta block is dropped (its @subject/@object move into F1; the
element/trick/hero/footing notes are already written into each video prompt).
Logline / Arc / MASTER AUDIO / Stills-to-generate are kept untouched.

Idempotent: a concept with no `## INGREDIENTS` block is skipped.

Usage:  python3 _tools/inframe_rebuild.py "<path>"
"""
import re
import sys

SUBJ_LABEL = "**Subject prompt** (generate once \u00b7 reuse as the subject image in every frame \u00b7 plain blank background \u00b7 no text/labels): "
OBJ_LABELS = {
    "object": "**Object prompt** (generate once \u00b7 reuse every frame \u00b7 plain blank background \u00b7 no text/labels): ",
    "product": "**Product prompt** (generate once \u00b7 reuse every frame \u00b7 plain blank background \u00b7 no text/labels): ",
    "texture": "**Texture/material prompt** (generate once \u00b7 plain blank background \u00b7 no text/labels): ",
}

ING_RE = re.compile(r"## INGREDIENTS \+ LOCKS.*?\n\n(?=---\n### FRAME 1)", re.DOTALL)
INGREDIENT_LINE_RE = re.compile(
    r"- \*\*`@(?P<name>\w+)`[^\n]*?\):\s*(?P<body>[^\n]*)"
)
FRAME_ANGLE_RE = re.compile(r"(?m)^\*\*Frame angle:\*\* [^\n]*\n")
ENV_RE = re.compile(r"(?m)^\*\*ENVIRONMENT[^:]*:\*\* (.*)$")
VIDEO_RE = re.compile(
    r"(?m)^\*\*VIDEO PROMPT:\*\*\n"
    r"- \*Facial consistency \+ expression \(identity-safe\):\* (.*)\n"
    r"- \*Animation:\* (.*)\n"
    r"- \*AUDIO \(in-frame\):\* (.*)$"
)
TRAIL_ITALIC_RE = re.compile(r"\s*\*\(?[^*]+?\)?\*\s*$")


def transform_concept(region, tag):
    if "## INGREDIENTS" not in region:
        return region, False  # already converted / nothing to do

    # 1. pull @subject + (object/product/texture) bodies out of the ingredients block
    ing_block = ING_RE.search(region)
    assert ing_block, f"{tag}: no ingredients block end found"
    ingredients = INGREDIENT_LINE_RE.findall(ing_block.group(0))
    assert ingredients and ingredients[0][0] == "subject", f"{tag}: subject not first"
    subject_body = ingredients[0][1].strip()
    extra = [(n, b.strip()) for (n, b) in ingredients[1:] if n in OBJ_LABELS]

    # 2. drop the whole ingredients meta block (keep the --- before FRAME 1)
    region = ING_RE.sub("", region)

    # 3. drop the standalone Frame angle lines (vantage+light already live in the
    #    environment prompt and the video framing note)
    region, n_angle = FRAME_ANGLE_RE.subn("", region)

    # 4. relabel ENVIRONMENT still -> Environment prompt (scene only: strip the
    #    trailing *(Animate ...)* / *element* italic note so the still has no subject)
    def env_repl(m):
        body = TRAIL_ITALIC_RE.sub("", m.group(1)).rstrip()
        return f"**Environment prompt:** {body}"

    region, n_env = ENV_RE.subn(env_repl, region)

    # 5. fold the VIDEO PROMPT triple into one Video prompt paragraph
    def vid_repl(m):
        facial, anim, audio = (g.strip() for g in m.groups())
        return f"**Video prompt:** {facial} {anim} Sound (diegetic): {audio}"

    region, n_vid = VIDEO_RE.subn(vid_repl, region)

    # 6. inject Subject (+Object) prompts into FRAME 1 (before its Environment prompt)
    inject = SUBJ_LABEL + subject_body + "\n"
    for name, body in extra:
        inject += OBJ_LABELS[name] + body + "\n"
    region, n_inj = re.subn(
        r"(?m)^(\*\*Environment prompt:\*\*)", inject + r"\1", region, count=1
    )

    assert n_angle == n_env == n_vid, (
        f"{tag}: counts differ angle={n_angle} env={n_env} vid={n_vid}"
    )
    assert n_inj == 1, f"{tag}: frame-1 injection failed ({n_inj})"
    print(f"{tag}: frames={n_vid} object_ingredients={len(extra)} angle_lines_dropped={n_angle}")
    return region, True


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    parts = re.split(r"(?m)^(?=# SC)", text)
    out = []
    converted = 0
    for part in parts:
        if part.startswith("# SC"):
            tag = part.splitlines()[0].strip()
            part, did = transform_concept(part, tag)
            converted += int(did)
        out.append(part)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("".join(out))
    print(f"\nDONE: {converted} concepts converted in {path}")


if __name__ == "__main__":
    main()

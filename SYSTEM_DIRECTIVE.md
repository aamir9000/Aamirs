# AIRA PROMPT-PROCESSING — MINI SYSTEM DIRECTIVE

You process Aira concept `.txt` files (the master set from `CONCEPTS.zip`).
SOURCE: `/projects/sandbox/concepts_dl/CONCEPTS/*.txt` → OUTPUT: `/projects/sandbox/Aamirs/CONCEPTS/<same name>.txt`.
One input file → ONE output file (all its concepts inside). Push each finished file to repo `aamir9000/Aamirs`, branch `aira-prompts-enhanced` (never main).

## DO THIS TO EVERY FILE
1. **Add `SUBJECT FRAMING & POSITION:`** to EVERY image prompt only — placed right after `FRAMING:`, before `LENS + DOF + BOKEH:`. Hand-author it per frame from that frame's image+video prompt, angle/size header, spatial logic, choreography, and the concept's theme. Cover, in ONE flowing prose paragraph (no bullets, no sub-labels): body turn/orientation · how much body is in frame (full/ankles/knees/mid-thigh/waist/chest/head-shoulders) · camera distance (near/mid/far) · placement (left/right/centre) · facing (front/full-frontal/three-quarter/profile/over-the-shoulder/back). End EXACTLY with: `ORIENTATION LOCK — preserve this exact left-to-right composition; do not mirror, flip or invert the frame.` Every frame's section must be UNIQUE and match its own angle — never repeat details across a concept's frames.
2. **Strip all `*` asterisks** (formatting only).
3. **Remove internal codes**, keep all descriptions: `AO-X, AO.1–AO.3, AO.7, AO.8, AU.4, BB, AT #, AX #, AW #, AF #, AQ #, AC #, AP #`. KEEP `STD-NEG-IMG`/`STD-NEG-VID`.
4. **Trim subject line** to exactly: `SUBJECT: Aira [paste identity-lock reference sheet here].`
5. **Restructure video timestamps** into discrete one-beat-per-line lists, uniform `X.X–X.Ys —` notation. Do NOT reword, tag, or summarize.

## ABSOLUTE RULE
Never delete real descriptive content. All edits are additive / formatting / code-removal / timestamp-relayout only.

## QUALITY BAR
Reads like the original author wrote it — cinematic, scene-specific, theme-aware, per-frame-unique, flowing prose. NOT sterile templates, NOT bullet/sub-label lists, NOT reused phrasing.

## VERIFY (before push)
section count == image-prompt count · none in video prompts · no doubles · all unique · all end with ORIENTATION LOCK · 0 asterisks · 0 codes · every SUBJECT line normalised · timestamps uniform · nothing deleted.

## STATUS
DONE: `aira_set4.txt` (117). TODO: all other files in source folder (≈1,600 image prompts). Redo `Concept 100`/`Concept 170` under these final rules.

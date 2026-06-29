# Special Concepts — Ingredient Mode (Google Flow / Veo 3.1)

This folder holds **ingredient-mode** versions of our concepts, reformatted for Google Flow's
**Ingredients-to-Video** workflow. They are derived from the master prompt files in `/CONCEPTS`
(do not edit the masters here — this folder is the Flow-ready delivery copy).

## What "ingredient mode" means
Instead of pure text-to-video, Flow animates a small set of **reference images ("ingredients")**
while following the text prompt, so identity / product / world / look do not drift.

- Veo 3.1 accepts roughly **3 reference images** per generation.
- Native **9:16 vertical** output (matches our reels).
- In Flow you drag the reference images in, then reference them in the prompt box with `@name`.

## Method: essence-continuation with cuts (NOT literal continuation)
Each shot is its own **new camera setup** — different angle, size, move, perspective — and we **cut**
between them. Continuity is the *essence*, carried by: same Aira + wardrobe + world + light across
shots, and the **momentum of the action** flowing across the cut (match-on-action), like real editing.
We do **not** chain end-frame→start-frame (that would morph, not cut).

## Mode: Ingredients-to-Video — 3 reference images per clip (built to Flow's own spec)
Google's guidance: provide **subject / product references on a plain or segmented background**, and
**describe in the prompt how each ingredient should be used.** So each ingredient is a **clean, isolated
single element — NOT a busy composite.** Composition / framing / action live in the **prompt**, not in the
images. Each clip we hand Flow 3 references:

| Slot | What it is | How to BUILD the still (Nano Banana Pro) | Carries |
|---|---|---|---|
| **SUBJECT** `@aira` | Aira in this shot's pose/wardrobe/hair | **isolated on a plain / segmented neutral background**, full figure, clean hands, **even lighting matched to the world's light**, high-res, 9:16; rendered from her identity reference | identity + wardrobe + pose |
| **WORLD** `@world` | this frame's location, **no subject** | a full scene carrying that beat's light + palette | place + light |
| **PROP / LOOK** `@prop` / `@look` | the hero prop **isolated on plain bg**, OR a clean palette/grade/light swatch | locks the object, or the colour-grade & mood | prop or grade |

> Identity is locked **upstream** — every SUBJECT still is rendered from Aira's reference, so she's the same
> person before Flow animates her. The 3 refs then hold subject + world + look steady across the cut.
> **The PROMPT does the composition:** name how to combine them ("`@aira` rides the `@bike` through
> `@world` …") + crop, angle, ONE dominant camera move, her per-limb action + expression, the signature —
> written as **timed beat-ranges** ([00:00–00:02] / [00:02–00:04] / [00:04–00:06]).
> **Match the SUBJECT still's lighting to the WORLD still's** or the cut-out reads fake.
> Pipeline: Nano Banana Pro renders the 3 stills (isolated subject + scene + prop/look) → load as
> Ingredients → the timed 6s prompt drives the beat → cut to the next → consistency held by refs + momentum.

> **Exact-composition beats** (e.g. the carve) can instead be run as **Frames-to-Video** (a composite
> start frame) — a *separate* mode from Ingredients, picked per clip when precise A→B framing matters.

## Performance rule: candid, alive — never a frozen pose
Keep **identity** constant (same person; face/build/hair fixed, only gaze/head/soft expression animate),
but **do not freeze the body.** In every clip the subject behaves like a real person, not a model holding
a pose — natural varied micro-actions appropriate to the beat (glancing around, shifting weight, adjusting
grip/hair, a breath/laugh/grin, a free hand, etc.), and a **different** combination of natural actions in
each shot. This is what makes the motion read natural rather than stiff.

## How each ingredient-mode file is laid out
- One concept per file.
- An `INGREDIENTS` block at the top (what to upload + the `@name` to give each).
- One `SHOT` block per frame: which ingredients to attach, the paste-ready VIDEO prompt
  (real-time, natural speed, identity-safe), and the handoff into the next shot.

See `_TEMPLATE.md` for the exact shot-card structure.


## STANDING RULES FOR EVERY SPECIAL CONCEPT (locked with SC-01)
1. **Different per concept:** environment, lighting scheme, wardrobe, and hairstyle are unique to each
   concept — never reused between concepts. Shot grammar (crop/angle/camera/pose) also never repeats
   across concepts.
2. **Wardrobe:** amazing + colourful + cute, premium fit; **constant within a concept** (one journey),
   different for each concept. Define HANDS & NAILS too.
3. **Hairstyle:** one distinct style per concept, constant within it.
4. **Progressing worlds:** within a concept the world is a continuous journey — each frame's WORLD is the
   believable *next place* after the previous frame's, with the light evolving naturally as she travels.
   (So the WORLD ingredient changes every frame; identity/wardrobe/hair/palette stay constant.)
5. **Full per-limb pose, every frame:** spell out gaze, neck, head, each shoulder, each arm→hand→fingers,
   waist, hips, each leg, feet (+ weight) — a held POSE block + the motion in the video prompt.
6. **Different expression every frame** (and across the set).
7. **Same prompt-detailing depth as the master /CONCEPTS files** (rich per-still description + timed
   SHOT BREAKDOWN beats), plus: controlled vibrancy (skin protected), real-time motion (no slow-mo),
   identity fixed but body never frozen (candid real movement), one grounded-surreal signature, 9:16, loops.
8. **Ingredient stills are CLEAN & ISOLATED (Flow's spec):** SUBJECT on a plain/segmented neutral
   background (lit to match the world); WORLD as a full scene with no subject; 3rd = prop isolated on plain
   bg OR a palette/grade swatch. Never a busy composite — composition lives in the prompt. Exact-composition
   beats may run as Frames-to-Video (composite start frame) instead.
9. **Video-prompt motion style:** write **timed beat-ranges** ([00:00–00:02] / [00:02–00:04] /
   [00:04–00:06]) — not free prose — to budget the action and stop Veo rushing/padding. **One dominant
   camera move per clip** (don't chain orbit→pull-back in one 6s shot) and **only ~2–3 actions per clip**;
   over-stuffing makes the model drop or cram beats.

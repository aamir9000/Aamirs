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

## Mode: Ingredients-to-Video — 3 images per clip
Flow lets us hand **3 reference images** to each clip. We spend them as:
| Slot | Image (generated per shot in Nano Banana Pro) | Carries |
|---|---|---|
| **SUBJECT** | Aira in *this shot's* pose & angle (from her identity-lock reference) | identity + wardrobe |
| **WORLD** | the environment for this beat, no subject | location + light |
| **COMPOSITE / look anchor** | the framed look of this beat | palette + composition |

> Identity is locked **upstream** — every SUBJECT/COMPOSITE still is rendered from Aira's reference in
> Nano Banana Pro, so each is already the same Aira before Flow animates it. Flow's 3 ingredients then
> hold subject + world + look steady across the cut.

> Pipeline: **Nano Banana Pro renders the 3 stills per shot → load as Ingredients (subject + world +
> composite/look) → the 6s prompt drives the motion of that beat → cut to the next beat (new angle),
> consistency held by the ingredients + carried action momentum.**

> (Frames-to-Video — start+end keyframe — is the alternative mode, used only when one shot needs a tight
> internal A→B move. It is a separate mode from Ingredients, so per clip we pick one.)

## How each ingredient-mode file is laid out
- One concept per file.
- An `INGREDIENTS` block at the top (what to upload + the `@name` to give each).
- One `SHOT` block per frame: which ingredients to attach, the paste-ready VIDEO prompt
  (real-time, natural speed, identity-safe), and the handoff into the next shot.

See `_TEMPLATE.md` for the exact shot-card structure.

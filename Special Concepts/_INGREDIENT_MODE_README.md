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

## Our fixed ingredient recipe (per shot)
| Slot | Ingredient | Source |
|---|---|---|
| `@aira` | Aira identity-lock reference (face / build / hair) — **required every shot** | character ref sheet |
| `@product` | the hero product / signature prop for the concept | the concept's hero-product still |
| `@world` | the location + colour/style look (palette, set, grade) | a Nano Banana Pro establishing still from that concept |

> Pipeline: **Nano Banana Pro renders the per-frame stills → those stills become the Flow Ingredients → our VIDEO prompt drives the 6s motion → `FRAME-JOIN HANDOFF` chains the shots into the full reel.**

## How each ingredient-mode file is laid out
- One concept per file.
- An `INGREDIENTS` block at the top (what to upload + the `@name` to give each).
- One `SHOT` block per frame: which ingredients to attach, the paste-ready VIDEO prompt
  (real-time, natural speed, identity-safe), and the handoff into the next shot.

See `_TEMPLATE.md` for the exact shot-card structure.

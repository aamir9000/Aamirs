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
between them. Continuity is the *essence*, carried by: the same subject + wardrobe + world + light across
shots, and the **momentum of the action** flowing across the cut (match-on-action), like real editing.
We do **not** chain end-frame→start-frame (that would morph, not cut).

## Mode: Ingredients-to-Video — 3 reference images per clip (built to Flow's own spec)
Google's guidance: provide **subject / product references on a plain or segmented background**, and
**describe in the prompt how each ingredient should be used.** So each ingredient is a **clean, isolated
single element — NOT a busy composite.** Composition / framing / action live in the **prompt**, not in the
images. Each clip we hand Flow 3 references:

| Slot | What it is | How to BUILD the still (Nano Banana Pro) | Carries |
|---|---|---|---|
| **SUBJECT** `@subject` | the subject in this shot's pose/wardrobe/hair | **isolated on a plain / segmented neutral background**, full figure, clean hands, **even lighting matched to the world's light**, high-res, 9:16; rendered from her identity reference | identity + wardrobe + pose |
| **WORLD** `@world` | this frame's location, **no subject** | a full scene carrying that beat's light + palette | place + light |
| **PROP / LOOK** `@prop` / `@look` | the hero prop **isolated on plain bg**, OR a clean palette/grade/light swatch | locks the object, or the colour-grade & mood | prop or grade |

> Identity is locked **upstream** — every SUBJECT still is rendered from the subject's reference, so she's the same
> person before Flow animates her. The 3 refs then hold subject + world + look steady across the cut.
> **The PROMPT does the composition:** name how to combine them ("`@subject` rides the `@bike` through
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


---

# SESSION-RESILIENT PLAYBOOK
*(everything needed to keep building these in a fresh chat if context is lost)*

## Naming convention (Veo-facing — important)
Veo only reads the **uploaded reference image**, not a name. So in every prompt we call her **`@subject`**
(= our locked model reference / the "Aira" character sheet) and describe her as **"the subject" / "a young
woman."** Never write the character's name into a Veo prompt. Ingredient labels are always generic:
**`@subject` · `@world` · `@prop` · `@look`.** (No physical enumeration of her — likeness is carried only by `@subject`.)

## Prompt-detailing format (reusable — write every video prompt like this)
1. **INGREDIENTS line:** `@subject` (isolated rider) · `@world` (scene) · `@look` (palette swatch) [+ `@prop` if used].
2. **Combine instruction:** "Animate `@subject` riding/…/ through `@world`, graded to `@look`."
3. **Shot:** crop + angle + **ONE dominant camera move.**
4. **Timed beats** — 3 ranges, ~2–3 actions total: `[00:00–00:02] … [00:02–00:04] … [00:04–00:06] …`
   (already-in-motion start; candid real movement; the per-limb actions; the signature on its beat).
5. **Rails (end of prompt):** hold `@subject`'s identity exactly (same face/build/hair; only gaze/head/expression
   move; never warp the face); real-time natural speed, no slow-motion; believable physics; the lighting +
   controlled vibrancy + natural skin tone; **9:16 vertical.**

**Worked sample (SC-01 · Shot 3 — the carve):**
> Animate `@subject` riding her cream bicycle through `@world`, graded to `@look`. Low three-quarter hero from inside the turn; one continuous orbit arcing around her. [00:00–00:02] she banks into a hard carving lean — inside LEFT knee dropping toward the road, both hands gripping the bars, hips to the outside saddle-edge, a sharp focused breath. [00:02–00:04] at the apex her slipstream blooms — blush-and-white blossom petals + bright sunlit light-motes with a soft prism shimmer spiral off the wheels, grounded in real spin/air physics (weighty petals, clean speculars, no cartoon sparkle). [00:04–00:06] she powers upright with a quick triumphant grin as the orbit settles to her front, the petal-wake streaming over the sparkling canal. Hold `@subject`'s identity exactly — same face/build/hair, only gaze/head/expression change, never warp the face. Real-time, no slow-motion. Believable lean and tyre grip. Bright high-midday daylight, controlled vibrancy, natural skin tone. 9:16.

## BUILT CONCEPTS REGISTRY
*(one entry per fully-built concept — difference string + theme + format + file, so a fresh session can pick up)*

### SC-01 · PETAL SLIPSTREAM (Bicycle) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** bicycle ride · journey **boulevard → market → canal bridge → seafront** · signature = **blossom-petal + sunlit-light wake** (peaks on the carve) · energy **bright-joyful** · light **bright morning → midday** · wardrobe **marigold/coral puff-sleeve colour-block sundress** · hair **sky-blue ribbon ponytail** · shot-grammar **low-hero crane / profile track / inside-orbit carve / hero push-in**.
- **THEME:** one girl, one cute outfit, one continuous daytime ride where the world opens grander each beat; candid real movement; one grounded-surreal petal-light bloom.
- **CONCEPT:** 4×6s ingredient-mode cut reel, progressing worlds, loops Shot 4 → Shot 1.
- **PROMPT FORMAT:** as above (`@subject` + `@world` + `@look`, timed beats, one camera move, identity-locked).
- **FILE:** `SC-01 · Petal Slipstream (Bicycle).md`

### SC-02 · RIVIERA DRIFT (Vespa) — **STATUS: BUILT** · 5 shots × 6s · SILENT
- **DIFFERENCE STRING:** pastel Vespa ride · journey **town square → bougainvillea lane → sea-reveal switchback → harbour quay → piazza overlook** · signature **golden sun-glints + sea-haze light-ribbon** (light-led, not petals) · energy **breezy glamour** · light **golden-hour Mediterranean (warming)** · wardrobe **tangerine-stripe halter midi + lemon silk headscarf** · hair **soft waves under headscarf** · shot-grammar **aerial-pan / low ground-track / bike-mounted ride-along / over-shoulder / crane pull-back**.
- **THEME:** a glamorous coastal descent to the sea; light-led signature; candid. **FILE:** `SC-02 · Riviera Drift (Vespa).md`

### SC-06 · MARKET DASH (Run) — **STATUS: BUILT** · 5 shots × 6s · SILENT
- **DIFFERENCE STRING:** run/weave · journey **flower bazaar → spice arcade → fabric souk → fruit & lantern lane → fountain square** · signature **colour-burst (petals + sun-caught spice-dust + fabric/bunting)** · energy **fast joyful chaos** · light **dappled bright mid-morning → open square** · wardrobe **gingham crop + butter culottes** · hair **double space-buns** · shot-grammar **top-down boom / over-shoulder track-behind / whip-pan half-orbit / parallel profile / CU→pull-out**.
- **THEME:** a joyful sprint-weave through a bursting bazaar; colour lifts in her wake. **FILE:** `SC-06 · Market Dash (Run).md`

### SC-16 · BECOME THE BLOOM (Material → Couture) — **STATUS: BUILT** · 3 shots × 6s · SILENT
- **DIFFERENCE STRING:** walk + **wardrobe-transform** · journey **garden path → marble colonnade → fountain court** · signature **blossom-petal+light material BUILDS into a couture gown** (wardrobe transforms — the intentional exception) · energy **luxe metamorphosis** · light **soft luxe sun → bright key** · hair **sculptural low chignon** · **3rd ingredient = `@texture`** (not `@look`).
- **THEME:** most ingredient-native — a material becomes haute couture, grounded. **FILE:** `SC-16 · Become the Bloom (Material to Couture).md`

### SC-10 · LAGOON GLIDE (Paddleboard) — **STATUS: BUILT** · 5 shots × 6s · SILENT
- **DIFFERENCE STRING:** paddleboard · journey **open lagoon → mangrove channel → lotus field → sandbar shallows → open reef** · signature **sun-caustics + lotus-bloom + fish-flash** · energy **serene aqua** · light **bright aqua noon** · wardrobe **coral scalloped one-piece + turquoise floral sarong** · hair **wet-look top-knot** · shot-grammar **top-down overhead / water-line dolly / rising-through-surface boom / parallel profile / gentle orbit**.
- **THEME:** a calm-powerful turquoise glide; water-light signature. **FILE:** `SC-10 · Lagoon Glide (Paddleboard).md`

### SC-13 · SKY BLOOM (Hot-Air Balloon) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** hot-air balloon · journey **meadow lift-off → drift over village → through a cloud → above the clouds (sunrise)** · signature **cloud-wisps + dawn light-motes + breaking rays** (airy, light-led) · energy **tranquil wonder** · light **pastel dawn → sunrise gold** · wardrobe **lavender-peach ombré ruffle midi + cream cardigan** · hair **loose romantic waves** · shot-grammar **crane-up lift / aerial descend-orbit / push-in through wisps / hero push-in**.
- **THEME:** a dreamy dawn ascent into the sunrise; gentle airy signature. **FILE:** `SC-13 · Sky Bloom (Hot-Air Balloon).md`

## CONCEPT ROADMAP — difference strings (planned, not yet built)
*(rickshaw dropped; redundant 2nd-blossom dropped; each has a UNIQUE signature/energy/light)*
- **SC-02 Riviera Drift** — pastel Vespa · clifftop town→switchback→harbour→piazza · sea-spray + sun-glints · golden-hour Med · halter midi · silk-headscarf waves · 5 shots
- **SC-03 Boardwalk Bloom** — rollerblades · promenade→skate bowl→pier→beach steps · chalk-dust + balloons · high-key coastal noon · colour-block crop set · high space-buns · 4
- **SC-04 Golden Coast Cruise** — convertible · coast road→light-tunnel→bridge→cliff overlook · golden road-dust + flare-streaks · sunset amber/rose · retro scarf-dress + cat-eye · retro waves · 4
- **SC-06 Market Dash** — run/weave · flower bazaar→spice arcade→fabric souk→fountain square · colour-powder + spice-dust + fabric ripples · dappled mid-morning · tied-blouse + shorts · double buns · 5
- **SC-07 Rooftop Run** — parkour · rooftop gardens→clothesline maze→water-tank deck→edge leap · pigeon-burst + snapping flags · hard high-noon city · sporty-chic brights · sleek high pony · 4
- **SC-08 Petal Promenade** — editorial walk · blossom avenue→colonnade→garden stairs→reflecting pool · cherry-blossom storm (THE petal concept) · soft diffused overcast-pink · blush flowy couture · soft glam waves · 4
- **SC-09 Puddle Symphony** — walk/dance, rain-break · wet plaza→arcade→fountain→sun-break square · splash-crowns + prism-light · storm-silver→sun · glossy bright raincoat · slicked low pony · 4
- **SC-10 Lagoon Glide** — paddleboard · lagoon→mangrove channel→sandbar→open reef · caustics + lotus + fish-flash · bright aqua noon · swim-modest + sarong · wet top-knot · 5
- **SC-11 Gondola Reverie** — gondola · narrow canals→under bridges→grand canal→lagoon mouth · water-mirror reflections · soft golden Venice afternoon · vintage day-dress · braided updo + ribbon · 4
- **SC-12 Freediver's Bloom** — swim (vertical) · surface→reef→kelp cathedral→sun-shaft ascent · sun-shaft caustics + bubble-stream · underwater blue→gold · sleek dive-suit chic · slicked · 5
- **SC-13 Sky Bloom** — hot-air balloon · meadow lift-off→over rooftops→through a cloud→sunrise vista · cloud-wisps + dawn rays · pastel dawn · soft romantic dress · loose waves · 4
- **SC-14 Alpine Ascent** — cable-car/hike · meadow→pine forest→cliff path→summit lake · snow-sparkle + crystal-light · crisp cool alpine bright · camel/white/forest knit · fishtail braid + beanie · 4
- **SC-15 Kite Run** — run w/ giant kite · headland→dune ridge→cliff edge→sky-launch lean · colour-ribbons forming shapes · bright windy coast · primary playsuit · windswept high pony · 4
- **SC-16 Become the Bloom** — walk (material→couture) · garden path→colonnade→fountain court→hero plinth · a texture climbs and becomes her evolving gown · soft luxe sun · transforming gown · sculptural updo · 3
- **SC-17 Four Seasons, One Path** — walk/ride · same path spring→summer→autumn→winter · season re-skin transitions · light shifts per season · cute layered look · long loose hair · 5
- **SC-18 Portal Steps** — step through arches · flower arch→reef arch→desert arch→city arch · threshold world-swap bloom · light changes per portal · bold colour-block · sleek geometric bob · 3
- **SC-19 The Product Builds the World** — hero product→set · studio→liquid set→bloom set→hero plinth · world grows from the bottle (liquid→architecture) · luxe controlled light · couture · glossy · 3
- **SC-21 Citrus Coast** — Amalfi stroll · lemon grove→tiled stairs→harbour→terrace · citrus-leaf + zest-mist · bright lemon-sun · sundress · headscarf updo · 4

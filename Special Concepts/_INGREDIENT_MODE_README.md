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

### SC-03 · BOARDWALK BLOOM (Rollerblades) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** rollerblades · journey **palm promenade → pier boardwalk → skate bowl → beach steps** · signature **pastel chalk-dust + drifting balloons + light off the wheels** · energy **playful youthful** · light **high-key candy coastal noon** · wardrobe **colour-block crop + white skort + quad skates** · hair **bubble pigtail braids** · shot-grammar **track-behind / parallel profile / high-angle bowl orbit / hero push-in**.
- **THEME:** youthful candy-bright coastal skate; bowl-carve money shot. **FILE:** `SC-03 · Boardwalk Bloom (Rollerblades).md`

### SC-04 · GOLDEN COAST CRUISE (Convertible) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** vintage convertible · journey **coast highway → tree light-tunnel → cliff bridge → clifftop overlook** · signature **golden road-dust + lens-flare streaks** (light/dust-led) · energy **cinematic cool glamour** · light **sunset amber/rose (deepening)** · wardrobe **coral-cream chiffon scarf-dress + cat-eye + silk hair-scarf** · hair **voluminous retro waves** · shot-grammar **high aerial track / inside-car over-shoulder push / low parallel / crane pull-back**.
- **THEME:** cinematic sunset drive; strobing light-tunnel money shot. **FILE:** `SC-04 · Golden Coast Cruise (Convertible).md`

### SC-07 · ROOFTOP RUN (Parkour) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** parkour free-run · journey **rooftop garden → laundry maze → water-tank deck → edge leap** · signature **pigeon-burst + snapping flags/laundry + hard light** · energy **powerful athletic** · light **hard high-noon city** · wardrobe **coral crop + electric-blue leggings + white windbreaker** · hair **sleek slicked high pony** · shot-grammar **low-hero track-with / over-shoulder track-behind / whip-pan low wide / side-profile leap-arc**.
- **THEME:** powerful high-noon free-run; gap-leap money shot. **FILE:** `SC-07 · Rooftop Run (Parkour).md`

### SC-08 · PETAL PROMENADE (Editorial Walk) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** editorial runway walk · journey **blossom avenue → marble colonnade → garden stairs → reflecting pool** · signature **cherry-blossom storm + mirror-light** (THE petal concept) · energy **serene editorial elegance** · light **soft diffused overcast-pink** · wardrobe **blush chiffon cape-sleeve gown + pearls** · hair **soft glam half-up waves** · shot-grammar **low dolly-in / track-with / high descend-boom / hero push-in+pull-back**.
- **THEME:** poised blossom-world walk; pool blossom-whirl money shot. **FILE:** `SC-08 · Petal Promenade (Editorial Walk).md`

### SC-09 · PUDDLE SYMPHONY (Rain-Break) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** rain-break walk/dance · journey **wet plaza → sheltered arcade → fountain court → sun-break square** · signature **splash-crowns + clean rainbow-prism light** · energy **rain-break catharsis** · light **storm-silver breaking into warm sun** · wardrobe **marigold vinyl raincoat + polka dress + red wellies + clear umbrella** · hair **wet-look low pony** · shot-grammar **high overhead / parallel profile / low orbit / hero push-in+pull-back**.
- **THEME:** joyful rain-to-sun; sun-break puddle-stomp money shot. **FILE:** `SC-09 · Puddle Symphony (Rain-Break).md`

### SC-11 · GONDOLA REVERIE (Gondola) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** Venetian gondola (seated passenger) · journey **side canals → under a bridge → grand canal → lagoon mouth** · signature **water-mirror reflections + drifting golden light + petals** · energy **dreamy vintage** · light **soft golden Venice afternoon (warm/muted)** · wardrobe **emerald vintage day-dress + gloves + lace parasol + pearls** · hair **braided ribbon updo** · shot-grammar **high descend / water-line dolly-through / parallel profile / crane pull-back**.
- **THEME:** dreamy canal glide; bridge→grand-canal reveal money shot. **FILE:** `SC-11 · Gondola Reverie (Gondola).md`

### SC-12 · FREEDIVER'S BLOOM (Swim) — **STATUS: BUILT** · 5 shots × 6s · SILENT
- **DIFFERENCE STRING:** freedive swim (vertical) · journey **surface duck-dive → reef wall → coral garden → kelp cathedral → sun-shaft ascent** · signature **sun-shaft caustics + silver bubble-stream + coral/fish flash** · energy **weightless otherworldly** · light **underwater deep-blue → glowing gold** · wardrobe **modest teal long-sleeve dive-suit + coral stripe** · hair **slicked low woven braid** · shot-grammar **descend-with-her / parallel glide / rising boom / slow orbit / rising crane up the shaft** · **NEUTRAL BUOYANCY (no foot-weight)**.
- **THEME:** a serene weightless descent-and-rise through the ocean; light/water signature, grounded buoyancy. **FILE:** `SC-12 · Freediver's Bloom (Swim).md`

### SC-14 · ALPINE ASCENT (Cable-Car / Hike) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** cable-car + hike · journey **cable-car rise → pine forest → cliff path → summit lake** · signature **snow-sparkle + crystalline ice/water light + alpine wildflowers** · energy **fresh exhilarated** · light **crisp cool alpine (brightening to brilliant)** · wardrobe **cream cable-knit + forest cord skirt + plaid scarf + beanie** · hair **fishtail braid under pompom beanie** · shot-grammar **inside-car rise / low track-with forest / high aerial ridge track / push-in+crane pull-back**.
- **THEME:** a crisp mountain climb to a mirror summit lake; cold-light signature. **FILE:** `SC-14 · Alpine Ascent (Cable-Car Hike).md`

### SC-15 · KITE RUN (Kite) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** giant-kite run · journey **headland launch → dune ridge → cliff-edge ribbon-bloom → sky-launch lean** · signature **kite colour-ribbons braiding into shapes + racing cloud-shadows + lifting grass/sand** · energy **free kinetic joy** · light **bright windy coast, clouds racing** · wardrobe **primary colour-block playsuit + tied windbreaker** · hair **high windswept ponytail** · shot-grammar **low-hero track-with / parallel ridge track / low looking-up orbit / crane pull-back** · uses 4th ref **`@kite`**.
- **THEME:** a wind-chasing kite run; ribbon-bloom + sky-lean money shots. **FILE:** `SC-15 · Kite Run (Kite).md`

### SC-17 · FOUR SEASONS, ONE PATH (Walk) — **STATUS: BUILT** · 5 shots × 6s · SILENT
- **DIFFERENCE STRING:** walk one path · journey **spring blossom → summer green → autumn gold → winter snow → first spring bud** (SAME path re-skinned) · signature **season-transition sweep at each cut (same trees morph season to season)** · energy **poetic magical** · light **soft pink spring → bright summer → warm autumn → cool blue winter → soft spring** · wardrobe **cream pleated midi + colour-block cardigan, layering shifts per season** · hair **long loose half-twist** · shot-grammar **low track-with / parallel profile / high descend / parallel profile / push-in+crane pull-back**.
- **THEME:** one walk, four seasons re-skin the world around her; season-sweep signature. **FILE:** `SC-17 · Four Seasons One Path (Walk).md`

### SC-18 · PORTAL STEPS (Arches) — **STATUS: BUILT** · 3 shots × 6s · SILENT
- **DIFFERENCE STRING:** stride through arches · journey **flower arch → reef-world · reef arch → desert-world · desert arch → neon-city-world** · signature **threshold world-swap bloom (world dissolves & rebuilds as she crosses each arch)** · energy **bold surreal kinetic** · light **flower-gold → reef-blue → desert-amber → city-neon** · wardrobe **cobalt/magenta/citron colour-block mini + white knee boots** · hair **sleek geometric bob + fringe** · shot-grammar **low-hero push-through / parallel profile push-through / low 3/4 push-through+crane pull-back**.
- **THEME:** doorways between worlds; each stride swaps the entire world. **FILE:** `SC-18 · Portal Steps (Arches).md`

### SC-19 · THE PRODUCT BUILDS THE WORLD (Product → Set) — **STATUS: BUILT** · 3 shots × 6s · SILENT
- **DIFFERENCE STRING:** product authors the set · journey **studio void+bottle → liquid architecture → bloom set → hero plinth-world** · signature **world grows from the bottle (liquid → built architecture → bloom → crystalline hero set)** · energy **luxe surreal controlled** · light **clean studio → reflective → warm bloom → deep glowing** · wardrobe **champagne-gold liquid-satin couture column gown** · hair **sculptural low chignon** · shot-grammar **hero push-in / slow orbit / crane pull-back** · **3rd ingredient = `@product`** (not `@look`).
- **THEME:** most product-native — the hero bottle authors the entire world, grounded fluid+material physics. **FILE:** `SC-19 · The Product Builds the World (Product to Set).md`

### SC-21 · CITRUS COAST (Amalfi Stroll) — **STATUS: BUILT** · 4 shots × 6s · SILENT
- **DIFFERENCE STRING:** Amalfi stroll · journey **lemon grove → tiled village stairs → harbour quay → sea-view terrace** · signature **citrus-leaf flutter + sun-caught zest-mist + lemon-light glints** · energy **warm fresh joy** · light **bright lemon-sun (warming to glittering)** · wardrobe **lemon-yellow broderie sundress + woven belt + straw basket** · hair **low updo + patterned headscarf** · shot-grammar **low track-with / high descend stairs / parallel profile quay / push-in+crane pull-back**.
- **THEME:** a sun-drenched coastal stroll down to the sea; citrus-and-sun signature. **FILE:** `SC-21 · Citrus Coast (Amalfi Stroll).md`

## CONCEPT ROADMAP — ALL CONCEPTS BUILT ✓
*(rickshaw SC-05 dropped; redundant 2nd-blossom SC-20 dropped. All 19 planned concepts are now fully built —
see the BUILT CONCEPTS REGISTRY above. SC-01 + SC-02, SC-03, SC-04, SC-06, SC-07, SC-08, SC-09, SC-10, SC-11,
SC-12, SC-13, SC-14, SC-15, SC-16, SC-17, SC-18, SC-19, SC-21.)*

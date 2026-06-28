# Aira Prompt Rewrite — COMPLETE Standard, History & Resume Guide

Purpose: a single source of truth so any new session can resume with full context.
Repo: **aamir9000/Aamirs** · Branch: **aira-prompts-enhanced** (all work committed & pushed there).
Originals are preserved in git history / on `main`.

The job: take the master Aira concept `.txt` files and turn each into a clean,
AI-generation-ready (Nano Banana Pro stills + VEO video) version — additive only,
never deleting real descriptive content, and progressively raise them to the
"advanced" cinematic standard defined below.

====================================================================
## FOLDER STRUCTURE (CONCEPTS/ — reorganised by category)
====================================================================
All concept files now live in category folders under CONCEPTS/ (the old flat layout +
CONCEPTS/Heavy-Detail/ were dissolved):
- CONCEPTS/Transformation/ — every transformation reel (mid-clip outfit/world/object/weather/
  time/place/era/lighting/season/material change). Files: 20 Cinematic Reels New Set; Set 3;
  Set 4 (51-70); Set 5 (71-79) + (cont) + (cont 2) + (cont 3) + (cont 4); 20 Reel Concepts
  Master-Depth Build; Concepts 91-110 FULL Heavy-Detail. THIS is where the L+M retrofit is applied.
- CONCEPTS/Beauty/ — Beauty Ad + GRWM/beauty-hero. File: 20 Beauty Ad Reels.
  (NOTE: Master-Depth's GRWM concepts 11-14 + lifestyle 15-20 currently live inside the Master-Depth
  file in Transformation/ because they are mid-clip wrap-transforms; can be split out to Beauty/ on
  request.)
- CONCEPTS/Surreal/ — surreal fantasy worlds. File: NEW Reel Concepts (131-150).
- CONCEPTS/Action/ — vehicle/fight/stunt. Files: 20 Magical Action Heavy-Detail; Magical Action
  Set 2 Expression; Magical Action Master Set; Concept 170 Phoenix Crash.
- CONCEPTS/Time-Freeze/ — time-freeze/VFX. File: Time-Freeze Reel Set.
- CONCEPTS/Travel-Scenic/ — travel/scenic/cultural realism. Files: aira_set4; aira_set5.
- CONCEPTS/Product/ — product films. File: Concept 100 The Unboxing.
NOTE: section E/J path references below use the OLD locations; resolve them against this map.

====================================================================
## A. EVERYTHING ALREADY DONE (global passes, all 20 files unless noted)
====================================================================
1. **SUBJECT FRAMING & POSITION** added to EVERY image prompt (one unique prose
   paragraph per frame), each ending with the EXACT clause:
   "ORIENTATION LOCK — preserve this exact left-to-right composition; do not mirror, flip or invert the frame."
2. **Asterisks stripped** (all `**bold**` markdown removed; zero words lost).
3. **Internal codes removed** (AO./AO-X/AU./AT #/AW #/AF #/AQ #/AC #/AP #/AX #/BB) — 0 remain.
   Kept STD-NEG-IMG / STD-NEG-VID (real negative content).
4. **Restored 38 descriptor words** that had been wrongly dropped together with codes
   (e.g. (living stillness), (override), (hyper-vibrant), (identity-through-transform),
   (vibrant-on-dark), (real pores and texture preserved throughout)). Rule: strip the
   code, KEEP the meaningful words.
5. **SUBJECT / IDENTITY-intro line normalised** to: `Aira [paste identity-lock reference sheet here].`
6. **Video timestamps restructured** to discrete one-beat-per-line earlier on.
7. **MASTER AUDIO block per concept** (Cinematic Audio Direction — see section C). Added
   where missing; NOT duplicated where a per-concept brief already existed (Beauty Ad,
   More Full Set 3, Master-Depth, Set 4, Set 5 variants, 91-110, Magical Master Set,
   Concept 100 already had briefs and were left).
8. **6-SECOND CLIP STANDARD** (user decision; reasoning: 4s too short, 10s too long/drifty,
   6s lets the action play cleanly without filler):
   - MASTER AUDIO runtime = frames x 6s, in self-resolving ~6s phrases.
   - Per-frame beat timings rescaled to fill 6s; all `DURATION:` = 6 seconds;
     Time-Freeze "running total" recomputed cumulatively (6,12,18…).
   - Decade refs (70s/80s/90s) and reel-totals were protected from the rescale.
9. **IDENTITY & CHARACTER-CONSISTENCY LOCK** added to every video prompt (1,714), then
   upgraded to the **expression-safe "fixed skeleton" model** (section D).
10. **Cleanup:** deleted the duplicate top-level "Aira — …Set 3…256.txt", the untracked
    `concepts_dl/` and `_work/` old copies, `CONCEPTS.zip`, the 1-byte "Ai voice".
    Moved 7 heavily-detailed concepts into `CONCEPTS/Heavy-Detail/`.
11. **Beauty Ad Reels — FULL ADVANCED REBUILD complete** (all 20 concepts, 129 video prompts) — section B.

====================================================================
## B. THE ADVANCED VIDEO-PROMPT REBUILD (the current standard)
====================================================================
For each concept: READ IT FULLY, understand its world + dance/hero-move, then rewrite
ONLY frames that are boring / unfit / ruining the moment. No blind templating.

Per VIDEO prompt:
1. REPLACE the old `SUBJECT ACTION WITH TIMING:` block with a heavily-detailed
   `SHOT BREAKDOWN (timed, 6s · real-time, continuous energetic motion — never slow-motion,
   never a static hold; expression eye-led and identity-safe):` with 3 beats:
   `- [00:00–00:02] …  - [00:02–00:04] …  - [00:04–00:06] …`
   Each beat = **shot size/angle + her action + object/world interaction + eye-led expression + camera move.**
2. DEDUP: delete the standalone `CAMERA MOVEMENT:` and `CHOREOGRAPHY & FLUID MOTION:`
   lines (motion + camera now live only inside the breakdown). Keep MICRO-MOVEMENT,
   LIGHTING, ENVIRONMENT, AUDIO, LIP-SYNC, NEGATIVE.
3. REPLACE `FRAME RATE + MOTION BLUR:` line with EXACTLY:
   `FRAME RATE + MOTION BLUR: 24fps, real-time playback at natural speed (no slow-motion), 180° shutter, natural motion blur.`
4. SET `DURATION:` to `6 seconds (the clip plays the full 6s at real-time natural speed).`
5. REPLACE the video `SHOT TYPE:` line with the frame's varied shot size/angle/placement.

Per IMAGE prompt: REPLACE the `FRAMING:` line with the frame's varied crop/angle/placement.
Keep the image still NATURAL/alive (Veo animates the expression from the still — don't
freeze a hammy peak expression into it).

ALL frames in a concept must differ in:
  • CROP: ECU / CU / head-&-shoulders / half (waist) / cowboy (knee) / full-body / wide.
  • ANGLE: front / three-quarter / profile(side) / over-the-shoulder / low-hero / high / overhead / symmetrical.
  • PLACEMENT: centre / left-third / right-third / near(fills frame) / far(small, env-dominant); flip negative space side to side.
  • CAMERA: orbit / dolly-in / crane-boom / tracking / whip-pan / arc / rack-focus / pull-out / snap-push — distinct per frame, matched to the concept's dance/world (NOT push-only).

Other rules:
  • ALREADY-IN-MOTION starts — beat 1 opens with motion already in progress (anti cold-start drift).
  • REAL-TIME, NO SLOW-MO anywhere.
  • EXPRESSIONS: eye-led + identity-safe (section D). ONE smooth transition per clip
    (e.g. focus → wonder → soft smile), eyes tracing the object. Tone-matched:
    playful/cute reactions (e.g. delighted hands-framing-cheeks, surprised eye-widen,
    cute scrunch) for LIGHT concepts; dramatic awe/intensity for SERIOUS ones.
    Hands near face must FRAME (not cover) and stay clean to avoid finger/face drift.
  • MAGICAL TOUCHES: concept-specific interactive magic tied to her touch + the hero
    material (chrome races where she traces, petals swirl to her gesture, light gathers
    to her palm) — never random VFX.
  • SUBCONSCIOUS CONTINUITY: maximum surface variety, but keep world/palette/identity/
    lighting + motion hand-off (each frame ends on a vector the next picks up) + loop
    (last frame resolves to frame 1) continuous, so it reads as ONE reel.
  • Preserve identity lock, scene detail, loop logic, and SPOKEN vs SILENT (silent reels
    have no spoken line — use an expression reveal instead).

====================================================================
## C. CINEMATIC AUDIO DIRECTION (the MASTER AUDIO block per concept)
====================================================================
Two layers: (1) one MASTER AUDIO block OUTSIDE the frames per concept; (2) per-frame
in-prompt audio. Master audio = custom score for the exact runtime, no fade-in (emotion
in first second), mood→instrument palette (luxury: deep sub+felt piano; romance: piano/
strings/violin; power: trailer perc/synth bass/brass; dream: harp/choir; mystery: cello/
dark; beauty: delicate piano/atmos), emotional arc across frames, vocals only if they
help (honour SPOKEN/SILENT), layered, and event IMPACTS reserved for major beats (reveal/
transform/peak) tuned to the score's key so they read as the music expanding, not added SFX.
Runtime now = frames x 6s (or ~60s self-resolving/cuttable if a fixed clip duration is implied).

====================================================================
## D. IDENTITY-SAFE EXPRESSION MODEL (in every video prompt's lock)
====================================================================
Problem: when Veo animates big/fast expressions it drifts the face. Solution wording
(already applied to all 1,714 locks): treat identity as a FIXED skeleton that never
changes (bone structure, face shape/proportions, eye shape+spacing+iris colour, nose &
lip shape, skin tone+texture, hairline, hair colour+texture, build, hands). ONLY soft
expression muscles (lids, brows, cheeks, mouth corners) + eyes/gaze/head may move,
animating ON TOP of fixed identity. Lead with EYES/gaze; keep expression smooth, moderate,
ONE clean transition per clip; no extreme grimace, wide-mouth distortion, hard squint, or
rapid flicker that warps geometry. Through any transform only the intended element changes;
interpolate strictly between locked keyframes; never invent a new face/hands/second subject.

====================================================================
## E. REMAINING QUEUE (apply section B advanced rebuild) + treatment notes
====================================================================
Read each fully first; tailor camera/expression to its dance/world. Suggested treatments:
- 20 Cinematic Reels New Set — DONE (all 20 concepts / 123 video prompts rebuilt). See PROGRESS below.
- 20 Full Reel Set 4 (51-70) — DONE (all 20 concepts / 122 video prompts rebuilt). See PROGRESS below.
- 20 Full Reel Set 5 (71-79) — DONE (all 51 intact video prompts rebuilt; concept 79 corrupt past Frame 1 — see PROGRESS).
- Set 5 (cont 2) / · Set 5 (cont) / Set 5 cont 3 / cont 4 — DONE (concepts 79-84, 42 video prompts). See PROGRESS below.
- 20 Magical Action Heavy-Detail — ACTION (hypercar/chase/combat); handheld, whip-pan, low-hero,
  hard hits on impacts. NOTE: inline single-line video prompts (different structure — adapt regex).
- 20 Magical Action Set 2 Expression — action/expression; inline format too.
- Magical Action · Master Set — action; uses "## 🌀 CONCEPT", "### Frame", MASTER TRACK BRIEF per concept.
- 20 More Full Reel Set 3 — varied; already has MASTER TRACK BRIEF per concept.
- Heavy-Detail/Master-Depth Build — varied; brief per concept.
- Heavy-Detail/Concept 100 (Unboxing), Concept 170 (Phoenix Crash) — single/few concepts, very dense.
- Heavy-Detail/Concepts 91-110 FULL Heavy-Detail — chrome/liquid-metal studio.
- Heavy-Detail/NEW Reel (131-150) — surreal worlds; rich.
- Heavy-Detail/Time-Freeze — time-freeze reels; NOTE 2 concepts are continuous "oner" single-takes
  with CUMULATIVE beat timings (e.g. 14.0–14.8s) and bare `### VIDEO PROMPT` headers — those 8 frames
  were intentionally LEFT (don't force discrete 6s). Some concepts have "running total" annotations.
- aira_set4 / aira_set5 — Format B plain text: headers `---- FRAME k · SIZE · ANGLE ----`,
  `IMAGE PROMPT (Nano …)`, `VIDEO PROMPT (VEO … · 6s · 24fps)`, audio woven inline; set4 video
  header has NO trailing colon. Already have per-frame audio; need the advanced breakdown + variety.

====================================================================
## F. METHOD, VERIFICATION, WORKFLOW
====================================================================
- Reusable Python pattern used for Beauty Ad lives in `_tools/beauty_c*.py` (per-concept
  authored content + region/frame regex application). Reuse/adapt per file format.
- Per concept: isolate region (`# CONCEPT N` → `# CONCEPT N+1`), split by frame headers,
  IMAGE→replace FRAMING, VIDEO→replace SHOT TYPE / delete CAMERA MOVEMENT + CHOREOGRAPHY /
  replace SUBJECT ACTION WITH TIMING → SHOT BREAKDOWN / replace FRAME RATE / set DURATION.
- VERIFY each file: 0 leftover `SUBJECT ACTION WITH TIMING`, 0 `^CAMERA MOVEMENT:`,
  0 non-negated `slow-mo`, breakdown count == video-prompt count, all DURATION 6s,
  identity-lock count == video-prompt count, ORIENTATION LOCK count == image-prompt count.
- Commit per concept or small batch with a clear message; PUSH with the GitHub power
  `push_to_remote` (NEVER raw `git push`). Update the PROGRESS section of this file as you go.

====================================================================
## G. OPEN / OPTIONAL ITEMS (decide with user)
====================================================================
- Optional: add explicit synced `IMPACT —` clauses to transform frames in non-Beauty files
  (offered earlier; only do where not already present, to avoid duplicates).
- The 8 Time-Freeze "oner" cumulative frames left as-is by design.
- Files with spelled-out `DURATION: N seconds` and inline-action single-line video prompts
  need format-specific regex (the simple line-replacements assume the markdown format).

====================================================================
## H. RESUME PROMPT (paste into a new session)
====================================================================
"Continue the Aira prompt rebuild on branch aira-prompts-enhanced. Read
.kiro/steering/aira-prompt-rewrite-standard.md fully for the standard, history and
progress. Beauty Ad is complete. Continue the ADVANCED video-prompt rebuild on the
remaining queued files, one concept at a time — read each fully first, tailor camera +
expression to its world, keep every frame distinct with subconscious continuity, then
commit and push each and tick it off the progress tracker."


====================================================================
## PROGRESS TRACKER (advanced video-prompt rebuild)
====================================================================
DONE (section B advanced rebuild applied + verified + pushed to aira-prompts-enhanced):
- CONCEPTS/Heavy-Detail/20 Beauty Ad Reels — COMPLETE (20 concepts, 129 video prompts).
- CONCEPTS/20 Cinematic Reels New Set.txt — COMPLETE (20 concepts, 123 video prompts).
  Format note: this file uses a RICHER per-frame structure than Beauty Ad — image prompts
  use `ANGLE & SHOT SIZE:` (not `FRAMING:`) and ALREADY had `SUBJECT FRAMING & POSITION` +
  ORIENTATION LOCK from the earlier global pass (so no image edits were needed). Video
  prompts used `SHOT TYPE & ANGLE` / `CAMERA MOVEMENT (CHOREOGRAPHY)` / `SUBJECT ACTION w/
  BEAT-TIMING` plus extra physics sections (FLUIDITY & WEIGHT, FABRIC/HAIR/PROP PHYSICS,
  FOOTWORK & BODY FLOW, TRANSITION, LIGHTING-IN-MOTION, AUDIO, LOOP LOGIC).
  Adaptation of section B for this format: removed the standalone `CAMERA MOVEMENT
  (CHOREOGRAPHY)` line (camera now lives in the breakdown), replaced `SUBJECT ACTION w/
  BEAT-TIMING` with a tailored timed 3-beat `SHOT BREAKDOWN (6s ... never slow-motion ...)`
  (each beat = shot/angle + action + world interaction + eye-led expression + camera move,
  already-in-motion starts, camera variety beyond push), and inserted the standard
  `FRAME RATE + MOTION BLUR: 24fps ...` + `DURATION: 6 seconds ...` lines. All other
  rich sections were PRESERVED (additive-only). SPOKEN-frame `SPOKEN LINE (...)` dialogue
  preserved in all 12 spoken concepts. Verified: 0 leftover SUBJECT ACTION, 0 standalone
  CAMERA MOVEMENT, 123 SHOT BREAKDOWN == 123 video prompts == 123 FRAME RATE == 123
  DURATION 6s == 123 identity locks; 123 image ORIENTATION LOCKs intact; no non-negated
  slow-mo. Reusable engine: `_tools/newset_rebuild.py` (BEATS dict per concept + region
  surgery, idempotent; run `python3 _tools/newset_rebuild.py N`).

NEXT IN QUEUE: 20 Full Reel Concepts Set 4 (51-70) — couture-material transforms.
(Remaining queue unchanged below in section E; each file may need a format-specific
adaptation of the section-B method like the one documented above.)


- CONCEPTS/20 Full Reel Concepts Set 4 (Concepts 51.txt (concepts 51-70) — COMPLETE
  (20 concepts, 122 video prompts; concept 66 = 8 frames, all others 6). This file is the
  Beauty-Ad markdown format, so section B applied directly: per video prompt removed the
  standalone `CAMERA MOVEMENT:` line, replaced `SUBJECT ACTION WITH TIMING` with a tailored
  timed 3-beat `SHOT BREAKDOWN` (track the transform / orbit the apex; each beat = shot/angle
  + action + transform/material interaction + eye-led expression + camera move; already-in-
  motion starts; camera variety), and RESET the existing `DURATION:` line (was mixed 5s/6s
  with "of 30s total" running annotations) and `FRAME RATE + MOTION BLUR:` line to the 6s
  standard strings. Image prompts already had varied FRAMING + SUBJECT FRAMING & POSITION +
  ORIENTATION LOCK and identity locks already the expression-safe model — left untouched.
  Spoken concepts 51-63 embed the line inside the Frame-4 beat (the image `SPOKEN LINE:`
  field, 29 of them, was NOT modified); silent concepts 64-70 use a wordless expression
  reveal in Frame 4 instead. Verified: 0 leftover SUBJECT ACTION, 0 standalone CAMERA
  MOVEMENT, 122 SHOT BREAKDOWN == 122 video prompts == 122 standard FRAME RATE == 122
  DURATION 6s == 122 first-beat brackets == 122 identity locks; 122 image ORIENTATION LOCKs
  intact; no non-negated slow-mo. Reusable engine: `_tools/set4_rebuild.py` (BEATS dict per
  concept; also resets DURATION + FRAME RATE lines in place; idempotent).

NEXT IN QUEUE: 20 Full Reel Concepts Set 5 (71-79) — studio couture transforms (image-heavy);
vary crop/angle hard. Check its exact format first (it may match the Beauty-Ad markdown like
Set 4, in which case set4_rebuild.py adapts with a path change).


- CONCEPTS/20 Full Reel Concepts Set 5 (Concepts 71.txt (concepts 71-79, all SILENT) —
  COMPLETE for all intact frames (51 video prompts: 71-77 = 6 frames each, 78 = 8 frames,
  79 = only Frame 1 intact). Same Beauty-Ad markdown format and same transform as Set 4
  (engine `_tools/set5_rebuild.py`): removed `CAMERA MOVEMENT:`, replaced `SUBJECT ACTION
  WITH TIMING` with tailored timed 3-beat `SHOT BREAKDOWN`, reset `DURATION:` (was mixed
  decimal/"of 30s total" annotations) and `FRAME RATE + MOTION BLUR:` to the 6s standard.
  All silent — Frame-4/face beats use a wordless expression reveal, no spoken line. Concepts
  72-77 share a structural pattern (push-in chest-up / arc-push material-form transform /
  rack-focus product->eye / face-dominant emotional beat / beauty 3D orbit synced to a
  bloom-burst / pull-back loop close); each tailored to its material (living-vine topiary,
  terrazzo, woven-rattan, chalk-bloom, sequin-cascade, liquid-enamel pour, kirigami lace-cut,
  mylar-foil balloon, oil-slick prism). Verified: 0 leftover SUBJECT ACTION, 0 standalone
  CAMERA MOVEMENT, 51 SHOT BREAKDOWN == 51 video prompts == 51 standard FRAME RATE == 51
  DURATION 6s == 51 first-beat brackets == 51 identity locks; 51 image ORIENTATION LOCKs
  intact; no non-negated slow-mo.
  ** SOURCE-CORRUPTION FLAG — CONCEPT 79 (Prism Mirror Studio): the source file is corrupted
  past Frame 1. Its brief says "7 frames" but only Frame 1 (image + video) exists; after the
  F1 video NEGATIVE line the text runs on (".muddy [colour.IO]...") into merged leftover
  fragments from CONCEPT 78 (a candy-electro-pop Master Track Brief, balloon-burst / mylar
  content, and two orphan DURATION lines: "3 seconds (0:27 to 0:30…)" and "4 seconds
  (0:20 to 0:24…)"). Frame 1 was rebuilt to standard; frames 2-7 do NOT exist and the merged
  garbage was intentionally LEFT as-is (not deleted, not fabricated). To fully finish 79 the
  user must supply the original frames 2-7; then rebuild them with set5_rebuild.py after
  cleaning the merged 78-fragment block. **

NEXT IN QUEUE: 20 Full Reel Concepts Set 5 (cont 2) / · Set 5 (cont) / Set 5 cont 3 / cont 4
— couture/clothes-change, transform-led (check each file's format first).


- Set 5 continuation files (concepts 79-84, all SILENT) — COMPLETE (42 video prompts):
  * "20 Full Reel Concepts · Set 5 (cont.txt" — concept 79 (FULL 7-frame Prism Mirror Studio
    — this is the real/complete version; the copy inside the main Set 5 file was the corrupted
    truncated duplicate, F1-only) + concept 80 (Cobalt & Marigold thermochromic; 6 real frames
    plus a stray duplicate Frame-1 block at the file end — rebuilt the dup identically to F1 to
    keep it consistent → 14 SHOT BREAKDOWN total).
  * "20 Full Reel Concepts Set 5 (cont 2).txt" — concept 81 (lava-lamp blob-morph, 7) +
    concept 82 (plasma-globe filament, 6) → 13.
  * "Set 5 (cont 3) Clothes-Change Transformation.txt" — concept 83 (Snap-Change four-look
    spin/flip/bloom runway, 8).
  * "Set 5 (cont 4) · Clothes-Change Transformation.txt" — concept 84 (Magnet-Snap three-look
    fly-on / light-zip, 7).
  Same Beauty-Ad markdown transform via the GENERIC engine `_tools/md_rebuild.py "<path>" N`
  (path-parameterised so one engine serves all four files). IMPORTANT engine upgrade: it now
  matches BOTH the multi-bullet AND the inline single-line `SUBJECT ACTION WITH TIMING:` forms
  (concepts 83 & 84 use the inline form) via regex
  `SUBJECT ACTION WITH TIMING:(?:\n(?:- .*\n)+| [^\n]*\n)`. All silent — wordless expression
  reveal, no spoken line. The clothes-change reels (83/84) keep their whip-spin / split-flap /
  magnetic-snap / light-zipper change beats folded into the breakdown. Verified per file:
  0 leftover SUBJECT ACTION, 0 standalone CAMERA MOVEMENT, and SHOT BREAKDOWN == video prompts
  == standard FRAME RATE == DURATION 6s == first-beat brackets (14 / 13 / 8 / 7); no
  non-negated slow-mo.
  NOTE: the corrupted Concept-79 stub still living in the MAIN "20 Full Reel Concepts Set 5
  (Concepts 71.txt" file (F1 rebuilt, frames 2-7 missing + merged 78-fragments) is now
  redundant — the complete 79 lives in the (cont) file. Optional cleanup: delete the corrupt
  79 block from the main Set 5 file (left as-is for now, not destructive).

NEXT IN QUEUE: 20 Magical Action Reels Heavy-Detail — ACTION (hypercar/chase/combat); handheld,
whip-pan, low-hero, hard hits on impacts. NOTE (from section E): inline single-line video
prompts (different structure) — md_rebuild.py's inline-form regex may already cover it, but
verify the per-frame layout first.


====================================================================
## I. COLOUR / VIBRANCY DISCIPLINE (controlled vibrancy — do NOT over-colour)
====================================================================
Principle (agreed with user): vibrancy is already baked into these concepts, so the goal
is RESTRAINT, not more colour. Too much saturation everywhere destroys the visuals — it
flattens depth, removes focal hierarchy, pushes skin tone unnatural, blows highlights and
causes eye-fatigue. Rich = curated, not maxed. Apply this to all Aira prompt work:

- CURATED PALETTE: one dominant hue family + 1-2 supporting accents per concept; anchor it
  with neutrals / tonal areas / negative space so the colour has somewhere to breathe.
- VIBRANCY THROUGH CONTRAST & LIGHT, not blanket saturation: get "pop" from rim-light,
  speculars, glow, a bright subject against a darker/cooler ground — not by cranking every
  surface to full chroma.
- HERO READS FIRST: Aira (and the hero product) must be the focal point; the environment
  supports, it does not compete. Keep a clear figure-to-ground separation.
- PROTECT IDENTITY & SKIN: natural, true skin tone — never push saturation onto the face;
  no colour cast that shifts identity, eye colour or makeup intent.
- "ALREADY-VIBRANT" = CEILING, NOT FLOOR: where a concept is tagged hyper-vibrant / neon /
  candy / electric, treat that as the maximum and balance it with dark/neutral grounds and
  restraint so colour punches rather than overwhelms. Do not add further saturation.
- LEAVE TONAL/LUXE CONCEPTS TONAL: porcelain, marble, ice, obsidian, ink, forge, pearl,
  sea-blue/pool, chrome — these are deliberately restrained; keep their elegant tonal palette,
  do not "colour them up."
- AVOID: neon-on-neon mud, clashing full-saturation fields, rainbow-everything, blown
  highlights, muddy/over-graded look. Favour clean, deliberate, cinematic colour.

NOTE: this is a guardrail for palette intent (lives in briefs / IMAGE prompts / LIGHTING /
ENVIRONMENT). The video SHOT BREAKDOWN rebuild does not change colour; it only references
each concept's existing palette. No destructive mass re-grade was applied — existing
vibrancy was preserved and is to be kept balanced per the above.


- CONCEPTS/20 Magical Action Reels Heavy-Detail.txt (20 concepts, 151 video prompts) —
  ALREADY-COMPLIANT, NO REBUILD APPLIED (and must NOT be templated). This file was built on
  a later base ("Sys Directive 3 + Vibrance Patch") and already meets/exceeds the advanced
  standard: every video prompt has the expression-safe FIXED-SKELETON identity lock, a varied
  `CAMERA MOVEMENT: one move only` action camera (push-in, shake-settle, parallel track,
  whip-pan, arcing orbit, crane-up, etc.), a 3-beat `SUBJECT + OBJECT ACTION (timecoded)`
  block (0.0-2.0 / 2.0-4.0 / 4.0-6.0) PLUS a dedicated `PHYSICS:` line and a separate eye-led
  `EXPRESSION TRANSITION:` line, `DURATION: 6.0s`, a per-frame diegetic `AUDIO (Block A)` and
  an external Master Soundtrack block; image prompts carry SUBJECT FRAMING & POSITION +
  ORIENTATION LOCK. Verified uniform: 151 of 151 for each marker. NO visual slow-motion (the
  only "slow-mo"/"half-time" matches are the music-tempo term in the score brief and the word
  "ramp"). Grades are controlled complementary palettes (e.g. gold + teal) with explicit
  `no oversaturation` / `no garish neon` negatives — already follows the Controlled Vibrancy
  discipline (section I). Converting its `SUBJECT + OBJECT ACTION (timecoded)` into a bare
  `SHOT BREAKDOWN` would STRIP the PHYSICS and EXPRESSION-TRANSITION detail — do not do it.
  Treat this file as a reference implementation of the standard.


- CONCEPTS/20 Magical Action Reels Set 2 Expression.txt (20 concepts, 151 video prompts) —
  ALREADY-COMPLIANT, NO REBUILD (same Sys-Directive-3 base as the Heavy-Detail action file).
  Verified uniform 151/151: SUBJECT + OBJECT ACTION (timecoded), EXPRESSION TRANSITION,
  CAMERA MOVEMENT: one move only, DURATION 6.0s, fixed-skeleton identity lock, SUBJECT
  FRAMING & POSITION + ORIENTATION LOCK on images. Do not template.

====================================================================
## J. FILE-FORMAT AUDIT (which files still need the rebuild) — quick map
====================================================================
DONE (SHOT BREAKDOWN, rebuilt): Beauty Ad (129), Cinematic New Set (123), Set 4 51-70 (122),
  Set 5 71-79 (51), Set 5 (cont) 79-80 (14), (cont 2) 81-82 (13), (cont 3) 83 (8),
  (cont 4) 84 (7).
ALREADY-ADVANCED (SUBJECT + OBJECT timecoded — leave as-is, do NOT template): Magical Action
  Heavy-Detail (151), Magical Action Set 2 Expression (151).
STILL NEEDS REBUILD (uses `SUBJECT ACTION WITH TIMING` markdown — apply section B):
  - 20 More Full Reel Concepts Set 3.txt — DONE (concepts 31-50, 128 video prompts; see PROGRESS).
  - Heavy-Detail/20 Reel Concepts Master-Depth Build.txt — DONE (concepts 01-20, 140 video prompts; see PROGRESS).
  - Heavy-Detail/Concept 100 · The Unboxing.txt (note SA=6 vs VP=4 — inspect; possible
    image-side SUBJECT ACTION or extra blocks)
  - Heavy-Detail/Concept 170 · Phoenix Crash.txt (8)
  - Heavy-Detail/Concepts 91-110 · FULL Heavy-Detail.txt (26)
  - Heavy-Detail/NEW Reel Concepts (131-150).txt (134)
  - Heavy-Detail/Time-Freeze Reel Set.txt (SA=136 vs VP=80 — inspect; remember the 8 "oner"
    cumulative-timing frames are intentionally LEFT per section E/G).
NEEDS REBUILD, NON-STANDARD FORMAT (verify per file before running an engine):
  - Magical Action Reels · Master Set.txt (129 VP; "## CONCEPT" + MASTER TRACK BRIEF; no
    SA/SB/SO marker — confirm its action/timing layout first).
  - aira_set4.txt (117 VP) and aira_set5.txt (123 VP) — Format B plain text
    ("---- FRAME k · SIZE · ANGLE ----"); audio woven inline; need advanced breakdown + variety.


- CONCEPTS/20 More Full Reel Concepts Set 3.txt (concepts 31-50, 128 video prompts) —
  COMPLETE. Clean Beauty-Ad markdown format; rebuilt with the GENERIC engine
  `_tools/md_rebuild.py "<path>" N` (handles bullet AND inline `SUBJECT ACTION WITH TIMING`).
  Per video prompt: removed `CAMERA MOVEMENT`, replaced action with a tailored timed 3-beat
  `SHOT BREAKDOWN`, reset `DURATION`/`FRAME RATE` to the 6s standard. Frame counts: 6 for most,
  7 for 31/34/37/40/43/48, 8 for 50 (Phoenix finale). Spoken concepts deliver the line in the
  Frame-5 beat (quoted accurately, e.g. "worth its weight in gold", "I always rise"); SILENT
  concepts 32/36/41/46 use a wordless expression reveal. Diversified the camera grammar (the
  source was push-heavy: added a slow arc on the gather frame + orbit on the hero/transform
  frame), kept already-in-motion starts, eye-led identity-safe expression, and the per-concept
  "single face stays clear and locked / never multiplied / never covered" guard inside the
  transform beat where the source required it. Controlled-vibrancy honoured (e.g. Gilded
  Renaissance kept gold+oxblood candlelit, not garish). Also neutralised the only 2 stray
  "slow-mo" phrases (in Concept 32's IMAGE prompt) to "weightless real-time". Verified: 0
  leftover SUBJECT ACTION, 0 standalone CAMERA MOVEMENT, 128 SHOT BREAKDOWN == 128 video
  prompts == 128 standard FRAME RATE == 128 DURATION 6s == 128 first-beat brackets; 128 image
  ORIENTATION LOCKs intact; 0 genuine (non-negated) slow-mo.

NEXT IN QUEUE (markdown SUBJECT ACTION WITH TIMING — use md_rebuild.py): Concepts 91-110 (26),
NEW Reel 131-150 (134), Time-Freeze (verify the 8 "oner" frames first), Concept 100/170. Then
non-standard: Magical Action · Master Set (advanced already; only variable durations differ) and
aira_set4 / aira_set5 (Format B).


- CONCEPTS/Heavy-Detail/20 Reel Concepts Master-Depth Build.txt (concepts 01-20, 140 video prompts)
  — COMPLETE. Zero-padded double-hash headers (`## CONCEPT 01 —` … `## CONCEPT 20 —`); rebuilt with
  the GENERIC engine `_tools/md_rebuild.py "<path>" N` (its region regex `#+ CONCEPT 0*N \u2014`
  handles the zero-padding). All 20 concepts are 7 frames each. Per video prompt: removed the
  standalone `CAMERA MOVEMENT` line, replaced the inline `SUBJECT ACTION WITH TIMING` with a tailored
  timed 3-beat `SHOT BREAKDOWN`, and reset `DURATION` (was "N seconds (0:00–0:03 of 24s total)" etc.)
  and `FRAME RATE + MOTION BLUR` (several carried "a touch of slow-mo" / Frame-4 "96fps deep slow-mo")
  to the 6s real-time / no-slow-mo standard strings — this neutralised every slow-mo callout. The
  separate `OBJECT ACTION WITH TIMING` block was PRESERVED untouched (verified holds at 140), as were
  all PHYSICS / LIGHTING / ENVIRONMENT / AUDIO / NEGATIVE / identity-lock / image-side sections
  (additive-only). Camera grammar diversified off the push-heavy source: F1 establishing push, F2
  build (descending settle/drift or tilt-up to the cresting element), F3 START keyframe given a slow
  lateral ARC to the three-quarter transform-anchor, F4 hero ORBIT through the transform, F5 END
  reveal (orbit→push), F6 spoken-line push + 6° turn (line lands Frame 6), F7 loop-close (orbit→push
  back to the Frame-1 hook). One eye-led identity-safe expression transition per clip; already-in-
  motion starts; subconscious continuity + seamless loop seam preserved per concept.
  Concepts 08-10 (Monochrome Riot ink-bloom / Liquid Metal chrome-pour / Paper & Petals petal-burst)
  ADDITIONALLY carry the section-K believability lens woven into the hero beat — named real physics
  (ink-in-water capillary diffusion through real fabric weave; liquid-metal surface tension + mirror
  spread/inertia reflected in the water-skin; paper crease-to-petal flutter with real petal-dust),
  "no garish glare / no cheap sparkles", identity locked and face cleanly lit through the transform.
  Concepts 11-14 (GRWM/beauty: First Day / Sangeet / 5 AM Club / Glass Skin) and 15-20 (lifestyle:
  Inked / Rain Check / Long Drive / Bookshop / Kitchen Light / Countdown) kept the EXISTING treatment
  (no believability overlay), each tailored to its world + prop (coffee mug, marigold garland, water
  glass, serum bottle, collarbone, café window, car door, open book, mixing bowl, rooftop railing)
  and tone. Spoken lines quoted accurately in the Frame-6 beat for all 20 (all concepts spoken).
  Concept 16 (Rain Check) keeps its seated waist-up F1/F7 framing. Verified whole-file: 0 leftover
  SUBJECT ACTION, 0 standalone CAMERA MOVEMENT, 140 SHOT BREAKDOWN == 140 video prompts == 140 OBJECT
  ACTION == 140 standard FRAME RATE == 140 DURATION 6s == 140 first-beat brackets == 140 identity
  locks; 140 image ORIENTATION LOCKs intact; 0 genuine (non-negated) slow-mo. Engine BEATS dict now
  carries concepts 1-20 + 31-50 + 79-84. Commits: 97549b8 / 403ee3e / 58ce1ee (01-07), 6b1321b
  (08-10), 18d6f60 (11-14), ae4924a (15-17), eee7053 (18-20).

NEXT IN QUEUE (markdown SUBJECT ACTION WITH TIMING — use md_rebuild.py): Concepts 91-110 (26 — FIRST
confirm the K.1 "8-10 concept" flag with the user), NEW Reel 131-150 (134), Time-Freeze (verify the 8
"oner" frames first), Concept 100/170. Then non-standard: Magical Action · Master Set (advanced
already; only variable durations differ) and aira_set4 / aira_set5 (Format B).


====================================================================
## K. NON-BEAUTY REEL ENHANCEMENT — BELIEVABILITY, REALISM & THEME-FIDELITY
====================================================================
(Decided with the user. This is the agreed "something else" to add to the NON-beauty /
NON-GRWM reels. It is ADDITIVE and sits ON TOP of everything above — sections A-J still
apply: do the section-B video rebuild where the file still uses `SUBJECT ACTION WITH TIMING`,
preserve all heavy detail [OBJECT ACTION / PHYSICS / LIGHTING / ENVIRONMENT / AUDIO / NEGATIVE
/ identity lock / etc.], honour Controlled Vibrancy [section I], 6s real-time / no slow-mo,
commit + push per concept/batch, and update the section-J audit + progress as you go. Beauty
Ad + GRWM/beauty-hero reels stay on the existing treatment and are OUT of scope here.)

### K.0 — CORE PRINCIPLE (applies to every non-beauty concept)
- Make EVERY element believable and describe each element CLEARLY and specifically — exact
  material, weight, surface, behaviour, and how it interacts with light and motion. No vague
  "magic happens"; name the physics.
- The ONE impossible / magical beat per concept may be surreal and DREAMY, but it must be
  GROUNDED in real physics and clean, premium execution. Explicitly forbid: cheap sparkles,
  fake/unreal cartoon VFX, floaty unmotivated effects, plasticky CGI, weightless nonsense.
  Real materials, real weight, real light, real momentum — even through the one magic beat.
- Read each concept's THEME and make the visuals serve that exact purpose precisely.
- GREEN LIGHT (granted by user): you MAY expand these concept files with MORE descriptive
  detail (materials, micro-physics, scale, placement, lighting, motion) wherever it increases
  believability and theme-fidelity. Additive only — never strip real detail.
- Structural vehicles available to express the above (from the earlier module idea):
  * a `WORLD / OBJECT ACTION (timecoded)` track to describe each world/material element
    clearly on its own clock (this is the main tool for "describe each element clearly");
  * a `TRANSFORM KEYFRAME (START-lock -> CROSSING -> END-lock)` continuity block for clean,
    identity-safe morphs.

### K.1 — CONCEPTS 91-110 (three-look liquid-material couture, SILENT)
- Make all elements BELIEVABLE and describe each clearly: the exact material behaviour —
  mercury pour viscosity & meniscus, chrome peel, ink-bloom diffusion in water, watercolour
  bleed, holographic/prism refraction, sunset-gradient sky-wash, molten blown-glass flow.
  Real fluid + optical physics for each.
- Keep everything ELSE surreal and make it feel DREAMY at the same time — believable materials
  behaving in a dream-like, elegant way (grounded substance, dreamlike motion/mood).
- [FLAG — CONFIRM WITH USER] User said: "Keep the 8 to 10 concept as it is but make sure it
  looks awesome." Ambiguous against the 91-110 numbering — confirm whether this means concepts
  98-100, 108-110, or "leave ~8-10 of them structurally unchanged." Until confirmed: apply the
  believability lens to all 20 and do NOT structurally alter the flagged concept(s) beyond
  polish that makes them look awesome.

### K.2 — NEW REEL 131-150 (surreal fantasy worlds)
- Make SCALE believable — correct relative sizing of subject vs. world (nebula glassblower,
  gravity-well tea house, deep-sea cathedral, sky-market, planetarium, dune sea, prism-rain
  subway, etc.). Consistent, real perspective.
- Everything PRECISELY PLACED — grounded in coherent 3D space, no floating/mis-scaled/
  arbitrarily positioned elements. Dreamy, surreal worlds, but with believable scale and
  exact placement so the eye trusts the space.

### K.3 — aira_set4 (1-20) & aira_set5 (21-40) (travel / scenic / cultural; Format B plain text)
- Keep as MUCH REALISM as possible — real locations, real natural light, real fabric / water /
  sand / foliage physics. Keep any impossible/transform beat minimal and grounded; lean
  documentary-real over fantastical. (Format B: headers "---- FRAME k · SIZE · ANGLE ----",
  audio woven inline; adapt the rebuild to that structure.)

### K.4 — MAGICAL ACTION · MASTER SET (1-20) (vehicle / fight / stunt)
- Top-notch, MIND-BLOWING action; every sequence action-packed.
- Subject ALWAYS IN MOTION and action-ready in EVERY frame of EVERY concept — never a static
  hold; she is mid-action / coiled to move at all times.
- Car chases & CRASHES must be 100% BELIEVABLE: real vehicle dynamics — weight transfer,
  suspension travel, tyre slip/smoke, body roll, real impact deformation, glass/debris physics,
  momentum and braking. NO cheap sparkles, no cartoon/unreal action.
- Planes, cars, bikes, boats and all props must look ULTRA-REAL; their movement, speed,
  momentum and damage must read fully realistic. The one magic move stays but is executed with
  grounded physics.
- NOTE: this file is already structurally advanced (timecoded action + `CAMERA MOVEMENT: one
  move only` + 100% real-time, no slow-mo). Enhancement here = realism polish + ensure the
  believability language is in every prompt. (Open: whether to normalise its variable
  per-frame durations to the 6s standard — confirm with user.)

### K.5 — TIME-FREEZE REEL SET (1-19)
- Everything must BEHAVE EXACTLY per the concept's theme.
- In a TIME-FREEZE beat: suspended elements are truly STILL in mid-air — water droplets,
  splashes, debris, sparks, fabric, hair, petals convincingly LOCKED as if time stopped, with
  correct mid-motion shape and real surface tension (water looks genuinely frozen mid-splash,
  not blobby/fake). If PEOPLE are frozen, freeze them realistically (held mid-gesture, true
  micro-stillness), with only Aira (or the intended subject) moving where the concept calls
  for it. The stillness must read as real frozen time, not a cheap pause.
- Part 2 (no-freeze signature tricks — RPM, Rewind, Echo, Vertigo, One Take, Freefall, Night
  Trails, Still Point, Metamorph, Locked On, Two Worlds): each trick reads as its real
  phenomenon, grounded and premium.
- KEEP the 8 "oner" cumulative-timing single-take frames AS-IS (per section E/G).

### K.6 — SINGLES & MIXED FILES
- Concept 170 (Phoenix Crash Rebirth): action -> apply K.4 realism (believable crash dynamics).
- Concept 100 (The Unboxing): product -> believable materials/lighting, premium real feel.
- Master-Depth Build: 08-10 (Monochrome Riot / Liquid Metal / Paper & Petals) take the
  K.0/K.1 believability lens; 11-14 are GRWM/beauty and 15-20 lifestyle -> keep the existing
  treatment (out of K scope unless user says otherwise).

### K.7 — RESUME PROMPT (paste into the fresh session)
"Continue the Aira rebuild on branch aira-prompts-enhanced. Read
.kiro/steering/aira-prompt-rewrite-standard.md FULLY (all sections A-K). Beauty Ad, Cinematic
New Set, Set 4, Set 5 (+continuations), More Set 3 are done; the two Magical Action files are
already compliant; Master-Depth Build 01-20 is DONE (whole file complete — 08-10 carry the
section-K believability lens, 11-20 kept the existing treatment). Now apply the section-B advanced
video rebuild PLUS the section-K Believability/Realism & Theme-Fidelity layer to the remaining
non-beauty files — 91-110, 131-150, aira_set4, aira_set5, Magical Action Master Set, Time-Freeze,
and Concept 170/100. Keep every detail heavily; only change what's necessary; controlled vibrancy;
6s real-time, no slow-mo; commit + push per concept; tick the section-J audit. First, confirm the
K.1 '8-10 concept' flag with the user before touching 91-110."



====================================================================
## L. TRANSFORMATION-REEL MODEL — MID-CLIP CHANGE + MATCH-CUT JOINS
====================================================================
(Decided with the user. Applies to ALL transformation reels — ANY concept where a change happens
mid-clip: outfit/wardrobe change, environment/world/set change, object/prop change, WEATHER
change, TIME-OF-DAY change, PLACE/LOCATION change, ERA/PERIOD change, LIGHTING change, season
change, material/finish change, look A->B, GRWM getting-ready wraps, and any "the world/outfit
turns" concept. A single reel may combine ONE or SEVERAL of these changes at once — handle each
precisely. ADDITIVE on top of sections A-K. The point: stop spreading one transform across multiple clips stitched by a fragile continuous-camera handoff; instead
CONTAIN each change inside one clip's middle, and make every frame join an intentional CUT.)

### L.1 — WHERE THE CHANGE HAPPENS (mid-clip, never at the seam)
- The visible Look-A -> Look-B change happens in the MIDDLE of ONE animated clip, never across a
  clip boundary. The transform clip plays:
  * [00:00-00:02] CUT in, ALREADY-IN-MOTION, in LOOK A, the look fully intact — NO change yet.
  * [00:02-00:04] the change BEGINS here (mid-clip) and flows SMOOTHLY across her in one continuous
    wavefront — gradual and motivated, never an abrupt swap.
  * [00:04-00:06] the wavefront completes and the look settles SMOOTHLY and fully into LOOK B and
    holds — never crammed into the last second, never a snap.
- Rationale: a change that must survive a clip join forces brittle frame-to-frame continuity. Keep
  the change safely inside one clip where the generator fully controls it.

### L.2 — HELD ANGLE INSIDE THE TRANSFORM CLIP (no abrupt angle shift mid-change)
- Within the transform clip the CAMERA ANGLE is HELD STEADY across the whole 6s — the angle must
  NOT shift abruptly while the change is occurring (an angle jump mid-transform fights the morph).
- The video generator's own natural camera MOVEMENT (a gentle push / drift / its subtle motion) is
  FINE and welcome — what is banned is a deliberate ANGLE change during the transformation. So the
  hero/transform clip no longer "orbits through" the change; it holds its angle and lets the change
  race through. (Big angle variety lives at the CUTS between frames, per L.3 — not inside the clip.)

### L.3 — EVERY JOIN IS A CUT + ANGLE CHANGE (the patch; viewer never feels they missed anything)
- At EVERY frame join, hard-CUT to a deliberately DIFFERENT angle/crop (different shot size +
  camera angle + placement). Never cut to the same/near-same angle (that exposes a mismatch as an
  ugly jump cut).
- That angle change IS the patch: it masks any slight variation between where the previous clip's
  Look B ended and where the next clip's still begins, and it makes the edit read as intentional —
  so the viewer feels they have NOT missed anything (polished editing rhythm, not a glitch).
- Every clip therefore opens ALREADY-IN-MOTION on its new angle (the cut lands mid-action).

### L.4 — TRANSFORMATION CONTINUITY VIA VEO FIRST/LAST-FRAME + CLEAR SMOOTH MID-CLIP MORPH (transformation clips ONLY)
- SCOPE: transformation clips only — a clip where something actually CHANGES mid-frame. Qualifying
  change types: OUTFIT/wardrobe, ENVIRONMENT/WORLD/SET, OBJECT/prop, WEATHER, TIME-OF-DAY,
  PLACE/LOCATION, ERA/PERIOD, LIGHTING, SEASON, MATERIAL/finish, look A->B. A reel may carry ONE or
  SEVERAL of these at once; whichever change(s) occur, choreograph all of them in the morph.
  Ordinary frames with no mid-clip change are exempt.
- CONTINUITY MECHANISM = VEO 3.1 FIRST-AND-LAST-FRAME, NOT TEXT. For a transform clip, supply the
  Look A still (= this frame's image) as the FIRST frame and the Look B still (= the NEXT frame's
  image) as the LAST frame; Veo morphs between them, so the clip ENDS EXACTLY on Look B = the next
  clip's start still. The cut is exact BY CONSTRUCTION. (This REPLACES the old exhaustive-1:1-text
  rule — Veo cannot text-generate a frame-exact match, so we hand it the exact end image instead.)
- TWO STILLS PER TRANSFORM CLIP: Look A (first) + Look B (last). Our frame structure already gives
  both — the transform frame's image = Look A; the NEXT frame's image = Look B (that same Look B
  still also starts the next clip, which guarantees the seam).
- Because the LAST-frame image carries the exact Look B, the transform clip's VIDEO TEXT does NOT
  need an exhaustive Look-B description — keep it LEAN. The text's only job is to CHOREOGRAPH THE
  MORPH clearly so it reads smooth:
  * [00:00-00:02] HOLD Look A, already in motion, the look fully intact — NO change yet.
  * [00:02-00:04] the morph BEGINS here (mid-clip) and flows smoothly across her in ONE continuous
    wavefront — state the PATH clearly: where it starts, which direction it travels, and what
    changes as it passes (if several things change at once, name each). Gradual, liquid, motivated.
  * [00:04-00:06] the wavefront completes and the look settles SMOOTHLY and fully into Look B (the
    last-frame still) and holds — NOT a last-second snap, NOT an abrupt swap.
- TIMING LAW: the change must START IN THE MIDDLE and resolve smoothly by the end — never instant,
  never crammed into the final second. Held angle throughout (L.2); camera may travel (track/push-with).
- The transform frame's OWN image = the clean LOOK A it opens on (not a mid-morph still).

### L.5 — WHAT STAYS THE SAME
- Identity lock (fixed-skeleton, section D); ONE eye-led identity-safe expression transition per
  clip; real-time / no slow-mo / 6s (sections B, D); Controlled Vibrancy (section I); section-K
  believability where it applies. The reel still LOOPS (final frame cuts back to match Frame 1).
- Subconscious continuity now lives in consistent IDENTITY / WORLD / PALETTE across the cuts + the
  loop — NOT in continuous camera motion-handoffs (those are replaced by the L.3 cuts).
- Replace the old per-concept "Movement ... locked transform keyframes START Frame 3 -> END Frame 5,
  interpolate strictly between keyframes across frames" language and any cross-frame orbit-handoff
  wording with the L.1-L.4 model (single held-angle transform clip + match-cut joins).

### L.6 — SCOPE / STATUS
- RETROFIT the transformation reels already rebuilt under the old continuous-handoff model
  (Master-Depth Build 01-20 first — nearly all transforms), AND carry this model forward to every
  remaining transformation reel in the queue.
- Per concept: read fully -> rebuild the video SHOT BREAKDOWN to the held-angle mid-clip transform
  with a strongly-specced Look B -> update the affected IMAGE prompts (transform still = Look A;
  next still = matched Look B, new angle) -> ensure every join is a cut to a new angle -> verify ->
  commit + push -> tick progress.



====================================================================
## M. ALIVE CAMERA — ACTIVE SUBJECT + CAMERA THAT RIDES WITH HER (real parallax)
====================================================================
(Decided with the user. Makes reels feel ALIVE: the subject is visibly DOING something and the
camera moves WITH her through an anchored, static world. ADDITIVE on top of A-L.)

### M.1 — THE SUBJECT IS ACTIVELY DOING SOMETHING (noticeable, motivated)
- In the alive (non-transform) beats she performs a real, READABLE action — walking/striding,
  working with her hands, reaching, turning through the space, moving toward/through something.
  Not just standing and breathing. The action should be clearly noticeable, motivated by the world.

### M.2 — CAMERA RIDES WITH THE SUBJECT (tracking / following moves)
- Use real DP moves where the camera MATCHES her motion vector so she stays framed while she moves:
  * SIDE-TRACK (the user's key example): she walks forward; the camera dollies LATERALLY alongside
    her at a steady side/profile angle, holding her in frame (capturing her sideways) as she travels.
  * FOLLOW: Steadicam/gimbal follow behind or ahead of her, matching her pace.
  * ARC-FOLLOW: camera arcs a few degrees while tracking her turn/walk.
  * CRANE-FOLLOW / PUSH-WITH: rise or push that travels with her, not at a static subject.

### M.3 — THE WORLD STAYS ANCHORED; LIFE COMES FROM REAL PARALLAX
- The background/environment is FIXED in real 3D space and stays in its place — it does NOT slide,
  float, warp or move on its own. The only reason it appears to move is genuine PARALLAX caused by
  the camera travelling: NEAR elements pass faster than FAR elements. That parallax is what sells
  "the camera is moving WITH the subject" (e.g. filming her sideways as she walks), not "the world
  is moving." Keep world geometry, scale and placement believable and consistent (ties to K.2).

### M.4 — INTEGRATION WITH THE TRANSFORM MODEL (sections L, B, D, I)
- A TRACK is a translation, not an angle rotation, so the camera MAY ride with her even during a
  transform clip — L.2's held-angle rule bans an abrupt ANGLE shift mid-change, NOT camera travel.
  So a transform beat can still be alive (tracking) while its angle holds.
- At each CUT (L.3) change the angle AND you may switch tracking style (side-track -> follow ->
  arc-follow), each clip opening ALREADY-IN-MOTION (the cut lands mid-stride / mid-action).
- Keep: identity lock + eye-led expression (D), real-time / no slow-mo / 6s (B), controlled
  vibrancy (I), believability/scale (K), and the F-last -> F1 loop. Write these alive tracking moves
  directly into the SHOT BREAKDOWN beats (shot/angle + her action + world interaction + camera move).



### M.5 — FULL CAMERA-MOVE VOCABULARY (draw from these; one move per clip, matched to the world)
ALIVE / TRAVELLING-WITH-SUBJECT (camera rides her; world anchored; real parallax):
- SIDE-TRACK / parallel dolly — camera travels laterally alongside a walk, capturing her side-on.
- FOLLOW (lead or trail) — Steadicam/gimbal follows behind or ahead, matching her pace.
- ARC-FOLLOW — camera arcs a few degrees around her as she turns/moves.
- CRANE-FOLLOW / BOOM-WITH — rise or descend while travelling with her.
- PUSH-WITH / PULL-WITH — push or pull that moves with a moving subject (not at a static one).
- WHIP-PAN / SWISH into the next beat's motion (use at energy spikes, action files).
STAGED / EXPRESSIVE (subject more contained; camera shapes the beat):
- PUSH-IN / DOLLY-IN, PULL-OUT / DOLLY-OUT, slow ORBIT, TRACKING across, CRANE/JIB up-down,
  TILT, PAN, RACK-FOCUS (pull focus product<->eye), SNAP-PUSH, HANDHELD breathe (doc-real),
  LOW-HERO rise, HIGH/OVERHEAD look-down, OVER-THE-SHOULDER.
RULES: pick ONE move per clip; never push-only across a concept; match the move to the
concept's world/action; alive tracking moves (top group) are preferred wherever she is moving;
during a TRANSFORM clip use a translation (track/push-with) NOT an angle rotation (L.2); switch
move + angle at every CUT (L.3); every clip opens ALREADY-IN-MOTION (B).



### M.6 — PER-FRAME POSE & MOTION VARIETY (default) vs HELD POSE (GRWM-only exception)
(Decided with the user. Corrects the earlier uniform "standing hero gesture" arc.)
- DEFAULT (almost every reel — fashion, transformation, material, fantasy, action, travel,
  editorial-beauty): the subject must be in a DIFFERENT POSE or genuinely IN MOTION in EVERY
  frame, tailored to the concept's theme — she walks/steps, shifts body orientation and level,
  leans, turns away and back, strides, sits/rises, strikes a distinct posture per shot. NEVER the
  same standing hand-gesture arc repeated across frames or across concepts. Pair with the alive
  camera (M.1-M.4) so she is visibly DOING something different each frame, and keep every frame's
  crop/angle/camera distinct (B). The eye-led identity-safe expression model (D) still governs the
  FACE, but the BODY should move.
- EXCEPTION — HELD / CONTAINED POSE (only where the theme truly requires it):
  * GRWM "get ready with me" reels (getting ready in one spot) — e.g. Concepts 11 (First Day),
    12 (Sangeet), 13 (5 AM Club).
  * Concepts whose premise IS an identical held pose by design — e.g. Concept 02 (Six Cities,
    "one her" = pose held identical across the match-cuts).
  * Genuine beauty-still / application moments where stillness is the point (e.g. Glass Skin
    serum beat) — keep mostly contained but still allow gentle per-frame variation.
- The TRANSFORM clip (F4) still HOLDS its camera ANGLE (L.2) and identity, but she MAY be in a
  distinct/dynamic pose there too — only the camera angle is fixed, never her body.
- ACTION: revisit any already-done NON-GRWM concept and inject real per-frame pose/motion variety;
  apply this to all remaining concepts. Fragrance "still radiant centre" reels (Midnight Bloom,
  Gold Hour) get GENTLE motion (a step, a turn, a drift) rather than fully static.



### M.7 — FULL-BODY MOTION VOCABULARY (layer several per frame — a head-to-toe kinetic chain)
(Decided with the user. Use with M.6: non-GRWM frames must move the WHOLE body — hands, arms,
legs, feet, waist/hips, torso, shoulders, neck/head, gaze, hair, fabric — not just one hand
gesture. Draw a DIFFERENT combination for each frame so no two repeat.)

GAZE & EYES: gaze-lift to lens, gaze cast down, eye-line sweep, glance over the shoulder, side-eye
  flick, eyes tracing the wavefront/object, slow blink, soft squint, widen in awe, lash flutter,
  focus snap, gaze drift then lock.
HEAD & NECK: head tilt, chin lift, chin tuck, slow head turn (L/R), head cant, gentle head roll,
  neck elongation, look-away-and-back, profile-to-front turn, soft nod, head float on the breath.
SHOULDERS: shoulder roll (fwd/back), shoulder drop, one shoulder forward, shoulder-blade draw,
  subtle shimmy, shoulder dip, shrug-and-release.
ARMS / HANDS / FINGERS: arm sweep, long extension, reach-and-trail, hand glide, fingers fanning
  open, fingertips trailing a surface or hair, wrist roll, wrist flick, hand to
  collarbone/jaw/hip/nape, hand framing the face (never covering), palm turn-up, open gesture,
  hair tuck behind the ear, cross/uncross arms, clasp-and-release, snap.
TORSO / WAIST / HIPS: torso rotation, waist twist, ribcage lift, spine elongation, gentle
  arch/backbend, side bend, contrapposto shift, hip sway, hip pop, hip counter-tilt, core spiral,
  slow undulation, figure-eight hip.
LEGS / FEET: step fwd/back, cross-step, weight shift (back<->front leg), pivot on the ball of the
  foot, heel lift, toe point, knee bend, lunge-step, ankle roll, half-turn step.
WHOLE-BODY / LOCOMOTION: walk-in, stride toward/away, turn-and-walk, slow spin, pivot-turn,
  saunter, sashay, glide, sway, level change (rise from a lean / lower), lean-on-a-surface-and-
  push-off, twirl, advance-and-glance-back.
HAIR & FABRIC (motion read): hair sway/flip, strand lift in the breeze, ponytail swing, fringe
  shift, skirt/hem flare, sleeve sweep, scarf/dupatta trailing, drape billow-and-settle.

RULE: each non-GRWM frame layers a HEAD-TO-TOE chain (e.g. strides in -> hips rotate -> waist
twists -> one arm sweeps up -> shoulders roll -> head turns -> gaze flicks to lens -> hair sways
-> hem flares); a DIFFERENT combination leads each frame so no two repeat. Real-time, natural
speed, NO slow-motion; identity-safe (face = eye-led only, D); energy matched to the concept
(powerful/strident, soft/flowing, or explosive/athletic). Exceptions per M.6 (GRWM / identical-
pose premise / beauty-still) stay contained. During a TRANSFORM clip the camera ANGLE holds (L.2)
but her body may still move through the kinetic chain.



### M.8 — IMPLEMENTATION: the pose/motion fix lives in BOTH the video AND the image prompts
Applying M.6/M.7 to a concept means editing TWO places per frame, not just one:
- VIDEO prompt: re-author the `SHOT BREAKDOWN` beats so each frame carries a head-to-toe kinetic
  chain (M.7), a different combination per frame. This is the primary motion driver for Veo.
- IMAGE prompt: update each frame's `BODY POSTURE & WEIGHT`, `SUBJECT FRAMING & POSITION`,
  `HANDS & NAILS` (and the `KINETIC STILLNESS` layers) so the START STILL already shows that
  DISTINCT DYNAMIC POSE (mid-stride, mid-turn, contrapposto, glance-back, level change, etc.).
  Veo animates from this still, so a static standing still will not produce the motion — the
  still itself must be a dynamic pose, and a different pose every frame.
- Loop + first/last-frame still hold: F-last returns to F1's (now dynamic) pose; the transform
  clip's first/last stills are the dynamic Look-A / Look-B poses.
SEQUENCING (per user): FIRST finish the L+M retrofit (sections L + lean-strip) across ALL
transformation concepts/files; THEN do this full-body pose/motion pass (M.6-M.8) over everything.
Exceptions stay contained: GRWM (11-13), identical-pose premise (02 Six Cities), beauty-still (14);
fragrance (06,07) gentle motion.



====================================================================
## *** CURRENT STATE & TWO-PASS PLAN — READ THIS FIRST ON RESUME (most recent) ***
====================================================================
Branch aira-prompts-enhanced. Folders: CONCEPTS/{Transformation, Beauty, Surreal, Action,
Time-Freeze, Travel-Scenic, Product} (see FOLDER STRUCTURE near top). Push via github power
push_to_remote (path /projects/sandbox/Aamirs, owner aamir9000, repository_name Aamirs,
remote_branch_name aira-prompts-enhanced). Commit per concept.

There are TWO sequential passes. FINISH PASS 1 across ALL transformation concepts/files BEFORE
starting PASS 2.

--- PASS 1 (IN PROGRESS) — L+M RETROFIT + LEAN-STRIP (sections L, M.1-M.5, B) ---
Per transformation concept:
  1. LEAN-STRIP the video prompts (engine `_tools/lean_strip.py "<path>"`, video-section scoped):
     short IDENTITY line, remove static LIGHTING + ENVIRONMENT lines, trim video NEGATIVE.
     ALREADY DONE on the 13 standard files (Transformation x10, Beauty, Surreal, Product).
  2. Rebuild the 7 video SHOT BREAKDOWN beats into the L+M model via engine
     `_tools/lm_rebuild.py "<path>" <N>` (add a BEATSLM[N] 7-tuple first): each frame opens
     "Cut to ..." (match-cut, new angle); transform happens MID-CLIP at a HELD angle inside the
     transform frame; smooth (begins middle, never abrupt/last-second); Veo first/last-frame
     wiring (transform-frame image = Look A = FIRST frame, next image = Look B = LAST frame);
     loop F-last -> F1. Engine also strips the old "(Transform-anchor distance ...)" / "(Camera
     distance ...)" parentheticals.
  3. IMAGE edits per concept (manual str_replace): rewrite the Movement line to the L+M model;
     flip the transform-frame (F4) IMAGE to the clean LOOK A it opens on; change F3/F5 keyframe
     notes + F2/F3/F5 COMPOSITION-REFERENCE lines from "START/END keyframe / suspended build /
     radiant reveal / imminent" to clean held-look / match-cut SHOT NOTES.
  4. VERIFY region: 0 of {mid-*, locked START/END, interpolate strictly, Camera distance,
     suspended build, macro build beat, radiant reveal, transform resolved, cause building to
     effect}; 7 "Cut to" beats; F4 image shows Look A. Whole file breakdown count unchanged.
  5. Commit + push.
PASS 1 DONE: Master-Depth Build concepts 01-12 (commits through 9a72427).
PASS 1 REMAINING:
  - Master-Depth Build: concepts 13-20 (13 5AM-GRWM, 14 Glass-Skin, 15 Inked, 16 Rain Check,
    17 Long Drive, 18 Bookshop, 19 Kitchen Light, 20 Countdown). lm_rebuild.py BEATSLM has 1-12.
  - Then the other Transformation/ files: 20 Cinematic Reels New Set; 20 More Full Reel Set 3;
    Set 4 (51); Set 5 (71); Set 5 (cont); Set 5 (cont 2); Set 5 (cont 3); Set 5 (cont 4);
    Concepts 91-110. (NOTE: these were section-B rebuilt + lean-stripped earlier but NOT yet on
    the L+M mid-clip/cuts/first-last-frame model — they still use the old orbit-through-transform
    beats; bring them onto L+M.)
  - Then non-transformation folders as applicable (Surreal 131-150, Action, Time-Freeze,
    Travel-Scenic aira_set4/5, Product) — these get lean-strip + section-K believability + L+M
    only where a real A->B/mid-clip change exists (match-cut/cut model otherwise).

--- PASS 2 (AFTER PASS 1 IS COMPLETE) — FULL-BODY POSE/MOTION (sections M.6, M.7, M.8) ---
Apply to EVERY concept EXCEPT the held-pose exceptions. Subject must be in a DIFFERENT POSE or
genuinely IN MOTION in EVERY frame — a head-to-toe kinetic chain (gaze/head/shoulders/arms/hands/
waist/hips/legs/feet/locomotion/hair/fabric), a DIFFERENT combination each frame, theme-tailored.
Written into BOTH (a) the video SHOT BREAKDOWN beats AND (b) the image BODY POSTURE & WEIGHT /
SUBJECT FRAMING / HANDS / KINETIC STILLNESS so the start still already shows a distinct dynamic
pose. Keep loop + first/last-frame.
  EXCLUDE / keep contained: GRWM reels (Master-Depth 11 First Day, 12 Sangeet, 13 5 AM Club, and
  any other GRWM); identical-pose-by-premise (Master-Depth 02 Six Cities); beauty-still
  (Master-Depth 14 Glass Skin). Fragrance (Master-Depth 06 Midnight Bloom, 07 Gold Hour) = GENTLE
  motion, not fully static.
  A full-body reference draft for Master-Depth Concept 01 (Steel to Silk) video beats was authored
  in chat (stride-in / profile-glance / pivot-arms-open / mid-turn transform / complete-turn-hem-
  flare / half-step-to-lens / pivot-back-loop) and can be reused when Pass 2 reaches it.

RULE OF THUMB: GRWM = held/contained pose (Pass 2 skips them); everything else = full per-frame
pose/motion variety in Pass 2. Pass 1 must be complete on a file before Pass 2 touches it.

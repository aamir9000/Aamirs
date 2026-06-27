# Aira Prompt Rewrite — COMPLETE Standard, History & Resume Guide

Purpose: a single source of truth so any new session can resume with full context.
Repo: **aamir9000/Aamirs** · Branch: **aira-prompts-enhanced** (all work committed & pushed there).
Originals are preserved in git history / on `main`.

The job: take the master Aira concept `.txt` files and turn each into a clean,
AI-generation-ready (Nano Banana Pro stills + VEO video) version — additive only,
never deleting real descriptive content, and progressively raise them to the
"advanced" cinematic standard defined below.

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
  - Heavy-Detail/20 Reel Concepts Master-Depth Build.txt (140)
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

NEXT IN QUEUE (markdown SUBJECT ACTION WITH TIMING — use md_rebuild.py): Heavy-Detail/Master-Depth
Build (140), Concepts 91-110 (26), NEW Reel 131-150 (134), Time-Freeze (verify the 8 "oner"
frames first), Concept 100/170. Then non-standard: Magical Action · Master Set (advanced already;
only variable durations differ) and aira_set4 / aira_set5 (Format B).


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
already compliant; Master-Depth Build 01-07 are done. Now apply the section-B advanced video
rebuild PLUS the section-K Believability/Realism & Theme-Fidelity layer to the remaining
non-beauty files — 91-110, 131-150, aira_set4, aira_set5, Magical Action Master Set,
Time-Freeze, Concept 170/100, and Master-Depth 08-10. Keep every detail heavily; only change
what's necessary; controlled vibrancy; 6s real-time, no slow-mo; commit + push per concept;
tick the section-J audit. First, confirm the K.1 '8-10 concept' flag with the user."

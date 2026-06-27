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
- 20 Full Reel Set 5 (71-79) — studio couture transforms (image-heavy); vary crop/angle hard.
- Set 5 (cont 2) / · Set 5 (cont) / Set 5 cont 3 / cont 4 — couture/clothes-change; transform-led.
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

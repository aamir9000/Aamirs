# Aira Prompt Rewrite — Standard & Resume Guide

This file lets any new session resume the prompt-improvement work without losing context.
Branch: **aira-prompts-enhanced** (repo aamir9000/Aamirs). All work is committed/pushed there.

---

## PROGRESS TRACKER

### Done globally (all 20 files)
- Added `SUBJECT FRAMING & POSITION:` to every image prompt (with exact ORIENTATION LOCK clause).
- Stripped asterisks; removed internal codes (0 remain); restored 38 dropped descriptor words.
- Added one `MASTER AUDIO` block per concept (or kept existing per-concept brief — no duplicates).
- Set clip standard to **6 seconds**; `MASTER AUDIO` runtimes = frames x 6s; rescaled per-frame beat
  timings to fill 6s; all explicit `DURATION:` = 6s.
- Added a detailed **IDENTITY & CHARACTER-CONSISTENCY LOCK** to every video prompt (1,714 total),
  upgraded to the **expression-safe "fixed skeleton"** model.
- Removed duplicate files; grouped 7 heavily-detailed concepts into `CONCEPTS/Heavy-Detail/`.

### Done — ADVANCED video-prompt rebuild (the new standard below)
- **Beauty Ad Reels (Heavy-Detail/) — ALL 20 concepts, 129 video prompts. COMPLETE.**

### REMAINING — apply the ADVANCED rebuild to these files (queue):
1. 20 Cinematic Reels New Set.txt
2. 20 Full Reel Concepts Set 4 (Concepts 51.txt
3. 20 Full Reel Concepts Set 5 (Concepts 71.txt
4. 20 Full Reel Concepts Set 5 (cont 2).txt
5. 20 Full Reel Concepts · Set 5 (cont.txt
6. 20 Magical Action Reels Heavy-Detail.txt
7. 20 Magical Action Reels Set 2 Expression.txt
8. 20 More Full Reel Concepts Set 3.txt
9. Magical Action Reels · Master Set.txt
10. Set 5 (cont 3) Clothes-Change Transformation.txt
11. Set 5 (cont 4) · Clothes-Change Transformation.txt
12. aira_set4.txt
13. aira_set5.txt
14. Heavy-Detail/20 Reel Concepts Master-Depth Build.txt
15. Heavy-Detail/Concept 100 · The Unboxing.txt
16. Heavy-Detail/Concept 170 · Phoenix Crash.txt
17. Heavy-Detail/Concepts 91–110 · FULL Heavy-Detail.txt
18. Heavy-Detail/NEW Reel Concepts (131–150) .txt
19. Heavy-Detail/Time-Freeze Reel Set · Fully-Detailed Concepts.txt
(Note: some files use inline single-line video prompts / different headers — adapt the regex.)

---

## THE ADVANCED VIDEO-PROMPT STANDARD (what "rebuild" means)

For each concept: read it fully first, understand its world + dance/move, then rewrite ONLY where weak.

1. **Replace** the old `SUBJECT ACTION WITH TIMING:` block with a heavily-detailed
   `SHOT BREAKDOWN (timed, 6s · real-time …):` — 3 beats `[00:00–00:02] [00:02–00:04] [00:04–00:06]`,
   each beat = **shot size/angle + her action + object/world interaction + eye-led expression + camera move**.
2. **Dedup:** delete the standalone `CAMERA MOVEMENT:` and `CHOREOGRAPHY & FLUID MOTION:` lines
   (motion/camera now live only in the breakdown). Keep MICRO-MOVEMENT, LIGHTING, ENVIRONMENT, AUDIO, etc.
3. **Vary every frame** in crop (ECU/CU/half/cowboy/full/wide), angle (front/3-4/profile/low-hero/high/
   overhead/over-shoulder/symmetrical), and placement (centre/left/right/near/far) — no two frames alike.
4. **Camera grammar matched to the concept's dance/world** — orbit, dolly-in, crane/boom, tracking,
   whip-pan, arc, rack-focus, pull-out, snap-push — a distinct one per frame (not push-only).
5. **Already-in-motion starts:** every beat 1 opens with motion ALREADY in progress (anti-drift cold-start).
6. **Real-time, no slow-mo.** Replace FRAME RATE line with:
   `FRAME RATE + MOTION BLUR: 24fps, real-time playback at natural speed (no slow-motion), 180° shutter, natural motion blur.`
7. **Expressions:** eye-led and identity-safe — ONE smooth transition per clip (focus→wonder→smile),
   eyes tracing objects; tone-matched (playful/cute for light concepts, dramatic awe for serious ones).
   Big expression deformation causes Veo face-drift, so keep moderate.
8. **DURATION:** `DURATION: 6 seconds (the clip plays the full 6s at real-time natural speed).`
9. **Update FRAMING (image prompt)** + `SHOT TYPE` (video) per frame to the varied crop/angle/placement.
10. **Subconscious continuity:** vary every frame on the surface, but keep world/palette/identity/
    motion-hand-off/loop continuous so the reel feels like one piece.
11. Preserve: identity lock, scene detail, loop logic, spoken/silent (silent reels = no line, expression reveal).

---

## REUSABLE METHOD (how Beauty Ad was done)
Per-concept Python scripts authored the content and applied it (see `_tools/beauty_c*.py`). Pattern:
- Isolate a concept region (`# CONCEPT N` to `# CONCEPT N+1`), split by frame headers.
- IMAGE block: replace `^FRAMING:` line. VIDEO block: replace `^SHOT TYPE:`, delete `CAMERA MOVEMENT:`
  and `CHOREOGRAPHY & FLUID MOTION:`, replace `SUBJECT ACTION WITH TIMING:` block with the authored
  `SHOT BREAKDOWN`, replace `FRAME RATE` line, set `DURATION` to 6s.
- Verify: 0 leftover `SUBJECT ACTION WITH TIMING`, 0 `CAMERA MOVEMENT`, 0 non-negated `slow-mo`,
  breakdown count == video-prompt count, DURATION all 6s. Commit one concept/batch, push.
- Push tool: github power -> push_to_remote (never raw git push). Commit per concept/batch.

---

## RESUME PROMPT (paste into a new session)
"Continue the Aira prompt rebuild on branch aira-prompts-enhanced. Read
.kiro/steering/aira-prompt-rewrite-standard.md for the full standard and progress.
Beauty Ad is fully done. Continue applying the ADVANCED video-prompt rebuild to the
remaining files in the queue, one concept at a time, reading each fully first and
tailoring camera/expression to its world — then commit and push each."

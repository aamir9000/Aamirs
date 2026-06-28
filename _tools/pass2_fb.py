#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 2 — full-body explicit per-limb pose/motion engine (sections M.6-M.9).

Region/frame-scoped surgery on the Master-Depth-format files:
  - image  BODY POSTURE & WEIGHT:  -> full per-limb articulation (named L/R parts)
  - image  HANDS & NAILS:          -> explicit RIGHT/LEFT hand + fingers
  - image  SUBJECT FRAMING & POSITION: insert a per-limb dynamic-pose recap before ORIENTATION LOCK
  - video  SHOT BREAKDOWN 3 beats  -> per-limb motion across the beat

Authored per concept (no templating). A different head-to-toe combination each frame,
flow-read (each pose flows out of the previous and sets up the next), logical + self-aware,
identity-safe (face = eyes/gaze/head/soft-expression only). Run:
    python3 _tools/pass2_fb.py "<exact path>" <concept_number>

POSE[N] = { frame_int : {"posture":..., "hands":..., "framing":..., "b1":..,"b2":..,"b3":..} }
Only the keys present are applied; omit a frame to leave it untouched.
"""
import sys, re, io

POSE = {}

# ============================ CONCEPT 01 — STEEL TO SILK ============================
# Flow: F1 arrive onto mark / hand to hip (hero)  -> F2 lift right wrist to collarbone, study cuff
#   -> F3 unfold both arms open, palms up (receive) -> F4 transform: lift into a held-angle pivot
#   -> F5 settle out of turn, gather a silk fold at waist -> F6 turn to lens, offer the line by hand
#   -> F7 pivot back, return hand to hip (loop to F1). Powerful->serene, poised, architectural.
POSE[1] = {
 1: {
  "posture": "GAZE level and direct to lens; HEAD level with the chin lifted a hair, neck long; SHOULDERS squared with the left shoulder carried a touch forward, both blades down; RIGHT ARM bent and settling, the RIGHT HAND coming to rest light on the right hipbone with the steel cuff turned forward, RIGHT FINGERS relaxed and lightly splayed over the bone (no grip); LEFT ARM hanging long down her side, the LEFT HAND open and quiet, LEFT FINGERS extended and softly trailing; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a soft contrapposto with the right hip carried high; RIGHT LEG the free/forward leg, knee soft, toe just grazing the floor from the step she has just finished; LEFT LEG weight-bearing and straight beneath her; FEET & WEIGHT rolling back onto the left heel as the last step lands and settles; HAIR waves settling at the shoulder, the gown's ice-blue specular sliding as she squares up — grounded, architectural, alive (living stillness).",
  "hands": "RIGHT HAND resting light on the right hip with the steel cuff forward, RIGHT FINGERS naturally curved and lightly splayed over the hipbone with relaxed nail-beds and no white-knuckle tension; LEFT ARM long at her side, LEFT HAND open and quiet with LEFT FINGERS gently extended and trailing toward the thigh; short almond nails in a cool silver-nude gloss, cuticles neat.",
  "framing": "She has just strided onto her mark and settled — right hand landing light on the right hip, left arm long, weight rolling back onto the straight left leg with the right hip high and the right toe grazing, a poised arriving hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the steel studio: the camera dollies laterally to settle on her as she strides the last step onto her mark — weight rolling back onto the straight left leg, the right toe grazing, her right hand landing light on her hip with the brushed-steel cuff forward and her left arm long at her side; the gunmetal panels slide behind with real parallax and one ice-blue specular travels the bodice.",
  "b2": "The track eases to rest as her shoulders square, the left carried a touch forward, a face-framing finger-wave shifts in the cool draft and her level gaze lifts to lens, a composed powerful quarter-smile settling.",
  "b3": "She holds the architectural steel look, right hand on the hip, left fingers trailing, weight grounded through the left heel, eyes direct and cool as the specular slides the polished gunmetal (silent here).",
 },
 2: {
  "posture": "GAZE casting down to the cuff at her collarbone; HEAD tilted down about 8 degrees and a touch to the right; SHOULDERS with the RIGHT shoulder rolled up and forward as the arm lifts, the left dropped; RIGHT ARM folded up across the chest, the RIGHT HAND at the collarbone turning the brushed-steel cuff into the key, RIGHT FINGERS curved delicately around the metal; LEFT ARM crossing low over the body, the LEFT HAND resting at the opposite waist, LEFT FINGERS soft and flat; TORSO rotated about 4 degrees and dipping a touch toward the wrist; WAIST & HIPS holding the soft counter-tilt; RIGHT LEG eased forward with the toe down, LEFT LEG weight-bearing; FEET & WEIGHT planted, weight still on the left leg as she studies the cuff; HAIR drifting at the temple as the head dips.",
  "hands": "RIGHT HAND raised to the collarbone turning the steel cuff into the light, RIGHT FINGERS light and delicately curved on the metal with relaxed nail-beds; LEFT HAND resting soft at the opposite waist, LEFT FINGERS gently flat against the gown; short almond silver-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right arm is folded up to the collarbone turning the cuff with curved fingers while the left hand rests at the opposite waist, head dipped to study the steel, weight held on the straight left leg.",
  "b1": "Cut to a medium-close three-quarter on the cuff: she is already folding her right arm up across her chest, the right shoulder rolling forward, her right fingers turning the brushed-steel cuff into the cool key while her left hand settles at the opposite waist; the camera pushes with the wrist as her head dips and her gaze lowers to the steel.",
  "b2": "An ice-blue specular travels the turning cuff as her gaze cools with quiet focus and a knowing micro-smile kindles, the head canted a touch to the right.",
  "b3": "She studies the steel cuff, right fingers curved on the metal, left hand soft at the waist, weight steady on the left leg, lips parting a millimetre in composed calm — still fully steel.",
 },
 3: {
  "posture": "GAZE lifting from the cuff up toward lens; HEAD rising to level, chin lifting, neck lengthening; SHOULDERS drawing back and down, the blades pulling together; RIGHT ARM sweeping down and out from the chest, opening, the RIGHT HAND turning palm-up, RIGHT FINGERS fanning open; LEFT ARM mirroring out and open from the body, the LEFT HAND turning palm-up, LEFT FINGERS spread soft; TORSO lengthening, the ribcage lifting; WAIST & HIPS easing toward square with a gentle counter-tilt; RIGHT LEG straightening as weight shifts toward centre, LEFT LEG still the anchor; FEET & WEIGHT widening a touch as the stance opens, weight moving to centre between the feet; HAIR lifting off the shoulders as the chest opens.",
  "hands": "BOTH HANDS easing open from the body, palms turning up to receive the sweep — RIGHT FINGERS fanning open and LEFT FINGERS spread soft, both with relaxed nail-beds; short almond silver-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Both arms unfold open from her body, palms turning up with fingers fanning, ribcage lifted and shoulder-blades drawing together as her weight eases to centre between widening feet — an opening, receiving pose.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she sweeps both arms down and open from her chest, palms turning up and fingers fanning open, the shoulder-blades drawing together as her weight eases to centre between widening feet; the camera arcs a few degrees and the panels swing behind with parallax as her gaze begins to lift.",
  "b2": "The arc settles as her chin lifts and her gaze rises to lens with rising calm, a serene knowing micro-smile forming, the ribcage lengthening — the gunmetal still at its sharpest cool polish.",
  "b3": "She holds the poised steel beat, both palms open and ready, fingers spread, weight centred and grounded, eyes calm and architectural — the composed breath before the change (silent here).",
 },
 4: {
  "posture": "GAZE lifting up into the move then warming; HEAD turning a few degrees to lead the body, chin level; SHOULDERS opening wide with the right shoulder leading the turn; RIGHT ARM sweeping up and out, the RIGHT HAND rising palm-outward, RIGHT FINGERS extending long and elegant; LEFT ARM opening out and back as a counterweight, the LEFT HAND trailing, LEFT FINGERS soft and drifting; TORSO beginning a slow spiral, ribcage lifted; WAIST & HIPS initiating a pivot, weight transferring across; RIGHT LEG taking the weight as she rises onto the ball of the right foot, LEFT LEG extending free and back with the heel lifting; FEET & WEIGHT mid-pivot, weight rolling onto the right foot — the body turns while the camera angle holds.",
  "hands": "BOTH ARMS opening into the move — the RIGHT HAND rising palm-outward with RIGHT FINGERS extending long and elegant, the LEFT HAND trailing back as a counterweight with LEFT FINGERS soft and drifting; short almond silver-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She lifts into the start of a pivot — right arm sweeping up palm-out with long fingers, left arm trailing back as counterweight, rising onto the ball of the right foot with the left heel lifting, the spine spiralling while the camera angle holds.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the steel Look A still): she is already lifting into a slow pivot — right arm sweeping up and out palm-outward, left arm trailing back as counterweight, rising onto the ball of her right foot with the left heel lifting — a gentle push-with easing toward her, the steel look fully intact, NO change yet, the angle fixed for the whole clip.",
  "b2": "The morph BEGINS here, mid-clip: a warm dissolve-front starts at her near shoulder and travels smoothly and diagonally down across the gown in one continuous liquid wavefront as her torso spirals through the turn, polished gunmetal turning to flowing champagne silk exactly where it passes — gradual and motivated, never a snap; eyes warming in serene awe as it crosses (angle held, identity locked).",
  "b3": "The wavefront completes its sweep as she settles through the pivot and the look resolves smoothly and fully into the champagne-silk Look B of the Veo last-frame still (Frame 5's image), held through the final beat — no last-second pop; a soft serene warmth landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing to lens, soft; HEAD settling to level with a gentle tilt; SHOULDERS easing down out of the turn, the right shoulder now carried slightly back; RIGHT ARM lowering, the RIGHT HAND drifting to the waist to gather a soft fold of champagne silk, RIGHT FINGERS curling gently around the fabric; LEFT ARM easing down and a touch out, the LEFT HAND open near the hip, LEFT FINGERS relaxed; TORSO unwinding from the turn, settling to about 4 degrees rotation; WAIST & HIPS re-finding a serene counter-tilt as weight settles onto the back leg; RIGHT LEG easing to free and forward, soft; LEFT LEG re-taking weight, straight; FEET & WEIGHT re-grounding from the pivot, settling onto the left foot; HAIR and silk drape settling soft from the spin.",
  "hands": "RIGHT HAND drifting to the waist to gather a soft fold of champagne silk, RIGHT FINGERS curling gently around the fabric with warm-nude nail-beds; LEFT HAND easing open near the hip, LEFT FINGERS relaxed and lightly curved; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Unwinding from the turn, her right hand drifts to her waist gathering a fold of silk with curling fingers while the left hand eases open at the hip and her weight settles serene onto the straight left leg.",
  "b1": "Cut to a medium close on a new angle in the warmed silk space: she is already settling out of the pivot, her right hand drifting to her waist to gather a soft fold of champagne silk with curling fingers while her left hand eases open near the hip; a slow push eases in and warm motes settle as her gaze eases to lens.",
  "b2": "A serene smile eases to lens on a slow warm breath, the weight settling onto her straight left leg, a warm specular travelling the satin cowl, eyes soft and luminous.",
  "b3": "She holds the warm serene silk look, right fingers curled in the gathered fold, left hand open at the hip, the drape settling soft, eyes shining direct (silent here).",
 },
 6: {
  "posture": "GAZE warm and direct to lens; HEAD turning a soft six degrees toward lens, chin level; SHOULDERS soft with the left carried a touch forward; RIGHT ARM extending from the waist out toward lens in a soft presenting gesture, the RIGHT HAND opening palm-up-and-out, RIGHT FINGERS gently spread; LEFT HAND resting soft on the gathered silk at the waist, LEFT FINGERS light; TORSO turning softly with the head; WAIST & HIPS in a gentle sway, weight rolling between the feet; RIGHT LEG easing forward as she turns, LEFT LEG bearing then sharing the weight; FEET & WEIGHT grounded with a slight pivot toward lens; HAIR swinging soft with the turn, the pearl drop swinging a hair.",
  "hands": "RIGHT HAND drifting open from the silk fold out toward the lens in a soft presenting gesture as she speaks, RIGHT FINGERS gently spread with warm-nude nail-beds; LEFT HAND resting soft on the gathered silk at the waist, LEFT FINGERS light and relaxed; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She turns a soft six degrees to lens and extends her right hand open from the silk in a presenting gesture while the left rests on the gathered fold, hips swaying gently as her weight rolls between the feet for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she turns a soft six degrees toward lens and extends her right hand open from the gathered silk out toward lens in a soft presenting gesture, the left hand resting on the fold, her hips swaying as weight rolls between the feet; the camera eases with her, gaze warm to lens.",
  "b2": "She delivers \u201cSteel to silk. Same power, softer edge.\u201d to lens with a soft knowing smile and natural lip-sync, right fingers gently spread on the gesture, the pearl drop swinging a hair, eyes warm and direct.",
  "b3": "She holds the warm serene look as the silk settles and her right hand eases back toward the waist, the smile easing into calm.",
 },
 7: {
  "posture": "GAZE easing back to the composed direct-to-lens of Frame 1; HEAD returning to level with the chin a hair lifted; SHOULDERS squaring back to the opening set, the left carried a touch forward; RIGHT ARM bending back as the RIGHT HAND returns to rest light on the right hip wrist-forward, RIGHT FINGERS relaxed and lightly splayed; LEFT ARM lowering long to the side, the LEFT HAND open with LEFT FINGERS trailing; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip high; RIGHT LEG easing to free and forward soft, LEFT LEG re-taking the weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance on a settling half-step; HAIR settling to the opening set.",
  "hands": "RIGHT HAND returning to rest light on the right hip exactly as in Frame 1 with the wrist forward, RIGHT FINGERS naturally curved and lightly splayed over the hipbone; LEFT ARM long at the side, LEFT HAND open with LEFT FINGERS gently trailing; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She pivots back precisely to the opening hook — right hand returning light to the hip, left arm long with trailing fingers, weight settling onto the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she pivots back and returns her right hand to rest light on her hip with the wrist forward, her left arm lowering long with fingers trailing, settling her weight onto the straight left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her gaze back to lens on a slow breath with the composed quarter-smile, the shoulders squaring to the opening set, the silk-warm space resolving toward the steel-cool opening palette to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand on the hip, left fingers trailing, weight settled and architectural — a seamless loop seam.",
 },
}


# ============================ CONCEPT 03 — SAREE TO STREETWEAR ============================
# Flow: F1 arrive regal / right hand at pallu -> F2 lift a fold of zari to collarbone, study it
#   -> F3 open both hands to release the drape -> F4 transform: open into a held-angle turn, saree unwinds
#   -> F5 settle out of turn in streetwear, adjust the bomber collar -> F6 stride to lens, line + open gesture
#   -> F7 pivot back, hand to pallu (loop). Regal grace -> cool spirited stride ("new stride").
POSE[3] = {
 1: {
  "posture": "GAZE warm and direct to lens; HEAD level with the chin lifted a hair, neck long and regal; SHOULDERS open with the right shoulder carried back a touch; RIGHT ARM raised and bent, the RIGHT HAND resting light at the gold-zari pallu where it falls over the shoulder, RIGHT FINGERS grazing the silk softly; LEFT ARM long down her side with the bangles soft on the wrist, the LEFT HAND open, LEFT FINGERS gently trailing; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a graceful contrapposto with the right hip carried high; RIGHT LEG the free/forward leg, knee soft, toe grazing from the step just finished; LEFT LEG weight-bearing and straight; FEET & WEIGHT rolling back onto the left heel as the last graceful step settles; HAIR tendrils settling at the cheek as the courtyard draft moves them — grounded, regal, alive (living stillness).",
  "hands": "RIGHT HAND raised resting light at the zari pallu over the shoulder, RIGHT FINGERS softly grazing the silk with relaxed nail-beds; LEFT ARM long at her side with the bangles soft on the wrist, LEFT HAND open with LEFT FINGERS gently trailing; short almond nails in a warm rose-nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just stepped regally onto her mark — right hand raised light to the pallu over her shoulder, left arm long with bangles, weight rolling back onto the straight left leg with the right hip high and the right toe grazing, a poised heritage hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the marigold-lit haveli courtyard: the camera dollies laterally to settle on her as she steps the last graceful pace onto her mark — weight rolling back onto the straight left leg, the right toe grazing, her right hand rising light to the gold-zari pallu over her shoulder and her left arm long with bangles soft; the sandstone arches and incense haze slide behind with real parallax.",
  "b2": "The track eases to rest as a face-framing tendril shifts in the courtyard draft and her warm gaze lifts to lens, the right shoulder carried back a touch, a regal quarter-smile settling.",
  "b3": "She holds the warm regal saree look, right fingers grazing the pallu, left bangles soft, weight grounded through the left heel, eyes warm and direct as the gold zari glints in the tungsten glow (silent here).",
 },
 2: {
  "posture": "GAZE lowering to the gold zari at her collarbone; HEAD dipping about 8 degrees toward the wrist; SHOULDERS with the RIGHT shoulder rolled gently forward as the hand lifts; RIGHT ARM folded up near the chest, the RIGHT HAND holding a fold of the zari pallu into the light, RIGHT FINGERS light and curved on the silk; LEFT ARM crossing low, the LEFT HAND soft at the waist, LEFT FINGERS flat and easy; TORSO rotated about 4 degrees and dipping toward the wrist; WAIST & HIPS holding the soft counter-tilt; RIGHT LEG eased forward toe-down, LEFT LEG weight-bearing; FEET & WEIGHT planted, weight on the left leg as she studies the thread; HAIR drifting at the temple as the head dips.",
  "hands": "RIGHT HAND raised near the collarbone holding a fold of the gold-zari pallu into the light, RIGHT FINGERS light and curved on the silk with relaxed nail-beds; LEFT HAND soft at the waist, LEFT FINGERS flat and easy; short almond rose-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand lifts a fold of the zari pallu to the collarbone with curved fingers while the left rests soft at the waist, head dipped to study the gold thread, weight held on the straight left leg.",
  "b1": "Cut to a medium-close three-quarter on the pallu: she is already folding her right arm up near her chest, the right shoulder rolling forward, her right fingers lifting a fold of the gold zari into the warm key while her left hand settles at the waist; the camera pushes with her hand as her head dips and her gaze lowers to the thread.",
  "b2": "A warm specular travels the zari as her gaze warms with quiet focus and a knowing micro-smile kindles, the head canted toward the wrist.",
  "b3": "She studies the glowing pallu, right fingers curved on the silk, left hand soft at the waist, weight steady on the left leg, lips parting a millimetre in regal calm — still fully saree.",
 },
 3: {
  "posture": "GAZE lifting from the silk up toward lens; HEAD rising to level, chin lifting; SHOULDERS drawing back and down, blades gathering; RIGHT ARM easing down and out, the RIGHT HAND turning palm-outward as if to release the drape, RIGHT FINGERS fanning open; LEFT ARM opening out from the body, the LEFT HAND turning palm-out, LEFT FINGERS spreading soft; TORSO lengthening, ribcage lifting; WAIST & HIPS easing toward square with a gentle counter-tilt; RIGHT LEG straightening as weight eases to centre, LEFT LEG still anchoring; FEET & WEIGHT widening a touch as the stance opens; HAIR lifting off the shoulders as the chest opens.",
  "hands": "BOTH HANDS easing open from the body, palms turning out as if to release the drape — RIGHT FINGERS fanning open and LEFT FINGERS spreading soft, both with relaxed nail-beds; short almond rose-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Both arms open out from her body, palms turning to release the drape with fingers fanning, ribcage lifted and blades gathering as her weight eases to centre between widening feet — a spirited opening pose.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she eases both arms open from her body, palms turning out as if to release the drape and fingers fanning open, the blades gathering as her weight eases to centre between widening feet; the camera arcs a few degrees and the courtyard swings behind with parallax as her gaze begins to lift.",
  "b2": "The arc settles as her chin lifts and her gaze rises to lens with rising spirit and a knowing micro-smile forms, the ribcage lengthening, the magenta silk still richly draped and fully intact.",
  "b3": "She holds the poised saree beat, both palms open and ready to release, fingers spread, weight centred and grounded, eyes bright and spirited — the breath before the unwind (silent here).",
 },
 4: {
  "posture": "GAZE lifting up into the move with spirited joy; HEAD turning a few degrees to lead the spiral, chin level; SHOULDERS opening wide, right shoulder leading; RIGHT ARM sweeping up and out, the RIGHT HAND rising palm-outward, RIGHT FINGERS extending long; LEFT ARM opening out and back as a counterweight, the LEFT HAND trailing, LEFT FINGERS soft; TORSO beginning a slow spiral, ribcage lifted; WAIST & HIPS initiating a pivot as weight transfers; RIGHT LEG taking weight onto the ball of the right foot, LEFT LEG extending free and back with the heel lifting; FEET & WEIGHT mid-pivot — the body spirals while the camera angle holds.",
  "hands": "BOTH ARMS opening into the spiral — the RIGHT HAND rising palm-outward with RIGHT FINGERS extending long, the LEFT HAND trailing back as counterweight with LEFT FINGERS soft and drifting; short rose-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She lifts into the start of a spiralling turn — right arm sweeping up palm-out with long fingers, left arm trailing back as counterweight, rising onto the ball of the right foot with the left heel lifting, the spine spiralling while the camera angle holds.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the magenta-saree Look A still): she is already lifting into a spiralling turn — right arm sweeping up and out palm-outward, left arm trailing back as counterweight, rising onto the ball of her right foot with the left heel lifting — a gentle push-with easing in, the saree fully draped and intact, NO change yet, the angle fixed for the whole clip.",
  "b2": "The morph BEGINS here, mid-clip: a cooling unwind-front starts at the pallu on her shoulder and spirals smoothly down and around her in one continuous ribbon as her torso spirals through the turn, the magenta silk and gold zari unwinding and reforming into the cream-and-graphite bomber and tapered cargos exactly where it passes — gradual and liquid, never a snap; eyes bright with spirited joy as it crosses (angle held, identity locked).",
  "b3": "The ribbon completes its spiral as she settles through the pivot and the look resolves smoothly and fully into the streetwear Look B of the Veo last-frame still (Frame 5's image), held through the final beat — no last-second pop; an easy cool confidence landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing to lens, cool and bright; HEAD settling level with a slight cant; SHOULDERS easing with an easy roll of the right as the hand lifts; RIGHT ARM rising, the RIGHT HAND reaching up to adjust the bomber collar, RIGHT FINGERS lightly pinching the collar-edge; LEFT ARM easing down, the LEFT HAND resting at the crossbody strap, LEFT FINGERS hooked loosely; TORSO unwinding from the turn to about 4 degrees rotation; WAIST & HIPS finding an easy counter-tilt as weight settles onto the back leg; RIGHT LEG easing free and forward, soft; LEFT LEG re-taking weight, knee soft; FEET & WEIGHT re-grounding from the pivot with a small settling step; HAIR settling cool from the spin.",
  "hands": "RIGHT HAND reaching up to adjust the bomber collar with an easy shoulder roll, RIGHT FINGERS lightly pinching the collar-edge with soft-nude nail-beds; LEFT HAND resting at the crossbody strap, LEFT FINGERS hooked loosely over it; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Settling out of the turn into streetwear, her right hand reaches up to adjust the bomber collar with an easy shoulder roll while the left hooks the crossbody strap, weight settling onto the soft-bent left leg.",
  "b1": "Cut to a medium close on a new angle in the cool mural-street light: she is already settling out of the spin in the cream-and-graphite bomber and cargos, her right hand reaching up to adjust the collar with an easy roll of the right shoulder while her left hooks the crossbody strap; gaze easing to lens.",
  "b2": "A confident smile eases to lens on a slow cool breath, her weight settling onto the soft left leg, the last motes settling, eyes relaxed and direct.",
  "b3": "She holds the cool easy streetwear look, right fingers easing off the collar, left hooked on the strap, the bomber settling soft, eyes relaxed and bright (silent here).",
 },
 6: {
  "posture": "GAZE cool and direct to lens; HEAD turning a soft six degrees toward lens, chin level; SHOULDERS easy with the left carried forward as she strides; RIGHT ARM swinging open from the bomber out toward lens in a relaxed gesture, the RIGHT HAND opening palm-up-and-out, RIGHT FINGERS loosely spread; LEFT HAND resting easy on the crossbody strap, LEFT FINGERS hooked; TORSO turning easily with the stride; WAIST & HIPS swaying with a confident step, weight transferring forward; RIGHT LEG stepping forward into the new stride, LEFT LEG pushing off behind; FEET & WEIGHT mid-stride, weight rolling onto the forward right foot; HAIR swinging soft with the step, the small gold hoops catching light.",
  "hands": "RIGHT HAND swinging open from the bomber out toward lens in a relaxed presenting gesture as she speaks, RIGHT FINGERS loosely spread with soft-nude nail-beds; LEFT HAND resting easy on the crossbody strap, LEFT FINGERS hooked over it; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She steps a confident stride toward lens and swings her right hand open in a relaxed gesture while the left stays hooked on the crossbody strap, hips swaying as her weight rolls onto the forward right foot for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she steps a confident new stride toward lens, her right hand swinging open from the bomber in a relaxed gesture while the left stays hooked on the crossbody strap, hips swaying as weight rolls onto the forward right foot; the camera eases with her, gaze cool to lens.",
  "b2": "She delivers \u201cSaree to streetwear. Same roots, new stride.\u201d to lens with a soft knowing smile and natural lip-sync, right fingers loosely spread on the gesture, the small gold hoops catching light, eyes warm and cool-confident.",
  "b3": "She holds the cool easy look as the bomber settles and her right hand eases back toward the strap, the smile easing into relaxed warmth.",
 },
 7: {
  "posture": "GAZE easing back to the warm direct-to-lens of Frame 1; HEAD returning level with the chin a hair lifted; SHOULDERS squaring back with the right carried back a touch; RIGHT ARM rising back as the RIGHT HAND returns to rest light at the pallu over the shoulder, RIGHT FINGERS grazing the silk; LEFT ARM lowering long with the bangles, the LEFT HAND open, LEFT FINGERS trailing; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip high; RIGHT LEG easing to free and forward soft, LEFT LEG re-taking weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance on a settling step; HAIR settling to the opening set.",
  "hands": "RIGHT HAND returning to rest light at the zari pallu over the shoulder exactly as in Frame 1, RIGHT FINGERS softly grazing the silk; LEFT ARM long with bangles, LEFT HAND open with LEFT FINGERS trailing; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She pivots back precisely to the opening hook — right hand returning light to the pallu over the shoulder, left arm long with bangles, weight settling onto the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she pivots back and returns her right hand to rest light at the zari pallu over her shoulder, her left arm lowering long with bangles, settling her weight onto the straight left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her gaze back to lens on a slow breath with the composed regal quarter-smile, the shoulders squaring to the opening set, the cool street palette resolving toward the warm courtyard opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand at the pallu, left bangles soft, weight settled and regal — a seamless loop seam.",
 },
}


# ----------------------------------------------------------------------------------
def find_concept_region(text, n):
    m = re.search(r'##\s*CONCEPT\s*0*%d\b' % n, text)
    if not m:
        raise SystemExit("CONCEPT %d not found" % n)
    start = m.start()
    m2 = re.search(r'##\s*CONCEPT\s*0*%d\b' % (n + 1), text[start + 5:])
    end = (start + 5 + m2.start()) if m2 else len(text)
    return start, end

def frame_blocks(region, k):
    """Return (img_span, vid_span) as (start,end) tuples within region for frame k."""
    im = re.search(r'###\s*Frame\s*%d\s*of\s*\d+\s*[\u2014-]\s*IMAGE PROMPT' % k, region)
    vm = re.search(r'###\s*Frame\s*%d\s*of\s*\d+\s*[\u2014-]\s*VIDEO PROMPT' % k, region)
    if not im or not vm:
        return None, None
    img_start = im.start()
    img_end = vm.start()
    # video ends at next "### Frame" or end of region
    nxt = re.search(r'###\s*Frame\s*%d\s*of' % (k + 1), region)
    vid_end = nxt.start() if nxt else len(region)
    return (img_start, img_end), (vm.start(), vid_end)

def replace_line(block, field, newval):
    """Replace a single-line 'FIELD: ...' within block. Returns (block, count)."""
    pat = re.compile(r'(?m)^' + re.escape(field) + r':[^\n]*$')
    if not pat.search(block):
        return block, 0
    return pat.sub(field + ': ' + newval.replace('\\', '\\\\'), block, count=1), 1

def insert_framing_pose(block, pose):
    anchor = " ORIENTATION LOCK \u2014 preserve this exact left-to-right composition; do not mirror, flip or invert the frame."
    if anchor not in block:
        return block, 0
    return block.replace(anchor, " " + pose + anchor, 1), 1

def replace_beat(block, tc, newtext):
    pat = re.compile(r'(?m)^- \[' + re.escape(tc) + r'\][^\n]*$')
    if not pat.search(block):
        return block, 0
    return pat.sub('- [' + tc + '] ' + newtext.replace('\\', '\\\\'), block, count=1), 1

def apply_concept(text, n):
    data = POSE.get(n)
    if not data:
        raise SystemExit("No POSE data for concept %d" % n)
    cs, ce = find_concept_region(text, n)
    region = text[cs:ce]
    report = []
    # process frames high-to-low so spans stay valid as we splice
    for k in sorted(data.keys(), reverse=True):
        fd = data[k]
        ib, vb = frame_blocks(region, k)
        if ib is None:
            report.append("F%d: BLOCK NOT FOUND" % k); continue
        # IMAGE block
        img = region[ib[0]:ib[1]]
        c = 0
        if "posture" in fd:
            img, n1 = replace_line(img, "BODY POSTURE & WEIGHT", fd["posture"]); c += n1
        if "hands" in fd:
            img, n2 = replace_line(img, "HANDS & NAILS", fd["hands"]); c += n2
        if "framing" in fd:
            img, n3 = insert_framing_pose(img, fd["framing"]); c += n3
        region = region[:ib[0]] + img + region[ib[1]:]
        # recompute video block (image length may have changed)
        ib2, vb2 = frame_blocks(region, k)
        vid = region[vb2[0]:vb2[1]]
        cv = 0
        if "b1" in fd:
            vid, m1 = replace_beat(vid, "00:00\u201300:02", fd["b1"]); cv += m1
        if "b2" in fd:
            vid, m2 = replace_beat(vid, "00:02\u201300:04", fd["b2"]); cv += m2
        if "b3" in fd:
            vid, m3 = replace_beat(vid, "00:04\u201300:06", fd["b3"]); cv += m3
        region = region[:vb2[0]] + vid + region[vb2[1]:]
        report.append("F%d: image edits=%d, beat edits=%d" % (k, c, cv))
    text = text[:cs] + region + text[ce:]
    return text, report


def main():
    if len(sys.argv) < 3:
        raise SystemExit("usage: pass2_fb.py <path> <concept_number>")
    path = sys.argv[1]; n = int(sys.argv[2])
    with io.open(path, encoding='utf-8') as f:
        text = f.read()
    text, report = apply_concept(text, n)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("CONCEPT %d:" % n)
    for r in sorted(report):
        print("  " + r)

if __name__ == '__main__':
    main()

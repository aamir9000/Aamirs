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


# ============================ CONCEPT 04 — SEASON TURN ============================
# Flow: F1 arrive serene by the tree / hand at fishtail braid -> F2 reach up to a low blossom branch, graze petals
#   -> F3 open both hands to feel the turning air -> F4 transform: open arms, four-season ring sweeps (held angle)
#   -> F5 winter reveal, adjust the scarf at the neck -> F6 soft turn to lens, line + mittened gesture
#   -> F7 ease back, hand to braid (loop). Energy soft / flowing / wondrous (a gentle step + turn, never strident).
POSE[4] = {
 1: {
  "posture": "GAZE calm and direct to lens; HEAD level with the chin a hair lifted, neck long; SHOULDERS soft and open, the right carried back a touch; RIGHT ARM raised and bent, the RIGHT HAND resting light at the fishtail braid where it falls over the shoulder, RIGHT FINGERS softly threading the braid; LEFT ARM relaxed and long at her side, the LEFT HAND open, LEFT FINGERS gently trailing; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a soft contrapposto with the right hip carried high; RIGHT LEG the free/forward leg, knee soft, toe grazing the meadow grass from the step just finished; LEFT LEG weight-bearing and straight; FEET & WEIGHT settling back onto the left foot in the soft grass; HAIR wisps drifting at the cheek in the spring breeze — grounded, serene, alive (living stillness).",
  "hands": "RIGHT HAND raised resting light at the fishtail braid over the shoulder, RIGHT FINGERS softly threading the braid with relaxed nail-beds; LEFT ARM long and relaxed at her side, LEFT HAND open with LEFT FINGERS gently trailing; short almond nails in a soft rose-nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just stepped softly onto her mark beneath the tree — right hand raised light to the fishtail braid over her shoulder, left arm long, weight settling back onto the straight left leg with the right hip high and the right toe grazing the grass, a serene arriving hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot by the lone meadow tree in spring: the camera dollies laterally to settle on her as she steps softly onto her mark — weight settling onto the straight left leg, the right toe grazing the grass, her right hand rising light to the fishtail braid over her shoulder and her left arm long at her side; pink blossom and the tree slide behind with real parallax.",
  "b2": "The track eases to rest as a face-framing wisp shifts in the spring breeze, the right shoulder carried back a touch, and her calm gaze lifts to lens, the serene quarter-smile settling, petals drifting in the soft sky-light.",
  "b3": "She holds the serene spring look in her cream knit and dusty-rose cardigan, right fingers threading the braid, left fingers trailing, weight grounded through the left foot, eyes calm and direct (silent here).",
 },
 2: {
  "posture": "GAZE lifting toward a low blossom branch; HEAD tilting up about 6 degrees and toward the branch; SHOULDERS with the RIGHT shoulder lifting as the arm reaches up; RIGHT ARM extending up and out, the RIGHT HAND reaching beneath the petals, RIGHT FINGERS spread soft and grazing the blossom; LEFT ARM eased up, the LEFT HAND resting soft at the braid, LEFT FINGERS light; TORSO lengthening upward toward the branch with a gentle reach; WAIST & HIPS easing as she rises slightly into the reach; RIGHT LEG taking a little more weight as she reaches up, LEFT LEG soft behind; FEET & WEIGHT rolling forward onto the balls of the feet in the reach; HAIR wisps lifting as she tips her head up.",
  "hands": "RIGHT HAND reaching up beneath a low blossom branch, RIGHT FINGERS spread soft and grazing the petals with relaxed nail-beds; LEFT HAND resting soft at the braid, LEFT FINGERS light; short almond rose-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right arm reaches up beneath a low blossom branch with fingers grazing the petals while the left rests at the braid, torso lengthening upward and weight rolling onto the balls of the feet in the gentle reach.",
  "b1": "Cut to a medium-close three-quarter: she is already reaching her right arm up beneath a low blossom branch, fingers spreading soft to graze the petals as her torso lengthens and her weight rolls onto the balls of her feet, the left hand resting at the braid; the camera pushes with her hand, gaze toward the blossom.",
  "b2": "The petals stir at her fingertips as her gaze warms with quiet wonder and a knowing micro-smile kindles, the head tipped gently up.",
  "b3": "A petal lifts free past her spread fingers, her eyes soft on the blossom, weight poised on the balls of her feet, lips parting a millimetre in gentle wonder — still full spring.",
 },
 3: {
  "posture": "GAZE easing down from the branch and lifting to lens; HEAD settling level; SHOULDERS easing back and down, blades softening; RIGHT ARM lowering and opening out from the body, the RIGHT HAND turning palm-up to feel the air, RIGHT FINGERS opening soft; LEFT ARM opening out to the other side, the LEFT HAND turning palm-up, LEFT FINGERS spreading gently; TORSO settling tall, ribcage lifting on the breath; WAIST & HIPS easing toward square with a gentle counter-tilt; RIGHT LEG settling back to even as weight eases to centre, LEFT LEG sharing; FEET & WEIGHT settling flat and even, weight centred; HAIR settling at the shoulders.",
  "hands": "BOTH HANDS easing open and out from the body, palms turning up to feel the turning air — RIGHT FINGERS opening soft and LEFT FINGERS spreading gently, both with relaxed nail-beds; short almond rose-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Both arms ease open and out, palms turning up to feel the turning air with fingers softening, ribcage lifting on the breath as her weight settles even and centred between the feet — a serene, receiving pose.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she eases both hands open and out from her body, palms turning up to feel the air and fingers softening, her weight settling even and centred as the ribcage lifts; the camera arcs a few degrees and the spring meadow swings behind with parallax, gaze beginning to lift.",
  "b2": "The arc settles as her gaze lifts to lens with rising wonder and a knowing micro-smile forms, the chest open, the canopy still in full spring blossom.",
  "b3": "She holds the poised spring beat, both palms open to the air, fingers soft, weight even and grounded, eyes bright with wonder — the breath before the seasons turn (silent here).",
 },
 4: {
  "posture": "GAZE lifting up and around with serene wonder; HEAD turning softly to follow the travelling ring, chin level; SHOULDERS opening wide and even; RIGHT ARM lifting up and out, the RIGHT HAND rising palm-up to the turning air, RIGHT FINGERS opening long; LEFT ARM opening out and back as a gentle counterweight, the LEFT HAND palm-up, LEFT FINGERS soft; TORSO lengthening and beginning a slow open turn from the waist; WAIST & HIPS easing into a gentle rotation as weight rolls; RIGHT LEG taking weight as she turns softly on the ball of the right foot, LEFT LEG easing free with the heel lifting a touch; FEET & WEIGHT in a slow grounded turn — the body turns softly while the camera angle holds.",
  "hands": "BOTH ARMS opening to the turning air — the RIGHT HAND rising palm-up with RIGHT FINGERS opening long, the LEFT HAND opening back as a gentle counterweight with LEFT FINGERS soft; short soft-rose nails, neat cuticles, no white-knuckle tension.",
  "framing": "She opens into a slow soft turn at centre — right arm lifting palm-up to the air with long fingers, left arm opening back as counterweight, turning gently on the ball of the right foot while the camera angle holds.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the spring Look A still): she is already opening into a slow soft turn at centre — right arm lifting up palm-up to the air with long fingers, left arm opening back as a gentle counterweight, turning on the ball of her right foot — full spring blossom and her dusty-rose cardigan intact, NO change yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The four-season turn BEGINS here, mid-clip: a travelling ring sweeps smoothly around her in one continuous wavefront as her torso turns softly through it — spring blossom giving to summer green, then to autumn leaf-fall as it passes, the tree, ground, light and her layers turning along the same front (cardigan easing to the bare summer dress, then a camel trench and rust scarf forming), gradual and continuous, never a snap; eyes wide with wonder as it crosses (angle held, identity locked).",
  "b3": "The ring completes its turn as she settles softly out of the rotation and the look resolves smoothly and fully into the winter Look B of the Veo last-frame still (Frame 5's image) — cream wool coat, oatmeal scarf and knit beanie under soft snow, held through the final beat, no last-second pop; a serene grounded calm landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing to lens, calm; HEAD settling level with a soft cant; SHOULDERS easing with a soft roll of the right as the hand lifts; RIGHT ARM rising, the mittened RIGHT HAND reaching up to adjust the scarf at her neck, RIGHT FINGERS soft in the mitten pinching the wool; LEFT ARM easing down, the LEFT HAND resting at the coat front, LEFT FINGERS soft; TORSO settling tall out of the turn to about 4 degrees rotation; WAIST & HIPS finding a calm counter-tilt as weight settles onto the back leg; RIGHT LEG easing free and forward soft in the snow, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the turn with a small settling step in the snow; HAIR settling under the beanie.",
  "hands": "Mittened RIGHT HAND reaching up to adjust the scarf at her neck with an easy shoulder roll, RIGHT FINGERS soft in the mitten pinching the wool, soft-rose nails beneath; LEFT HAND resting at the coat front, LEFT FINGERS soft; neat cuticles, no white-knuckle tension.",
  "framing": "Settling out of the turn into winter, her mittened right hand reaches up to adjust the scarf at her neck with an easy shoulder roll while the left rests at the coat front, weight settling onto the back leg in the snow.",
  "b1": "Cut to a medium close on a new angle in soft falling snow: she is already settling out of the turn in the cream wool coat and oatmeal scarf, her mittened right hand reaching up to adjust the scarf at her neck with an easy roll of the right shoulder while the left rests at the coat front; gaze easing to lens.",
  "b2": "A serene smile eases to lens on a slow cool breath, her weight settling onto the back leg, the last flakes settling around her, eyes calm and direct.",
  "b3": "She holds the calm cosy winter look, the mittened right hand easing off the scarf, left soft at the coat, eyes serene and bright (silent here).",
 },
 6: {
  "posture": "GAZE calm and direct to lens; HEAD turning a soft six degrees toward lens, chin level; SHOULDERS soft with the left carried a touch forward; RIGHT ARM opening from the coat out toward lens in a relaxed gesture, the mittened RIGHT HAND turning open, RIGHT FINGERS soft in the mitten; LEFT HAND resting easy at the coat, LEFT FINGERS soft; TORSO turning softly with the head; WAIST & HIPS in a gentle sway, weight rolling between the feet; RIGHT LEG easing forward with a small soft step, LEFT LEG behind sharing weight; FEET & WEIGHT grounded in the snow with a gentle pivot toward lens; HAIR shifting soft under the beanie, snow drifting.",
  "hands": "Mittened RIGHT HAND opening from the coat out toward lens in a soft relaxed gesture as she speaks, RIGHT FINGERS soft in the mitten; LEFT HAND resting easy at the coat, LEFT FINGERS soft; soft-rose nails beneath, neat cuticles, no white-knuckle tension.",
  "framing": "She turns a soft six degrees to lens with a small step and opens her mittened right hand in a relaxed gesture while the left rests at the coat, hips swaying gently as her weight rolls between the feet for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she turns a soft six degrees toward lens with a small step and opens her mittened right hand out from the coat in a relaxed gesture, the left resting at the coat, hips swaying as weight rolls between the feet; the camera eases with her, gaze calm to lens.",
  "b2": "She delivers \u201cSeasons change. I don\u2019t.\u201d to lens with a soft serene smile and natural lip-sync, the mittened right hand soft on the gesture, soft snow drifting, eyes calm and warm.",
  "b3": "She holds the calm cosy look as the coat settles and her right hand eases back, the smile easing into grounded warmth.",
 },
 7: {
  "posture": "GAZE easing back to the calm direct-to-lens of Frame 1; HEAD returning level with the chin a hair lifted; SHOULDERS softening back, the right carried back a touch; RIGHT ARM rising back as the RIGHT HAND returns to rest light at the fishtail braid over the shoulder, RIGHT FINGERS threading the braid; LEFT ARM lowering long, the LEFT HAND open, LEFT FINGERS trailing; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip high; RIGHT LEG easing to free and forward soft, LEFT LEG re-taking weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance; HAIR settling to the opening set as the snow resolves toward blossom.",
  "hands": "RIGHT HAND returning to rest light at the fishtail braid over the shoulder exactly as in Frame 1, RIGHT FINGERS softly threading the braid; LEFT ARM long, LEFT HAND open with LEFT FINGERS trailing; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases back precisely to the opening hook — right hand returning light to the fishtail braid, left arm long with trailing fingers, weight settling onto the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she eases back and returns her right hand to rest light at the fishtail braid over her shoulder, her left arm lowering long with fingers trailing, settling her weight onto the straight left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her calm gaze back to lens on a slow breath with the composed serene quarter-smile, the shoulders softening to the opening set, the winter palette resolving toward the spring blossom opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand at the braid, left fingers trailing, weight settled and serene — a seamless loop seam.",
 },
}


# ============================ CONCEPT 05 — THE SNAP ============================
# Flow: F1 arrive power-stance / snap-ready hand at chest -> F2 raise snapping hand to cheek, pressed ready
#   -> F3 press fingers hard at snap-point, left hand opens -> F4 SNAP: light-pulse sweep black->white (held angle)
#   -> F5 white reveal, adjust lapel, confident set -> F6 sharp stride to lens, line + gesture
#   -> F7 pivot back to snap-ready (loop). Energy sharp / editorial / playful spark (attitude, hip-pop, stride).
POSE[5] = {
 1: {
  "posture": "GAZE bold and direct to lens; HEAD level with a slight chin lift, neck long and sharp; SHOULDERS squared and strong, the right rising a touch as the hand comes up; RIGHT ARM bent up to chest height, the RIGHT HAND poised with thumb and middle finger lightly together ready to snap, RIGHT FINGERS crisp and deliberate; LEFT ARM long and relaxed at her side, the LEFT HAND open, LEFT FINGERS lightly curved; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a sharp contrapposto with the right hip popped; RIGHT LEG the free/forward leg, knee soft, toe planted from the step just landed; LEFT LEG weight-bearing and straight in a confident wide stance; FEET & WEIGHT planted strong on the left foot in an editorial power stance; HAIR fringe-edge shifting crisp in the studio air — grounded, sharp, alive (living stillness).",
  "hands": "RIGHT HAND raised to chest height with thumb and middle finger lightly together ready to snap, RIGHT FINGERS crisp and deliberate with relaxed nail-beds; LEFT ARM long at her side, LEFT HAND open with LEFT FINGERS lightly curved; short almond nails in a deep berry-nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just landed into a confident wide power stance — right hand poised at chest height with thumb and middle finger ready to snap, left arm long, weight planted strong on the straight left leg with the right hip popped, a sharp editorial hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot against the graphite cyclorama: the camera dollies laterally to settle on her as she lands into a confident wide power stance — weight planting strong on the straight left leg, the right hip popping, her right hand rising to chest height with thumb and middle finger together ready to snap and her left arm long; the studio slides behind with real parallax.",
  "b2": "The track eases to rest as a fringe edge shifts in the studio air, the right shoulder rising a touch, and her bold gaze lifts to lens, a playful spark settling at the outer eye.",
  "b3": "She holds the sharp all-black editorial look, right fingers poised to snap, left hand easy, weight planted on the left foot, eyes direct and bold (silent here).",
 },
 2: {
  "posture": "GAZE cutting sharp to the poised fingers; HEAD turning about 10 degrees toward the hand and tipping in; SHOULDERS with the RIGHT shoulder lifting as the hand rises to the cheek; RIGHT ARM folded up to the cheek, the RIGHT HAND with thumb and middle finger pressed ready to snap, RIGHT FINGERS taut and deliberate; LEFT ARM easing across low, the LEFT HAND soft at the waist, LEFT FINGERS flat; TORSO rotated about 4 degrees, coiling a touch toward the hand; WAIST & HIPS holding the popped counter-tilt; RIGHT LEG eased forward toe-planted, LEFT LEG bearing weight; FEET & WEIGHT planted, weight on the left leg as she eyes the fingers; HAIR fringe shifting as the head tips in.",
  "hands": "RIGHT HAND raised near the cheek with thumb and middle finger pressed ready to snap, the gesture crisp and deliberate, RIGHT FINGERS taut with relaxed nail-beds; LEFT HAND soft at the waist, LEFT FINGERS flat; short almond berry-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand rises to the cheek with thumb and middle finger pressed crisp and ready while the left rests at the waist, head tipping toward the fingers, weight coiled on the straight left leg.",
  "b1": "Cut to a medium-close three-quarter: she is already raising the snapping hand to her cheek, thumb and middle finger pressing crisp and ready, her left hand settling at the waist as the camera pushes with her hand; gaze cutting to the fingers.",
  "b2": "Her gaze sharpens with playful focus on the fingertips as a knowing micro-smile kindles, the head tipped in toward the hand.",
  "b3": "Her fingers hold pressed and poised at the cheek, left hand soft at the waist, weight coiled on the left leg, eyes bright and playful, the all-black set crisp and intact — the hush before the snap (silent here).",
 },
 3: {
  "posture": "GAZE bright, flicking from the fingers up toward lens; HEAD lifting to level; SHOULDERS squaring and dropping ready to release; RIGHT ARM holding at the snap-point at chest, the RIGHT HAND with thumb and middle finger pressed hard, RIGHT FINGERS tensed to release; LEFT ARM easing open and out from the body, the LEFT HAND turning open, LEFT FINGERS spreading; TORSO lengthening, coiling tall on the breath; WAIST & HIPS easing toward a charged square with the hip still set; RIGHT LEG settling firmer as weight centres a touch, LEFT LEG anchoring; FEET & WEIGHT widening into a charged ready stance; HAIR settling crisp as she squares up.",
  "hands": "RIGHT HAND at the snap-point with thumb and middle finger pressed hard ready to release, RIGHT FINGERS tensed and deliberate; LEFT HAND easing open at her side, LEFT FINGERS spreading; short almond berry-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right fingers press hard at the chest-height snap-point while the left hand opens at her side, the torso coiling tall and the stance widening into a charged ready pose.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she presses her thumb and middle finger hard at the chest-height snap-point and eases her left hand open and spreading, coiling tall on a slow breath as the camera arcs a few degrees and the cyclorama swings behind with parallax; gaze flicking up.",
  "b2": "The arc settles as her gaze lifts to lens with rising spark and a knowing micro-smile forms, the stance widening charged, the all-black set still crisp and fully intact.",
  "b3": "She holds the poised black beat, right fingers tensed at the snap-point, left hand open, weight set in the charged stance, eyes bright and ready — the charged instant before the snap (silent here).",
 },
 4: {
  "posture": "GAZE wide and bright into the move; HEAD held sharp and level, a crisp micro-recoil with the snap; SHOULDERS snapping open and down with the release; RIGHT ARM driving the snap at chest height, the RIGHT HAND releasing thumb off middle finger, RIGHT FINGERS flicking crisp and extending on the snap; LEFT ARM flaring open and out as a sharp counterweight, the LEFT HAND opening, LEFT FINGERS spread; TORSO giving a crisp editorial pop with the snap, ribcage lifting; WAIST & HIPS popping sharp with the beat; RIGHT LEG taking weight as she sets onto the right foot with the pop, LEFT LEG bracing; FEET & WEIGHT set strong and wide on the snap — the body pops crisp while the camera angle holds.",
  "hands": "RIGHT HAND driving the snap at chest height, thumb releasing off the middle finger and RIGHT FINGERS flicking crisp and extending; LEFT ARM flaring open as a sharp counterweight, LEFT HAND open with LEFT FINGERS spread; short berry-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She drives the snap at chest height — right fingers flicking crisp off the thumb, left arm flaring open as counterweight, the torso popping sharp onto the set right foot, the editorial pop landing while the camera angle holds.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the all-black Look A still): she holds the snap-ready pose, already in motion — right hand poised at chest, left arm set — the sharp black set fully intact, NO change yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The change BEGINS here, mid-clip: she snaps her fingers crisp (thumb flicking off the middle finger, fingers extending) with a sharp editorial body-pop, and a clean light-pulse rings out and sweeps across her in one quick continuous wavefront, the all-black tailored set flipping to the bold sculptural all-white set exactly where the pulse passes — crisp and clean but smooth, starting here in the middle, never an instant last-second cut; the bob catching travelling light, eyes wide with playful spark (angle held, identity locked).",
  "b3": "The pulse completes its sweep as her body settles strong out of the pop and the look resolves smoothly and fully into the all-white Look B of the Veo last-frame still (Frame 5's image), held through the final beat — no last-second pop; a sharp confidence landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing sharp to lens; HEAD settling level with a crisp cant; SHOULDERS easing with a sharp roll of the right as the hand lifts; RIGHT ARM rising, the RIGHT HAND reaching up to adjust the white lapel, RIGHT FINGERS pinching the lapel-edge crisp; LEFT ARM easing to the hip, the LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; TORSO settling tall out of the pop to about 4 degrees rotation; WAIST & HIPS finding a confident counter-tilt with the hip set as weight settles onto the back leg; RIGHT LEG easing free and forward, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the pop with a confident settling step; HAIR settling crisp.",
  "hands": "RIGHT HAND reaching up to adjust the white lapel with a sharp shoulder roll, RIGHT FINGERS pinching the lapel-edge crisp with clean soft-red nail-beds; LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Settling out of the snap into the white set, her right hand reaches up to adjust the lapel with a sharp shoulder roll while the left settles on the popped hip, weight settling onto the back leg in a confident set.",
  "b1": "Cut to a medium close on a new angle in brighter white-studio light: she is already in the bold all-white set, her right hand reaching up to adjust the white lapel with a sharp roll of the right shoulder while her left settles on the hip; gaze easing to lens.",
  "b2": "A sharp confident smile eases to lens on a slow breath, her weight settling onto the back leg with the hip set, the last light-sparks settling, eyes sharp and direct.",
  "b3": "She holds the assured all-white editorial look, right fingers easing off the lapel, left set on the hip, the white set crisp, eyes sharp and bright (silent here).",
 },
 6: {
  "posture": "GAZE bold and direct to lens; HEAD turning a sharp six degrees toward lens, chin level; SHOULDERS sharp with the left carried forward as she steps; RIGHT ARM swinging open toward lens in a crisp gesture, the RIGHT HAND opening palm-out, RIGHT FINGERS sharply spread; LEFT HAND resting easy at the white lapel, LEFT FINGERS light; TORSO turning crisp with the stride; WAIST & HIPS swaying sharp with a confident step, weight transferring forward; RIGHT LEG stepping forward into a sharp stride, LEFT LEG pushing off behind; FEET & WEIGHT mid-stride, weight rolling onto the forward right foot; HAIR snapping soft with the step.",
  "hands": "RIGHT HAND swinging open toward lens in a crisp sharp gesture as she speaks, RIGHT FINGERS sharply spread with soft-red nail-beds; LEFT HAND resting easy at the white lapel, LEFT FINGERS light; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She steps a sharp stride toward lens and swings her right hand open in a crisp gesture while the left rests at the lapel, hips swaying sharp as her weight rolls onto the forward right foot for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she steps a sharp stride toward lens, her right hand swinging open in a crisp gesture while the left rests at the white lapel, hips swaying as weight rolls onto the forward right foot; the camera eases with her, gaze direct to lens.",
  "b2": "She delivers \u201cOne snap. New me.\u201d to lens with a sharp knowing smile and natural lip-sync, right fingers sharply spread on the gesture, eyes bold and direct.",
  "b3": "She holds the assured editorial look as the white set settles and her right hand eases back toward the lapel, the smile easing into sharp calm.",
 },
 7: {
  "posture": "GAZE easing back to the bold direct-to-lens of Frame 1; HEAD returning level with a slight chin lift; SHOULDERS squaring back strong, the right rising a touch; RIGHT ARM bending back up to chest height as the RIGHT HAND returns to the poised snap-ready pose, RIGHT FINGERS with thumb and middle finger lightly together; LEFT ARM lowering long, the LEFT HAND open, LEFT FINGERS lightly curved; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the popped contrapposto; RIGHT LEG easing to free and forward, LEFT LEG re-taking weight straight in the wide power stance; FEET & WEIGHT re-grounding into the exact Frame-1 stance; HAIR settling crisp as the white resolves toward graphite.",
  "hands": "RIGHT HAND returning to the poised snap-ready pose at chest height exactly as in Frame 1 with thumb and middle finger lightly together, RIGHT FINGERS crisp; LEFT ARM long, LEFT HAND open with LEFT FINGERS lightly curved; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She pivots back precisely to the opening hook — right hand returning to the snap-ready pose at chest height, left arm long, weight planted strong on the straight left leg in the Frame-1 power stance for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she pivots back and returns her right hand to the poised snap-ready pose at chest height, her left arm lowering long, planting her weight strong on the straight left leg in the opening power stance with the hip popped exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her gaze back to lens on a slow breath with the composed sharp quarter-smile, the shoulders squaring to the opening set, the white palette resolving toward the graphite opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right fingers snap-ready, left hand easy, weight planted and sharp — a seamless loop seam.",
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

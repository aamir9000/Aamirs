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


# ============================ CONCEPT 06 — MIDNIGHT BLOOM (fragrance · GENTLE) ============================
# Flow: F1 cradle flacon at waist (moonlit garden) -> F2 raise flacon to collarbone, index at atomizer
#   -> F3 press atomizer, fine mist releases -> F4 ease flacon down, night-blooms bloom open (held angle)
#   -> F5 lower flacon to waist, radiant reveal -> F6 soft sway to lens, line + gentle gesture -> F7 loop.
# GENTLE: still radiant centre — per-limb articulated but soft (gentle sway, soft weight-shift, a drift); NO stride.
POSE[6] = {
 1: {
  "posture": "GAZE soft and direct to lens; HEAD level with a gentle tilt, neck long; SHOULDERS soft and even, the right carried a touch forward over the flacon; RIGHT ARM bent low, the RIGHT HAND cradling the fragrance flacon softly at waist height, RIGHT FINGERS curved gently around the glass; LEFT ARM soft at her side, the LEFT HAND resting light against the midnight-blue satin gown, LEFT FINGERS relaxed; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a soft contrapposto with the right hip a touch high; RIGHT LEG the free/forward leg, knee soft, toe lightly grazing; LEFT LEG weight-bearing and easy; FEET & WEIGHT settled gently onto the left foot in the garden hush; HAIR tendrils drifting at the cheek in the night breeze — still, romantic, alive (living stillness).",
  "hands": "RIGHT HAND cradling the fragrance flacon softly at waist height, RIGHT FINGERS curved gently around the glass with relaxed nail-beds; LEFT HAND resting light against the gown, LEFT FINGERS relaxed; short almond nails in a soft rose, neat cuticles, no white-knuckle tension.",
  "framing": "She stands the still radiant centre — right hand cradling the flacon softly at waist height with curved fingers, left hand light against the satin, weight settled gently onto the easy left leg with the right hip a touch high.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the moonlit night garden: the camera dollies laterally to settle on her as she eases her weight gently onto her left leg and cradles the fragrance flacon at waist height with curved right fingers, her left hand light against the satin; the dark closed night-blooms and trellis slide behind with real parallax.",
  "b2": "The track eases to rest as a face-framing tendril drifts in the night breeze, the right shoulder soft over the flacon, and her serene gaze eases to lens, low ground-mist curling.",
  "b3": "She holds, romantic and still in the midnight-blue satin, right fingers cradling the flacon, left hand soft at the gown, eyes gentle in the moon glow, the buds dark and closed around her (silent here).",
 },
 2: {
  "posture": "GAZE softening down toward the flacon; HEAD tilting down about 6 degrees and toward the hand; SHOULDERS with the RIGHT shoulder lifting gently as the flacon rises; RIGHT ARM folding up near the collarbone, the RIGHT HAND raising the flacon with the index finger resting at the atomizer, RIGHT FINGERS poised and soft; LEFT ARM easing across low, the LEFT HAND soft at the waist, LEFT FINGERS relaxed; TORSO easing about 4 degrees toward the flacon; WAIST & HIPS holding the soft counter-tilt; RIGHT LEG eased forward soft, LEFT LEG bearing weight; FEET & WEIGHT planted gentle, weight on the left leg; HAIR drifting soft at the temple.",
  "hands": "RIGHT HAND raising the flacon near the collarbone with the index finger resting at the atomizer poised to mist, RIGHT FINGERS soft around the glass; LEFT HAND soft at the waist, LEFT FINGERS relaxed; short almond soft-rose nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand raises the flacon to the collarbone with the index finger poised at the atomizer while the left rests soft at the waist, head tilting gently toward the flacon, weight easy on the left leg.",
  "b1": "Cut to a medium-close three-quarter: she is already raising the flacon near her collarbone, her right index finger settling at the atomizer while her left hand rests soft at the waist, the right shoulder lifting gently as the camera pushes with her hand; gaze easing toward the flacon.",
  "b2": "Her gaze softens toward the flacon as a dreamy micro-smile kindles, the head tilted gently in, she drawing a slow breath.",
  "b3": "She holds the flacon poised at her collarbone, right index at the atomizer, left hand soft at the waist, eyes soft and dreamy, the night blooms still dark and closed behind (silent here).",
 },
 3: {
  "posture": "GAZE lifting softly from the flacon toward lens; HEAD easing to level; SHOULDERS easing back soft; RIGHT ARM holding the flacon up, the RIGHT HAND pressing the atomizer with the index, RIGHT FINGERS soft on the press; LEFT ARM easing open at her side, the LEFT HAND turning open, LEFT FINGERS softening; TORSO settling tall on a slow breath; WAIST & HIPS easing toward soft-square with a gentle counter-tilt; RIGHT LEG easing back to even, LEFT LEG sharing; FEET & WEIGHT settling gently even; HAIR settling soft at the shoulders.",
  "hands": "RIGHT INDEX pressing the atomizer to release the mist, RIGHT FINGERS soft around the flacon; LEFT HAND easing open at her side, LEFT FINGERS softening; short almond soft-rose nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right index presses the atomizer to mist while the left hand eases open soft at her side, the torso settling tall on the breath as her weight eases gently even between the feet.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she presses the atomizer with her right index and a fine fragrance-mist releases, her left hand easing open soft at her side as her weight settles gently even; the camera arcs a few degrees and the trellis swings behind with parallax, gaze beginning to lift.",
  "b2": "The arc settles as her gaze lifts to lens with rising warmth and a tender micro-smile forms, the chest soft and open, the buds still closed dark in the moonlight.",
  "b3": "She holds the poised mist beat, right fingers soft on the flacon, left hand open, the fine mist drifting, eyes warm with wonder — the breath before the bloom (silent here).",
 },
 4: {
  "posture": "GAZE lifting with tender wonder, then widening soft; HEAD easing softly to follow the bloom-wave, chin level; SHOULDERS soft and open; RIGHT ARM easing the flacon down from the mist, the RIGHT HAND lowering soft, RIGHT FINGERS curved around the glass; LEFT ARM soft and open at her side, the LEFT HAND turned gently open, LEFT FINGERS soft; TORSO settling tall with a soft breath, the gentlest sway toward the opening blooms; WAIST & HIPS easing in a soft sway as weight rolls gently; RIGHT LEG soft and forward, LEFT LEG easy beneath; FEET & WEIGHT rolling gently on the spot — she stays the still radiant centre while the bloom moves around her, the camera angle held.",
  "hands": "RIGHT HAND easing the flacon down from the mist, RIGHT FINGERS curved soft around the glass; LEFT ARM soft and open at her side, LEFT HAND turned gently open with LEFT FINGERS soft; short soft-rose nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases the flacon down from the mist with curved fingers, the left hand opening soft, her torso swaying the gentlest touch toward the opening blooms as the wave rolls around her still radiant centre, the camera angle held.",
  "b1": "Cut to an ethereal medium at a HELD angle (Veo first frame = the closed-bud Look A still): she eases the flacon down from the mist with curved right fingers, her left hand opening soft, the gentlest sway toward the blooms — the night-flowers still closed dark buds, NO bloom yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The bloom BEGINS here, mid-clip: from the fragrance mist a soft bloom-wave rolls out and travels smoothly around her in one continuous expanding front, the closed dark buds unfurling open pale and luminous exactly where the wave passes — petals opening on believable soft spring, fine luminous pollen-motes drifting like real flecks, gradual and tender, never a snap; her head easing softly to follow it, eyes widening in radiant wonder (angle held, identity locked).",
  "b3": "The bloom-wave completes its sweep as she sways gently back to centre and the garden resolves smoothly and fully into the full-bloom Look B of the Veo last-frame still (Frame 5's image) — pale luminous flowers open across the trellis and vines, held through the final beat, no last-second pop; a soft radiant calm landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing soft to lens; HEAD settling level with a gentle tilt; SHOULDERS easing with a soft roll of the right; RIGHT ARM lowering, the RIGHT HAND drifting to rest the flacon at her waist, RIGHT FINGERS curved soft around it; LEFT ARM easing down, the LEFT HAND resting light at the gown, LEFT FINGERS soft; TORSO settling tall and soft to about 4 degrees rotation; WAIST & HIPS finding a serene counter-tilt as weight settles gently onto the left leg; RIGHT LEG easing free and forward soft; LEFT LEG re-taking the easy weight; FEET & WEIGHT settling gentle onto the left foot among the open blooms; HAIR settling soft.",
  "hands": "RIGHT HAND drifting to rest the flacon at her waist with an easy shoulder roll, RIGHT FINGERS curved soft around the glass with soft-rose nail-beds; LEFT HAND resting light at the gown, LEFT FINGERS soft; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Among the open blooms, her right hand drifts to rest the flacon at her waist with curved fingers while the left rests light at the gown, weight settling gently onto the easy left leg in a serene centre.",
  "b1": "Cut to a medium close on a new angle amid the bloomed garden: she is already lowering the flacon to rest at her waist with an easy roll of the right shoulder, her left hand resting light at the gown, pale blooms open around her; gaze easing to lens.",
  "b2": "A soft radiant smile eases to lens on a slow breath, her weight settling onto the easy left leg, the last pollen-motes settling among the open blooms, eyes soft and luminous.",
  "b3": "She holds the serene radiant look, right fingers soft on the flacon at her waist, left hand at the gown, the blooms breathing pale around her, eyes soft and direct (silent here).",
 },
 6: {
  "posture": "GAZE warm and direct to lens; HEAD turning a soft six degrees toward lens with a gentle tilt; SHOULDERS soft with the left carried a touch forward; RIGHT ARM drifting open soft from the waist toward lens, the RIGHT HAND turning gently open, RIGHT FINGERS soft and relaxed; LEFT HAND resting easy with the flacon at the waist, LEFT FINGERS soft; TORSO turning softly with the head; WAIST & HIPS in the gentlest sway, weight rolling soft between the feet; RIGHT LEG easing forward a soft touch, LEFT LEG bearing the easy weight; FEET & WEIGHT settled gentle with the softest pivot toward lens; HAIR drifting soft, blooms breathing behind.",
  "hands": "RIGHT HAND drifting open soft from the waist toward the lens in a gentle gesture as she speaks, RIGHT FINGERS soft and relaxed; LEFT HAND resting easy with the flacon at the waist, LEFT FINGERS soft; short almond soft-rose nails, neat cuticles, no white-knuckle tension.",
  "framing": "She turns a soft six degrees to lens and drifts her right hand open in a gentle gesture while the left holds the flacon easy at the waist, hips swaying the gentlest touch as her weight rolls soft between the feet for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she turns a soft six degrees toward lens and drifts her right hand open from the waist in a gentle gesture, the left holding the flacon easy, her hips swaying the gentlest touch as weight rolls soft between the feet; the camera eases with her, gaze warm to lens.",
  "b2": "She delivers \u201cSome nights, you just bloom.\u201d to lens with a soft radiant smile and natural lip-sync, right fingers soft on the gesture, eyes warm and serene.",
  "b3": "She holds the serene look as the bloomed petals breathe soft and her right hand eases back to the waist, the smile easing into calm radiance.",
 },
 7: {
  "posture": "GAZE easing back to the soft direct-to-lens of Frame 1; HEAD returning level with a gentle tilt; SHOULDERS softening back, the right a touch forward over the flacon; RIGHT ARM lowering back as the RIGHT HAND returns to cradle the flacon at waist height, RIGHT FINGERS curved gently around the glass; LEFT ARM soft at her side, the LEFT HAND light at the gown, LEFT FINGERS relaxed; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip a touch high; RIGHT LEG easing to free and forward soft, LEFT LEG re-taking the easy weight; FEET & WEIGHT settling gently into the exact Frame-1 stance; HAIR settling soft as the open blooms resolve toward closed buds.",
  "hands": "RIGHT HAND returning to cradle the flacon at waist height exactly as in Frame 1, RIGHT FINGERS curved gently around the glass; LEFT HAND light at the gown, LEFT FINGERS relaxed; short almond soft-rose nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases back precisely to the opening hook — right hand cradling the flacon at waist height with curved fingers, left hand light at the gown, weight settling gently onto the easy left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she eases the flacon back to cradle at waist height with curved right fingers, her left hand resting light at the gown, settling her weight gently onto the easy left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her serene gaze back to lens on a slow breath with the composed half-smile, the shoulders softening to the opening set, the open blooms resolving toward the closed-bud opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand cradling the flacon, left hand at the gown, weight settled in the moonlight — a seamless loop seam.",
 },
}

# ============================ CONCEPT 07 — GOLD HOUR (fragrance · GENTLE) ============================
# Flow: F1 cradle flacon at waist (golden rooftop) -> F2 raise flacon to collarbone, index at atomizer
#   -> F3 press atomizer, fine mist -> F4 ease flacon down, sunbeams turn to gold-dust spiral (held angle)
#   -> F5 lower flacon to waist, radiant reveal -> F6 soft sway to lens, line + gentle gesture -> F7 loop.
# GENTLE: still warm centre — per-limb articulated but soft; NO stride. Palette warm champagne-gold / low sun.
POSE[7] = {
 1: {
  "posture": "GAZE warm and direct to lens; HEAD level with a gentle tilt toward the low sun, neck long; SHOULDERS soft and even, the right carried a touch forward over the flacon; RIGHT ARM bent low, the RIGHT HAND cradling the amber flacon softly at waist height, RIGHT FINGERS curved gently around the glass; LEFT ARM soft at her side, the LEFT HAND resting light against the champagne-gold satin dress, LEFT FINGERS relaxed; TORSO rotated about 6 degrees to open the right shoulder toward the sun; WAIST & HIPS in a soft contrapposto with the right hip a touch high; RIGHT LEG the free/forward leg, knee soft, toe lightly grazing; LEFT LEG weight-bearing and easy; FEET & WEIGHT settled gently onto the left foot on the warm rooftop; HAIR wisps drifting at the cheek in the rooftop breeze — still, warm, alive (living stillness).",
  "hands": "RIGHT HAND cradling the amber flacon softly at waist height, RIGHT FINGERS curved gently around the glass with relaxed nail-beds; LEFT HAND resting light against the dress, LEFT FINGERS relaxed; short almond nails in a warm nude, neat cuticles, no white-knuckle tension.",
  "framing": "She stands the still warm centre — right hand cradling the amber flacon softly at waist height with curved fingers, left hand light against the satin, weight settled gently onto the easy left leg with the right shoulder open to the low sun.",
  "b1": "Cut to a medium-wide thigh-up tracking shot on the warm golden-hour rooftop: the camera dollies laterally to settle on her as she eases her weight gently onto her left leg and cradles the amber flacon at waist height with curved right fingers, her left hand light against the satin; the hazy gold skyline and rooftop edge slide behind with real parallax.",
  "b2": "The track eases to rest as a face-framing wisp drifts in the rooftop breeze, the right shoulder open to the sun, and her serene gaze eases to lens, the low sun warm on the satin.",
  "b3": "She holds, warm and still in the champagne-gold satin, right fingers cradling the flacon, left hand soft at the dress, eyes gentle in the low sun, the light plain and golden around her (silent here).",
 },
 2: {
  "posture": "GAZE softening down toward the flacon; HEAD tilting down about 6 degrees and toward the hand; SHOULDERS with the RIGHT shoulder lifting gently as the flacon rises, gilded by the sun; RIGHT ARM folding up near the collarbone, the RIGHT HAND raising the flacon with the index finger resting at the atomizer, RIGHT FINGERS poised and soft; LEFT ARM easing across low, the LEFT HAND soft at the waist, LEFT FINGERS relaxed; TORSO easing about 4 degrees toward the flacon; WAIST & HIPS holding the soft counter-tilt; RIGHT LEG eased forward soft, LEFT LEG bearing weight; FEET & WEIGHT planted gentle, weight on the left leg; HAIR drifting soft at the temple, the chignon gilding.",
  "hands": "RIGHT HAND raising the flacon near the collarbone with the index finger resting at the atomizer poised to mist, RIGHT FINGERS soft around the glass; LEFT HAND soft at the waist, LEFT FINGERS relaxed; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand raises the flacon to the collarbone with the index poised at the atomizer while the left rests soft at the waist, head tilting gently toward the flacon, the low sun gilding the chignon, weight easy on the left leg.",
  "b1": "Cut to a medium-close three-quarter: she is already raising the flacon near her collarbone, her right index finger settling at the atomizer while her left hand rests soft at the waist, the right shoulder lifting gently as the camera pushes with her hand; gaze easing toward the flacon.",
  "b2": "Her gaze softens toward the flacon as a dreamy micro-smile kindles, the head tilted gently in, she drawing a slow breath, the low sun gilding the chignon.",
  "b3": "She holds the flacon poised at her collarbone, right index at the atomizer, left hand soft at the waist, eyes soft and dreamy, the light still plain golden behind (silent here).",
 },
 3: {
  "posture": "GAZE lifting softly from the flacon toward lens; HEAD easing to level; SHOULDERS easing back soft; RIGHT ARM holding the flacon up, the RIGHT HAND pressing the atomizer with the index, RIGHT FINGERS soft on the press; LEFT ARM easing open at her side, the LEFT HAND turning open, LEFT FINGERS softening; TORSO settling tall on a slow breath; WAIST & HIPS easing toward soft-square with a gentle counter-tilt; RIGHT LEG easing back to even, LEFT LEG sharing; FEET & WEIGHT settling gently even; HAIR settling soft, gilded at the edges.",
  "hands": "RIGHT INDEX pressing the atomizer to release the mist, RIGHT FINGERS soft around the flacon; LEFT HAND easing open at her side, LEFT FINGERS softening; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right index presses the atomizer to mist while the left hand eases open soft at her side, the torso settling tall on the breath as her weight eases gently even between the feet in the low sun.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she presses the atomizer with her right index and a fine fragrance-mist releases, her left hand easing open soft at her side as her weight settles gently even; the camera arcs a few degrees and the rooftop swings behind with parallax, gaze beginning to lift.",
  "b2": "The arc settles as her gaze lifts to lens with rising warmth and a tender micro-smile forms, the chest soft and open, the light still plain golden-hour sun.",
  "b3": "She holds the poised mist beat, right fingers soft on the flacon, left hand open, the fine mist drifting in the low sun, eyes warm with wonder — the breath before the wrap (silent here).",
 },
 4: {
  "posture": "GAZE lifting with tender wonder, then widening soft; HEAD easing softly to follow the gold-dust spiral, chin level; SHOULDERS soft and open; RIGHT ARM easing the flacon down from the mist, the RIGHT HAND lowering soft, RIGHT FINGERS curved around the glass; LEFT ARM soft and open at her side, the LEFT HAND turned gently open, LEFT FINGERS soft; TORSO settling tall with a soft breath, the gentlest sway into the gilding air; WAIST & HIPS easing in a soft sway as weight rolls gently; RIGHT LEG soft and forward, LEFT LEG easy beneath; FEET & WEIGHT rolling gently on the spot — she stays the still warm centre while the gold-dust spirals around her, the camera angle held.",
  "hands": "RIGHT HAND easing the flacon down from the mist, RIGHT FINGERS curved soft around the glass; LEFT ARM soft and open at her side, LEFT HAND turned gently open with LEFT FINGERS soft; short warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases the flacon down from the mist with curved fingers, the left hand opening soft, her torso swaying the gentlest touch into the gilding air as the gold-dust spiral wraps around her still warm centre, the camera angle held.",
  "b1": "Cut to an ethereal medium at a HELD angle (Veo first frame = the plain golden-light Look A still): she eases the flacon down from the mist with curved right fingers, her left hand opening soft, the gentlest sway into the gilding air — the light still plain golden-hour sun, NO gold-dust yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The wrap BEGINS here, mid-clip: from the fragrance mist the low sunbeams visibly turn to fine gold dust and spiral smoothly around her in one continuous travelling ring, the air and satin edges gilding exactly where the spiral passes — fine gold motes streaming on believable airborne drift like real flecks, gradual and tender, never a snap; her head easing softly to follow it, eyes widening in radiant wonder (angle held, identity locked).",
  "b3": "The gold-dust spiral completes its sweep as she sways gently back to centre and the scene resolves smoothly and fully into the full gold-dust-wrap Look B of the Veo last-frame still (Frame 5's image) — fine luminous gold dust wrapped around her in the warm light, held through the final beat, no last-second pop; a soft radiant calm landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing soft to lens; HEAD settling level with a gentle tilt; SHOULDERS easing with a soft roll of the right; RIGHT ARM lowering, the RIGHT HAND drifting to rest the flacon at her waist, RIGHT FINGERS curved soft around it; LEFT ARM easing down, the LEFT HAND resting light at the dress, LEFT FINGERS soft; TORSO settling tall and soft to about 4 degrees rotation; WAIST & HIPS finding a serene counter-tilt as weight settles gently onto the left leg; RIGHT LEG easing free and forward soft; LEFT LEG re-taking the easy weight; FEET & WEIGHT settling gentle onto the left foot in the gilded air; HAIR settling soft, gold motes drifting.",
  "hands": "RIGHT HAND drifting to rest the flacon at her waist with an easy shoulder roll, RIGHT FINGERS curved soft around the glass with warm-nude nail-beds; LEFT HAND resting light at the dress, LEFT FINGERS soft; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "In the gilded gold-dust air, her right hand drifts to rest the flacon at her waist with curved fingers while the left rests light at the dress, weight settling gently onto the easy left leg in a serene warm centre.",
  "b1": "Cut to a medium close on a new angle in the gilded gold-dust air: she is already lowering the flacon to rest at her waist with an easy roll of the right shoulder, her left hand resting light at the dress, fine gold motes drifting around her; gaze easing to lens.",
  "b2": "A soft radiant smile eases to lens on a slow breath, her weight settling onto the easy left leg, the last gold motes settling in the warm light, eyes soft and luminous.",
  "b3": "She holds the serene radiant look, right fingers soft on the flacon at her waist, left hand at the dress, the gold dust drifting warm around her, eyes soft and direct (silent here).",
 },
 6: {
  "posture": "GAZE warm and direct to lens; HEAD turning a soft six degrees toward lens with a gentle tilt; SHOULDERS soft with the left carried a touch forward; RIGHT ARM drifting open soft from the waist toward lens, the RIGHT HAND turning gently open, RIGHT FINGERS soft and relaxed; LEFT HAND resting easy with the flacon at the waist, LEFT FINGERS soft; TORSO turning softly with the head; WAIST & HIPS in the gentlest sway, weight rolling soft between the feet; RIGHT LEG easing forward a soft touch, LEFT LEG bearing the easy weight; FEET & WEIGHT settled gentle with the softest pivot toward lens; HAIR drifting soft, gold dust shimmering behind.",
  "hands": "RIGHT HAND drifting open soft from the waist toward the lens in a gentle gesture as she speaks, RIGHT FINGERS soft and relaxed; LEFT HAND resting easy with the flacon at the waist, LEFT FINGERS soft; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She turns a soft six degrees to lens and drifts her right hand open in a gentle gesture while the left holds the flacon easy at the waist, hips swaying the gentlest touch as her weight rolls soft between the feet for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she turns a soft six degrees toward lens and drifts her right hand open from the waist in a gentle gesture, the left holding the flacon easy, her hips swaying the gentlest touch as weight rolls soft between the feet; the camera eases with her, gaze warm to lens.",
  "b2": "She delivers \u201cSome moments just stay golden.\u201d to lens with a soft radiant smile and natural lip-sync, right fingers soft on the gesture, eyes warm and serene.",
  "b3": "She holds the serene look as the gold dust drifts soft and her right hand eases back to the waist, the smile easing into calm radiance.",
 },
 7: {
  "posture": "GAZE easing back to the warm direct-to-lens of Frame 1; HEAD returning level with a gentle tilt toward the sun; SHOULDERS softening back, the right a touch forward over the flacon; RIGHT ARM lowering back as the RIGHT HAND returns to cradle the amber flacon at waist height, RIGHT FINGERS curved gently around the glass; LEFT ARM soft at her side, the LEFT HAND light at the dress, LEFT FINGERS relaxed; TORSO rotating back to about 6 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip a touch high; RIGHT LEG easing to free and forward soft, LEFT LEG re-taking the easy weight; FEET & WEIGHT settling gently into the exact Frame-1 stance; HAIR settling soft as the gold-dust wrap resolves toward plain golden light.",
  "hands": "RIGHT HAND returning to cradle the amber flacon at waist height exactly as in Frame 1, RIGHT FINGERS curved gently around the glass; LEFT HAND light at the dress, LEFT FINGERS relaxed; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases back precisely to the opening hook — right hand cradling the amber flacon at waist height with curved fingers, left hand light at the dress, weight settling gently onto the easy left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she eases the amber flacon back to cradle at waist height with curved right fingers, her left hand resting light at the dress, settling her weight gently onto the easy left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her serene gaze back to lens on a slow breath with the composed half-smile, the shoulders softening to the opening set, the gold-dust wrap resolving toward the plain golden-light opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand cradling the flacon, left hand at the dress, weight settled in the low sun — a seamless loop seam.",
 },
}


# ============================ CONCEPT 08 — MONOCHROME RIOT (ink-bloom · K-believability) ============================
# Flow: F1 hero / right hand soft at sternum (ivory) -> F2 hand flat at sternum, fingers spread on the breath
#   -> F3 press hand at sternum, draw breath, left opens -> F4 ease hand off sternum, colour blooms (held angle)
#   -> F5 colour reveal, adjust the flooded lapel -> F6 stride to lens, line + bold gesture -> F7 loop to sternum.
# Energy composed editorial -> bold. Ink-in-water capillary believability kept in the transform beat.
POSE[8] = {
 1: {
  "posture": "GAZE composed and direct to lens; HEAD level, chin a hair lifted, neck long; SHOULDERS even, the right carried a touch forward; RIGHT ARM folded soft to the chest, the RIGHT HAND resting at her sternum as if about to breathe, RIGHT FINGERS gently curved against the ivory cloth; LEFT ARM relaxed and long at her side, the LEFT HAND open, LEFT FINGERS softly extended; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a clean contrapposto with the right hip a touch high; RIGHT LEG the free/forward leg, knee soft, toe grazing from the step just landed; LEFT LEG weight-bearing and straight; FEET & WEIGHT settling onto the left foot on the ivory floor; HAIR sleek and still as the ivory world holds — composed, editorial, alive (living stillness).",
  "hands": "RIGHT HAND resting soft at her sternum as if about to breathe, RIGHT FINGERS gently curved against the ivory cloth with relaxed nail-beds; LEFT ARM long at her side, LEFT HAND open with LEFT FINGERS softly extended; short almond nails in a soft nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just stepped onto her mark in the ivory world — right hand resting soft at her sternum, left arm long, weight settling onto the straight left leg with the right hip a touch high, a composed editorial hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the pure all-ivory editorial world: the camera dollies laterally to settle on her as she steps onto her mark — weight settling onto the straight left leg, the right toe grazing, her right hand resting soft at her sternum and her left arm long; the ivory cyclorama and props slide behind with real parallax.",
  "b2": "The track eases to rest as the right shoulder eases forward and her composed gaze holds to lens, a quiet quarter-smile settling in the clean ivory light.",
  "b3": "She holds the pure ivory editorial look, right fingers soft at the sternum, left fingers extended, weight grounded through the left leg, eyes composed and direct (silent here).",
 },
 2: {
  "posture": "GAZE casting soft down to the hand at her chest; HEAD tilting down about 6 degrees; SHOULDERS easing in over the breath; RIGHT ARM held to the chest, the RIGHT HAND flat-soft at the sternum, RIGHT FINGERS gently spread as if feeling the breath; LEFT ARM easing across low, the LEFT HAND soft at the waist, LEFT FINGERS flat; TORSO easing about 4 degrees and softening inward; WAIST & HIPS holding the soft counter-tilt; RIGHT LEG eased forward soft, LEFT LEG bearing weight; FEET & WEIGHT planted, weight on the left leg; HAIR settling at the cheek as the head dips.",
  "hands": "RIGHT HAND flat-soft at the sternum, RIGHT FINGERS gently spread as if feeling the breath with relaxed nail-beds; LEFT HAND soft at the waist, LEFT FINGERS flat; short almond nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand lies flat-soft at the sternum with fingers gently spread to feel the breath while the left rests at the waist, head dipping softly, weight held on the straight left leg.",
  "b1": "Cut to a medium-close three-quarter: she rests her right hand flat-soft at her sternum and gently spreads her fingers as if feeling the breath, her left hand settling at the waist, the shoulders easing in as the camera pushes with her hand; gaze cast soft to the hand.",
  "b2": "Her gaze softens on the breath and a quiet knowing micro-smile kindles, the head dipped gently, the ivory world holding pure.",
  "b3": "She holds the breath beat, right fingers spread at the sternum, left hand at the waist, weight steady on the left leg, eyes soft — the hush before the colour (silent here).",
 },
 3: {
  "posture": "GAZE lifting from the chest up toward lens; HEAD rising to level; SHOULDERS drawing back and down on the breath; RIGHT ARM pressing soft, the RIGHT HAND at the sternum on the deep breath, RIGHT FINGERS soft against the cloth; LEFT ARM easing open and out, the LEFT HAND turning open, LEFT FINGERS spreading; TORSO lengthening tall on the inhale, ribcage lifting; WAIST & HIPS easing toward square with a gentle counter-tilt; RIGHT LEG settling firmer as weight eases to centre, LEFT LEG anchoring; FEET & WEIGHT widening a touch as she breathes tall; HAIR lifting a touch as the chest opens.",
  "hands": "RIGHT HAND pressing soft at the sternum on the breath, RIGHT FINGERS soft against the cloth; LEFT HAND easing open at her side, LEFT FINGERS spreading; short almond nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand presses soft at the sternum on a deep breath while the left opens at her side with fingers spreading, the ribcage lifting tall as her weight eases to centre between widening feet.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she presses her right hand soft at the sternum and draws a slow tall breath, her left hand easing open and spreading as her weight eases to centre and the ribcage lifts; the camera arcs a few degrees and the ivory cyclorama swings behind with parallax, gaze beginning to lift.",
  "b2": "The arc settles as her chin lifts and her gaze rises to lens with rising calm and a knowing micro-smile forms, the chest open, the ivory world still pure.",
  "b3": "She holds the poised ivory beat, right hand soft at the sternum, left open, breathing tall and grounded, eyes calm and ready — the breath before the bloom (silent here).",
 },
 4: {
  "posture": "GAZE lifting then widening with editorial awe; HEAD held level, easing softly to follow the colour-front; SHOULDERS opening as the hand eases off the chest; RIGHT ARM easing the RIGHT HAND off the sternum and opening outward, RIGHT FINGERS unfurling open; LEFT ARM opening out as a counterweight, the LEFT HAND turning open, LEFT FINGERS spread; TORSO lengthening and beginning a soft open turn from the waist; WAIST & HIPS easing into a gentle rotation as weight rolls; RIGHT LEG taking weight onto the ball of the right foot, LEFT LEG easing free with the heel lifting a touch; FEET & WEIGHT in a soft grounded turn — the body opens while the camera angle holds.",
  "hands": "RIGHT HAND easing off the sternum and opening outward, RIGHT FINGERS unfurling open; LEFT ARM opening out as a counterweight, LEFT HAND turning open with LEFT FINGERS spread; short nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases her right hand off the sternum and opens it outward with unfurling fingers, the left arm opening as counterweight, turning softly onto the ball of the right foot while the camera angle holds and the colour blooms around her.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the all-ivory Look A still): she eases her hand off the sternum on the breath and opens it outward with unfurling fingers, the left arm opening as counterweight, turning onto the ball of her right foot — the world still pure all-ivory, NO colour yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The bloom BEGINS here, mid-clip: on the breath a saturated colour-riot blooms through the ivory along one travelling wavefront as her torso opens through the turn, deep magenta, cobalt and emerald diffusing through the real fabric weave by true ink-in-water capillary spread exactly where the wave passes — painterly and continuous, never a snap, no garish glare; the sleek straight fall catching travelling colour, eyes widening in playful editorial awe (angle held, face cleanly lit, identity locked).",
  "b3": "The ink-wash completes its sweep as she settles through the soft turn and the look resolves smoothly and fully into the bold colour-riot Look B of the Veo last-frame still (Frame 5's image) — magenta, cobalt and emerald set rich through the sculptural silhouette and backdrop, held through the final beat, no last-second pop; a bold alive spark landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing bright to lens; HEAD settling level with a cant; SHOULDERS easing with a roll of the right as the hand lifts; RIGHT ARM rising, the RIGHT HAND reaching up to adjust the colour-flooded lapel, RIGHT FINGERS pinching the lapel-edge; LEFT ARM easing to the hip, the LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; TORSO settling tall out of the turn to about 4 degrees rotation; WAIST & HIPS finding a confident counter-tilt as weight settles onto the back leg; RIGHT LEG easing free and forward, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the turn with a settling step; HAIR settling as colour holds.",
  "hands": "RIGHT HAND reaching up to adjust the colour-flooded lapel with an easy shoulder roll, RIGHT FINGERS pinching the lapel-edge with clean colour-pop nail-beds; LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Settling out of the turn into colour, her right hand reaches up to adjust the flooded lapel with an easy shoulder roll while the left settles on the hip, weight settling onto the back leg.",
  "b1": "Cut to a medium close on a new angle in the colour-flooded world: she is already in the saturated colour-riot look, her right hand reaching up to adjust the flooded lapel with an easy roll of the right shoulder while her left settles on the hip; gaze easing to lens.",
  "b2": "A bold confident smile eases to lens on a slow breath, her weight settling onto the back leg, the last colour blooming rich, eyes bright and direct.",
  "b3": "She holds the bold colour-riot look, right fingers easing off the lapel, left set on the hip, the colour rich around her, eyes alive and direct (silent here).",
 },
 6: {
  "posture": "GAZE bold and direct to lens; HEAD turning a soft six degrees toward lens, chin level; SHOULDERS easy with the left carried forward as she steps; RIGHT ARM swinging open toward lens in a relaxed bold gesture, the RIGHT HAND opening palm-out, RIGHT FINGERS spread; LEFT HAND resting easy at the colour lapel, LEFT FINGERS light; TORSO turning with the stride; WAIST & HIPS swaying with a confident step, weight transferring forward; RIGHT LEG stepping forward into the stride, LEFT LEG pushing off behind; FEET & WEIGHT mid-stride, weight rolling onto the forward right foot; HAIR swinging soft with the step.",
  "hands": "RIGHT HAND swinging open toward lens in a relaxed bold gesture as she speaks, RIGHT FINGERS spread with colour-pop nail-beds; LEFT HAND resting easy at the colour lapel, LEFT FINGERS light; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She steps a confident stride toward lens and swings her right hand open in a bold gesture while the left rests at the colour lapel, hips swaying as her weight rolls onto the forward right foot for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she steps a confident stride toward lens, her right hand swinging open in a relaxed bold gesture while the left rests at the colour lapel, hips swaying as weight rolls onto the forward right foot; the camera eases with her, gaze direct to lens.",
  "b2": "She delivers \u201cColor was always the point.\u201d to lens with a knowing smile and natural lip-sync, right fingers spread on the gesture, eyes bold and direct.",
  "b3": "She holds the bold colour look as the saturation settles and her right hand eases back toward the lapel, the smile easing into alive calm.",
 },
 7: {
  "posture": "GAZE easing back to the composed direct-to-lens of Frame 1; HEAD returning level with the chin a hair lifted; SHOULDERS squaring back, the right a touch forward; RIGHT ARM folding back as the RIGHT HAND returns to rest soft at the sternum, RIGHT FINGERS gently curved; LEFT ARM lowering long, the LEFT HAND open, LEFT FINGERS extended; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip a touch high; RIGHT LEG easing to free and forward, LEFT LEG re-taking weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance; HAIR settling as colour resolves toward ivory.",
  "hands": "RIGHT HAND returning to rest soft at the sternum exactly as in Frame 1, RIGHT FINGERS gently curved; LEFT ARM long, LEFT HAND open with LEFT FINGERS extended; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She pivots back precisely to the opening hook — right hand returning soft to the sternum, left arm long with extended fingers, weight settling onto the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she pivots back and returns her right hand to rest soft at her sternum, her left arm lowering long, settling her weight onto the straight left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her gaze back to lens on a slow breath with the composed quarter-smile, the shoulders squaring, the colour-riot resolving toward the ivory opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand at the sternum, left fingers extended, weight settled and composed — a seamless loop seam.",
 },
}

# ============================ CONCEPT 09 — LIQUID METAL (chrome-pour · K-believability) ============================
# Flow: F1 hero / right hand at collarbone (dark studio) -> F2 lift hand toward cresting chrome, fingers open
#   -> F3 raise hand to receive chrome -> F4 hold hand up, chrome pours and wraps (held angle)
#   -> F5 chrome-sash reveal, settle the sash -> F6 stride to lens, line + strong gesture -> F7 loop to collarbone.
# Energy strong / fluid. Chrome surface-tension + mirror-spread believability kept in the transform beat.
POSE[9] = {
 1: {
  "posture": "GAZE cool and direct to lens; HEAD level with a strong chin, neck long; SHOULDERS squared and strong, the right carried back a touch; RIGHT ARM bent up, the RIGHT HAND resting soft at her collarbone, RIGHT FINGERS lightly along the clavicle; LEFT ARM relaxed and long at her side, the LEFT HAND open, LEFT FINGERS extended; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a strong contrapposto with the right hip set; RIGHT LEG the free/forward leg, knee soft, toe planted from the step just landed; LEFT LEG weight-bearing and straight; FEET & WEIGHT planted strong on the left foot on the black water-skin floor; HAIR high sleek pony still, its tail settling — strong, fluid, alive (living stillness).",
  "hands": "RIGHT HAND resting soft at her collarbone, RIGHT FINGERS lightly along the clavicle with relaxed nail-beds; LEFT ARM long at her side, LEFT HAND open with LEFT FINGERS extended; short almond nails in a cool nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just set into a strong stance on the water-skin floor — right hand soft at the collarbone, left arm long, weight planted on the straight left leg with the right hip set, a cool fluid hero pose mirrored beneath her.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the dark futurist studio on the black water-skin floor: the camera dollies laterally to settle on her as she sets onto her mark — weight planting on the straight left leg, the right toe planted, her right hand resting soft at her collarbone and her left arm long; the dark wall and her mirror reflection slide behind with real parallax.",
  "b2": "The track eases to rest as the right shoulder eases back and her cool gaze holds to lens, a composed quarter-smile settling, the floor mirroring her clean.",
  "b3": "She holds the composed matte look, right fingers at the collarbone, left fingers extended, weight planted on the left foot, eyes cool and direct (silent here).",
 },
 2: {
  "posture": "GAZE rising toward the chrome cresting above; HEAD tilting up about 8 degrees toward the crest; SHOULDERS with the RIGHT shoulder lifting as the arm reaches up; RIGHT ARM extending up and out, the RIGHT HAND lifting soft toward the cresting chrome, RIGHT FINGERS opening as if to receive it; LEFT ARM eased back, the LEFT HAND soft at the waist, LEFT FINGERS relaxed; TORSO lengthening upward toward the crest; WAIST & HIPS easing as she rises into the reach; RIGHT LEG taking more weight as she reaches up, LEFT LEG soft behind; FEET & WEIGHT rolling onto the balls of the feet in the reach; HAIR pony swinging a touch as she tips up.",
  "hands": "RIGHT HAND lifting soft toward the cresting chrome above with RIGHT FINGERS gently open as if to receive it; LEFT HAND soft at the waist, LEFT FINGERS relaxed; short almond cool-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right arm reaches up toward the cresting chrome with fingers opening to receive it while the left rests at the waist, torso lengthening upward and weight rolling onto the balls of the feet.",
  "b1": "Cut to a medium-close three-quarter: she is already lifting her right hand soft toward the chrome cresting above and opening her fingers as if to receive it, her torso lengthening up and weight rolling onto the balls of her feet, the left hand at the waist; the camera pushes with her hand and tilts up, gaze rising toward the crest.",
  "b2": "The chrome glints at her opening fingertips as her gaze rises with cool focus and a composed micro-smile kindles, the head tipped up.",
  "b3": "Her right hand holds open to the crest, left hand soft at the waist, weight poised on the balls of her feet, eyes cool and luminous, the set still matte — the breath before the pour (silent here).",
 },
 3: {
  "posture": "GAZE lifting from the crest toward lens; HEAD easing toward level; SHOULDERS easing back and down; RIGHT ARM held raised, the RIGHT HAND open to receive the chrome, RIGHT FINGERS soft and open; LEFT ARM easing open and out, the LEFT HAND turning open, LEFT FINGERS spreading; TORSO lengthening tall on the breath; WAIST & HIPS easing toward square with the hip set; RIGHT LEG settling firmer as weight centres, LEFT LEG anchoring; FEET & WEIGHT settling even and grounded; HAIR pony settling.",
  "hands": "RIGHT HAND raised soft and open to receive the chrome, RIGHT FINGERS open; LEFT HAND easing open at her side, LEFT FINGERS spreading; short almond cool-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand holds raised and open to receive the chrome while the left opens at her side with spreading fingers, the torso lengthening tall as her weight settles even and grounded.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she raises her right hand soft and open to receive the chrome and draws a slow tall breath, her left hand easing open and spreading as her weight settles even; the camera arcs a few degrees and the dark wall swings behind with parallax, gaze lifting.",
  "b2": "The arc settles as her gaze lifts to lens with cool resolve and a composed micro-smile forms, the chest open, the set still matte.",
  "b3": "She holds the poised matte beat, right hand open to the crest, left open, weight even and grounded, eyes cool and ready — the breath before the pour (silent here).",
 },
 4: {
  "posture": "GAZE cool and luminous, easing to follow the spiralling chrome; HEAD held strong and level; SHOULDERS opening fluid; RIGHT ARM holding raised to receive the pour, the RIGHT HAND open, RIGHT FINGERS catching the chrome; LEFT ARM opening out and back as a fluid counterweight, the LEFT HAND turning open, LEFT FINGERS soft; TORSO lengthening and beginning a slow fluid turn from the waist; WAIST & HIPS easing into a strong rotation as weight rolls; RIGHT LEG taking weight onto the ball of the right foot, LEFT LEG extending free with the heel lifting; FEET & WEIGHT in a strong grounded turn — the body turns fluid while the camera angle holds.",
  "hands": "RIGHT HAND held raised to receive the pour, RIGHT FINGERS catching the chrome; LEFT ARM opening out as a fluid counterweight, LEFT HAND turning open with LEFT FINGERS soft; short cool-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She holds her right hand raised to receive the pour, the left opening back as a fluid counterweight, turning strong onto the ball of the right foot while the camera angle holds and the chrome spirals around her.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the matte-graphite Look A still): she holds her right hand raised to receive the chrome, left arm opening back as a fluid counterweight, turning onto the ball of her right foot — the set still matte, NO chrome yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The pour BEGINS here, mid-clip: the liquid chrome pours down and wraps smoothly around her in one continuous travelling spiral as her torso turns fluid through it, the metal flowing and setting over the matte bodice with believable fluid surface-tension, spread and inertia exactly where it passes — mirror-bright and continuous, mirrored true in the water-skin, never a snap, no garish glare; the high sleek pony catching travelling chrome, eyes luminous with cool awe (angle held, face cleanly lit, identity locked).",
  "b3": "The chrome completes its spiral as she settles through the fluid turn and the look resolves smoothly and fully into the chrome Look B of the Veo last-frame still (Frame 5's image) — a sculptural mirror-chrome sash-and-collar set over the matte set, held through the final beat, no last-second pop; a strong fluid resolve landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing cool to lens; HEAD settling level with a cant; SHOULDERS easing with a fluid roll of the right; RIGHT ARM lowering, the RIGHT HAND reaching to settle the chrome sash at her side, RIGHT FINGERS smoothing the sash-edge; LEFT ARM easing to the hip, the LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; TORSO settling tall out of the turn to about 4 degrees rotation; WAIST & HIPS finding a strong counter-tilt with the hip set as weight settles onto the back leg; RIGHT LEG easing free and forward, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the turn with a settling step; HAIR pony settling cool.",
  "hands": "RIGHT HAND reaching to settle the chrome sash with an easy shoulder roll, RIGHT FINGERS smoothing the sash-edge with clean cool-sheen nail-beds; LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Settling out of the turn in the chrome sash, her right hand smooths the sash-edge with a fluid shoulder roll while the left settles on the set hip, weight settling onto the back leg with the floor mirroring chrome light.",
  "b1": "Cut to a medium close on a new angle, mirror-light off the water-skin: she is already wrapped in the mirror-chrome sash-and-collar, her right hand reaching to settle the sash with an easy roll of the right shoulder while her left settles on the hip; gaze easing to lens.",
  "b2": "A cool confident smile eases to lens on a slow breath, her weight settling onto the back leg with the hip set, the chrome catching mirror-light, eyes cool and direct.",
  "b3": "She holds the strong chrome look, right fingers easing off the sash, left set on the hip, the metal mirror-bright around her, eyes cool and luminous (silent here).",
 },
 6: {
  "posture": "GAZE cool and direct to lens; HEAD turning a soft six degrees toward lens, chin level; SHOULDERS strong with the left carried forward as she steps; RIGHT ARM swinging open toward lens in a relaxed strong gesture, the RIGHT HAND opening palm-out, RIGHT FINGERS spread; LEFT HAND resting easy at the chrome sash, LEFT FINGERS light; TORSO turning fluid with the stride; WAIST & HIPS swaying strong with a confident step, weight transferring forward; RIGHT LEG stepping forward into the stride, LEFT LEG pushing off behind; FEET & WEIGHT mid-stride, weight rolling onto the forward right foot; HAIR pony swinging with the step.",
  "hands": "RIGHT HAND swinging open toward lens in a relaxed strong gesture as she speaks, RIGHT FINGERS spread with cool-sheen nail-beds; LEFT HAND resting easy at the chrome sash, LEFT FINGERS light; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She steps a strong stride toward lens and swings her right hand open in a confident gesture while the left rests at the chrome sash, hips swaying strong as her weight rolls onto the forward right foot for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she steps a strong stride toward lens, her right hand swinging open in a relaxed strong gesture while the left rests at the chrome sash, hips swaying as weight rolls onto the forward right foot; the camera eases with her, gaze direct to lens.",
  "b2": "She delivers \u201cI flow. I don\u2019t break.\u201d to lens with a composed strong smile and natural lip-sync, right fingers spread on the gesture, eyes cool and direct.",
  "b3": "She holds the strong chrome look as the sash settles and her right hand eases back toward it, the smile easing into fluid calm.",
 },
 7: {
  "posture": "GAZE easing back to the cool direct-to-lens of Frame 1; HEAD returning level with a strong chin; SHOULDERS squaring back strong, the right a touch back; RIGHT ARM folding back as the RIGHT HAND returns to rest soft at the collarbone, RIGHT FINGERS along the clavicle; LEFT ARM lowering long, the LEFT HAND open, LEFT FINGERS extended; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip set; RIGHT LEG easing to free and forward, LEFT LEG re-taking weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance; HAIR pony settling as chrome resolves toward matte.",
  "hands": "RIGHT HAND returning to rest soft at the collarbone exactly as in Frame 1, RIGHT FINGERS along the clavicle; LEFT ARM long, LEFT HAND open with LEFT FINGERS extended; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She pivots back precisely to the opening hook — right hand returning soft to the collarbone, left arm long, weight planted on the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she pivots back and returns her right hand to rest soft at her collarbone, her left arm lowering long, planting her weight on the straight left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her gaze back to lens on a slow breath with the composed cool quarter-smile, the shoulders squaring, the chrome resolving toward the matte opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand at the collarbone, left fingers extended, weight planted and cool — a seamless loop seam.",
 },
}

# ============================ CONCEPT 10 — PAPER & PETALS (petal-burst · K-believability) ============================
# Flow: F1 hero / right hand near folded-paper flower at shoulder -> F2 cradle the paper flower, fingers round stem
#   -> F3 open hand as the flower unfolds -> F4 ease hand open, petal-burst wraps (held angle)
#   -> F5 petal reveal, settle a petal at shoulder -> F6 soft turn to lens, line + tender gesture -> F7 loop.
# Energy soft / tender / alive. Paper crease-to-petal flutter believability kept in the transform beat.
POSE[10] = {
 1: {
  "posture": "GAZE soft and direct to lens; HEAD level with a gentle tilt, neck long; SHOULDERS soft, the right carried up a touch toward the shoulder flower; RIGHT ARM raised soft, the RIGHT HAND resting near a folded-paper flower at her shoulder, RIGHT FINGERS lightly near the paper petals; LEFT ARM relaxed and long at her side, the LEFT HAND open, LEFT FINGERS softly extended; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a soft contrapposto with the right hip a touch high; RIGHT LEG the free/forward leg, knee soft, toe grazing from the step just finished; LEFT LEG weight-bearing and straight; FEET & WEIGHT settling onto the left foot in the paper world; HAIR tousled shag drifting soft at the cheek — soft, tender, alive (living stillness).",
  "hands": "RIGHT HAND resting soft near a folded-paper flower at her shoulder, RIGHT FINGERS lightly near the paper petals with relaxed nail-beds; LEFT ARM long at her side, LEFT HAND open with LEFT FINGERS softly extended; short almond nails in a soft petal-nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just stepped softly onto her mark in the paper world — right hand raised light near the folded-paper flower at her shoulder, left arm long, weight settling onto the straight left leg with the right hip a touch high, a soft romantic hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the handmade paper-craft world: the camera dollies laterally to settle on her as she steps softly onto her mark — weight settling onto the straight left leg, the right toe grazing, her right hand rising soft near the folded-paper flower at her shoulder and her left arm long; the folded-paper backdrop and paper props slide behind with real parallax.",
  "b2": "The track eases to rest as a tousled wisp shifts in the soft air, the right shoulder lifting a touch toward the flower, and her soft gaze holds to lens, a romantic quarter-smile settling.",
  "b3": "She holds the soft paper-world look, right fingers near the paper flower, left fingers extended, weight grounded through the left leg, eyes soft and direct (silent here).",
 },
 2: {
  "posture": "GAZE casting soft to the paper flower at her shoulder; HEAD tilting toward the shoulder about 8 degrees; SHOULDERS with the RIGHT shoulder lifting as the hand cradles; RIGHT ARM folded up to the shoulder, the RIGHT HAND cradling the folded-paper flower, RIGHT FINGERS curling gently around the stem; LEFT ARM easing across low, the LEFT HAND soft at the waist, LEFT FINGERS flat; TORSO easing about 4 degrees toward the shoulder; WAIST & HIPS holding the soft counter-tilt; RIGHT LEG eased forward soft, LEFT LEG bearing weight; FEET & WEIGHT planted, weight on the left leg; HAIR drifting at the temple as the head tilts in.",
  "hands": "RIGHT HAND cradling the folded-paper flower soft, RIGHT FINGERS curling gently around the stem; LEFT HAND soft at the waist, LEFT FINGERS flat; short almond petal-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand cradles the folded-paper flower at the shoulder with fingers curling round the stem while the left rests soft at the waist, head tilting in toward it, weight held on the straight left leg.",
  "b1": "Cut to a medium-close three-quarter: she is already cradling the folded-paper flower soft at her shoulder, her right fingers curling gently around the stem while her left hand settles at the waist, the head tilting in as the camera pushes with her hand; gaze cast soft to it.",
  "b2": "The paper petals stir at her curled fingers as her gaze warms with tender focus and a soft micro-smile kindles, the head tilted in.",
  "b3": "She holds the folded flower cradled at her shoulder, right fingers round the stem, left hand at the waist, weight steady on the left leg, eyes soft and tender — the hush before the bloom (silent here).",
 },
 3: {
  "posture": "GAZE lifting from the flower toward lens; HEAD easing to level; SHOULDERS easing back soft; RIGHT ARM easing down a touch, the RIGHT HAND opening soft as the flower begins to unfold, RIGHT FINGERS unfurling open; LEFT ARM easing open and out, the LEFT HAND turning open, LEFT FINGERS spreading; TORSO lengthening tall on the breath; WAIST & HIPS easing toward soft-square with a gentle counter-tilt; RIGHT LEG easing back to even as weight centres, LEFT LEG sharing; FEET & WEIGHT settling even and soft; HAIR settling at the shoulders.",
  "hands": "RIGHT HAND opening soft as the flower begins to unfold, RIGHT FINGERS unfurling open; LEFT HAND easing open at her side, LEFT FINGERS spreading; short almond petal-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand opens soft as the folded flower begins to unfold with unfurling fingers while the left opens at her side, the torso lengthening tall as her weight settles even between the feet.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she opens her right hand soft as the folded flower unfolds and draws a slow breath, her left hand easing open and spreading as her weight settles even; the camera arcs a few degrees and the paper backdrop swings behind with parallax, gaze lifting.",
  "b2": "The arc settles as her gaze lifts to lens with rising tenderness and a soft micro-smile forms, the chest open, the world still folded paper.",
  "b3": "She holds the poised paper beat, right fingers unfurling open, left open, weight even and soft, eyes warm and tender — the breath before the burst (silent here).",
 },
 4: {
  "posture": "GAZE lifting then softening with tender awe; HEAD easing softly to follow the petal-arc, chin level; SHOULDERS opening soft; RIGHT ARM easing fully open, the RIGHT HAND open as the flower bursts, RIGHT FINGERS unfurled; LEFT ARM opening out as a soft counterweight, the LEFT HAND turning open, LEFT FINGERS soft; TORSO lengthening and beginning a soft open turn from the waist; WAIST & HIPS easing into a gentle rotation as weight rolls; RIGHT LEG taking weight onto the ball of the right foot, LEFT LEG easing free with the heel lifting a touch; FEET & WEIGHT in a soft grounded turn — the body opens tender while the camera angle holds.",
  "hands": "RIGHT HAND easing open as the folded-paper flower unfolds and bursts, RIGHT FINGERS unfurled; LEFT ARM opening out as a soft counterweight, LEFT HAND turning open with LEFT FINGERS soft; short petal-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases her right hand fully open as the flower bursts, the left opening as a soft counterweight, turning gently onto the ball of the right foot while the camera angle holds and the petals wrap around her.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the folded-paper Look A still): she eases her right hand open as the flower unfolds, her left arm opening as a soft counterweight, turning onto the ball of her right foot — the world still folded paper, NO burst yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The burst BEGINS here, mid-clip: the folded paper unfolds and bursts into soft real petals that wrap smoothly around her in one continuous travelling arc as her torso opens through the soft turn, warm rose and blush petals fluttering across the pleats by believable real crease-to-petal flutter exactly where the arc passes — fine petal-dust drifting like real flecks, gradual and tender, never a snap, no cheap sparkles; the tousled shag catching travelling petals, eyes warming in soft awe (angle held, face cleanly lit, identity locked).",
  "b3": "The petal-burst completes its arc as she settles through the soft turn and the look resolves smoothly and fully into the petal Look B of the Veo last-frame still (Frame 5's image) — soft real-petal texture and warm petal-colour washed through the pleats, held through the final beat, no last-second pop; a soft radiant warmth landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing soft to lens; HEAD settling level with a gentle tilt; SHOULDERS easing with a soft roll of the right; RIGHT ARM rising, the RIGHT HAND reaching to settle a soft petal at her shoulder, RIGHT FINGERS lightly pinching the petal; LEFT ARM easing to the waist, the LEFT HAND resting at the petal pleats, LEFT FINGERS soft; TORSO settling tall out of the turn to about 4 degrees rotation; WAIST & HIPS finding a serene counter-tilt as weight settles onto the back leg; RIGHT LEG easing free and forward soft, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the turn with a soft settling step; HAIR settling soft, petals drifting.",
  "hands": "RIGHT HAND reaching to settle a soft petal at her shoulder with an easy shoulder roll, RIGHT FINGERS lightly pinching the petal with clean soft-rose nail-beds; LEFT HAND resting at the petal pleats, LEFT FINGERS soft; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Among the bloomed petals, her right hand reaches to settle a soft petal at her shoulder with an easy roll while the left rests at the petal pleats, weight settling onto the back leg.",
  "b1": "Cut to a medium close on a new angle amid the bloomed petals: she is already in the petal-bloomed look, her right hand reaching to settle a soft petal at her shoulder with an easy roll of the right shoulder while her left rests at the petal pleats; gaze easing to lens.",
  "b2": "A soft tender smile eases to lens on a slow breath, her weight settling onto the back leg, the last petal-dust settling around her, eyes soft and warm.",
  "b3": "She holds the soft petal look, right fingers easing off the petal, left at the pleats, the petals breathing warm around her, eyes soft and direct (silent here).",
 },
 6: {
  "posture": "GAZE warm and direct to lens; HEAD turning a soft six degrees toward lens with a gentle tilt; SHOULDERS soft with the left carried a touch forward; RIGHT ARM drifting open from the pleats toward lens in a tender gesture, the RIGHT HAND turning open, RIGHT FINGERS soft; LEFT HAND resting easy at the petal pleats, LEFT FINGERS soft; TORSO turning softly with the head; WAIST & HIPS in a gentle sway, weight rolling soft between the feet; RIGHT LEG easing forward a soft step, LEFT LEG behind sharing weight; FEET & WEIGHT grounded with a gentle pivot toward lens; HAIR shifting soft, petals drifting behind.",
  "hands": "RIGHT HAND drifting open from the petal pleats toward the lens in a soft tender gesture as she speaks, RIGHT FINGERS soft; LEFT HAND resting easy at the petal pleats, LEFT FINGERS soft; short almond soft-rose nails, neat cuticles, no white-knuckle tension.",
  "framing": "She turns a soft six degrees to lens with a small step and drifts her right hand open in a tender gesture while the left rests at the petal pleats, hips swaying gently as her weight rolls between the feet for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she turns a soft six degrees toward lens with a small step and drifts her right hand open from the petal pleats in a tender gesture, the left resting at the pleats, hips swaying as weight rolls between the feet; the camera eases with her, gaze warm to lens.",
  "b2": "She delivers \u201cUnfold. Then bloom.\u201d to lens with a soft tender smile and natural lip-sync, right fingers soft on the gesture, eyes warm and gentle.",
  "b3": "She holds the soft petal look as the petals breathe and her right hand eases back to the pleats, the smile easing into tender calm.",
 },
 7: {
  "posture": "GAZE easing back to the soft direct-to-lens of Frame 1; HEAD returning level with a gentle tilt; SHOULDERS softening back, the right lifting a touch toward the shoulder flower; RIGHT ARM rising back as the RIGHT HAND returns to rest soft near the folded-paper flower at her shoulder, RIGHT FINGERS lightly near the petals; LEFT ARM lowering long, the LEFT HAND open, LEFT FINGERS extended; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip a touch high; RIGHT LEG easing to free and forward soft, LEFT LEG re-taking weight straight; FEET & WEIGHT settling into the exact Frame-1 stance; HAIR settling soft as petals resolve toward folded paper.",
  "hands": "RIGHT HAND returning to rest soft near the folded-paper flower at her shoulder exactly as in Frame 1, RIGHT FINGERS lightly near the petals; LEFT ARM long, LEFT HAND open with LEFT FINGERS extended; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases back precisely to the opening hook — right hand returning soft near the folded-paper flower at her shoulder, left arm long, weight settling onto the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she eases back and returns her right hand to rest soft near the folded-paper flower at her shoulder, her left arm lowering long, settling her weight onto the straight left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her gaze back to lens on a slow breath with the composed romantic quarter-smile, the shoulders softening, the petals resolving toward the folded-paper opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand near the paper flower, left fingers extended, weight settled and soft — a seamless loop seam.",
 },
}


# ============================ CONCEPT 15 — INKED (winged-liner ink-draw) ============================
# Flow: F1 hero / right hand soft at collarbone -> F2 lift toward cresting ink-stroke -> F3 raise to meet the ink
#   -> F4 ease hand down, ink draws the winged liner + look (held angle) -> F5 settle the sculptural shoulder
#   -> F6 sharp stride to lens, line + clean gesture -> F7 loop to collarbone. Energy sharp / graphic / editorial.
POSE[15] = {
 1: {
  "posture": "GAZE sharp and direct to lens; HEAD level with a crisp chin, neck long and graphic; SHOULDERS squared, the right carried back a touch; RIGHT ARM bent up, the RIGHT HAND resting soft near her collarbone, RIGHT FINGERS lightly along the clavicle; LEFT ARM long at her side, the LEFT HAND open, LEFT FINGERS extended; TORSO rotated about 5 degrees to open the right shoulder; WAIST & HIPS in a sharp contrapposto with the right hip set; RIGHT LEG the free/forward leg, knee soft, toe planted from the step just landed; LEFT LEG weight-bearing and straight; FEET & WEIGHT planted on the left foot in the graphic studio; HAIR space buns crisp and still — sharp, graphic, alive (living stillness).",
  "hands": "RIGHT HAND resting soft near her collarbone, RIGHT FINGERS lightly along the clavicle with relaxed nail-beds; LEFT ARM long at her side, LEFT HAND open with LEFT FINGERS extended; short almond nails in a clean soft nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just set onto her mark in the graphic studio — right hand soft near the collarbone, left arm long, weight planted on the straight left leg with the right hip set, a sharp editorial hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the bold editorial studio: the camera dollies laterally to settle on her as she sets onto her mark — weight planting on the straight left leg, the right toe planted, her right hand resting soft near her collarbone and her left arm long; the graphic dark seamless backdrop and liquid-ink motif slide behind with real parallax.",
  "b2": "The track eases to rest as the right shoulder eases back and her sharp gaze holds to lens, a composed graphic quarter-smile settling under the hard key.",
  "b3": "She holds the clean charcoal base look, right fingers at the collarbone, left fingers extended, weight planted on the left foot, eyes sharp and direct (silent here).",
 },
 2: {
  "posture": "GAZE rising toward the cresting ink-stroke; HEAD tilting up about 8 degrees toward the ink edge; SHOULDERS with the RIGHT shoulder lifting as the arm reaches; RIGHT ARM extending up and out, the RIGHT HAND lifting soft toward the cresting ink-stroke as if to meet it, RIGHT FINGERS gently open; LEFT ARM eased back, the LEFT HAND soft at the waist, LEFT FINGERS relaxed; TORSO lengthening upward toward the ink edge; WAIST & HIPS easing as she rises into the reach; RIGHT LEG taking more weight as she reaches, LEFT LEG soft behind; FEET & WEIGHT rolling onto the balls of the feet; HAIR buns crisp as she tips up.",
  "hands": "RIGHT HAND lifting soft toward the cresting ink-stroke as if to meet it, RIGHT FINGERS gently open; LEFT HAND soft at the waist, LEFT FINGERS relaxed; short almond nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right arm reaches up toward the cresting ink-stroke with fingers gently open while the left rests at the waist, torso lengthening upward and weight rolling onto the balls of the feet.",
  "b1": "Cut to a medium-close three-quarter: she is already lifting her right hand soft toward the cresting ink-stroke as if to meet it, fingers gently open, her torso lengthening up and weight rolling onto the balls of her feet, the left hand at the waist; the camera pushes with her hand, gaze toward the ink edge.",
  "b2": "The ink edge glints at her fingertips as her gaze sharpens with graphic focus and a knowing micro-smile kindles, the head tipped up.",
  "b3": "Her right hand holds open toward the ink, left hand soft at the waist, weight poised on the balls of her feet, eyes sharp and bright, the base still clean — the beat before the draw (silent here).",
 },
 3: {
  "posture": "GAZE lifting from the ink toward lens; HEAD easing toward level; SHOULDERS easing back and down; RIGHT ARM held raised, the RIGHT HAND open to meet the ink, RIGHT FINGERS soft and open; LEFT ARM easing open and out, the LEFT HAND turning open, LEFT FINGERS spreading; TORSO lengthening tall on the breath; WAIST & HIPS easing toward square with the hip set; RIGHT LEG settling firmer as weight centres, LEFT LEG anchoring; FEET & WEIGHT settling even and grounded; HAIR buns settling.",
  "hands": "RIGHT HAND raised soft and open to meet the ink, RIGHT FINGERS open; LEFT HAND easing open at her side, LEFT FINGERS spreading; short almond nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand holds raised and open to meet the ink while the left opens at her side with spreading fingers, the torso lengthening tall as her weight settles even and grounded.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she raises her right hand soft to meet the ink and draws a slow tall breath, her left hand easing open and spreading as her weight settles even; the camera arcs a few degrees and the backdrop swings behind with parallax, gaze lifting.",
  "b2": "The arc settles as her gaze lifts to lens with sharp resolve and a knowing micro-smile forms, the chest open, the base still clean charcoal.",
  "b3": "She holds the poised base beat, right hand open to the ink, left open, weight even and grounded, eyes sharp and ready — the beat before the draw (silent here).",
 },
 4: {
  "posture": "GAZE sharp, easing to follow the drawing ink; HEAD held graphic and level; SHOULDERS opening sharp; RIGHT ARM easing down from meeting the ink, the RIGHT HAND lowering open, RIGHT FINGERS relaxed; LEFT ARM opening out and back as a graphic counterweight, the LEFT HAND turning open, LEFT FINGERS soft; TORSO lengthening and beginning a sharp open turn from the waist; WAIST & HIPS easing into a crisp rotation as weight rolls; RIGHT LEG taking weight onto the ball of the right foot, LEFT LEG extending free with the heel lifting; FEET & WEIGHT in a sharp grounded turn — the body turns crisp while the camera angle holds.",
  "hands": "RIGHT HAND easing down from meeting the ink, RIGHT FINGERS relaxed; LEFT ARM opening out as a graphic counterweight, LEFT HAND turning open with LEFT FINGERS soft; short clean-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases her right hand down from the ink, the left opening back as a graphic counterweight, turning crisp onto the ball of the right foot while the camera angle holds and the ink draws across her.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the clean-base Look A still): she eases her right hand down from meeting the ink, her left arm opening back as a graphic counterweight, turning onto the ball of her right foot — still the clean charcoal base, NO draw yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The ink draw BEGINS here, mid-clip: a single travelling ink-stroke draws smoothly across the frame in one continuous wet line as her torso turns through it, drawing her crisp winged liner and resolving the clean charcoal base into the architectural sculptural-shoulder editorial top in deep black exactly where the stroke passes — real liquid-ink flow and cloth resolving with believable spread and inertia, gradual and sharp but smooth, never a snap, no garish glare; the high space buns catching travelling graphic light, eyes sharpening in bold focus (angle held, face cleanly lit, identity locked).",
  "b3": "The ink-stroke completes its draw as she settles through the crisp turn and the look resolves smoothly and fully into the bold winged-liner Look B of the Veo last-frame still (Frame 5's image) — the architectural deep-black top with crisp graphic winged liner under the hard editorial key, held through the final beat, no last-second pop; a sharp graphic resolve landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing sharp to lens; HEAD settling level with a crisp cant; SHOULDERS easing with a sharp roll of the right; RIGHT ARM rising, the RIGHT HAND drifting to settle the sculptural shoulder, RIGHT FINGERS smoothing the structured seam; LEFT ARM easing to the hip, the LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; TORSO settling tall out of the turn to about 4 degrees rotation; WAIST & HIPS finding a sharp counter-tilt with the hip set as weight settles onto the back leg; RIGHT LEG easing free and forward, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the turn with a sharp settling step; HAIR buns crisp.",
  "hands": "RIGHT HAND drifting to settle the sculptural shoulder with an easy roll, RIGHT FINGERS smoothing the structured seam with clean groomed-nude nail-beds; LEFT HAND settling on the hip, LEFT FINGERS along the hipbone; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Settling out of the turn in the winged-liner look, her right hand smooths the sculptural shoulder with a sharp roll while the left settles on the set hip, weight settling onto the back leg.",
  "b1": "Cut to a medium close on a new angle in the sharpened graphic light: she is already in the bold winged-liner editorial look, her right hand drifting to settle the sculptural shoulder with an easy roll of the right shoulder while her left settles on the hip; gaze easing to lens.",
  "b2": "A sharp confident smile eases to lens on a slow breath, her weight settling onto the back leg with the hip set, the crisp liner catching the hard key, eyes sharp and direct.",
  "b3": "She holds the bold winged-liner look, right fingers easing off the shoulder, left set on the hip, the graphic look crisp, eyes sharp and bright (silent here).",
 },
 6: {
  "posture": "GAZE sharp and direct to lens; HEAD turning a sharp six degrees toward lens, chin level; SHOULDERS sharp with the left carried forward as she steps; RIGHT ARM swinging open toward lens in a sharp clean gesture, the RIGHT HAND opening palm-out, RIGHT FINGERS sharply spread; LEFT HAND resting easy at her side, LEFT FINGERS light; TORSO turning crisp with the stride; WAIST & HIPS swaying sharp with a confident step, weight transferring forward; RIGHT LEG stepping forward into the stride, LEFT LEG pushing off behind; FEET & WEIGHT mid-stride, weight rolling onto the forward right foot; HAIR buns crisp with the step.",
  "hands": "RIGHT HAND swinging open toward lens in a sharp clean gesture as she speaks, RIGHT FINGERS sharply spread with groomed-nude nail-beds; LEFT HAND resting easy at her side, LEFT FINGERS light; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She steps a sharp stride toward lens and swings her right hand open in a clean gesture while the left stays easy at her side, hips swaying sharp as her weight rolls onto the forward right foot for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she steps a sharp stride toward lens, her right hand swinging open in a clean gesture while the left stays easy at her side, hips swaying as weight rolls onto the forward right foot; the camera eases with her, gaze direct to lens.",
  "b2": "She delivers \u201cI draw my own line.\u201d to lens with a sharp knowing smile and natural lip-sync, right fingers sharply spread on the gesture, eyes bold and direct.",
  "b3": "She holds the bold graphic look as the liner sets and her right hand eases back to her side, the smile easing into sharp calm.",
 },
 7: {
  "posture": "GAZE easing back to the sharp direct-to-lens of Frame 1; HEAD returning level with a crisp chin; SHOULDERS squaring back, the right a touch back; RIGHT ARM folding back as the RIGHT HAND returns to rest soft near her collarbone, RIGHT FINGERS along the clavicle; LEFT ARM lowering long, the LEFT HAND open, LEFT FINGERS extended; TORSO rotating back to about 5 degrees; WAIST & HIPS returning to the opening contrapposto with the right hip set; RIGHT LEG easing to free and forward, LEFT LEG re-taking weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance; HAIR buns settling as the graphic look holds toward the clean base.",
  "hands": "RIGHT HAND returning to rest soft near her collarbone exactly as in Frame 1, RIGHT FINGERS along the clavicle; LEFT ARM long, LEFT HAND open with LEFT FINGERS extended; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She pivots back precisely to the opening hook — right hand returning soft near the collarbone, left arm long, weight planted on the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she pivots back and returns her right hand to rest soft near her collarbone, her left arm lowering long, planting her weight on the straight left leg in the opening contrapposto exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her gaze back to lens on a slow breath with the composed sharp quarter-smile, the shoulders squaring, the winged-liner look resolving toward the clean-base opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand at the collarbone, left fingers extended, weight planted and sharp — a seamless loop seam.",
 },
}

# ============================ CONCEPT 16 — RAIN CHECK (rain-ripple · SEATED) ============================
# Flow: F1 seated, cradle warm cup on the table -> F2 lift hand from cup toward the rain-streamed glass
#   -> F3 raise toward the glass -> F4 ease hand down toward the cup, rain-ripple rolls (held angle)
#   -> F5 cradle the warm cup again -> F6 lean to lens, line + warm gesture -> F7 loop to the cup.
# SEATED throughout (keep seated waist-up framing) — articulate within the seat (lean/reach/shift/legs under table);
# NO standing or striding. Energy warm / dreamy / cozy.
POSE[16] = {
 1: {
  "posture": "GAZE soft and direct to lens; HEAD level with a gentle tilt toward the window, neck relaxed; SHOULDERS soft and dropped, the near shoulder eased toward the table; RIGHT ARM resting on the table, the RIGHT HAND cradling the warm coffee cup, RIGHT FINGERS curved around the warm ceramic; LEFT ARM resting on the table, the LEFT HAND soft beside the cup, LEFT FINGERS relaxed; TORSO seated tall but easy, leaned a soft few degrees toward the table; WAIST & HIPS settled into the chair with the weight on the seat and a soft lean; LEGS seated with the knees angled toward the window, the RIGHT LEG crossed gently over the LEFT beneath the table; FEET tucked soft, the left foot flat and the right hooked behind the ankle; HAIR half-up boho braids drifting soft at the cheek — warm, dreamy, seated and alive (living stillness).",
  "hands": "RIGHT HAND cradling the warm coffee cup on the wooden table, RIGHT FINGERS curved around the warm ceramic with relaxed nail-beds; LEFT HAND resting soft beside it on the table, LEFT FINGERS relaxed; short almond nails in a soft warm nude, neat cuticles, no white-knuckle tension.",
  "framing": "Seated easy at the worn wooden table, she cradles the warm cup with curved right fingers while the left rests soft beside it, leaning a soft few degrees toward the table with the knees angled to the window and the right leg crossed gently over the left.",
  "b1": "Cut to a medium-wide waist-up tracking shot at the rainy café window: the camera dollies gently laterally to settle on her seated at the worn wooden table — leaned soft toward the table, the right leg crossed gently over the left beneath it — as she cradles the warm coffee cup with curved right fingers, gentle steam curling; the rain-streamed glass and amber interior slide behind with real parallax.",
  "b2": "The track eases to rest as a face-framing braid shifts and her soft gaze eases to lens, the near shoulder dropped easy, a warm dreamy quarter-smile settling.",
  "b3": "She holds the cozy seated look, right fingers cradling the cup, left hand soft on the table, leaned easy in the chair, eyes warm and direct as rain beads the glass (silent here).",
 },
 2: {
  "posture": "GAZE drifting to the rain-streamed glass; HEAD turning about 10 degrees toward the window and tilting up a touch; SHOULDERS with the RIGHT shoulder lifting as the hand leaves the cup; RIGHT ARM lifting from the cup toward the glass, the RIGHT HAND rising soft toward a rain-bead, RIGHT FINGERS gently open; LEFT ARM resting on the table, the LEFT HAND soft on the wood, LEFT FINGERS relaxed; TORSO leaning a few degrees more toward the window over the table; WAIST & HIPS shifting soft in the seat toward the glass; LEGS still seated, the RIGHT LEG crossed over the LEFT, knees angled to the window; FEET soft, the left flat, the right hooked at the ankle; HAIR braids drifting as she leans in.",
  "hands": "RIGHT HAND lifting soft from the cup toward the rain-streamed glass as if to touch a bead, RIGHT FINGERS gently open; LEFT HAND soft on the table, LEFT FINGERS relaxed; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Seated, she lifts her right hand from the cup toward the rain-streamed glass with fingers gently open while the left rests on the table, leaning a few degrees more toward the window and shifting soft in the seat.",
  "b1": "Cut to a medium-close three-quarter: she is already lifting her right hand soft from the cup toward the rain-streamed glass as if to touch a bead, fingers gently open, leaning toward the window and shifting soft in the seat as the camera pushes with her hand; gaze toward the rain.",
  "b2": "Her gaze warms toward the running beads as a dreamy micro-smile kindles, the head tilted up toward the glass.",
  "b3": "Her right hand holds soft toward the glass, left resting on the table, leaned toward the window in the seat, eyes warm and dreamy as the rain runs — the hush before the ripple (silent here).",
 },
 3: {
  "posture": "GAZE easing from the glass back toward lens; HEAD easing to level; SHOULDERS easing back into the chair; RIGHT ARM held raised soft toward the glass, the RIGHT HAND open near the beads, RIGHT FINGERS soft; LEFT ARM easing open on the table, the LEFT HAND turning open on the wood, LEFT FINGERS spreading; TORSO settling tall but easy back from the lean; WAIST & HIPS settling back into the seat; LEGS seated, the RIGHT LEG crossed over the LEFT, knees easing toward the lens; FEET soft, the left flat, the right hooked; HAIR braids settling.",
  "hands": "RIGHT HAND raised soft toward the glass, RIGHT FINGERS soft near the beads; LEFT HAND easing open on the table, LEFT FINGERS spreading; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Seated, her right hand holds soft toward the glass while the left eases open on the table with spreading fingers, the torso settling tall and easy back from the lean in the chair.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she holds her right hand soft toward the glass and draws a slow breath, her left hand easing open on the table as she settles tall back into the chair; the camera arcs a few degrees and the café swings behind with parallax, gaze lifting.",
  "b2": "The arc settles as her gaze eases to lens with rising warmth and a dreamy micro-smile forms, the layers still the soft oatmeal knit.",
  "b3": "She holds the poised seated beat, right hand soft toward the glass, left open on the table, eased back in the chair, eyes warm and dreamy — the breath before the ripple (silent here).",
 },
 4: {
  "posture": "GAZE warm, easing to follow the rain-ripple across the glass; HEAD held level with a soft tilt; SHOULDERS easing soft; RIGHT ARM easing down from the glass toward the cup, the RIGHT HAND lowering soft, RIGHT FINGERS relaxed; LEFT ARM resting on the table, the LEFT HAND soft on the wood, LEFT FINGERS easy; TORSO easing tall in the seat with the gentlest lean toward the table; WAIST & HIPS settled easy in the chair; LEGS seated, the RIGHT LEG crossed over the LEFT beneath the table; FEET soft, the left flat, the right hooked — she stays the still warm centre in the seat while the ripple rolls, the camera angle held.",
  "hands": "RIGHT HAND easing soft down from the rain-streamed glass toward the cup, RIGHT FINGERS relaxed; LEFT HAND soft on the table, LEFT FINGERS easy; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Seated, she eases her right hand down from the glass toward the cup with relaxed fingers, the left soft on the table, easing tall in the chair as the rain-ripple rolls across the glass around her, the camera angle held.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the soft-day Look A still): she eases her right hand down from the glass toward the cup, the left soft on the table, easing tall in the seat — still the soft oatmeal knit, NO ripple yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The ripple BEGINS here, mid-clip: a single travelling rain-ripple rolls smoothly across the rain-streamed window and the frame in one continuous warm front, the light knit deepening into the chunky caramel cardigan with a snug modest scarf and the room warming to amber exactly where the ripple passes — cloth resolving with believable weight and inertia, real rain-on-glass refraction, gradual and warm, never a snap, no garish glare; the boho braids catching travelling amber light, eyes warming in dreamy wonder (angle held, face cleanly lit, identity locked).",
  "b3": "The ripple completes its roll as she settles easy in the seat and the look resolves smoothly and fully into the cozy cardigan Look B of the Veo last-frame still (Frame 5's image) — the warm chunky caramel cardigan and snug scarf over the knit in a snug amber glow, held through the final beat, no last-second pop; a warm dreamy calm landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing soft to lens; HEAD settling level with a gentle tilt; SHOULDERS easing with a soft roll of the right into the cardigan; RIGHT ARM lowering, the RIGHT HAND drifting to cradle the warm cup again, RIGHT FINGERS curved around the ceramic; LEFT ARM resting on the table, the LEFT HAND soft on the wood, LEFT FINGERS relaxed; TORSO settling tall and cozy in the seat with a soft lean; WAIST & HIPS settled easy in the chair; LEGS seated, the RIGHT LEG crossed over the LEFT; FEET soft, the left flat, the right hooked; HAIR braids settling soft in the amber glow.",
  "hands": "RIGHT HAND drifting to cradle the warm cup again with an easy roll of the shoulder, RIGHT FINGERS curved around the ceramic with soft groomed-nude nail-beds; LEFT HAND soft on the table, LEFT FINGERS relaxed; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "In the cozy cardigan, seated, her right hand drifts back to cradle the warm cup with curved fingers while the left rests soft on the table, leaned easy in the chair in the amber glow.",
  "b1": "Cut to a medium close on a new angle in the snug amber glow: she is already in the cozy cardigan-and-scarf look, seated, her right hand drifting to cradle the warm cup again with an easy roll of the right shoulder while her left rests soft on the table; gaze easing to lens.",
  "b2": "A warm dreamy smile eases to lens on a slow breath, leaned easy in the chair, the amber glow warming the braids, eyes soft and warm.",
  "b3": "She holds the cozy cardigan look, right fingers cradling the cup, left soft on the table, seated easy, eyes warm and direct (silent here).",
 },
 6: {
  "posture": "GAZE warm and direct to lens; HEAD turning a soft six degrees toward lens with a gentle tilt; SHOULDERS soft, the near shoulder dropped easy; RIGHT ARM drifting open soft from the cup toward lens in a warm gesture, the RIGHT HAND turning open, RIGHT FINGERS soft; LEFT ARM resting on the table, the LEFT HAND easy on the wood, LEFT FINGERS relaxed; TORSO leaning an easy few degrees toward lens over the table; WAIST & HIPS shifting soft in the seat toward lens; LEGS seated, the RIGHT LEG crossed over the LEFT; FEET soft, the left flat, the right hooked; HAIR braids drifting as she leans in.",
  "hands": "RIGHT HAND drifting open soft from the cup toward the lens in a warm easy gesture as she speaks, RIGHT FINGERS soft; LEFT HAND resting easy on the table, LEFT FINGERS relaxed; short almond groomed-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Seated, she leans an easy few degrees toward lens and drifts her right hand open from the cup in a warm gesture while the left rests on the table, shifting soft in the seat for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she leans an easy few degrees toward lens and drifts her right hand open soft from the cup in a warm easy gesture, the left resting on the table, shifting soft in the seat; the camera eases with her, gaze warm to lens.",
  "b2": "She delivers \u201cSome days are made for rain.\u201d to lens with a warm dreamy smile and natural lip-sync, right fingers soft on the gesture, eyes warm and gentle.",
  "b3": "She holds the cozy look as the rain runs soft and her right hand eases back to the cup, the smile easing into warm calm.",
 },
 7: {
  "posture": "GAZE easing back to the soft direct-to-lens of Frame 1; HEAD returning level with a gentle tilt toward the window; SHOULDERS softening back, the near shoulder eased toward the table; RIGHT ARM resting back on the table as the RIGHT HAND returns to cradle the warm cup, RIGHT FINGERS curved around the ceramic; LEFT ARM resting on the table, the LEFT HAND soft beside it, LEFT FINGERS relaxed; TORSO seated tall but easy, leaned a soft few degrees toward the table; WAIST & HIPS settled into the chair with a soft lean; LEGS seated, the RIGHT LEG crossed gently over the LEFT beneath the table; FEET tucked soft, the left flat and the right hooked behind the ankle; HAIR braids settling soft as the amber resolves toward soft daylight.",
  "hands": "RIGHT HAND returning to cradle the warm coffee cup exactly as in Frame 1, RIGHT FINGERS curved around the ceramic; LEFT HAND soft beside it on the table, LEFT FINGERS relaxed; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "Seated, she eases back precisely to the opening hook — right hand cradling the warm cup with curved fingers, left soft beside it on the table, leaned easy in the chair with the right leg crossed over the left for a seamless loop.",
  "b1": "Cut to a medium-wide waist-up matched to Frame 1: she returns her right hand to cradle the warm coffee cup seated at the table, leaned soft toward the table with the right leg crossed gently over the left, exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her soft gaze back to lens on a slow breath with the composed warm quarter-smile, the cozy cardigan resolving toward the soft-day opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand cradling the cup, left soft on the table, seated easy — a seamless loop seam.",
 },
}


# ============================ CONCEPT 17 — LONG DRIVE (wind-and-light · coastal) ============================
# Flow: F1 hero / right hand on open car door, left easing a strand from cheek -> F2 lift right toward the wind-wave
#   -> F3 raise toward the breeze -> F4 ease right down, wind-and-light wave sweeps (held angle)
#   -> F5 settle the silk scarf -> F6 step from the car toward lens, line + warm gesture -> F7 loop to the door.
# Energy breezy / golden / dreamy with movement (lean on car, a step into the breeze, hair in wind).
POSE[17] = {
 1: {
  "posture": "GAZE warm and direct to lens; HEAD level with a soft tilt into the breeze, neck relaxed; SHOULDERS easy, the right carried back over the car door; RIGHT ARM extended to the side, the RIGHT HAND resting soft on the open car door, RIGHT FINGERS draped over the door-top; LEFT ARM raised to the face, the LEFT HAND easing a wind-blown strand from her cheek, LEFT FINGERS light at the hair; TORSO rotated about 6 degrees toward the road, leaning a touch on the door; WAIST & HIPS in a soft contrapposto with the right hip eased toward the car; RIGHT LEG the free leg, knee soft, toe grazing; LEFT LEG weight-bearing and straight; FEET & WEIGHT settled on the left foot on the open road; HAIR wind-blown beach waves lifting at the cheek — breezy, golden, alive (living stillness).",
  "hands": "RIGHT HAND resting soft on the open car door, RIGHT FINGERS draped over the door-top with relaxed nail-beds; LEFT HAND easing a wind-blown strand from her cheek, LEFT FINGERS light at the hair; short almond nails in a soft warm nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just paused by the open convertible — right hand resting soft on the car door, left easing a wind-blown strand from her cheek, weight settled on the straight left leg with the right hip eased toward the car, a warm easy hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot on the coastal cliff road at golden hour: the camera dollies laterally to settle on her as she pauses by the open convertible — weight settling onto the straight left leg, her right hand resting soft on the open car door and her left easing a wind-blown strand from her cheek; the open ocean sky and a vintage convertible slide behind with real parallax.",
  "b2": "The track eases to rest as the beach waves lift in the sea-breeze and her warm gaze holds to lens, the right shoulder eased over the door, an easy quarter-smile settling in the low gold light.",
  "b3": "She holds the warm breezy look, right fingers on the car door, left easing the strand, weight grounded through the left foot, eyes warm and direct over the ocean (silent here).",
 },
 2: {
  "posture": "GAZE rising toward the cresting wind-and-light wave; HEAD tilting up about 8 degrees into the breeze; SHOULDERS with the RIGHT shoulder lifting as the arm reaches; RIGHT ARM lifting from the door up and out, the RIGHT HAND rising soft toward the wind as if to feel the breeze, RIGHT FINGERS gently open; LEFT ARM easing down to the car door, the LEFT HAND soft on the door-top, LEFT FINGERS relaxed; TORSO lengthening upward into the breeze; WAIST & HIPS easing as she rises into the reach; RIGHT LEG taking more weight as she reaches, LEFT LEG soft behind; FEET & WEIGHT rolling onto the balls of the feet; HAIR waves streaming as she tips up into the wind.",
  "hands": "RIGHT HAND lifting soft toward the cresting wind-and-light wave as if to feel the breeze, RIGHT FINGERS gently open; LEFT HAND soft on the car door, LEFT FINGERS relaxed; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right arm lifts from the door up toward the breeze with fingers gently open while the left rests on the door, torso lengthening into the wind and weight rolling onto the balls of the feet.",
  "b1": "Cut to a medium-close three-quarter: she is already lifting her right hand soft from the door toward the cresting wind-and-light wave as if to feel the breeze, fingers gently open, her torso lengthening into the wind and weight rolling onto the balls of her feet, the left hand on the car door; the camera pushes with her hand, gaze toward the open sky.",
  "b2": "The breeze streams through her fingers as her gaze warms with dreamy wonder and a soft micro-smile kindles, the head tipped up into the wind.",
  "b3": "Her right hand holds open to the breeze, left soft on the door, weight poised on the balls of her feet, eyes warm and dreamy, the layers still the soft white shirt — the breath before the wave (silent here).",
 },
 3: {
  "posture": "GAZE easing from the sky back toward lens; HEAD easing to level; SHOULDERS easing back and down; RIGHT ARM held raised soft toward the breeze, the RIGHT HAND open to the wind, RIGHT FINGERS soft; LEFT ARM easing open on the car door, the LEFT HAND turning open on the door-top, LEFT FINGERS spreading; TORSO lengthening tall on the breath; WAIST & HIPS easing toward square with a gentle counter-tilt; RIGHT LEG settling firmer as weight centres, LEFT LEG anchoring; FEET & WEIGHT settling even and grounded on the road; HAIR waves settling from the gust.",
  "hands": "RIGHT HAND raised soft toward the breeze, RIGHT FINGERS open to the wind; LEFT HAND easing open on the car door, LEFT FINGERS spreading; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand holds raised soft to the breeze while the left eases open on the car door with spreading fingers, the torso lengthening tall as her weight settles even and grounded on the road.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she raises her right hand soft toward the breeze and draws a slow breath, her left hand easing open on the car door as her weight settles even; the camera arcs a few degrees and the coast swings behind with parallax, gaze lifting.",
  "b2": "The arc settles as her gaze eases to lens with rising warmth and a dreamy micro-smile forms, the light still soft afternoon gold.",
  "b3": "She holds the poised breezy beat, right hand open to the wind, left open on the door, weight even and grounded, eyes warm and dreamy — the breath before the wave (silent here).",
 },
 4: {
  "posture": "GAZE warm, easing to follow the sweeping wave; HEAD held level with a soft tilt into the breeze; SHOULDERS easing soft; RIGHT ARM easing down from the breeze, the RIGHT HAND lowering soft, RIGHT FINGERS relaxed; LEFT ARM opening out from the door as a soft counterweight, the LEFT HAND turning open, LEFT FINGERS soft; TORSO lengthening and beginning a soft open turn into the wind from the waist; WAIST & HIPS easing into a gentle rotation as weight rolls; RIGHT LEG taking weight onto the ball of the right foot, LEFT LEG easing free with the heel lifting; FEET & WEIGHT in a soft grounded turn on the road — the body turns into the breeze while the camera angle holds.",
  "hands": "RIGHT HAND easing soft down from feeling the breeze, RIGHT FINGERS relaxed; LEFT ARM opening out from the door as a soft counterweight, LEFT HAND turning open with LEFT FINGERS soft; short warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases her right hand down from the breeze, the left opening out from the door as a soft counterweight, turning gently into the wind onto the ball of the right foot while the camera angle holds and the wave sweeps across her.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the breezy-day Look A still): she eases her right hand down from the breeze, her left arm opening out from the door as a soft counterweight, turning into the wind onto the ball of her right foot — still the soft white shirt, NO wave yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The wave BEGINS here, mid-clip: a single travelling wind-and-light wave sweeps smoothly across the frame in one continuous golden front as her torso turns into the breeze, the breezy shirt flowing into the soft silk scarf and light caramel jacket and the light warming to deep gold exactly where the wave passes — silk and cloth flowing with believable wind weight and inertia, real golden-hour light spread, gradual and warm, never a snap, no garish glare; the beach waves lifting in travelling gold light, eyes warming in dreamy wonder (angle held, face cleanly lit, identity locked).",
  "b3": "The wave completes its sweep as she settles through the soft turn and the look resolves smoothly and fully into the golden-coastal Look B of the Veo last-frame still (Frame 5's image) — the soft flowing silk scarf and light caramel jacket over the shirt in deep golden light, held through the final beat, no last-second pop; a warm dreamy calm landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing warm to lens; HEAD settling level with a soft tilt; SHOULDERS easing with a soft roll of the right; RIGHT ARM rising, the RIGHT HAND drifting to settle the soft silk scarf at her neck, RIGHT FINGERS smoothing the silk; LEFT ARM easing to the car door, the LEFT HAND resting on the door-top, LEFT FINGERS soft; TORSO settling tall out of the turn to about 5 degrees rotation; WAIST & HIPS finding a soft counter-tilt as weight settles onto the back leg; RIGHT LEG easing free and forward soft, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the turn with a settling step; HAIR waves settling soft in the gold light.",
  "hands": "RIGHT HAND drifting to settle the soft silk scarf with an easy roll of the shoulder, RIGHT FINGERS smoothing the silk with soft groomed-nude nail-beds; LEFT HAND resting on the car door, LEFT FINGERS soft; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "In the golden-coastal look, her right hand drifts to settle the silk scarf with an easy roll while the left rests on the car door, weight settling onto the back leg in the deep gold light.",
  "b1": "Cut to a medium close on a new angle in the deep golden light: she is already in the golden-coastal look, her right hand drifting to settle the soft silk scarf with an easy roll of the right shoulder while her left rests on the car door; gaze easing to lens.",
  "b2": "A warm dreamy smile eases to lens on a slow breath, her weight settling onto the back leg, the silk and waves lifting soft in the gold, eyes warm and luminous.",
  "b3": "She holds the golden-coastal look, right fingers easing off the scarf, left on the car door, the silk drifting warm, eyes warm and direct (silent here).",
 },
 6: {
  "posture": "GAZE warm and direct to lens; HEAD turning a soft six degrees toward lens with a tilt into the breeze; SHOULDERS easy with the left carried forward as she steps; RIGHT ARM drifting open from the scarf toward lens in a warm gesture, the RIGHT HAND turning open, RIGHT FINGERS soft; LEFT HAND resting easy on the car door, LEFT FINGERS soft; TORSO turning with the step from the car; WAIST & HIPS swaying with an easy step toward lens, weight transferring forward; RIGHT LEG stepping forward from the car into an easy stride, LEFT LEG pushing off behind; FEET & WEIGHT mid-step, weight rolling onto the forward right foot; HAIR waves streaming with the step.",
  "hands": "RIGHT HAND drifting open soft from the scarf toward the lens in a warm easy gesture as she speaks, RIGHT FINGERS soft; LEFT HAND resting easy on the car door, LEFT FINGERS soft; short almond groomed-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She steps an easy stride from the car toward lens and drifts her right hand open in a warm gesture while the left stays on the car door, hips swaying as her weight rolls onto the forward right foot for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she steps an easy stride from the car toward lens and drifts her right hand open soft in a warm easy gesture, the left staying on the car door, hips swaying as weight rolls onto the forward right foot; the camera eases with her, gaze warm to lens.",
  "b2": "She delivers \u201cSome roads feel like home.\u201d to lens with a warm dreamy smile and natural lip-sync, right fingers soft on the gesture, eyes warm and gentle.",
  "b3": "She holds the golden-coastal look as the silk drifts and her right hand eases back toward the scarf, the smile easing into warm calm.",
 },
 7: {
  "posture": "GAZE easing back to the warm direct-to-lens of Frame 1; HEAD returning level with a soft tilt into the breeze; SHOULDERS easing back, the right carried back over the door; RIGHT ARM extending back to the side as the RIGHT HAND returns to rest soft on the open car door, RIGHT FINGERS draped over the door-top; LEFT ARM easing up, the LEFT HAND light at a wind-blown strand at the cheek, LEFT FINGERS light; TORSO rotating back to about 6 degrees toward the road; WAIST & HIPS returning to the opening contrapposto with the right hip eased toward the car; RIGHT LEG easing to free soft, LEFT LEG re-taking weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance; HAIR waves settling as the gold resolves toward soft afternoon.",
  "hands": "RIGHT HAND returning to rest soft on the open car door exactly as in Frame 1, RIGHT FINGERS draped over the door-top; LEFT HAND easing a wind-blown strand at the cheek, LEFT FINGERS light; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases back precisely to the opening hook — right hand resting soft on the car door, left easing a strand from the cheek, weight settled on the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she eases back to the open convertible and returns her right hand to rest soft on the car door, her left easing a wind-blown strand from her cheek, settling her weight onto the straight left leg exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her warm gaze back to lens on a slow breath with the composed easy quarter-smile, the golden-coastal look resolving toward the breezy-day opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand on the door, left at the strand, weight settled and breezy — a seamless loop seam.",
 },
}

# ============================ CONCEPT 18 — BOOKSHOP (page-flutter · indie store) ============================
# Flow: F1 hero / right holds an open book, left on a shelf-edge -> F2 lift right from book toward cresting pages
#   -> F3 raise toward the pages -> F4 ease right down toward the book, page-flutter sweeps (held angle)
#   -> F5 settle the blazer lapel -> F6 browse-step to lens, line + warm gesture -> F7 loop to the book.
# Energy refined / warm / quiet, with a soft browse-step along the shelf and a lean.
POSE[18] = {
 1: {
  "posture": "GAZE quiet and direct to lens; HEAD level with a soft tilt, neck relaxed; SHOULDERS soft, the right carried forward over the book; RIGHT ARM bent up holding the open book, the RIGHT HAND cradling the spine, RIGHT FINGERS spread soft under the pages; LEFT ARM extended to the shelf, the LEFT HAND resting on a shelf-edge, LEFT FINGERS draped over the wood; TORSO rotated about 5 degrees toward the shelf; WAIST & HIPS in a soft contrapposto with the right hip a touch high; RIGHT LEG the free/forward leg, knee soft, toe grazing; LEFT LEG weight-bearing and straight; FEET & WEIGHT settled on the left foot on the worn floor; HAIR ribboned low ponytail settling soft — refined, warm, alive (living stillness).",
  "hands": "RIGHT HAND holding the open book soft, RIGHT FINGERS spread soft under the pages cradling the spine; LEFT HAND resting on a shelf-edge, LEFT FINGERS draped over the wood; short almond nails in a soft warm nude, neat cuticles, no white-knuckle tension.",
  "framing": "She has just paused at the shelf — right hand holding the open book with fingers under the pages, left resting on a shelf-edge, weight settled on the straight left leg with the right hip a touch high, a refined warm hero pose.",
  "b1": "Cut to a medium-wide thigh-up tracking shot in the warm indie bookstore: the camera dollies laterally to settle on her as she pauses at the shelf — weight settling onto the straight left leg, her right hand holding an open book soft and her left resting on a shelf-edge; the tall worn shelves and brass lamps slide behind with real parallax.",
  "b2": "The track eases to rest as a face-framing wisp shifts in the dust-mote light, the right shoulder soft over the book, and her quiet gaze holds to lens, a warm quarter-smile settling.",
  "b3": "She holds the soft cream-blouse look, right fingers under the pages, left on the shelf-edge, weight grounded through the left leg, eyes quiet and direct in the lamplight (silent here).",
 },
 2: {
  "posture": "GAZE lifting toward the cresting pages; HEAD tilting up about 6 degrees toward the pages; SHOULDERS with the RIGHT shoulder lifting as the hand leaves the book; RIGHT ARM lifting from the book up toward the pages, the RIGHT HAND rising soft as if to feel them, RIGHT FINGERS gently open; LEFT ARM resting on the shelf, the LEFT HAND soft on the shelf-edge, LEFT FINGERS relaxed; TORSO lengthening upward toward the pages; WAIST & HIPS easing as she rises into the reach; RIGHT LEG taking more weight as she reaches, LEFT LEG soft behind; FEET & WEIGHT rolling onto the balls of the feet; HAIR ponytail shifting as she tips up.",
  "hands": "RIGHT HAND lifting soft from the book toward the cresting pages as if to feel them, RIGHT FINGERS gently open; LEFT HAND soft on the shelf, LEFT FINGERS relaxed; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right arm lifts from the book up toward the cresting pages with fingers gently open while the left rests on the shelf, torso lengthening upward and weight rolling onto the balls of the feet.",
  "b1": "Cut to a medium-close three-quarter: she is already lifting her right hand soft from the book toward the cresting pages as if to feel them, fingers gently open, her torso lengthening up and weight rolling onto the balls of her feet, the left hand on the shelf; the camera pushes with her hand, gaze toward the pages.",
  "b2": "The pages stir at her fingertips as her gaze warms with quiet wonder and a soft micro-smile kindles, the head tipped up.",
  "b3": "Her right hand holds open toward the pages, left soft on the shelf, weight poised on the balls of her feet, eyes warm and quiet, the look still the cream blouse — the breath before the flutter (silent here).",
 },
 3: {
  "posture": "GAZE easing from the pages back toward lens; HEAD easing to level; SHOULDERS easing back and down; RIGHT ARM held raised soft toward the pages, the RIGHT HAND open near them, RIGHT FINGERS soft; LEFT ARM easing open on the shelf, the LEFT HAND turning open on the shelf-edge, LEFT FINGERS spreading; TORSO lengthening tall on the breath; WAIST & HIPS easing toward square with a gentle counter-tilt; RIGHT LEG settling firmer as weight centres, LEFT LEG anchoring; FEET & WEIGHT settling even and grounded; HAIR ponytail settling.",
  "hands": "RIGHT HAND raised soft toward the pages, RIGHT FINGERS soft near them; LEFT HAND easing open on the shelf, LEFT FINGERS spreading; short almond warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "Her right hand holds raised soft toward the pages while the left eases open on the shelf with spreading fingers, the torso lengthening tall as her weight settles even and grounded.",
  "b1": "Cut to a medium chest-up on a fresh three-quarter angle: she raises her right hand soft toward the pages and draws a slow breath, her left hand easing open on the shelf as her weight settles even; the camera arcs a few degrees and the shelves swing behind with parallax, gaze lifting.",
  "b2": "The arc settles as her gaze eases to lens with rising warmth and a soft micro-smile forms, the look still the cream blouse in soft daylight.",
  "b3": "She holds the poised quiet beat, right hand soft toward the pages, left open on the shelf, weight even and grounded, eyes warm and refined — the breath before the flutter (silent here).",
 },
 4: {
  "posture": "GAZE warm, easing to follow the page-flutter; HEAD held level with a soft tilt; SHOULDERS easing soft; RIGHT ARM easing down toward the book, the RIGHT HAND lowering soft, RIGHT FINGERS relaxed; LEFT ARM opening out from the shelf as a soft counterweight, the LEFT HAND turning open, LEFT FINGERS soft; TORSO lengthening and beginning a soft open turn from the waist; WAIST & HIPS easing into a gentle rotation as weight rolls; RIGHT LEG taking weight onto the ball of the right foot, LEFT LEG easing free with the heel lifting; FEET & WEIGHT in a soft grounded turn — the body opens warm while the camera angle holds.",
  "hands": "RIGHT HAND easing soft down from the cresting pages toward the book, RIGHT FINGERS relaxed; LEFT ARM opening out from the shelf as a soft counterweight, LEFT HAND turning open with LEFT FINGERS soft; short warm-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases her right hand down toward the book, the left opening out from the shelf as a soft counterweight, turning gently onto the ball of the right foot while the camera angle holds and the pages flutter around her.",
  "b1": "Cut to an energized medium at a HELD angle (Veo first frame = the soft-day Look A still): she eases her right hand down from the pages toward the book, her left arm opening out from the shelf as a soft counterweight, turning onto the ball of her right foot — still the cream blouse, NO flutter yet, a gentle push-with easing in, the angle fixed for the whole clip.",
  "b2": "The page-flutter BEGINS here, mid-clip: a single travelling page-flutter sweeps smoothly across the frame in one continuous warm front as her torso opens through the turn, real book pages fluttering up by believable paper weight and air-drift, the soft cream blouse deepening into the tailored caramel blazer over a soft knit vest and the room warming to a snug reading glow exactly where the flutter passes — cloth resolving with real spread and inertia, gradual and warm, never a snap, no garish glare; the ribboned ponytail catching travelling amber light, eyes warming in refined wonder (angle held, face cleanly lit, identity locked).",
  "b3": "The flutter completes its sweep as she settles through the soft turn and the look resolves smoothly and fully into the refined-warm Look B of the Veo last-frame still (Frame 5's image) — the tailored caramel blazer over the knit vest and blouse in a snug amber reading glow, held through the final beat, no last-second pop; a warm refined calm landing in her eyes.",
 },
 5: {
  "posture": "GAZE easing warm to lens; HEAD settling level with a soft tilt; SHOULDERS easing with a soft roll of the right; RIGHT ARM rising, the RIGHT HAND drifting to settle the blazer lapel, RIGHT FINGERS smoothing the lapel-edge; LEFT ARM easing to the shelf, the LEFT HAND resting on the shelf-edge, LEFT FINGERS soft; TORSO settling tall out of the turn to about 4 degrees rotation; WAIST & HIPS finding a soft counter-tilt as weight settles onto the back leg; RIGHT LEG easing free and forward soft, LEFT LEG re-taking weight; FEET & WEIGHT re-grounding from the turn with a settling step; HAIR ponytail settling soft in the amber glow.",
  "hands": "RIGHT HAND drifting to settle the blazer lapel with an easy roll of the shoulder, RIGHT FINGERS smoothing the lapel-edge with soft groomed-nude nail-beds; LEFT HAND resting on the shelf-edge, LEFT FINGERS soft; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "In the refined-warm look, her right hand drifts to settle the blazer lapel with an easy roll while the left rests on the shelf-edge, weight settling onto the back leg in the amber reading glow.",
  "b1": "Cut to a medium close on a new angle in the snug amber reading glow: she is already in the refined warm look, her right hand drifting to settle the blazer lapel with an easy roll of the right shoulder while her left rests on the shelf-edge; gaze easing to lens.",
  "b2": "A warm refined smile eases to lens on a slow breath, her weight settling onto the back leg, the amber glow warming the ponytail, eyes warm and quiet.",
  "b3": "She holds the refined-warm look, right fingers easing off the lapel, left on the shelf, the reading glow snug, eyes warm and direct (silent here).",
 },
 6: {
  "posture": "GAZE warm and direct to lens; HEAD turning a soft six degrees toward lens with a gentle tilt; SHOULDERS soft with the left carried forward as she steps; RIGHT ARM drifting open from the lapel toward lens in a warm gesture, the RIGHT HAND turning open, RIGHT FINGERS soft; LEFT HAND resting easy on the shelf, LEFT FINGERS soft; TORSO turning with a soft browse-step along the shelf; WAIST & HIPS swaying with an easy step toward lens, weight transferring forward; RIGHT LEG stepping forward into an easy browse-step, LEFT LEG pushing off behind; FEET & WEIGHT mid-step, weight rolling onto the forward right foot; HAIR ponytail shifting with the step.",
  "hands": "RIGHT HAND drifting open soft from the lapel toward the lens in a warm easy gesture as she speaks, RIGHT FINGERS soft; LEFT HAND resting easy on the shelf, LEFT FINGERS soft; short almond groomed-nude nails, neat cuticles, no white-knuckle tension.",
  "framing": "She takes a soft browse-step along the shelf toward lens and drifts her right hand open in a warm gesture while the left stays on the shelf, hips swaying as her weight rolls onto the forward right foot for the line.",
  "b1": "Cut to a medium chest-up on a fresh angle: she takes a soft browse-step along the shelf toward lens and drifts her right hand open in a warm easy gesture, the left staying on the shelf, hips swaying as weight rolls onto the forward right foot; the camera eases with her, gaze warm to lens.",
  "b2": "She delivers \u201cLost in the pages, found myself.\u201d to lens with a warm refined smile and natural lip-sync, right fingers soft on the gesture, eyes warm and quiet.",
  "b3": "She holds the refined-warm look as the lamplight glows and her right hand eases back toward the lapel, the smile easing into warm calm.",
 },
 7: {
  "posture": "GAZE easing back to the quiet direct-to-lens of Frame 1; HEAD returning level with a soft tilt; SHOULDERS softening back, the right carried forward over the book; RIGHT ARM bending back up holding the open book as the RIGHT HAND cradles the spine, RIGHT FINGERS spread soft under the pages; LEFT ARM extending to the shelf, the LEFT HAND resting on the shelf-edge, LEFT FINGERS draped; TORSO rotating back to about 5 degrees toward the shelf; WAIST & HIPS returning to the opening contrapposto with the right hip a touch high; RIGHT LEG easing to free and forward soft, LEFT LEG re-taking weight straight; FEET & WEIGHT re-grounding into the exact Frame-1 stance; HAIR ponytail settling as the amber resolves toward soft daylight.",
  "hands": "RIGHT HAND returning to hold the open book soft exactly as in Frame 1, RIGHT FINGERS spread soft under the pages; LEFT HAND resting on the shelf-edge, LEFT FINGERS draped; short almond nails, neat cuticles, no white-knuckle tension.",
  "framing": "She eases back precisely to the opening hook — right hand holding the open book with fingers under the pages, left on the shelf-edge, weight settled on the straight left leg in the Frame-1 contrapposto for a seamless loop.",
  "b1": "Cut to a medium-wide thigh-up matched to Frame 1: she eases back to the shelf and returns her right hand to hold the open book soft, her left hand on the shelf-edge, settling her weight onto the straight left leg exactly as in Frame 1 as the camera settles to the opening framing.",
  "b2": "She eases her quiet gaze back to lens on a slow breath with the composed warm quarter-smile, the refined-warm look resolving toward the soft-day opening to seed the loop.",
  "b3": "She lands precisely on the Frame 1 pose and gaze — right hand holding the book, left on the shelf, weight settled and refined — a seamless loop seam.",
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

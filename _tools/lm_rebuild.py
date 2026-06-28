#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L+M RETROFIT engine — rewrites the EXISTING `SHOT BREAKDOWN` blocks of an
already-advanced concept into the new transformation model (steering sections
L + M):
  * the A->B change happens MID-CLIP inside the transform frame at a HELD angle,
  * every frame join reads as a CUT to a new angle/crop,
  * the transform clip's second half is fully-resolved Look B (carried to the
    next image prompt),
  * ALIVE camera: active subject + camera that rides with her (track/follow/
    arc/push-with) through an anchored world with real parallax.

Unlike md_rebuild.py (which matched `SUBJECT ACTION WITH TIMING`), this matches
the existing `SHOT BREAKDOWN (timed ...):` + its three `- [..]` beat lines and
swaps in new beats. DURATION / FRAME RATE are already standard, so they are left
untouched. Image-prompt edits (transform still -> Look A, next still -> matched
Look B, decoupling the old cross-frame keyframe notes) are done separately.

Idempotent. Usage:  python3 _tools/lm_rebuild.py "<path>" <concept_number>
"""
import re
import sys

BREAKDOWN_HEADER = (
    "SHOT BREAKDOWN (timed, 6s \u00b7 real-time, continuous energetic motion "
    "\u2014 never slow-motion, never a static hold; expression eye-led and "
    "identity-safe):"
)

BEATSLM = {}

BEATSLM[1] = [
    # F1 - Look A establishing, ALIVE lateral track, cut in
    (
        "Cut to a medium-wide thigh-up tracking shot in the steel studio: the camera dollies "
        "laterally to settle on her as she steps her weight onto the back leg and sets her "
        "right hand to her hip with the brushed-steel cuff forward, the gunmetal panels "
        "sliding behind with real parallax; one ice-blue specular travelling the bodice.",
        "The track eases to rest as a face-framing finger-wave shifts in the cool draft and "
        "her cool gaze begins to lift, a composed powerful quarter-smile settling.",
        "She holds the architectural steel look, eyes direct and cool, the specular sliding "
        "the polished gunmetal (silent here).",
    ),
    # F2 - Look A build, push-with the wrist, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter on the cuff: she is already raising her right "
        "wrist toward her collarbone and turning the brushed-steel cuff into the cool key as "
        "the camera pushes with the wrist; gaze lowering to the steel.",
        "An ice-blue specular travels the turning cuff as her gaze cools with quiet focus and "
        "a knowing micro-smile kindles.",
        "She studies the steel cuff, eyes steady and cool, lips parting a millimetre in "
        "composed calm \u2014 still fully steel.",
    ),
    # F3 - Look A clean (NO dissolve here), slow arc to a fresh angle, cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases both hands open "
        "from her body, palms turning up, drawing a slow composed breath as the camera arcs a "
        "few degrees and the panels swing behind with parallax; gaze beginning to lift.",
        "The arc settles as her gaze lifts to lens with rising calm and a serene knowing "
        "micro-smile forms, the gunmetal still at its sharpest cool polish.",
        "She holds the poised steel beat, hands open and ready, eyes calm and architectural "
        "\u2014 the composed breath before the change (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip morph; Veo first=Look A still, last=Look B still
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the steel Look A "
        "still): she opens her arms in the gunmetal gown, already in motion, a gentle "
        "push-with easing toward her \u2014 the steel look fully intact, NO change yet, the "
        "angle fixed for the whole clip.",
        "The morph BEGINS here, mid-clip: a warm dissolve-front starts at her near shoulder "
        "and travels smoothly and diagonally down across the gown in one continuous liquid "
        "wavefront, polished gunmetal turning to flowing champagne silk exactly where it "
        "passes \u2014 gradual and motivated, never a snap; eyes warming in serene awe as it "
        "crosses (angle held, identity locked).",
        "The wavefront completes its sweep and the look settles smoothly and fully into the "
        "champagne-silk Look B of the Veo last-frame still (Frame 5's image), resolved and "
        "held through the final beat \u2014 no last-second pop; a soft serene warmth landing "
        "in her eyes.",
    ),
    # F5 - Look B clean reveal, cut to a NEW angle, slow push
    (
        "Cut to a medium close on a new angle in the warmed silk space: she is already in the "
        "champagne silk-satin gown, gathering a soft fold of silk near her waist as a slow "
        "push eases in and warm motes settle; gaze easing to lens.",
        "A serene smile eases to lens on a slow warm breath, a warm specular travelling the "
        "satin cowl, eyes soft and luminous.",
        "She holds the warm serene silk look, the drape settling soft, eyes shining direct "
        "(silent here).",
    ),
    # F6 - Look B spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she turns a soft six degrees toward lens "
        "and opens her right hand in a gentle gesture as the camera eases with her; gaze warm "
        "to lens.",
        "She delivers \u201cSteel to silk. Same power, softer edge.\u201d to lens with a soft "
        "knowing smile and natural lip-sync, the pearl drop swinging a hair, eyes warm and "
        "direct.",
        "She holds the warm serene look as the silk settles, the smile easing into calm.",
    ),
    # F7 - loop close, cut back to match Frame 1
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "light on her hip and settles her weight onto the back leg exactly as in Frame 1 as "
        "the camera settles to the opening framing.",
        "She eases her gaze back to lens on a slow breath with the composed quarter-smile, "
        "the silk-warm space resolving toward the steel-cool opening palette to seed the "
        "loop.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled and architectural "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[3] = [
    # F1 - saree Look A establishing, alive lateral track, cut in
    (
        "Cut to a medium-wide thigh-up tracking shot in the marigold-lit haveli courtyard: the "
        "camera dollies laterally to settle on her as she steps her weight onto the back leg "
        "and rests her right hand soft at the gold zari pallu over her shoulder, the sandstone "
        "arches and incense haze sliding behind with real parallax; a regal quarter-smile "
        "holding.",
        "The track eases to rest as a face-framing tendril shifts in the courtyard draft and "
        "her warm gaze begins to lift, the regal quarter-smile settling.",
        "She holds the warm regal saree look, eyes warm and direct, the gold zari glinting in "
        "the tungsten glow (silent here).",
    ),
    # F2 - saree, push-with raising the pallu fold, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter on the pallu: she is already raising a fold of the "
        "gold zari pallu near her collarbone and turning it into the warm key as the camera "
        "pushes with her hand; gaze lowering to the gold thread.",
        "A warm specular travels the zari as her gaze warms with quiet focus and a knowing "
        "micro-smile kindles.",
        "She studies the glowing pallu, eyes steady and warm, lips parting a millimetre in "
        "regal calm \u2014 still fully saree.",
    ),
    # F3 - saree clean (NO unwind yet), slow arc to a fresh angle, cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases both hands open "
        "from her body as if to release the drape, drawing a slow breath as the camera arcs a "
        "few degrees and the courtyard swings behind with parallax; gaze beginning to lift.",
        "The arc settles as her gaze lifts to lens with rising spirit and a knowing micro-smile "
        "forms, the magenta silk still richly draped and fully intact.",
        "She holds the poised saree beat, hands open and ready, eyes bright and spirited \u2014 "
        "the breath before the unwind (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip morph; Veo first=saree still, last=streetwear still
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the magenta-saree Look A "
        "still): she opens her arms, already in motion \u2014 the saree fully draped and intact, "
        "NO change yet, a gentle push-with easing in, the angle fixed for the whole clip.",
        "The morph BEGINS here, mid-clip: a cooling unwind-front starts at the pallu on her "
        "shoulder and spirals smoothly down and around her in one continuous ribbon, the "
        "magenta silk and gold zari unwinding and reforming into the cream-and-graphite bomber "
        "and tapered cargos exactly where it passes \u2014 gradual and liquid, never a snap; "
        "eyes bright with spirited joy as it crosses (angle held, identity locked).",
        "The ribbon completes its spiral and the look settles smoothly and fully into the "
        "streetwear Look B of the Veo last-frame still (Frame 5's image), resolved and held "
        "through the final beat \u2014 no last-second pop; an easy cool confidence landing in "
        "her eyes.",
    ),
    # F5 - streetwear Look B reveal, cut to a NEW angle, adjust bomber collar
    (
        "Cut to a medium close on a new angle in the cool mural-street light: she is already in "
        "the cream-and-graphite bomber and cargos, reaching up to adjust the bomber collar with "
        "an easy roll of the shoulder; gaze easing to lens.",
        "A confident smile eases to lens on a slow cool breath, the last motes settling, eyes "
        "relaxed and direct.",
        "She holds the cool easy streetwear look, the bomber settling soft, eyes relaxed and "
        "bright (silent here).",
    ),
    # F6 - streetwear spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed gesture as the camera eases with "
        "her; gaze easy to lens.",
        "She delivers \u201cSaree to streetwear. Same roots, new stride.\u201d to lens with a "
        "soft knowing smile and natural lip-sync, the small gold hoops catching light, eyes "
        "warm and cool-confident.",
        "She holds the cool easy look as the bomber settles, the smile easing into relaxed "
        "warmth.",
    ),
    # F7 - loop close, cut back to match Frame 1 saree courtyard
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft at the zari pallu over her shoulder and settles her weight onto the back leg "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her gaze back to lens on a slow breath with the composed regal quarter-smile, "
        "the cool street palette resolving toward the warm courtyard opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled and regal \u2014 a "
        "seamless loop seam.",
    ),
]


BEATSLM[4] = [
    # F1 - spring Look A establishing, alive lateral track, cut in
    (
        "Cut to a medium-wide thigh-up tracking shot by the lone meadow tree in spring: the "
        "camera dollies laterally to settle on her as she steps her weight onto the back leg "
        "and rests her right hand soft at the fishtail braid over her shoulder, pink blossom "
        "and the tree sliding behind with real parallax; a serene quarter-smile holding.",
        "The track eases to rest as a face-framing wisp shifts in the spring breeze and her "
        "calm gaze begins to lift, the serene quarter-smile settling, petals drifting in the "
        "soft sky-light.",
        "She holds the serene spring look in her cream knit and dusty-rose cardigan, eyes calm "
        "and direct (silent here).",
    ),
    # F2 - spring, push-with toward the blossom branch, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already raising a soft hand toward a low "
        "blossom branch and grazing the petals as the camera pushes with her hand; gaze toward "
        "the blossom.",
        "The petals stir at her fingertips as her gaze warms with quiet wonder and a knowing "
        "micro-smile kindles.",
        "A petal lifts free, her eyes soft on the blossom, lips parting a millimetre in gentle "
        "wonder \u2014 still full spring.",
    ),
    # F3 - spring clean (NO turn yet), slow arc to a fresh angle, cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases both hands open and "
        "out as if to feel the air, drawing a slow breath as the camera arcs a few degrees and "
        "the spring meadow swings behind with parallax; gaze beginning to lift.",
        "The arc settles as her gaze lifts to lens with rising wonder and a knowing micro-smile "
        "forms, the canopy still in full spring blossom.",
        "She holds the poised spring beat, hands open and ready, eyes bright with wonder \u2014 "
        "the breath before the seasons turn (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip 4-season morph; Veo first=spring, last=winter
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the spring Look A "
        "still): she opens her arms and holds centre, already in motion \u2014 full spring "
        "blossom and her dusty-rose cardigan intact, NO change yet, a gentle push-with easing "
        "in, the angle fixed for the whole clip.",
        "The four-season turn BEGINS here, mid-clip: a travelling ring sweeps smoothly around "
        "her in one continuous wavefront \u2014 spring blossom giving to summer green, then to "
        "autumn leaf-fall as it passes, the tree, ground, light and her layers turning along "
        "the same front (cardigan easing to the bare summer dress, then a camel trench and rust "
        "scarf forming), gradual and continuous, never a snap; eyes wide with wonder as it "
        "crosses (angle held, identity locked).",
        "The ring completes its turn and settles smoothly and fully into the winter Look B of "
        "the Veo last-frame still (Frame 5's image) \u2014 cream wool coat, oatmeal scarf and "
        "knit beanie under soft snow, resolved and held through the final beat, no last-second "
        "pop; a serene grounded calm landing in her eyes.",
    ),
    # F5 - winter Look B reveal, cut to a NEW angle, adjust scarf
    (
        "Cut to a medium close on a new angle in soft falling snow: she is already in the cream "
        "wool coat and oatmeal scarf, reaching up to adjust the scarf at her neck with an easy "
        "roll of the shoulder; gaze easing to lens.",
        "A serene smile eases to lens on a slow cool breath, the last flakes settling around "
        "her, eyes calm and direct.",
        "She holds the calm cosy winter look, the coat and scarf settling, eyes serene and "
        "bright (silent here).",
    ),
    # F6 - winter spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right mittened hand in a relaxed gesture as the camera "
        "eases with her; gaze calm to lens.",
        "She delivers \u201cSeasons change. I don\u2019t.\u201d to lens with a soft serene "
        "smile and natural lip-sync, soft snow drifting, eyes calm and warm.",
        "She holds the calm cosy look as the coat settles, the smile easing into grounded "
        "warmth.",
    ),
    # F7 - loop close, cut back to match Frame 1 spring
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft at the fishtail braid over her shoulder and settles her weight onto the back leg "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her calm gaze back to lens on a slow breath with the composed serene "
        "quarter-smile, the winter palette resolving toward the spring blossom opening to seed "
        "the loop.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled and serene \u2014 a "
        "seamless loop seam.",
    ),
]


BEATSLM[2] = [
    # F1 - Paris held city, alive lateral track, cut in
    (
        "Cut to a medium-wide thigh-up tracking shot on the Haussmann Paris balcony at "
        "silver-blue dawn: the camera dollies laterally to settle on her as she steps her "
        "weight onto the back leg and tucks her right hand into the coat pocket, the "
        "wrought-iron railings and zinc rooftops sliding behind with real parallax; a composed "
        "quarter-smile holding.",
        "The track eases to rest as a centre-part strand lifts in the dawn breeze and her warm "
        "gaze begins to lift, a worldly calm settling.",
        "She holds the assured Paris look, eyes direct and worldly, the cool dawn light on the "
        "rooftops (silent here).",
    ),
    # F2 - MATCH-CUT to Tokyo (pose held = one her), alive track
    (
        "Match-cut to a medium-wide thigh-up on a rain-glossed neon-dusk Tokyo crossing \u2014 "
        "her pose and face held identical (one her), now in the Tokyo look: she eases her "
        "right hand from the pocket to the lapel as the camera tracks with her, neon signage "
        "and wet-asphalt reflections sliding behind with parallax.",
        "She holds the identical composed quarter-smile through the city-change, neon "
        "catchlights warming her eyes (identity locked across the match-cut).",
        "A strand lifts in the Tokyo draft, her gaze steady to lens, assured and unchanged "
        "(silent here).",
    ),
    # F3 - MATCH-CUT to New York, alive track
    (
        "Match-cut to a medium chest-up on a steam-and-steel Manhattan street at golden hour "
        "\u2014 pose held: she eases her right hand open from the lapel in a soft confident "
        "gesture as the camera tracks the street edge, yellow cabs and rising steam sliding "
        "behind with parallax; gaze direct.",
        "Her gaze holds to lens with rising assurance and the composed smile lifts, warm gold "
        "light raking the avenue.",
        "She holds the assured New York beat, eyes steady and worldly (silent here).",
    ),
    # F4 - MATCH-CUT to Mumbai (the signature city), alive arc, held look (NOT a morph)
    (
        "Match-cut to an energized medium on a gold-teal Mumbai sea-link evening \u2014 pose "
        "held identical (one her), now in the Mumbai look: she opens her right hand in a warm "
        "worldly gesture as the camera arcs a few degrees with her, the sea-link cables and a "
        "lit archway sliding behind with parallax.",
        "She holds the composed quarter-smile, the dupatta and lob catching the warm evening "
        "light, eyes bright with worldly wonder (identity locked across the match-cut).",
        "She holds the assured Mumbai beat at its warm golden peak, eyes warm and direct \u2014 "
        "the signature city (silent here).",
    ),
    # F5 - MATCH-CUT to London, alive
    (
        "Match-cut to a medium close on a cool-overcast London stone-and-mist lane \u2014 pose "
        "held: she eases her right hand to hold the trench lapel as the camera eases with her, "
        "Portland-stone fa\u00e7ades and soft mist sliding behind; gaze easing to lens.",
        "An assured calm settles to lens on a slow cool breath, the last mist drifting in the "
        "grey light.",
        "She holds the cool assured London look, the trench settling, eyes calm and direct "
        "(silent here).",
    ),
    # F6 - MATCH-CUT to Dubai, spoken line, alive
    (
        "Match-cut to a medium chest-up in warm champagne Dubai sky-deck light \u2014 pose "
        "held: she turns a soft six degrees toward lens and opens her right hand in a gentle "
        "gesture as the camera eases with her, the skyline glittering behind; gaze warm to "
        "lens.",
        "She delivers \u201cSix cities. One her. Wherever I land \u2014 still me.\u201d to lens "
        "with a soft knowing smile and natural lip-sync, eyes warm and assured.",
        "She holds the warm assured look as the coat settles, the smile easing into calm "
        "confidence.",
    ),
    # F7 - MATCH-CUT back to Paris, loop close
    (
        "Match-cut back to the medium-wide thigh-up Paris balcony matched to Frame 1 \u2014 "
        "pose held: she returns her right hand to the coat pocket and settles her weight onto "
        "the back leg exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her gaze back to lens on a slow breath with the composed quarter-smile, the "
        "dawn Paris palette resolving to the opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled and worldly \u2014 a "
        "seamless loop seam.",
    ),
]


BEATSLM[5] = [
    # F1 - black Look A establishing, alive lateral track, snap-ready, cut in
    (
        "Cut to a medium-wide thigh-up tracking shot against the graphite cyclorama: the camera "
        "dollies laterally to settle on her as she steps her weight onto the back leg and "
        "raises her right hand to chest height, thumb and middle finger lightly together ready "
        "to snap, the studio sliding behind with real parallax; a sharp quarter-smile holding.",
        "The track eases to rest as a fringe edge shifts in the studio air and her bold gaze "
        "begins to lift, a playful spark settling at the outer eye.",
        "She holds the sharp all-black editorial look, eyes direct and bold, fingers poised to "
        "snap (silent here).",
    ),
    # F2 - black Look A, push-with the snapping hand near cheek, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already raising the snapping hand near her "
        "cheek, thumb and middle finger pressed ready, as the camera pushes with her hand; gaze "
        "toward the fingers.",
        "Her gaze sharpens with playful focus on the fingertips as a knowing micro-smile "
        "kindles.",
        "Her fingers hold poised at the ready, eyes bright and playful, the all-black set crisp "
        "and intact \u2014 the hush before the snap (silent here).",
    ),
    # F3 - black Look A, arc, presses the snap-point (NO flip yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she presses her thumb and "
        "middle finger hard at the snap-point and eases her left hand open, drawing a slow "
        "breath as the camera arcs a few degrees and the cyclorama swings behind with parallax; "
        "gaze beginning to lift.",
        "The arc settles as her gaze lifts to lens with rising spark and a knowing micro-smile "
        "forms, the all-black set still crisp and fully intact.",
        "She holds the poised black beat, fingers tensed at the snap-point, eyes bright and "
        "ready \u2014 the charged instant before the snap (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth-but-crisp mid-clip snap-pulse; first=black, last=white
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the all-black Look A "
        "still): she holds the snap-ready pose, already in motion \u2014 the sharp black set "
        "fully intact, NO change yet, a gentle push-with easing in, the angle fixed for the "
        "whole clip.",
        "The change BEGINS here, mid-clip: she snaps her fingers crisp and a clean editorial "
        "light-pulse rings out and sweeps across her in one quick continuous wavefront, the "
        "all-black tailored set flipping to the bold sculptural all-white set exactly where the "
        "pulse passes \u2014 crisp and clean but smooth, starting here in the middle, never an "
        "instant last-second cut; the bob catching travelling light, eyes wide with playful "
        "spark (angle held, identity locked).",
        "The pulse completes its sweep and the look settles smoothly and fully into the "
        "all-white Look B of the Veo last-frame still (Frame 5's image), resolved and held "
        "through the final beat \u2014 no last-second pop; a sharp confidence landing in her "
        "eyes.",
    ),
    # F5 - white Look B reveal, cut to a NEW angle, adjust white lapel
    (
        "Cut to a medium close on a new angle in brighter white-studio light: she is already in "
        "the bold all-white set, reaching up to adjust the white lapel with an easy roll of the "
        "shoulder; gaze easing to lens.",
        "A sharp confident smile eases to lens on a slow breath, the last light-sparks "
        "settling, eyes sharp and direct.",
        "She holds the assured all-white editorial look, the white set crisp, eyes sharp and "
        "bright (silent here).",
    ),
    # F6 - white spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed sharp gesture as the camera "
        "eases with her; gaze direct to lens.",
        "She delivers \u201cOne snap. New me.\u201d to lens with a sharp knowing smile and "
        "natural lip-sync, eyes bold and direct.",
        "She holds the assured editorial look as the white set settles, the smile easing into "
        "sharp calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 black snap-ready
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to the "
        "poised snap-ready pose at chest height and settles her weight onto the back leg "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her gaze back to lens on a slow breath with the composed sharp quarter-smile, "
        "the white palette resolving toward the graphite opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled and sharp \u2014 a "
        "seamless loop seam.",
    ),
]


BEATSLM[6] = [
    # F1 - closed-bud garden Look A establishing, alive lateral track, flacon at waist
    (
        "Cut to a medium-wide thigh-up tracking shot in the moonlit night garden: the camera "
        "dollies laterally to settle on her as she steps her weight onto the back leg and "
        "cradles the fragrance flacon at waist height, the dark closed night-blooms and trellis "
        "sliding behind with real parallax; a serene half-smile holding.",
        "The track eases to rest as a face-framing tendril drifts in the night breeze and her "
        "serene gaze begins to ease to lens, low ground-mist curling.",
        "She holds, romantic and still in the midnight-blue satin, eyes soft in the moon glow, "
        "the buds dark and closed around her (silent here).",
    ),
    # F2 - closed buds, push-with raising flacon to collarbone, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already raising the flacon near her "
        "collarbone and resting her index finger at the atomizer as the camera pushes with her "
        "hand; gaze toward the flacon.",
        "Her gaze softens toward the flacon as a dreamy micro-smile kindles, she drawing a slow "
        "breath.",
        "She holds the flacon poised at her collarbone, eyes soft and dreamy, the night blooms "
        "still dark and closed behind (silent here).",
    ),
    # F3 - closed buds, arc, presses atomizer (mist releasing, NO bloom yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she presses the atomizer and "
        "a fine fragrance-mist releases as the camera arcs a few degrees and the trellis swings "
        "behind with parallax; gaze beginning to lift.",
        "The arc settles as her gaze lifts to lens with rising warmth and a tender micro-smile "
        "forms, the buds still closed dark in the moonlight.",
        "She holds the poised mist beat, the fine mist drifting, eyes warm with wonder \u2014 "
        "the breath before the bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip bloom; first=closed-bud, last=full-bloom
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the closed-bud Look A "
        "still): she eases the flacon down from the mist, already in motion \u2014 the "
        "night-flowers still closed dark buds, NO bloom yet, a gentle push-with easing in, the "
        "angle fixed for the whole clip.",
        "The bloom BEGINS here, mid-clip: from the fragrance mist a soft bloom-wave rolls out "
        "and travels smoothly around her in one continuous expanding front, the closed dark "
        "buds unfurling open pale and luminous exactly where the wave passes \u2014 petals "
        "opening on believable soft spring, fine luminous pollen-motes drifting like real "
        "flecks, gradual and tender, never a snap; eyes widening in radiant wonder (angle "
        "held, identity locked).",
        "The bloom-wave completes its sweep and the garden settles smoothly and fully into the "
        "full-bloom Look B of the Veo last-frame still (Frame 5's image) \u2014 pale luminous "
        "flowers open across the trellis and vines, resolved and held through the final beat, "
        "no last-second pop; a soft radiant calm landing in her eyes.",
    ),
    # F5 - full-bloom Look B reveal, cut to a NEW angle, flacon to waist
    (
        "Cut to a medium close on a new angle amid the bloomed garden: she is already lowering "
        "the flacon to rest at her waist with an easy roll of the shoulder, pale blooms open "
        "around her; gaze easing to lens.",
        "A soft radiant smile eases to lens on a slow breath, the last pollen-motes settling "
        "among the open blooms, eyes soft and luminous.",
        "She holds the serene radiant look, the blooms breathing pale around her, eyes soft "
        "and direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a soft gesture as the camera eases with "
        "her; gaze warm to lens.",
        "She delivers \u201cSome nights, you just bloom.\u201d to lens with a soft radiant "
        "smile and natural lip-sync, eyes warm and serene.",
        "She holds the serene look as the bloomed petals breathe soft, the smile easing into "
        "calm radiance.",
    ),
    # F7 - loop close, cut back to match Frame 1 closed-bud garden
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns the flacon to cradle at "
        "waist height and settles her weight onto the back leg exactly as in Frame 1 as the "
        "camera settles to the opening framing.",
        "She eases her serene gaze back to lens on a slow breath with the composed half-smile, "
        "the open blooms resolving toward the closed-bud opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled in the moonlight "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[7] = [
    # F1 - plain golden-light Look A establishing, alive lateral track, flacon at waist
    (
        "Cut to a medium-wide thigh-up tracking shot on the warm golden-hour rooftop: the "
        "camera dollies laterally to settle on her as she steps her weight onto the back leg "
        "and cradles the amber flacon at waist height, the hazy gold skyline and rooftop edge "
        "sliding behind with real parallax; a warm half-smile holding.",
        "The track eases to rest as a face-framing wisp drifts in the rooftop breeze and her "
        "serene gaze begins to ease to lens, the low sun warm on the satin.",
        "She holds, warm and still in the champagne-gold satin, eyes soft in the low sun, the "
        "light plain and golden around her (silent here).",
    ),
    # F2 - plain light, push-with raising flacon to collarbone, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already raising the flacon near her "
        "collarbone and resting her index finger at the atomizer as the camera pushes with her "
        "hand; gaze toward the flacon.",
        "Her gaze softens toward the flacon as a dreamy micro-smile kindles, she drawing a slow "
        "breath, the low sun gilding the chignon.",
        "She holds the flacon poised at her collarbone, eyes soft and dreamy, the light still "
        "plain golden behind (silent here).",
    ),
    # F3 - plain light, arc, presses atomizer (mist releasing, NO wrap yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she presses the atomizer and "
        "a fine fragrance-mist releases as the camera arcs a few degrees and the rooftop swings "
        "behind with parallax; gaze beginning to lift.",
        "The arc settles as her gaze lifts to lens with rising warmth and a tender micro-smile "
        "forms, the light still plain golden-hour sun.",
        "She holds the poised mist beat, the fine mist drifting in the low sun, eyes warm with "
        "wonder \u2014 the breath before the wrap (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip gold-dust wrap; first=plain-light, last=full-wrap
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the plain golden-light "
        "Look A still): she eases the flacon down from the mist, already in motion \u2014 the "
        "light still plain golden-hour sun, NO gold-dust yet, a gentle push-with easing in, the "
        "angle fixed for the whole clip.",
        "The wrap BEGINS here, mid-clip: from the fragrance mist the low sunbeams visibly turn "
        "to fine gold dust and spiral smoothly around her in one continuous travelling ring, "
        "the air and satin edges gilding exactly where the spiral passes \u2014 fine gold motes "
        "streaming on believable airborne drift like real flecks, gradual and tender, never a "
        "snap; eyes widening in radiant wonder (angle held, identity locked).",
        "The gold-dust spiral completes its sweep and the scene settles smoothly and fully "
        "into the full gold-dust-wrap Look B of the Veo last-frame still (Frame 5's image) "
        "\u2014 fine luminous gold dust wrapped around her in the warm light, resolved and held "
        "through the final beat, no last-second pop; a soft radiant calm landing in her eyes.",
    ),
    # F5 - full gold-dust-wrap Look B reveal, cut to a NEW angle, flacon to waist
    (
        "Cut to a medium close on a new angle in the gilded gold-dust air: she is already "
        "lowering the flacon to rest at her waist with an easy roll of the shoulder, fine gold "
        "motes drifting around her; gaze easing to lens.",
        "A soft radiant smile eases to lens on a slow breath, the last gold motes settling in "
        "the warm light, eyes soft and luminous.",
        "She holds the serene radiant look, the gold dust drifting warm around her, eyes soft "
        "and direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a soft gesture as the camera eases with "
        "her; gaze warm to lens.",
        "She delivers \u201cSome moments just stay golden.\u201d to lens with a soft radiant "
        "smile and natural lip-sync, eyes warm and serene.",
        "She holds the serene look as the gold dust drifts soft, the smile easing into calm "
        "radiance.",
    ),
    # F7 - loop close, cut back to match Frame 1 plain golden light
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns the amber flacon to "
        "cradle at waist height and settles her weight onto the back leg exactly as in Frame 1 "
        "as the camera settles to the opening framing.",
        "She eases her serene gaze back to lens on a slow breath with the composed half-smile, "
        "the gold-dust wrap resolving toward the plain golden-light opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled in the low sun "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[8] = [
    # F1 - all-ivory Look A establishing, alive lateral track, hand at sternum
    (
        "Cut to a medium-wide thigh-up tracking shot in the pure all-ivory editorial world: the "
        "camera dollies laterally to settle on her as she steps her weight onto the back leg "
        "and rests her right hand soft at her sternum, the ivory cyclorama and props sliding "
        "behind with real parallax; a composed quarter-smile holding.",
        "The track eases to rest as a strand of the sleek straight centre-part fall shifts in "
        "the studio air and her cool gaze begins to lift, a composed editorial micro-smile "
        "settling.",
        "She holds, pure and poised in the all-ivory set, eyes direct and architectural (silent "
        "here).",
    ),
    # F2 - ivory, push-with, hand flat at sternum, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she rests her hand flat-soft at her sternum and "
        "gently spreads her fingers as if feeling the breath, as the camera pushes with her "
        "hand; gaze cast soft to the hand.",
        "Her gaze softens with quiet focus as a composed micro-smile holds, the ivory weave "
        "pure and pristine.",
        "She holds the still poised ivory beat, eyes calm on the hand, the world pure white "
        "(silent here).",
    ),
    # F3 - ivory, arc, presses sternum, draws breath (NO bloom yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she presses her hand soft at "
        "the sternum and draws a slow breath, her left hand easing open, as the camera arcs a "
        "few degrees and the ivory cyclorama swings behind with parallax; gaze beginning to "
        "lift.",
        "The arc settles as her gaze lifts to lens with rising spark and a knowing micro-smile "
        "forms, the world still pure all-ivory.",
        "She holds the poised ivory beat, hand at the breath, eyes bright and architectural "
        "\u2014 the slow breath before the colour (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip ink bloom; first=ivory, last=colour-riot
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the all-ivory Look A "
        "still): she eases her hand off the sternum on the breath, already in motion \u2014 the "
        "world still pure all-ivory, NO colour yet, a gentle push-with easing in, the angle "
        "fixed for the whole clip.",
        "The bloom BEGINS here, mid-clip: on the breath a saturated colour-riot blooms through "
        "the ivory along one travelling wavefront, deep magenta, cobalt and emerald diffusing "
        "through the real fabric weave by true ink-in-water capillary spread exactly where the "
        "wave passes \u2014 painterly and continuous, never a snap, no garish glare; the sleek "
        "straight fall catching travelling colour, eyes widening in playful editorial awe "
        "(angle held, face cleanly lit, identity locked).",
        "The ink-wash completes its sweep and the look settles smoothly and fully into the bold "
        "colour-riot Look B of the Veo last-frame still (Frame 5's image) \u2014 magenta, "
        "cobalt and emerald set rich through the sculptural silhouette and backdrop, resolved "
        "and held through the final beat, no last-second pop; a bold alive spark landing in her "
        "eyes.",
    ),
    # F5 - colour-riot Look B reveal, cut to a NEW angle, adjust colour lapel
    (
        "Cut to a medium close on a new angle in the colour-flooded world: she is already in "
        "the saturated colour-riot look, reaching up to adjust the now colour-flooded lapel "
        "with an easy roll of the shoulder; gaze easing to lens.",
        "A bold confident smile eases to lens on a slow breath, the last colour-droplets "
        "settling with a rich glint, eyes shining direct.",
        "She holds the bold alive editorial look, the colour set sitting sharp, eyes bright and "
        "direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed bold gesture as the camera eases "
        "with her; gaze direct to lens.",
        "She delivers \u201cColor was always the point.\u201d to lens with a bold knowing smile "
        "and natural lip-sync, the colour-pop earring swinging a hair, eyes warm and direct.",
        "She holds the assured editorial look as the colour set settles, the smile easing into "
        "bold calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 all-ivory
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft at the sternum and settles her weight onto the back leg exactly as in Frame 1 as "
        "the camera settles to the opening framing.",
        "She eases her cool gaze back to lens on a slow breath with the composed calm "
        "micro-smile, the colour-riot resolving back toward the all-ivory opening to seed the "
        "loop.",
        "She lands precisely on the Frame 1 pose and gaze, pure and poised \u2014 a seamless "
        "loop seam.",
    ),
]


BEATSLM[9] = [
    # F1 - matte Look A establishing, alive lateral track, water-skin floor, hand at collarbone
    (
        "Cut to a medium-wide thigh-up tracking shot in the dark futurist studio on the black "
        "water-skin floor: the camera dollies laterally to settle on her as she steps her "
        "weight onto the back leg and rests her right hand soft at her collarbone, the dark "
        "wall and her mirror reflection sliding behind with real parallax; a composed cool "
        "quarter-smile holding.",
        "The track eases to rest as a strand of the high sleek pony shifts in the studio air "
        "and her cool gaze begins to lift, faint vapour drifting low, a composed architectural "
        "micro-smile settling.",
        "She holds, cool and sculptural in the matte graphite set, eyes direct, her mirror "
        "reflection breathing in the water-skin (silent here).",
    ),
    # F2 - matte, push-with the hand lifting toward cresting chrome, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting her hand soft toward the "
        "chrome cresting above and opening her fingers as if to receive it, as the camera "
        "pushes with her hand and tilts up; gaze rising toward the crest.",
        "The first liquid-chrome bead gathers above her by real surface tension, a mirror "
        "highlight cresting at its meniscus, as her eyes brighten with quiet anticipation.",
        "She holds the poised beat, gaze up on the gathering chrome, the matte set still clean "
        "and intact (silent here).",
    ),
    # F3 - matte, arc, raises hand to receive (chrome cresting, NO pour yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft to "
        "receive the chrome and draws a slow breath, her left hand easing open, as the camera "
        "arcs a few degrees and the dark wall swings behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising spark and a knowing micro-smile "
        "forms, the chrome cresting and tipping above by real fluid surface tension, the set "
        "still matte.",
        "She holds the poised matte beat, hand raised to the crest, eyes steady and bright "
        "\u2014 the instant before the pour (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip chrome pour; first=matte, last=chrome
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the matte-graphite Look "
        "A still): she holds her hand from receiving the chrome, already in motion \u2014 the "
        "set still matte, NO chrome yet, a gentle push-with easing in, the angle fixed for the "
        "whole clip.",
        "The pour BEGINS here, mid-clip: the liquid chrome pours down and wraps smoothly around "
        "her in one continuous travelling spiral, the metal flowing and setting over the matte "
        "bodice with believable fluid spread and inertia exactly where it passes \u2014 "
        "mirror-bright and continuous, mirrored true in the water-skin, never a snap, no garish "
        "glare; the high sleek pony catching travelling chrome, eyes luminous with cool awe "
        "(angle held, face cleanly lit, identity locked).",
        "The chrome completes its spiral and the look settles smoothly and fully into the "
        "chrome Look B of the Veo last-frame still (Frame 5's image) \u2014 a sculptural "
        "mirror-chrome sash-and-collar set over the matte set, resolved and held through the "
        "final beat, no last-second pop; a strong fluid resolve landing in her eyes.",
    ),
    # F5 - chrome Look B reveal, cut to a NEW angle, settle chrome sash
    (
        "Cut to a medium close on a new angle, mirror-light off the water-skin: she is already "
        "wrapped in the mirror-chrome sash-and-collar, reaching to settle it with an easy roll "
        "of the shoulder; gaze easing to lens.",
        "A strong confident smile eases to lens on a slow breath, the last chrome-droplets "
        "settling with a slow mirror glint, eyes shining direct.",
        "She holds the strong fluid architectural look, the chrome sitting sharp over the "
        "matte, eyes shining direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed strong gesture as the camera "
        "eases with her; gaze direct to lens.",
        "She delivers \u201cI flow. I don\u2019t break.\u201d to lens with a strong knowing "
        "smile and natural lip-sync, the chrome collar catching travelling light on its real "
        "planes, eyes direct.",
        "She holds the assured architectural look as the chrome set settles, the smile easing "
        "into strong calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 matte set
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft at her collarbone and settles her weight onto the back leg exactly as in Frame 1 "
        "as the camera settles to the opening framing.",
        "She eases her cool gaze back to lens on a slow breath with the composed calm "
        "micro-smile, the chrome wrap resolving back toward the matte graphite opening and the "
        "light bar re-settling cool, to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, cool and sculptural on the "
        "water-skin \u2014 a seamless loop seam.",
    ),
]


BEATSLM[10] = [
    # F1 - folded-paper Look A establishing, alive lateral track, hand near folded flower
    (
        "Cut to a medium-wide thigh-up tracking shot in the handmade paper-craft world: the "
        "camera dollies laterally to settle on her as she steps her weight onto the back leg "
        "and rests her right hand soft near a folded-paper flower at her shoulder, the "
        "folded-paper backdrop and paper props sliding behind with real parallax; a soft "
        "romantic quarter-smile holding.",
        "The track eases to rest as a curtain-fringe strand shifts in the soft air and her warm "
        "gaze begins to lift, fine paper-dust drifting in the key, a soft micro-smile settling.",
        "She holds, soft and crafted in the origami-pleated dress, eyes warm and direct, the "
        "folded flower trembling on its slim stem (silent here).",
    ),
    # F2 - paper, push-with, cradling the folded flower, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already cradling the folded-paper flower "
        "soft and curling her fingers gently around the stem, as the camera pushes with her "
        "hand; gaze cast soft to it.",
        "The flower's first crease eases open in her hand by real paper-fold mechanics as her "
        "gaze softens with tender focus and a soft micro-smile kindles.",
        "She holds the still tender beat, eyes warm on the folded flower, the paper world still "
        "crisply folded (silent here).",
    ),
    # F3 - paper, arc, opens hand as flower unfolds (NO burst yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she opens her hand soft as "
        "the folded flower unfolds and draws a slow breath, her left hand easing open, as the "
        "camera arcs a few degrees and the paper backdrop swings behind with parallax; gaze "
        "lifting.",
        "The arc settles as her gaze lifts to lens with rising warmth and a knowing soft smile "
        "forms, the world still folded paper, just the one flower unfolding in her hand.",
        "She holds the poised paper beat, the flower opening, eyes bright and tender \u2014 the "
        "breath before the burst (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip petal burst; first=paper, last=petal
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the folded-paper Look A "
        "still): she eases her hand open as the flower unfolds, already in motion \u2014 the "
        "world still folded paper, NO burst yet, a gentle push-with easing in, the angle fixed "
        "for the whole clip.",
        "The burst BEGINS here, mid-clip: the folded paper unfolds and bursts into soft real "
        "petals that wrap smoothly around her in one continuous travelling arc, warm rose and "
        "blush petals fluttering across the pleats by believable real crease-to-petal flutter "
        "exactly where the arc passes \u2014 fine petal-dust drifting like real flecks, gradual "
        "and tender, never a snap, no cheap sparkles; the tousled shag catching travelling "
        "petals, eyes warming in soft awe (angle held, face cleanly lit, identity locked).",
        "The petal-burst completes its arc and the look settles smoothly and fully into the "
        "petal Look B of the Veo last-frame still (Frame 5's image) \u2014 soft real-petal "
        "texture and warm petal-colour washed through the pleats, resolved and held through the "
        "final beat, no last-second pop; a soft radiant warmth landing in her eyes.",
    ),
    # F5 - petal Look B reveal, cut to a NEW angle, settle a petal at the shoulder
    (
        "Cut to a medium close on a new angle amid the bloomed petals: she is already in the "
        "petal-bloomed look, reaching to settle a soft petal at her shoulder with an easy roll "
        "of the shoulder; gaze easing to lens.",
        "A soft radiant smile eases to lens on a slow breath, the last petals settling with a "
        "slow soft drift, eyes soft and luminous.",
        "She holds the soft alive tender look, the petal dress sitting soft, eyes shining "
        "direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed tender gesture as the camera "
        "eases with her; gaze warm to lens.",
        "She delivers \u201cUnfold. Then bloom.\u201d to lens with a soft radiant smile and "
        "natural lip-sync, the real-petal hairpiece trembling a hair at her temple, eyes warm "
        "and direct.",
        "She holds the alive tender look as the petal dress settles, the smile easing into soft "
        "warmth.",
    ),
    # F7 - loop close, cut back to match Frame 1 folded-paper world
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft near the folded-paper flower and settles her weight onto the back leg exactly as "
        "in Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed calm "
        "micro-smile, the petal wrap resolving back toward the folded-paper opening and the "
        "flower re-settling on its stem, to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, soft and crafted in the gentle hush "
        "\u2014 a seamless loop seam.",
    ),
]


def build_block(beats):
    return (
        BREAKDOWN_HEADER + "\n"
        f"- [00:00\u201300:02] {beats[0]}\n"
        f"- [00:02\u201300:04] {beats[1]}\n"
        f"- [00:04\u201300:06] {beats[2]}\n"
    )


def apply_concept(text, concept_no):
    frames = BEATSLM[concept_no]
    start_m = re.search(rf"#+ CONCEPT 0*{concept_no} \u2014", text)
    start = start_m.start()
    nxt = re.search(rf"#+ CONCEPT 0*{concept_no + 1} \u2014", text)
    end = nxt.start() if nxt else len(text)
    region = text[start:end]

    state = {"i": 0}

    # Strip the old cross-frame camera-anchor / interpolation parentheticals
    # (the new model uses cuts, so frames no longer share a locked distance).
    region = re.sub(
        r" \(Transform-anchor distance \u2014 matches Frames [0-9]+ and [0-9]+\.\)",
        "", region,
    )
    region = re.sub(r" \(Camera distance [^)]*\.\)", "", region)

    def repl(_m):
        beats = frames[state["i"]]
        state["i"] += 1
        return build_block(beats)

    # Match the existing SHOT BREAKDOWN header + its three "- [..]" beat lines.
    region, n_bd = re.subn(
        r"SHOT BREAKDOWN \(timed[^\n]*\):\n(?:- \[[^\n]*\n){3}", repl, region
    )

    nf = len(frames)
    assert n_bd == nf, f"concept {concept_no}: {n_bd} breakdown blocks vs {nf} frames"
    print(f"concept {concept_no}: rebuilt {n_bd} SHOT BREAKDOWN blocks into the L+M model")
    return text[:start] + region + text[end:]


def main():
    path = sys.argv[1]
    concept_no = int(sys.argv[2])
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    text = apply_concept(text, concept_no)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()

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


BEATSLM[11] = [
    # F1 - morning-loungewear Look A establishing, alive lateral track, coffee mug
    (
        "Cut to a medium-wide thigh-up tracking shot in the soft new-city morning: the camera "
        "dollies laterally to settle on her as she steps her weight onto the back leg and "
        "cradles the warm coffee mug soft at her chest, gentle steam curling, the bright window "
        "and room sliding behind with real parallax; a warm sleepy quarter-smile holding.",
        "The track eases to rest as a face-framing piece shifts in the morning air and she "
        "lifts her warm sleepy gaze toward lens, a soft easy quarter-smile settling.",
        "She holds, fresh and unhurried in the cozy loungewear, the half-up claw-clip easy, "
        "eyes soft and warm (silent here).",
    ),
    # F2 - loungewear, push-with reaching toward the vanity, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already reaching her right hand soft "
        "toward the vanity mirror and gently opening her fingers as if to begin getting ready, "
        "as the camera pushes with her hand; gaze toward the vanity.",
        "Her gaze brightens with quiet intent as a soft micro-smile holds, the loungewear soft "
        "and lived-in.",
        "She holds the easy beat, eyes bright with morning intent, the room calm and soft "
        "(silent here).",
    ),
    # F3 - loungewear, arc, raises hand to begin (NO wrap yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft to "
        "begin and draws a slow breath, her left hand easing open, as the camera arcs a few "
        "degrees and the room swings behind with parallax; gaze beginning to lift.",
        "The arc settles as her gaze lifts to lens with rising spark and a knowing soft smile "
        "forms, still in the morning loungewear.",
        "She holds the poised loungewear beat, hand raised to begin, eyes bright and ready "
        "\u2014 the breath before the getting-ready (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip speed-wrap; first=loungewear, last=day-look
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the morning-loungewear "
        "Look A still): she eases her hand from beginning, already in motion \u2014 still the "
        "cozy loungewear, NO wrap yet, a gentle push-with easing in, the angle fixed for the "
        "whole clip.",
        "The wrap BEGINS here, mid-clip: a single travelling speed-ramp wraps smoothly over her "
        "in one continuous front, the cozy knit resolving into the clean tailored blazer over a "
        "modest top and tapered trousers exactly where it passes \u2014 cloth resolving with "
        "believable spread and inertia, the room brightening morning-to-day, gradual and "
        "smooth, never a snap; the half-up hair catching travelling light, eyes brightening in "
        "ready delight (angle held, face cleanly lit, identity locked).",
        "The speed-ramp completes its pass and the look settles smoothly and fully into the "
        "put-together day-look Look B of the Veo last-frame still (Frame 5's image) \u2014 "
        "tailored blazer, modest top, tapered trousers, clean sneakers and a crossbody with "
        "small hoops, resolved and held through the final beat, no last-second pop; a bright "
        "confident spark landing in her eyes.",
    ),
    # F5 - day-look Look B reveal, cut to a NEW angle, settle blazer lapel
    (
        "Cut to a medium close on a new angle in the brightened day-lit room: she is already in "
        "the put-together day look, reaching up to settle the blazer lapel with an easy roll of "
        "the shoulder; gaze easing to lens.",
        "A bright confident smile eases to lens on a slow breath, the last warm dust-motes "
        "settling, eyes bright and direct.",
        "She holds the alive ready look, the blazer sitting crisp, eyes bright and direct "
        "(silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed bright gesture as the camera "
        "eases with her; gaze direct to lens.",
        "She delivers \u201cNew city. Let\u2019s begin.\u201d to lens with a bright knowing "
        "smile and natural lip-sync, the crossbody and hoops settling, eyes warm and direct.",
        "She holds the alive ready look as the day look settles, the smile easing into bright "
        "calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 loungewear + coffee mug
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to cradle "
        "the warm coffee mug at her chest and settles her weight onto the back leg exactly as "
        "in Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed calm sleepy "
        "micro-smile, the bright day look resolving back toward the soft morning loungewear "
        "opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, fresh and unhurried \u2014 a seamless "
        "loop seam.",
    ),
]


BEATSLM[12] = [
    # F1 - getting-ready-set Look A establishing (GRWM contained), marigold garland
    (
        "Cut to a medium-wide thigh-up tracking shot in the warm pre-sangeet room: the camera "
        "dollies laterally to settle on her as she settles her weight onto the back leg and "
        "rests her right hand soft near the marigold garland at her shoulder, the warm room "
        "sliding behind with real parallax; a serene quarter-smile holding.",
        "The track eases to rest as a softly-laid baby-hair strand shifts in the evening air "
        "and she lifts her warm gaze to lens, a serene quarter-smile settling.",
        "She holds, warm and pre-glam in the simple cotton kurta, the braided low bun sleek, "
        "eyes soft and luminous (silent here).",
    ),
    # F2 - set, push-with + tilt-up, lift hand toward cresting lights, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter, the camera pushing with her hand and tilting up "
        "as she lifts it soft toward the cresting fairy lights and opens her fingers as if to "
        "receive them; gaze rising toward the warm glow.",
        "The first warm bulbs crest and twinkle above her as her eyes brighten with warm "
        "anticipation, a soft micro-smile holding.",
        "She holds the poised beat, gaze up on the gathering lights, the simple set still calm "
        "and intact (silent here).",
    ),
    # F3 - set, arc, raise to receive (lights cresting, NO wrap yet), cut
    (
        "Cut to a medium chest-up on a fresh three-quarter angle, the camera arcing a few "
        "degrees as she raises her hand soft to receive the lights and draws a slow breath, "
        "her left hand easing open; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising spark and a knowing soft smile "
        "forms, the fairy lights cresting above, the simple set still intact.",
        "She holds the poised getting-ready beat, hand raised to the crest, eyes warm and "
        "bright \u2014 the breath before the bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, mid-clip fairy-light wrap; first=set, last=festive
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the getting-ready Look A "
        "still): she holds her hand from receiving the lights, already in motion \u2014 still "
        "the simple cotton kurta, NO wrap yet, a gentle push-with easing in, the angle fixed "
        "for the whole clip.",
        "The wrap BEGINS here, mid-clip: warm fairy lights bloom down and wrap smoothly around "
        "her in one continuous travelling spiral, warm bulbs racing around her and the venue "
        "blooming with real string-light glow exactly where the spiral passes \u2014 the simple "
        "set resolving into the embellished festive look, gradual and warm, never a snap, no "
        "garish glare; the braided bun catching travelling warm-light, eyes warming in radiant "
        "awe (angle held, face cleanly lit, identity locked).",
        "The spiral completes and the look settles smoothly and fully into the festive Look B "
        "of the Veo last-frame still (Frame 5's image) \u2014 the richly embroidered Indo-"
        "modern lehenga-and-blouse with a draped dupatta under warm string lights, resolved "
        "and held through the final beat, no last-second pop; a warm radiant joy landing in "
        "her eyes.",
    ),
    # F5 - festive Look B reveal, cut to a NEW angle, settle dupatta
    (
        "Cut to a medium close on a new angle amid the warm string lights: she is already in "
        "the embellished festive look, reaching to settle the draped dupatta with an easy roll "
        "of the shoulder; gaze easing to lens.",
        "A warm radiant smile eases to lens on a slow breath, the last warm bokeh orbs settling "
        "around her, eyes warm and shining.",
        "She holds the alive festive look, the embroidery glinting soft, eyes warm and direct "
        "(silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed festive gesture as the camera "
        "eases with her; gaze warm to lens.",
        "She delivers \u201cTonight, we light it up.\u201d to lens with a warm radiant smile "
        "and natural lip-sync, the dupatta and jhumkas settling, eyes warm and direct.",
        "She holds the alive festive look as the festive set settles, the smile easing into "
        "warm radiance.",
    ),
    # F7 - loop close, cut back to match Frame 1 set + garland
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft near the marigold garland and settles her weight onto the back leg exactly as in "
        "Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed calm warm "
        "micro-smile, the festive look resolving back toward the simple pre-glam opening to "
        "seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, warm and serene \u2014 a seamless "
        "loop seam.",
    ),
]


BEATSLM[13] = [
    # F1 - loungewear Look A establishing (GRWM contained), alive lateral track, glass of water
    (
        "Cut to a medium-wide thigh-up tracking shot in the cool pre-dawn apartment: the camera "
        "dollies laterally to settle on her as she settles her weight onto the back leg and "
        "cradles the glass of water soft at her chest, the wide pre-dawn window and rolled yoga "
        "mat sliding behind with real parallax; a calm sleepy quarter-smile holding.",
        "The track eases to rest as a loose tendril shifts in the still pre-dawn air and she "
        "lifts her calm just-woken gaze to lens on a slow inhale, a quiet quarter-smile "
        "settling.",
        "She holds, fresh and unhurried in the soft sleep-loungewear, the messy top knot easy, "
        "eyes calm and soft in the blue pre-dawn light (silent here).",
    ),
    # F2 - loungewear, push-with reaching toward the brightening window, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already reaching her right hand soft toward "
        "the brightening window and gently opening her fingers as if to greet the sunrise, as "
        "the camera pushes with her hand; gaze toward the warming sill.",
        "The first warm light edges the sill as her gaze wakes with quiet intent and a soft "
        "micro-smile holds.",
        "She holds the still beat, eyes waking and calm, the room hushed and blue around her "
        "(silent here).",
    ),
    # F3 - loungewear clean (NO sweep yet), slow arc to a fresh angle, raise hand to greet sunrise
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft to "
        "greet the sunrise and draws a slow breath, her left hand easing open, as the camera "
        "arcs a few degrees and the room swings behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising spark and a knowing soft smile "
        "forms, the sunrise cresting at the window, still in the soft morning loungewear.",
        "She holds the poised loungewear beat, hand raised to greet the light, eyes bright and "
        "ready \u2014 the breath before the sunrise sweep (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip sunrise sweep; first=loungewear, last=active
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the sleep-loungewear "
        "Look A still): she eases her hand from greeting the sunrise, already in motion \u2014 "
        "still the soft sleep-loungewear, NO sweep yet, a gentle push-with easing in, the angle "
        "fixed for the whole clip.",
        "The sweep BEGINS here, mid-clip: a single travelling sunrise-light sweep rolls smoothly "
        "across the room and over her in one continuous front, the soft tee and lounge shorts "
        "resolving into the modest active set \u2014 full-coverage leggings, a loose long-line "
        "sports top and a light zip layer \u2014 exactly where the sweep passes, the room "
        "brightening pre-dawn to sunrise along the same front, cloth resolving with believable "
        "spread and inertia, gradual and smooth, never a snap; the messy top knot catching "
        "travelling warm-light, eyes brightening in fresh awe (angle held, face cleanly lit, "
        "identity locked).",
        "The sweep completes its roll and the look settles smoothly and fully into the active "
        "morning Look B of the Veo last-frame still (Frame 5's image) \u2014 the modest active "
        "set with clean training shoes, a sleek smartwatch and a water bottle under warm "
        "sunrise light, resolved and held through the final beat, no last-second pop; a bright "
        "grounded resolve landing in her eyes.",
    ),
    # F5 - active Look B reveal, cut to a NEW angle, bring up the water bottle
    (
        "Cut to a medium close on a new angle in the warm sunrise-lit room: she is already in "
        "the clean active morning look, bringing the water bottle up with an easy roll of the "
        "shoulder; gaze easing to lens.",
        "A bright calm smile eases to lens on a slow breath, the last warm dust-motes settling "
        "in the sunrise glow, eyes bright and direct.",
        "She holds the alive ready look, the active set sitting clean, eyes bright and grounded "
        "(silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a relaxed grounded gesture as the camera "
        "eases with her; gaze direct to lens.",
        "She delivers \u201c5 AM. This is my hour.\u201d to lens with a bright calm smile and "
        "natural lip-sync, the light zip layer and smartwatch settling, eyes warm and direct.",
        "She holds the alive ready look as the active set settles, the smile easing into "
        "grounded calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 loungewear + glass of water
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to cradle "
        "the glass of water at her chest and settles her weight onto the back leg exactly as in "
        "Frame 1 as the camera settles to the opening framing.",
        "She eases her calm gaze back to lens on a slow breath with the composed sleepy "
        "micro-smile, the warm sunrise active look resolving back toward the soft pre-dawn "
        "loungewear opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, fresh and unhurried in the pre-dawn "
        "hush \u2014 a seamless loop seam.",
    ),
]


BEATSLM[14] = [
    # F1 - spa Look A establishing (beauty-still contained), alive lateral track, serum at collarbone
    (
        "Cut to a medium-wide thigh-up tracking shot on the soft minimalist beauty set: the "
        "camera dollies laterally to settle on her as she settles her weight onto the back leg "
        "and holds the glass serum bottle soft at her collarbone, the soft white-to-pastel "
        "seamless backdrop and vanity sliding behind with real parallax; a serene soft "
        "quarter-smile holding.",
        "The track eases to rest as a glossy strand of the pin-straight micro-fringe shifts in "
        "the soft studio air and she eases her calm gaze to lens, fine dew-droplets drifting, a "
        "soft luminous quarter-smile settling.",
        "She holds, soft and dewy in the spa wrap, the pin-straight micro-fringe glossy, eyes "
        "soft and luminous in the clean beauty light (silent here).",
    ),
    # F2 - spa, push-with lifting serum to cheekbone, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting the serum soft toward her "
        "cheekbone as if to apply it, fingertips gently open, as the camera pushes with her "
        "hand; gaze cast soft to the serum.",
        "A clean dewy sheen gathers along her cheekbone as her gaze softens with quiet focus "
        "and a soft luminous micro-smile kindles.",
        "She holds the serum poised at her cheekbone, eyes soft and dewy, the spa look soft and "
        "intact (silent here).",
    ),
    # F3 - spa clean (NO bloom yet), slow arc to a fresh angle, ease hand from cheek as glow crests
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases her hand from her "
        "cheek as the dewy glow crests and draws a slow breath, her left hand easing open, as "
        "the camera arcs a few degrees and the backdrop swings behind with parallax; gaze "
        "lifting.",
        "The arc settles as her gaze lifts to lens with rising soft spark and a knowing "
        "luminous smile forms, the dewy glow cresting on her skin, still in the soft spa look.",
        "She holds the poised spa beat, the glow cresting at her cheek, eyes soft and bright "
        "\u2014 the breath before the glass bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip glass-glow wave; first=spa, last=glass-skin
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the soft-spa Look A "
        "still): she eases her hand down from her cheek, already in motion \u2014 still the soft "
        "spa wrap and dewy bare skin, NO bloom yet, a gentle push-with easing in, the angle "
        "fixed for the whole clip.",
        "The glass bloom BEGINS here, mid-clip: a single travelling dewy glass-glow wave rolls "
        "smoothly over her skin in one continuous front, the soft spa wrap resolving into the "
        "sleek ivory editorial top and the bare skin blooming to a luminous lit-from-within "
        "glass-skin finish exactly where the wave passes \u2014 real skin-and-light physics, "
        "true pores and fine vellus texture kept beneath the glow (never plastic, never "
        "over-smoothed), gradual and soft, never a snap; the pin-straight micro-fringe catching "
        "travelling clean light, eyes softening in luminous wonder (angle held, face cleanly "
        "lit, identity locked).",
        "The glass-glow wave completes its roll and the look settles smoothly and fully into "
        "the luminous glass-skin Look B of the Veo last-frame still (Frame 5's image) \u2014 "
        "the sleek ivory editorial top with a clean lit-from-within glow under crisp beauty "
        "light, resolved and held through the final beat, no last-second pop; a soft luminous "
        "calm landing in her eyes.",
    ),
    # F5 - glass-skin Look B reveal, cut to a NEW angle, hand drifts to jaw to show the finish
    (
        "Cut to a medium close on a new angle in the crisp luminous beauty light: she is "
        "already in the luminous glass-skin finish, drifting her right hand soft to her jaw to "
        "show the glow with an easy roll of the shoulder; gaze easing to lens.",
        "A soft luminous smile eases to lens on a slow breath, the last dew-droplets settling "
        "with a clean glint, eyes soft and shining.",
        "She holds the clean luminous look, the glass-skin glow even and real, eyes soft and "
        "direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a soft clean gesture as the camera eases "
        "with her; gaze direct to lens.",
        "She delivers \u201cGlass skin. No filter.\u201d to lens with a soft luminous smile and "
        "natural lip-sync, the fine ear studs catching a clean glint, eyes soft and direct.",
        "She holds the clean luminous look as the editorial top settles, the smile easing into "
        "soft calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 spa + serum bottle
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to hold "
        "the glass serum bottle soft at her collarbone and settles her weight onto the back leg "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her calm gaze back to lens on a slow breath with the composed luminous "
        "micro-smile, the crisp editorial light resolving back toward the soft dewy spa opening "
        "to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, soft and dewy in the clean beauty "
        "light \u2014 a seamless loop seam.",
    ),
]


BEATSLM[15] = [
    # F1 - clean base Look A establishing, alive lateral track, hand near collarbone
    (
        "Cut to a medium-wide thigh-up tracking shot in the bold editorial studio: the camera "
        "dollies laterally to settle on her as she settles her weight onto the back leg and "
        "rests her right hand soft near her collarbone, the graphic dark seamless backdrop and "
        "liquid-ink motif sliding behind with real parallax; a sharp composed quarter-smile "
        "holding.",
        "The track eases to rest as a laid edge of the sleek space buns catches the hard key "
        "and she eases her bold gaze to lens, a sharp composed quarter-smile settling.",
        "She holds, stark and poised in the clean charcoal base, the high space buns glossy, "
        "eyes direct and graphic in the hard key (silent here).",
    ),
    # F2 - clean base, push-with lifting hand toward cresting ink-stroke, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting her right hand soft toward "
        "the cresting ink-stroke as if to meet it, fingers gently open, as the camera pushes "
        "with her hand; gaze toward the ink edge.",
        "The ink-stroke crests at the frame edge as her gaze sharpens with quiet focus and a "
        "knowing micro-smile kindles.",
        "She holds the hand poised toward the ink, eyes bright and sharp, the clean base crisp "
        "and intact (silent here).",
    ),
    # F3 - clean base clean (NO draw yet), slow arc to a fresh angle, raise hand to meet ink
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft to "
        "meet the ink and draws a slow breath, her left hand easing open, as the camera arcs a "
        "few degrees and the backdrop swings behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising sharp spark and a knowing "
        "micro-smile forms, the ink-stroke cresting at the edge, still in the clean charcoal "
        "base.",
        "She holds the poised base beat, hand raised to meet the ink, eyes bright and graphic "
        "\u2014 the breath before the ink draw (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip ink draw; first=clean base, last=winged-liner
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the clean-base Look A "
        "still): she eases her hand from meeting the ink, already in motion \u2014 still the "
        "clean charcoal base, NO draw yet, a gentle push-with easing in, the angle fixed for "
        "the whole clip.",
        "The ink draw BEGINS here, mid-clip: a single travelling ink-stroke draws smoothly "
        "across the frame in one continuous wet line, drawing her crisp winged liner and "
        "resolving the clean charcoal base into the architectural sculptural-shoulder editorial "
        "top in deep black exactly where the stroke passes \u2014 real liquid-ink flow and "
        "cloth resolving with believable spread and inertia, gradual and sharp but smooth, "
        "never a snap, no garish glare; the high space buns catching travelling graphic light, "
        "eyes sharpening in bold focus (angle held, face cleanly lit, identity locked).",
        "The ink-stroke completes its draw and the look settles smoothly and fully into the "
        "bold winged-liner Look B of the Veo last-frame still (Frame 5's image) \u2014 the "
        "architectural deep-black top with crisp graphic winged liner under the hard editorial "
        "key, resolved and held through the final beat, no last-second pop; a sharp graphic "
        "resolve landing in her eyes.",
    ),
    # F5 - winged-liner Look B reveal, cut to a NEW angle, settle the sculptural shoulder
    (
        "Cut to a medium close on a new angle in the sharpened graphic light: she is already in "
        "the bold winged-liner editorial look, drifting her right hand to settle the sculptural "
        "shoulder with an easy roll of the shoulder; gaze easing to lens.",
        "A sharp confident smile eases to lens on a slow breath, the last ink-droplets settling "
        "with a graphic glint, eyes sharp and direct.",
        "She holds the bold graphic look, the architectural top sitting sharp, eyes bold and "
        "direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and opens her right hand in a sharp clean gesture as the camera eases "
        "with her; gaze direct to lens.",
        "She delivers \u201cI draw my own line.\u201d to lens with a sharp knowing smile and "
        "natural lip-sync, the space buns crisp, eyes bold and direct.",
        "She holds the bold graphic look as the editorial top settles, the smile easing into "
        "sharp calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 clean base
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft near her collarbone and settles her weight onto the back leg exactly as in Frame "
        "1 as the camera settles to the opening framing.",
        "She eases her bold gaze back to lens on a slow breath with the composed sharp "
        "quarter-smile, the bold graphic look resolving back toward the clean charcoal-base "
        "opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, stark and poised in the hard key "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[16] = [
    # F1 - soft day Look A establishing (seated café, contained), alive lateral track, coffee cup
    (
        "Cut to a medium-wide waist-up tracking shot at the rainy café window: the camera "
        "dollies gently laterally to settle on her seated at the worn wooden table as she "
        "cradles the warm coffee cup, gentle steam curling, the rain-streamed glass and amber "
        "interior sliding behind with real parallax; a warm soft quarter-smile holding.",
        "The track eases to rest as a tiny face-framing braid shifts in the café warmth and she "
        "eases her warm gaze to lens, rain beading on the glass behind, a soft dreamy "
        "quarter-smile settling.",
        "She holds, warm and easy in the soft oatmeal knit, the half-up boho braids gently "
        "tousled, eyes soft in the amber light (silent here).",
    ),
    # F2 - day look, push-with lifting hand from cup toward the rain-streamed glass, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting her right hand soft from "
        "the cup toward the rain-streamed glass as if to touch a bead, fingers gently open, as "
        "the camera pushes with her hand; gaze toward the rain.",
        "A rain-bead trembles under her fingertip as her gaze softens with quiet warmth and a "
        "dreamy micro-smile kindles.",
        "She holds the hand poised at the glass, eyes soft and warm, the soft day look easy and "
        "intact (silent here).",
    ),
    # F3 - day look clean (NO ripple yet), slow arc to a fresh angle, raise hand toward glass
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft "
        "toward the glass and draws a slow breath, her left hand easing open on the table, as "
        "the camera arcs a few degrees and the café swings behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising soft warmth and a knowing dreamy "
        "smile forms, the rain-ripple cresting on the glass, still in the soft day look.",
        "She holds the poised café beat, hand raised toward the glass, eyes soft and dreamy "
        "\u2014 the breath before the rain-ripple (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip rain-ripple; first=day look, last=cozy cardigan
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the soft-day Look A "
        "still): she eases her hand down from the glass, already in motion \u2014 still the soft "
        "oatmeal knit, NO ripple yet, a gentle push-with easing in, the angle fixed for the "
        "whole clip.",
        "The ripple BEGINS here, mid-clip: a single travelling rain-ripple rolls smoothly "
        "across the rain-streamed window and the frame in one continuous warm front, the light "
        "knit deepening into the chunky caramel cardigan with a snug modest scarf and the room "
        "warming to amber exactly where the ripple passes \u2014 cloth resolving with believable "
        "weight and inertia, real rain-on-glass refraction, gradual and warm, never a snap, no "
        "garish glare; the boho braids catching travelling amber light, eyes warming in dreamy "
        "wonder (angle held, face cleanly lit, identity locked).",
        "The ripple completes its roll and the look settles smoothly and fully into the cozy "
        "cardigan Look B of the Veo last-frame still (Frame 5's image) \u2014 the warm chunky "
        "caramel cardigan and snug scarf over the knit in a snug amber glow, resolved and held "
        "through the final beat, no last-second pop; a warm dreamy calm landing in her eyes.",
    ),
    # F5 - cozy Look B reveal, cut to a NEW angle, cradle the warm cup again
    (
        "Cut to a medium close on a new angle in the snug amber glow: she is already in the "
        "cozy cardigan-and-scarf look, drifting her right hand to cradle the warm cup again with "
        "an easy roll of the shoulder; gaze easing to lens.",
        "A warm dreamy smile eases to lens on a slow breath, the last rain-bokeh softening "
        "behind, eyes soft and warm.",
        "She holds the cozy dreamy look, the cardigan settling snug, eyes warm and direct "
        "(silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the lean
    (
        "Cut to a medium chest-up on a fresh angle: she leans an easy few degrees toward lens "
        "and drifts her right hand open soft from the cup in a warm easy gesture as the camera "
        "eases with her; gaze warm to lens.",
        "She delivers \u201cSome days are made for rain.\u201d to lens with a warm dreamy smile "
        "and natural lip-sync, the steam curling soft, eyes warm and direct.",
        "She holds the cozy dreamy look as the cardigan settles, the smile easing into warm "
        "calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 seated café + coffee cup
    (
        "Cut to a medium-wide waist-up matched to Frame 1: she returns her right hand to cradle "
        "the warm coffee cup seated at the table exactly as in Frame 1 as the camera settles to "
        "the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed dreamy "
        "micro-smile, the snug amber cozy look resolving back toward the soft day-look opening "
        "to seed the loop.",
        "She lands precisely on the Frame 1 seated pose and gaze, warm and easy by the rain "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[17] = [
    # F1 - breezy day Look A establishing, alive lateral track, hand on open car door
    (
        "Cut to a medium-wide thigh-up tracking shot on the coastal cliff road at golden hour: "
        "the camera dollies laterally to settle on her as she rests her right hand soft on the "
        "open car door and eases a wind-blown strand from her cheek, the open ocean sky and a "
        "vintage convertible sliding behind with real parallax; a warm easy quarter-smile "
        "holding.",
        "The track eases to rest as the beach waves lift in the sea-breeze and she eases her "
        "warm gaze to lens, low gold light raking the road, a soft easy quarter-smile settling.",
        "She holds, breezy and easy in the soft white shirt, the wind-blown waves loose, eyes "
        "warm in the afternoon light (silent here).",
    ),
    # F2 - day look, push-with lifting hand toward cresting wind-and-light wave, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting her right hand soft toward "
        "the cresting wind-and-light wave as if to feel the breeze, fingers gently open, as the "
        "camera pushes with her hand; gaze toward the open sky.",
        "The sea-breeze haze gathers warm at her fingertips as her gaze warms with quiet wonder "
        "and an easy micro-smile kindles.",
        "She holds the hand poised to the breeze, eyes warm and open, the breezy day look easy "
        "and intact (silent here).",
    ),
    # F3 - day look clean (NO sweep yet), slow arc to a fresh angle, raise hand toward breeze
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft "
        "toward the breeze and draws a slow breath, her left hand easing open on the car door, "
        "as the camera arcs a few degrees and the coast swings behind with parallax; gaze "
        "lifting.",
        "The arc settles as her gaze lifts to lens with rising warm wonder and a knowing easy "
        "smile forms, the wind-and-light wave cresting on the sky, still in the breezy day look.",
        "She holds the poised coastal beat, hand raised to the breeze, eyes warm and open "
        "\u2014 the breath before the wind-and-light wave (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip wind-and-light wave; first=breezy day, last=golden coastal
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the breezy-day Look A "
        "still): she eases her hand down from the breeze, already in motion \u2014 still the "
        "soft white shirt, NO wave yet, a gentle push-with easing in, the angle fixed for the "
        "whole clip.",
        "The wave BEGINS here, mid-clip: a single travelling wind-and-light wave sweeps "
        "smoothly across the frame in one continuous golden front, the breezy shirt flowing into "
        "the soft silk scarf and light caramel jacket and the light warming to deep gold "
        "exactly where the wave passes \u2014 silk and cloth flowing with believable wind weight "
        "and inertia, real golden-hour light spread, gradual and warm, never a snap, no garish "
        "glare; the beach waves lifting in travelling gold light, eyes warming in dreamy wonder "
        "(angle held, face cleanly lit, identity locked).",
        "The wave completes its sweep and the look settles smoothly and fully into the "
        "golden-coastal Look B of the Veo last-frame still (Frame 5's image) \u2014 the soft "
        "flowing silk scarf and light caramel jacket over the shirt in deep golden light, "
        "resolved and held through the final beat, no last-second pop; a warm dreamy calm "
        "landing in her eyes.",
    ),
    # F5 - golden coastal Look B reveal, cut to a NEW angle, settle the silk scarf
    (
        "Cut to a medium close on a new angle in the deep golden light: she is already in the "
        "golden-coastal look, drifting her right hand to settle the soft silk scarf with an "
        "easy roll of the shoulder; gaze easing to lens.",
        "A warm dreamy smile eases to lens on a slow breath, the last sea-breeze haze drifting "
        "gold, eyes soft and warm.",
        "She holds the golden dreamy look, the silk scarf flowing soft, eyes warm and direct "
        "(silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and drifts her right hand open soft in a warm easy gesture as the "
        "camera eases with her; gaze warm to lens.",
        "She delivers \u201cSome roads feel like home.\u201d to lens with a warm dreamy smile "
        "and natural lip-sync, the silk scarf lifting soft in the breeze, eyes warm and direct.",
        "She holds the golden dreamy look as the scarf settles, the smile easing into warm "
        "calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 hand on car door
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft on the open car door and settles her weight onto the back leg exactly as in Frame "
        "1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed easy "
        "quarter-smile, the deep golden look resolving back toward the breezy afternoon opening "
        "to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, breezy and easy on the open road "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[18] = [
    # F1 - soft day Look A establishing, alive lateral track, holding open book
    (
        "Cut to a medium-wide thigh-up tracking shot in the warm indie bookstore: the camera "
        "dollies laterally to settle on her as she settles her weight onto the back leg and "
        "holds an open book soft, her left hand on a shelf-edge, the tall worn shelves and brass "
        "lamps sliding behind with real parallax; a warm quiet quarter-smile holding.",
        "The track eases to rest as a laid edge of the ribboned low ponytail catches the warm "
        "lamp and she eases her warm gaze to lens, soft dust-motes drifting in the window shaft, "
        "a soft quiet quarter-smile settling.",
        "She holds, soft and quiet in the cream blouse, the ribboned ponytail tidy, eyes warm in "
        "the amber reading light (silent here).",
    ),
    # F2 - day look, push-with lifting hand from book toward cresting pages, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting her right hand soft from "
        "the book toward the cresting pages as if to feel them, fingers gently open, as the "
        "camera pushes with her hand; gaze toward the pages.",
        "A page-edge trembles at her fingertip as her gaze warms with quiet wonder and a soft "
        "micro-smile kindles.",
        "She holds the hand poised toward the pages, eyes warm and soft, the soft day look quiet "
        "and intact (silent here).",
    ),
    # F3 - day look clean (NO sweep yet), slow arc to a fresh angle, raise hand toward pages
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft "
        "toward the pages and draws a slow breath, her left hand easing open on the shelf, as "
        "the camera arcs a few degrees and the shelves swing behind with parallax; gaze "
        "lifting.",
        "The arc settles as her gaze lifts to lens with rising warm wonder and a knowing soft "
        "smile forms, the page-flutter cresting in frame, still in the soft day look.",
        "She holds the poised bookshop beat, hand raised toward the pages, eyes warm and soft "
        "\u2014 the breath before the page-flutter (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip page-flutter; first=soft day, last=refined warm
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the soft-day Look A "
        "still): she eases her hand down from the pages, already in motion \u2014 still the cream "
        "blouse, NO flutter yet, a gentle push-with easing in, the angle fixed for the whole "
        "clip.",
        "The page-flutter BEGINS here, mid-clip: a single travelling page-flutter sweeps "
        "smoothly across the frame in one continuous warm front, real book pages fluttering up "
        "by believable paper weight and air-drift, the soft cream blouse deepening into the "
        "tailored caramel blazer over a soft knit vest and the room warming to a snug reading "
        "glow exactly where the flutter passes \u2014 cloth resolving with real spread and "
        "inertia, gradual and warm, never a snap, no garish glare; the ribboned ponytail "
        "catching travelling amber light, eyes warming in refined wonder (angle held, face "
        "cleanly lit, identity locked).",
        "The flutter completes its sweep and the look settles smoothly and fully into the "
        "refined-warm Look B of the Veo last-frame still (Frame 5's image) \u2014 the tailored "
        "caramel blazer over the knit vest and blouse in a snug amber reading glow, resolved and "
        "held through the final beat, no last-second pop; a warm refined calm landing in her "
        "eyes.",
    ),
    # F5 - refined Look B reveal, cut to a NEW angle, settle the blazer lapel
    (
        "Cut to a medium close on a new angle in the snug amber reading glow: she is already in "
        "the refined warm look, drifting her right hand to settle the blazer lapel with an easy "
        "roll of the shoulder; gaze easing to lens.",
        "A warm refined smile eases to lens on a slow breath, the last dust-motes settling in "
        "the lamp-glow, eyes soft and warm.",
        "She holds the refined warm look, the blazer sitting clean, eyes warm and direct "
        "(silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and drifts her right hand open soft in a warm easy gesture as the "
        "camera eases with her; gaze warm to lens.",
        "She delivers \u201cLost in the pages, found myself.\u201d to lens with a warm refined "
        "smile and natural lip-sync, the reading glasses catching a soft glint, eyes warm and "
        "direct.",
        "She holds the refined warm look as the blazer settles, the smile easing into warm "
        "calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 holding open book
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to hold "
        "the open book soft, her left hand on the shelf-edge, settling her weight onto the back "
        "leg exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed quiet "
        "quarter-smile, the refined reading glow resolving back toward the soft quiet day-look "
        "opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, soft and quiet among the books "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[19] = [
    # F1 - sleepy morning Look A establishing, alive lateral track, hand on mixing bowl
    (
        "Cut to a medium-wide thigh-up tracking shot in the sunlit morning kitchen: the camera "
        "dollies laterally to settle on her as she settles her weight onto the back leg and "
        "rests her right hand soft on a wooden mixing bowl, her left hand on the counter-edge, "
        "the warm wood counters and copper utensils sliding behind with real parallax; a warm "
        "sleepy quarter-smile holding.",
        "The track eases to rest as a soft face-framing tendril shifts in the kitchen warmth and "
        "she eases her warm gaze to lens, the kettle breathing a curl of steam, a soft homey "
        "quarter-smile settling.",
        "She holds, soft and sleepy in the oatmeal tee, the claw-clip twist lived-in, eyes warm "
        "in the pale morning light (silent here).",
    ),
    # F2 - morning look, push-with lifting hand from bowl toward cresting flour-dust, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting her right hand soft from "
        "the bowl toward the cresting flour-dust as if to feel it, fingers gently open, as the "
        "camera pushes with her hand; gaze toward the dust.",
        "Fine flour-dust drifts soft at her fingertips as her gaze warms with quiet wonder and a "
        "soft micro-smile kindles.",
        "She holds the hand poised toward the flour-dust, eyes warm and soft, the sleepy morning "
        "look soft and intact (silent here).",
    ),
    # F3 - morning look clean (NO bloom yet), slow arc to a fresh angle, raise hand toward flour-dust
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft "
        "toward the flour-dust and draws a slow breath, her left hand easing open on the "
        "counter, as the camera arcs a few degrees and the kitchen swings behind with parallax; "
        "gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising warm wonder and a knowing soft "
        "smile forms, the flour-dust bloom cresting in frame, still in the sleepy morning look.",
        "She holds the poised kitchen beat, hand raised toward the flour-dust, eyes warm and "
        "soft \u2014 the breath before the flour-dust bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip flour-dust bloom; first=sleepy morning, last=homey
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the sleepy-morning Look A "
        "still): she eases her hand down from the flour-dust, already in motion \u2014 still the "
        "oatmeal tee, NO bloom yet, a gentle push-with easing in, the angle fixed for the whole "
        "clip.",
        "The bloom BEGINS here, mid-clip: a single travelling flour-dust bloom sweeps smoothly "
        "across the frame in one continuous warm front, fine soft flour-dust blooming up by "
        "believable airborne drift, the sleepy oatmeal tee deepening into the soft caramel "
        "cardigan over a tidy apron and the room warming to a honey glow exactly where the bloom "
        "passes \u2014 cloth resolving with real spread and inertia, gradual and warm, never a "
        "snap, no garish glare; the claw-clip twist catching travelling honey light, eyes "
        "warming in homey wonder (angle held, face cleanly lit, identity locked).",
        "The bloom completes its sweep and the look settles smoothly and fully into the "
        "warm-homey Look B of the Veo last-frame still (Frame 5's image) \u2014 the soft caramel "
        "cardigan over the tidy apron and tee in a snug honey glow, resolved and held through "
        "the final beat, no last-second pop; a warm homey calm landing in her eyes.",
    ),
    # F5 - homey Look B reveal, cut to a NEW angle, settle the apron tie
    (
        "Cut to a medium close on a new angle in the snug honey glow: she is already in the warm "
        "homey look, drifting her right hand to settle the apron tie with an easy roll of the "
        "shoulder; gaze easing to lens.",
        "A warm homey smile eases to lens on a slow breath, the last flour-dust settling in the "
        "honey light, eyes soft and warm.",
        "She holds the warm homey look, the cardigan and apron settling soft, eyes warm and "
        "direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and drifts her right hand open soft in a warm easy gesture as the "
        "camera eases with her; gaze warm to lens.",
        "She delivers \u201cHome is something you make.\u201d to lens with a warm homey smile and "
        "natural lip-sync, the kettle steam curling soft, eyes warm and direct.",
        "She holds the warm homey look as the cardigan settles, the smile easing into warm "
        "calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 hand on mixing bowl
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft on the wooden mixing bowl, her left hand on the counter-edge, settling her weight "
        "onto the back leg exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed sleepy "
        "quarter-smile, the snug honey homey look resolving back toward the soft pale morning "
        "opening to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, soft and sleepy in the morning "
        "kitchen \u2014 a seamless loop seam.",
    ),
]


BEATSLM[20] = [
    # F1 - chic evening Look A establishing, alive lateral track, hand on rooftop railing
    (
        "Cut to a medium-wide thigh-up tracking shot on the rooftop at New Year's Eve night: "
        "the camera dollies laterally to settle on her as she settles her weight onto the back "
        "leg and rests her right hand soft on the rooftop railing, the glittering skyline and "
        "warm string lights sliding behind with real parallax against the cool night; a chic "
        "composed quarter-smile holding.",
        "The track eases to rest as a feathered face-framing wave shifts in the cool night air "
        "and she eases her gaze to lens, the first distant fireworks just beginning on the "
        "horizon, a chic composed quarter-smile settling.",
        "She holds, cool and chic in the deep-midnight top, the voluminous 70s blowout full, "
        "eyes direct in the cool blue anticipation (silent here).",
    ),
    # F2 - chic look, push-with lifting hand from railing toward cresting sparkler-light, cut to a closer three-quarter
    (
        "Cut to a medium-close three-quarter: she is already lifting her right hand soft from "
        "the railing toward the cresting sparkler-light as if to feel it, fingers gently open, "
        "as the camera pushes with her hand; gaze toward the sparkle.",
        "The first sparkler-light crests warm at her fingertips against the cool night as her "
        "gaze brightens with quiet anticipation and a knowing micro-smile kindles.",
        "She holds the hand poised toward the sparkler-light, eyes bright and cool, the chic "
        "evening look crisp and intact (silent here).",
    ),
    # F3 - chic look clean (NO burst yet), slow arc to a fresh angle, raise hand toward sparkler-light
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she raises her hand soft "
        "toward the sparkler-light and draws a slow breath, her left hand easing open at her "
        "side, as the camera arcs a few degrees and the skyline swings behind with parallax; "
        "gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising spark and a knowing micro-smile "
        "forms, the sparkler-and-confetti wave cresting in frame, still in the chic evening "
        "look.",
        "She holds the poised rooftop beat, hand raised to the sparkler-light, eyes bright and "
        "cool \u2014 the breath before the sparkler-and-confetti wave (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip sparkler-confetti wave; first=chic evening, last=glam NYE
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the chic-evening Look A "
        "still): she eases her hand down from the sparkler-light, already in motion \u2014 still "
        "the deep-midnight top, NO burst yet, a gentle push-with easing in, the angle fixed for "
        "the whole clip.",
        "The burst BEGINS here, mid-clip: a single travelling sparkler-and-confetti wave sweeps "
        "smoothly across the frame in one continuous front, warm sparkler-light and soft "
        "confetti blooming up by believable airborne drift against the dark night, the chic "
        "midnight top deepening into the shimmering softly-sequined modest gown and the scene "
        "warming from cool blue to a sparkling celebratory glow exactly where the wave passes "
        "\u2014 cloth and sequins resolving with real weight and inertia, sparkle balanced "
        "against the dark sky (not garish), gradual and warm, never a snap; the 70s blowout "
        "catching travelling sparkle-light, eyes brightening in celebratory awe (angle held, "
        "face cleanly lit, identity locked).",
        "The wave completes its sweep and the look settles smoothly and fully into the glamorous "
        "NYE Look B of the Veo last-frame still (Frame 5's image) \u2014 the shimmering "
        "softly-sequined modest gown with long sleeves in a sparkling warm celebratory glow "
        "against the night skyline, resolved and held through the final beat, no last-second "
        "pop; a bright celebratory resolve landing in her eyes.",
    ),
    # F5 - glam NYE Look B reveal, cut to a NEW angle, settle the clutch
    (
        "Cut to a medium close on a new angle in the sparkling celebratory glow: she is already "
        "in the glamorous shimmering gown, drifting her right hand to settle the small clutch "
        "with an easy roll of the shoulder; gaze easing to lens.",
        "A bright celebratory smile eases to lens on a slow breath, the last confetti settling "
        "with a warm sparkle against the night, eyes shining and warm.",
        "She holds the glamorous celebratory look, the sequined gown shimmering soft, eyes "
        "bright and direct (silent here).",
    ),
    # F6 - spoken line, cut to a fresh angle, push-with the turn
    (
        "Cut to a medium chest-up on a fresh angle: she shifts her weight with an easy "
        "six-degree turn and drifts her right hand open soft in a warm easy gesture as the "
        "camera eases with her; gaze warm to lens.",
        "She delivers \u201cNew year. Same fire, brighter.\u201d to lens with a bright "
        "celebratory smile and natural lip-sync, the delicate pendant catching a warm glint, "
        "eyes warm and direct.",
        "She holds the glamorous celebratory look as the gown settles, the smile easing into "
        "bright calm.",
    ),
    # F7 - loop close, cut back to match Frame 1 hand on railing
    (
        "Cut to a medium-wide thigh-up matched to Frame 1: she returns her right hand to rest "
        "soft on the rooftop railing and settles her weight onto the back leg exactly as in "
        "Frame 1 as the camera settles to the opening framing.",
        "She eases her gaze back to lens on a slow breath with the composed chic quarter-smile, "
        "the sparkling celebratory glow resolving back toward the cool blue rooftop opening to "
        "seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, cool and chic on the night rooftop "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[31] = [
    # F1 - opulent gilded-glow beauty hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the candlelit Renaissance studio: she is already "
        "cradling the faceted amber-gold Gold \u00c9lixir bottle at her collarbone as a slow "
        "push eases in, the deep oxblood velvet drapery and gilded baroque frame soft behind in "
        "warm chiaroscuro; her left hand resting easy near her jaw.",
        "The push settles as a face-framing strand shifts in the warm candle-draft and her warm "
        "gaze eases to lens, dust-motes hanging in the light shaft, an opulent quarter-smile "
        "settling.",
        "She holds the opulent gilded-glow look, the burgundy velvet drinking the candle key, "
        "eyes warm and direct, the bottle glinting (the line lands later).",
    ),
    # F2 - build, lifting dropper to cheekbone, a gold drop; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already lifting the Gold \u00c9lixir dropper near her cheekbone and releasing a "
        "single warm liquid-gold drop that catches the candlelight; gaze cast soft to the drop.",
        "The gold drop beads warm on her cheekbone as her gaze warms with quiet focus and a "
        "knowing micro-smile kindles, the first gold-leaf flakes drifting in.",
        "She holds the dropper poised near her cheek, eyes warm and opulent, the gilded-glow "
        "look intact (silent here).",
    ),
    # F3 - START clean (flakes gathering, NO sweep yet), slow arc to a fresh angle
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the dropper down "
        "from her cheek and opens her left hand soft into the gathering gold flakes, drawing a "
        "slow breath as the camera arcs a few degrees and the velvet drapery swings behind with "
        "parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising warmth and a knowing micro-smile "
        "forms, gold-leaf flakes gathering and suspending in the warm air, still the opulent "
        "gilded-glow look.",
        "She holds the poised opulent beat, the flakes suspended, eyes warm and bright \u2014 the "
        "hush before the gilding sweep (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip gilding sweep; first=gilded-glow, last=fully-gilded
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the gilded-glow Look A "
        "still): she drifts both arms open from her body, already in motion \u2014 still the "
        "opulent gilded-glow look, NO full gilding yet, a gentle push-with easing in, the angle "
        "fixed for the whole clip.",
        "The gilding sweep BEGINS here, mid-clip: a shimmering gold-leaf sweep travels smoothly "
        "across her skin and gilds the air in one continuous warm wavefront, real beaten-gold "
        "foil settling along her cheekbone, shoulder and the velvet exactly where it passes "
        "\u2014 painterly true gold-leaf physics, no garish glare, gradual and opulent, never a "
        "snap; her face stays clear and warmly lit, eyes warming in opulent wonder (angle held, "
        "identity locked).",
        "The sweep completes and the look settles smoothly and fully into the fully-gilded "
        "radiant after-look of the Veo last-frame still (Frame 5's image) \u2014 a warm gilded "
        "glow set across her skin in the candlelight, resolved and held through the final beat, "
        "no last-second pop; a warm opulent calm landing in her eyes.",
    ),
    # F5 - END fully-gilded reveal, hand back to bottle, spoken line; slow orbit/push
    (
        "Cut to a medium close on a new angle in the candlelit warmth: she is already in the "
        "fully-gilded radiant after-look, easing both hands open and drifting her right back "
        "toward the faceted bottle at her collarbone as a slow orbit eases around her; gaze "
        "warm to lens.",
        "She delivers \u201cworth its weight in gold.\u201d to lens with a warm knowing smile "
        "and natural lip-sync, a settling gold-leaf shimmer catching the candle key, eyes warm "
        "and radiant.",
        "She holds the fully-gilded opulent look, the bottle cradled soft, eyes warm and direct.",
    ),
    # F6 - held opulent, cradling bottle; gentle push
    (
        "Cut to a medium-close chest-up on a fresh angle: she settles both hands gently, the "
        "right cradling the faceted bottle soft near her collarbone, the left easy near her "
        "jaw, as a gentle push eases in; gaze warm to lens.",
        "A serene opulent smile holds to lens on a slow warm breath, the gilded glow even on "
        "her skin, dust-motes drifting in the candle shaft.",
        "She holds the regal opulent beat, the velvet rich and the gold settled, eyes warm and "
        "direct \u2014 a held moment before the loop (silent here).",
    ),
    # F7 - loop close, cradle bottle matched to F1; pull-out
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to "
        "cradle the faceted amber-gold bottle at collarbone height and her left easy near her "
        "jaw exactly as in Frame 1 as a soft pull-out settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed opulent "
        "quarter-smile, the fully-gilded glow resolving back toward the opening gilded-glow look "
        "to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, opulent and candlelit \u2014 a "
        "seamless loop seam.",
    ),
]


BEATSLM[32] = [
    # F1 - bioluminescent-glow hero (silent), drifting upright in the abyss, push-in
    (
        "Cut to a medium-close chest-up in the deep-sea abyss: she is already drifting upright "
        "and buoyant in the inky teal-black water as a slow push eases in, drifting "
        "bioluminescent plankton and pale god-rays filtering from far above behind her; her "
        "right hand cradling the faceted bottle soft at her collarbone.",
        "The push settles as a strand of hair lifts weightless in the real water and her cool "
        "gaze eases to lens, glowing motes hanging in the dark, a serene mysterious "
        "quarter-smile settling.",
        "She holds the bioluminescent-glow look in the deep-teal iridescent gown drifting "
        "weightless, eyes cool and luminous (silent reel).",
    ),
    # F2 - build, serum drop, first plankton sparking; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already releasing a glowing aqua drop near her cheekbone and the first plankton "
        "spark alight in the dark water; gaze cast soft to the drop.",
        "The aqua drop beads cool and luminous as her gaze softens with quiet wonder and a "
        "mysterious micro-smile kindles, plankton motes beginning to drift in.",
        "She holds the drop poised near her cheek, eyes cool and dreamy, the bioluminescent-glow "
        "look intact (silent here).",
    ),
    # F3 - START clean (plankton gathering, NO bloom yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases her hand down and "
        "opens it soft into the gathering plankton, drawing a slow underwater breath as the "
        "camera arcs a few degrees and the abyss drifts behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising cool wonder and a knowing "
        "micro-smile forms, bioluminescent plankton gathering and suspending in the dark water, "
        "still the bioluminescent-glow look.",
        "She holds the poised mysterious beat, the plankton suspended and glowing soft, eyes "
        "cool and bright \u2014 the hush before the glow bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip plankton bloom; first=glow, last=fully-glowing
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the bioluminescent-glow "
        "Look A still): she drifts both arms open from her body, already in motion \u2014 still "
        "the bioluminescent-glow look, NO full bloom yet, a gentle buoyant push-with easing in, "
        "the angle fixed for the whole clip.",
        "The glow bloom BEGINS here, mid-clip: a cloud of bioluminescent plankton blooms alight "
        "around her in one continuous expanding aura, glowing motes kindling across her "
        "cheekbone, shoulder and the drifting gown exactly where the bloom passes \u2014 "
        "believable real bioluminescent particle physics, motes drifting on true underwater "
        "currents (no cheap sparkles), her face clear and cool-lit, eyes widening in mysterious "
        "wonder (angle held, identity locked).",
        "The bloom completes and the look settles smoothly and fully into the fully-glowing "
        "radiant after-look of the Veo last-frame still (Frame 5's image) \u2014 a glowing "
        "bioluminescent aura set around her in the dark water, resolved and held through the "
        "final beat, no last-second pop; a cool radiant calm landing in her eyes.",
    ),
    # F5 - END fully-glowing reveal (silent, wordless awe), new angle, hand to bottle
    (
        "Cut to a medium close on a new angle in the glowing dark: she is already in the "
        "fully-glowing radiant after-look, drifting her right hand soft back toward the faceted "
        "bottle at her collarbone with a buoyant roll of the shoulder; gaze easing to lens.",
        "A serene radiant wordless awe eases to lens on a slow underwater breath, the last "
        "plankton settling into a soft glowing aura, eyes cool and luminous (silent reveal).",
        "She holds the mysterious radiant look, the glow even around her in the water, eyes cool "
        "and direct (silent here).",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the faceted bottle soft at her collarbone and drifts upright exactly as in Frame 1 as "
        "the camera settles to the opening framing.",
        "She eases her cool gaze back to lens on a slow underwater breath with the composed "
        "mysterious quarter-smile, the fully-glowing aura resolving back toward the opening "
        "bioluminescent-glow look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, drifting buoyant in the abyss "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[33] = [
    # F1 - fresh dewy-glow spring hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the bright spring grove: she is already cradling the "
        "faceted bottle soft at her collarbone as a slow push eases in, soft pale-pink cherry "
        "blossoms and dappled morning sun behind her, a few petals drifting; her left hand easy "
        "near her jaw.",
        "The push settles as a face-framing strand lifts in the spring breeze and her bright "
        "gaze eases to lens, petals drifting through the dappled light, a fresh joyful "
        "quarter-smile settling.",
        "She holds the fresh dewy-glow look in the soft blush-pink wrap dress, eyes bright and "
        "warm in the spring sun (the line lands later).",
    ),
    # F2 - build, blush drop, first buds swelling; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already releasing a soft blush drop near her cheekbone and the first blossom "
        "buds swell on the branches; gaze cast soft to the drop.",
        "The blush drop beads dewy on her cheekbone as her gaze warms with quiet joy and a fresh "
        "micro-smile kindles, buds swelling in around her.",
        "She holds the drop poised near her cheek, eyes bright and fresh, the dewy-glow look "
        "intact (silent here).",
    ),
    # F3 - START clean (buds swelling, NO bloom yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases her hand down and "
        "opens it soft toward the swelling buds, drawing a slow spring breath as the camera "
        "arcs a few degrees and the blossom grove swings behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising fresh joy and a knowing "
        "micro-smile forms, blossom buds swelling and the first petals unfurling, still the "
        "fresh dewy-glow look.",
        "She holds the poised spring beat, buds swelling at her shoulder, eyes bright and joyful "
        "\u2014 the hush before the blossom bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip time-lapse bloom; first=dewy-glow, last=full-blossom
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the fresh dewy-glow Look "
        "A still): she opens both arms soft from her body, already in motion \u2014 still the "
        "fresh dewy-glow look, the buds NOT yet bloomed, a gentle push-with easing in, the angle "
        "fixed for the whole clip.",
        "The blossom bloom BEGINS here, mid-clip: the cherry blossoms burst into full bloom "
        "around her in one continuous time-lapse wave, buds unfurling to full petals across the "
        "branches and petals showering down exactly where the bloom passes \u2014 believable "
        "real botanical time-lapse physics, petals fluttering on true spring air (no cheap "
        "sparkles), her face clear and bright, eyes widening in fresh joyful wonder (angle held, "
        "identity locked).",
        "The bloom completes and the look settles smoothly and fully into the full-blossom "
        "radiant after-look of the Veo last-frame still (Frame 5's image) \u2014 cherry blossoms "
        "in full bloom around her and a fresh dewy radiance on her skin, resolved and held "
        "through the final beat, no last-second pop; a fresh joyful calm landing in her eyes.",
    ),
    # F5 - END full-blossom reveal, hand to bottle, spoken line
    (
        "Cut to a medium close on a new angle amid the full blossom: she is already in the "
        "full-blossom radiant after-look, drifting her right hand soft back toward the faceted "
        "bottle at her collarbone with an easy roll of the shoulder, petals showering soft; "
        "gaze warm to lens.",
        "She delivers \u201cspring starts with me.\u201d to lens with a fresh joyful smile and "
        "natural lip-sync, petals drifting through the dappled sun, eyes bright and warm.",
        "She holds the fresh radiant spring look, the blossoms full around her, eyes bright and "
        "direct.",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the faceted bottle soft at her collarbone and her left easy near her jaw exactly as in "
        "Frame 1 as the camera settles to the opening framing.",
        "She eases her bright gaze back to lens on a slow spring breath with the composed joyful "
        "quarter-smile, the full-blossom radiance resolving back toward the opening dewy-glow "
        "look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, fresh and joyful in the spring sun "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[34] = [
    # F1 - celestial-glow hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the cosmic night: she is already cradling the faceted "
        "bottle soft at her collarbone as a slow push eases in, the midnight indigo-to-violet "
        "starfield and drifting nebula haze behind her, scattered stars glowing; her left hand "
        "easy near her jaw.",
        "The push settles as a face-framing strand lifts in the still cosmic air and her cool "
        "gaze eases to lens, soft star-shimmer hanging in the dark, a serene mystic "
        "quarter-smile settling.",
        "She holds the celestial-glow look in the deep-indigo star-flecked gown, silver "
        "constellation embroidery catching the light, eyes cool and luminous (the line lands "
        "later).",
    ),
    # F2 - build, elixir drop, first stars sparking; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already releasing a glowing elixir drop near her cheekbone and the first stars "
        "spark alight in the dark around her; gaze cast soft to the drop.",
        "The glowing drop beads cool on her cheekbone as her gaze softens with quiet wonder and "
        "a mystic micro-smile kindles, glowing stars beginning to gather.",
        "She holds the drop poised near her cheek, eyes cool and dreamy, the celestial-glow look "
        "intact (silent here).",
    ),
    # F3 - START clean (stars gathering, lines beginning, NO full draw yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases her hand down and "
        "opens it soft into the gathering stars, drawing a slow breath as the camera arcs a few "
        "degrees and the starfield drifts behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising cool wonder and a knowing "
        "micro-smile forms, glowing stars gathering and the first silver light-lines beginning "
        "to reach between them, still the celestial-glow look.",
        "She holds the poised mystic beat, stars suspended and lines just kindling, eyes cool "
        "and bright \u2014 the hush before the constellation draws (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip line-draw; first=celestial-glow, last=full-constellation
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the celestial-glow Look A "
        "still): she opens both arms soft from her body, already in motion \u2014 still the "
        "celestial-glow look, the constellation NOT yet drawn, a gentle push-with easing in, the "
        "angle fixed for the whole clip.",
        "The line-draw BEGINS here, mid-clip: glowing stars connect with silver light-lines "
        "drawing a full constellation around her in one continuous reaching pattern, the lines "
        "tracing star to star across the dark exactly where the draw passes \u2014 believable "
        "real light-line physics, true point-to-point glow (no cheap sparkles), her face clear "
        "and cool-lit, eyes widening in mystic wonder (angle held, identity locked).",
        "The draw completes and the look settles smoothly and fully into the full-constellation "
        "radiant after-look of the Veo last-frame still (Frame 5's image) \u2014 a glowing "
        "silver constellation drawn around her in the starfield, resolved and held through the "
        "final beat, no last-second pop; a cool radiant calm landing in her eyes.",
    ),
    # F5 - END full-constellation reveal, hand to bottle, spoken line
    (
        "Cut to a medium close on a new angle in the glowing dark: she is already in the "
        "full-constellation radiant after-look, drifting her right hand soft back toward the "
        "faceted bottle at her collarbone with an easy roll of the shoulder; gaze warm to lens.",
        "She delivers \u201cwritten in the stars.\u201d to lens with a serene mystic smile and "
        "natural lip-sync, the silver constellation glowing soft around her, eyes cool and "
        "radiant.",
        "She holds the mystic radiant look, the constellation glowing around her, eyes cool and "
        "direct.",
    ),
    # F6 - held mystic, cradling bottle
    (
        "Cut to a medium-close chest-up on a fresh angle: she settles both hands gently, the "
        "right cradling the faceted bottle soft near her collarbone, the left easy near her "
        "jaw, as a gentle push eases in; gaze cool to lens.",
        "A serene mystic smile holds to lens on a slow cool breath, the constellation glowing "
        "even around her, soft star-shimmer drifting.",
        "She holds the serene mystic beat, the starfield deep behind and the constellation "
        "glowing, eyes cool and direct \u2014 a held moment before the loop (silent here).",
    ),
    # F7 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the faceted bottle soft at her collarbone and her left easy near her jaw exactly as in "
        "Frame 1 as the camera settles to the opening framing.",
        "She eases her cool gaze back to lens on a slow breath with the composed mystic "
        "quarter-smile, the full-constellation glow resolving back toward the opening "
        "celestial-glow look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, serene in the cosmic night \u2014 a "
        "seamless loop seam.",
    ),
]


BEATSLM[35] = [
    # F1 - warm golden-glow beauty hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the warm honey-lit space: she is already cradling the "
        "faceted amber bottle of Golden Honey soft at her collarbone as a slow push eases in, the "
        "rich amber-gold backdrop and honeycomb-warm light behind her, slow golden motes "
        "drifting; her left hand easy near her jaw.",
        "The push settles as a face-framing strand drifts in the warm air and her warm gaze eases "
        "to lens, golden motes hanging in the honeyed light, a content sensorial quarter-smile "
        "settling.",
        "She holds the warm golden-glow look in the honey-gold-to-caramel satin wrap dress, the "
        "satin drinking the golden key, eyes warm and luminous (the line lands later).",
    ),
    # F2 - build, honey drop, first amber-glaze glints; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already lifting the Golden Honey dropper near her cheekbone and releasing a "
        "single slow golden honey drop that stretches and catches the warm light; gaze cast soft "
        "to the drop.",
        "The honey drop beads warm on her cheekbone as her gaze warms with quiet pleasure and a "
        "content micro-smile kindles, the first warm amber-glaze glints gathering in.",
        "She holds the drop poised near her cheek, eyes warm and sensorial, the golden-glow look "
        "intact (silent here).",
    ),
    # F3 - START clean (ribbons gathering, glaze beginning, NO full sweep yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the dropper down and "
        "opens her hand soft into the gathering golden ribbons, drawing a slow warm breath as the "
        "camera arcs a few degrees and the amber backdrop swings behind with parallax; gaze "
        "lifting.",
        "The arc settles as her gaze lifts to lens with rising sensorial warmth and a knowing "
        "micro-smile forms, slow golden honey ribbons gathering and drifting and the first "
        "amber-glaze gilding her shoulder, still the warm golden-glow look.",
        "She holds the poised warm beat, the honey ribbons suspended and drifting, eyes warm and "
        "bright \u2014 the hush before the amber-glaze sweep (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip honey-glaze; first=golden-glow, last=honey-gilded
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the warm golden-glow Look "
        "A still): she drifts both arms open from her body, already in motion \u2014 still the "
        "warm golden-glow look, NO full glaze yet, a gentle push-with easing in, the angle fixed "
        "for the whole clip.",
        "The honey-glaze BEGINS here, mid-clip: slow golden honey ribbons drift and a warm "
        "amber-glaze of light sweeps smoothly across her and gilds the air in one continuous warm "
        "wavefront, real viscous-honey drift and warm gilding light settling along her cheekbone, "
        "shoulder and the satin exactly where it passes \u2014 believable true viscous-honey and "
        "warm-light physics, no garish glare, gradual and indulgent, never a snap; her face stays "
        "clear and warmly lit, eyes warming in sensorial wonder (angle held, identity locked).",
        "The glaze completes and the look settles smoothly and fully into the full honey-gilded "
        "radiant after-look of the Veo last-frame still (Frame 5's image) \u2014 a warm honey-gild "
        "set across her skin and the satin in the amber light, resolved and held through the final "
        "beat, no last-second pop; a warm sensorial calm landing in her eyes.",
    ),
    # F5 - END honey-gilded reveal, hand to bottle, spoken line
    (
        "Cut to a medium close on a new angle in the honeyed warmth: she is already in the full "
        "honey-gilded radiant after-look, easing both hands open and drifting her right back "
        "toward the amber bottle at her collarbone with an easy roll of the shoulder; gaze warm "
        "to lens.",
        "She delivers \u201cgolden, inside and out.\u201d to lens with a warm content smile and "
        "natural lip-sync, a last honey ribbon settling and catching the warm key, eyes warm and "
        "radiant.",
        "She holds the full honey-gilded warm look, the bottle cradled soft, eyes warm and "
        "direct.",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the faceted amber bottle soft at her collarbone and her left easy near her jaw exactly "
        "as in Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed content "
        "quarter-smile, the full honey-gild resolving back toward the opening warm golden-glow "
        "look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, warm and sensorial in the honey-lit "
        "room \u2014 a seamless loop seam.",
    ),
]


BEATSLM[36] = [
    # F1 - fresh dewy rain-glow beauty hero (contained, product-at-face, SILENT), push-in
    (
        "Cut to a medium-close chest-up in the cool monsoon scene: she is already cradling the "
        "misted rain-clear bottle of Monsoon Mist soft at her collarbone as a slow push eases in, "
        "the soft rain-grey-to-teal backdrop and a sheet of soft falling rain behind her, "
        "drifting mist; her left hand easy near her jaw.",
        "The push settles as a rain-damp face-framing strand eases at the temple and her calm "
        "gaze eases to lens, soft rain drifting in the cool light, a fresh serene quarter-smile "
        "settling.",
        "She holds the fresh dewy rain-glow look in the cool slate-teal satin wrap dress, the "
        "satin catching the cool key, eyes calm and luminous (silent reel).",
    ),
    # F2 - build, cool essence drop, first ripples; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already releasing a single cool translucent drop near her cheekbone and the "
        "first soft ripples bloom on a wet surface around her; gaze cast soft to the drop.",
        "The cool drop beads dewy on her cheekbone as her gaze softens with fresh anticipation "
        "and a serene micro-smile kindles, the first ripples spreading in.",
        "She holds the drop poised near her cheek, eyes cool and refreshed, the fresh rain-glow "
        "look intact (silent here).",
    ),
    # F3 - START clean (rain gathering, ripples beginning, NO full bloom yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases her hand down and "
        "opens it soft into the gathering rain, drawing a slow cool breath as the camera arcs a "
        "few degrees and the rain backdrop drifts behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising cool freshness and a knowing "
        "micro-smile forms, the soft sheet of rain gathering and sweeping closer and the first "
        "dewy ripples blooming, still the fresh rain-glow look.",
        "She holds the poised cool beat, the rain gathering and ripples spreading soft, eyes "
        "cool and bright \u2014 the hush before the rain-bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip rain bloom; first=rain-glow, last=rain-kissed
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the fresh rain-glow Look A "
        "still): she drifts both arms open from her body, already in motion \u2014 still the "
        "fresh rain-glow look, NO full bloom yet, a gentle push-with easing in, the angle fixed "
        "for the whole clip.",
        "The rain-bloom BEGINS here, mid-clip: a soft sheet of rain sweeps smoothly across her "
        "and dewy ripples bloom in concentric rings across the air and wet surfaces around her "
        "in one continuous fresh wavefront, cool rain-beads kissing her cheekbone, shoulder and "
        "the satin exactly where it passes \u2014 believable real rain and water-ripple physics, "
        "droplets falling on true gravity and rings spreading by real surface tension (no cheap "
        "sparkles), her face clear and cool-lit, eyes brightening in refreshed wonder (angle "
        "held, identity locked).",
        "The bloom completes and the look settles smoothly and fully into the full rain-kissed "
        "radiant after-look of the Veo last-frame still (Frame 5's image) \u2014 a fresh dewy "
        "rain-kissed glow set across her skin and the satin in the cool monsoon light, resolved "
        "and held through the final beat, no last-second pop; a cool radiant calm landing in her "
        "eyes.",
    ),
    # F5 - END rain-kissed reveal (silent, wordless), new angle, hand to bottle
    (
        "Cut to a medium close on a new angle in the fresh rain: she is already in the full "
        "rain-kissed radiant after-look, drifting her right hand soft back toward the misted "
        "bottle at her collarbone with an easy roll of the shoulder; gaze easing to lens.",
        "A fresh serene wordless smile eases to lens on a cool soft breath, the last rain "
        "drifting and a final ripple settling, eyes cool and luminous (silent reveal \u2014 no "
        "words).",
        "She holds the fresh radiant rain-kissed look, the dew even across her skin, eyes cool "
        "and direct (silent here).",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the misted rain-clear bottle soft at her collarbone and her left easy near her jaw "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her cool gaze back to lens on a soft breath with the composed serene "
        "quarter-smile, the full rain-kissed glow resolving back toward the opening fresh "
        "rain-glow look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, fresh and cool in the monsoon hush "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[37] = [
    # F1 - regal pearl-glow couture hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the regal couture salon: she is already cradling the "
        "pearl-white opaline bottle of Plume at her collarbone as a slow push eases in, the soft "
        "ivory-and-champagne backdrop and drifting white feather-plumes behind her in gilded "
        "light; her left hand resting easy near her jaw.",
        "The push settles as a face-framing tendril drifts in the salon air and her serene gaze "
        "eases to lens, a feather-plume drifting past, a poised regal quarter-smile settling.",
        "She holds the regal pearl-glow look, the ivory-and-champagne couture gown drinking the "
        "gilded key, eyes serene and direct, the bottle glinting (the line lands later).",
    ),
    # F2 - build, atomizer mist, first feather-plumes; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already lifting the Plume atomizer near her cheekbone and pressing a fine "
        "pearlescent mist that catches the gilded light; gaze cast soft to the mist.",
        "The pearl mist drifts soft at her cheekbone as her gaze warms with poise and a knowing "
        "regal micro-smile kindles, the first white feather-plumes drifting in.",
        "She holds the atomizer poised near her cheek, eyes serene and regal, the pearl-glow "
        "look intact (silent here).",
    ),
    # F3 - START clean (plumes gathering, NO full burst yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the atomizer down "
        "from her cheek and opens her left hand soft into the gathering feather-plumes, drawing "
        "a slow regal breath as the camera arcs a few degrees and the salon swings behind with "
        "parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising poise and a knowing micro-smile "
        "forms, white feather-plumes gathering and drifting and suspending in the gilded air, "
        "still the regal pearl-glow look.",
        "She holds the poised regal beat, the plumes suspended and drifting, eyes serene and "
        "bright \u2014 the hush before the feather-burst (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip feather-burst; first=pearl-glow, last=feather-crowned
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the regal pearl-glow Look "
        "A still): she drifts both arms open from her body, already in motion \u2014 still the "
        "regal pearl-glow look, NO full burst yet, a gentle push-with easing in, the angle fixed "
        "for the whole clip.",
        "The feather-burst BEGINS here, mid-clip: a soft cloud of white feather-plumes bursts "
        "and drifts in graceful regal arcs around her in one continuous wavefront, real plumes "
        "fanning out across the gilded air and settling along her shoulder and the gown exactly "
        "where it passes \u2014 believable real feather-drift physics, soft plumes riding true "
        "air currents at their own natural pace (no cheap sparkles), her face clear and warmly "
        "lit, eyes warming in regal wonder (angle held, identity locked).",
        "The burst completes and the look settles smoothly and fully into the feather-crowned "
        "radiant after-look of the Veo last-frame still (Frame 5's image) \u2014 a soft crown of "
        "white feather-plumes drifted around her in the gilded salon light, resolved and held "
        "through the final beat, no last-second pop; a serene regal calm landing in her eyes.",
    ),
    # F5 - END feather-crowned reveal, hand to bottle, spoken line; slow orbit
    (
        "Cut to a medium close on a new angle in the gilded salon light: she is already in the "
        "feather-crowned radiant after-look, easing both hands open and drifting her right back "
        "toward the opaline bottle at her collarbone as a slow orbit eases around her; gaze warm "
        "to lens.",
        "She delivers \u201cborn to wear the crown.\u201d to lens with a poised regal smile and "
        "natural lip-sync, a settling feather-plume catching the gilded key, eyes serene and "
        "radiant.",
        "She holds the feather-crowned regal look, the bottle cradled soft, eyes serene and "
        "direct.",
    ),
    # F6 - held regal, cradling bottle; gentle push
    (
        "Cut to a medium-close chest-up on a fresh angle: she settles both hands gently, the "
        "right cradling the opaline bottle soft near her collarbone, the left easy near her jaw, "
        "as a gentle push eases in; gaze serene to lens.",
        "A poised regal smile holds to lens on a slow soft breath, the feather-plumes drifting "
        "even around her, gilded light on her skin.",
        "She holds the regal couture beat, the salon soft and the plumes settled, eyes serene "
        "and direct \u2014 a held moment before the loop (silent here).",
    ),
    # F7 - loop close, cradle bottle matched to F1; pull-out
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the pearl-white opaline bottle at collarbone height and her left easy near her jaw "
        "exactly as in Frame 1 as a soft pull-out settles to the opening framing.",
        "She eases her serene gaze back to lens on a slow breath with the composed regal "
        "quarter-smile, the feather-crowned look resolving back toward the opening pearl-glow "
        "look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, regal in the gilded salon \u2014 a "
        "seamless loop seam.",
    ),
]


BEATSLM[38] = [
    # F1 - whimsical iridescent-glow hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the bright whimsical studio: she is already cradling "
        "the clear faceted Prism tube at her collarbone as a slow push eases in, the soft "
        "pearl-white-to-pastel backdrop and drifting iridescent soap-bubbles behind her in "
        "bright airy light; her left hand easy near her jaw.",
        "The push settles as a face-framing strand drifts in the studio air and her bright gaze "
        "eases to lens, an iridescent bubble drifting past, a bright playful quarter-smile "
        "settling.",
        "She holds the whimsical iridescent-glow look in the pearlescent oil-slick satin top, "
        "the fabric catching rainbow-pearl light, eyes bright and direct (the line lands "
        "later).",
    ),
    # F2 - build, gloss-swipe, first soap-bubbles; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the tube to her eye: she "
        "is already sweeping the Prism gloss soft across her lip and the first iridescent "
        "soap-bubbles drift up around her catching rainbow light; gaze cast soft to the tube.",
        "The iridescent gloss catches the bright key on her lip as her gaze brightens with "
        "playful delight and a knowing micro-smile kindles, more soap-bubbles drifting in.",
        "She holds the gloss poised near her lip, eyes bright and playful, the iridescent-glow "
        "look intact (silent here).",
    ),
    # F3 - START clean (bubbles gathering, film beginning, NO full bloom yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the tube down and "
        "opens her hand soft into the gathering soap-bubbles, drawing a slow bright breath as "
        "the camera arcs a few degrees and the pastel backdrop swings behind with parallax; gaze "
        "lifting.",
        "The arc settles as her gaze lifts to lens with rising playful delight and a knowing "
        "micro-smile forms, iridescent soap-bubbles gathering and drifting and an oil-slick "
        "rainbow film just beginning to shimmer in the air, still the iridescent-glow look.",
        "She holds the poised whimsical beat, the bubbles suspended and drifting, eyes bright "
        "and delighted \u2014 the hush before the soap-film bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip soap-film bloom; first=iridescent-glow, last=iridescent-radiant
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the iridescent-glow Look "
        "A still): she drifts both arms open from her body, already in motion \u2014 still the "
        "iridescent-glow look, NO full bloom yet, a gentle push-with easing in, the angle fixed "
        "for the whole clip.",
        "The soap-film bloom BEGINS here, mid-clip: a cloud of iridescent soap-bubbles drifts "
        "and an oil-slick rainbow film blooms across the air around her in one continuous "
        "shimmering wavefront, thin-film rainbow sheen rippling across the bubbles and her "
        "shoulder and the satin exactly where it passes \u2014 believable real soap-film optics "
        "(true thin-film interference shifting with the angle), bubbles riding real air drift "
        "(no cheap sparkles), her face clear and bright-lit, eyes brightening in playful wonder "
        "(angle held, identity locked).",
        "The bloom completes and the look settles smoothly and fully into the iridescent-radiant "
        "after-look of the Veo last-frame still (Frame 5's image) \u2014 a bright oil-slick "
        "rainbow shimmer drifted around her in the airy studio, resolved and held through the "
        "final beat, no last-second pop; a bright delighted calm landing in her eyes.",
    ),
    # F5 - END iridescent-radiant reveal, hand to tube, spoken line
    (
        "Cut to a medium close on a new angle in the bright airy studio: she is already in the "
        "iridescent-radiant after-look, easing both hands open and drifting her right back "
        "toward the Prism tube at her collarbone with an easy roll of the shoulder; gaze bright "
        "to lens.",
        "She delivers \u201ccatch the light, catch the magic.\u201d to lens with a bright "
        "playful smile and natural lip-sync, a settling soap-bubble catching a rainbow glint, "
        "eyes bright and delighted.",
        "She holds the iridescent-radiant whimsical look, the tube cradled soft, eyes bright and "
        "direct.",
    ),
    # F6 - loop close, cradle tube matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the clear faceted Prism tube soft at her collarbone and her left easy near her jaw "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her bright gaze back to lens on a soft breath with the composed playful "
        "quarter-smile, the iridescent shimmer resolving back toward the opening iridescent-glow "
        "look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, bright and playful in the airy studio "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[39] = [
    # F1 - bold graphic op-art hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the graphic op-art studio: she is already cradling "
        "the op-art striped Optic tube at her collarbone as a slow push eases in, the bold "
        "black-and-white concentric backdrop and one electric pop-color accent behind her, a "
        "slow kaleidoscope light-play drifting; her left hand easy near her jaw.",
        "The push settles as a strand of the glossy bob catches the crisp key and her bright "
        "gaze eases to lens, the op-art pattern crisp behind, a knowing playful quarter-smile "
        "settling.",
        "She holds the bold graphic op-art look, the geometric top holding clean edges, eyes "
        "bright and direct (the line lands later).",
    ),
    # F2 - build, lip-and-liner snap, first facets mirroring; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the tube to her eye: she "
        "is already snapping the chrome Optic cap and sweeping the bold liner-flick crisp at her "
        "eye as the first op-art facets begin to mirror in the light around her; gaze cast soft "
        "to the tube.",
        "The crisp graphic flick lands sharp at her eye as her gaze brightens with playful focus "
        "and a knowing micro-smile kindles, the kaleidoscope light beginning to turn behind "
        "her.",
        "She holds the liner poised at her eye, eyes bright and mod-cool, the graphic op-art "
        "look intact (silent here).",
    ),
    # F3 - START clean (facets beginning to mirror, NO full split yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the tube down and "
        "opens her hand soft as the op-art facets begin to mirror and turn, drawing a slow "
        "breath as the camera arcs a few degrees and the backdrop swings behind with parallax; "
        "gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising playful spark and a knowing "
        "micro-smile forms, the op-art pattern and light beginning to fracture and mirror into "
        "slow kaleidoscope facets around her, her single face clear and unmirrored, still the "
        "graphic op-art look.",
        "She holds the poised mod beat, the facets just beginning to turn, eyes bright and "
        "hypnotic \u2014 the hush before the kaleidoscope split (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip world-fracture (NOT her face); first=op-art, last=full-kaleidoscope
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the graphic op-art Look A "
        "still): she holds her bold op-art look, already in motion \u2014 the backdrop still a "
        "normal op-art pattern, NO kaleidoscope yet, a gentle push-with easing in, the angle "
        "fixed for the whole clip.",
        "The kaleidoscope split BEGINS here, mid-clip: the op-art backdrop and light fracture "
        "and mirror into a slow-spinning kaleidoscope of facets around her in one continuous "
        "turning pattern, the checkerboard and the electric pop-color folding into true mirrored "
        "symmetry exactly where it passes \u2014 believable real kaleidoscopic mirror optics "
        "(the surrounding PATTERN mirrors, never her face), her single face clear, centred and "
        "locked (NEVER multiplied, mirrored or duplicated), eyes bright with hypnotic delight "
        "(angle held, identity locked).",
        "The split completes and the look settles smoothly and fully into the full-kaleidoscope "
        "after-look of the Veo last-frame still (Frame 5's image) \u2014 a slow-spinning op-art "
        "kaleidoscope turning around her single locked face, resolved and held through the final "
        "beat, no last-second pop; a bright playful calm landing in her eyes.",
    ),
    # F5 - END full-kaleidoscope reveal, hand to tube, spoken line
    (
        "Cut to a medium close on a new angle in the turning kaleidoscope: she is already "
        "centred in the full op-art kaleidoscope, easing her right hand back toward the Optic "
        "tube at her collarbone with an easy roll of the shoulder, her single face clear and "
        "unmirrored; gaze bright to lens.",
        "She delivers \u201csee the world in motion.\u201d to lens with a knowing playful smile "
        "and natural lip-sync, the kaleidoscope facets turning slow around her, eyes bright and "
        "hypnotic.",
        "She holds the full-kaleidoscope graphic look, her single face locked and the tube "
        "cradled soft, eyes bright and direct.",
    ),
    # F6 - loop close, cradle tube matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the op-art striped Optic tube soft at her collarbone and her left easy near her jaw "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her bright gaze back to lens on a soft breath with the composed playful "
        "quarter-smile, the kaleidoscope resolving back toward the opening normal op-art pattern "
        "to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, bright and mod in the graphic studio "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[40] = [
    # F1 - electric neon-glow hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the dark neon-night studio: she is already cradling "
        "the matte-black Lumen tube at her collarbone as a slow push eases in, the deep black "
        "backdrop and soft city-bokeh behind her, faint neon light-trails drifting; her left "
        "hand easy near her jaw.",
        "The push settles as a neon-edge glint travels the slicked crown and her bright gaze "
        "eases to lens, a cyan trail drifting past, a confident playful quarter-smile settling.",
        "She holds the electric neon-glow look, the liquid-black top catching one neon-edge "
        "glint, eyes bright and direct (the line lands later).",
    ),
    # F2 - build, highlighter-drop glow, first trails; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the tube to her eye: she "
        "is already pressing a glowing Lumen drop high on her cheekbone and the first neon "
        "light-trail begins to draw in the dark around her; gaze cast soft to the tube.",
        "The luminous drop catches a wet neon glow on her cheekbone as her gaze brightens with "
        "electric focus and a knowing micro-smile kindles, the first cyan-and-magenta trail "
        "drawing in.",
        "She holds the glow poised at her cheek, eyes bright and electric, the neon-glow look "
        "intact (silent here).",
    ),
    # F3 - START clean (trails drawing, NO full wrap yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the tube down and "
        "opens her hand soft as the first neon light-trails draw and drift, drawing a slow "
        "breath as the camera arcs a few degrees and the dark backdrop swings behind with "
        "parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising electric spark and a knowing "
        "micro-smile forms, long-exposure neon light-trails beginning to draw and loop in the "
        "dark around her, her single face clear and untouched, still the neon-glow look.",
        "She holds the poised electric beat, the trails just beginning to wrap, eyes bright and "
        "glowing \u2014 the hush before the light-trail wrap (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip light-wrap (NOT her face); first=neon-glow, last=neon-wrapped
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the electric neon-glow "
        "Look A still): she holds her neon-glow look, already in motion \u2014 no light-trails "
        "drawn yet, a gentle push-with easing in, the angle fixed for the whole clip.",
        "The light-trail wrap BEGINS here, mid-clip: long-exposure neon light-trails draw and "
        "wrap in luminous cyan-and-magenta ribbons around her in one continuous looping pattern, "
        "the glowing streaks tracing through the dark air and around her shoulder exactly where "
        "they pass \u2014 believable real long-exposure light-trail physics (continuous luminous "
        "streaks from a real moving light, true motion-blur trails, no cheap sparkles), her "
        "single face clear and locked (NEVER traced over, replaced or duplicated), eyes bright "
        "with electric delight (angle held, identity locked).",
        "The wrap completes and the look settles smoothly and fully into the full "
        "neon-trail-wrapped after-look of the Veo last-frame still (Frame 5's image) \u2014 "
        "glowing neon ribbons looped around her single locked face in the dark studio, resolved "
        "and held through the final beat, no last-second pop; a bright electric calm landing in "
        "her eyes.",
    ),
    # F5 - END neon-wrapped reveal, hand to tube, spoken line; slow orbit
    (
        "Cut to a medium close on a new angle in the glowing dark: she is already wrapped in the "
        "full neon light-trails, easing her right hand back toward the Lumen tube at her "
        "collarbone with an easy roll of the shoulder, her single face clear and untouched; gaze "
        "bright to lens.",
        "She delivers \u201cI light up the night.\u201d to lens with a confident playful smile "
        "and natural lip-sync, the neon ribbons glowing soft around her, eyes bright and "
        "electric.",
        "She holds the neon-wrapped electric look, her single face locked and the tube cradled "
        "soft, eyes bright and direct.",
    ),
    # F6 - held electric, cradling tube; gentle push
    (
        "Cut to a medium-close chest-up on a fresh angle: she settles both hands gently, the "
        "right cradling the Lumen tube soft near her collarbone, the left easy near her jaw, as "
        "a gentle push eases in; gaze bright to lens.",
        "A confident playful smile holds to lens on a slow breath, the neon trails glowing even "
        "around her, electric light on her skin.",
        "She holds the electric beat, the dark deep and the neon ribbons glowing, eyes bright "
        "and direct \u2014 a held moment before the loop (silent here).",
    ),
    # F7 - loop close, cradle tube matched to F1; pull-out
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the matte-black Lumen tube at collarbone height and her left easy near her jaw exactly "
        "as in Frame 1 as a soft pull-out settles to the opening framing.",
        "She eases her bright gaze back to lens on a slow breath with the composed confident "
        "quarter-smile, the neon-trail wrap resolving back toward the opening neon-glow look to "
        "seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, bright and electric in the neon-night "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[41] = [
    # F1 - dreamy aquatic-glow hero (contained, product-at-face, SILENT), push-in
    (
        "Cut to a medium-close chest-up in the dreamy underwater-light studio: she is already "
        "cradling the sea-glass Nacre jar at her collarbone as a slow push eases in, the soft "
        "aqua-teal gradient backdrop and dappled caustic water-light behind her, drifting "
        "bubbles; her left hand easy near her jaw.",
        "The push settles as a wet-look mermaid wave drifts in the water-light and her bright "
        "gaze eases to lens, a bubble drifting past, a soft dreamy quarter-smile settling.",
        "She holds the dreamy aquatic-glow look in the pearlescent aqua-teal scaled top, the "
        "scales catching the aqua key, eyes bright and luminous (silent reel).",
    ),
    # F2 - build, pearl-balm glide, first coral; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the jar to her eye: she "
        "is already gliding the pearl-aqua balm soft along her cheekbone and the first soft "
        "coral begins to bloom in the water around her; gaze cast soft to the jar.",
        "The pearl balm catches a dewy aqua sheen on her cheekbone as her gaze softens with "
        "dreamy wonder and a soft micro-smile kindles, the first sea-flora unfurling in.",
        "She holds the balm poised near her cheek, eyes bright and dreamy, the aquatic-glow look "
        "intact (silent here).",
    ),
    # F3 - START clean (corals beginning, NO full bloom yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the jar down and "
        "opens her hand soft as the first corals begin to bloom and drift, drawing a slow "
        "underwater breath as the camera arcs a few degrees and the aqua backdrop drifts behind "
        "with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising dreamy wonder and a knowing "
        "micro-smile forms, soft corals and sea-flora beginning to grow and bloom around her, "
        "her single face clear and unovergrown, still the aquatic-glow look.",
        "She holds the poised dreamy beat, the first corals unfurling soft, eyes bright and "
        "dreamy \u2014 the hush before the coral-growth bloom (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip coral-growth (NOT her face); first=aquatic-glow, last=coral-bloomed
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the dreamy aquatic-glow "
        "Look A still): she drifts both arms open from her body, already in motion \u2014 still "
        "the aquatic-glow look, NO full bloom yet, a gentle buoyant push-with easing in, the "
        "angle fixed for the whole clip.",
        "The coral-growth bloom BEGINS here, mid-clip: soft corals and sea-flora grow and bloom "
        "in dreamy unfurling arcs around her in one continuous expanding front, coral-pink fans "
        "and aqua sea-flora opening across the water and along her shoulder exactly where the "
        "bloom passes \u2014 believable real coral-growth and botanical physics (polyps and "
        "fronds unfurling on true underwater currents at their own natural pace, no cheap "
        "sparkles), her single face clear and locked (NEVER overgrown, replaced or duplicated), "
        "eyes brightening in dreamy wonder (angle held, identity locked).",
        "The bloom completes and the look settles smoothly and fully into the full coral-bloomed "
        "after-look of the Veo last-frame still (Frame 5's image) \u2014 soft corals and "
        "sea-flora bloomed around her single locked face in the dreamy water-light, resolved and "
        "held through the final beat, no last-second pop; a dreamy radiant calm landing in her "
        "eyes.",
    ),
    # F5 - END coral-bloomed reveal (silent, wordless), new angle, hand to jar
    (
        "Cut to a medium close on a new angle in the dreamy water-light: she is already in the "
        "full coral-bloomed after-look, drifting her right hand soft back toward the Nacre jar "
        "at her collarbone with a buoyant roll of the shoulder, her single face clear and "
        "unovergrown; gaze easing to lens.",
        "A soft dreamy wordless smile eases to lens on a slow underwater breath, the last "
        "sea-flora settling and a bubble drifting, eyes bright and luminous (silent reveal "
        "\u2014 no words).",
        "She holds the dreamy radiant coral-bloomed look, her single face clear, eyes bright and "
        "direct (silent here).",
    ),
    # F6 - loop close, cradle jar matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the sea-glass Nacre jar soft at her collarbone and her left easy near her jaw exactly "
        "as in Frame 1 as the camera settles to the opening framing.",
        "She eases her bright gaze back to lens on a slow underwater breath with the composed "
        "dreamy quarter-smile, the full coral-bloom resolving back toward the opening "
        "aquatic-glow look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, dreamy and buoyant in the water-light "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[42] = [
    # F1 - warm molten-glow hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the warm glassblowing studio: she is already cradling "
        "the hand-blown amber-glass Molten bottle at her collarbone as a slow push eases in, the "
        "deep furnace glow and molten-amber ember light behind her, glowing glass on the bench; "
        "her left hand easy near her jaw.",
        "The push settles as a face-framing strand catches the warm key and her warm gaze eases "
        "to lens, ember light drifting, a quietly assured quarter-smile settling.",
        "She holds the warm molten-glow look in the sculptural bronze-satin top, the satin "
        "catching one molten-amber glint, eyes warm and direct (the line lands later).",
    ),
    # F2 - build, serum glide, first molten orb; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already gliding the liquid-glass serum soft along her cheekbone and a glowing "
        "molten-glass orb begins to gather on the blowpipe beside her; gaze cast soft to the "
        "bottle.",
        "The serum catches a warm molten sheen on her cheekbone as her gaze warms with assured "
        "focus and a knowing micro-smile kindles, the molten orb glowing brighter beside her.",
        "She holds the dropper poised near her cheek, eyes warm and assured, the molten-glow "
        "look intact (silent here).",
    ),
    # F3 - START clean (orb gathering, NO formed artwork yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the dropper down and "
        "opens her hand soft toward the gathering molten-glass orb beside her, drawing a slow "
        "warm breath as the camera arcs a few degrees and the workshop swings behind with "
        "parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising warm assurance and a knowing "
        "micro-smile forms, the glowing molten-glass orb gathering and beginning to flow beside "
        "her, her single face clear and unglassed, still the molten-glow look.",
        "She holds the poised artisanal beat, the molten orb glowing soft beside her, eyes warm "
        "and bright \u2014 the hush before the glass forms (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip glass-form (beside her, NOT her face); first=molten-glow, last=clear-glass-artwork
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the warm molten-glow Look "
        "A still): she holds her molten-glow look, already in motion \u2014 the molten-glass orb "
        "still just glowing beside her, NO formed artwork yet, a gentle push-with easing in, the "
        "angle fixed for the whole clip.",
        "The glass-form BEGINS here, mid-clip: the glowing molten-glass form flows and sculpts "
        "then cools into a clear glass artwork in graceful arcs beside her in one continuous "
        "shaping motion, the molten amber stretching and setting clear exactly where it flows "
        "\u2014 believable real glassblowing physics (true molten-glass viscosity, gather and "
        "stretch, thermal cool from amber-glow to clear with real optical refraction, no cheap "
        "sparkles), her single face clear and locked (NEVER glassed over, replaced or "
        "duplicated), eyes warming in assured wonder (angle held, identity locked).",
        "The form completes and the look settles smoothly and fully into the cooled "
        "clear-glass-artwork after-look of the Veo last-frame still (Frame 5's image) \u2014 a "
        "finished clear glass artwork set beside her single locked face in the warm workshop "
        "glow, resolved and held through the final beat, no last-second pop; a warm assured calm "
        "landing in her eyes.",
    ),
    # F5 - END clear-glass-artwork reveal, hand to bottle, spoken line
    (
        "Cut to a medium close on a new angle in the warm workshop glow: she is already beside "
        "the cooled clear-glass artwork, easing her right hand back toward the amber-glass "
        "bottle at her collarbone with an easy roll of the shoulder, her single face clear and "
        "unglassed; gaze warm to lens.",
        "She delivers \u201cshaped by fire, made to last.\u201d to lens with a quietly assured "
        "smile and natural lip-sync, the clear glass catching a warm ember glint, eyes warm and "
        "assured.",
        "She holds the warm artisanal look, the glass artwork beside her and the bottle cradled "
        "soft, eyes warm and direct.",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the hand-blown amber-glass bottle soft at her collarbone and her left easy near her jaw "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed assured "
        "quarter-smile, the cooled glass artwork resolving back toward the opening molten-glow "
        "look and ember glow to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, warm and assured in the workshop glow "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[43] = [
    # F1 - electric-storm hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the dramatic storm studio: she is already cradling "
        "the storm-gray Volt bottle at her collarbone as a slow push eases in, the dark "
        "charcoal-blue backdrop and a far electric-white lightning flicker behind her, charged "
        "atmosphere; her left hand easy near her jaw.",
        "The push settles as a wind-swept lock lifts in the charged air and her intense gaze "
        "eases to lens, a distant arc flickering, a powerful composed quarter-smile settling.",
        "She holds the electric-storm look in the structured storm-gray power top, the metallic "
        "threading catching one steel glint, eyes intense and direct (the line lands later).",
    ),
    # F2 - build, charged-primer apply, first arc; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already pressing the charged Volt primer high on her cheekbone and the first "
        "electric-white lightning arc crackles to life in the dark around her; gaze cast soft to "
        "the bottle.",
        "The charged primer catches a cool electric sheen on her cheekbone as her gaze sharpens "
        "with powerful focus and a knowing micro-smile kindles, the first arc crackling "
        "brighter.",
        "She holds the primer poised near her cheek, eyes intense and charged, the electric-"
        "storm look intact (silent here).",
    ),
    # F3 - START clean (arcs gathering, NO full crackle yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the bottle down and "
        "opens her hand soft as the first lightning arcs crackle and branch in the dark, drawing "
        "a slow charged breath as the camera arcs a few degrees and the storm backdrop swings "
        "behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising powerful intensity and a knowing "
        "micro-smile forms, electric-white lightning arcs beginning to crackle and branch around "
        "her, her single face clear and unstruck, still the electric-storm look.",
        "She holds the poised powerful beat, the arcs crackling soft around her, eyes intense "
        "and bright \u2014 the hush before the lightning crackle (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip lightning-crackle (NOT her face); first=electric-storm, last=storm-charged
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the electric-storm Look A "
        "still): she holds her storm look, already in motion \u2014 only a far arc flickering, "
        "NO full crackle yet, a gentle push-with easing in, the angle fixed for the whole clip.",
        "The lightning crackle BEGINS here, mid-clip: electric-white lightning arcs crackle and "
        "strike in powerful branching arcs around her in one continuous charged burst, the "
        "plasma arcs branching through the dark air and around her shoulder exactly where they "
        "strike \u2014 believable real lightning physics (true plasma-arc branching, crackle and "
        "afterglow at real speed, no cheap sparkles), her single face clear and locked (NEVER "
        "struck over, replaced or duplicated), eyes intense with powerful awe (angle held, "
        "identity locked).",
        "The crackle completes and the look settles smoothly and fully into the full "
        "storm-charged after-look of the Veo last-frame still (Frame 5's image) \u2014 "
        "electric-white lightning arcs crackling around her single locked face in the dark storm "
        "studio, resolved and held through the final beat, no last-second pop; a powerful "
        "charged calm landing in her eyes.",
    ),
    # F5 - END storm-charged reveal, hand to bottle, spoken line; slow orbit
    (
        "Cut to a medium close on a new angle in the charged dark: she is already in the full "
        "storm-charged look, easing her right hand back toward the Volt bottle at her collarbone "
        "with an easy roll of the shoulder, her single face clear and unstruck; gaze intense to "
        "lens.",
        "She delivers \u201cI am the storm.\u201d to lens with a powerful composed smile and "
        "natural lip-sync, a lightning arc crackling soft around her, eyes intense and charged.",
        "She holds the storm-charged powerful look, her single face locked and the bottle "
        "cradled soft, eyes intense and direct.",
    ),
    # F6 - held powerful, cradling bottle; gentle push
    (
        "Cut to a medium-close chest-up on a fresh angle: she settles both hands gently, the "
        "right cradling the Volt bottle soft near her collarbone, the left easy near her jaw, as "
        "a gentle push eases in; gaze intense to lens.",
        "A powerful composed smile holds to lens on a slow charged breath, the lightning "
        "crackling even around her, electric light on her skin.",
        "She holds the powerful beat, the dark deep and the arcs crackling, eyes intense and "
        "direct \u2014 a held moment before the loop (silent here).",
    ),
    # F7 - loop close, cradle bottle matched to F1; pull-out
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the storm-gray Volt bottle at collarbone height and her left easy near her jaw exactly "
        "as in Frame 1 as a soft pull-out settles to the opening framing.",
        "She eases her intense gaze back to lens on a slow breath with the composed powerful "
        "quarter-smile, the full storm-charge resolving back toward the opening electric-storm "
        "look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, powerful and charged in the storm "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[44] = [
    # F1 - '70s disco-glam hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the '70s disco lounge: she is already cradling the "
        "faceted mirrored-glass Disco bottle at her collarbone as a slow push eases in, the "
        "warm-gold dancefloor and a spinning mirror-ball scattering soft light-shards behind "
        "her, glowing disco haze; her left hand easy near her jaw.",
        "The push settles as a feathered flick bounces in the warm air and her warm gaze eases "
        "to lens, a gold shard drifting across, a playful groovy quarter-smile settling.",
        "She holds the '70s disco-glam look in the gold-sequined mock-neck top, the sequins "
        "catching a thousand warm glints, eyes warm and direct (the line lands later).",
    ),
    # F2 - build, glow-oil glide, first shards; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already gliding the shimmer glow-oil soft along her cheekbone and the first "
        "golden mirror-ball shards begin to scatter across the scene around her; gaze cast soft "
        "to the bottle.",
        "The glow-oil catches a warm golden sheen on her cheekbone as her gaze warms with "
        "playful delight and a knowing micro-smile kindles, more light-shards sweeping in.",
        "She holds the bottle poised near her cheek, eyes warm and groovy, the disco-glam look "
        "intact (silent here).",
    ),
    # F3 - START clean (shards gathering, NO full scatter yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the bottle down and "
        "opens her hand soft as the first golden light-shards sweep and scatter, drawing a slow "
        "warm breath as the camera arcs a few degrees and the dancefloor swings behind with "
        "parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising groovy joy and a knowing "
        "micro-smile forms, the spinning mirror-ball beginning to scatter a swirl of golden "
        "shards across her and the scene, her single face clear and unshard-covered, still the "
        "disco-glam look.",
        "She holds the poised groovy beat, the shards sweeping soft around her, eyes warm and "
        "bright \u2014 the hush before the mirror-ball scatter (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip mirror-ball scatter (NOT her face); first=disco-glam, last=shard-scattered
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the '70s disco-glam Look "
        "A still): she holds her disco look, already in motion \u2014 only a few soft shards "
        "drifting, NO full scatter yet, a gentle push-with easing in, the angle fixed for the "
        "whole clip.",
        "The mirror-ball scatter BEGINS here, mid-clip: the spinning mirror-ball scatters a "
        "swirl of golden light-shards across her and the scene in sweeping arcs in one "
        "continuous turning pattern, bright specular dots travelling across the dancefloor, the "
        "sequins and her shoulder exactly where they sweep \u2014 believable real mirror-ball "
        "optics (a faceted mirror reflecting a real light into moving specular shards at the "
        "ball's true spin-rate, no cheap sparkles), her single face clear and locked (NEVER "
        "shard-covered, replaced or duplicated), eyes warming in groovy delight (angle held, "
        "identity locked).",
        "The scatter completes and the look settles smoothly and fully into the full "
        "shard-scattered after-look of the Veo last-frame still (Frame 5's image) \u2014 a swirl "
        "of golden mirror-ball shards sweeping around her single locked face in the warm disco "
        "lounge, resolved and held through the final beat, no last-second pop; a warm groovy "
        "calm landing in her eyes.",
    ),
    # F5 - END shard-scattered reveal, hand to bottle, spoken line
    (
        "Cut to a medium close on a new angle in the glowing disco haze: she is already in the "
        "full shard-scattered look, easing her right hand back toward the mirrored-glass bottle "
        "at her collarbone with an easy roll of the shoulder, her single face clear and "
        "unshard-covered; gaze warm to lens.",
        "She delivers \u201cborn to shine.\u201d to lens with a playful groovy smile and natural "
        "lip-sync, golden shards sweeping soft across her, eyes warm and shining.",
        "She holds the shard-scattered groovy look, her single face clear and the bottle cradled "
        "soft, eyes warm and direct.",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the faceted mirrored-glass Disco bottle soft at her collarbone and her left easy near "
        "her jaw exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her warm gaze back to lens on a slow breath with the composed groovy "
        "quarter-smile, the full shard-scatter resolving back toward the opening disco-glam look "
        "to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, warm and groovy in the disco lounge "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[45] = [
    # F1 - bubblegum-sweet hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the candy-pop studio: she is already cradling the "
        "glossy pink Bubblegum lip-gloss bottle at her collarbone as a slow push eases in, the "
        "bright bubblegum-pink backdrop and soft pastel-pink bubble bokeh behind her, a sweet "
        "playful air; her left hand easy near her jaw.",
        "The push settles as a glossy bubble-ponytail section bounces and her bright gaze eases "
        "to lens, a translucent pink bubble drifting past, a playful sweet quarter-smile "
        "settling.",
        "She holds the bubblegum-sweet look in the glossy pink mock-neck top, the sheen catching "
        "the bright key, eyes bright and direct (the line lands later).",
    ),
    # F2 - build, lip-gloss swipe, first bubble; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already swiping the plumping Bubblegum gloss soft across her lip and a "
        "translucent bubblegum-pink bubble begins to swell and stretch in the air beside her; "
        "gaze cast soft to the bottle.",
        "The glossy gloss catches a wet bright-pink sheen on her lip as her gaze brightens with "
        "playful sweetness and a knowing micro-smile kindles, the bubble stretching bigger.",
        "She holds the gloss poised near her lip, eyes bright and playful, the bubblegum-sweet "
        "look intact (silent here).",
    ),
    # F3 - START clean (bubble inflating, NO full stretch-and-pop yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the bottle down and "
        "opens her hand soft as the translucent bubblegum bubble inflates and stretches, drawing "
        "a slow sweet breath as the camera arcs a few degrees and the candy backdrop swings "
        "behind with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising playful joy and a knowing "
        "micro-smile forms, the translucent bubblegum-pink bubble stretching and inflating "
        "bigger beside her, her single face clear and unbubble-covered, still the bubblegum-"
        "sweet look.",
        "She holds the poised sweet beat, the bubble stretched taut and glossy, eyes bright and "
        "delighted \u2014 the hush before the bubble pops (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip bubble stretch+pop (NOT her face); first=bubblegum-sweet, last=shimmer-burst
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the bubblegum-sweet Look "
        "A still): she holds her candy look, already in motion \u2014 the bubble only just "
        "swelling, NO full stretch-and-pop yet, a gentle push-with easing in, the angle fixed "
        "for the whole clip.",
        "The bubblegum stretch & pop BEGINS here, mid-clip: a translucent bubblegum-pink bubble "
        "stretches and inflates then pops into a glossy pink shimmer-burst around her in one "
        "continuous motion, the gum membrane ballooning taut then bursting into a soft elastic "
        "shimmer-spray exactly where it pops \u2014 believable real bubblegum physics (true "
        "elastic gum stretch, surface tension, a real pop with elastic snap-back and glossy "
        "spray, no cheap sparkles), her single face clear and locked (NEVER bubble-covered, "
        "replaced or duplicated), eyes bright with playful delight (angle held, identity "
        "locked).",
        "The pop completes and the look settles smoothly and fully into the full shimmer-burst "
        "after-look of the Veo last-frame still (Frame 5's image) \u2014 a glossy pink "
        "shimmer-burst spread around her single locked face in the candy studio, resolved and "
        "held through the final beat, no last-second pop; a bright sweet calm landing in her "
        "eyes.",
    ),
    # F5 - END shimmer-burst reveal, hand to bottle, spoken line
    (
        "Cut to a medium close on a new angle in the candy-pink glow: she is already in the full "
        "shimmer-burst look, easing her right hand back toward the lip-gloss bottle at her "
        "collarbone with an easy roll of the shoulder, her single face clear and "
        "unbubble-covered; gaze bright to lens.",
        "She delivers \u201csweet, but make it iconic.\u201d to lens with a playful sweet smile "
        "and natural lip-sync, the glossy pink shimmer settling soft around her, eyes bright and "
        "delighted.",
        "She holds the shimmer-burst sweet look, her single face clear and the bottle cradled "
        "soft, eyes bright and direct.",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the glossy pink Bubblegum bottle soft at her collarbone and her left easy near her jaw "
        "exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her bright gaze back to lens on a slow breath with the composed sweet "
        "quarter-smile, the glossy shimmer-burst resolving back toward the opening bubblegum-"
        "sweet look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, bright and sweet in the candy studio "
        "\u2014 a seamless loop seam.",
    ),
]


BEATSLM[46] = [
    # F1 - lunar-mystic hero (contained, product-at-face, SILENT), push-in
    (
        "Cut to a medium-close chest-up in the celestial night chamber: she is already cradling "
        "the midnight-blue frosted Eclipse bottle at her collarbone as a slow push eases in, the "
        "deep midnight-blue void and a glowing lunar-eclipse orb with a soft corona behind her, "
        "scattered silver star-glints; her left hand easy near her jaw.",
        "The push settles as a face-framing strand catches the cool moonlight and her calm gaze "
        "eases to lens, a silver star-glint drifting, a serene knowing quarter-smile settling.",
        "She holds the lunar-mystic look in the midnight-blue velvet top, the silver star-threads "
        "catching moonlit glints, eyes calm and luminous (silent reel).",
    ),
    # F2 - build, glow-balm glide, first moonlight; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already gliding the lunar glow-balm soft along her cheekbone and the "
        "lunar-eclipse orb begins to deepen and a first silver corona-light sweeps in around "
        "her; gaze cast soft to the bottle.",
        "The pearl balm catches a cool silver-blue sheen on her cheekbone as her gaze softens "
        "with serene wonder and a knowing micro-smile kindles, the moonlight gathering in.",
        "She holds the balm poised near her cheek, eyes calm and serene, the lunar-mystic look "
        "intact (silent here).",
    ),
    # F3 - START clean (eclipse beginning, NO full sweep yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the bottle down and "
        "opens her hand soft as the eclipse-shadow begins to sweep across the void, drawing a "
        "slow cool breath as the camera arcs a few degrees and the celestial void drifts behind "
        "with parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising serene wonder and a knowing "
        "micro-smile forms, a soft lunar-eclipse shadow beginning to sweep across the scene with "
        "the silver corona just kindling, her single face clear and lit (never shadow-swallowed), "
        "still the lunar-mystic look.",
        "She holds the poised serene beat, the eclipse beginning to sweep, eyes calm and bright "
        "\u2014 the hush before the eclipse-shadow sweep (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip eclipse/moonlight sweep (NOT her face); first=lunar-mystic, last=silver-corona-washed
    (
        "Cut to an ethereal medium at a HELD angle (Veo first frame = the lunar-mystic Look A "
        "still): she holds her lunar look, already in motion \u2014 only the orb deepening, NO "
        "full sweep yet, a gentle push-with easing in, the angle fixed for the whole clip.",
        "The eclipse-shadow light sweep BEGINS here, mid-clip: a soft lunar-eclipse shadow "
        "sweeps across the scene then a silver corona of moonlight sweeps back, washing serene "
        "silver-blue light around her in one continuous travelling wash, the penumbra darkening "
        "the void then the corona-ring lighting it silver exactly where it sweeps \u2014 "
        "believable real eclipse and moonlight physics (true penumbra shadow sweep and "
        "corona-ring light wash, no cheap sparkles), her single face staying clear and LIT "
        "(NEVER shadow-swallowed, replaced or duplicated), eyes calm with serene wonder (angle "
        "held, identity locked).",
        "The sweep completes and the look settles smoothly and fully into the full "
        "silver-corona-washed after-look of the Veo last-frame still (Frame 5's image) \u2014 "
        "serene silver-blue moonlight washed around her single lit face under the corona-ringed "
        "eclipse, resolved and held through the final beat, no last-second pop; a serene cool "
        "calm landing in her eyes.",
    ),
    # F5 - END silver-corona-washed reveal (silent, wordless), new angle, hand to bottle
    (
        "Cut to a medium close on a new angle in the silver moonlight: she is already in the "
        "full silver-corona-washed look, drifting her right hand soft back toward the Eclipse "
        "bottle at her collarbone with an easy roll of the shoulder, her single face clear and "
        "lit; gaze easing to lens.",
        "A serene knowing wordless smile eases to lens on a slow cool breath, the silver corona "
        "glowing soft around her, eyes calm and luminous (silent reveal \u2014 no words).",
        "She holds the serene moonlit look, her single face lit and clear, eyes calm and direct "
        "(silent here).",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the midnight-blue frosted Eclipse bottle soft at her collarbone and her left easy near "
        "her jaw exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her calm gaze back to lens on a slow cool breath with the composed serene "
        "quarter-smile, the silver-corona wash resolving back toward the opening lunar-mystic "
        "look to seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, serene in the celestial night \u2014 "
        "a seamless loop seam.",
    ),
]


BEATSLM[47] = [
    # F1 - fluid-art hero (contained, product-at-face), push-in
    (
        "Cut to a medium-close chest-up in the fluid-art studio: she is already cradling the "
        "clear cylindrical Fluid Art pigment bottle at her collarbone as a slow push eases in, "
        "the sleek charcoal-to-deep-teal backdrop and glossy poured surface behind her, soft "
        "galaxy paint ribbons drifting; her left hand easy near her jaw.",
        "The push settles as a finger-wave catches the cool key and her deep gaze eases to lens, "
        "a galaxy ribbon swirling past, a mesmerized knowing quarter-smile settling.",
        "She holds the fluid-art look in the iridescent deep-teal top, the sheen shifting "
        "teal-to-purple, eyes deep and luminous (the line lands later).",
    ),
    # F2 - build, pigment glide, first ribbon; rack-focus product->eye
    (
        "Cut to a medium-close three-quarter, a rack-focus pulling from the bottle to her eye: "
        "she is already gliding the liquid pigment soft along her cheekbone and the first glossy "
        "galaxy paint ribbon begins to pour and swirl through the air beside her; gaze cast soft "
        "to the bottle.",
        "The pigment catches a jewel-tone sheen on her cheekbone as her gaze deepens with "
        "mesmerized focus and a knowing micro-smile kindles, more paint ribbons swirling in.",
        "She holds the bottle poised near her cheek, eyes deep and mesmerized, the fluid-art "
        "look intact (silent here).",
    ),
    # F3 - START clean (ribbons gathering, NO full swirl yet), slow arc
    (
        "Cut to a medium chest-up on a fresh three-quarter angle: she eases the bottle down and "
        "opens her hand soft as the first galaxy paint ribbons pour and swirl, drawing a slow "
        "breath as the camera arcs a few degrees and the glossy studio swings behind with "
        "parallax; gaze lifting.",
        "The arc settles as her gaze lifts to lens with rising mesmerized calm and a knowing "
        "micro-smile forms, glossy galaxy-toned paint ribbons beginning to pour and swirl in "
        "marbled arcs around her, her single face clear and unpaint-covered, still the fluid-art "
        "look.",
        "She holds the poised mesmerized beat, the ribbons swirling soft around her, eyes deep "
        "and bright \u2014 the hush before the paint-pour swirl (silent here).",
    ),
    # F4 - THE TRANSFORM, HELD ANGLE, smooth mid-clip paint-pour swirl (NOT her face); first=fluid-art, last=paint-swirled
    (
        "Cut to an energized medium at a HELD angle (Veo first frame = the fluid-art Look A "
        "still): she holds her fluid-art look, already in motion \u2014 only a few soft ribbons "
        "drifting, NO full swirl yet, a gentle push-with easing in, the angle fixed for the "
        "whole clip.",
        "The galaxy paint-pour swirl BEGINS here, mid-clip: glossy galaxy-toned paint ribbons "
        "pour and swirl through the air in mesmerizing marbled arcs around her in one continuous "
        "flowing pour, cosmic blue, purple and teal with gold veins marbling through the air and "
        "around her shoulder exactly where they pour \u2014 believable real fluid paint-pour "
        "physics (true viscous marbling, ribbon flow and surface tension, gold flecks suspended "
        "in the swirl, no cheap sparkles), her single face clear and locked (NEVER paint-"
        "covered, replaced or duplicated), eyes deep with mesmerized wonder (angle held, "
        "identity locked).",
        "The swirl completes and the look settles smoothly and fully into the full paint-swirled "
        "after-look of the Veo last-frame still (Frame 5's image) \u2014 glossy marbled galaxy "
        "paint ribbons swirling around her single locked face in the jewel-tone studio, resolved "
        "and held through the final beat, no last-second pop; a deep mesmerized calm landing in "
        "her eyes.",
    ),
    # F5 - END paint-swirled reveal, hand to bottle, spoken line
    (
        "Cut to a medium close on a new angle in the glossy jewel-tone haze: she is already in "
        "the full paint-swirled look, easing her right hand back toward the pigment bottle at "
        "her collarbone with an easy roll of the shoulder, her single face clear and unpaint-"
        "covered; gaze deep to lens.",
        "She delivers \u201cI'm a work of art.\u201d to lens with a mesmerized knowing smile and "
        "natural lip-sync, the marbled ribbons swirling soft around her, eyes deep and "
        "luminous.",
        "She holds the paint-swirled mesmerizing look, her single face clear and the bottle "
        "cradled soft, eyes deep and direct.",
    ),
    # F6 - loop close, cradle bottle matched to F1
    (
        "Cut to a medium-close chest-up matched to Frame 1: she returns her right hand to cradle "
        "the clear cylindrical Fluid Art pigment bottle soft at her collarbone and her left easy "
        "near her jaw exactly as in Frame 1 as the camera settles to the opening framing.",
        "She eases her deep gaze back to lens on a slow breath with the composed mesmerized "
        "quarter-smile, the full paint-swirl resolving back toward the opening fluid-art look to "
        "seed the loop.",
        "She lands precisely on the Frame 1 pose and gaze, deep and mesmerized in the fluid-art "
        "studio \u2014 a seamless loop seam.",
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

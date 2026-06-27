#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic advanced video-prompt rebuild engine for the Beauty-Ad markdown format
(used by the Set 5 continuation files, concepts 79-84, all SILENT).

Same transform as set4/set5 engines, but the file PATH is passed as argv[1] so
one engine can serve several files. Per VIDEO prompt in a concept region:
  - delete the standalone `CAMERA MOVEMENT:` line,
  - replace `SUBJECT ACTION WITH TIMING` with a tailored timed 3-beat
    `SHOT BREAKDOWN`,
  - reset the `DURATION:` and `FRAME RATE + MOTION BLUR:` lines to the 6s
    standard.

All concepts here are silent: wordless expression reveal, no spoken line.

Idempotent. Usage:  python3 _tools/md_rebuild.py "<path>" <concept_number>
"""
import re
import sys

BREAKDOWN_HEADER = (
    "SHOT BREAKDOWN (timed, 6s \u00b7 real-time, continuous energetic motion "
    "\u2014 never slow-motion, never a static hold; expression eye-led and "
    "identity-safe):"
)
FRAME_RATE_LINE = (
    "FRAME RATE + MOTION BLUR: 24fps, real-time playback at natural speed "
    "(no slow-motion), 180\u00b0 shutter, natural motion blur."
)
DURATION_LINE = (
    "DURATION: 6 seconds (the clip plays the full 6s at real-time natural speed)."
)

BEATS = {}

BEATS[79] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "faceted prism bottle a few degrees into the key, the cut glass splitting a clean "
        "rainbow fan across her collarbone and the pearlescent liquid settling inside; gaze "
        "lowered to the glass.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a knowing "
        "asymmetric quarter-smile blooms, a refraction spark crossing her cheek.",
        "She holds, iridescent and composed, one brow a hair higher and a tiny rainbow "
        "flickering in her catchlight, eyes bright and direct (silent \u2014 no words).",
    ),
    # F2 - medium waist-up TRANSFORM (6deg arc camera-left, oil-slick swirl -> prism gown)
    (
        "Medium waist-up easing wider: a slow 6\u00b0 arc camera-left is already tracking the "
        "swirl as a ribbon of iridescent oil-slick foil pours from her shoulders and begins "
        "to spiral the torso, her right hand lifting into the pour; gaze following the foil.",
        "The arc rides the wrap as the foil spirals her body in one continuous turn, "
        "petrol-rainbow racing across its surface and her hips counter-rotating; a wondering "
        "breath, brows lifting.",
        "The leading edge crystallises and facets into the structured holographic prism gown, "
        "micro shards spinning off and catching light as she settles into the new silhouette, "
        "eyes lifting to lens with wonder.",
    ),
    # F3 - macro/tight insert on bottle, rack-focus (eyes->drop) + creep
    (
        "Macro tight insert on the hero bottle with her face soft behind: a precise "
        "rack-focus is already pulling from her defocused eyes down to the dropper tip on a "
        "4% creep-in as a single pearlescent rainbow drop swells and trembles at the tip.",
        "Focus holds tight on the tip as the drop releases and falls a short clean arc, "
        "splitting the key into a brief rainbow flare as it goes.",
        "Her lips ease into a knowing micro-smile in the soft background, gaze warming behind "
        "the falling drop.",
    ),
    # F4 - wide-medium near full-length, vertical tilt-up (heel->face) + creep
    (
        "Wide-medium near full-length: a slow vertical tilt-up paired with a 4% creep-in is "
        "already reading the lucite prism-heel sandal as she shifts her weight and turns the "
        "front foot out, internal rainbows flaring in the heel and a caustic sliding on the "
        "floor.",
        "The tilt rises past the chrome cuff and prism-drop earring as her hand settles on "
        "the hip, the gown catching travelling spectra; gaze beginning to lift.",
        "The tilt lands on her face as she meets the lens with a cool micro-smile, weight "
        "grounded, eyes direct and composed.",
    ),
    # F5 - tight beauty close-up (3% push)
    (
        "Tight beauty close-up, face filling the frame: an almost-imperceptible 3% push is "
        "already breathing in as she brushes her fingertips softly at the jaw on a slow "
        "serene exhale, lashes lowering.",
        "Her eyes lift to a soft direct gaze as a quiet confident half-smile blooms and a "
        "rainbow refraction streak drifts across the cheekbone.",
        "The half-smile holds, gentle and present, eyes luminous and direct to lens.",
    ),
    # F6 - medium-wide MAGIC, 3D orbit + rise (spectrum-burst)
    (
        "Medium-wide waist-up with headroom: a graphic slow 15\u00b0 3D orbit with a slight "
        "rise is already arcing around the bottle as it lifts off her palm to hover and "
        "rotate, she opening her hands beneath it; gaze drawn to the rising prism.",
        "The orbit rides the burst as the key strikes the rotating prism and detonates a "
        "360\u00b0 radial spectrum-burst, faceted shards spiralling into orbit and beams "
        "sweeping the studio; her face lifting into luminous awe.",
        "The burst holds at full bloom and begins a gentle settle as shards drift and the "
        "orbit eases; a radiant almost-smile breaking, eyes alight.",
    ),
    # F7 - perfect-loop close (orbit eases to rest, 2% drift, match F1)
    (
        "Medium close chest-up resolving to match Frame 1: the orbit is already easing to "
        "rest on a barely-perceptible 2% drift-in as the last prism-shards drift down and "
        "dissolve and the hovering bottle settles back into her cradling hand at collarbone "
        "height, the gown resolving to liquid-chrome.",
        "The drift settles as she eases into the exact opening pose and expression, one final "
        "soft rainbow fan splitting across the collarbone; eyes calming.",
        "She holds still on the knowing quarter-smile, framing locked to the Frame 1 "
        "composition \u2014 a seamless loop seam.",
    ),
]


BEATS[80] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "cobalt bottle a few degrees into the key, specular glints sliding along the glass "
        "and the clear oil settling inside; gaze lowered to the glass.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a knowing "
        "asymmetric quarter-smile blooms, the cobalt-and-marigold colour-block crisp behind.",
        "She holds, bold and composed, one brow a hair higher, eyes bright and direct "
        "(silent \u2014 no words).",
    ),
    # F2 - medium waist-up TRANSFORM (6% push + 4deg arc, thermochromic colour-shift)
    (
        "Medium waist-up: a slow 6% push paired with a gentle 4\u00b0 arc is already following "
        "the colour-front as a warm heat-bloom ignites at her shoulder and a clean diagonal "
        "colour-shift begins sweeping the gown, cobalt blooming into marigold; gaze tracking "
        "the front.",
        "The move rides the wave fully across the torso as she lifts a spread hand to trail "
        "it and the silhouette re-sculpts, the shoulder sharpening and a peplum forming; eyes "
        "widening in wonder.",
        "The colour sets fully marigold-and-cobalt and one last specular ribbon races down "
        "the new seam as the look locks; her chin lifting a degree as the bloom settles.",
    ),
    # F3 - macro product, 5% macro push + rack-focus (label->wrist bloom)
    (
        "Macro product, bottle and wrist swatch filling the upper frame: a slow 5% macro "
        "push with a tiny rack-focus is already underway as the dropper releases one clear "
        "bead onto the inner wrist, surface tension holding then breaking as it touches "
        "skin.",
        "The oil blooms outward into a vivid marigold-coral swatch as the rack-focus pulls "
        "from the label to the bloom and a soft specular travels the cobalt glass.",
        "The swatch settles rich on the wrist, the bottle soft behind, the colour vivid and "
        "controlled.",
    ),
    # F4 - full-length low angle, vertical tilt-up (heels->face) + 4% push
    (
        "Full-length three-quarter low angle: a slow vertical tilt-up with a gentle 4% push "
        "is already travelling up from the marigold heels as she rolls her weight onto the "
        "platform, the cobalt sole-flash catching light.",
        "The tilt rises as her hand settles on the peplum and the gown catches travelling "
        "light; gaze beginning to lift on a confident under-look.",
        "The tilt lands on her face as she meets the lens, a cool quarter-smile blooming, "
        "weight grounded and balanced.",
    ),
    # F5 - medium-wide MAGIC, 5% pull-back (concentric colour-pulse rings)
    (
        "Medium-wide with raised arms: a slow steady 5% pull-back is already revealing the "
        "space as she raises the cobalt bottle and the first radial colour-pulse detonates "
        "outward in a clean cobalt-marigold ring; gaze lifting to the ring.",
        "The pull-back rides the burst as successive concentric shockwave rings expand at "
        "constant speed, re-painting the studio as they pass and her free hand lifting "
        "palm-out to feel them; eyes widening in awe.",
        "The rings reach the frame edge and dissipate into pinprick motes as the pull-back "
        "eases; her confident half-smile locking, eyes alight.",
    ),
    # F6 - perfect-loop close (8% push-in to F1)
    (
        "Medium close chest-up matching Frame 1: a slow 8% push-in is already settling toward "
        "the exact opening framing as the last colour-pulse mote fades behind her; she "
        "cradles the cobalt bottle back to collarbone height, the clear oil settling inside.",
        "The push settles as she holds the knowing asymmetric quarter-smile direct to lens "
        "on a soft held breath, the studio returning to its opening calm; eyes calming.",
        "Every element resolves to the Frame 1 pose, framing locked for an invisible cut "
        "\u2014 a seamless loop seam.",
    ),
    # F7 - stray duplicate Frame-1 block at file end (kept consistent with F1)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "cobalt bottle a few degrees into the key, specular glints sliding along the glass "
        "and the clear oil settling inside; gaze lowered to the glass.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a knowing "
        "asymmetric quarter-smile blooms, the cobalt-and-marigold colour-block crisp behind.",
        "She holds, bold and composed, one brow a hair higher, eyes bright and direct "
        "(silent \u2014 no words).",
    ),
]


BEATS[81] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "clear orb jar a few degrees into the key, the magenta jelly wobbling and internal "
        "glints sliding across the dome; gaze lowered to the jar.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a knowing "
        "asymmetric quarter-smile blooms, a lava-lamp blob rising lazily behind.",
        "She holds, playful and glossy, one brow a hair higher, eyes bright and direct "
        "(silent \u2014 no words).",
    ),
    # F2 - medium waist-up TRANSFORM (6% crane lift, blobs rise/merge -> blob-form gown)
    (
        "Medium waist-up rising: a slow 6% craning lift is already tracking the rising blobs "
        "as glossy candy globes float up around her body, magenta, lime and tangerine "
        "wobbling with believable surface tension; gaze following the floating blobs, face "
        "delighted.",
        "The lift rides the merge as the blobs join around her torso into a single marbled "
        "sheet and the leading edge sets into the sculpted blob-form gown; a wondering "
        "breath, brows lifting.",
        "The gown finishes with a final glossy ripple and a small blob pinches off and "
        "wobbles free as her shoulders settle and she lifts her chin into the reveal.",
    ),
    # F3 - extreme macro, 5% rack-focus pull (label->face)
    (
        "Extreme macro on the domed orb jar with her soft presence behind: a slow 5% "
        "rack-focus pull is already underway as the magenta jelly trembles mid-wobble inside "
        "the dome and a specular slides across the curve, her fingertips feather-light on "
        "the lime base.",
        "The rack-focus pulls from the crisp label window back toward her soft delighted face "
        "as the candy bokeh blooms; gaze warming behind the jar.",
        "The jelly settles with a hairline ripple, her face soft and pleased in focus, eyes "
        "bright.",
    ),
    # F4 - low 3/4 body, 6% pan up (jelly mule -> bangled wrist)
    (
        "Low three-quarter body down the leg-and-wrist line: a slow 6% pan up is already "
        "travelling from the jelly mule as she pushes the leg forward and rotates the ankle, "
        "the translucent platform catching candy light and the lime sole flashing a "
        "specular.",
        "The pan rises up the body line as she lifts and rotates the bangled wrist into "
        "frame, the candy-resin stack rocking and the pendant swinging; gaze glancing down "
        "the line.",
        "She lands a pleased quarter-smile glancing down the body, weight grounded, the "
        "accessories settling.",
    ),
    # F5 - full-length, 7% arc (twirl -> power-pose)
    (
        "Full-length: a slow 7% arc is already following her as she sweeps one arm overhead "
        "and begins a confident quarter-twirl, the gown skirt and glossy flip swinging out "
        "and bangles sliding down the forearm; gaze leading the turn.",
        "The arc rides the twirl through its sweep, the candy gown flaring and the lava-lamp "
        "blobs rising fast behind; eyes bright and alive.",
        "She lands the power-pose facing lens with a bright open smile, the skirt and hoops "
        "settling, eyes sparkling.",
    ),
    # F6 - medium-full MAGIC, 8% orbital arc (candy mitosis -> orbital rings)
    (
        "Medium-full with the orbital rings filling the width: a slow 8% orbital arc is "
        "already circling her as she raises her open palms and the hovering candy blobs defy "
        "gravity, a larger globe pinching and splitting into two in clean candy mitosis; "
        "gaze drawn to the split.",
        "The orbit rides the magic as the split globes arc into two concentric orbital rings "
        "circling her like planets, each trailing a glossy comet-sheen; her face "
        "serene-radiant at the centre, eyes widening.",
        "The rings settle into a steady glowing orbit with a final small blob wobbling at the "
        "apex as she holds the transcendent pose; a radiant smile landing, eyes alight.",
    ),
    # F7 - perfect-loop close (8% push-in to F1)
    (
        "Medium close chest-up matching Frame 1: a slow 8% push-in is already resolving "
        "toward the exact opening framing as the last orbiting candy blob settles softly to "
        "the floor; she lowers her gaze to the hero jar and tilts it, the magenta jelly "
        "rocking gently inside.",
        "The push settles as she lifts her eyes back to lens on a soft exhale with a composed "
        "knowing quarter-smile, the scene resolving to the opening tableau; eyes calming.",
        "Every element resolves precisely to the Frame 1 composition, framing locked \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[82] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "clear orb a few degrees into the key, the electric-violet oil wobbling and the "
        "filament core crackling, glints sliding across the glass; gaze lowered to the orb.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a knowing "
        "asymmetric quarter-smile blooms, a plasma arc branching slowly behind on the gloss "
        "black.",
        "She holds, charged and composed, one brow a hair higher, eyes bright and direct "
        "(silent \u2014 no words).",
    ),
    # F2 - medium waist-up TRANSFORM (6% crane lift, plasma filaments weave + chrome sets gown)
    (
        "Medium waist-up rising: a slow 6% craning lift is already tracking the arcing "
        "filaments as crackling plasma threads race up around her body in glowing electric "
        "lines, magenta and cyan lacing the air; gaze following the racing filaments, face "
        "charged.",
        "The lift rides the weave as the threads lattice her torso and liquid chrome flows in "
        "to set around them, the leading edge solidifying into the sculptural gown; a "
        "wondering breath, brows lifting.",
        "The gown finishes with a final electric pulse and a single spark arcs free as her "
        "shoulders settle and she lifts her chin into the reveal.",
    ),
    # F3 - extreme macro, 5% rack-focus pull (label->face)
    (
        "Extreme macro on the glass orb with her soft presence behind: a slow 5% rack-focus "
        "pull is already underway as the filament core crackles and a tiny plasma thread "
        "licks the inner glass, a specular sliding across the curve and her fingertips "
        "feather-light on the chrome cap.",
        "The rack-focus pulls from the crisp label window back toward her soft charged face "
        "as the electric bokeh blooms; gaze warming behind the orb.",
        "The oil settles with a faint internal current, her face soft and charged in focus, "
        "eyes bright.",
    ),
    # F4 - low 3/4 body, 6% pan up (boot -> cuffed wrist)
    (
        "Low three-quarter body down the leg-and-wrist line: a slow 6% pan up is already "
        "travelling from the illuminated boot as she pushes the leg forward and rotates the "
        "ankle, the clear platform catching electric light and the cyan core glowing "
        "brighter, casting a wash at the floor.",
        "The pan rises up the body line as she lifts and rotates the cuffed wrist into frame, "
        "the chrome stack rocking with plasma threads arcing across the gaps and the choker "
        "pulsing; gaze glancing down the line.",
        "She lands a pleased quarter-smile glancing down the body, weight grounded, the "
        "plasma accessories settling.",
    ),
    # F5 - medium-full MAGIC, 8% orbital arc (plasma helixes)
    (
        "Medium-full with the orbital helixes filling the width: a slow 8% orbital arc is "
        "already circling her as she raises her open palms and ribbons of live plasma stream "
        "from her fingertips, coiling and branching in mid-air in defiance of gravity; gaze "
        "drawn to the dancing filaments.",
        "The orbit rides the magic as the filaments sweep into two spiralling orbital "
        "helixes circling her like captured lightning, each trailing a glowing comet-glow; "
        "her face serene-radiant at the centre, eyes widening.",
        "The helixes settle into a steady glowing orbit with a final spark shedding free at "
        "the apex as she holds the transcendent pose; a radiant smile landing, eyes alight.",
    ),
    # F6 - perfect-loop close (8% push-in to F1)
    (
        "Medium close chest-up matching Frame 1: a slow 8% push-in is already resolving "
        "toward the exact opening framing as the last orbiting plasma filament fades into a "
        "drifting arc; she lowers her gaze to the hero orb and tilts it, the electric-violet "
        "oil rocking gently and the core crackling soft.",
        "The push settles as she lifts her eyes back to lens on a soft exhale with a composed "
        "knowing quarter-smile, the scene resolving to the opening tableau; eyes calming.",
        "Every element resolves precisely to the Frame 1 composition, framing locked \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[83] = [
    # F1 - HOOK / opening Look A (Voltage Tangerine), 6% push-in rising
    (
        "Medium close rising to medium: a slow 6% push-in is already gliding in as she holds "
        "a confident freeze in the Voltage Tangerine look, eyes locked to lens with a "
        "knowing quarter-smile, the Prism clutch glinting at her hip and baby-hair drifting.",
        "The push continues as she raises her hand and lands a crisp finger-snap, chin "
        "tipping a degree as the studio light pulses on the click \u2014 the trigger for the "
        "first change; gaze sharp on lens.",
        "She holds the post-snap beat, eyes bright and direct, the tangerine seamless crisp "
        "behind (silent \u2014 no words).",
    ),
    # F2 - CHANGE 1 spin-blur snap-change A->B, 5% whip-pan
    (
        "Medium waist-up: off the snap a 5% whip-pan is already following her into a fast "
        "180\u00b0 whip-spin, the tangerine look streaking into motion-blur; gaze sweeping "
        "with the turn.",
        "At the blur-peak the wardrobe, footwear, accessories, hair and makeup-accent all "
        "flip from Look A to the Liquid Cyan look, the seamless re-gelling tangerine to cyan "
        "(face pin-locked); eyes alive through the spin.",
        "She resolves out of the spin facing lens in the liquid-sequin gown, the gown and "
        "chokers settling and the clutch landing at her hip with a glint; a cool composed "
        "look arriving.",
    ),
    # F3 - Look B movement (Liquid Cyan), 5% push settling
    (
        "Medium-full: a slow 5% push-in is already settling on the hip-led pose as the "
        "liquid-sequin gown ripples a light-wave and stills, the clutch easing forward; gaze "
        "level.",
        "The push settles as she lifts her gaze to lens with a cool composed quarter-smile "
        "and the cyan crystal drops settle; a final sequin shimmer travelling the gown.",
        "She holds the composed cyan pose, eyes bright and direct, the gown glittering "
        "softly.",
    ),
    # F4 - CHANGE 2 split-flap flip-board cascade B->C, 5% push steady
    (
        "Medium-full: a steady 5% push holds as she lifts a conducting hand and a wave of "
        "glossy split-flap panels is already rippling down from her shoulders; gaze tracking "
        "the cascade.",
        "The panels flip top-to-bottom in a clean cascade, the wardrobe, footwear, "
        "accessories, hair and makeup-accent locking from cyan into the Ultraviolet Latex "
        "look (face pin-locked, panels never crossing the face), the seamless re-gelling "
        "cyan to ultraviolet.",
        "The final lower row flips and the magenta boots lock as she settles into a "
        "confident planted stance, the look completing; eyes sharpening.",
    ),
    # F5 - Look C power pose (Ultraviolet Latex), 5% push settling
    (
        "Medium-full: a slow 5% push-in is already settling as she snaps into the wide power "
        "stance, the latex catching a hard specular-slide and the clutch angling sharp; gaze "
        "driving to lens.",
        "The push settles as she locks a fierce gaze to lens, one brow lifting in challenge "
        "and the bangles settling; a final ultraviolet sheen travelling the shoulder-line.",
        "She holds the fierce power pose, eyes bold and direct, the latex glinting.",
    ),
    # F6 - CHANGE 3 MAGIC light-ribbon bloom C->D, 6% rise-with-the-bloom
    (
        "Medium-full: a slow 6% crane-rise is already following the bloom as she lifts an arm "
        "and the first gold light-ribbons spiral up from the floor; gaze lifting with the "
        "ribbons.",
        "The crane rides the bloom as the ribbons wrap the ultraviolet away and resolve the "
        "molten-gold gown, footwear, accessories, hair and makeup-accent (face pin-locked, "
        "ribbons never crossing the face), gold sparks suspending, the seamless re-gelling "
        "to gold; eyes widening in awe.",
        "The last ribbons settle into the draped gold gown as she rises onto the balls of "
        "her feet into the finished finale glow; a radiant awe landing.",
    ),
    # F7 - Look D finale hero (Molten Gold), 5% push settling
    (
        "Medium-full: a slow 5% push-in is already settling on the finale as she settles the "
        "tall hero stance, the gold gown catching a molten specular-slide and the clutch "
        "rising into the triumphant hero-line; gaze lifting to lens.",
        "The push settles as a radiant confident smile blooms to lens, both brows lifting in "
        "triumph and the gold earrings settling; a final molten sheen travelling the gown.",
        "She holds the triumphant hero pose, eyes radiant and direct, the gold gown "
        "luminous.",
    ),
    # F8 - perfect-loop close, snap back to Look A, fast 5% whip-settle
    (
        "Medium waist-up matching Frame 1: a fast 5% whip-settle is already resolving toward "
        "the exact opening framing as the gold finale whip-flashes back into the Voltage "
        "Tangerine look in a single quick motion-blur (face pin-locked); gaze snapping to "
        "lens.",
        "The whip-settle lands as she resolves onto the exact Frame 1 stance, expression and "
        "clutch position, the tangerine look fully matched; eyes settling bright.",
        "She holds precisely on the Frame 1 beat, framing locked so the next loop continues "
        "invisibly \u2014 a seamless loop seam.",
    ),
]


BEATS[84] = [
    # F1 - HOOK / opening Look A (Electric Lime), 6% push-in rising
    (
        "Medium close rising to medium: a slow 6% push-in is already gliding in as she holds "
        "a confident freeze in the electric-lime mod look, eyes locked to lens with a "
        "knowing quarter-smile, the Halo cuff glinting on her wrist and baby-hair drifting.",
        "The push continues as she curls one finger in a playful come-here beckon, chin "
        "tipping a degree as the studio light pulses on the gesture \u2014 the trigger for "
        "the first change; gaze bright on lens.",
        "She holds the post-beckon beat, eyes playful and direct, the lime seamless crisp "
        "behind (silent \u2014 no words).",
    ),
    # F2 - CHANGE 1 magnetic-panel snap-on A->B, 5% push steady through converge
    (
        "Medium-full: a steady 5% push holds as off the beckon the electric-lime look "
        "releases and the first fuchsia panels are already streaking in from the frame "
        "edges; gaze tracking the converging panels.",
        "The panels, marabou, footwear, accessories, hair and makeup-accent all fly in and "
        "snap together magnetically onto her body assembling the Fuchsia Bloom look (face "
        "pin-locked, nothing crossing the face), the seamless re-gelling lime to fuchsia.",
        "The final marabou hem-pieces lock as she settles into a confident stance, the look "
        "completing; a delighted set arriving in her eyes.",
    ),
    # F3 - Look B movement (Fuchsia Bloom), slow arc following the turn
    (
        "Medium to medium-full: a smooth slow arc is already following her as she sweeps one "
        "arm out and begins a confident turn, the fuchsia hem and feather trim flaring and "
        "earrings swinging; gaze leading the turn.",
        "The arc rides the turn as she comes back to camera, the marabou and waves easing to "
        "rest; a bright delighted smile blooming.",
        "She settles into a poised stance facing lens, eyes warm and sparkling, the feather "
        "trim stilling.",
    ),
    # F4 - CHANGE 2 zipper-of-light unzip-reveal B->C (MAGIC), 5% push steady
    (
        "Full-length to medium-full: a steady 5% push holds as a brilliant vertical "
        "light-zipper is already materialising at the hem and the fuchsia begins to part; "
        "gaze drawn to the rising seam.",
        "The seam unzips smoothly upward, the fuchsia peeling away to the sides as the "
        "liquid-chrome gown spills out and resolves behind it, footwear, accessories, hair "
        "and makeup-accent transforming in its wake (face pin-locked, the seam never "
        "crossing the face), the seamless cooling fuchsia toward chrome; eyes widening in "
        "wonder.",
        "The seam completes at the shoulder and dissolves in a soft bloom as she settles "
        "into a poised chrome stance, the Mirror look fully revealed; a serene awe landing.",
    ),
    # F5 - Look C finale hero (Chrome Mirror), 6% push-in
    (
        "Medium-full to full: a slow 6% push-in is already gliding in as she holds the "
        "chrome finale power-pose, chin lifted, the gown settling and mirror-discs throwing "
        "roving light, the Halo cuff glinting; gaze level to lens.",
        "The push continues as she lifts her raised hand a touch and the serene quarter-smile "
        "blooms, a cool light-pulse riding across the chrome.",
        "She holds the chrome power-pose, eyes cool and luminous, mirror-discs glinting.",
    ),
    # F6 - Look C strut/turn (Chrome Mirror), slow arc tracking the pivot
    (
        "Medium-full to full: a smooth slow arc is already tracking her as she steps into a "
        "confident strut and begins a pivot, the chrome gown swinging out in a mirror-arc, "
        "earrings swinging and cuff leading; gaze sweeping with the turn.",
        "The arc rides the pivot as she cuts her eyes back to lens and settles the turn into "
        "a poised stance, the gown easing to rest; a commanding half-smile arriving.",
        "She holds the commanding stance, eyes bold and direct, the chrome gown stilling.",
    ),
    # F7 - perfect-loop close, mirror snap-back to Look A, quick settle
    (
        "Medium close rising to medium, matching Frame 1: a quick settle is already resolving "
        "toward the exact opening framing as the chrome look snap-collapses in a mirror-glint "
        "burst and the electric-lime mod look snaps back on, the seamless re-gelling lime; "
        "gaze snapping to lens.",
        "The settle lands as she re-locks into the exact opening pose with the raised-finger "
        "beckon and knowing quarter-smile; eyes settling bright.",
        "She holds the freeze precisely on the Frame 1 beat, framing locked so the reel "
        "loops seamlessly back \u2014 a seamless loop seam.",
    ),
]


BEATS[31] = [
    # F1 - medium close chest-up (8% push)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "faceted amber-gold bottle a few degrees into the candle key, warm gold speculars "
        "sliding along the glass and the liquid-gold oil settling; gaze lowered to the "
        "bottle, candlelit chiaroscuro deep behind.",
        "The push continues as she lifts her warm gaze to lens on a soft inhale and an "
        "opulent quarter-smile blooms, a single gold-leaf flake drifting in the warm shaft.",
        "She holds, regal and warm, one brow a hair higher, eyes catching the candle "
        "catchlight (silent here).",
    ),
    # F2 - medium close, push + 3deg tilt-up following the gold drop
    (
        "Medium close: the slow push continues with a faint 3\u00b0 tilt-up already following "
        "her hand as she lifts the dropper near her cheekbone and releases a single warm "
        "liquid-gold drop; gaze tracing the falling drop.",
        "The tilt rides the drop down as the first gold-leaf flakes catch light in the air, "
        "her eyes warming with anticipation.",
        "The drop meets her skin with a soft gilded sheen, lashes lowering, a quiet opulent "
        "focus holding.",
    ),
    # F3 - medium, 6% push tracking the gathering flakes
    (
        "Medium chest-up: a slow push is already tracking the gathering gold-leaf flakes as "
        "she lowers the dropper a touch and they begin to swirl around her; gaze following "
        "the drifting gold.",
        "The push holds as the suspended flakes catch rotating warm glints, her eyes warming "
        "with anticipation.",
        "The gathering tightens and brightens, cueing the sweep, her gaze lifting a degree "
        "in expectation.",
    ),
    # F4 - energized medium-wide, push easing into gentle orbit (gilding sweep hero)
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "suspended gold-leaf flakes sweep across her skin in warm arcs and she opens her "
        "arms; gaze lifting into the sweep.",
        "The orbit rides the hero beat as a sweeping gold shimmer races across her and the "
        "velvet and chignon catch travelling gold light (face clear, framed by the sweep); "
        "eyes widening in opulent awe.",
        "The sweep settles and the gilding resolves as the orbit eases; a radiant regal "
        "look landing, eyes alight with warm gold.",
    ),
    # F5 - medium close, 6% push (SPOKEN)
    (
        "Medium close chest-up: a slow push is already gliding in as she eases her hands open "
        "and the gilding settles, the last flakes drifting; gaze warm to lens.",
        "She delivers \u201cworth its weight in gold.\u201d to lens with a soft knowing "
        "opulent smile, eyes warm and direct.",
        "She holds the radiant regal look as one final flake settles, the smile easing into "
        "calm warmth.",
    ),
    # F6 - medium close, 6% push (regal hold, no words)
    (
        "Medium close chest-up: a slow push is already gliding in as she settles her hands "
        "and cradles the bottle softly near her collarbone; gaze easing to lens.",
        "The push holds as she settles a serene opulent smile to lens on a slow breath, a "
        "regal beat with no words; eyes calm and warm.",
        "She holds the composed regal look, candle-glow soft on the velvet, eyes luminous.",
    ),
    # F7 - medium close, 8% push loop close to F1
    (
        "Medium close chest-up matching Frame 1: a slow push is already resolving toward the "
        "exact opening framing as she re-cradles the faceted bottle and tilts it into the "
        "candle key, gold speculars sliding along the glass; gaze lowering to the bottle.",
        "The push settles as she eases her warm gaze back to lens on a slow breath with the "
        "composed quarter-smile, the composition resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, weight settled \u2014 a seamless "
        "loop seam.",
    ),
]


BEATS[32] = [
    (
        "Medium close chest-up in the inky deep-sea dark: a slow push-in is already gliding "
        "toward her as she tilts the glowing bottle a few degrees into the soft aqua key, "
        "speculars sliding along the glass and the luminous serum drifting inside; gaze "
        "lowered to the bottle, plankton motes hanging in the cool dark.",
        "The push continues as she lifts her serene gaze to lens on a slow deep-water inhale "
        "and a mysterious quarter-smile blooms, a few strands drifting weightless.",
        "She holds, suspended and calm, eyes catching the aqua glow, a loose strand drifting "
        "across the dark (silent).",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she lifts the dropper near her cheekbone and releases a single glowing aqua "
        "drop; gaze tracing the drop down through the water.",
        "The first bioluminescent plankton spark alight in the dark water around her, her "
        "eyes softening with mysterious wonder.",
        "The drop meets her skin with a luminous bloom, more strands drifting, lashes "
        "lowering in quiet awe.",
    ),
    (
        "Medium chest-up: a slow weightless arc is already drifting around her as she lowers "
        "the dropper a touch and the bioluminescent plankton gather; gaze following the "
        "gathering glow.",
        "The arc eases round as the suspended plankton pulse slow with glowing breaths, her "
        "eyes softening with wonder.",
        "The gathering tightens and brightens, cueing the bloom, her gaze lifting a degree in "
        "expectation.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "bioluminescent plankton bloom alight outward in weightless real-time underwater "
        "arcs and she opens her arms; gaze lifting into the bloom.",
        "The orbit rides the hero beat as a soft aqua glow sweeps across her and the gown and "
        "waves drift to their ethereal float (face clear, framed by the bloom); eyes widening "
        "in mysterious awe.",
        "The bloom settles and the glow resolves as the orbit eases; a serene wonder landing, "
        "eyes alight with aqua light.",
    ),
    (
        "Medium close, fully suspended: a slow push is already gliding in as she drifts her "
        "hands open and weightless, the glow settling and plankton pulsing slow; gaze easing "
        "to lens.",
        "She holds a serene mysterious wonder-smile to lens on a slow underwater breath, eyes "
        "luminous (silent \u2014 no words).",
        "She holds the radiant suspended look, plankton drifting around her, the smile easing "
        "into calm wonder.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the glowing bottle and tilts it into the aqua key, "
        "speculars sliding along the glass; gaze lowering to the bottle.",
        "The push settles as she eases her serene gaze back to lens on a slow underwater "
        "breath with the composed quarter-smile, the composition resolving to the opening; "
        "eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, suspended in the dark water \u2014 "
        "a seamless loop seam (silent).",
    ),
]

BEATS[33] = [
    (
        "Medium close chest-up in the bright blossom grove: a slow push-in is already gliding "
        "toward her as she tilts the bottle a few degrees into the morning sun, speculars "
        "sliding along the glass and the blush serum settling; gaze lowered to the bottle, a "
        "petal drifting past.",
        "The push continues as she lifts her bright gaze to lens on a soft inhale and a "
        "joyful quarter-smile blooms, dappled sun warming her face.",
        "She holds, fresh and happy, eyes sparkling, a petal drifting across the soft pink "
        "bokeh.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she lifts the dropper near her cheekbone and releases a single soft blush "
        "drop; gaze tracing the drop.",
        "The first blossom buds swell on the branches around her, her eyes brightening with "
        "anticipation.",
        "The drop meets her skin with a fresh dewy bloom, a petal drifting, a happy breath "
        "held.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the dropper "
        "a touch and the blossom buds swell and gather; gaze following the budding branches.",
        "The arc eases round as the first petals unfurl, her eyes brightening with joy.",
        "The gathering tightens and brightens, cueing the bloom, her gaze lifting in "
        "delight.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "cherry blossoms burst into full bloom in fast-forward and she opens her arms; gaze "
        "lifting into the bloom.",
        "The orbit rides the hero beat as a petal-shower sweeps across her and the dress and "
        "waves catch drifting petals (face clear, framed by the bloom); eyes widening in "
        "joyful awe.",
        "The bloom settles and the blossoms resolve as the orbit eases; a radiant fresh smile "
        "landing, petals drifting.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "bloom settles, the last petals drifting; gaze bright to lens.",
        "She delivers \u201cspring starts with me.\u201d to lens with a bright joyful smile, "
        "eyes warm and direct.",
        "She holds the radiant fresh look as one final petal settles, the smile easing into "
        "happy warmth.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the bottle and tilts it into the morning sun, "
        "speculars sliding along the glass; gaze lowering to the bottle.",
        "The push settles as she eases her bright gaze back to lens on a soft breath with the "
        "composed quarter-smile, the grove resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, a petal drifting past \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[34] = [
    (
        "Medium close chest-up in the cosmic dark: a slow push-in is already gliding toward "
        "her as she tilts the glowing bottle a few degrees into the soft silver-violet key, "
        "speculars sliding along the glass and the star-flecked elixir drifting; gaze lowered "
        "to the bottle, a star-mote drifting past.",
        "The push continues as she lifts her serene gaze to lens on a slow inhale and a "
        "mystic quarter-smile blooms, nebula haze drifting behind.",
        "She holds, serene and cosmic, eyes catching the silver-violet light, a strand "
        "drifting.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she lifts the dropper near her cheekbone and releases a single glowing "
        "star-flecked drop; gaze tracing the drop.",
        "The first glowing stars spark alight in the dark around her, her eyes softening with "
        "mystic wonder.",
        "The drop meets her skin with a luminous bloom, a strand drifting, lashes lowering in "
        "awe.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the dropper "
        "a touch and the glowing stars gather; gaze following the gathering constellation.",
        "The arc eases round as the suspended stars pulse slow and the first silver "
        "light-lines reach between them, her eyes softening with wonder.",
        "The gathering tightens and brightens, cueing the line-draw, her gaze lifting in "
        "expectation.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "silver light-lines draw bright between the stars and she opens her arms; gaze "
        "tracing the drawing lines.",
        "The orbit rides the hero beat as a sweeping silver glow races along the "
        "constellation and the gown and strands catch travelling light (face clear, framed by "
        "the draw); eyes widening in mystic awe.",
        "The draw settles and the constellation resolves as the orbit eases; a radiant cosmic "
        "look landing, eyes alight.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "constellation settles, light-lines glowing steady; gaze serene to lens.",
        "She delivers \u201cwritten in the stars.\u201d to lens with a serene knowing mystic "
        "smile, eyes warm and direct.",
        "She holds the radiant cosmic look, the constellation pulsing soft, the smile easing "
        "into calm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she settles her hands and cradles "
        "the glowing bottle softly near her collarbone; gaze easing to lens.",
        "The push holds as she settles a serene mystic smile to lens on a slow breath, a "
        "composed beat with no words; eyes calm.",
        "She holds the composed cosmic look, the constellation glowing soft behind, eyes "
        "luminous.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the glowing bottle and tilts it into the "
        "silver-violet key, speculars sliding along the glass; gaze lowering to the bottle.",
        "The push settles as she eases her serene gaze back to lens on a slow breath with the "
        "composed quarter-smile, the starfield resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, a star-mote drifting past \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[35] = [
    (
        "Medium close chest-up in the warm honey-lit space: a slow push-in is already gliding "
        "toward her as she tilts the amber bottle a few degrees into the golden key, "
        "speculars sliding along the glass and the honey-toned oil settling; gaze lowered to "
        "the bottle, a golden mote drifting past.",
        "The push continues as she lifts her warm gaze to lens on a soft inhale and a content "
        "quarter-smile blooms, honeycomb-warm light on her skin.",
        "She holds, warm and sensorial, eyes catching the amber glow, a golden mote drifting "
        "across the soft bokeh.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she lifts the dropper near her cheekbone and releases a single slow golden "
        "honey drop that stretches as it falls; gaze tracing the drop.",
        "The first warm amber-glaze glints gather in the air around her, her eyes warming "
        "with anticipation.",
        "The drop meets her skin with a warm gilded sheen, a mote drifting, lashes lowering "
        "in pleasure.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the dropper "
        "a touch and the golden honey ribbons gather and drift; gaze following the drifting "
        "gold.",
        "The arc eases round as the first warm amber-glaze gilds her shoulder, her eyes "
        "warming with pleasure.",
        "The gathering tightens and brightens, cueing the glaze, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "golden honey ribbons drift and the warm amber-light sweeps and she opens her arms; "
        "gaze lifting into the glaze.",
        "The orbit rides the hero beat as the glaze gilds bright across her and the satin and "
        "waves catch travelling gold (face clear, gilded by the glaze); eyes warming in "
        "sensorial awe.",
        "The glaze settles and the gild resolves as the orbit eases; a radiant honeyed look "
        "landing, eyes warm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "glaze settles, the last honey ribbons drifting; gaze warm to lens.",
        "She delivers \u201cgolden, inside and out.\u201d to lens with a warm content smile, "
        "eyes soft and direct.",
        "She holds the radiant honeyed look as one final ribbon settles, the smile easing "
        "into warm calm.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the amber bottle and tilts it into the golden key, "
        "speculars sliding along the glass; gaze lowering to the bottle.",
        "The push settles as she eases her warm gaze back to lens on a soft breath with the "
        "composed quarter-smile, the honeyed space resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, a golden mote drifting \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[36] = [
    (
        "Medium close chest-up in the cool monsoon scene: a slow push-in is already gliding "
        "toward her as she tilts the misted bottle a few degrees into the cool key, "
        "speculars sliding along the glass and a droplet tracing down as the essence settles; "
        "gaze lowered to the bottle, rain drifting behind.",
        "The push continues as she lifts her calm gaze to lens on a cool inhale and a serene "
        "quarter-smile blooms, a faint rain-kissed sheen on her skin.",
        "She holds, cool and refreshed, eyes calm, a soft sheet of rain drifting across the "
        "teal bokeh (silent).",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she lifts the dropper near her cheekbone and releases a single cool "
        "translucent drop; gaze tracing the drop.",
        "The first soft ripples bloom on a wet surface around her, her eyes cooling with "
        "anticipation.",
        "The drop meets her skin with a cool dewy sheen, rain drifting, lashes lowering "
        "calmly.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as the soft sheet of rain "
        "gathers and sweeps closer; gaze following the nearing rain.",
        "The arc eases round as the first dewy ripples bloom on a wet surface, her eyes "
        "cooling with pleasure.",
        "The gathering tightens and the rain brightens, cueing the bloom, her gaze lifting a "
        "degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "soft sheet of rain sweeps and dewy ripples bloom and she opens her arms; gaze "
        "lifting into the rain.",
        "The orbit rides the hero beat as the rain kisses bright across her and the satin and "
        "waves catch travelling beads (face clear, rain-kissed); eyes brightening in "
        "refreshed awe.",
        "The rain settles and the dew resolves as the orbit eases; a radiant rain-kissed look "
        "landing, eyes cool and bright.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "rain settles, the last ripples spreading; gaze fresh to lens.",
        "She lifts her fresh serene gaze to lens with a refreshed smile, lips softly closed "
        "(silent \u2014 no words), eyes bright and direct.",
        "She holds the radiant rain-kissed look as one final ripple settles, the smile easing "
        "into cool calm.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the misted bottle and tilts it into the cool key, "
        "speculars sliding along the glass; gaze lowering to the bottle.",
        "The push settles as she eases her cool gaze back to lens on a soft breath with the "
        "composed quarter-smile, the monsoon scene resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, rain drifting behind \u2014 a "
        "seamless loop seam (silent).",
    ),
]

BEATS[37] = [
    (
        "Medium close chest-up in the regal couture salon: a slow push-in is already gliding "
        "toward her as she tilts the opaline bottle a few degrees into the gilded key, "
        "speculars sliding along the glass and the pearlescent mist settling; gaze lowered "
        "to the bottle, a feather-plume drifting past.",
        "The push continues as she lifts her serene gaze to lens on a soft inhale and a regal "
        "quarter-smile blooms, gilded soft light on her skin.",
        "She holds, poised and regal, eyes catching the champagne light, a feather drifting "
        "across the warm-neutral bokeh.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she lifts the atomizer near her collarbone and releases a single soft "
        "pearlescent mist-spritz that blooms and drifts; gaze tracing the mist.",
        "The first white feather-plumes gather in the air around her, her eyes warming with "
        "anticipation.",
        "The mist settles to a pearl sheen, a feather drifting, lashes lowering in poise.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the "
        "atomizer a touch and the white feather-plumes gather and drift; gaze following the "
        "drifting plumes.",
        "The arc eases round as the first soft feather-cloud forms at her shoulder, her eyes "
        "warming with poise.",
        "The gathering tightens and brightens, cueing the burst, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "white feather-plumes burst and drift in slow regal arcs and she opens her arms; "
        "gaze lifting into the cloud.",
        "The orbit rides the hero beat as the feather-cloud blooms bright across her and the "
        "gown and updo catch travelling pearl (face clear, feather-framed); eyes warming in "
        "regal awe.",
        "The burst settles and the plumes resolve as the orbit eases; a radiant "
        "feather-framed look landing, eyes serene.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "burst settles, the last feathers drifting; gaze poised to lens.",
        "She delivers \u201cborn to wear the crown.\u201d to lens with a poised regal smile, "
        "eyes warm and direct.",
        "She holds the radiant feather-framed look as one final plume settles, the smile "
        "easing into regal calm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she holds the radiant "
        "feather-framed look on a slow content breath, the poised smile easing softer; gaze "
        "serene to lens.",
        "The push holds as the last plumes settle around her, eyes serene and composed, a "
        "regal beat with no words.",
        "She holds the lens with serene regal composure, plumes drifting soft, eyes "
        "luminous.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the opaline bottle and tilts it into the gilded "
        "key, speculars sliding along the glass; gaze lowering to the bottle.",
        "The push settles as she eases her serene gaze back to lens on a soft breath with the "
        "composed quarter-smile, the salon resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, a feather-plume drifting \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[38] = [
    (
        "Medium close chest-up in the bright whimsical studio: a slow push-in is already "
        "gliding toward her as she tilts the iridescent tube a few degrees into the bright "
        "key, rainbow speculars sliding along the glass and the shimmer settling; gaze "
        "lowered to the tube, a soap-bubble drifting past.",
        "The push continues as she lifts her bright gaze to lens on a soft inhale and a "
        "playful quarter-smile blooms, soft rainbow bokeh behind.",
        "She holds, bright and whimsical, eyes sparkling, an iridescent bubble drifting "
        "across the pearl-white air.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she lifts the Prism wand near her lips and eases a soft iridescent "
        "gloss-swipe, a rainbow glint travelling; gaze warm to the wand.",
        "The first iridescent soap-bubbles gather and drift around her, her eyes warming "
        "with delight.",
        "The gloss settles to a rainbow sheen, a bubble drifting, lashes lowering in "
        "playful warmth.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the tube a "
        "touch and the iridescent soap-bubbles gather and drift; gaze following the floating "
        "bubbles.",
        "The arc eases round as the first thin oil-slick film stretches at her shoulder, her "
        "eyes warming with delight.",
        "The gathering tightens and brightens, cueing the bloom, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "soap-film blooms iridescent and the bubbles drift and she opens her arms; gaze "
        "lifting into the film.",
        "The orbit rides the hero beat as the oil-slick film stretches bright across her and "
        "the top and waves catch travelling rainbow (face clear, iridescent-framed); eyes "
        "widening in whimsical delight.",
        "The bloom settles and the bubbles resolve as the orbit eases; a radiant "
        "iridescent-framed look landing, eyes bright.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "bloom settles, the last bubbles drifting; gaze bright to lens.",
        "She delivers \u201ccatch the light, catch the magic.\u201d to lens with a bright "
        "playful smile, eyes warm and direct.",
        "She holds the radiant iridescent-framed look as one final bubble drifts, the smile "
        "easing into playful warmth.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the iridescent tube and tilts it into the bright "
        "key, rainbow speculars sliding along the glass; gaze lowering to the tube.",
        "The push settles as she eases her bright gaze back to lens on a soft breath with the "
        "composed quarter-smile, the whimsical studio resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, a bubble drifting \u2014 a seamless "
        "loop seam.",
    ),
]

BEATS[39] = [
    (
        "Medium close chest-up in the graphic op-art studio: a slow push-in is already "
        "gliding toward her as she tilts the op-art tube a few degrees into the key, chrome "
        "speculars sliding along the cap and the bullet settling; gaze lowered to the tube, "
        "a kaleidoscope facet rotating slow behind her.",
        "The push continues as she lifts her bright gaze to lens on a soft inhale and a "
        "playful quarter-smile blooms, the black-and-white op-art crisp behind.",
        "She holds, playful and hypnotic, her single face clear and locked, eyes bright, one "
        "facet turning slow behind.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the Optic bullet near her lips and eases a crisp bold-color "
        "application, a chrome glint travelling; gaze sharpening.",
        "The first kaleidoscope facets mirror and rotate around her, her eyes sharpening with "
        "playful focus (her single face stays clear and locked).",
        "The colour settles crisp on her lips, a facet turning, lashes steady in playful "
        "focus.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the tube a "
        "touch and the op-art backdrop gathers into slow-mirroring facets; gaze following "
        "the turning facets.",
        "The arc eases round as the first facets rotate at her shoulder, her eyes sharpening "
        "with playful focus.",
        "The gathering tightens and snaps brighter, cueing the split, her gaze lifting a "
        "degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "op-art backdrop and light fracture and mirror into a slow-spinning kaleidoscope and "
        "she opens her arms; gaze tracing the spinning facets.",
        "The orbit rides the hero beat as the facets spin bright around her and the top and "
        "bob catch travelling facet-light (her single face clear and facet-framed, never "
        "multiplied); eyes widening in playful wonder.",
        "The split settles and the facets resolve as the orbit eases; a radiant facet-framed "
        "look landing, her single face clear, eyes bright.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "split settles, the last facets spinning slow; gaze bright to lens.",
        "She delivers \u201csee the world in motion.\u201d to lens with a knowing playful "
        "smile, eyes warm and direct, her single face clear and locked.",
        "She holds the radiant facet-framed look as one final facet settles, the smile easing "
        "into playful calm.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the op-art tube and tilts it into the key, chrome "
        "speculars sliding along the cap; gaze lowering to the tube.",
        "The push settles as she eases her bright gaze back to lens on a soft breath with the "
        "composed quarter-smile, the op-art studio resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, one facet turning slow \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[40] = [
    (
        "Medium close chest-up in the dark neon-night studio: a slow push-in is already "
        "gliding toward her as she tilts the Lumen tube a few degrees into the key, "
        "neon-cyan speculars sliding along the cap and the glowing bullet settling; gaze "
        "lowered to the tube, a faint neon trail drifting behind her.",
        "The push continues as she lifts her bright gaze to lens on a soft inhale and a "
        "confident quarter-smile blooms, electric cyan-and-magenta glow behind.",
        "She holds, electric and confident, her single face clear and locked, eyes bright, a "
        "neon trail drifting across the black.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the glowing Lumen applicator near her cheekbone and eases a "
        "luminous glow-drop along the high point, a neon glint travelling; gaze sharpening.",
        "The first neon light-trail draws and curls near her shoulder, her eyes sharpening "
        "with electric focus (her single face stays clear and locked).",
        "The glow settles bright on her cheekbone, a ribbon curling, lashes steady in "
        "electric focus.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the "
        "applicator a touch and the long-exposure neon trails draw and gather into luminous "
        "ribbons; gaze following the curling light.",
        "The arc eases round as the first ribbon curls at her shoulder, her eyes sharpening "
        "with electric focus.",
        "The gathering tightens and brightens, cueing the wrap, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "neon trails wrap in luminous ribbons and she opens her arms; gaze tracing the "
        "curling ribbons.",
        "The orbit rides the hero beat as the ribbons curl bright around her and the top and "
        "crown catch travelling neon (her single face clear and trail-framed, never traced "
        "over); eyes widening in electric awe.",
        "The wrap settles and the ribbons resolve as the orbit eases; a radiant trail-framed "
        "look landing, her single face clear, eyes alight.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "wrap settles, the last ribbons curling slow; gaze bright to lens.",
        "She delivers \u201cI light up the night.\u201d to lens with a confident bright "
        "smile, eyes warm and direct, her single face clear and locked.",
        "She holds the radiant trail-framed look as one final ribbon settles, the smile "
        "easing into confident calm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases from the bright smile "
        "to a calm confident half-smile and the last neon ribbon dissolves behind her; gaze "
        "steady to lens.",
        "The push holds as she settles her hand near the Lumen tube on a soft breath, "
        "holding the radiant glow; eyes calm and bright.",
        "She holds the confident half-smile toward the loop, neon glow soft behind, her "
        "single face clear and locked.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the Lumen tube and tilts it into the key, "
        "neon-cyan speculars sliding along the cap; gaze lowering to the tube.",
        "The push settles as she eases her bright gaze back to lens on a soft breath with the "
        "composed quarter-smile, the neon-night studio resolving to the opening; eyes "
        "calming.",
        "She lands precisely on the Frame 1 pose and gaze, a neon trail drifting \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[41] = [
    (
        "Medium close chest-up in the dreamy underwater-light studio: a slow push-in is "
        "already gliding toward her as she tilts the Nacre jar a few degrees into the key, "
        "pearl speculars sliding along the lid and the balm settling; gaze lowered to the "
        "jar, a coral frond swaying slow behind her.",
        "The push continues as she lifts her bright gaze to lens on a soft inhale and a "
        "dreamy quarter-smile blooms, dappled caustic water-light playing over her.",
        "She holds, dreamy and aquatic, her single face clear and locked, eyes soft, a coral "
        "frond swaying behind.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she glides a dab of pearl-aqua balm along her cheekbone with a soft dreamy "
        "press, a pearl glint travelling; gaze soft to the touch.",
        "The first tiny coral polyps sprout and sway near her shoulder, her eyes softening "
        "with dreamy focus (her single face stays clear and locked).",
        "The balm settles to a pearl sheen, a frond swaying, lashes lowering in dreamy "
        "calm.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers her hand a "
        "touch and the soft corals sprout and gather into a slow blooming arc; gaze "
        "following the curling fronds.",
        "The arc eases round as the first frond curls at her shoulder, her eyes softening "
        "with dreamy wonder.",
        "The gathering tightens and brightens, cueing the bloom, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "corals bloom in dreamy arcs and she opens her arms; gaze lifting into the bloom.",
        "The orbit rides the hero beat as the fronds unfurl soft around her and the waves "
        "and top catch travelling coral-light (her single face clear and coral-framed, never "
        "overgrown); eyes widening in dreamy wonder.",
        "The bloom settles and the corals resolve as the orbit eases; a serene radiant look "
        "landing, her single face clear, eyes soft.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "bloom settles, the last corals curling slow; gaze serene to lens.",
        "She lifts a serene radiant smile to lens in the full coral-frame, lips softly "
        "closed (silent \u2014 no words), eyes soft and direct.",
        "She holds the dreamy coral-framed look as one final frond settles, the smile easing "
        "into calm wonder.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the Nacre jar and tilts it into the key, pearl "
        "speculars sliding along the lid; gaze lowering to the jar.",
        "The push settles as she eases her bright gaze back to lens on a soft breath with the "
        "composed dreamy quarter-smile, the aquatic studio resolving to the opening; eyes "
        "calming.",
        "She lands precisely on the Frame 1 pose and gaze, a coral frond swaying \u2014 a "
        "seamless loop seam (silent).",
    ),
]

BEATS[42] = [
    (
        "Medium close chest-up in the artisanal glassblowing studio: a slow push-in is "
        "already gliding toward her as she tilts the amber-glass bottle a few degrees into "
        "the key, molten-amber speculars sliding along the dropper and the serum settling; "
        "gaze lowered to the bottle, an ember drifting behind her.",
        "The push continues as she lifts her warm gaze to lens on a soft inhale and an "
        "assured quarter-smile blooms, furnace-glow warm on her skin.",
        "She holds, warm and assured, her single face clear and locked, eyes steady, an "
        "ember drifting across the dark.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the frosted-glass dropper near her cheekbone and glides a warm "
        "liquid-glass serum drop along the high point, a molten glint travelling; gaze warm "
        "to the touch.",
        "The first molten-glass thread flows and curls near her shoulder, her eyes warming "
        "with assured focus (her single face stays clear and locked).",
        "The serum settles to a warm sheen, a thread curling, lashes lowering in assured "
        "calm.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the dropper "
        "a touch and the molten-glass threads flow and gather into a glowing sculptural arc; "
        "gaze following the molten thread.",
        "The arc eases round as the first thread curls at her shoulder, her eyes warming "
        "with assured focus.",
        "The gathering tightens and glows brighter, cueing the form, her gaze lifting a "
        "degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "molten glass flows and sculpts in slow arcs and she opens her arms; gaze tracing "
        "the flowing glass.",
        "The orbit rides the hero beat as the glass curls and begins to cool from "
        "molten-amber to clear beside her and the chignon and top catch travelling molten "
        "light (her single face clear and glass-framed, never glassed-over); eyes warming in "
        "artisanal awe.",
        "The form settles cooled and the glass resolves as the orbit eases; a radiant "
        "glass-framed look landing, her single face clear, eyes warm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "form settles cooled, the last glass arcs clarifying; gaze warm to lens.",
        "She delivers \u201cshaped by fire, made to last.\u201d to lens with a quietly proud "
        "smile, eyes warm and direct, her single face clear and locked.",
        "She holds the radiant glass-framed look as one final arc settles, the smile easing "
        "into assured calm.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the amber-glass bottle and tilts it into the key, "
        "molten-amber speculars sliding along the dropper; gaze lowering to the bottle.",
        "The push settles as she eases her warm gaze back to lens on a soft breath with the "
        "composed assured quarter-smile, the workshop resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, an ember drifting \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[43] = [
    (
        "Medium close chest-up in the dramatic storm studio: a slow push-in is already "
        "gliding toward her as she tilts the Volt bottle a few degrees into the key, "
        "electric-white speculars sliding along the cap and the charged liquid settling; "
        "gaze lowered to the bottle, a distant lightning flickering behind her.",
        "The push continues as she lifts her intense gaze to lens on a soft inhale and a "
        "powerful quarter-smile sets, cool steel-blue storm-light on her.",
        "She holds, charged and powerful, her single face clear and locked, eyes intense, "
        "distant lightning flickering behind.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the charged Volt applicator near her cheekbone and presses a "
        "charged-glow primer along the high point, an electric glint travelling; gaze "
        "sharpening.",
        "The first electric-white spark crackles near her shoulder, her eyes sharpening with "
        "charged focus (her single face stays clear and locked).",
        "The primer settles bright on her cheekbone, a spark crackling, lashes steady in "
        "charged focus.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the "
        "applicator a touch and the electric-white sparks crackle and gather into charged "
        "arcs; gaze following the leaping light.",
        "The arc eases round as the first arc leaps at her shoulder, her eyes sharpening with "
        "charged power.",
        "The gathering tightens and brightens, cueing the crackle, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "lightning arcs leap and crackle and she opens her arms; gaze tracing the striking "
        "arcs.",
        "The orbit rides the hero beat as the arcs strike bright around her and the "
        "windswept crown and top catch travelling electric light (her single face clear and "
        "arc-framed, never struck-over); eyes blazing in powerful awe.",
        "The crackle settles and the arcs resolve as the orbit eases; a radiant arc-framed "
        "look landing, her single face clear, eyes fierce.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "crackle resolves into a radiant halo around her; gaze fierce to lens.",
        "She delivers \u201cI am the storm.\u201d to lens with a fierce composed smile, eyes "
        "intense and direct, her single face clear and locked.",
        "She holds the radiant arc-framed look as the last arc crackles slow, the smile "
        "holding fierce and composed.",
    ),
    (
        "Medium close: a slow push is already gliding in as she re-cradles the Volt bottle "
        "near her collarbone and the arc-halo eases to a slow crackle; gaze steady to lens.",
        "The push holds as she settles a quietly powerful look to lens on a slow breath, a "
        "distant lightning flickering behind her; eyes calm and intense.",
        "She holds the quietly powerful look toward the loop, storm-light soft behind, her "
        "single face clear and locked.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the Volt bottle and tilts it into the key, "
        "electric-white speculars sliding along the cap; gaze lowering to the bottle.",
        "The push settles as she eases her intense gaze back to lens on a soft breath with "
        "the composed quarter-smile, the storm studio resolving to the opening; eyes "
        "calming.",
        "She lands precisely on the Frame 1 pose and gaze, distant lightning flickering "
        "\u2014 a seamless loop seam.",
    ),
]


BEATS[44] = [
    (
        "Medium close chest-up in the '70s disco lounge: a slow push-in is already gliding "
        "toward her as she tilts the faceted bottle a few degrees into the key, gold "
        "speculars sliding along the cap and the shimmer oil settling; gaze lowered to the "
        "bottle, the mirror-ball scattering a faint shard behind her.",
        "The push continues as she lifts her warm gaze to lens on a soft inhale and a playful "
        "groovy quarter-smile blooms, warm-gold disco haze around her.",
        "She holds, warm and groovy, her single face clear and locked, eyes warm, a gold "
        "shard drifting across the dancefloor glow.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the glow-oil applicator near her cheekbone and glides a warm "
        "golden shimmer drop along the high point, a gold glint travelling; gaze warm to the "
        "touch.",
        "The first light-shard drifts and glints near her shoulder, her eyes warming with "
        "groovy focus (her single face stays clear and locked).",
        "The shimmer settles to a gold sheen, a shard arcing, lashes lowering in groovy "
        "warmth.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the "
        "applicator a touch and the mirror-ball spins up and golden light-shards gather into "
        "a glittering swirl; gaze following the arcing shards.",
        "The arc eases round as the first shard arcs at her shoulder, her eyes warming with "
        "groovy joy.",
        "The swirl tightens and glitters brighter, cueing the scatter, her gaze lifting a "
        "degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "light-shards leap and scatter in slow glittering arcs and she opens her arms; gaze "
        "lifting into the swirl.",
        "The orbit rides the hero beat as the shards swirl bright around her and the "
        "feathered flip and top catch travelling gold light (her single face clear and "
        "shard-framed, never shard-covered); eyes sparkling in groovy joy.",
        "The scatter settles and the shards resolve as the orbit eases; a radiant "
        "shard-framed look landing, her single face clear, eyes warm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "scatter resolves into a glittering halo around her; gaze warm to lens.",
        "She delivers \u201cborn to shine.\u201d to lens with a joyful groovy smile, eyes "
        "warm and direct, her single face clear and locked.",
        "She holds the radiant shard-framed look as the last shards drift slow, the smile "
        "easing into groovy warmth.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the faceted bottle and tilts it into the key, "
        "gold speculars sliding along the cap; gaze lowering to the bottle.",
        "The push settles as she eases her warm gaze back to lens on a soft breath with the "
        "playful groovy quarter-smile, the disco lounge resolving to the opening; eyes "
        "calming.",
        "She lands precisely on the Frame 1 pose and gaze, a gold shard drifting \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[45] = [
    (
        "Medium close chest-up in the candy-pop studio: a slow push-in is already gliding "
        "toward her as she tilts the gloss bottle a few degrees into the key, glossy "
        "speculars sliding along the clear cap and the gloss settling; gaze lowered to the "
        "bottle, a soft bubble drifting behind her.",
        "The push continues as she lifts her bright gaze to lens on a soft inhale and a "
        "playful sweet quarter-smile blooms, bright bubblegum-pink glow around her.",
        "She holds, bright and sweet, her single face clear and locked, eyes sparkling, a "
        "soft bubble drifting.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the gloss applicator near her lip and swipes a bright "
        "bubblegum-pink gloss across the lower lip, a glossy glint travelling; gaze bright.",
        "The first translucent bubble forms and drifts near her shoulder, her eyes "
        "brightening with playful focus (her single face stays clear and locked).",
        "The gloss settles glossy on her lip, a bubble drifting, lashes lowering in playful "
        "glee.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the "
        "applicator a touch and a translucent bubblegum-pink bubble inflates and stretches "
        "into a glossy rounded form beside her; gaze following the swelling bubble.",
        "The arc eases round as the bubble swells with a rainbow sheen, her eyes brightening "
        "with playful glee.",
        "The bubble stretches to its fullest and thins, cueing the pop, her gaze lifting a "
        "degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "bubble bursts into a glossy pink shimmer-burst and she opens her arms; gaze lifting "
        "into the burst.",
        "The orbit rides the hero beat as the shimmer scatters bright around her and the "
        "bubble-ponytail and top catch travelling pink light (her single face clear and "
        "shimmer-framed, never bubble-covered); eyes widening in playful glee.",
        "The burst settles and the shimmer resolves as the orbit eases; a radiant "
        "shimmer-framed look landing, her single face clear, eyes bright.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "burst resolves into a glossy shimmer halo around her; gaze bright to lens.",
        "She delivers \u201csweet, but make it iconic.\u201d to lens with a joyful playful "
        "smile, eyes warm and direct, her single face clear and locked.",
        "She holds the radiant shimmer-framed look as the last droplets drift slow, the "
        "smile easing into sweet warmth.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the glossy pink bottle and tilts it into the key, "
        "glossy speculars sliding along the clear cap; gaze lowering to the bottle.",
        "The push settles as she eases her bright gaze back to lens on a soft breath with the "
        "playful sweet quarter-smile, the candy studio resolving to the opening; eyes "
        "calming.",
        "She lands precisely on the Frame 1 pose and gaze, a soft bubble drifting \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[46] = [
    (
        "Medium close chest-up in the celestial night chamber: a slow push-in is already "
        "gliding toward her as she tilts the frosted bottle a few degrees into the key, "
        "silver speculars sliding along the crescent cap and the balm settling; gaze lowered "
        "to the bottle, the eclipse orb pulsing soft behind her.",
        "The push continues as she lifts her calm gaze to lens on a soft inhale and a serene "
        "quarter-smile blooms, cool silver-blue moonlight on her.",
        "She holds, serene and mystic, her single lit face clear and locked, eyes calm, the "
        "eclipse orb glowing soft behind (silent).",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the glow-balm applicator near her cheekbone and glides a cool "
        "silver-blue balm along the high point, a silver glint travelling; gaze calm.",
        "The eclipse orb dims a touch at one edge, her eyes calming with serene focus (her "
        "single face stays lit and locked).",
        "The balm settles to a silver sheen, the corona brightening, lashes lowering in "
        "serene calm.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as the eclipse orb dims "
        "toward totality and a soft lunar shadow gathers and arcs at the frame edge; gaze "
        "following the brightening corona.",
        "The arc eases round as the corona brightens around the dark moon, her eyes calming "
        "with serene wonder.",
        "The gather tightens and the corona glows brighter, cueing the sweep, her gaze "
        "lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "eclipse-shadow sweeps across and a silver corona sweeps back and she opens her "
        "arms; gaze lifting into the moonlight.",
        "The orbit rides the hero beat as the moonlight washes serene around her and the "
        "chignon and velvet catch travelling silver light (her single lit face clear and "
        "moonlight-framed, never shadow-swallowed); eyes calming in serene awe.",
        "The sweep settles and the moonlight resolves as the orbit eases; a serene radiant "
        "look landing, her single lit face clear, eyes calm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "sweep resolves into a serene silver-blue halo around her; gaze calm to lens.",
        "She holds a calm knowing look to lens, lips softly closed (silent \u2014 no words), "
        "eyes serene and direct, her single lit face clear and locked.",
        "She holds the radiant moonlight-framed look as the last glints drift slow, the "
        "expression easing into serene calm.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the frosted bottle and tilts it into the key, "
        "silver speculars sliding along the crescent cap; gaze lowering to the bottle.",
        "The push settles as she eases her calm gaze back to lens on a soft breath with the "
        "serene quarter-smile, the night chamber resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, the eclipse orb pulsing soft "
        "\u2014 a seamless loop seam (silent).",
    ),
]


BEATS[47] = [
    (
        "Medium close chest-up in the fluid-art studio: a slow push-in is already gliding "
        "toward her as she tilts the clear bottle a few degrees into the key, chrome "
        "speculars sliding along the cap and the galaxy liquid swirling inside with gold "
        "flecks drifting; gaze lowered to the bottle, a paint ribbon curling slow behind "
        "her.",
        "The push continues as she lifts her deep gaze to lens on a soft inhale and a "
        "mesmerized quarter-smile blooms, glossy jewel-tone swirls behind.",
        "She holds, deep and mesmerized, her single face clear and locked, eyes rich, a "
        "paint ribbon curling across the gloss.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the pigment applicator near her cheekbone and glides a glossy "
        "galaxy-toned pigment along the high point, a jewel glint travelling; gaze deep.",
        "The first paint ribbon pours and curls near her shoulder, her eyes deepening with "
        "mesmerized focus (her single face stays clear and locked).",
        "The pigment settles to a glossy sheen, a ribbon curling, lashes lowering in "
        "mesmerized calm.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the "
        "applicator a touch and glossy galaxy paint ribbons pour and gather into a marbled "
        "swirl; gaze following the threading gold veins.",
        "The arc eases round as the ribbons thread with gold veins and curl tighter, her "
        "eyes deepening with mesmerized wonder.",
        "The swirl tightens and glints richer, cueing the pour, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "galaxy paint ribbons pour and swirl in slow marbled arcs and she opens her arms; "
        "gaze tracing the swirling ribbons.",
        "The orbit rides the hero beat as the ribbons swirl glossy around her and the "
        "slicked hair and top catch travelling jewel light (her single face clear and "
        "ribbon-framed, never paint-covered); eyes deepening in mesmerized awe.",
        "The swirl settles and the ribbons resolve as the orbit eases; a radiant "
        "ribbon-framed look landing, her single face clear, eyes rich.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "swirl resolves into a glossy marbled halo around her; gaze deep to lens.",
        "She delivers \u201cI'm a work of art.\u201d to lens with a mesmerized confident "
        "smile, eyes rich and direct, her single face clear and locked.",
        "She holds the radiant ribbon-framed look as the last ribbons drift slow, the smile "
        "easing into deep calm.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the clear bottle and tilts it into the key, "
        "chrome speculars sliding along the cap and the galaxy liquid swirling inside; gaze "
        "lowering to the bottle.",
        "The push settles as she eases her deep gaze back to lens on a soft breath with the "
        "mesmerized quarter-smile, the fluid-art studio resolving to the opening; eyes "
        "calming.",
        "She lands precisely on the Frame 1 pose and gaze, a paint ribbon curling \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[48] = [
    (
        "Medium close chest-up in the summer-dusk meadow: a slow push-in is already gliding "
        "toward her as she tilts the amber bottle a few degrees into the warm key, brass "
        "speculars sliding along the cap and the honey-gold oil settling; gaze lowered to "
        "the bottle, a firefly drifting slow behind her.",
        "The push continues as she lifts her warm gaze to lens on a soft inhale and a tender "
        "quarter-smile blooms, warm-on-cool dusk light around her.",
        "She holds, tender and nostalgic, her single face clear and locked, eyes warm, a "
        "firefly drifting across the dusky field.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the glow-oil dropper near her cheekbone and glides a warm "
        "honey-gold sheen along the high point, a warm glint travelling; gaze warm.",
        "The first fireflies drift in near her shoulder, her eyes warming with tender focus "
        "(her single face stays clear and locked).",
        "The sheen settles warm on her cheekbone, a firefly drifting, lashes lowering in "
        "tender calm.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the dropper "
        "a touch and warm golden fireflies drift in and gather into a glowing swarm; gaze "
        "following the pulsing swarm.",
        "The arc eases round as the swarm thickens and pulses warm, her eyes warming with "
        "tender wonder.",
        "The swarm tightens and glows richer, cueing the swarm-wrap, her gaze lifting a "
        "degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "warm fireflies swirl into slow tender arcs and she opens her arms; gaze lifting "
        "into the swarm.",
        "The orbit rides the hero beat as the swarm wraps warm around her and the soft waves "
        "and knit catch travelling golden light (her single face clear and firefly-framed, "
        "never firefly-covered); eyes warming in tender wonder.",
        "The swarm settles and the fireflies resolve as the orbit eases; a tender radiant "
        "look landing, her single face clear, eyes warm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "swarm resolves into a soft glowing firefly-halo around her; gaze warm to lens.",
        "She delivers \u201cI carry my own light.\u201d to lens with a tender confident "
        "smile, eyes warm and direct, her single face clear and locked.",
        "She holds the radiant firefly-framed look as the last fireflies drift slow, the "
        "smile easing into tender warmth.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases into a warm closed-lip "
        "afterglow smile and the fireflies drift soft around her; gaze tender to lens.",
        "The push holds as she holds a tender gaze to lens with a slow soft blink, the "
        "bottle resting at her collarbone; eyes warm and wistful.",
        "She holds the tender afterglow look, fireflies drifting soft, her single face clear "
        "and locked.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the amber bottle and tilts it into the warm key, "
        "brass speculars sliding along the cap and the honey-gold oil settling; gaze "
        "lowering to the bottle.",
        "The push settles as she eases her warm gaze back to lens on a soft breath with the "
        "wistful quarter-smile, the dusk meadow resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, a firefly drifting \u2014 a "
        "seamless loop seam.",
    ),
]

BEATS[49] = [
    (
        "Medium close chest-up in the cozy snow-globe cabin: a slow push-in is already "
        "gliding toward her as she tilts the round globe-jar a few degrees into the warm "
        "key, silver speculars sliding along the base and the frosted-pearl balm catching a "
        "soft glint; gaze lowered to the jar, snow drifting slow at the window behind her.",
        "The push continues as she lifts her warm gaze to lens on a soft inhale and a cozy "
        "quarter-smile blooms, warm amber lamp-glow meeting cool snow-blue.",
        "She holds, warm and cozy, her single face clear and locked, eyes soft, snow drifting "
        "at the window.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the frost-shimmer balm on a fingertip near her cheekbone and "
        "glides a soft frosted-pearl sheen along the high point, a silver glint travelling; "
        "gaze warm.",
        "The first snowflakes lift and drift near her shoulder, her eyes warming with cozy "
        "focus (her single face stays clear and locked).",
        "The sheen settles to a frosted pearl, a snowflake drifting, lashes lowering in cozy "
        "calm.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the jar a "
        "touch and glittering snowflakes lift and gather into a swirling flurry; gaze "
        "following the silver glints.",
        "The arc eases round as the flurry thickens and glints silver, her eyes warming with "
        "magical wonder.",
        "The flurry tightens and swirls richer, cueing the shake, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "scene shakes like a snow-globe and the glittering snow lifts and spirals into slow "
        "magical arcs and she opens her arms; gaze lifting into the flurry.",
        "The orbit rides the hero beat as the snow swirls cozy around her and the braid and "
        "knit catch travelling silver light (her single face clear and snow-framed, never "
        "snow-covered); eyes warming in magical wonder.",
        "The flurry settles and the snow resolves as the orbit eases; a cozy radiant look "
        "landing, her single face clear, eyes warm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands open and the "
        "flurry resolves into a soft glowing snow-halo around her; gaze warm to lens.",
        "She delivers \u201cthe magic's already inside.\u201d to lens with a cozy magical "
        "smile, eyes warm and direct, her single face clear and locked.",
        "She holds the radiant snow-framed look as the last snowflakes drift slow, the smile "
        "easing into cozy warmth.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the globe-jar and tilts it into the warm key, "
        "silver speculars sliding along the base and the frosted-pearl balm settling; gaze "
        "lowering to the jar.",
        "The push settles as she eases her warm gaze back to lens on a soft breath with the "
        "wistful quarter-smile, the cozy cabin resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, snow drifting at the window "
        "\u2014 a seamless loop seam.",
    ),
]

BEATS[50] = [
    (
        "Medium close chest-up in the dark studio of rising embers: a slow push-in is already "
        "gliding toward her as she tilts the flame-bottle a few degrees into the warm key, "
        "gold speculars sliding along the cap and the molten-amber elixir settling; gaze "
        "lowered to the bottle, embers rising slow behind her.",
        "The push continues as she lifts her gaze to lens on a soft inhale and a triumphant "
        "quarter-smile blooms, molten-gold rim-light on her.",
        "She holds, radiant and triumphant, her single face clear and locked, eyes bright, "
        "embers rising across the charcoal void.",
    ),
    (
        "Medium close: the slow push continues with a faint tilt-up already following her "
        "hand as she raises the radiance elixir on a fingertip near her cheekbone and glides "
        "a soft warm-glow sheen along the high point, a gold glint travelling; gaze warm.",
        "The first embers lift and rise near her shoulder, her eyes warming with triumphant "
        "focus (her single face stays clear and locked).",
        "The sheen settles warm on her cheekbone, an ember rising, lashes lowering in "
        "resolve.",
    ),
    (
        "Medium chest-up: a slow arc is already drifting around her as she lowers the bottle "
        "a touch and glowing embers lift and gather into the first phoenix-feather wing "
        "forms; gaze following the gathering wings.",
        "The arc eases round as the embers thicken and glint gold, her eyes warming with "
        "triumphant resolve.",
        "The wing-forms tighten and brighten, cueing the rise, her gaze lifting a degree.",
    ),
    (
        "Energized medium-wide: the push is already easing into a smooth gentle orbit as the "
        "embers stream upward and unfurl into great glowing phoenix-feather wings and she "
        "opens and lifts her arms; gaze rising with the wings.",
        "The orbit rides the hero beat as the wings unfurl triumphant around her and the "
        "updo and gown catch travelling gold light (her single face clear and ember-framed, "
        "never ember-covered); eyes blazing in triumphant awe.",
        "The rise crests and the embers resolve as the orbit eases; a radiant triumphant "
        "look landing, her single face clear, eyes alight.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases her hands down and the "
        "rise resolves into a soft glowing ember-halo around her; gaze radiant to lens.",
        "She delivers \u201cI always rise.\u201d to lens with a triumphant radiant smile, "
        "eyes bright and direct, her single face clear and locked.",
        "She holds the radiant ember-framed look as the last embers drift slow, the smile "
        "holding triumphant and warm.",
    ),
    (
        "Medium close: a slow push is already gliding in as she eases into a warm assured "
        "closed-lip afterglow smile and the embers drift soft around her; gaze proud to "
        "lens.",
        "The push holds as she holds a proud gaze to lens with a slow soft blink, the bottle "
        "resting at her collarbone; eyes warm and assured.",
        "She holds the proud afterglow look, embers drifting soft, her single face clear and "
        "locked.",
    ),
    (
        "Medium close: a slow push is already gliding in as she raises the flame-bottle to a "
        "proud hero-present beside her cheek, embers drifting soft around it; gaze warm to "
        "lens.",
        "The push holds as she eases a warm triumphant smile to lens, the gold cap catching "
        "a clean specular as the bottle holds; eyes bright.",
        "She holds the proud hero-present, the bottle glinting, eyes radiant and direct.",
    ),
    (
        "Medium close matching Frame 1: a slow push is already resolving toward the exact "
        "opening framing as she re-cradles the flame-bottle and tilts it into the warm key, "
        "gold speculars sliding along the cap and the molten-amber elixir settling; gaze "
        "lowering to the bottle.",
        "The push settles as she eases her bright gaze back to lens on a soft breath with the "
        "composed quarter-smile, the ember studio resolving to the opening; eyes calming.",
        "She lands precisely on the Frame 1 pose and gaze, embers rising slow \u2014 a "
        "seamless loop seam and a triumphant set-closing button.",
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
    frames = BEATS[concept_no]
    start = text.index(f"# CONCEPT {concept_no} \u2014")
    nxt = re.search(rf"# CONCEPT {concept_no + 1} \u2014", text)
    end = nxt.start() if nxt else len(text)
    region = text[start:end]

    region, n_cam = re.subn(r"CAMERA MOVEMENT: [^\n]*\n\n", "", region)

    state = {"i": 0}

    def repl(_m):
        beats = frames[state["i"]]
        state["i"] += 1
        return build_block(beats)

    region, n_act = re.subn(
        r"SUBJECT ACTION WITH TIMING:(?:\n(?:- .*\n)+| [^\n]*\n)", repl, region
    )
    region, n_dur = re.subn(r"(?m)^DURATION: [^\n]*$", DURATION_LINE, region)
    region, n_fr = re.subn(
        r"(?m)^FRAME RATE \+ MOTION BLUR: [^\n]*$", FRAME_RATE_LINE, region
    )

    nf = len(frames)
    assert n_act == nf, f"concept {concept_no}: {n_act} action blocks vs {nf} frames"
    assert n_cam == nf, f"concept {concept_no}: {n_cam} camera lines vs {nf} frames"
    assert n_dur == nf, f"concept {concept_no}: {n_dur} DURATION lines vs {nf} frames"
    assert n_fr == nf, f"concept {concept_no}: {n_fr} FRAME RATE lines vs {nf} frames"
    print(
        f"concept {concept_no}: removed {n_cam} camera lines, rebuilt {n_act} "
        f"breakdowns, reset {n_dur} DURATION + {n_fr} FRAME RATE lines"
    )
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

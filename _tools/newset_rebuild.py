#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced video-prompt rebuild engine for
CONCEPTS/20 Cinematic Reels New Set.txt

Per VIDEO prompt in a concept region:
  - remove the standalone `CAMERA MOVEMENT (CHOREOGRAPHY): ...` line
    (camera now lives inside the breakdown),
  - replace the `SUBJECT ACTION w/ BEAT-TIMING:` block with a tailored
    `SHOT BREAKDOWN (timed, 6s ...)` of 3 beats, each carrying
    shot size/angle + her action + object/world interaction + eye-led
    expression + camera move,
  - insert `FRAME RATE + MOTION BLUR:` and `DURATION: 6 seconds` lines.

Everything else (SHOT TYPE & ANGLE, LENS, FLUIDITY & WEIGHT NOTES,
FABRIC/HAIR/PROP PHYSICS, FOOTWORK & BODY FLOW, TRANSITION/IMPOSSIBLE MOVE,
LIGHTING-IN-MOTION, AUDIO, LOOP LOGIC, identity lock) is preserved.

Idempotent: once a concept's SUBJECT ACTION blocks are consumed the regex no
longer matches, so re-running is a no-op for already-rebuilt concepts.

Usage:  python _tools/newset_rebuild.py <concept_number>
"""
import re
import sys

PATH = "CONCEPTS/20 Cinematic Reels New Set.txt"

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

# concept_number -> list of frames; each frame is a 3-tuple of beat strings
# (beats use en dash brackets [00:00-00:02] applied by the engine).
BEATS = {}

BEATS[1] = [
    # Frame 1 - high-angle wide establishing (silent)
    (
        "High-angle wide, full figure on the lower-third power point: the camera is "
        "already craning slowly downward as she stands at the tiled edge mid-breath, "
        "gaze travelling down the glowing pool, ivory linen hem already rippling in the "
        "warm breeze; lids soft, eyes tracing the bright water-line.",
        "The move eases out of the crane into a gentle forward track toward the water as "
        "she turns her face back over the shoulder to lens, a serene closed-lip half-smile "
        "blooming, eyes warming under the crisp low-sun catchlight.",
        "The track settles; her hand drifts from the sunglasses at her temple down toward "
        "her side as her weight rolls onto the water-side foot, gaze lowering to the "
        "surface to motivate the next beat.",
    ),
    # Frame 2 - low macro on feet
    (
        "Low macro on the feet, the detail filling the frame: a slow lateral slider is "
        "already gliding along the wet tile lip as one foot eases out of the woven slide "
        "mid-motion, toes pointing, the empty slide rocking on the travertine \u2014 "
        "expression carried by the deliberate, articulate step.",
        "The slider arcs a touch toward the tile edge following the lifting foot; the bare "
        "foot hovers and lowers toward the glowing aqua water as a single droplet forms, "
        "stretches and falls.",
        "Camera holds low and close as the toes break the surface and a clean ripple ring "
        "spreads outward \u2014 the seed of the water that will later climb her arm.",
    ),
    # Frame 3 - profile medium, crouch reaching into water
    (
        "Profile medium in a clean side silhouette: the camera is already arcing in a slow "
        "orbit from full profile toward three-quarter as she lowers into the crouch "
        "mid-descent, arm reaching for the water; eyes following her own hand down, lashes "
        "lowering in concentration.",
        "The orbit keeps rolling the gold rim across her cheek as her fingers slip into the "
        "water, ripple rings blooming and caustics climbing her forearm; lips parting a "
        "millimetre in quiet wonder.",
        "She tilts her head, gaze tracking a thin sheet of water that begins to defy "
        "gravity and creep up her wrist; inner brow lifting in soft awe as the orbit eases "
        "to rest.",
    ),
    # Frame 4 - 3/4 front cowboy, rise + transform keyframe A
    (
        "Three-quarter front cowboy, rising in frame: a smooth crane-up is already tracking "
        "her ascent as she begins to rise and the pool water climbs her arm; her gaze lifts "
        "with the spiral, eyes beginning to widen.",
        "The crane continues upward as the water-ribbon wraps her torso and aqua-to-teal "
        "chiffon weaves into being around her; chin lifting, breath caught with parted "
        "lips, cheeks lifting in serene awe.",
        "At the apex her arms bloom open and droplets fling outward on real ballistic arcs, "
        "head lifting fully to lens \u2014 the hero water-to-silk weave at its peak, eyes "
        "alight.",
    ),
    # Frame 5 - front full/wide hero, transform keyframe B resolve
    (
        "Front-on full/wide hero, centred: the orbit completes to dead-front and "
        "decelerates as she settles tall, the finished sea-silk gown drifting into place "
        "around her; energy easing, shoulders opening.",
        "Near-locked now on a whisper of a push-in, she lowers the tortoise-and-gold "
        "sunglasses onto her eyes with one fluid hand, the mirror-lens catching the gold "
        "sky; cheeks lifting beneath the lens.",
        "A serene, confident closed-lip smile lands as the water stills to a mirror around "
        "her ankles and the trailing hand settles \u2014 the calm after the rise.",
    ),
    # Frame 6 - high-angle wide loop close
    (
        "High-angle wide matching Frame 1: the camera is already drifting up and pulling "
        "back, exactly reversing the open, as she turns back toward the deck and the gown "
        "trails on the water; her gaze beginning its over-the-shoulder arc.",
        "The pull-back continues as the sea-silk softens back toward ivory linen at the "
        "trailing hem and the sunglasses slide up into her hair; a soft serene half-smile "
        "returning.",
        "She settles into the exact three-quarter-back, over-the-shoulder gaze of Frame 1, "
        "weight rolling to the deck-side foot, eyes warm \u2014 a frame-accurate loop seam.",
    ),
]


BEATS[2] = [
    # Frame 1 - low-angle medium-wide, car exit
    (
        "Low-angle medium-wide from the wet marble: the black-car door is already swinging "
        "open and a crane is rising off the heel as her gown slides out, one pointed satin "
        "heel reaching for the sapphire-lit step; gaze lowered to her footing.",
        "The crane keeps tilting up her body as the heel meets the wet marble and her weight "
        "commits, brass portico light raking up the midnight-blue satin; eyes beginning to "
        "lift.",
        "She rises to full height and lifts her gaze to the towering portico and revolving "
        "door, a knowing half-smile arriving, chin tipping down a touch in confident calm.",
    ),
    # Frame 2 - high-angle macro on the step (no face)
    (
        "High-angle macro on the marble step: the camera is already easing down toward the "
        "stone as the satin hem cascades and settles, the pointed heel rolling flat and its "
        "reflection forming in the wet mirror-floor.",
        "A slow drift follows the gloved hand as it enters frame and sets the box-clutch "
        "down beside the heel, oxblood nails crisp at the glove cuff.",
        "The trailing foot draws in beside the planted heel, weight grounding, the Deco "
        "diamond cuff throwing a travelling sparkle across the marble.",
    ),
    # Frame 3 - 3/4 front close-up, glove + glasses ritual
    (
        "Three-quarter front close-up: a slow push is already gliding toward her eyes as she "
        "smooths the long opera glove up her forearm mid-motion, lashes lowered to the "
        "gesture.",
        "The push eases into a micro-arc to three-quarter as she lowers the tinted gold-rim "
        "glasses onto her eyes, the lens catching a travelling specular; gaze sliding toward "
        "lens beneath the lashes.",
        "A slow, confident smile blooms toward camera on a soft inhale, lips parting a "
        "millimetre, eyes bright with intent toward the revolving door.",
    ),
    # Frame 4 - profile-to-front medium, revolving-door transform (SPOKEN)
    (
        "Profile-to-front medium: she is already pressing the brass push-bar and stepping "
        "into the revolving door as the camera begins to swing with the pane, sapphire night "
        "filling the glass; gaze forward through the door.",
        "The camera rides the door through its arc and the colour seam wipes across her "
        "body, midnight-blue satin shifting to deep emerald with warm gold blooming behind; "
        "eyes brightening behind the tint.",
        "She emerges into the emerald-gold lobby and turns her face to lens, a radiant "
        "knowing smile landing with the spoken line, brows lifting a hair in delight.",
    ),
    # Frame 5 - full-length wide, lobby runway walk
    (
        "Full-length wide down the one-point-perspective hall: she is already mid-stride out "
        "of the door into the emerald-gold lobby as a smooth dolly-back leads her, gown "
        "trailing, gaze level and proud.",
        "The dolly holds her centred through a confident runway walk toward lens, chandelier "
        "speculars sweeping the satin and hips driving the line; a soft proud smile steady.",
        "She eases her pace into a graceful settle and begins to turn, weight rolling onto "
        "the door-side foot, eyes softening toward the hall behind.",
    ),
    # Frame 6 - low-angle medium-wide, loop close
    (
        "Low-angle medium-wide matching Frame 1: a slow descend-and-tilt-down is already "
        "reversing the opening crane as she turns back toward the revolving door, the palette "
        "cooling toward sapphire; gaze beginning its over-the-shoulder arc.",
        "The descent continues as the emerald gown softens back toward midnight-blue at the "
        "trailing hem and the warm rim cools to brass; a knowing half-smile returning.",
        "She settles into the exact over-the-shoulder glance of Frame 1, weight on the "
        "door-side foot, eyes warm \u2014 a frame-accurate loop seam back to the arrival.",
    ),
]


BEATS[3] = [
    # Frame 1 - front-on medium-wide, neon awning threshold
    (
        "Front-on medium-wide under the glowing neon awning: she is already scanning the "
        "rain-slicked street from the dry threshold as a slow push drifts in with a faint "
        "handheld life, magenta-and-cyan signage mirrored across her cobalt vinyl trench; "
        "eyes tracing the falling rain.",
        "The push breathes closer as she shifts her weight forward and lifts a hand toward "
        "the tinted shield glasses, neon reflections racing along the vinyl; a cool, focused "
        "calm settling in her gaze.",
        "She steps her lead boot toward the rain line, intent building, eyes narrowing a "
        "touch with electric anticipation as the umbrella hand readies.",
    ),
    # Frame 2 - low macro on boot striking puddle (no face)
    (
        "Low macro on the cobalt boot: a fast-but-smooth push is already tracking the boot "
        "down toward a neon puddle, pink-and-cyan reflections trembling on the water's skin.",
        "Impact \u2014 the boot strikes and the splash crowns upward, neon reflections "
        "shattering into flying beads as the push eases.",
        "Droplets arc and fall on real ballistic paths, ripple rings racing outward and the "
        "shattered reflection beginning to knit back together \u2014 foreshadowing the freeze.",
    ),
    # Frame 3 - 3/4 back over-shoulder medium, walk + glance back
    (
        "Three-quarter back over-shoulder medium: she is already walking away into the neon "
        "street, umbrella up and rain sheeting off it, as the camera tracks behind her in a "
        "gentle arc.",
        "The arc catches her as she rotates her torso and glances back to lens, neon "
        "catchlights flaring in her eyes, a cool half-smile crossing her face.",
        "She faces forward again and her stride continues, energy coiling in the shoulders "
        "for the coming spin, gaze front.",
    ),
    # Frame 4 - front-on full, rain-freeze transform (bullet-time orbit)
    (
        "Front-on full, centred: she launches into the spin mid-turn, trench and ponytail "
        "flaring, as the camera begins a smooth 180\u00b0 orbit around her; gaze sweeping "
        "with the turn.",
        "At the spin apex the falling rain freezes into a glittering suspended ripple-sphere "
        "around her while the orbit keeps gliding through the held droplets; eyes widening in "
        "cool wonder, lips parting on a caught breath.",
        "Time releases, the droplets drop and the orbit carries on as she completes the turn, "
        "a confident half-smile landing, gaze settling forward.",
    ),
    # Frame 5 - profile medium-wide, walk on
    (
        "Profile medium-wide in clean side silhouette: she is already walking on through the "
        "rain as a lateral dolly tracks alongside at matched pace, the umbrella trailing a "
        "sheet of water; gaze level down the street.",
        "The dolly holds her stride steady and confident through the neon glow, reflections "
        "sliding along the vinyl; eyes calm, a faint satisfied set to the mouth.",
        "She begins to slow her pace, weight easing back, gaze drifting toward the awning "
        "behind to seed the turn.",
    ),
    # Frame 6 - front-on medium-wide loop close
    (
        "Front-on medium-wide matching Frame 1: a slow pull-back toward the awning is already "
        "reversing the opening push as she turns back toward the glowing doorway; gaze "
        "lifting to the neon light.",
        "The pull-back continues as the translucent umbrella closes and the tinted glasses "
        "slide up, rain sheeting off the awning edge; a cool, knowing calm returning to her "
        "face.",
        "She settles into the exact threshold stance of Frame 1, weight on the doorway-side "
        "foot, eyes tracing the rain again \u2014 a seamless loop seam.",
    ),
]


BEATS[4] = [
    # Frame 1 - 3/4 front medium, seated slipping on heel
    (
        "Three-quarter front medium: she is already guiding the heel-strap over her ankle on "
        "the velvet bench as a slow push drifts toward her hands, the tall gilt mirror "
        "glowing warm behind; gaze down on the buckle.",
        "The push settles as she presses the nude block heel home and flexes the ankle, the "
        "blush-tinted room soft around her; a small pleased smile beginning.",
        "She lifts her gaze toward the mirror, eyes brightening with curiosity, a soft "
        "playful smile forming as the reflection catches her.",
    ),
    # Frame 2 - profile medium-wide, lifting coat at rail
    (
        "Profile medium-wide: she is already lifting the blush wrap-coat onto her shoulders "
        "as a gentle lateral dolly glides with her toward the mirror; gaze following the "
        "coat into place.",
        "The dolly eases toward a stop as she adjusts the collar and shifts the bag to one "
        "hand, fabric settling; a light, breezy set to her mouth.",
        "She squares to face the mirror and lifts a hand toward the glass, eyes fixing on "
        "her reflection with playful intent.",
    ),
    # Frame 3 - front-on medium facing mirror, SWAP 1 blush->ivory
    (
        "Front-on medium facing the mirror: her fingertips are already meeting the glass as "
        "a slow push glides toward the touch-point, the surface beginning to shimmer.",
        "A swap-ripple radiates out from her fingertip and sweeps her body, the blush look "
        "re-dressing into the crisp ivory pantsuit while the whole room re-tints ivory.",
        "She reacts with a delighted grin, eyes dropping to take in the new look, cheeks "
        "lifting in bright surprise.",
    ),
    # Frame 4 - low-angle close-up, SWAP 2 ivory->emerald
    (
        "Low-angle close-up on her face and shoulder: her fingertips touch the glass again "
        "as a smooth crane begins to rise from below toward eye-level; gaze flicking to the "
        "mirror.",
        "The emerald ripple sweeps up her body and the room re-tints emerald as the crane "
        "lifts; eyes following the colour climbing, lips curving.",
        "At eye-level a confident playful smirk lands with a slow, delighted blink to her "
        "own reflection.",
    ),
    # Frame 5 - front-on full/wide hero, SPOKEN line
    (
        "Front-on full/wide hero: she is already settling into the emerald shirt-dress, hand "
        "finding her hip, as a slow push eases toward dead-front; gaze steady and pleased.",
        "She gestures lightly to the three faint past-look reflections shimmering in the "
        "glass, eyes flicking across them with playful pride.",
        "She turns fully to lens and delivers the spoken line with a radiant smile, brows "
        "lifting in light delight as the push settles.",
    ),
    # Frame 6 - 3/4 front medium loop close
    (
        "Three-quarter front medium matching Frame 1: she touches the glass one last time as "
        "a slow pull-back begins to reverse the opening push, the emerald softening back "
        "toward blush; gaze on the fading colour.",
        "The pull-back continues as the room warms back to blush and the accessories reform, "
        "a soft contented smile returning.",
        "She eases back toward the velvet bench into the exact seated lean of Frame 1, eyes "
        "drifting down to the heel again \u2014 a seamless loop seam.",
    ),
]


BEATS[5] = [
    # Frame 1 - low-angle medium-wide, stepping down from carriage
    (
        "Low-angle medium-wide from the platform boards: she is already steadying on the "
        "gleaming brass handrail and reaching a boot down from the carriage as a crane "
        "begins to rise toward her face; gaze down to her footing, dawn sky behind.",
        "The crane lifts as her weight transfers onto the weathered platform, the duster "
        "coat swinging; eyes beginning to rise.",
        "She straightens fully and lifts her gaze to the open desert, a soft awed breath, "
        "eyes warming in the peach-gold dawn.",
    ),
    # Frame 2 - high-angle macro on boot buckle (no face)
    (
        "High-angle macro on the boot at the platform step: her fingers are already "
        "threading the brass buckle strap as a slow push drifts in, sand grains scattered "
        "across the board.",
        "She cinches the buckle tight, the strap creasing, the push holding close on the "
        "deft fingers.",
        "She pats the boot and her hand lifts away, a thin trail of sand sifting off the "
        "leather.",
    ),
    # Frame 3 - 3/4 front medium, scarf tie in wind
    (
        "Three-quarter front medium on the open sand: she is already raising the long scarf "
        "as the wind catches it into a streaming ribbon, a slow arc swinging toward front; "
        "gaze following the cloth.",
        "The arc eases with a gentle push as she ties the scarf at her throat and it streams "
        "sideways, hair lifting; a free, happy set to her mouth.",
        "She lowers her hands and gazes to the horizon, a warm smile blooming, eyes bright "
        "with anticipation as the wind builds.",
    ),
    # Frame 4 - front-on full/wide hero, sand-to-gown transform (SPOKEN)
    (
        "Front-on full/wide hero: a gust is already lifting the desert sand around her into "
        "a swirling column as a crane begins to rise and orbit toward dead-front; gaze "
        "lifting with the rising sand.",
        "The sand swirls up her body and weaves into the flowing golden gown as the crane "
        "climbs; chin lifting, eyes widening in romantic awe, lips parting on a caught "
        "breath.",
        "Her arms bloom open and she turns fully to lens delivering the spoken line with a "
        "radiant smile, the gown settling in the wind, eyes alight.",
    ),
    # Frame 5 - profile wide, dune-crest walk
    (
        "Profile wide in side silhouette: she is already striding along the dune crest in "
        "the finished golden gown as a lateral dolly tracks alongside at matched pace, the "
        "gown trailing a ribbon of fine sand; gaze level to the horizon.",
        "The dolly holds her serene confident walk, the gown rippling and sand streaming "
        "behind; a calm, content smile.",
        "She slows her stride, weight easing, gaze drifting back toward the tiny train to "
        "seed the turn.",
    ),
    # Frame 6 - low-angle medium-wide loop close
    (
        "Low-angle medium-wide matching Frame 1: a slow descend-and-pull-back is already "
        "reversing the opening crane as she turns back toward the train; gaze beginning its "
        "over-the-shoulder arc.",
        "The descent continues as the golden gown dissolves back into the sand-toned travel "
        "set and accessories reform, sand sifting away; a soft warm smile returning.",
        "She settles into the over-the-shoulder glance echoing the opening, weight on the "
        "train-side foot, eyes warm in the dawn \u2014 a seamless loop seam.",
    ),
]


BEATS[6] = [
    # Frame 1 - front-on medium-wide, stepping into elevator
    (
        "Front-on medium-wide: she is already stepping over the threshold into the mirrored "
        "chrome elevator as a slow push follows her in, infinite reflections sliding behind "
        "and the LED strip glowing; gaze sweeping the car.",
        "The push glides as she draws the single statement opera glove up her arm, chrome "
        "speculars travelling; a cool, composed set to her eyes.",
        "She turns to the button panel and reaches, gaze fixing on the glowing button with "
        "editorial focus.",
    ),
    # Frame 2 - macro on gloved fingertip pressing button (no face)
    (
        "Extreme macro on the gloved fingertip: it is already approaching the glowing floor "
        "button as a slow push closes in, chrome reflections curving around it.",
        "The fingertip presses and the LED blooms ruby, light igniting under the glove.",
        "The ruby wash spills outward across the polished chrome, the mirror-reflections "
        "catching fire with colour.",
    ),
    # Frame 3 - profile medium, RUBY floor reveal
    (
        "Profile medium: the elevator chimes and the doors are already parting as a slow arc "
        "swings from profile toward three-quarter; gaze turning to the widening gap.",
        "Ruby light spills in across her body and the architectural jumpsuit re-tones ruby, "
        "the velvet hall blooming beyond; eyes catching the warm glow.",
        "She lowers the sculptural visor and gazes into the ruby hall, a cool powerful calm "
        "in her eyes.",
    ),
    # Frame 4 - low-angle close-up, COBALT floor
    (
        "Low-angle close-up: the doors are already sliding shut on ruby and reopening on a "
        "cobalt glass atrium as a smooth crane begins to rise from below; gaze flicking to "
        "the cool light.",
        "Cobalt light washes over her and the jumpsuit re-tones cobalt as the crane lifts "
        "toward eye-level; eyes cooling, brow settling into command.",
        "At eye-level she lifts her chin into the cool light with a confident set, gaze "
        "steady and bold.",
    ),
    # Frame 5 - front-on full/wide hero, GOLD floor
    (
        "Front-on full/wide hero: the doors are already opening fully on a gold-leaf gallery "
        "as she steps out and a slow push settles toward dead-front; gaze rising into the "
        "gold.",
        "She squares tall into the gold light, the jumpsuit fully re-toned gold and "
        "reflections glinting; eyes proud and luminous.",
        "She frames a powerful editorial pose, a radiant micro-smile landing to lens as the "
        "push locks.",
    ),
    # Frame 6 - front-on medium-wide loop close
    (
        "Front-on medium-wide matching Frame 1: a slow pull-back into the car is already "
        "reversing the opening push as she turns back toward the elevator; gaze following "
        "the chrome.",
        "The pull-back continues as the gold tone cools back to chrome-neutral and the visor "
        "slides up, reflections calming; a composed cool expression returning.",
        "She settles into the exact entry stance of Frame 1, weight on the threshold foot, "
        "eyes sweeping the mirrored car \u2014 a seamless loop seam.",
    ),
]


BEATS[7] = [
    # Frame 1 - front-on medium-wide, stepping onto runway
    (
        "Front-on medium-wide: she is already stepping onto the candy-striped runway rug "
        "with a light bounce as a slow push drifts in, pleated skirt swishing and the peach "
        "skyline glowing behind; eyes bright and happy.",
        "The push bounces gently closer as she reaches up and clips the heart sunglasses "
        "down onto her nose, a playful grin starting; gaze flicking to the balloons.",
        "She beams toward the sherbet balloons at the rug edge, cheeks lifting in joyful "
        "anticipation, eyes sparkling.",
    ),
    # Frame 2 - macro on hand closing on ribbons (no face)
    (
        "Extreme macro on her pastel-nailed hand: her fingers are already reaching into the "
        "balloon ribbons as a slow push closes in, sherbet balloons soft behind.",
        "She gathers and wraps the ribbons in her palm, the bundle bunching together.",
        "The ribbons tauten and tug upward as the balloons pull, her grip flexing against "
        "the lift.",
    ),
    # Frame 3 - 3/4 front medium, twirl + heels lifting
    (
        "Three-quarter front medium: she is already beginning to twirl with the balloons as "
        "a smooth arc follows her with a gentle rise, the pleated skirt flaring out; a "
        "delighted grin spreading.",
        "Her heels lift off the rug as the balloons pull her upward and the arc rises with "
        "her; eyes widening with giddy joy.",
        "She laughs openly as she floats up into the lift, gaze lifting to the balloons "
        "overhead, cheeks round with delight.",
    ),
    # Frame 4 - low-angle full/wide hero, balloon float (SPOKEN)
    (
        "Low-angle full/wide hero: the balloons are already lifting her off the rug as a "
        "smooth crane rises with her into a slow orbit to front, the city glowing below; "
        "eyes alight in weightless wonder.",
        "She floats up into a gentle weightless arc, skirt and hair drifting, the crane "
        "carrying the city behind; a buoyant joyful smile.",
        "She opens an arm and delivers the spoken line to lens with a laughing smile, eyes "
        "crinkling in pure delight.",
    ),
    # Frame 5 - profile medium-wide, drift down
    (
        "Profile medium-wide in side silhouette: she is already drifting back down as a "
        "smooth descend-and-track moves alongside, the balloons easing their pull; gaze soft "
        "toward the rug.",
        "Her pointed toe reaches for the candy-striped rug, the descent gentle; a content "
        "happy smile lingering.",
        "She settles her weight onto the rug and begins to turn back, eyes drifting toward "
        "the runway start.",
    ),
    # Frame 6 - front-on medium-wide loop close
    (
        "Front-on medium-wide matching Frame 1: a slow pull-back to the runway start is "
        "already reversing the opening push as she turns back; gaze sweeping the rooftop.",
        "The pull-back continues as the balloons settle at the rug edge and the heart "
        "sunglasses slide up into her hair; a bright easy smile returning.",
        "She settles into the exact entry stance of Frame 1, weight on the lead foot, eyes "
        "happy on the skyline \u2014 a seamless loop seam.",
    ),
]


BEATS[8] = [
    # Frame 1 - front-on medium-wide, entering aisle
    (
        "Front-on medium-wide: she is already stepping into the lantern-lit market aisle as "
        "a slow push glides down it, amber lanterns sliding past and the dupatta drifting; "
        "gaze lifting to the warm lights.",
        "The push follows her in as she gazes up at the strung lanterns and hanging "
        "garlands, a soft enchanted smile, eyes catching the amber glow.",
        "She reaches toward a hanging marigold garland, eyes warming with anticipation, "
        "fingertips brushing the blooms.",
    ),
    # Frame 2 - macro on hands lifting garland (no face)
    (
        "Extreme macro on her hands: she is already lifting a marigold garland upward as a "
        "slow push rises with it, petals and thread crisp in the lamp-light.",
        "She lowers the garland over her head, the loop of blooms passing down past the "
        "frame.",
        "It settles around her neck, petals shedding gently and drifting down \u2014 "
        "foreshadowing the bloom-burst.",
    ),
    # Frame 3 - profile medium, slipping on jutti
    (
        "Profile medium: she is already lifting one foot to a low stall step and guiding the "
        "jewelled jutti on as a slow arc swings from profile toward three-quarter; gaze down "
        "to the slipper.",
        "She presses the jutti home and lowers the foot, the arc easing round; a content "
        "festive calm in her eyes.",
        "She straightens and tucks the glasses away, gaze rising toward the glowing market "
        "centre with quiet expectation.",
    ),
    # Frame 4 - front-on full/wide hero, bloom-burst transform
    (
        "Front-on full/wide hero: she is already lifting a bundle of buds at the market "
        "centre as a crane begins to rise and orbit toward dead-front; gaze lifting to the "
        "buds.",
        "The buds burst and petals swirl up around her, weaving the marigold-and-jasmine "
        "flower-couture gown as the crane climbs; eyes widening in radiant awe, lips "
        "parting.",
        "Her arms bloom open and a radiant awed smile lands to lens, petals settling into "
        "the gown, eyes shining.",
    ),
    # Frame 5 - 3/4 back over-shoulder medium, walk + glance
    (
        "Three-quarter back over-shoulder medium: she is already walking on through the "
        "market in the flower gown as the camera tracks behind in a gentle arc, the "
        "petal-train trailing; gaze ahead down the aisle.",
        "The arc catches her as she rotates her torso and glances back to lens, lantern-"
        "light warm in her eyes, a soft proud smile.",
        "She faces forward again and her stride continues, petals drifting in her wake, gaze "
        "settling front.",
    ),
    # Frame 6 - front-on medium-wide loop close
    (
        "Front-on medium-wide matching Frame 1: a slow pull-back to the aisle entrance is "
        "already reversing the opening push as she turns back; gaze sweeping the lanterns.",
        "The pull-back continues as the flower gown dissolves back into the embroidered "
        "kurta-set and the garland reforms at her neck; a soft warm smile returning.",
        "She settles into the exact entry stance of Frame 1, weight on the lead foot, eyes "
        "warm on the glowing aisle \u2014 a seamless loop seam.",
    ),
]


BEATS[9] = [
    # Frame 1 - 3/4 front medium, towel to face
    (
        "Three-quarter front medium at the marble basin: she is already pressing a warm face "
        "towel to her cheeks as a slow push drifts toward her face, steam drifting and the "
        "backlit mirror glowing behind; eyes softly closed in calm.",
        "The push settles as she draws the towel slowly down with a contented exhale, skin "
        "dewy; lids beginning to lift.",
        "She opens her eyes to the mirror, a serene smile forming, gaze warm and luminous.",
    ),
    # Frame 2 - macro on misting spritz (no face)
    (
        "Extreme macro on her hand: she is already raising the glowing skincare bottle "
        "toward her face as a slow push closes in, the nozzle catching the light.",
        "She presses the pump and a fine mist fans out, droplets hanging in a rack-focused "
        "shimmer.",
        "The droplets settle and catch the morning light as she breathes them in, the haze "
        "drifting up.",
    ),
    # Frame 3 - low-angle macro on slipper (no face)
    (
        "Low-angle macro on the warm marble floor: her foot is already hovering over the "
        "pearl-satin mule as a slow push follows it down.",
        "The foot slides into the slipper, the satin flexing and creasing around the arch.",
        "She settles her weight and the heel seats, a pearl sheen travelling across the "
        "satin.",
    ),
    # Frame 4 - profile medium, steam-reveal transform
    (
        "Profile medium: warm steam is already billowing up from the basin as a crane begins "
        "to rise with a slow arc from profile toward three-quarter; gaze following the "
        "rising steam.",
        "The steam wraps her body and resolves into the pearl-couture gown as the crane "
        "climbs; chin lifting, eyes softening in serene awe, lips parting on a gentle "
        "breath.",
        "Her arms bloom and her hair releases in the warm air, a serene awed smile arriving, "
        "eyes luminous.",
    ),
    # Frame 5 - front-on full/wide hero (SPOKEN)
    (
        "Front-on full/wide hero before the backlit mirror: she is already settling into the "
        "finished pearl gown, a hand rising to her collarbone, as a slow push eases toward "
        "dead-front; gaze soft and glowing.",
        "She turns softly to lens, the pearl satin catching the mirror's halo, eyes warm and "
        "calm.",
        "She delivers the spoken line with a radiant serene smile, cheeks lifting gently as "
        "the push settles.",
    ),
    # Frame 6 - 3/4 front medium loop close
    (
        "Three-quarter front medium matching Frame 1: a slow pull-back to the basin is "
        "already reversing the opening push as she turns back; gaze drifting toward the "
        "marble.",
        "The pull-back continues as the pearl gown softens back into the ivory silk robe and "
        "the warm towel reappears in her hand; a soft serene smile returning.",
        "She settles into the exact ritual stance of Frame 1, weight grounded at the basin, "
        "eyes calm on the mirror \u2014 a seamless loop seam.",
    ),
]


BEATS[10] = [
    # Frame 1 - front-on medium-wide corridor, suspense
    (
        "Front-on medium-wide down the charcoal corridor: she is already drawing the second "
        "glove on as a slow suspenseful push glides toward the glowing red door behind her, "
        "amber sconces pooling; gaze low and focused.",
        "The push creeps closer as she squares to the red door and lowers her gaze to the "
        "brass handle, jaw set; eyes steady with resolve.",
        "She lifts a hand toward the handle, resolve building, eyes narrowing a touch in "
        "dramatic focus.",
    ),
    # Frame 2 - macro on gloved hand on handle (no face)
    (
        "Extreme macro on her gloved hand: it is already rising into frame toward the brass "
        "handle as a slow push closes in, red lacquer glowing behind.",
        "The fingers wrap the handle, leather creasing around the cool brass.",
        "The handle turns and the door begins to give, a sliver of light breaking at the "
        "seam.",
    ),
    # Frame 3 - profile medium, fastening boot
    (
        "Profile medium: she is already pulling the zip of one black ankle boot on a raised "
        "foot at a low ledge as a slow arc swings from profile toward three-quarter; gaze "
        "down to the boot.",
        "She lowers the foot and presses it home, the arc easing round; a quiet "
        "determination in her eyes.",
        "She straightens and her gaze rises to the red door, hand returning to the handle "
        "with renewed resolve.",
    ),
    # Frame 4 - profile-to-front medium, world-flip transform (SPOKEN)
    (
        "Profile-to-front medium: she is already pushing the red door and stepping through "
        "as the camera begins to swing with it, the dark corridor still behind; gaze forward "
        "into the gap.",
        "The camera rides the door through its arc and the world-seam crosses her body, "
        "flipping the charcoal corridor to sunlit terrace and the trench to the ivory-gold "
        "gown; eyes brightening as the light hits.",
        "She emerges into the sun and turns her face to lens, delivering the spoken line "
        "with a radiant released smile, brows lifting in warmth.",
    ),
    # Frame 5 - full-length wide, terrace walk
    (
        "Full-length wide: she is already striding onto the sunlit rooftop terrace from the "
        "door as a smooth dolly-back leads her, white drapes billowing and blue sky behind; "
        "gaze open and free.",
        "The dolly holds her centred through a confident free walk into the sun, the "
        "ivory-gold gown flowing; a serene radiant smile.",
        "She eases her pace into a serene settle and begins to turn, weight rolling onto the "
        "door-side foot, eyes softening back toward the threshold.",
    ),
    # Frame 6 - front-on medium-wide loop close
    (
        "Front-on medium-wide matching Frame 1: a slow push back into the corridor is "
        "already reversing the opening move as she turns back toward the red door at the "
        "threshold; gaze drifting to the door.",
        "The push continues as the world and look flip back toward the charcoal corridor and "
        "tailored trench, sunlight giving way to amber sconce-glow; a composed dramatic calm "
        "returning.",
        "She settles into the exact stance of Frame 1 before the door, weight grounded, eyes "
        "low on the handle \u2014 a seamless loop seam.",
    ),
]


BEATS[11] = [
    # Frame 1 - wide establishing, glide
    (
        "Wide establishing down the submerged marble gallery: she is already gliding between "
        "glowing columns mid-frame as a weightless glide-forward drifts with her, hair "
        "fanning slowly in the current; eyes wide with awe.",
        "The glide carries her deeper as she scans the glowing artifacts on their pedestals, "
        "caustic shafts raining down; gaze tracing the light, lips parted in wonder.",
        "She angles her body toward a floating pedestal ahead, eyes locking onto a glowing "
        "orb, drawn forward.",
    ),
    # Frame 2 - macro on hand closing on orb (no face)
    (
        "Extreme macro: her hand is already drifting toward the glowing artifact orb as a "
        "slow push closes in, motes and bubbles rising past.",
        "Her fingers close around the orb and its glow surges, light leaking between them.",
        "She lifts the orb gently off the pedestal, the light flaring and casting moving "
        "caustics.",
    ),
    # Frame 3 - profile medium, cradling orb
    (
        "Profile medium: she is already drawing the glowing orb to her chest, hovering "
        "upright as a slow arc swings from profile toward three-quarter; hair drifting, gaze "
        "down into the glow.",
        "She gazes into the brightening orb as the arc eases round, its light warming her "
        "face; eyes softening in mystified awe.",
        "She begins to lift it outward as the light starts to spill, gaze rising with the "
        "glow.",
    ),
    # Frame 4 - front-on full/wide hero, light-bloom transform
    (
        "Front-on full/wide hero: she is already raising the orb aloft as a weightless crane "
        "rises with a slow orbit to dead-front; gaze following the orb up, eyes brightening.",
        "The light blooms outward and weaves the luminous gown around her as the crane "
        "climbs; chin lifting, eyes widening in radiant awe, hair fanning.",
        "Her arms open and a radiant awed smile lands to lens, the gown shimmering with "
        "artifact-light, eyes alight.",
    ),
    # Frame 5 - 3/4 back over-shoulder medium, drift + glance
    (
        "Three-quarter back over-shoulder medium: she is already drifting onward through the "
        "gallery in the luminous gown as a weightless tracking follow trails her, the "
        "light-train streaming; gaze ahead.",
        "The arc catches her as she rotates her torso and glances back to lens, caustics "
        "dancing in her eyes, a soft awed smile.",
        "She faces forward again and her glide continues, light trailing in her wake, gaze "
        "settling front.",
    ),
    # Frame 6 - wide loop close
    (
        "Wide matching Frame 1: a slow drift-back through the gallery is already reversing "
        "the opening glide as she turns back into it; gaze sweeping the glowing columns.",
        "The drift continues as the light-gown dissolves back into the teal swim-couture and "
        "the orb returns to its pedestal; a soft awed calm returning.",
        "She settles into the exact glide stance of Frame 1, body weightless between the "
        "columns, eyes wide on the artifacts \u2014 a seamless loop seam.",
    ),
]


BEATS[12] = [
    # Frame 1 - wide establishing, push off wall
    (
        "Wide establishing of the luminous pod: she is already pushing gently off a curved "
        "wall and drifting mid-frame as a weightless drift-in with a faint roll matches her "
        "float, the vast Earth-window behind; eyes wide with wonder.",
        "The drift carries her as she scans the pod and the blue Earth beyond, hair lifting "
        "in the zero-G; gaze tracing the starfield, lips parted.",
        "She reaches toward a floating chrome boot, eyes locking onto it, drawn through the "
        "weightless air.",
    ),
    # Frame 2 - macro on guiding boot (no face)
    (
        "Extreme macro: the floating chrome boot is already drifting toward her pointed foot "
        "as a slow push follows, LED strips reflecting on it.",
        "Her hands guide it onto the foot, fingers closing the seam mid-air.",
        "It seats with a settling chrome glint, the foot pointing as it locks on.",
    ),
    # Frame 3 - profile medium, tapping console
    (
        "Profile medium: she is already reaching for the glowing console, floating upright, "
        "as a weightless arc swings from profile toward three-quarter; hair drifting, gaze "
        "on the panel.",
        "She taps the console and it flares, the arc easing round; eyes brightening with "
        "anticipation.",
        "Iridescent fabric panels begin to drift in from the pod edges as she turns toward "
        "them, gaze following the floating cloth.",
    ),
    # Frame 4 - front-on full/wide hero, anti-gravity dress transform
    (
        "Front-on full/wide hero, floating centred: the iridescent panels are already "
        "drifting in toward her as a weightless orbit eases to dead-front with a slow "
        "drift-in; gaze tracking the converging cloth.",
        "The panels assemble into the couture gown around her weightless body; chin "
        "lifting, eyes widening in radiant wonder, hair fanning out.",
        "Her arms open and a radiant awed smile lands to lens, the gown settling around her "
        "in the zero-G, eyes alight.",
    ),
    # Frame 5 - 3/4 back over-shoulder medium, drift to window + glance
    (
        "Three-quarter back over-shoulder medium: she is already drifting toward the "
        "Earth-window in the couture gown as a weightless tracking follow trails her, the "
        "panel-train streaming; gaze toward the blue planet.",
        "The arc catches her as she rotates her torso and glances back to lens, Earth-light "
        "glowing in her eyes, a soft awed smile.",
        "She faces the window again and her drift continues, panels trailing in her wake, "
        "gaze settling on Earth.",
    ),
    # Frame 6 - wide loop close
    (
        "Wide matching Frame 1: a slow weightless drift-back is already reversing the "
        "opening drift-in as she turns back into the pod; gaze sweeping the curved panels.",
        "The drift continues as the couture gown dissolves back into the space-suit "
        "base-layer and the floating orbs disperse; a soft wondering calm returning.",
        "She settles into the exact float stance of Frame 1, reaching once more for the "
        "floating boot, eyes wide on the Earth-window \u2014 a seamless loop seam.",
    ),
]


BEATS[13] = [
    # Frame 1 - wide establishing, kneeling at water
    (
        "Wide establishing of the riverside: she is already kneeling at the water's edge "
        "cradling a paper lantern as a slow drift-in and gentle crane-down move toward her, "
        "the dark river mirroring the first rising lights; gaze soft on the water.",
        "The crane settles as she slips on a jutti and settles her weight, glowing lanterns "
        "around her; a hopeful warmth in her eyes.",
        "She lifts the lantern, ready to light it, eyes catching the amber flame-glow, lips "
        "parting in quiet hope.",
    ),
    # Frame 2 - macro on tying glowing ribbon (no face)
    (
        "Extreme macro: her fingers are already looping the glowing ribbon of light at her "
        "wrist as a slow push closes in, the lit lantern glowing just beyond.",
        "She draws the ribbon snug at the wrist, the loop tightening into a knot.",
        "The ribbon-glow surges as the knot sets, light pulsing up her wrist \u2014 "
        "foreshadowing the gown.",
    ),
    # Frame 3 - profile medium, rising + lifting lantern
    (
        "Profile medium: she is already rising to her feet and lifting the lit lantern "
        "toward her face as a slow arc swings from profile toward three-quarter; hair and "
        "dupatta stirring, gaze into the flame.",
        "She whispers a wish to the flame, the arc easing round and lantern-light warming "
        "her profile; eyes closing softly then opening with hope.",
        "She draws the lantern back, ready to release it upward, gaze lifting to the night "
        "sky.",
    ),
    # Frame 4 - front-on full/wide hero, lantern-light gown transform (SPOKEN)
    (
        "Front-on full/wide hero: she is already releasing the lantern skyward as a crane "
        "begins to rise and orbit toward dead-front, a thousand lanterns lifting around her; "
        "gaze following them up, eyes shining.",
        "The streaming light pours down and weaves the glowing festival gown around her as "
        "the crane climbs; chin lifting, eyes widening in radiant wonder.",
        "Her arms open and a radiant smile lands as she delivers the spoken line to lens, "
        "the gown blazing with lantern-light, eyes joyful.",
    ),
    # Frame 5 - 3/4 back over-shoulder medium, sky-watch + glance
    (
        "Three-quarter back over-shoulder medium: she is already watching the lantern-filled "
        "sky and reaching upward in the glowing gown as a tracking arc rises behind her "
        "toward the lights; gaze up among the lanterns.",
        "The arc curves back to catch her as she rotates her torso and glances back to lens, "
        "lantern-glow warm in her eyes, a soft joyful smile.",
        "She faces the sky again, light trailing from the gown, gaze drifting up after the "
        "rising lanterns.",
    ),
    # Frame 6 - wide loop close
    (
        "Wide matching Frame 1: a slow drift-out and crane-up is already reversing the "
        "opening move as she kneels back toward the water's edge; gaze lowering to the "
        "river.",
        "The drift continues as the lantern-light gown dissolves back into the indigo "
        "festival set and a fresh lantern returns to her hands; a soft hopeful warmth "
        "returning.",
        "She settles into the exact kneel of Frame 1 at the water, eyes soft on the "
        "mirrored lights \u2014 a seamless loop seam.",
    ),
]


BEATS[14] = [
    # Frame 1 - wide establishing, stepping into arcade
    (
        "Wide establishing down the glowing arcade aisle: she is already stepping in between "
        "the cabinets as a slow glide-in moves toward her, CRT glow and laser-grid behind; "
        "eyes scanning the neon with cool delight.",
        "The glide carries closer as she slips on a sneaker at a cabinet step and pockets "
        "the token, the checkerboard floor lit beneath; a playful set to her mouth.",
        "She steps toward a big glowing cabinet button, eyes locking onto it with "
        "mischievous anticipation.",
    ),
    # Frame 2 - macro on finger pressing button (no face)
    (
        "Extreme macro: her finger is already descending toward the big glowing arcade "
        "button as a slow push closes in, light pooling beneath the fingertip.",
        "She presses and the glow surges up around her fingertip, the button depressing.",
        "The glow flares and a scanline ripple breaks outward as the first decade-shift "
        "triggers.",
    ),
    # Frame 3 - profile medium, SHIFT 1 70s->80s
    (
        "Profile medium: the glitch is already triggering as a slow arc swings from profile "
        "toward three-quarter, a scanline ripple breaking across her body; gaze flicking "
        "down at herself.",
        "The scanline-wipe shifts her 70s jumpsuit to the 80s power-blazer and re-tints the "
        "arcade magenta-cyan; eyes widening with playful surprise.",
        "She reacts with a delighted grin, checking the new look, cheeks lifting in bright "
        "amusement.",
    ),
    # Frame 4 - low-angle close-up, SHIFT 2 80s->90s
    (
        "Low-angle close-up on her face and shoulder: the second press glitches as a smooth "
        "crane begins to rise from below toward eye-level; gaze catching the green flicker.",
        "The grunge-green glitch sweeps up her body and the arcade re-tints as the crane "
        "lifts; eyes following the colour, lips curving.",
        "At eye-level a confident playful smirk lands with a slow, delighted blink.",
    ),
    # Frame 5 - front-on full/wide hero (SPOKEN)
    (
        "Front-on full/wide hero: she is already settling into the clean-now look, hand "
        "finding her hip, as a slow push eases toward dead-front; gaze cool and pleased.",
        "She gestures to the faint decade-ghosts glitching in the CRTs behind, eyes flicking "
        "across them with playful pride.",
        "She turns fully to lens and delivers the spoken line with a radiant smile, brows "
        "lifting in playful confidence.",
    ),
    # Frame 6 - wide loop close
    (
        "Wide matching Frame 1: a slow glide-out down the aisle is already reversing the "
        "opening glide-in as she turns back; gaze sweeping the cabinets.",
        "The glide continues as the now-look glitches back to the 70s jumpsuit and the token "
        "returns to her hand; a cool playful smile returning.",
        "She settles into the exact stance of Frame 1 in the aisle, eyes bright on the neon "
        "\u2014 a seamless loop seam.",
    ),
]


BEATS[15] = [
    # Frame 1 - wide establishing, turntable centre
    (
        "Wide establishing of the ice-palace music box: she is already standing at the "
        "centre of the mirrored turntable slipping on a crystal-heel slipper as a slow "
        "drift-in and crane-down move toward her, gilded gears turning overhead; gaze calm "
        "and dreamy.",
        "The crane settles as she lifts the giant golden wind-key, snow-glitter falling "
        "around her; eyes warming with anticipation.",
        "She sets the key to wind and the gears engage with a glint, gaze rising to the "
        "slow-turning gears above.",
    ),
    # Frame 2 - macro on winding key (no face)
    (
        "Extreme macro: her hands are already gripping the giant golden wind-key as a slow "
        "push closes in, gears catching gold glints behind.",
        "She turns the key and the gears engage, teeth meshing with a frosted shimmer.",
        "A final wind-click lands as the mirrored turntable begins to spin beneath her.",
    ),
    # Frame 3 - profile medium, rising onto toes
    (
        "Profile medium: she is already rising onto her toes like a music-box figurine as "
        "the turntable begins to spin her and a slow arc swings from profile toward "
        "three-quarter; tulle drifting, gaze lifting.",
        "Her arms lift into the figurine pose as the turntable spins, the arc easing round; "
        "a serene dreamy calm in her eyes.",
        "She begins the spin into the crystallise, gaze sweeping with the turn, lips parting "
        "softly.",
    ),
    # Frame 4 - front-on full/wide hero, spin-freeze crystal transform
    (
        "Front-on full/wide hero, spinning centred: she is already reaching the spin apex as "
        "a smooth orbit glides around her, snow-glitter trailing; gaze bright with the "
        "turn.",
        "Frost races across the gown and crystallises it into the frosted couture gown of "
        "frozen light as the orbit keeps gliding through the suspended glitter; eyes "
        "widening in dreamy awe, lips parting.",
        "Her arms open and a radiant awed smile lands, curls and snow-glitter fanning "
        "outward, eyes luminous.",
    ),
    # Frame 5 - 3/4 back over-shoulder medium, wind-down + glance
    (
        "Three-quarter back over-shoulder medium: she is already slowing from the spin in "
        "the frosted gown as a tracking arc trails her, the frost-train streaming and the "
        "box winding down; gaze ahead.",
        "The arc catches her as she rotates her torso and glances back to lens, gear-glints "
        "warm in her eyes, a soft serene smile.",
        "She faces forward again as the turntable winds down, frost-light trailing, gaze "
        "settling front.",
    ),
    # Frame 6 - wide loop close
    (
        "Wide matching Frame 1: a slow drift-out and crane-up is already reversing the "
        "opening move as she settles back to the turntable centre; gaze lowering to the "
        "mirror floor.",
        "The drift continues as the frost-gown dissolves back into the pale-blue "
        "velvet-and-tulle gown and the wind-key returns to her hand; a soft dreamy calm "
        "returning.",
        "She settles into the exact centre stance of Frame 1, eyes calm under the turning "
        "gears \u2014 a seamless loop seam.",
    ),
]


BEATS[16] = [
    # Frame 1 - wide establishing, walking glasshouse aisle
    (
        "Wide establishing down the glasshouse aisle: she is already walking onto the mossy "
        "path as a slow glide-in moves toward her, ferns and climbing roses arching "
        "overhead; eyes scanning the dappled greenery with delight.",
        "The glide carries closer as she slips on a garden flat and steadies the seed-pot, "
        "dappled sun crossing her; a fresh, happy calm in her gaze.",
        "She steps toward the soil bed, eyes settling on the rich dark earth with gentle "
        "anticipation.",
    ),
    # Frame 2 - macro on pressing seed (no face)
    (
        "Extreme macro: her fingers are already pressing a seed into rich dark soil as a "
        "slow push closes in, crumbs of earth shifting.",
        "She pats the soil and a green sprout breaks the surface, unfurling toward the "
        "light.",
        "The sprout surges upward as the bloom triggers, tendrils racing out from where she "
        "touched.",
    ),
    # Frame 3 - profile medium, vines climbing
    (
        "Profile medium: she is already rising as the first vines climb around her and a "
        "slow arc swings from profile toward three-quarter; gaze following the racing "
        "greenery.",
        "Blossoms open and a vine curls around her wrist where she gestures, the arc easing "
        "round; eyes brightening in enchanted wonder.",
        "She begins the bloom-spin into the forming gown, gaze sweeping with the turn, a "
        "delighted breath.",
    ),
    # Frame 4 - front-on full/wide hero, plant-growth bloom transform
    (
        "Front-on full/wide hero, spinning centred: she is already reaching the bloom apex "
        "as a smooth orbit glides around her, leaves whirling; gaze bright with the turn.",
        "Vines and blossoms weave into the living floral couture gown as the orbit keeps "
        "gliding through the suspended petals; eyes widening in radiant awe, lips parting.",
        "Her arms open and a radiant awed smile lands, petals flung outward on real arcs, "
        "eyes alight.",
    ),
    # Frame 5 - 3/4 front cowboy/full (SPOKEN)
    (
        "Three-quarter front cowboy/full: she is already settling into the floral gown amid "
        "the blooming glasshouse as a slow push eases toward three-quarter front; gaze warm "
        "and fresh.",
        "She gestures lightly to the blooming garden around her, eyes flicking across the "
        "opening blossoms with bright pride.",
        "She turns to lens and delivers the spoken line with a radiant smile, cheeks lifting "
        "in gentle delight.",
    ),
    # Frame 6 - wide loop close
    (
        "Wide matching Frame 1: a slow glide-out down the aisle is already reversing the "
        "opening glide-in as she turns back; gaze sweeping the greenery.",
        "The glide continues as the floral gown softens back into the sage-linen set and the "
        "seed-pot returns to her hand; a fresh content smile returning.",
        "She settles into the exact stance of Frame 1 on the mossy path, eyes soft on the "
        "arching ferns \u2014 a seamless loop seam.",
    ),
]


BEATS[17] = [
    # Frame 1 - wide establishing, kitchen island
    (
        "Wide establishing down the copper kitchen: she is already stepping to the marble "
        "island as a slow glide-in moves toward her, hanging copper pans gleaming overhead; "
        "eyes scanning the warm range with lively focus.",
        "The glide carries closer as she slips on a clog and ties the wrap-apron, pendant "
        "light warming her; a confident, easy set to her mouth.",
        "She lifts the copper pan toward the flaming range, eyes catching the blue flame, "
        "anticipation rising.",
    ),
    # Frame 2 - macro on pan toss (no face)
    (
        "Extreme macro on the copper pan: her wrist is already setting the pan over the "
        "flame as a slow push closes in, flour-dust catching the light.",
        "She flicks the toss and spices arc upward with a curl of blue flame, the pan "
        "sweeping.",
        "The swirl of flour, steam and spice-light rises as the flare triggers, embers "
        "tumbling.",
    ),
    # Frame 3 - profile medium, swirl wrapping
    (
        "Profile medium: she is already rising as the swirl of flour, steam and spice-light "
        "begins to wrap her and a slow arc swings from profile toward three-quarter; gaze "
        "following the rising swirl.",
        "The apron begins to re-plate into silk and a ribbon of spice-light curls her wrist "
        "where she gestures, the arc easing round; eyes brightening in warm wonder.",
        "She begins the flourish-spin into the forming gown, gaze sweeping with the turn, a "
        "delighted breath.",
    ),
    # Frame 4 - front-on full/wide hero, apron-to-couture flare transform
    (
        "Front-on full/wide hero, spinning centred: she is already reaching the flare apex "
        "as a smooth orbit glides around her, spice-light whirling; gaze bright with the "
        "turn.",
        "The swirl re-plates her apron into the flowing saffron-and-cream couture gown as "
        "the orbit keeps gliding through the suspended embers; eyes widening in radiant awe, "
        "lips parting.",
        "Her arms open and a radiant awed smile lands, spice-light flung outward on real "
        "arcs, eyes alight.",
    ),
    # Frame 5 - 3/4 front cowboy/full (SPOKEN)
    (
        "Three-quarter front cowboy/full: she is already settling into the couture gown at "
        "the marble island as a slow push eases toward three-quarter front; gaze warm and "
        "assured.",
        "She gestures with a confident flourish to the warm copper kitchen, eyes flicking "
        "across the gleaming pans with bright pride.",
        "She turns to lens and delivers the spoken line with a radiant smile, cheeks lifting "
        "in lively delight.",
    ),
    # Frame 6 - wide loop close
    (
        "Wide matching Frame 1: a slow glide-out is already reversing the opening glide-in "
        "as she turns back to the island; gaze sweeping the copper.",
        "The glide continues as the couture gown softens back into the cream chef's set and "
        "the copper pan returns to her hand; a warm content smile returning.",
        "She settles into the exact stance of Frame 1 at the island, eyes on the range "
        "\u2014 a seamless loop seam.",
    ),
]


def build_block(beats):
    # Replaces ONLY the `SUBJECT ACTION w/ BEAT-TIMING:` header + its bullet
    # beat lines. Whatever follows (a blank line then SPOKEN LINE or
    # FLUIDITY & WEIGHT NOTES) is left untouched, so spoken-line frames keep
    # their dialogue. Ends with a single trailing newline so the original
    # blank line that followed the beats still separates the next section.
    return (
        BREAKDOWN_HEADER + "\n"
        f"- [00:00\u201300:02] {beats[0]}\n"
        f"- [00:02\u201300:04] {beats[1]}\n"
        f"- [00:04\u201300:06] {beats[2]}\n\n"
        + FRAME_RATE_LINE + "\n\n"
        + DURATION_LINE + "\n"
    )


def apply_concept(text, concept_no):
    frames = BEATS[concept_no]
    start = text.index(f"# CONCEPT {concept_no} \u2014")
    nxt = re.search(rf"# CONCEPT {concept_no + 1} \u2014", text)
    end = nxt.start() if nxt else len(text)
    region = text[start:end]

    # 1) drop the standalone camera line (+ its trailing blank line)
    region, n_cam = re.subn(
        r"CAMERA MOVEMENT \(CHOREOGRAPHY\): [^\n]*\n\n", "", region
    )

    # 2) replace each SUBJECT ACTION block in order
    state = {"i": 0}

    def repl(_m):
        beats = frames[state["i"]]
        state["i"] += 1
        return build_block(beats)

    region, n_act = re.subn(
        r"SUBJECT ACTION w/ BEAT-TIMING:\n(?:- .*\n)+",
        repl,
        region,
    )

    assert n_act == len(frames), (
        f"concept {concept_no}: replaced {n_act} action blocks but have "
        f"{len(frames)} frame breakdowns"
    )
    assert state["i"] == len(frames)
    print(
        f"concept {concept_no}: removed {n_cam} camera lines, "
        f"rebuilt {n_act} video breakdowns"
    )
    return text[:start] + region + text[end:]


def main():
    concept_no = int(sys.argv[1])
    with open(PATH, encoding="utf-8") as fh:
        text = fh.read()
    text = apply_concept(text, concept_no)
    with open(PATH, "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()

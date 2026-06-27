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

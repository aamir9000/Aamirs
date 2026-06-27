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

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
        r"SUBJECT ACTION WITH TIMING:\n(?:- .*\n)+", repl, region
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

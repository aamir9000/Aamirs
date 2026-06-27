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

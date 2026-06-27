#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced video-prompt rebuild engine for
CONCEPTS/20 Full Reel Concepts Set 5 (Concepts 71.txt   (concepts 71-79, all SILENT)

Same Beauty-Ad markdown format and same transform as _tools/set4_rebuild.py:
per VIDEO prompt remove the standalone `CAMERA MOVEMENT:` line, replace
`SUBJECT ACTION WITH TIMING` with a tailored timed 3-beat `SHOT BREAKDOWN`,
and reset the existing `DURATION:` and `FRAME RATE + MOTION BLUR:` lines to the
6-second standard strings.

NOTE: concept 79 is CORRUPTED in the source (only Frame 1 of 7 present, then
merged leftover fragments from concept 78). Do NOT run this engine on 79 — its
region has mismatched DURATION/FRAME RATE counts. Concept 79 Frame 1 is handled
separately/surgically.

All concepts here are silent: Frame 4-ish wordless beats use an expression
reveal, no spoken line.

Idempotent. Usage:  python3 _tools/set5_rebuild.py <concept_number>
"""
import re
import sys

PATH = "CONCEPTS/20 Full Reel Concepts Set 5 (Concepts 71.txt"

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

BEATS[71] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts "
        "the emerald oil bottle a few degrees into the sun, speculars sliding along the "
        "glass and the green-gold oil settling inside; gaze lowered to the glass.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a serene "
        "half-smile blooms, golden-green conservatory light warming her face.",
        "She holds, calm and luminous, a loose tendril drifting at her temple, eyes soft and "
        "direct.",
    ),
    # F2 - medium transform showpiece (majestic 20deg arc + boom, track the growth)
    (
        "Medium transformation showpiece: a slow majestic 20\u00b0 arc with a gentle boom-rise "
        "is already tracking the growth as vines race up from the hem and the velvet "
        "dissolves into a leaf-bodice; gaze following the climbing green.",
        "The arc keeps rising as leaves unfurl in waves up the skirt and arms and vivid buds "
        "swell, she beginning her slow quarter-turn; a wondering breath, brows lifting in "
        "awe.",
        "The couture gown locks in with buds poised to bloom and a flurry of pollen-light "
        "lifting as the arc eases; she settles into the finished silhouette, calm and "
        "radiant.",
    ),
    # F3 - beauty close, product-at-cheek hero (6% push to cheekbone)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her cheekbone is "
        "already gliding in as she brings the open bottle to her cheek, a luminous oil-drop "
        "swelling at the tip; eyes lowered to the touch.",
        "The drop glides to the skin and blooms a dewy sheen, the push settling; lashes "
        "lowering, a serene focus holding.",
        "She lifts her eyes to lens with a serene micro-smile, the glow set, leaf-bodice "
        "glinting in her gaze.",
    ),
    # F4 - bold beauty close, wordless hero beat (SILENT — expression reveal)
    (
        "Bold beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes lock the lens with a confident radiant half-smile, "
        "the bottle presented at her chest (silent \u2014 no words).",
        "She lands a single assured chin-lift into a slow blink as a warm glass glint "
        "flickers across the bottle, lips softly closed, the look itself doing the work.",
        "The half-smile holds, eyes luminous and direct \u2014 a wordless expression reveal in "
        "place of any line.",
    ),
    # F5 - full-figure magical grand hero, blossom-bloom burst (push + boom-rise)
    (
        "Full-figure magical grand hero from a slightly low angle: a slow majestic push-in "
        "with a gentle boom-rise is already lifting as a single bud at the heart of the "
        "bodice splits and flares its first vivid petal; gaze drawn to the opening bud.",
        "The boom keeps rising as the bloom races outward bud to bud, petal-confetti and "
        "pollen-light swirling around her and the topiary blooming behind; eyes lifting into "
        "the swirl, a radiant awe blooming.",
        "The petals trail out, easing to a sustained drifting halo as the move settles; her "
        "radiant smile landing, eyes triumphant and haloed.",
    ),
    # F6 - perfect-loop close (settle back to F1)
    (
        "Medium close chest-up easing toward the Frame 1 framing: a slow settle-back is "
        "already reversing the opening push as the blossom-bloom eases out and the last "
        "petals drift down; she begins settling toward her opening posture, gaze softening.",
        "The settle continues as she cradles the bottle at the collarbone and the "
        "conservatory eases fully back to its calm Frame 1 look; a soft serene smile easing "
        "in, eyes calming.",
        "She lands exactly on the opening posture, framing and headroom matched, holding "
        "still for the seamless hand-back \u2014 a frame-accurate loop seam.",
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
    concept_no = int(sys.argv[1])
    assert concept_no != 79, "concept 79 is corrupted in source; handle separately"
    with open(PATH, encoding="utf-8") as fh:
        text = fh.read()
    text = apply_concept(text, concept_no)
    with open(PATH, "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()

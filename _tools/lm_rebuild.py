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

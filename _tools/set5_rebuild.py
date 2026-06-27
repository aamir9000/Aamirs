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


BEATS[72] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "clear acrylic compact a few degrees into the key, specular glints sliding across "
        "the acrylic and the candy gel settling inside; gaze lowered to the puck.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a confident "
        "asymmetric quarter-smile blooms, the bold colour-block panels crisp behind.",
        "She holds, electric and composed, one brow a hair higher, eyes bright and direct to "
        "lens.",
    ),
    # F2 - medium waist-up, arc-push (terrazzo chips form the dress, track the transform)
    (
        "Medium waist-up: a smooth 10% arc-push is already drifting a few degrees around her "
        "as terrazzo chips rush in from the frame edges on graphic arcs and she opens her "
        "arms to present; gaze tracking the incoming chips.",
        "The arc-push rides the build as chips lock into the bodice, peplum and belt, edges "
        "sharpening to hard graphic lines; a delighted breath, brows lifting in wonder.",
        "The last chips settle and the chip-shimmer fades as the move eases; she lands a "
        "confident finished pose, eyes alight on the formed dress.",
    ),
    # F3 - tight medium close + macro foreground, rack-focus pull (product->eye)
    (
        "Tight medium close with a macro foreground on the compact: a slow rack-focus pull "
        "with a 5% drift-in is already underway as she slowly rotates the clear compact, the "
        "gel catching light while focus holds on the label.",
        "Focus racks smoothly off the product toward her near eye as she lifts her gaze, the "
        "drift settling; a confident half-smile beginning.",
        "The half-smile settles with her eye now tack-sharp, the compact soft in the "
        "foreground, gaze direct and assured.",
    ),
    # F4 - beauty close-up, face-dominant (4% push, emotional beat — silent)
    (
        "Beauty close-up, face-dominant: an almost-imperceptible 4% push is already breathing "
        "in as the radiant smile blooms with a genuine eye-crinkle and her gaze lifts to "
        "lens (silent \u2014 no words).",
        "A soft exhale and a tiny confident chin-lift follow as her fingertips settle at the "
        "jaw, the expression warm and open.",
        "The warm open expression holds, eyes bright and direct \u2014 a wordless emotional "
        "reveal in place of any line.",
    ),
    # F5 - medium chest-up, beauty 3D orbit synced to halftone-dot burst
    (
        "Medium chest-up: the beauty 3D orbit is already arcing a smooth 12% around the "
        "levitating compact as it eases up and she frames it, halftone dots tight at its "
        "surface; gaze drawn to the rising compact.",
        "The orbit rides the burst as the halftone dots fly outward in clean graphic arcs "
        "and her wonder peaks; eyes widening into the spray, a radiant awe blooming.",
        "The dots radiate full-frame then begin resolving as the bright pulse eases and the "
        "orbit settles; her radiant smile landing, eyes alight.",
    ),
    # F6 - medium close loop close (8% pull-back to F1)
    (
        "Medium close chest-up matching Frame 1: a gentle 8% pull-back is already easing the "
        "orbit to rest toward the opening framing as the last dots dissolve; she settles the "
        "compact back to the collarbone, gaze softening.",
        "The pull-back continues as the radiant smile eases to the confident Frame 1 "
        "quarter-smile and the colour-block panels settle to their opening look; eyes "
        "calming.",
        "She lands precisely on the Frame 1 opening posture and gaze, weight settled \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[73] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "neon faceted bottle a few degrees into the key, prismatic glints sliding across the "
        "facets and the chartreuse-to-pink juice settling inside; gaze lowered to the glass.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a confident "
        "asymmetric quarter-smile blooms, backlit monstera silhouettes glowing behind.",
        "She holds, tropical and electric, one brow a hair higher, eyes bright and direct to "
        "lens.",
    ),
    # F2 - medium waist-up, arc-push (rattan strands self-weave the bodice, track transform)
    (
        "Medium waist-up: a smooth 10% arc-push is already drifting a few degrees around her "
        "as glowing rattan strands spiral in from the frame edges and she opens her arms to "
        "present; gaze tracking the incoming strands.",
        "The arc-push rides the build as the strands self-weave into the lattice and hot-pink "
        "piping threads along the tightening weave; a delighted breath, brows lifting in "
        "wonder.",
        "The last strands settle and the strand-shimmer fades as the move eases; she lands a "
        "confident finished pose, eyes alight on the woven bodice.",
    ),
    # F3 - tight medium close + macro foreground, rack-focus pull (product->eye)
    (
        "Tight medium close with a macro foreground on the bottle: a slow rack-focus pull "
        "with a 5% drift-in is already underway as she slowly rotates the neon bottle, the "
        "juice catching light while focus holds on the label.",
        "Focus racks smoothly off the product toward her near eye as she lifts her gaze, the "
        "drift settling; a confident half-smile beginning.",
        "The half-smile settles with her eye now tack-sharp, the bottle soft in the "
        "foreground, gaze direct and assured.",
    ),
    # F4 - beauty close-up, face-dominant (4% push, emotional beat — silent)
    (
        "Beauty close-up, face-dominant: an almost-imperceptible 4% push is already breathing "
        "in as the radiant smile blooms with a genuine eye-crinkle and her gaze lifts to "
        "lens (silent \u2014 no words).",
        "A soft exhale and a tiny confident chin-lift follow as her fingertips settle at the "
        "jaw, the expression warm and open.",
        "The warm open expression holds, eyes bright and direct \u2014 a wordless emotional "
        "reveal in place of any line.",
    ),
    # F5 - medium chest-up, beauty 3D orbit synced to neon-orchid bloom
    (
        "Medium chest-up: the beauty 3D orbit is already arcing a smooth 12% around the "
        "levitating bottle as it eases up and a single neon orchid bud swells at the bodice; "
        "gaze drawn to the rising bottle.",
        "The orbit rides the bloom as the orchids unfurl and burst open in a radiant halo, "
        "petals lifting and swirling and her wonder peaking; eyes widening into the swirl, a "
        "radiant awe blooming.",
        "The petals radiate full-frame then begin resolving as the bright pulse eases and "
        "the orbit settles; her radiant smile landing, eyes alight.",
    ),
    # F6 - medium close loop close (8% pull-back to F1)
    (
        "Medium close chest-up matching Frame 1: a gentle 8% pull-back is already easing the "
        "orbit to rest toward the opening framing as the last petals dissolve; she settles "
        "the bottle back to the collarbone, gaze softening.",
        "The pull-back continues as the radiant smile eases to the confident Frame 1 "
        "quarter-smile and the neon garden settles to its opening glow; eyes calming.",
        "She lands precisely on the Frame 1 opening posture and gaze, weight settled \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[74] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "clear palette a few degrees into the key, soft speculars sliding across the acrylic "
        "and the rainbow-pastel dome catching light; gaze lowered to the palette.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a dreamy "
        "quarter-smile blooms, the hand-drawn chalk murals soft behind.",
        "She holds, dreamy and luminous, chalk-dust drifting past, eyes soft and direct to "
        "lens.",
    ),
    # F2 - medium waist-up, arc-push (chalk smudge-forms the gown, track the transform)
    (
        "Medium waist-up: a smooth 10% arc-push is already drifting a few degrees around her "
        "as pastel chalk-clouds sweep in from the frame edges and she opens her arms to "
        "present; gaze tracking the drifting dust.",
        "The arc-push rides the build as the dust smudge-settles into the bodice and tiered "
        "skirt, edges crisping from soft smudge to clean graphic line; a wondering breath, "
        "brows lifting.",
        "The last veils settle and the chalk-shimmer fades as the move eases; she lands a "
        "confident finished pose, eyes alight on the ombr\u00e9 tulle.",
    ),
    # F3 - tight medium close + macro foreground, rack-focus pull (product->eye)
    (
        "Tight medium close with a macro foreground on the palette: a slow rack-focus pull "
        "with a 5% drift-in is already underway as she slowly rotates the clear palette, the "
        "pastel dome catching light while focus holds on the swirl.",
        "Focus racks smoothly off the palette toward her near eye as she lifts her gaze, the "
        "drift settling; a dreamy half-smile beginning.",
        "The half-smile settles with her eye now tack-sharp, the palette soft in the "
        "foreground, gaze direct and gentle.",
    ),
    # F4 - beauty close-up, face-dominant (4% push, emotional beat — silent)
    (
        "Beauty close-up, face-dominant: an almost-imperceptible 4% push is already breathing "
        "in as the radiant smile blooms with a genuine eye-crinkle and her gaze lifts to "
        "lens (silent \u2014 no words).",
        "A soft exhale and a tiny confident chin-lift follow as her fingertips settle at the "
        "jaw, the expression warm and open.",
        "The warm open expression holds, eyes bright and direct \u2014 a wordless emotional "
        "reveal in place of any line.",
    ),
    # F5 - medium-wide three-quarter body, graphic 3D orbit (rainbow-bloom burst)
    (
        "Medium-wide three-quarter body: a smooth graphic 20\u00b0 3D orbit is already arcing "
        "around her as she sweeps her arms outward and the chalk-pastel rainbow arc blooms "
        "open in radiant bands; gaze lifting into the bloom.",
        "The orbit rides the burst to its luminous peak, prismatic dust spiralling around "
        "her; eyes widening, an awe-struck joyful smile at full bloom.",
        "The arc holds and begins a gentle settle as the dust drifts and the orbit eases; "
        "her joyful smile landing, eyes alight.",
    ),
    # F6 - medium close loop close (6% settle-back to F1)
    (
        "Medium close chest-up matching Frame 1: a gentle 6% settle-back is already returning "
        "the framing toward the opening position as the last rainbow-dust settles; she eases "
        "her arms back in and re-cradles the palette at collarbone height, gaze softening.",
        "The settle continues as she resolves into the calm hero pose with the dreamy "
        "quarter-smile and a soft settling exhale, the chalk studio easing to its opening "
        "look; eyes calming.",
        "She lands exactly on the Frame 1 composition and gaze, weight settled \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[75] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "citrine bottle a few degrees into the key, speculars sliding across the facets and "
        "the liquid-sequins flickering electric colour-flips; gaze lowered to the glass.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a confident "
        "quarter-smile blooms, suspended glossy citrus slices glowing behind.",
        "She holds, electric and glossy, one brow a hair higher, eyes bright and direct to "
        "lens.",
    ),
    # F2 - medium waist-up, arc-push (sequins flip-form the gown, track the transform)
    (
        "Medium waist-up: a smooth 10% arc-push is already drifting a few degrees around her "
        "as sequin-streams cascade in from the frame edges and she opens her arms to "
        "present; gaze tracking the cascading sequins.",
        "The arc-push rides the build as the sequins flip-lock onto the bodice and skirt, "
        "the structured shoulders crisping into clean line; a delighted breath, brows "
        "lifting.",
        "The last streams settle and the sequin-shimmer fades as the move eases; she lands a "
        "confident finished pose, eyes alight on the colour-flipping gown.",
    ),
    # F3 - tight medium close + macro foreground, rack-focus pull (product->eye)
    (
        "Tight medium close with a macro foreground on the bottle: a slow rack-focus pull "
        "with a 5% drift-in is already underway as she slowly rotates the citrine bottle, "
        "the amber serum and facets catching light while focus holds on the glass.",
        "Focus racks smoothly off the bottle toward her near eye as she lifts her gaze, the "
        "drift settling; a confident half-smile beginning.",
        "The half-smile settles with her eye now tack-sharp, the bottle soft in the "
        "foreground, gaze direct and assured.",
    ),
    # F4 - beauty close-up, face-dominant (4% push, emotional beat — silent)
    (
        "Beauty close-up, face-dominant: an almost-imperceptible 4% push is already breathing "
        "in as the radiant smile blooms with a genuine eye-crinkle and her gaze lifts to "
        "lens (silent \u2014 no words).",
        "A soft exhale and a tiny confident chin-lift follow as her fingertips settle at the "
        "jaw, the expression warm and open.",
        "The warm open expression holds, eyes bright and direct \u2014 a wordless emotional "
        "reveal in place of any line.",
    ),
    # F5 - medium-wide three-quarter body, graphic 3D orbit (citrus-sequin supernova)
    (
        "Medium-wide three-quarter body: a smooth graphic 20\u00b0 3D orbit is already arcing "
        "around her as she sweeps her arms outward and the citrus-sequin supernova explodes "
        "open in radiant rays; gaze lifting into the burst.",
        "The orbit rides the burst to its luminous peak, sequin-sparks spiralling around "
        "her; eyes widening, an awe-struck joyful smile at full bloom.",
        "The rays hold and begin a gentle settle as the sparks drift and the orbit eases; "
        "her joyful smile landing, eyes alight.",
    ),
    # F6 - medium close loop close (6% settle-back to F1)
    (
        "Medium close chest-up matching Frame 1: a gentle 6% settle-back is already returning "
        "the framing toward the opening position as the last citrus-sparks settle; she eases "
        "her arms back in and re-cradles the bottle at collarbone height, gaze softening.",
        "The settle continues as she resolves into the calm hero pose with the confident "
        "quarter-smile and a soft settling exhale, the citrus studio easing to its opening "
        "look; eyes calming.",
        "She lands exactly on the Frame 1 composition and gaze, weight settled \u2014 a "
        "seamless loop seam.",
    ),
]


BEATS[76] = [
    # F1 - medium close chest-up (push-in)
    (
        "Medium close chest-up: a slow push-in is already gliding toward her as she tilts the "
        "chrome-capped vial a few degrees into the key, speculars sliding across the glass "
        "and wet-gloss ribbons gliding on the vinyl gown; gaze lowered to the vial.",
        "The push continues as she lifts her eyes to lens on a soft inhale and a cool "
        "quarter-smile blooms, the UV enamel-drip walls glowing behind.",
        "She holds, sleek and high-gloss, one brow a hair higher, eyes bright and direct to "
        "lens.",
    ),
    # F2 - medium waist-up, arc-push (enamel gloss-forms the gown, track the transform)
    (
        "Medium waist-up: a smooth 10% arc-push is already drifting a few degrees around her "
        "as glossy enamel-ribbons pour down from above and she opens her arms to present; "
        "gaze tracking the pouring enamel.",
        "The arc-push rides the build as the enamel sheets around the bodice and peplum and "
        "gloss-sets into sculptural form, edges snapping to a wet-lacquer sheen; a cool "
        "breath, brows lifting.",
        "The last ribbons set and the gloss-shimmer fades as the move eases; she lands a "
        "confident finished pose, eyes alight on the liquid-vinyl gown.",
    ),
    # F3 - tight medium close + macro foreground, rack-focus pull (product->eye)
    (
        "Tight medium close with a macro foreground on the vial: a slow rack-focus pull with "
        "a 5% drift-in is already underway as she slowly rotates the chrome-capped vial, the "
        "violet lacquer and facets catching light while focus holds on the glass.",
        "Focus racks smoothly off the vial toward her near eye as she lifts her gaze, the "
        "drift settling; a cool half-smile beginning.",
        "The half-smile settles with her eye now tack-sharp, the vial soft in the "
        "foreground, gaze direct and composed.",
    ),
    # F4 - beauty close-up, face-dominant (4% push, emotional beat — silent)
    (
        "Beauty close-up, face-dominant: an almost-imperceptible 4% push is already breathing "
        "in as the radiant smile blooms with a genuine eye-crinkle and her gaze lifts to "
        "lens (silent \u2014 no words).",
        "A soft exhale and a tiny confident chin-lift follow as her fingertips settle at the "
        "jaw, the expression warm and open.",
        "The warm open expression holds, eyes bright and direct \u2014 a wordless emotional "
        "reveal in place of any line.",
    ),
    # F5 - medium-wide three-quarter body, graphic 3D orbit (liquid-enamel splash-crown)
    (
        "Medium-wide three-quarter body: a smooth graphic 20\u00b0 3D orbit is already arcing "
        "around her as she sweeps her arms outward and the liquid-enamel splash-crown bursts "
        "open in glossy ribboned rays; gaze lifting into the burst.",
        "The orbit rides the burst to its luminous peak, gloss-droplets spiralling around "
        "her; eyes widening, an awe-struck joyful smile at full bloom.",
        "The rays hold and begin a gentle settle as the droplets drift and the orbit eases; "
        "her joyful smile landing, eyes alight.",
    ),
    # F6 - medium close loop close (6% settle-back to F1)
    (
        "Medium close chest-up matching Frame 1: a gentle 6% settle-back is already returning "
        "the framing toward the opening position as the last gloss-droplets settle; she "
        "eases her arms back in and re-cradles the vial at collarbone height, gaze "
        "softening.",
        "The settle continues as she resolves into the calm hero pose with the cool "
        "quarter-smile and a soft settling exhale, the UV gloss studio easing to its opening "
        "look; eyes calming.",
        "She lands exactly on the Frame 1 composition and gaze, weight settled \u2014 a "
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
    concept_no = int(sys.argv[1])
    assert concept_no != 79, "concept 79 is corrupted in source; handle separately"
    with open(PATH, encoding="utf-8") as fh:
        text = fh.read()
    text = apply_concept(text, concept_no)
    with open(PATH, "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()

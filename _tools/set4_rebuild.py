#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced video-prompt rebuild engine for
CONCEPTS/20 Full Reel Concepts Set 4 (Concepts 51.txt   (concepts 51-70)

This file uses the Beauty-Ad markdown format. Per VIDEO prompt in a concept
region:
  - delete the standalone `CAMERA MOVEMENT:` line (camera now lives in the
    breakdown),
  - replace the `SUBJECT ACTION WITH TIMING:` block with a tailored
    `SHOT BREAKDOWN (timed, 6s ...)` of 3 beats (shot/angle + her action +
    transform/material interaction + eye-led expression + camera move;
    already-in-motion starts; camera variety; track-the-transform / orbit
    the apex),
  - replace the existing `DURATION:` line with the 6-second standard string,
  - replace the existing `FRAME RATE + MOTION BLUR:` line with the standard.

Everything else (SHOT TYPE — already varied per frame, LENS, LIGHTING,
ENVIRONMENT, AUDIO, LIP-SYNC, NEGATIVE, identity lock) is preserved. Image
prompts already carry varied FRAMING + SUBJECT FRAMING & POSITION + ORIENTATION
LOCK from the earlier global pass, so they are left untouched. Spoken concepts
embed the line inside the Frame-4 beats (no standalone field in the video
prompt) and the image-prompt `SPOKEN LINE:` field is not modified.

Idempotent. Usage:  python3 _tools/set4_rebuild.py <concept_number>
"""
import re
import sys

PATH = "CONCEPTS/20 Full Reel Concepts Set 4 (Concepts 51.txt"

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

# concept_number -> list of frames; each frame is a 3-tuple of beat strings.
BEATS = {}

BEATS[51] = [
    # F1 - full-figure-to-waist symmetrical hero, processional (push-in)
    (
        "Full-figure-to-waist symmetrical hero in the central jewel-shaft: a slow reverent "
        "push-in is already gliding down the nave as she cradles the faceted vial to her "
        "heart, the sapphire velvet breathing; eyes lifting to the towering window in quiet "
        "awe.",
        "The push continues as she takes one slow processional step into the brightest "
        "shaft, coloured light washing up her gown; lips parting on a held breath, gaze "
        "tracing the glass.",
        "She settles tall in the shaft, the vial glinting at her heart, a serene reverent "
        "calm holding in her eyes as a soft jewel caustic dances on the back of her hand.",
    ),
    # F2 - full-figure transform, slightly low angle (arc rising, track the seam)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising with "
        "her as the jewel-shaft strikes and shatters into travelling stained-glass shards; "
        "gaze catching the fracturing light, eyes widening a hair.",
        "The arc tracks the diagonal light-seam sweeping up her body, sapphire velvet "
        "re-forming into jewel-mosaic beadwork as it passes; an awed breath, brows lifting "
        "in wonder.",
        "The last shard clears overhead and the finished jewel-mosaic gown settles as the "
        "arc eases; a small luminous smile landing, eyes alight on the resolved beadwork.",
    ),
    # F3 - beauty close, product-at-face (6% push to cheekbone)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her cheekbone is "
        "already gliding in as she tilts the vial and brings a luminous radiance-drop on her "
        "fingertip toward her face; eyes lowered to the drop in serene focus.",
        "She presses the drop to the high cheekbone and it catches the jewel light, the push "
        "settling; a small private smile beginning, lashes lowering.",
        "She lowers the hand a touch and lifts her eyes softly, the beadwork glinting, a "
        "content glow in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN, barely-there push)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a warm smile, the vial presented "
        "at her chest.",
        "She delivers \u201clit like a cathedral.\u201d with natural lip-sync and a soft "
        "brow lift, eyes bright and direct, the jewel window glowing symmetrically behind.",
        "The radiant smile lands and holds with a warm blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, radiance-halo bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as she raises the vial and light kindles at the "
        "cap; gaze lifting into the kindling glow.",
        "The boom keeps rising as the jewel-halo ring blooms outward in a slow wave, "
        "igniting the windows in sequence; eyes widening into the light, a radiant awe "
        "blooming.",
        "Gold motes drift down and the halo eases to a sustained glow as the move settles; "
        "her radiant smile landing, eyes serene and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back / gentle pull)
    (
        "Full-figure-to-waist symmetrical hero matching Frame 1: a slow settle-back is "
        "already easing the framing toward the opening position as the halo glow fades and "
        "the last motes drift down; she returns the vial to her heart, gaze lowering.",
        "The pull continues as her smile eases to the serene parted-lip awe of the opening "
        "and the jewel-mosaic softens back toward reverent stillness; eyes calming.",
        "She lifts her eyes toward the great window again, landing precisely on the Frame 1 "
        "pose, weight settled in the shaft \u2014 a seamless loop seam.",
    ),
]


BEATS[52] = [
    # F1 - medium-full three-quarter hero beside plinth (push-in)
    (
        "Medium-full three-quarter hero beside the porcelain plinth: a slow push-in is "
        "already gliding toward her as she rests a hand by the ceramic pot, the blush silk "
        "breathing; she turns her face softly to lens with a calm smile, eyes warm.",
        "The push continues as she begins a graceful quarter-turn toward camera, the slip "
        "catching pearly north-window light; gaze easing to lens, lashes soft.",
        "She settles mid-turn, weight rolling onto the front foot, a serene closed-lip calm "
        "holding as the silk sways to rest.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the glaze down)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already following "
        "downward as a ribbon of glossy white liquid-porcelain glaze begins to pour from her "
        "shoulder; gaze tracking the pouring glaze, eyes brightening.",
        "The arc rides the glaze sheeting down her body, setting into the sculptural "
        "porcelain gown with cobalt china-motifs blooming across it; a delighted breath, "
        "brows lifting in wonder.",
        "The last glaze sets at the hem and the finished gown settles as the arc eases; a "
        "soft luminous smile landing, eyes alight on the patterned porcelain.",
    ),
    # F3 - beauty close, product-at-face (6% push to cheekbone)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her cheekbone is "
        "already gliding in as she dips two fingertips into the open pot, the pearly primer "
        "catching light; eyes lowered to the gesture.",
        "She sweeps it along her cheekbone and the skin behind blurs to a soft-matte finish, "
        "the push settling; a small assured smile beginning, gaze steadying.",
        "She lowers the hand a touch and lifts her eyes softly, the porcelain bodice "
        "glinting, a poised calm in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a warm smile, the porcelain pot "
        "presented at her chest.",
        "She delivers \u201csmooth as porcelain.\u201d with natural lip-sync and a soft brow "
        "lift, eyes bright and direct, the blush atelier soft behind.",
        "The smile lands and holds with a soft blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, kintsugi gold-vein bloom (push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow push-in with a gentle "
        "boom-rise is already lifting as she opens a hand at her heart and a gold point "
        "kindles on the porcelain; gaze drawn to the kindling vein.",
        "The boom keeps rising as kintsugi gold veins trace outward along the cobalt "
        "patterns in a slow wicking and the gown warms to a glow; eyes lifting into it, a "
        "proud serene awe blooming.",
        "Gold-dust motes drift up and the veins hold as a sustained glow as the move "
        "settles; her serene proud smile landing, eyes composed and luminous.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the gold glow fades and the last "
        "motes drift down; she returns her hand to rest by the pot, gaze softening.",
        "The pull continues as her smile eases to the serene closed-lip calm of the opening "
        "and the porcelain softens back toward the blush slip's stillness; eyes calming.",
        "She turns her face softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled beside the plinth \u2014 a seamless loop seam.",
    ),
]


BEATS[53] = [
    # F1 - medium-full three-quarter hero amid gears (push-in)
    (
        "Medium-full three-quarter hero amid the brass gears: a slow push-in is already "
        "gliding toward her as she holds the amber bottle to her heart, the bronze silk "
        "breathing and a giant gear turning slowly behind; she lifts her eyes to lens with a "
        "knowing calm.",
        "The push continues as she begins a graceful quarter-turn, the bronze silk catching "
        "amber gaslight; gaze easing to lens, a poised set to her mouth.",
        "She settles mid-turn, weight rolling onto the front foot, a precise knowing calm "
        "holding as a floating cog drifts past.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the assembly up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as "
        "the first brass cogs and clock-hands spin in from the air toward her; gaze tracking "
        "the incoming gears, eyes brightening.",
        "The arc rides the assembly up her body as gears fly in along clean arcs and "
        "interlock, the gilded gown meshing into being piece by piece like a watch movement "
        "closing; a delighted breath, brows lifting in wonder.",
        "The last cog meshes and clicks home and the finished gown settles as the arc eases; "
        "a warm luminous smile landing, eyes alight on the brass filigree.",
    ),
    # F3 - beauty close, product-at-face (6% push to collarbone)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her collarbone is "
        "already gliding in as she raises the amber dropper above it, a drop swelling at the "
        "tip; eyes lowered to the bead of oil.",
        "A single radiance-oil drop releases and falls catching the gaslight, the push "
        "settling; a small assured smile beginning, gaze following the drop.",
        "She lowers the bottle a touch and lifts her eyes softly, the gilded gearwork "
        "glinting, a precise calm in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a warm knowing smile, the bottle "
        "presented at her chest.",
        "She delivers \u201cbeauty, like clockwork.\u201d with natural lip-sync and a soft "
        "brow lift, eyes bright and direct, the slow gears glowing behind.",
        "The smile lands and holds with a soft blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, golden gear-ring bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as the clock-hands align and a gold point "
        "kindles at the central gear; gaze drawn to the kindling point.",
        "The boom keeps rising as a golden ring and brass cogs bloom outward in a slow wave, "
        "the giant gears brightening in sequence; eyes lifting into it, a radiant knowing "
        "awe blooming.",
        "Gold motes and cogs drift and the halo eases to a sustained glow as the move "
        "settles; her radiant knowing smile landing, eyes serene and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the golden glow fades and the "
        "last motes and cogs drift down; she returns the bottle to her heart, gaze "
        "softening.",
        "The pull continues as her smile eases to the knowing closed-lip calm of the opening "
        "and the gilded gearwork softens back toward the bronze silk's stillness; eyes "
        "calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled among the gears \u2014 a seamless loop seam.",
    ),
]


BEATS[54] = [
    # F1 - medium-full three-quarter hero in spotlight (push-in)
    (
        "Medium-full three-quarter hero in the single overhead spotlight: a slow push-in is "
        "already gliding toward her as she holds the black-glass bottle to her collarbone, "
        "the charcoal slip breathing and cool haze curling through the beam; she lifts her "
        "eyes to lens with a cool knowing set.",
        "The push continues as she begins a graceful quarter-turn, a steel specular "
        "travelling the slip; gaze easing to lens, chin level.",
        "She settles mid-turn, weight rolling onto the front foot, a cool electric calm "
        "holding as a chrome rim catches her shoulder.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the sheet up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as a "
        "sheet of glossy black ferrofluid lifts off the mirror-floor and begins to climb her "
        "form; gaze tracking the rising sheet, eyes sharpening.",
        "The arc rides the sheet upward as it pulls into crisp magnetic spikes along "
        "invisible field-lines that arc then smooth into the liquid-obsidian gown; a charged "
        "breath, brows lifting.",
        "The last spikes smooth and the chrome detailing sets as the arc eases; a cool "
        "luminous look landing, eyes alight on the obsidian seams.",
    ),
    # F3 - beauty close, product-at-face (6% push to collarbone)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her collarbone is "
        "already gliding in as she raises the faceted dropper above it, a glossy drop "
        "swelling at the tip; eyes lowered to the bead.",
        "A single serum drop releases and falls catching the chrome rim-light, the push "
        "settling; a small assured set beginning, gaze following the drop.",
        "She lowers the bottle a touch and lifts her eyes, the obsidian bodice glinting, a "
        "cool composed calm in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a cool knowing smile, the bottle "
        "presented at her chest.",
        "She delivers \u201cpower, poured on.\u201d with natural lip-sync and a soft brow "
        "lift, eyes bright and direct, the dark studio cool behind.",
        "The smile lands and holds with a cool blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, magnetic-spike crown bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as a bead of ferrofluid lifts from her shoulder "
        "and a cool chrome point kindles behind her head; gaze drawn to the kindling point.",
        "The boom keeps rising as a crown of crisp magnetic spikes fans outward along "
        "field-lines and the gown catches the glow; eyes lifting into it, a cool radiant awe "
        "blooming.",
        "Droplets and motes drift and the crown eases to a sustained radiant halo as the "
        "move settles; her cool radiant smile landing, eyes serene and crowned.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the cool glow fades and the last "
        "droplets drift down; she returns the bottle to her collarbone, gaze softening.",
        "The pull continues as her smile eases to the cool knowing set of the opening and "
        "the liquid-obsidian softens back toward the charcoal slip's stillness; eyes "
        "calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled in the spotlight \u2014 a seamless loop seam.",
    ),
]


BEATS[55] = [
    # F1 - medium-full three-quarter hero beside embroidery hoop (push-in)
    (
        "Medium-full three-quarter hero beside the embroidery hoop: a slow push-in is "
        "already gliding toward her as she rests a hand on the hoop, the ivory silk "
        "breathing and a gold-thread skein swaying behind; she lifts her eyes to lens with a "
        "soft romantic smile.",
        "The push continues as she begins a graceful quarter-turn, the slip catching warm "
        "pearly-gold window light; gaze easing to lens, lashes soft.",
        "She settles mid-turn, weight rolling onto the front foot, a warm romantic calm "
        "holding as the silk sways to rest.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the stitching up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as "
        "the first silk and gold threads fly in from the air toward her; gaze tracking the "
        "streaming threads, eyes brightening.",
        "The arc rides the stitching up her body as the threads self-stitch along embroidery "
        "paths, ornate floral goldwork building blossom by blossom; a delighted breath, "
        "brows lifting in wonder.",
        "The last loop couches home and the finished embroidered gown settles as the arc "
        "eases; a warm luminous smile landing, eyes alight on the goldwork.",
    ),
    # F3 - beauty close, product-at-face / lips (6% push to lips)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her lips is already "
        "gliding in as she raises the slim wand to her lower lip, the rose-gold oil catching "
        "light; eyes lowered to the glide.",
        "She glides it along the lip leaving a glossy sheen, the push settling; a small "
        "assured smile beginning, gaze warming.",
        "She lowers the wand a touch, lips lightly pressing, and lifts her eyes softly, the "
        "goldwork glinting, a soft glow in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a soft romantic smile, the wand "
        "tube presented at her chest.",
        "She delivers \u201cspun by hand.\u201d with natural lip-sync and a gentle brow lift, "
        "eyes bright and direct, the warm atelier soft behind.",
        "The smile lands and holds with a warm blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, goldwork-blossom bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as a blossom at her shoulder swells and a warm "
        "gold point kindles at its centre; gaze drawn to the kindling bloom.",
        "The boom keeps rising as the goldwork flowers open in sequence, lifting fine "
        "spirals of gold thread-light and silk petals; eyes lifting into them, a radiant awe "
        "blooming.",
        "The thread-light and petals drift up and out, easing to a sustained warm halo as "
        "the move settles; her radiant smile landing, eyes serene and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the warm glow fades and the last "
        "petals drift down; she returns her hand to the embroidery hoop, gaze softening.",
        "The pull continues as her smile eases to the soft romantic calm of the opening and "
        "the embroidered goldwork softens back toward the ivory slip's stillness; eyes "
        "calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled beside the hoop \u2014 a seamless loop seam.",
    ),
]


BEATS[56] = [
    # F1 - medium-full three-quarter hero among crystal clusters (push-in)
    (
        "Medium-full three-quarter hero among the amethyst clusters: a slow push-in is "
        "already gliding toward her as she holds the faceted bottle to her collarbone, the "
        "lilac slip breathing and cool mist drifting through the violet glow; she lifts her "
        "eyes to lens with a serene calm smile.",
        "The push continues as she begins a graceful quarter-turn, an iridescent shimmer "
        "travelling the slip; gaze easing to lens, lashes soft.",
        "She settles mid-turn, weight rolling onto the front foot, a serene ethereal calm "
        "holding as a quartz cluster glints behind.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the growth up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as "
        "the first faceted crystal points nucleate at the hem and bodice seams; gaze "
        "tracking the kindling facets, eyes brightening.",
        "The arc rides the growth up her body as crystals grow outward along crystallographic "
        "axes, faceting into the structured gown; an awed breath, brows lifting in wonder.",
        "The last facets lock and the crystalline gown settles as the arc eases; a cool "
        "luminous look landing, eyes alight on the prismatic edges.",
    ),
    # F3 - beauty close, product-at-face / mist-spritz (6% push to face)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her face is already "
        "gliding in as she raises the faceted bottle and presses the atomizer, a fine "
        "luminous mist beginning to fan; eyes lowered to the spray.",
        "The mist drifts down across her face as she closes then opens her eyes dewy and "
        "clear, the push settling; a serene smile beginning.",
        "She lowers the bottle a touch and lifts her eyes, the crystalline bodice glinting, "
        "a refreshed clarity in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a serene knowing smile, the bottle "
        "presented at her chest.",
        "She delivers \u201cclarity, crystallized.\u201d with natural lip-sync and a gentle "
        "brow lift, eyes bright and direct, the violet cavern soft behind.",
        "The smile lands and holds with a cool blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, prism-burst bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as a facet at her shoulder kindles with a "
        "warm-white inner light; gaze drawn to the kindling facet.",
        "The boom keeps rising as the light races across the gown and bursts outward as "
        "prism-beams and rainbow caustics, crystal shards lifting; eyes lifting into the "
        "light, a radiant awe blooming.",
        "The shards and motes drift out, easing to a sustained prismatic halo as the move "
        "settles; her radiant smile landing, eyes serene and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the prismatic glow fades and the "
        "last shards drift down; she returns the bottle to her collarbone, gaze softening.",
        "The pull continues as her smile eases to the serene calm of the opening and the "
        "crystalline gown softens back toward the lilac slip's stillness; eyes calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled among the clusters \u2014 a seamless loop seam.",
    ),
]


BEATS[57] = [
    # F1 - medium-full three-quarter hero on wet rooftop (push-in)
    (
        "Medium-full three-quarter hero on the rain-slick neon rooftop: a slow push-in is "
        "already gliding toward her as she holds the gloss bottle to her collarbone, the "
        "matte-black bodysuit breathing and drizzle drifting through magenta-and-cyan glow; "
        "she lifts her eyes to lens with a cool knowing set.",
        "The push continues as she begins a graceful quarter-turn, neon speculars travelling "
        "the matte fabric; gaze easing to lens, chin level.",
        "She settles mid-turn, weight rolling onto the front foot, a cool electric calm "
        "holding as wet-ground reflections shimmer behind.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the fill up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as "
        "fine clear glass-tube channels trace into being over her form; gaze tracking the "
        "channels, eyes sharpening.",
        "The arc rides the fill up her body as liquid magenta-and-cyan neon floods through "
        "the channels, racing and lighting them up; a charged breath, brows lifting.",
        "The last run floods to full glow and the neon gown settles as the arc eases; an "
        "electric luminous look landing, eyes alight on the blazing tubes.",
    ),
    # F3 - beauty close, product-at-face / lips (6% push to lips)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her lips is already "
        "gliding in as she raises the chrome wand to her lower lip, the electric-clear gloss "
        "catching neon; eyes lowered to the swipe.",
        "She swipes it across the lip leaving a high-shine film, the push settling; a small "
        "electric smile beginning, gaze warming.",
        "She lowers the wand a touch, lips lightly pressing, and lifts her eyes, the neon "
        "channels glinting, a charged calm in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a cool knowing smile, the bottle "
        "presented at her chest.",
        "She delivers \u201cturn it on.\u201d with natural lip-sync and a soft brow lift, "
        "eyes bright and direct, the neon city glowing behind.",
        "The smile lands and holds with a cool blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, neon-ring surge bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as a tube at her heart pulses brighter and a "
        "bright magenta-cyan point kindles; gaze drawn to the kindling point.",
        "The boom keeps rising as the surge races through every tube and bursts outward as "
        "concentric neon rings, the gown blazing; eyes lifting into the light, an euphoric "
        "awe blooming.",
        "Droplets and motes drift out, easing to a sustained brilliant glow as the move "
        "settles; her radiant smile landing, eyes euphoric and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the neon halo fades and the last "
        "droplets drift down; she returns the bottle to her collarbone, gaze softening.",
        "The pull continues as her smile eases to the cool knowing set of the opening and "
        "the neon gown softens back toward the matte-black bodysuit's stillness; eyes "
        "calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled on the wet rooftop \u2014 a seamless loop seam.",
    ),
]


BEATS[58] = [
    # F1 - medium-full three-quarter hero before mosaic wall (push-in)
    (
        "Medium-full three-quarter hero before the antique-gold mosaic wall: a slow push-in "
        "is already gliding toward her as she holds the balm pot to her collarbone, the "
        "ivory slip breathing and incense haze drifting through candle glow; she lifts her "
        "eyes to lens with a warm serene smile.",
        "The push continues as she begins a graceful quarter-turn, a honeyed sheen "
        "travelling the slip; gaze easing to lens, lashes soft.",
        "She settles mid-turn, weight rolling onto the front foot, a warm opulent calm "
        "holding as candle flames flicker behind.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the tiling up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as "
        "the first tiny tesserae alight onto the hem and bodice seams; gaze tracking the "
        "alighting tiles, eyes brightening.",
        "The arc rides the tiling up her body as thousands of tesserae fly in along clean "
        "mosaic lines and lock grout-tight; an awed breath, brows lifting in wonder.",
        "The last panels lock and the mosaic gown settles as the arc eases; a warm luminous "
        "look landing, eyes alight on the lapis-and-gold tesserae.",
    ),
    # F3 - beauty close, product-at-face (6% push to face)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her face is already "
        "gliding in as she dips a fingertip into the open pot and lifts it, the jewel-toned "
        "balm catching candlelight; eyes lowered to the gesture.",
        "She presses it to the high of her cheekbone and a warm gold-fleck sheen blooms, the "
        "push settling; a small smile beginning, gaze warming.",
        "She lowers the hand a touch and lifts her eyes, the mosaic bodice glinting, a warm "
        "calm in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a serene knowing smile, the balm "
        "pot presented at her chest.",
        "She delivers \u201cset in gold.\u201d with natural lip-sync and a gentle brow lift, "
        "eyes bright and direct, the candlelit mosaic glowing behind.",
        "The smile lands and holds with a warm blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, gilded light-tile bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as a gold tessera at her heart kindles with a "
        "warm inner light; gaze drawn to the kindling tile.",
        "The boom keeps rising as the light sweeps across the mosaic and bursts outward as a "
        "shimmer of floating gold-and-jewel light-tiles, the gown blazing; eyes lifting into "
        "the light, a radiant awe blooming.",
        "The light-tiles and motes drift out, easing to a sustained gilded halo as the move "
        "settles; her radiant smile landing, eyes serene and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the gilded glow fades and the "
        "last light-tiles drift down; she returns the pot to her collarbone, gaze "
        "softening.",
        "The pull continues as her smile eases to the serene calm of the opening and the "
        "mosaic gown softens back toward the ivory slip's stillness; eyes calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled before the mosaic wall \u2014 a seamless loop seam.",
    ),
]


BEATS[59] = [
    # F1 - medium-full three-quarter hero among marble columns (push-in)
    (
        "Medium-full three-quarter hero among the white marble columns: a slow push-in is "
        "already gliding toward her as she holds the compact to her collarbone, the oatmeal "
        "linen breathing and marble dust drifting through the daylight beam; she lifts her "
        "eyes to lens with a calm sculptural smile.",
        "The push continues as she begins a graceful quarter-turn, a soft matte highlight "
        "travelling the linen; gaze easing to lens, lashes soft.",
        "She settles mid-turn, weight rolling onto the front foot, a serene sculptural calm "
        "holding as a column gleams behind.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the marble setting up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as "
        "the first veil of liquid marble washes up the hem and begins to set; gaze tracking "
        "the climbing marble, eyes brightening.",
        "The arc rides the setting up her body as the marble wraps her form and hardens "
        "along carved folds, fine grey veins drawing through it; an awed breath, brows "
        "lifting in wonder.",
        "The last folds set and the sculpted gown settles as the arc eases; a calm luminous "
        "look landing, eyes alight on the carved drapery.",
    ),
    # F3 - beauty close, product-at-face / highlighter (6% push to face)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her face is already "
        "gliding in as she loads the fine brush from the open marble compact, the "
        "pearl-champagne powder catching daylight; eyes lowered to the brush.",
        "She sweeps it along the high of her cheekbone and a soft dewy pearl sheen blooms, "
        "the push settling; a calm smile beginning, gaze warming.",
        "She lowers the brush a touch and lifts her eyes, the veined marble bodice glinting, "
        "a serene calm in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a serene knowing smile, the "
        "compact presented at her chest.",
        "She delivers \u201ccarved to last.\u201d with natural lip-sync and a gentle brow "
        "lift, eyes bright and direct, the marble gallery soft behind.",
        "The smile lands and holds with a calm blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, living-warmth flush bloom (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as a warm rose flush kindles at her heart and "
        "the marble softens to living warmth; gaze drawn to the kindling flush.",
        "The boom keeps rising as the flush sweeps through the gown and across her skin, "
        "fine marble-dust motes and soft rose light lifting as the stone warms to living "
        "blush; eyes lifting into the light, a radiant awe blooming.",
        "The motes drift out, easing to a sustained living warmth as the move settles; her "
        "radiant smile landing, eyes serene and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the rose warmth fades and the "
        "last motes drift down; she returns the compact to her collarbone, gaze softening.",
        "The pull continues as her smile eases to the calm poise of the opening and the "
        "sculpted marble softens back toward the oatmeal linen's stillness; eyes calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled among the columns \u2014 a seamless loop seam.",
    ),
]


BEATS[60] = [
    # F1 - medium-full three-quarter hero among greenery and glass frames (push-in)
    (
        "Medium-full three-quarter hero among the greenery and pressed-flower glass frames: "
        "a slow push-in is already gliding toward her as she holds the blush bottle to her "
        "collarbone, the sage silk breathing and a fresh petal drifting through the daylight "
        "beam; she lifts her eyes to lens with a soft fresh smile.",
        "The push continues as she begins a graceful quarter-turn, a soft highlight "
        "travelling the silk; gaze easing to lens, lashes soft.",
        "She settles mid-turn, weight rolling onto the front foot, a fresh romantic calm "
        "holding as a hanging bloom sways behind.",
    ),
    # F2 - full-figure transform, slightly low angle (arc following the resin setting up)
    (
        "Full-figure from a slightly low angle: a slow controlled arc is already rising as "
        "the first real petals settle onto the hem and a clear resin begins to flow around "
        "them; gaze tracking the gathering petals, eyes brightening.",
        "The arc rides the setting up her body as petals drift in and arrange while the "
        "resin flows and hardens into translucent panels suspending the blooms; an awed "
        "breath, brows lifting in wonder.",
        "The last panels set and the resin gown settles as the arc eases; a fresh luminous "
        "look landing, eyes alight on the suspended blossoms.",
    ),
    # F3 - beauty close, product-at-face / liquid blush (6% push to face)
    (
        "Beauty close, chest-up at a three-quarter: a slow push toward her face is already "
        "gliding in as she lifts the doe-foot applicator and dabs two small dots of "
        "rosy-coral blush onto her cheek; eyes lowered to the dabs.",
        "She blends with two fingertips and a soft fresh dewy flush blooms, the push "
        "settling; a warm smile beginning, gaze warming.",
        "She lowers the hand a touch and lifts her eyes, the petal-set resin glinting, a "
        "fresh calm in her gaze.",
    ),
    # F4 - beauty close, direct address (SPOKEN)
    (
        "Beauty close, chest-up squared to lens: the camera is already settled on a "
        "barely-there push as her eyes find the lens with a serene knowing smile, the bottle "
        "presented at her chest.",
        "She delivers \u201cin full bloom.\u201d with natural lip-sync and a gentle brow "
        "lift, eyes bright and direct, the sunlit greenhouse soft behind.",
        "The smile lands and holds with a fresh blink, gaze staying eye-to-eye.",
    ),
    # F5 - full-figure magical hero, bloom-burst petal cascade (majestic push + boom-rise)
    (
        "Full-figure magical hero from a slightly low angle: a slow majestic push-in with a "
        "gentle boom-rise is already lifting as a closed bud at her heart panel quivers and "
        "begins to unfurl; gaze drawn to the opening bud.",
        "The boom keeps rising as the bloom sweeps across the gown, every suspended bud "
        "unfurling and releasing a swirling cascade of fresh petals; eyes lifting into the "
        "swirl, a radiant awe blooming.",
        "The petals drift out, easing to a sustained ring of slowly falling petals as the "
        "move settles; her radiant smile landing, eyes serene and haloed.",
    ),
    # F6 - loop close, matched to F1 (settle-back)
    (
        "Medium-full three-quarter hero matching Frame 1: a slow settle-back is already "
        "easing the framing toward the opening position as the petal-glow fades and the last "
        "petals drift down; she returns the bottle to her collarbone, gaze softening.",
        "The pull continues as her smile eases to the soft poise of the opening and the "
        "resin gown softens back toward the sage silk's stillness; eyes calming.",
        "She lifts her eyes softly to the lens, landing precisely on the Frame 1 pose, "
        "weight settled among the glass frames \u2014 a seamless loop seam.",
    ),
]


def build_block(beats):
    # Replaces ONLY the `SUBJECT ACTION WITH TIMING:` header + its bullet beat
    # lines. Ends with a single trailing newline so the original blank line
    # that followed the beats still separates the next section (LIGHTING / any
    # embedded line).
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

    region, n_dur = re.subn(
        r"(?m)^DURATION: [^\n]*$", DURATION_LINE, region
    )
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
    with open(PATH, encoding="utf-8") as fh:
        text = fh.read()
    text = apply_concept(text, concept_no)
    with open(PATH, "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()

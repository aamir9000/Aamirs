#!/usr/bin/env python3
"""
fix_addons.py — repair context-wrong premium add-ons introduced by premium_finish.py.

Two add-on sentences were sometimes appended in the wrong context:
  SKY = "Sky richly graded and cinematic with elegant clouds and premium light, never flat or empty."
  WATER = "Water rendered crystal-clear in rich sea-blue and turquoise gradients, with beautiful caustics and clean sparkling reflections."

Fixes (conservative, only when context clearly warrants):
  * SKY in SPACE/COSMIC context      -> reword to a cosmic-sky sentence (no clouds).
  * SKY in UNDERWATER context        -> reword to a water-light sentence (no sky/clouds).
  * SKY in ENCLOSED-INDOOR context, with no window/skylight/open-sky -> remove the SKY sentence.
  * WATER on a NON-SEA liquid (rain/ink/molten/bath/tears/oil/wine/etc) with no real sea/pool -> reword to a neutral 'true to its material' sentence.
Everything else is left untouched.

Usage: python3 _tools/fix_addons.py "<file>"
"""
import sys, io, re

SKY = "Sky richly graded and cinematic with elegant clouds and premium light, never flat or empty."
SKY_SPACE = "The cosmos rendered richly graded and cinematic with deep, luminous space tones and premium light, never flat or empty."
SKY_WATERLIGHT = "The water-light rendered richly graded and luminous with premium caustics, god-rays and depth, never flat or empty."

WATER = "Water rendered crystal-clear in rich sea-blue and turquoise gradients, with beautiful caustics and clean sparkling reflections."
LIQUID_NEUTRAL = "Any liquid rendered clean, clear and premium — true to its own material and real colour."

SPACE = re.compile(r"\b(nebula|deep space|outer space|cosmos|cosmic|galaxy|galactic|starfield|star-field|zero-?gravity|orbit|orbital|space station|among the stars|celestial|interstellar|astral)\b", re.I)
UNDER = re.compile(r"\b(underwater|aquarium|submerged|beneath the surface|under the sea|ocean floor|seabed|coral reef|deep-sea|sub-aqua|kelp|abyss)\b", re.I)
INDOOR = re.compile(r"\b(elevator|lift lobby|lobby|dressing room|bathroom|kitchen|corridor|hallway|tunnel|interior|indoors?|windowless|vault|chamber|cabin interior|inside the)\b", re.I)
OPEN_SKY = re.compile(r"\b(open sky|night sky|dawn sky|dusk sky|sunset|sunrise|horizon|open to the (?:sky|stars|night)|skylight|window|clouds?|moonlit sky|starlit sky|aurora)\b", re.I)

NONSEA = re.compile(r"\b(rain|raindrop|drizzle|downpour|monsoon|puddle|ink|inky|molten|lava|magma|tears?|teardrop|milk|milky|oil|wine|champagne|blood|paint|mud|muddy|soup|coffee|tea|honey|syrup|chrome-pour|liquid metal)\b", re.I)
REALSEA = re.compile(r"\b(sea|ocean|pool|lagoon|lake|cenote|aquarium|reef|waterfall|cascade|river|grotto|turquoise|tropical water|infinity pool|spring|bay|cove|shore|surf|tide)\b", re.I)

def fix_line(line):
    changed = False
    if SKY in line:
        if SPACE.search(line):
            line = line.replace(SKY, SKY_SPACE); changed = True
        elif UNDER.search(line):
            line = line.replace(SKY, SKY_WATERLIGHT); changed = True
        elif INDOOR.search(line) and not OPEN_SKY.search(line):
            line = line.replace(" " + SKY, "").replace(SKY, ""); changed = True
    if WATER in line:
        if NONSEA.search(line) and not REALSEA.search(line):
            line = line.replace(WATER, LIQUID_NEUTRAL); changed = True
    return line, changed

def main():
    if len(sys.argv) != 2:
        print("usage: fix_addons.py <file>"); sys.exit(2)
    path = sys.argv[1]
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    n = 0
    out = []
    for ln in lines:
        new, ch = fix_line(ln)
        if ch: n += 1
        out.append(new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print(f"{path}: fixed {n} lines")

if __name__ == "__main__":
    main()

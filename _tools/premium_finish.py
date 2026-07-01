#!/usr/bin/env python3
"""
premium_finish.py — additive PREMIUM CINEMATIC EDITORIAL FINISH enricher (steering section O).

Appends a tailored premium clause to descriptive field lines ONLY. Never edits framing, camera,
lens, shot size, wardrobe, hair, makeup, hands, pose (SUBJECT FRAMING), SHOT BREAKDOWN action
beats, identity, ORIENTATION LOCK, MOOD (emotion preserved), or NEGATIVE lines.

Target descriptive fields (leading label of the line, colon- or em-dash-terminated, short):
  SCENE INTENT / SETTING / ENVIRONMENT / WORLD / BACKDROP / SPATIAL LOGIC / DEPTH / COMPOSITION /
  LIGHTING / ATMOSPHERE[/FX] / COLOR|COLOUR GRADE / TEXTURE|TEXTURES / MATERIALS / PALETTE.

Two formats handled cleanly:
  * SIMPLE line (single field, one fragment)  -> append the field-specific premium clause.
  * PACKED line (multiple fields / sentences) -> append ONE consolidated premium clause at end.
Placement is ALWAYS at end of the line, so it can never be misplaced between fields.

Context-aware: detects water / sky / greenery / architecture in the line and adds the matching
premium clause. Tonal-safe: colour language is "rich clean, controlled elegant saturation,
natural skin" so it honours vibrant AND intentionally tonal/noir/ice/chrome concepts (section I).
Idempotent: each clause has a stable signature; if present, the line is skipped.

Usage: python3 _tools/premium_finish.py "<file>" [--after "MARKER"]
"""
import sys, io, re, hashlib

TONAL = re.compile(r"\b(noir|obsidian|onyx|ink|inky|monochrome|ash|charcoal|smoke|smoky|midnight|"
                   r"gothic|gunmetal|chrome|pewter|marble|porcelain|alabaster|ice|icy|frost|"
                   r"glacial|storm|overcast|moody|sombre|somber|eclipse)\b", re.I)
WATER = re.compile(r"\b(water|pool|sea|ocean|waves?|lagoon|river|lake|rain|wet|splash|droplets?|"
                   r"aqua|turquoise|underwater|ripples?|tide|surf|spray|waterfall|cascade)\b", re.I)
SKY   = re.compile(r"\b(sky|skies|clouds?|horizon|sunset|sunrise|dawn|dusk|twilight|stars|starlit|"
                   r"aurora|nebula)\b", re.I)
GREEN = re.compile(r"\b(forest|gardens?|leaves|leaf|foliage|jungle|trees?|palms?|flowers?|floral|"
                   r"meadow|grass|vines?|moss|fern|petals?|botanical|greenery|orchard|blossom)\b", re.I)
ARCH  = re.compile(r"\b(marble|palace|temple|hall|columns?|arch|arches|villa|penthouse|staircase|"
                   r"stairs|facade|cathedral|lobby|colonnade|atrium|terrace|balcony|courtyard|dome|"
                   r"corridor|architecture|architectural|mansion|estate|suite)\b", re.I)

# leading label: optional bullet/bold, LABEL (<=26 chars, no period), then : or —
HEAD = re.compile(r"^(\s*(?:[-*>]\s*)?(?:\*\*)?\s*)([A-Za-z][A-Za-z /&]{1,25}?)(?:\*\*)?\s*(:|—)\s")
# a second inline field label (=> packed line)
SECOND = re.compile(r"[.;]\s+[A-Z]|(?:^|\s)(?:Color|Colour|Grade|Lighting|Atmosphere|Textures?|"
                    r"Spatial|Composition|Environment|Palette|Continuity|Kinetic|Micro|Cloth|Lip)\b"
                    r"[A-Za-z /&-]{0,20}[:—]")

TARGET = {
    "scene intent":"ENV","setting":"ENV","environment":"ENV","world":"ENV","backdrop":"ENV",
    "spatial logic":"DEPTH","depth":"DEPTH","composition":"DEPTH",
    "lighting":"LIGHT",
    "atmosphere":"ATMO","atmosphere / fx":"ATMO","atmosphere/fx":"ATMO",
    "color grade":"GRADE","colour grade":"GRADE","grade":"GRADE","colour palette":"PAL","color palette":"PAL",
    "texture":"TEX","textures":"TEX","materials":"TEX",
    "palette":"PAL",
}
BANK = {
 "ENV": ["Every zone of the frame intentionally designed, immaculately clean and premium, with"
         " layered foreground, midground and background depth and rich environmental storytelling",
         "Each area of the frame intentionally composed, pristine and luxurious, with true"
         " foreground-to-background layering and immersive environmental depth"],
 "DEPTH": ["Premium foreground, midground and background layering with strong three-dimensional"
           " depth and clean visual balance (original framing preserved)",
           "Rich layered foreground-to-background depth, elegant spatial hierarchy and clean visual"
           " flow (original framing and angle preserved)"],
 "LIGHT": ["Premium cinematic lighting quality — soft volumetric light, natural rim separation,"
           " elegant shadow gradients, high dynamic range, never flat or dull",
           "Elevated cinematic lighting — beautiful bounce and rim separation, soft highlight"
           " roll-off, elegant shadow gradients and high dynamic range, never flat"],
 "ATMO": ["Premium atmospheric depth — subtle volumetric haze and fine particulate, clean and"
          " immersive",
          "Rich atmospheric layering — delicate volumetric light and fine airborne detail, clean"
          " and immersive"],
 "GRADE": ["Premium editorial grade — rich clean colour, luminous mid-tones, deep-but-clean blacks,"
           " controlled elegant saturation, no faded or muddy tones, natural true skin preserved",
           "World-class editorial colour — rich and vivid yet clean, luminous mid-tones, deep-but-"
           "clean blacks, controlled saturation, nothing washed-out, natural skin protected"],
 "TEX": ["Elevated micro-texture and true premium material finish — realistic surfaces, natural"
         " imperfections, fine reflections, no plastic or noise",
         "Premium material realism — refined micro-texture, believable surface detail and natural"
         " reflections, nothing plastic or synthetic"],
 "PAL": ["Rendered as a rich, clean, harmonious premium palette — luminous and alive, never dull or"
         " faded, natural skin preserved"],
 "ALL": ["Premium editorial finish — rich clean colour and luminous mid-tones, deep-but-clean"
         " blacks, cinematic lighting with soft rim separation and high dynamic range, layered"
         " foreground-to-background depth, elevated material realism, immaculately clean and never"
         " dull or faded, natural true skin preserved"],
}
ADDON = {
 "water_v":"Water rendered crystal-clear in rich sea-blue and turquoise gradients, with beautiful caustics and clean sparkling reflections",
 "water_t":"Water kept deep, clean and glassy — premium and clear, never muddy or grey",
 "sky":"Sky richly graded and cinematic with elegant clouds and premium light, never flat or empty",
 "green":"Greenery lush and healthy with premium landscaping",
 "arch":"Architecture in fine premium materials with an immaculate finish",
}
SIGS = [c[:34] for v in BANK.values() for c in v]

def pick(key, seed):
    opts = BANK[key]
    if len(opts) == 1: return opts[0]
    h = int(hashlib.md5(seed.strip().encode("utf-8")).hexdigest(), 16)
    return opts[h % len(opts)]

def enrich_line(line):
    m = HEAD.match(line)
    if not m: return line
    label = m.group(2).strip().lower()
    if label not in TARGET: return line
    body = line.rstrip("\n")
    stripped = body.rstrip()
    if not stripped or stripped.endswith((":", "—")): return line
    if "STD-NEG" in body or "NEGATIVE:" in body.upper(): return line
    if any(s in body for s in SIGS): return line     # idempotent

    remainder = body[m.end():]
    packed = bool(SECOND.search(remainder)) or (". " in remainder)
    key = "ALL" if packed else TARGET[label]
    clause = pick(key, body)
    parts = [clause]
    if key in ("ENV","ATMO","ALL"):
        tonal = bool(TONAL.search(body))
        if WATER.search(body): parts.append(ADDON["water_t"] if tonal else ADDON["water_v"])
        if SKY.search(body):   parts.append(ADDON["sky"])
        if GREEN.search(body): parts.append(ADDON["green"])
        if ARCH.search(body):  parts.append(ADDON["arch"])
    sep = " " if stripped[-1:] in ".!?;)]\"'" else " — "
    nl = "\n" if line.endswith("\n") else ""
    return stripped + sep + ". ".join(parts) + "." + nl

def main():
    args = sys.argv[1:]; after = None
    if "--after" in args:
        i = args.index("--after"); after = args[i+1]; del args[i:i+2]
    if len(args) != 1:
        print("usage: premium_finish.py <file> [--after MARKER]"); sys.exit(2)
    path = args[0]
    with io.open(path,"r",encoding="utf-8") as f: lines = f.readlines()
    active = after is None; changed = 0; out = []
    for ln in lines:
        if not active:
            out.append(ln)
            if after in ln: active = True
            continue
        new = enrich_line(ln)
        if new != ln: changed += 1
        out.append(new)
    with io.open(path,"w",encoding="utf-8") as f: f.write("".join(out))
    print(f"{path}: enriched {changed} field lines")

if __name__ == "__main__":
    main()

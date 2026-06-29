#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 2 — Travel-Scenic (aira_set4.txt / aira_set5.txt).
These files use a non-standard layout (no BODY POSTURE field). The held pose lives
in CHOREOGRAPHY / WEARING-ACTION (set4) or the IMAGE prose (set5); both have a
SUBJECT FRAMING & POSITION recap line ending in the ORIENTATION LOCK anchor, plus
timed SHOT BREAKDOWN beats.

This tool inserts a full per-limb "Her pose reads" recap into SUBJECT FRAMING &
POSITION, just before ORIENTATION LOCK, on every frame. The recap is GROUNDED and
REAL (travel-scenic = maximum realism), faithful to each frame's actual action
(classified from the frame's own pose text into a motivated archetype). It leaves
the original CHOREOGRAPHY line, the IMAGE prose and ALL beats untouched.

Usage: python3 _tools/travel_fb.py "<path>"
Idempotent: skips any frame whose SUBJECT FRAMING already contains "Her pose reads".
"""
import io, re, sys

ANCHOR = " ORIENTATION LOCK \u2014 preserve this exact left-to-right composition; do not mirror, flip or invert the frame."

# ---- per-limb archetype scaffolds (grounded, real; lead/trailing where handedness is free) ----
SCAFFOLDS = {
    "locomotion": [
        "gaze carried ahead in her direction of travel, chin level and assured; head leading the line of the walk; the shoulders swinging in easy opposition to the stride; the leading arm easing forward while the trailing arm swings back, hands relaxed and open; torso tall and carried forward over the steps; waist rotating gently with each stride; the front leg reaching to plant heel-first while the rear leg drives off the toe; weight rolling heel-to-toe from foot to foot in true ground contact; hair and fabric lifting a beat behind the motion.",
        "gaze set along her path, calm and purposeful; head balanced and level into the travel; one shoulder easing forward as the opposite arm counter-swings, hands loose; torso lifted and moving forward through the step; waist turning softly with the gait; the lead foot rolling onto the ground as the trailing foot pushes off behind; weight transferring smoothly forward, soles in real contact; hair and hem trailing the stride.",
        "gaze travelling ahead toward her next mark, alert and easy; head carried level on a long neck; the shoulders relaxed and alternating with the walk; the forward arm swinging up gently as the other draws back, fingers easy; torso upright and gliding over the legs; waist loose and counter-rotating with the steps; the planting foot meeting the ground heel-first while the rear toe lifts to swing through; weight flowing foot to foot with grounded, gliding steps; hair lifting and resettling with each pace.",
    ],
    "spin": [
        "gaze sweeping round with the turn, bright and alive; head tipping with the rotation; both shoulders open and carrying the spin; both arms sweeping wide and lifted, fingers relaxed and spread; torso tall with a gentle lift through the spine, revolving through the turn; waist winding with the rotation; the pivot leg planted and bearing the turn while the free leg sweeps out and tucks; weight centred over the spinning foot, the other grazing the ground; hair and fabric fanning out with the spin.",
        "gaze trailing the turn then finding its line, eyes shining; head carried round with the rotation; shoulders level and open through the spin; the arms floating wide and high in a balletic line, fingers soft; torso lengthened and turning on its axis; waist coiling through the turn; the supporting leg rooted on the ball of the foot while the other arcs out; weight spinning over the planted foot; hair and hem sweeping into a wide arc.",
    ],
    "throw": [
        "gaze lifting up after the release, eyes wide and delighted; head tipping back with the upward motion; both shoulders driving up and open; both arms extending upward and out in the throw, fingers releasing and spread; torso arching back through the launch; waist opening with the upward drive; both legs planted and driving up from the ground, knees springing; weight driving up through planted feet; hair and fabric lifting on the upward burst.",
    ],
    "seated": [
        "gaze easing toward the lens or her task, soft and composed; head level with a gentle tilt; the shoulders relaxed and open; one arm resting or working at the task while the other settles, hands articulate; torso poised and lengthened over the seat; waist long with a gentle lean; the legs folded or crossed at the seat, one knee leading; weight settled into the seat and the grounded foot; hair falling naturally with the seated poise.",
    ],
    "gesture": [
        "gaze drawn to her hands then lifting, intent and soft; head tilting into the gesture; the working shoulder rising as the hands engage, the other settling; both hands caught mid wearing-action, fingers precise and articulate; torso poised and inclined a touch toward the action; waist long with a soft lean; the legs steady beneath her, one bearing a touch more weight; weight settled evenly with a gentle hip set; hair framing the lifted face.",
        "gaze following the wearing-action with quiet focus; head inclined toward her hands; one shoulder easing in as the arms work, the other relaxed; both hands articulate in the precise gesture, fingers unwarped; torso lengthened and softly leaning into the action; waist easy with a slight tilt; the legs grounded and even, one knee soft; weight balanced with a gentle counter-tilt; hair settling beside the working hands.",
    ],
    "glanceback": [
        "gaze thrown back over the shoulder to the lens, warm and inviting; the head and neck rotated back over the leading shoulder; the shoulders spiralling so the front opens to camera; the near arm easing across while the far arm trails; torso carrying forward into the scene with the upper body spiralling back; waist rotating between the forward hips and the turned shoulders; the legs carrying the forward line, one stepping ahead; weight rolling onto the forward foot as she moves away; hair sweeping with the turn of the head.",
    ],
    "wade": [
        "gaze level along her line through the water, serene; head leading the slow glide; the shoulders easing forward into the wade; both arms fanning out and trailing through the water for balance, fingers relaxed; torso leading gently forward through the surface; waist long, hips easing forward; the front leg wading ahead while the rear trails; weight transferring slowly forward through the submerged footing; hair and fabric drifting with the water's drag.",
    ],
    "lean": [
        "gaze out toward the view, reflective and calm; head tipped gently toward the gaze; the shoulders settling open and relaxed; one arm resting along the support while the other eases, hands soft; torso inclining gently into the lean; waist long with a soft side-tilt; the legs grounded with weight shared into the lean and the planted foot; weight eased between the support and her feet; hair settling with the quiet pose.",
    ],
    "stand": [
        "gaze level and assured to the lens, composed; head balanced and tall; both shoulders open, level and relaxed; the arms easy at her sides, hands relaxed and open; torso tall and lifted, open to camera; waist long with a soft hip counter-tilt; both legs grounded and even, one taking a touch more weight; weight settled and balanced over both feet in true ground contact; hair settling around her.",
        "gaze steady to camera with quiet confidence; head level and poised; the shoulders squared and easy; both arms relaxed at her sides, fingers soft; torso tall and open, breath lifting the chest; waist long, hips set with a gentle counter-tilt; the legs planted even, one knee soft; weight grounded and balanced across both feet; hair falling naturally at rest.",
        "gaze calm and present, taking in the scene; head balanced with a soft tilt; the shoulders open and dropped, unhurried; one hand resting easy while the other hangs relaxed, fingers soft; torso lifted and quietly poised; waist long with a light contrapposto; one leg taking the weight as the other eases, knee soft; weight settled into the standing leg with real ground contact; hair resting against her shoulders.",
    ],
}

# keyword -> archetype (checked in priority order; matched at word-start via \b prefix)
RULES = [
    ("spin",       ["pirouette", "spin", "twirl", "whirl", "turn on the", "turning"]),
    ("throw",      ["throw", "toss", "fling", "hurl"]),
    ("seated",     ["sit", "booth", "the wheel", "basket", "folded over", "crossed knee", "seated", "perched", "stool", "recline"]),
    ("wade",       ["wade", "wading", "glide", "gliding", "into the water", "submerged", "swim", "drift into"]),
    ("glanceback", ["over the shoulder", "over her shoulder", "rotated back", "head rotated", "back over", "glance back", "look back", "back toward camera"]),
    ("gesture",    ["fasten", "clasp", "lace", "lacing", "tying", "knot", "cinch", "zip", "wrap", "pull on", "pulls on", "shape the", "shaping", "reach", "rising into", "hand rising", "easing down", "adjust", "lifting the", "draw", "clay", "earring", "scarf", "shades"]),
    ("lean",       ["window-gaze", "window", "lean", "gazing", "against the rail", "barre", "railing"]),
    ("locomotion", ["stroll", "walk", "stride", "step", "descent", "descend", "exit", "advance", "dismount", "deeper", "into the"]),
]

def classify(text):
    t = text.lower()
    for arch, kws in RULES:
        for kw in kws:
            if re.search(r'\b' + re.escape(kw), t):
                return arch
    return "stand"

# pose-cue keywords used to pick the pose sentence out of set5 prose
POSE_CUES = ["captured", "caught", "weight", "mid-", "step", "stride", "walk", "wade",
             "glide", "sit", "fasten", "clasp", "lace", "reach", "spin", "twirl", "pirouette",
             "lean", "gaz", "stand", "lift", "settl", "twist", "rotat", "kneel", "perch",
             "drape", "fold", "sway", "pivot", "rise", "rising", "poised", "tilt", "crouch",
             "turns", "turning", "throw", "toss", "wrap", "tying", "knot", "descend"]

def clean_lead(s):
    s = s.strip().rstrip(".")
    # keep it tight: cut at an em-dash flourish if very long
    if len(s) > 150 and " \u2014 " in s:
        s = s.split(" \u2014 ", 1)[0].strip()
    if s:
        s = s[0].lower() + s[1:]
    return s

def main():
    path = sys.argv[1]
    text = io.open(path, encoding="utf-8").read()
    # frame headers: --- FRAME k · ... ---  or  ---- FRAME k · ... ----
    fhdr = re.compile(r'(?m)^-{3,4}\s*FRAME\s+\d+\s*\u00b7')
    starts = [m.start() for m in fhdr.finditer(text)]
    if not starts:
        raise SystemExit("no FRAME headers found")
    starts.append(len(text))
    counters = {}
    out = text
    edits = 0
    # process high-to-low so offsets stay valid
    for i in range(len(starts) - 2, -1, -1):
        bstart, bend = starts[i], starts[i + 1]
        block = out[bstart:bend]
        if ANCHOR not in block:
            continue
        if "Her pose reads" in block:
            continue
        # IMAGE part ends at VIDEO PROMPT (anchor should be inside IMAGE part)
        vm = re.search(r'(?m)^VIDEO PROMPT', block)
        img_end = vm.start() if vm else len(block)
        anchor_pos = block.find(ANCHOR)
        if anchor_pos == -1 or (vm and anchor_pos > img_end):
            continue
        # pose source text for classification + lead
        chor = re.search(r'(?m)^CHOREOGRAPHY[^:]*:\s*(.+)$', block[:img_end])
        if chor:
            pose_src = chor.group(1)
            lead = clean_lead(pose_src)
        else:
            # set5 prose: classify from the subject pose sentence; no fragile lead-quote
            ip = re.search(r'(?m)^IMAGE PROMPT', block)
            prose = block[ip.end():img_end] if ip else block[:img_end]
            lead = ""
            picked = ""
            for sent in re.split(r'(?<=[.;])\s+', prose):
                sl = sent.lower()
                if "----" in sent or "framing is" in sl or "spatial logic" in sl or "subject framing" in sl:
                    continue
                if not ("she " in sl or " her " in sl or sl.startswith("she")):
                    continue
                if any(re.search(r'\b' + k, sl) for k in POSE_CUES):
                    picked = sent
                    break
            pose_src = picked or prose
        fhead = block.split("\n", 1)[0]
        arch = classify((pose_src or "") + " " + fhead)
        variants = SCAFFOLDS[arch]
        idx = counters.get(arch, 0)
        scaffold = variants[idx % len(variants)]
        counters[arch] = idx + 1
        if lead:
            recap = "Her pose reads as %s \u2014 %s" % (lead, scaffold)
        else:
            recap = "Her pose reads: %s" % scaffold
        block = block.replace(ANCHOR, " " + recap + ANCHOR, 1)
        out = out[:bstart] + block + out[bend:]
        edits += 1
    io.open(path, "w", encoding="utf-8").write(out)
    print("inserted recaps:", edits)

if __name__ == "__main__":
    main()

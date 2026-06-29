#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 2 — Action reels (Heavy-Detail, Set 2 Expression, Master Set).
These files keep their pose fields INLINE inside one big IMAGE-PROMPT paragraph:
  'BODY POSTURE & WEIGHT: ...' (or 'BIOMECHANICS & WEIGHT: ...' in Master Set) and
  'SUBJECT FRAMING & POSITION: ... ORIENTATION LOCK — preserve ... invert the frame.'
plus a VIDEO 'SUBJECT + OBJECT ACTION (timecoded)' line.

This tool inserts a full per-limb 'Her pose reads' recap into SUBJECT FRAMING &
POSITION, just before the ORIENTATION LOCK anchor, on every frame. The recap quotes
that frame's real posture clause (faithful lead) then adds an action-ready per-limb
breakdown chosen by an ACTION archetype. NON-DESTRUCTIVE: the existing BODY POSTURE /
BIOMECHANICS clause, the timecoded action, and everything else are left intact.
Subject is action-ready every frame; physics believable; identity-safe (face = gaze/
expression only); swim/underwater = neutral buoyancy (no foot-weight). Idempotent.

Usage: python3 _tools/action_fb.py "<path>"
"""
import io, re, sys

ANCHOR = " ORIENTATION LOCK \u2014 preserve this exact left-to-right composition; do not mirror, flip or invert the frame."

SCAFFOLDS = {
 "establish": "gaze level and reading the scene with cold focus; head steady, turned to the action; both shoulders settled and squared, alive with breath; the RIGHT arm poised and ready with the hand relaxed but set; the LEFT arm easy and counter-balanced at her side; torso upright and composed in living stillness; waist long with the hips squared, weight carried on the back foot; the RIGHT leg bearing the load with a soft knee while the LEFT braces with one heel just lifted; both feet planted and grounded, weight back and ready to spring; hair alive in the wind, sealed and controlled.",
 "cockpit": "gaze locked dead ahead through the screen, hard and level; head steady, chin level against the G; both shoulders coiled forward over the wheel; the RIGHT hand gripping the wheel with raised tendons; the LEFT hand locked on the opposite rim, knuckles set; torso pinned back into the seat by acceleration, core braced; waist compressed, hips planted in the seat; the RIGHT leg driving the throttle with a flexed ankle while the LEFT braces hard on the floor; both feet committed to the pedals, weight pinned rearward; braid snapping straight back in the rush.",
 "launch": "gaze fixed dead ahead, pupils tight on the vanishing point; head held level and steady through the lurch; both shoulders driving forward then pinned; the RIGHT hand clamping the wheel or grip while the LEFT hand locks beside it, tendons raised; torso thrown back into the seat by explosive acceleration, core locked; waist braced, hips pinned; the RIGHT leg stamping the throttle while the LEFT braces on the floor; both feet committed, weight slamming rearward; braid whipping straight back as speed builds.",
 "chase": "gaze drilling down the road in a thousand-yard lock; head dead-level and steady; both shoulders driving and committed forward; the RIGHT hand firm on the wheel with micro-corrections in the wrist while the LEFT controls the opposite rim; torso forward-leaning into the speed, weight centred and driving; waist engaged, hips set into the seat; the RIGHT leg steady on the throttle with the heel down while the LEFT braces; both feet planted and controlling, weight centred; braid streaming horizontal in the slipstream.",
 "react": "gaze blown wide and snapping to the hazard, whites flashing at the edges; head whipping toward the threat; both shoulders snapping square to the danger; the RIGHT hand tightening its grip with the wrist already turning into the correction while the LEFT hand braces hard; torso pitching forward over the dipping nose, core catching the load; waist bracing, hips pitching forward; the RIGHT leg easing off power while the LEFT boot braces the floor; both feet loading for the reaction, weight pitching forward; braid whipping with the head-snap.",
 "drift": "gaze fierce and narrowed through the slide, reading the exit; head braced and steady against the lateral G; both shoulders driving the counter-steer; the RIGHT arm cranking full opposite-lock with forearm cords standing out while the LEFT arm braces the wheel; torso thrown against the lateral G, braced and coiled; waist torqued, hips wedged into the seat; the RIGHT leg feeding throttle mid-slide while the LEFT boot stays hard on the floor; both feet committed, weight slung outward against the slide; braid flung across the shoulder by the lateral throw.",
 "leap": "gaze locked on the landing point ahead, committed; head leading the airborne arc; both shoulders thrown forward and reaching; the RIGHT arm reaching ahead for the catch with fingers splayed while the LEFT arm trails then gathers; torso stretched into a committed flying line, core braced; waist extended, hips opening into the leap; the RIGHT leg reaching to lead the landing while the LEFT trails and gathers; both feet off the ground, weight suspended at the arc's peak; hair streaming back off the leap.",
 "strike": "gaze drilling into the strike's mark, eyes fierce; head squared and driving behind the blow; the RIGHT shoulder whipping forward through the strike while the LEFT shoulder tucks in guard; the RIGHT arm driving the blow with the fist or edge leading and the forearm corded while the LEFT hand stays raised in a tight guard; torso torqued through the hips into the strike, core rotated; waist whipping with the rotation, hips driving forward; the RIGHT rear leg pivoting on the ball as it drives while the LEFT front leg braces; both feet driving the ground, weight transferring forward through the blow; hair whipping with the torque.",
 "sprint": "gaze pinned ahead on the exit, hard and driving; head leading the hard run; the shoulders driving in opposition to the legs; the RIGHT arm and LEFT arm pumping hard in loose driving blades; torso pitched forward over the driving legs, core driving; waist driving with the stride, hips powering ahead; the RIGHT leg and LEFT leg in a full sprint with opposite arm and leg driving; both feet striking and pushing off in real contact, weight powering forward; hair streaming back off the run.",
 "brace": "gaze level and hard on the threat, reading it; head steady and squared; both shoulders squared and dropped, packed low; the RIGHT arm loaded and ready while the LEFT arm braces for balance; torso braced and coiled, core locked; waist tight, hips dropped low and set; the RIGHT leg and LEFT leg planted wide in a low grounded stance with both knees bent; both feet gripping the ground, weight low and forward, coiled to move; hair settling against the charged air.",
 "helm": "gaze sweeping the swells with steady nerve; head squared into the gale; both shoulders square to the threat and braced; the RIGHT hand gripping the tiller or rail with knuckles set while the LEFT arm reaches out for balance; torso braced wide and low against the pitch, core centred; waist low, hips squared over the deck; the RIGHT leg and LEFT leg braced wide on the pitching wet deck with knees soft; both grip-soled feet planted and weighted low, riding the heave; soaked braid whipping in the gale.",
 "swim": "gaze fixed on her line through the water, calm and committed; head leading the glide with the neck long; both shoulders rolling with the stroke; the RIGHT arm reaching and pulling through the water while the LEFT arm extends in counter-stroke, fingers together; torso streamlined and undulating with the swim; waist driving the line, hips rolling; the RIGHT leg and LEFT leg trailing in a fluid pointed flutter; feet neutral and buoyant with no ground contact, weight suspended in the water; hair drifting free in the current.",
 "summon": "gaze blazing and commanding on the force before her; head lifted and resolute; both shoulders opening wide and squared with power; the RIGHT arm and LEFT arm both raised and extended in command with fingers spread as the magic answers; torso lengthened and rooted, chest open and driving the gesture; waist long, hips squared and grounded; the RIGHT leg and LEFT leg planted firm and even, braced against the force; both feet rooted in real contact, weight centred and immovable; hair and clothing streaming back off the surge.",
 "ride": "gaze pinned forward along the ride, fierce and steady; head low and committed in the line; both shoulders rolled forward over the mount; the RIGHT hand gripping for control while the LEFT hand braces and holds on; torso leaning into a committed riding crouch, core tight; waist set forward, hips locked to the mount; the RIGHT leg and LEFT leg clamped to the flanks with knees gripping; feet set and braced, weight committed forward over the mount; hair streaming back off the speed.",
 "balance": "gaze fixed and precise on her next point, focused; head level and still for balance; both shoulders open and level, micro-adjusting; the RIGHT arm extended for counter-balance while the LEFT arm reaches out to steady the line; torso tall and poised over the narrow base, core engaged; waist long, hips stacked precisely over the support; the RIGHT support leg bearing the weight with a soft knee while the LEFT extends to balance; both feet precise on the narrow footing, weight pinpoint and controlled; hair settling with the held poise.",
}

# keyword -> archetype (priority order; matched at word-start via \b prefix)
RULES = [
 ("swim",    ["underwater","swim","kicking through the water","sphere of air","weightless in the water","diving through the water"]),
 ("summon",  ["raises both hands","both hands raised","summon","pendant flar","parts the wave","calls the","conjur","command the","raises her hand","arms raised","casting"]),
 ("ride",    ["riding crouch","astride","mounted","rides the","saddle","on the back of","bareback","riding the"]),
 ("drift",   ["opposite-lock","opposite lock","counter-steer","drift","slung sideways","lateral g","slide","oversteer","slung past"]),
 ("strike",  ["palm-heel","palm heel","elbow-strike","spinning back-fist","back-fist","punch","strike","kick","jab","clothesline","blow","cross into","hammer"]),
 ("leap",    ["leap","vault","airborne","apex of","mid-vault","flight across","long-jump","soar","dive-leap","hurdle","mid-flight","jump"]),
 ("sprint",  ["sprint","full-sprint","mid full-sprint","dash","running","charge","run-off","footwork","tatkar"]),
 ("launch",  ["launch","at the moment of launch","explosive","pinned back into the seat","acceleration throws","lurch"]),
 ("cockpit", ["seated low in the cockpit","cockpit","gripping the wheel","both gloved hands gripping the wheel","white-knuckle grip","hands on the wheel","at the wheel"]),
 ("react",   ["pitching forward","snaps toward","blown wide","reads it","reads the hazard","braking","nose dips","snapping square","recoil","flinch"]),
 ("helm",    ["helm","tiller","on the deck","pitching wet deck","braced wide","longboat","at the rail","ship","boat"]),
 ("balance", ["narrow beam","high-wire","on the beam","ledge","tightrope","poised on","balance","balancing","gantry edge","catwalk","girder"]),
 ("brace",   ["power-stance","grounded power","planted wide","low stance","fighting stance","braced and coiled","crouched brace","low grounded"]),
 ("chase",   ["forward-lean","commitment into the speed","full-flight","weight centred","driving","at speed","cruising","holding the line"]),
]

GROUND_CUE = re.compile(r'\b(planted|rooted|grounded|weight low|weight on the back|stands?|tall on|braced wide|landing|landed|crouch|kneel|seated|balanced|demi-pli|stance|astride|on the deck|on the altar)\b', re.I)
AIR_CUE = re.compile(r'\b(airborne|mid-air|off the ground|in the air|fully suspended|at the apex|mid-flight|in flight)\b', re.I)

def classify(text, lead=""):
    t = text.lower()
    arch = "establish"
    for a, kws in RULES:
        if any(re.search(r'\b' + re.escape(kw), t) for kw in kws):
            arch = a; break
    # guard: never put an airborne scaffold on a clearly grounded posture
    if arch in ("swim", "leap") and lead and GROUND_CUE.search(lead) and not AIR_CUE.search(lead):
        ll = lead.lower()
        if re.search(r'\b(balanc|precise|narrow|beam|gear-tooth|ledge|wire)', ll):
            arch = "balance"
        elif re.search(r'\b(duck|tuck|crouch|coil|brace|low)', ll):
            arch = "brace"
        else:
            arch = "establish"
    return arch

def clean_lead(s):
    s = s.strip().rstrip(" .;")
    # trim a trailing 'living stillness' flourish parenthetical noise but keep substance
    if s:
        s = s[0].lower() + s[1:]
    return s

POSE_RE = re.compile(r'(?:BODY POSTURE & WEIGHT|BIOMECHANICS & WEIGHT):\s*(.+?)(?=\s+[A-Z][A-Z0-9 &/()\u2014+\-]{2,}:|\n)', re.S)
SCENE_RE = re.compile(r'(?:The beat:|Scene:)\s*(.+?)(?=\s+[A-Z][A-Z0-9 &/()\u2014+\-]{2,}:|\.)', re.S)

def main():
    path = sys.argv[1]
    text = io.open(path, encoding="utf-8").read()
    matches = list(re.finditer(re.escape(ANCHOR), text))
    if not matches:
        raise SystemExit("no ORIENTATION LOCK anchors found")
    out = []
    prev = 0
    edits = 0
    for mt in matches:
        p = mt.start()
        before = text[prev:p]
        if "Her pose reads" in text[max(0, p - 900):p]:
            out.append(before); out.append(ANCHOR); prev = mt.end(); continue
        # current frame's posture = LAST BODY POSTURE/BIOMECHANICS clause before this anchor
        look = text[max(0, p - 4000):p]
        pm = None
        for pm in POSE_RE.finditer(look):
            pass
        pose = pm.group(1).strip() if pm else ""
        sm = None
        for sm in SCENE_RE.finditer(look):
            pass
        scene = sm.group(1) if sm else ""
        arch = classify(pose + " " + scene, lead=pose)
        lead = clean_lead(pose)
        recap = ("Her pose reads as %s \u2014 %s" % (lead, SCAFFOLDS[arch])) if lead else ("Her pose reads: %s" % SCAFFOLDS[arch])
        out.append(before); out.append(" " + recap); out.append(ANCHOR)
        prev = mt.end()
        edits += 1
    out.append(text[prev:])
    io.open(path, "w", encoding="utf-8").write("".join(out))
    print("inserted recaps:", edits)

if __name__ == "__main__":
    main()

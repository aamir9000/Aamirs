#!/usr/bin/env python3
"""
fix_action_audio.py — convert per-frame AUDIO cue timestamps from absolute reel-time to
clip-relative (0-6s), so each frame's audio matches its 6-second clip.

The Action Master Set writes per-frame audio as `00:MM.m` (and ranges `00:MM.m–MM.m`) on the
old assembled-reel timeline, so later frames carry times like `00:08.4`/`00:18.0` (> 6s) and even
early ones start a few seconds in. This re-baselines EACH AUDIO line by subtracting floor(min
timestamp) from every timestamp in that line, so every frame's cues begin near 0 and sit inside
0-6s. Frame-1 lines (min = 0) are unchanged.

Usage: python3 _tools/fix_action_audio.py "<file>"
"""
import sys, io, re, math

TOK = re.compile(r'`00:(\d+(?:\.\d+)?)(?:\s*[\u2013-]\s*(?:00:)?(\d+(?:\.\d+)?))?`')

def fix_line(line):
    if not line.lstrip().startswith("AUDIO"):
        return line, False
    toks = TOK.findall(line)
    if not toks:
        return line, False
    vals = []
    for a, b in toks:
        vals.append(float(a))
        if b: vals.append(float(b))
    base = math.floor(min(vals))
    if base == 0:
        return line, False  # already clip-relative (frame 1)
    def repl(m):
        a = float(m.group(1)) - base
        if m.group(2):
            b = float(m.group(2)) - base
            return f"`00:{a:04.1f}\u2013{b:04.1f}`"
        return f"`00:{a:04.1f}`"
    new = TOK.sub(repl, line)
    return new, (new != line)

def main():
    path = sys.argv[1]
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    n = 0; out = []
    for ln in lines:
        new, ch = fix_line(ln)
        if ch: n += 1
        out.append(new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print(f"{path}: re-baselined {n} AUDIO lines to clip-relative")

if __name__ == "__main__":
    main()

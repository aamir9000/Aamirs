#!/usr/bin/env python3
"""
normalize_6s.py — force a single consistent duration model: EVERY frame/clip = 6 seconds.

The video shot-breakdowns ([00:00-00:06]) and per-frame "duration: 6 seconds" are already 6s.
This normalises the REEL-TOTAL / summary statements + MASTER AUDIO totals so nothing implies a
non-6s clip:
  * "Duration ... <total> <unit> <·|> N frames"  -> total recomputed to N*6 (keeps ~/≈, unit, fps tail).
  * "(<x>s each)"                                 -> "(6s each)".
  * "<M>-second ... score (<N> clips × <y>s)"     -> M = N*6, y = 6.
  * in any duration/clips line, "× <y>s"          -> "× 6s".
Recomputes from the frame/clip COUNT, so totals are always internally consistent.

Usage: python3 _tools/normalize_6s.py "<file>"
"""
import sys, io, re

def process_line(line):
    out = line

    # A) reel total immediately before "N frames": recompute total = N*6
    def total_repl(m):
        n = int(m.group('n'))
        return f"{m.group('pre') or ''}{n*6}{m.group('unit')}{m.group('sep')}{m.group('n')}{m.group('f')}"
    out = re.sub(
        r'(?P<pre>[~≈]\s*)?(?P<num>\d+(?:\.\d+)?)(?P<unit>\s*(?:seconds|second|secs|sec|s))'
        r'(?P<sep>\s*[·|]\s*)(?P<n>\d+)(?P<f>\s*frames)',
        total_repl, out)

    # B) "(x s each)" -> "(6s each)"
    out = re.sub(r'\(\s*\d+(?:\.\d+)?\s*s(?:ec(?:onds)?)?\s*each\s*\)', '(6s each)', out)

    # C) master audio: "M-second ... score (N clips × y s)" -> M=N*6, y=6
    def score_repl(m):
        clips = int(m.group('clips'))
        return f"{clips*6}{m.group('mid')}{m.group('clips')}{m.group('cm')}6{m.group('cu')}"
    out = re.sub(
        r'(?P<num>\d+)(?P<mid>[-\u2013 ]second[^()]*\(\s*)(?P<clips>\d+)'
        r'(?P<cm>\s*clips?\s*[x\u00d7]\s*)(?P<cl>\d+(?:\.\d+)?)(?P<cu>\s*s)',
        score_repl, out)

    # D) any "clips × y s" or duration "× y s" -> "× 6s" (only if line is duration/clip/score context)
    if re.search(r'(?i)duration|clips?\s*[x\u00d7]|score', out):
        out = re.sub(r'([x\u00d7]\s*)\d+(?:\.\d+)?(\s*s\b)', r'\g<1>6\g<2>', out)

    # E) "Frames: N · <total>s"  -> total = N*6
    out = re.sub(r'(?P<pre>Frames:\s*(?P<n>\d+)\s*[·|]\s*)\d+(?:\.\d+)?(?P<u>\s*s)\b',
                 lambda m: f"{m.group('pre')}{int(m.group('n'))*6}{m.group('u')}", out)

    # F) "N × 6s | <total>s total"  -> total = N*6
    out = re.sub(r'(?P<pre>(?P<n>\d+)\s*[x\u00d7]\s*6\s*s\s*[|·]\s*)\d+(?:\.\d+)?(?P<u>\s*s\s*total)',
                 lambda m: f"{m.group('pre')}{int(m.group('n'))*6}{m.group('u')}", out)

    # G) legacy windowed per-frame duration "DURATION: Xs (0:MM–0:NN of Ys ...)" -> uniform 6s line
    out = re.sub(r'DURATION:\s*\d+(?:\.\d+)?\s*seconds?\s*\(\s*0:[^)]*\)\.?',
                 'DURATION: 6 seconds (real-time; one 6-second frame of the reel).', out)

    # H) stray prose reel/loop totals -> frame-neutral (precise total lives in the master-audio line)
    for a, b in (
        ("a 21-second vertical", "a vertical"),
        ("an 18-second vertical", "a vertical"),
        ("24-second triumphant", "triumphant"),
        ("30-second reel", "seamless reel"),
        ("30-second loop", "seamless loop"),
    ):
        out = out.replace(a, b)

    return out

def main():
    if len(sys.argv) != 2:
        print("usage: normalize_6s.py <file>"); sys.exit(2)
    path = sys.argv[1]
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    n = 0; out = []
    for ln in lines:
        new = process_line(ln)
        if new != ln: n += 1
        out.append(new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print(f"{path}: normalized {n} lines")

if __name__ == "__main__":
    main()

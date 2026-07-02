#!/usr/bin/env python3
"""
fix_reel_totals.py — final duration cleanup so nothing implies a non-6s/frame reel.

Rules:
  1) "(running total 00:XX.X[ active; ~Ns with handles])"  -> "(one 6-second frame)"
     (old edited-reel cumulative that implied trimmed <6s frames).
  2) "finished <N>s <...>reel"  -> drop the "<N>s" (frame-neutral; precise total lives in the
     'Duration: 36/42/48 seconds | N frames' header + 'N-second score (M clips × 6s)' line).
  3) range-format per-frame arc "Fk (0:a-0:b)" -> "Fk (0:(k-1)*6-0:k*6)" (6s-per-frame grid).

Usage: python3 _tools/fix_reel_totals.py "<file>"
"""
import sys, io, re

def fmt(sec):
    return f"{sec//60}:{sec%60:02d}" if sec >= 60 else f"0:{sec:02d}"

def fix_line(line):
    ch = False
    new = re.sub(r'\(running total 00:[\d.]+(?:\s*active;\s*~\d+s with handles)?\)',
                 '(one 6-second frame)', line)
    if new != line: ch = True; line = new
    new = re.sub(r'finished \d+(?:\.\d+)?s ', 'finished ', line)
    if new != line: ch = True; line = new
    # range-format arc markers Fk (0:a–0:b)
    if re.search(r'F\d+\s*\(0:[\d.]+\s*[\u2013-]\s*0:[\d.]+\)', line):
        def rng(m):
            k = int(m.group(1))
            return f"F{k} ({fmt((k-1)*6)}\u2013{fmt(k*6)})"
        new = re.sub(r'F(\d+)\s*\(0:[\d.]+\s*[\u2013-]\s*0:[\d.]+\)', rng, line)
        if new != line: ch = True; line = new
    return line, ch

def main():
    path = sys.argv[1]
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    n = 0; out = []
    for ln in lines:
        new, c = fix_line(ln)
        if c: n += 1
        out.append(new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print(f"{path}: cleaned {n} lines")

if __name__ == "__main__":
    main()

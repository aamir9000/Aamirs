#!/usr/bin/env python3
"""
fix_master_arc.py — rescale MASTER-AUDIO 'Dynamic arc' timelines from the old per-frame grid
to the 6-second-per-frame grid, so the master audio spans the same length as the 6s video reel.

Handles lines like:
  "Dynamic arc across all 7 frames (0:00-0:24.5): F1 (0:00) ...; F2 (0:03.5) ...; F7 (0:21) ..."
->
  "Dynamic arc across all 7 frames (0:00-0:42): F1 (0:00) ...; F2 (0:06) ...; F7 (0:36) ..."

Deterministic: total = N*6; each Fk marker = (k-1)*6 seconds. Only touches lines that contain
"across all N frames (0:00-0:T)".

Usage: python3 _tools/fix_master_arc.py "<file>"
"""
import sys, io, re

def fmt(sec):
    # seconds -> "M:SS" if >=60 else "0:SS"
    if sec >= 60:
        return f"{sec//60}:{sec%60:02d}"
    return f"0:{sec:02d}"

def fix_line(line):
    m = re.search(r'across all (\d+) frames\s*\(0:00\s*[\u2013-]\s*0:[\d.]+\)', line)
    if not m:
        return line, False
    n = int(m.group(1))
    total = n * 6
    # replace the total range
    line = re.sub(r'(across all \d+ frames\s*\(0:00\s*[\u2013-]\s*)0:[\d.]+(\))',
                  lambda mm: f"{mm.group(1)}{fmt(total)}{mm.group(2)}", line)
    # replace each Fk (0:x) marker with (k-1)*6
    def fk(mm):
        k = int(mm.group(1))
        return f"F{k} ({fmt((k-1)*6)})"
    line = re.sub(r'F(\d+)\s*\(0:[\d.]+\)', fk, line)
    return line, True

def main():
    if len(sys.argv) != 2:
        print("usage: fix_master_arc.py <file>"); sys.exit(2)
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
    print(f"{path}: rescaled {n} arc lines")

if __name__ == "__main__":
    main()

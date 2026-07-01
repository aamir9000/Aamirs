#!/usr/bin/env python3
"""
enrich_apply.py — safe, additive field-enrichment applier for the Aira concept files.

Usage:  python3 _tools/enrich_apply.py "<file path>" "<pairs.json>"

pairs.json = a JSON list of [old, new] string pairs (hand-authored, tailored per concept).

Safety rules (so we NEVER ruin anything):
  * Each `old` MUST occur EXACTLY ONCE in the whole file. If it occurs 0 or >1 times,
    the pair is REPORTED and SKIPPED (nothing is written until all pairs are unambiguous),
    unless it is already satisfied (old absent + new present => treated as done).
  * We only ever REPLACE the matched field text with an enriched version the author wrote.
    We never touch framing / camera / lens / wardrobe / action / identity lines (those are
    simply not in the pairs list).
  * Writes only if every pair is either applied or already-done. Prints a clear report.
"""
import sys, json, io

def main():
    if len(sys.argv) != 3:
        print("usage: enrich_apply.py <file> <pairs.json>"); sys.exit(2)
    path, pairs_path = sys.argv[1], sys.argv[2]
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    with io.open(pairs_path, "r", encoding="utf-8") as f:
        pairs = json.load(f)

    problems, applied, already = [], 0, 0
    staged = text
    for i, (old, new) in enumerate(pairs):
        c_old = staged.count(old)
        if c_old == 1:
            staged = staged.replace(old, new, 1)
            applied += 1
        elif c_old == 0:
            if staged.count(new) >= 1:
                already += 1
            else:
                problems.append((i, "NOT FOUND (0 matches, new absent too)", old[:80]))
        else:
            problems.append((i, f"AMBIGUOUS ({c_old} matches)", old[:80]))

    if problems:
        print("!! NOT WRITTEN — fix these pairs (add surrounding context to make unique):")
        for idx, why, snip in problems:
            print(f"  pair[{idx}] {why}: {snip!r}")
        print(f"(applied-would-be={applied}, already-done={already}, problems={len(problems)})")
        sys.exit(1)

    with io.open(path, "w", encoding="utf-8") as f:
        f.write(staged)
    print(f"OK: applied={applied}, already-done={already}, total_pairs={len(pairs)}")

if __name__ == "__main__":
    main()

# AIRA CONCEPT FILES — PROCESSING DIRECTIVE (Complete Spec)

## 0. GOAL (one line)
Transform every Aira concept `.txt` file into a clean, AI-generation-ready version by ADDING a per-frame framing section to image prompts, cleaning formatting/codes, restructuring video timestamps — without ever deleting a single piece of real descriptive content — then push each finished file to GitHub.

---

## 1. SOURCE & DESTINATION
- **Source files (originals, read-only):** `/projects/sandbox/concepts_dl/CONCEPTS/*.txt` (20 files; the duplicate "Aira — 20 More Full Reel Concepts · Set 3 …256.txt" was already deleted).
- **Output destination:** `/projects/sandbox/Aamirs/CONCEPTS/<same-filename>.txt`
- **Repo:** `aamir9000/Aamirs`, branch **`aira-prompts-enhanced`** (originals stay on `main` inside `CONCEPTS.zip`).
- **Rule:** one input file → ONE output file. If an input file holds 20 concepts, the output holds all 20 concepts in a single clean file (same filename).

---

## 2. THE FIVE TRANSFORMATIONS (apply to every file)

### 2A. ADD `SUBJECT FRAMING & POSITION:` to EVERY IMAGE PROMPT only
- **Placement:** immediately AFTER the `FRAMING:` line and BEFORE the `LENS + DOF + BOKEH:` line (Format B) / before `LENS + DOF + BOKEH:` (Format A markdown). It must sit with the other framing sections so it never breaks the document's flow.
- **NEVER add it to VIDEO PROMPTs.**
- **It must be authored per-frame** — read that frame's full IMAGE prompt AND its VIDEO prompt, the frame header (shot size + angle), `FRAMING:`, `SPATIAL LOGIC:`, `CHOREOGRAPHY`, `BODY POSTURE`, and the concept's overall theme/story/mood — then write prose that fits that exact frame as if it had always been there.
- **Every frame's section MUST be unique.** Angles/sizes differ frame to frame within a concept (WS → Full → Cowboy → MS → MCU → CU → ECU; high / low-hero / front / three-quarter / profile / over-the-shoulder). The section must reflect those exact differences — do NOT repeat the same details across frames of a concept.

**Each section must specify all five attributes, in flowing prose (NOT bullet points, NOT sub-labels):**
1. **Body turn / orientation** — how far the torso is rotated (square-front / ~30° three-quarter / full profile / turned away / mid-spin).
2. **How much of the body is in frame** — full body to the floor / cut at ankles / knees / mid-thigh (cowboy) / waist / chest / head-and-shoulders / extreme-detail.
3. **Camera distance** — near / mid / far, intimate vs. establishing.
4. **Horizontal placement** — left / right / centre (and node, e.g. upper-left third).
5. **Facing** — front shot / full frontal / three-quarter front / profile / over-the-shoulder / back shot.

**Anti-flip string (mandatory closing clause of every section):**
`ORIENTATION LOCK — preserve this exact left-to-right composition; do not mirror, flip or invert the frame.`

### 2B. STRIP ASTERISKS
- Remove every `*` character (all formatting `**bold**` markdown). Formatting-only; deletes zero words. (Format B files already have none.)

### 2C. REMOVE INTERNAL CODES (they do NOT affect AI generation — confirmed)
Delete these bookkeeping tags but KEEP all surrounding descriptive words:
- `AO-X`, `AO.1`, `AO.2`, `AO.3`, `AO.7`, `AO.8` (and ranges like `AO.1–AO.3`)
- `AU.4`, `BB` (face-lock refs), `AT #1`/`AT #2`… (camera-move codes), `AX #87` (format ref)
- `AW #126`, `AF #66`, `AQ #77`, `AC #66`, `AP #71` (wardrobe/footwear/makeup/accessory/hair catalogue numbers)
- Any "(AO.8 living stillness)" style parenthetical → remove code, keep meaningful words; delete empty leftover parentheses and fix double spaces.
- **KEEP** `STD-NEG-IMG` / `STD-NEG-VID` (these are real negative-prompt content), and KEEP the actual rule text in GLOBAL RULES (just remove the code tokens).

### 2D. SIMPLIFY THE `SUBJECT:` LINE (first section of every image prompt)
- Make every image prompt's subject-introduction line exactly:
  `SUBJECT: Aira [paste identity-lock reference sheet here].`
- i.e. "Aira", then a placeholder for the reference sheet, then proceed to the next section. Remove the "no physical enumeration; likeness from reference only / AO-X" trailing text.

### 2E. RESTRUCTURE VIDEO TIMESTAMPS (do NOT change any words)
- Timestamps already exist; only re-place/structure them cleanly so VEO parses them perfectly.
- Convert inline runs into discrete one-beat-per-line lists:
```
CHOREOGRAPHY & SUBJECT ACTION (timed, fluid):
- 0.0–2.0s — she stands at deck-edge, inhales, robe settling.
- 2.0–4.0s — she takes two unhurried steps toward the water, weight rolling heel-to-toe.
- 4.0–6.0s — she pauses at the lip, head tilting toward the horizon.
```
- Uniform notation: `X.X–X.Ys` (en-dash, one decimal, lowercase s), `—` (em-dash) before the action text, one beat per line, contiguous and in order.
- Beats already discrete (Format A) need no change beyond notation consistency.
- **Do not add tags, summaries, or "total Xs" labels. Do not reword descriptions.**

---

## 3. ABSOLUTE HARD RULE
**Never remove a single piece of real descriptive content from any concept or prompt — ever.** All changes are: additive (new section), formatting-only (asterisks), code-token removal, subject-line trim, and timestamp re-layout. Verify after every file.

---

## 4. QUALITY BAR (this is the part that was failing — read carefully)
The section must read like the human author wrote it originally — cinematic, specific, in the file's own voice. NOT generic, NOT a keyword lookup, NOT bullet points/sub-labels.

**GOOD (target quality — hand-authored, Concept 01 Frame 5, over-the-shoulder):**
> SUBJECT FRAMING & POSITION: Aira is framed from roughly the chest upward — her back-shoulder fills the soft near-foreground while her face, rotated back toward camera in a fluid spiral, sits sharp on the upper-third line. The composition is an over-the-shoulder view: her torso faces the sea horizon with forearms resting on the pool's infinity lip, but her head and shoulders have rotated back through roughly 120 degrees to deliver the glance to the lens. Camera is close and intimate, pushing past the shoulder mass to settle on her expression — the sea-glow horizon reads as a creamy warm wash behind her turned face. She is positioned slightly left-of-centre so the horizon opens to frame-right. The body turn creates maximum torsion — back to the world, face to us, the classic inviting spiral. ORIENTATION LOCK — preserve this exact left-to-right composition; do not mirror, flip or invert the frame.

**BAD (avoid — sterile/templated, reused phrasing across frames):**
> SUBJECT FRAMING & POSITION: Aira reads as a complete but environment-dwarfed figure within the wide establishing composition... She anchors the dead center of the frame... Camera maintains a wide establishing distance... ORIENTATION LOCK — ...

**BAD (avoid — bullet/sub-label format that breaks flow):**
> SUBJECT FRAMING & POSITION:
>   Body turn/orientation: torso at a gentle angle, viewed from above.
>   Body in frame: full body (small in frame).
>   Camera distance: far.

Calibration checklist for each section: Does it (a) name the real scene/props of THIS frame, (b) describe the actual body action from the choreography, (c) differ clearly from the other frames in the concept, (d) speak the file's cinematic voice, (e) flow as one prose paragraph, (f) end with the ORIENTATION LOCK line?

---

## 5. PER-FILE WORKFLOW
1. Copy/work from the original in `concepts_dl/CONCEPTS/`.
2. Strip asterisks (verify only `*` removed; line count unchanged).
3. Remove internal codes (keep descriptions; clean leftover spaces/parens).
4. Normalise every `SUBJECT:` line.
5. Restructure video timestamps (words unchanged).
6. **Hand-author** the `SUBJECT FRAMING & POSITION:` section for EVERY image prompt, reading each frame fully + the concept theme, ensuring per-frame uniqueness and angle-accuracy.
7. Verify (see §6).
8. Write output to `/projects/sandbox/Aamirs/CONCEPTS/<filename>.txt`.
9. `git add` that file, commit with a clear message, push via the GitHub push tool to branch `aira-prompts-enhanced`.
10. Give the user the branch link and move to the next file.

---

## 6. VERIFICATION (run for every file before pushing)
- `SUBJECT FRAMING & POSITION:` count == number of IMAGE PROMPTs in the file.
- 0 of those sections fall inside a VIDEO PROMPT.
- No two `SUBJECT FRAMING & POSITION:` lines are back-to-back (no double inserts).
- All sections are unique (no identical text).
- Every section ends with the exact ORIENTATION LOCK clause.
- 0 remaining asterisks; 0 remaining codes (`AO.`, `AO-X`, `AU.`, `AT #`, `AW #`, `AF #`, `AQ #`, `AC #`, `AP #`, `BB`, `AX #`).
- Every `SUBJECT:` line == `SUBJECT: Aira [paste identity-lock reference sheet here].`
- All video timestamps in uniform `X.X–X.Ys —` discrete-line form.
- No descriptive sentence from the original is missing (additive-only diff).

---

## 7. FORMAT NOTES
- **Format A (markdown, ~18 files):** `**SECTION:**` labels, `## Frame X of Y — IMAGE PROMPT`. Has thousands of asterisks. Negatives written inline.
- **Format B (plain, `aira_set4.txt`, `aira_set5.txt`):** `--- FRAME X · SIZE · ANGLE ---` headers, plain `SECTION:` labels, `NEGATIVE: STD-NEG-IMG`. No asterisks.
- Filenames contain unicode (`·` middot, `—` em-dash, `–` en-dash) shown as mojibake in some terminals — handle via UTF-8, quote paths.

---

## 8. FILE INVENTORY & STATUS (20 files)
| # | File | Image prompts | Status |
|---|------|:---:|:---:|
| 1 | aira_set4.txt | 117 (20 concepts) | DONE & pushed (quality = "BAD" baseline for C03–C20; C01–C02 good — consider redo to GOOD bar) |
| 2 | aira_set5.txt | 123 | TODO |
| 3 | Concept 100 · The Unboxing.txt | 6 | done earlier then branch cleared — REDO under final rules |
| 4 | Concept 170 · Phoenix Crash.txt | 8 | done earlier then branch cleared — REDO under final rules |
| 5 | Concepts 91–110 · FULL Heavy-Detail.txt | 26 | TODO |
| 6 | 20 Beauty Ad Reels · Mind-Blowing Choreograpgy.txt | 129 | TODO |
| 7 | 20 Cinematic Reels New Set.txt | 123 | TODO |
| 8 | 20 Full Reel Concepts Set 4 (Concepts 51.txt | 122 | TODO |
| 9 | 20 Full Reel Concepts Set 5 (Concepts 71.txt | 51 | TODO |
| 10 | 20 Full Reel Concepts Set 5 (cont 2).txt | 13 | TODO |
| 11 | 20 Full Reel Concepts · Set 5 (cont.txt | 13 | TODO |
| 12 | 20 Magical Action Reels Heavy-Detail.txt | 152 | TODO |
| 13 | 20 Magical Action Reels Set 2 Expression.txt | 152 | TODO |
| 14 | 20 More Full Reel Concepts Set 3.txt | 128 | TODO |
| 15 | 20 Reel Concepts Master-Depth Build.txt | 140 | TODO |
| 16 | Magical Action Reels · Master Set.txt | 130 | TODO |
| 17 | NEW Reel Concepts (131–150) .txt | 135 | TODO |
| 18 | Set 5 (cont 3) Clothes-Change Transformation.txt | 8 | TODO |
| 19 | Set 5 (cont 4) · Clothes-Change Transformation.txt | 7 | TODO |
| 20 | Time-Freeze Reel Set · Fully-Detailed Concepts.txt | 136 | TODO |

Total image prompts ≈ 1,719 (each needs one hand-authored section).

---

## 9. GITHUB
- Branch: `aira-prompts-enhanced`. Push one file per commit. Never push to `main`.
- Use the GitHub push tool (not raw `git push`).
- After each push, give the user: `https://github.com/aamir9000/Aamirs/tree/aira-prompts-enhanced`.

---

## 10. DECISIONS ALREADY CONFIRMED BY USER
- Section name = `SUBJECT FRAMING & POSITION:`.
- Image prompts only; video prompts untouched except timestamp re-layout.
- Remove internal codes (confirmed they don't affect generation).
- `SUBJECT:` line trimmed to `Aira [paste identity-lock reference sheet here]`.
- One input file → one combined output file (all its concepts).
- Push each finished file to the branch.
- Quality must equal the hand-authored Concept 01 / Concept 100 / Concept 170 standard — deeply read, theme-aware, per-frame-unique, flowing prose, no bullet points, no detail removed.

# AIRA PROMPT-PROCESSING — SYSTEM DIRECTIVE

## PURPOSE
Take the master Aira concept files (the `.txt` files that came out of `CONCEPTS.zip`) and turn each one into a clean, AI-generation-ready version. The work means ADDING a precise per-frame framing section to image prompts, cleaning up formatting and internal codes, normalising the subject line, and restructuring the video timestamps so a video model (VEO) reads them perfectly — all without ever deleting one piece of real descriptive content. Each finished file is pushed to GitHub for review.

## SOURCE, OUTPUT, REPO
- **Source (read-only originals):** `/projects/sandbox/concepts_dl/CONCEPTS/*.txt` (20 files; the one duplicate file has already been removed).
- **Output:** `/projects/sandbox/Aamirs/CONCEPTS/<same filename>.txt`.
- **One input file → ONE output file.** If an input file contains 20 concepts, the output contains all 20 concepts in that single clean file (same filename).
- **Repo / branch:** `aamir9000/Aamirs`, branch **`aira-prompts-enhanced`**. Originals stay safe on `main` inside `CONCEPTS.zip`. Push one finished file per commit; never push to `main`; use the GitHub push tool (not raw `git push`).

---

## THE FIVE THINGS TO DO IN EVERY FILE

### 1. Add a `SUBJECT FRAMING & POSITION:` section to EVERY image prompt
- **Where:** immediately AFTER the `FRAMING:` line and BEFORE the `LENS + DOF + BOKEH:` line, so it sits naturally among the existing framing sections and never breaks the document's flow.
- **Image prompts ONLY.** Never add it to a video prompt.
- **How to author it:** before writing, read that frame's full IMAGE prompt and its VIDEO prompt, the frame header (shot size + angle), the `FRAMING:`, `SPATIAL LOGIC:`, `CHOREOGRAPHY`, and `BODY POSTURE` lines, and understand the concept's overall theme, story and mood. Then write the section so it fits that exact frame as if it had always been there.
- **It must be unique for every frame.** Within a concept the angles and sizes change frame to frame (e.g. WS → Full → Cowboy → MS → MCU → CU → ECU; high / low-hero / front / three-quarter / profile / over-the-shoulder). The section must reflect those exact differences. Do NOT repeat the same wording or details across the frames of a concept.
- **Write it as one flowing prose paragraph** — never bullet points, never sub-labels like "Body turn:". It should read in the file's own cinematic voice.
- **It must clearly convey all five of these:**
  1. **Body turn / orientation** — how far the torso is rotated (squared front / about a three-quarter turn / full profile / turned away / mid-spin, etc.).
  2. **How much of the body is in frame** — full body to the floor / cut at the ankles / knees / mid-thigh (cowboy) / waist / chest / head-and-shoulders / extreme detail only.
  3. **Camera distance** — near / mid / far, and whether it feels intimate or establishing.
  4. **Horizontal placement** — left / right / centre (and the node if relevant, e.g. upper-left third).
  5. **Facing** — front shot / full frontal / three-quarter front / profile / over-the-shoulder / back shot.
- **Mandatory closing clause (exact text), as the last sentence of every section:**
  `ORIENTATION LOCK — preserve this exact left-to-right composition; do not mirror, flip or invert the frame.`
  (This is the anti-flip instruction. It belongs here because flipping is exactly what would ruin the carefully described left/right placement and body turn.)

### 2. Strip every asterisk
- Remove all `*` characters (the `**bold**` markdown). This is formatting-only and removes zero words. (The two plain-text files already have none.)

### 3. Remove internal bookkeeping codes (they do NOT affect AI generation)
- Delete these tokens but keep every surrounding descriptive word: `AO-X`, `AO.1`/`AO.2`/`AO.3` (and ranges like `AO.1–AO.3`), `AO.7`, `AO.8`, `AU.4`, `BB`, `AT #1`/`AT #2`…, `AX #…`, `AW #…`, `AF #…`, `AQ #…`, `AC #…`, `AP #…`.
- When a code sits inside a parenthetical such as "(AO.8 living stillness)", remove the code, keep any meaningful words, and clean up any empty parentheses or double spaces left behind.
- **KEEP** `STD-NEG-IMG` and `STD-NEG-VID` — these are real negative-prompt content, not codes. In the GLOBAL RULES block, keep the actual rule wording and only drop the code tokens.

### 4. Normalise the subject-introduction line
- Make the first line of every image prompt exactly:
  `SUBJECT: Aira [paste identity-lock reference sheet here].`
- That is: the name "Aira", then a placeholder for the reference sheet, then move on. Remove trailing text like "no physical enumeration; likeness from reference only" / "AO-X".

### 5. Restructure the video timestamps (structure only — never the words)
- The timestamps already exist; the job is only to place and structure them cleanly so VEO can parse and execute them perfectly.
- Convert any inline run into a discrete, one-beat-per-line list, for example:
```
CHOREOGRAPHY & SUBJECT ACTION (timed, fluid):
- 0.0–2.0s — she stands at deck-edge, inhales, robe settling.
- 2.0–4.0s — she takes two unhurried steps toward the water, weight rolling heel-to-toe.
- 4.0–6.0s — she pauses at the lip, head tilting toward the horizon.
```
- Uniform notation: `X.X–X.Ys` (en-dash, one decimal, lowercase `s`), an em-dash `—` before the action text, one beat per line, beats contiguous and in order.
- Beats that are already discrete only need notation made consistent.
- Do NOT reword the action text, do NOT add tags, totals, or summaries.

---

## THE ONE ABSOLUTE RULE
Never remove a single piece of real descriptive content from any concept or prompt — ever. Every change is one of: additive (the new section), formatting-only (asterisks), code-token removal, subject-line trim, or timestamp re-layout. Confirm this after every file.

---

## QUALITY BAR (the part that matters most)
Each `SUBJECT FRAMING & POSITION:` section must read as though the original author wrote it — cinematic, specific to that exact frame's scene and action, aware of the concept's theme, unique among the concept's frames, and flowing as one prose paragraph. It must NOT be a sterile template, a keyword lookup, a bullet/sub-label list, or reused phrasing copied across frames.

**Good (target) — Concept 01, Frame 5, over-the-shoulder:**
> SUBJECT FRAMING & POSITION: Aira is framed from roughly the chest upward — her back-shoulder fills the soft near-foreground while her face, rotated back toward camera in a fluid spiral, sits sharp on the upper-third line. The composition is an over-the-shoulder view: her torso faces the sea horizon with forearms resting on the pool's infinity lip, but her head and shoulders have rotated back through roughly 120 degrees to deliver the glance to the lens. Camera is close and intimate, pushing past the shoulder mass to settle on her expression — the sea-glow horizon reads as a creamy warm wash behind her turned face. She is positioned slightly left-of-centre so the horizon opens to frame-right. The body turn creates maximum torsion — back to the world, face to us, the classic inviting spiral. ORIENTATION LOCK — preserve this exact left-to-right composition; do not mirror, flip or invert the frame.

**Avoid (too generic / reused across frames):**
> SUBJECT FRAMING & POSITION: Aira reads as a complete but environment-dwarfed figure within the wide establishing composition. She anchors the dead center of the frame. Camera maintains a wide establishing distance. ORIENTATION LOCK — …

**Avoid (bullet/sub-label format that breaks the flow):**
> SUBJECT FRAMING & POSITION:
>   Body turn/orientation: torso at a gentle angle, viewed from above.
>   Body in frame: full body.
>   Camera distance: far.

Quick check per section: does it name the real scene/props of THIS frame, describe the actual body action from the choreography, clearly differ from the other frames in the concept, speak the cinematic voice, flow as one paragraph, and end with the exact ORIENTATION LOCK line?

---

## PER-FILE WORKFLOW
1. Work from the original in `concepts_dl/CONCEPTS/`.
2. Strip asterisks (verify only `*` changed; line count unchanged).
3. Remove internal codes (keep descriptions; clean leftover spaces/parentheses).
4. Normalise every `SUBJECT:` line.
5. Restructure the video timestamps (words unchanged).
6. Hand-author the `SUBJECT FRAMING & POSITION:` section for every image prompt, reading each frame and the concept theme, ensuring per-frame uniqueness and angle accuracy.
7. Verify (below).
8. Write the output file to `/projects/sandbox/Aamirs/CONCEPTS/`.
9. Commit that one file with a clear message and push to `aira-prompts-enhanced`.
10. Give the user the branch link, then move to the next file.

## VERIFICATION (run before every push)
- Number of `SUBJECT FRAMING & POSITION:` sections equals the number of image prompts.
- None of those sections fall inside a video prompt.
- No two sections are back-to-back (no accidental double insert).
- All sections are unique.
- Every section ends with the exact ORIENTATION LOCK clause.
- Zero asterisks remain; zero codes remain (`AO.`, `AO-X`, `AU.`, `AT #`, `AW #`, `AF #`, `AQ #`, `AC #`, `AP #`, `BB`, `AX #`).
- Every `SUBJECT:` line equals `SUBJECT: Aira [paste identity-lock reference sheet here].`
- All video timestamps use the uniform discrete-line `X.X–X.Ys —` form.
- No original descriptive sentence is missing (additive-only diff).

---

## FORMAT NOTES
- **Format A (markdown, most files):** `**SECTION:**` labels and `## Frame X of Y — IMAGE PROMPT` headers; thousands of asterisks; negatives written inline.
- **Format B (plain text — `aira_set4.txt`, `aira_set5.txt`):** `--- FRAME X · SIZE · ANGLE ---` headers, plain `SECTION:` labels, `NEGATIVE: STD-NEG-IMG`; no asterisks.
- Filenames contain unicode (`·`, `—`, `–`) which can show as mojibake in some terminals — always handle as UTF-8 and quote paths.

## STATUS
- DONE & pushed (exact original filenames in CONCEPTS/): `20 Beauty Ad Reels · Mind-Blowing Choreograpgy.txt` (20 concepts, 129 image prompts).
- TODO: every other file in the source folder (~1,600 image prompts total).
- `Concept 100` and `Concept 170` were processed earlier but the branch was reset — redo them under this directive.

## CONFIRMED DECISIONS
Section name is `SUBJECT FRAMING & POSITION:` · image prompts only · video prompts untouched except timestamp re-layout · internal codes removed (confirmed they don't affect generation) · subject line trimmed to `Aira [paste identity-lock reference sheet here]` · one input file → one combined output file · push each finished file to the branch · quality must match the hand-authored Concept 01 / 100 / 170 standard.

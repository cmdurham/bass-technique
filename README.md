# Bass Technique

A three-finger plucking program for bass, written block by block. Each block is a short
set of exercises with notation, tab and a printable PDF.

**Live at [cmdurham.com/bass-technique](https://cmdurham.com/bass-technique/)** (GitHub Pages,
served under the `cmdurham.com` custom domain from `cmdurham/cmdurham.github.io`).

## Structure

| Path | What it is |
|---|---|
| `index.html` | Section index: one card per block (generated) |
| `three-finger-plucking/block-N/` | Block page and its PDF (generated) |
| `style.css` | All web styling, hand-edited |
| `fonts/` | Self-hosted woff2 fonts, with licenses in `fonts/licenses/` |
| `tools/blocks/block_N.py` | **The source for a block**: text and the string/rhythm spec of every variation |
| `tools/` | Build: `scores.py` (LilyPond notation), `pdf.py` (workbook), `web.py` (pages), `build.py` (entry point) |
| `.nojekyll` | Serve files as-is; no Jekyll processing |

Everything under `three-finger-plucking/` and the root `index.html` is generated. Edit
`tools/blocks/` and `style.css`, then rebuild. Don't edit the generated HTML by hand.

## Building

```bash
pip install lilypond weasyprint     # lilypond ships its own binary; nothing else to install
python3 tools/build.py              # all blocks + index
python3 tools/build.py 2            # one block + index
```

The build prints each variation's fingering so you can check it against your intent. Notation
intermediates go to `tools/.build/` (ignored by git). LilyPond loads Barlow from `tools/fonts/`,
so no system fonts are needed.

To preview locally under the same base path as production:

```bash
mkdir -p /tmp/srv && ln -sfn "$PWD" /tmp/srv/bass-technique
cd /tmp/srv && python3 -m http.server 8080      # then open http://localhost:8080/bass-technique/
```

## Adding a block

1. Copy the closest existing block (`tools/blocks/block_1.py` for plucking-only, `block_2.py` for
   fretting work) to `block_N.py` and set `NUMBER`, `SUBTITLE`, `FOCUS` (index-card label,
   default "Plucking hand"), `CARD`, `DESCRIPTION` and `EXERCISES`.
2. Write each variation one of two ways:
   - `strings=["E", "A", ...]`: one string per note, with one fixed pitch per string from
     the block's `PITCHES` (Block 1).
   - `pattern=[("E", 8), ("E", 9), ...]` plus `position=8`: a fretting pattern that repeats.
     The fretting finger is `fret - position + 1`; write `("E", 9, 3)` to override it. The
     fretting fingers print above the staff.
   - Rhythm and layout: `dur` (LilyPond duration), `time`, `per_bar`, `bars_per_line`, `tempo`,
     optional `beat` (tempo note, default `"4"`). With `pattern=`, `length` defaults to `"auto"`.
3. Run `python3 tools/build.py N`. It prints the plucking fingers for every variation, plus the
   fretting fingers and which plucking fingers each fretting finger gets. Check those against
   your intent, then commit and push.

Exercise pages flow: when an exercise has more variations than fit on one PDF page, it
continues onto the next page with the same footer, and a variation is never split across pages.

## Plucking rules (as implemented in `tools/scores.py`)

- PIMA labels, lowercase: p thumb, i index, m middle, a ring. Fretting fingers 1–4, index to pinky.
- The cycle is **a–m–i**, in strict order, never reset.
- **Rake:** when the next note is on a lower-pitched string (toward the E string), the finger
  that played the last note plays again on the new string, and the cycle continues from it.
  Set `rake=False` on a variation to turn this off.
- The build fails unless every variation:
  - **closes the plucking cycle:** the finger that would follow the last note is the first
    finger, so the repeat always returns to `a`;
  - **closes the fretting pattern:** the length is a whole number of patterns;
  - **fills whole bars.**

  `length="auto"` picks the shortest length that passes all three. For example, a 4-note
  pattern against the 3-finger cycle closes at 12 notes, three bars of quarter notes.

## Notation conventions

Bass clef at written pitch over 4-string tab, with plucking-finger letters between the staves.
A rake is shown only by the repeated finger letter. Triplet feel is written in 12/8. The
notation is never stylized.

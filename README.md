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

1. Copy `tools/blocks/block_1.py` to `block_2.py` and set `NUMBER`, `SUBTITLE`, `CARD`, `PITCHES`,
   `DESCRIPTION` and `EXERCISES`.
2. Each variation lists the **string per note** (`strings`), the rhythm and the line breaks.
   Fingerings are never written by hand: `tools/scores.py` derives them.
3. Run `python3 tools/build.py 2`, check the printed fingerings, then commit and push.

## Plucking rules (as implemented in `tools/scores.py`)

- PIMA labels, lowercase: p thumb, i index, m middle, a ring.
- The cycle is **a–m–i**, in strict order, never reset.
- **Rake:** when the next note is on a lower-pitched string (toward the E string), the finger
  that played the last note plays again on the new string, and the cycle continues from it.
  Set `rake=False` on a variation to turn this off.
- Every variation must close: the finger that would follow its last note has to be its first
  finger, so the repeat sign always returns to `a`. The build fails if one doesn't.

## Notation conventions

Bass clef at written pitch over 4-string tab, with plucking-finger letters between the staves.
A rake is shown only by the repeated finger letter. Triplet feel is written in 12/8. The
notation is never stylized.

"""Notation + tab for a block, rendered with LilyPond to cropped SVG.

Plucking rules (fingerings are derived, never typed):
  - strict a-m-i cycle, never reset
  - rake: moving to a lower-pitched string (G->D->A->E direction), the finger
    that played the last note plays the first note on the new string, and the
    cycle continues from it

A variation is written one of two ways:
  strings=[...]          one string name per note; pitch per string from block.PITCHES
  pattern=[(s, fret)...] a fretting pattern, repeated; (s, fret, finger) overrides the
                         fretting finger, otherwise it comes from position=<fret of index finger>

Checks (the build fails if any is broken):
  - the plucking cycle closes: the finger after the last note is the first finger
  - the fretting pattern closes: the written length is a whole number of patterns
  - the line is a whole number of bars
With pattern=, length="auto" (the default) picks the shortest length that passes all three.
"""
import pathlib, subprocess
import lilypond

TOOLS = pathlib.Path(__file__).resolve().parent
FONT_DIR = TOOLS / "fonts"          # Barlow (.woff) for the notation text
CYCLE = ["a", "m", "i"]
STRING_NO = {"G": 1, "D": 2, "A": 3, "E": 4}
OPEN_MIDI = {"E": 40, "A": 45, "D": 50, "G": 55}      # written pitch (bass reads an octave up)
NAMES = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
MAX_LEN = 96


def lily_pitch(midi):
    octave = midi // 12 - 4                            # MIDI 48 = LilyPond c (C3)
    return NAMES[midi % 12] + ("'" * octave if octave > 0 else "," * -octave)


def _next(f):
    return CYCLE[(CYCLE.index(f) + 1) % 3]


def pluck(string_nos, rake=True):
    out = []
    for k, sn in enumerate(string_nos):
        if k == 0:
            out.append(CYCLE[0])
        elif rake and sn > string_nos[k - 1]:          # higher number = lower-pitched string
            out.append(out[-1])
        else:
            out.append(_next(out[-1]))
    return out


def closes(string_nos, fingers, rake=True):
    nxt = fingers[-1] if rake and string_nos[0] > string_nos[-1] else _next(fingers[-1])
    return nxt == fingers[0]


def expand(block, v):
    """Variation spec -> list of notes {pitch, string_no, lh}."""
    if "strings" in v:
        return [dict(pitch=block.PITCHES[s][0], string_no=block.PITCHES[s][1], lh=None) for s in v["strings"]]
    pos = v.get("position")
    cell = []
    for t in v["pattern"]:
        s, fret = t[0], t[1]
        lh = t[2] if len(t) > 2 else (fret - pos + 1 if pos is not None and fret > 0 else None)
        if lh is not None and not 1 <= lh <= 4:
            raise ValueError(f"fretting finger {lh} out of range for {t} at position {pos}")
        cell.append(dict(pitch=lily_pitch(OPEN_MIDI[s] + fret), string_no=STRING_NO[s], lh=lh))
    rake = v.get("rake", True)
    length = v.get("length", "auto")
    if length == "auto":
        for L in range(len(cell), MAX_LEN + 1, len(cell)):
            sn = [cell[k % len(cell)]["string_no"] for k in range(L)]
            if L % v["per_bar"] == 0 and closes(sn, pluck(sn, rake), rake):
                length = L
                break
        else:
            raise ValueError(f"no closing length up to {MAX_LEN} notes for {v.get('title')}")
    if length % len(cell):
        raise ValueError(f"{v.get('title')}: length {length} is not a whole number of {len(cell)}-note patterns")
    return [cell[k % len(cell)] for k in range(length)]


def lily_source(v, notes, fingers):
    out = []
    per_bar, n = v["per_bar"], len(notes)
    for k, note in enumerate(notes):
        tok = f"{note['pitch']}{v['dur']}\\{note['string_no']}"
        if note["lh"]:
            tok += f"^{note['lh']}"
        out.append(tok)
        if (k + 1) % per_bar == 0 and k != n - 1:
            out.append("|")
            if ((k + 1) // per_bar) % v["bars_per_line"] == 0:
                out.append("\\break")
    beat = v.get("beat", "4")
    tempo = f'\\tempo \\markup {{ \\fontsize #-1 \\note {{{beat}}} #1 \\fontsize #-1 "= {v["tempo"]}" }}'
    return rf'''\version "2.25.12"
#(ly:font-config-add-directory "{FONT_DIR}")
#(set-global-staff-size 19)
\paper {{
  paper-width = 190\mm  line-width = 186\mm  indent = 0  ragged-right = ##f
  left-margin = 2\mm  top-margin = 0\mm  bottom-margin = 0\mm
  print-page-number = ##f  tagline = ##f
  system-system-spacing = #'((basic-distance . 22) (minimum-distance . 20) (padding . 4) (stretchability . 0))
  property-defaults.fonts.sans = "Barlow"
  property-defaults.fonts.serif = "Barlow"
}}
\header {{ tagline = ##f }}
music = {{ \bar ".|:" {" ".join(out)} \bar ":|." }}
\score {{
  \new StaffGroup \with {{ systemStartDelimiter = #'SystemStartBrace }} <<
    \new Staff = "notes" \with {{ \omit StringNumber \numericTimeSignature \override Fingering.add-stem-support = ##t }}
      {{ \clef bass \time {v["time"]} {tempo} \new Voice = "v" \music }}
    \new Lyrics \with {{ \override LyricText.font-family = #'sans
                        \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #1.2 }}
      \lyricsto "v" {{ {" ".join(fingers)} }}
    \new TabStaff \with {{ stringTunings = \stringTuning <e, a, d g> \omit Fingering }}
      {{ \clef moderntab \time {v["time"]} \music }}
  >>
  \layout {{
    \context {{ \Score \override BarNumber.font-size = #-2 \override MetronomeMark.font-family = #'sans }}
    \context {{ \TabStaff \omit TimeSignature \override TabNoteHead.font-size = #-0.5 }}
  }}
}}
'''


def render(block, out_dir):
    """Render every variation. Returns {name: (svg_path, pluck_fingers, fretting_fingers)}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    for e in block.EXERCISES:
        for k, v in enumerate(e["vars"], 1):
            name = f"ex{e['n']}_v{k}"
            notes = expand(block, v)
            rake = v.get("rake", True)
            sn = [x["string_no"] for x in notes]
            fingers = pluck(sn, rake)
            if not closes(sn, fingers, rake):
                raise ValueError(f"{name}: plucking cycle does not close: {' '.join(fingers)}")
            if len(notes) % v["per_bar"]:
                raise ValueError(f"{name}: {len(notes)} notes is not a whole number of {v['per_bar']}-note bars")
            ly = out_dir / f"{name}.ly"
            ly.write_text(lily_source(v, notes, fingers))
            run = subprocess.run([str(lilypond.executable()), "-dbackend=svg", "-dcrop", "-dno-point-and-click",
                                  "-o", str(out_dir / name), str(ly)], capture_output=True, text=True)
            if run.returncode != 0:
                raise RuntimeError(f"LilyPond failed on {name}:\n{run.stderr[-2000:]}")
            result[name] = (out_dir / f"{name}.cropped.svg", fingers, [x["lh"] for x in notes])
    return result

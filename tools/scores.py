"""Notation + tab for a block, rendered with LilyPond to cropped SVG.

Plucking rules (fingerings are derived, never typed):
  - strict a-m-i cycle, never reset and never reversed; it starts on a unless a
    variation sets start="m" or start="i" (the lead finger), and the repeat
    returns to that finger
  - rake: moving to a lower-pitched string (G->D->A->E direction), the finger
    that played the last note plays the first note on the new string, and the
    cycle continues from it

A variation is written one of two ways:
  strings=[...]          one string name per note; pitch per string from block.PITCHES
  pattern=[(s, fret)...] a fretting pattern, repeated; (s, fret, finger) overrides the
                         fretting finger, otherwise it comes from position=<fret of index finger>.
                         ("r", "4") is a rest (LilyPond duration); the plucking cycle carries
                         on across it, and it counts toward the bar but takes no finger

Checks (the build fails if any is broken):
  - the plucking cycle closes: the finger after the last note is the first finger
  - the fretting pattern closes: the written length is a whole number of patterns
  - the line is a whole number of bars (rests included)
With pattern=, length="auto" (the default) picks the shortest length that passes all three.
open_end=True skips the cycle check: the line is one pass of the pattern, ends on a final
barline instead of a repeat, and the cycle carries on if it is played again.
"""
import pathlib, subprocess
import lilypond

TOOLS = pathlib.Path(__file__).resolve().parent
FONT_DIR = TOOLS / "fonts"          # Barlow (.woff) for the notation text
CYCLE = ["a", "m", "i"]
STRING_NO = {"G": 1, "D": 2, "A": 3, "E": 4}
OPEN_MIDI = {"E": 40, "A": 45, "D": 50, "G": 55}      # written pitch (bass reads an octave up)
NAMES = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
MAX_LEN = 480


def lily_pitch(midi):
    octave = midi // 12 - 4                            # MIDI 48 = LilyPond c (C3)
    return NAMES[midi % 12] + ("'" * octave if octave > 0 else "," * -octave)


def _next(f):
    return CYCLE[(CYCLE.index(f) + 1) % 3]


def pluck(string_nos, rake=True, start="a"):
    out = []
    for k, sn in enumerate(string_nos):
        if k == 0:
            out.append(start)
        elif rake and sn > string_nos[k - 1]:          # higher number = lower-pitched string
            out.append(out[-1])
        else:
            out.append(_next(out[-1]))
    return out


def closes(string_nos, fingers, rake=True):
    nxt = fingers[-1] if rake and string_nos[0] > string_nos[-1] else _next(fingers[-1])
    return nxt == fingers[0]


def _units(note_dur, rest_dur):
    """Length of a rest in units of the variation's note duration (plain LilyPond durations only)."""
    u, r = divmod(int(note_dur), int(rest_dur))
    if r or u < 1:
        raise ValueError(f"rest r{rest_dur} is not a whole number of {note_dur} notes")
    return u


def _played(seq):
    """String numbers of the notes in seq, rests left out."""
    return [x["string_no"] for x in seq if "rest" not in x]


def expand(block, v):
    """Variation spec -> list of notes {pitch, string_no, lh}; rests are {rest, units}."""
    if "strings" in v:
        return [dict(pitch=block.PITCHES[s][0], string_no=block.PITCHES[s][1], lh=None) for s in v["strings"]]
    pos = v.get("position")
    cell = []
    for t in v["pattern"]:
        if t[0] == "r":
            cell.append(dict(rest=t[1], units=_units(v["dur"], t[1])))
            continue
        s, fret = t[0], t[1]
        lh = t[2] if len(t) > 2 else (fret - pos + 1 if pos is not None and fret > 0 else None)
        if lh is not None and not 1 <= lh <= 4:
            raise ValueError(f"fretting finger {lh} out of range for {t} at position {pos}")
        cell.append(dict(pitch=lily_pitch(OPEN_MIDI[s] + fret), string_no=STRING_NO[s], lh=lh))
    rake = v.get("rake", True)
    start = v.get("start", CYCLE[0])
    length = v.get("length", "auto")
    if length == "auto":
        for L in range(len(cell), MAX_LEN + 1, len(cell)):
            seq = [cell[k % len(cell)] for k in range(L)]
            sn = _played(seq)
            if sum(x.get("units", 1) for x in seq) % v["per_bar"] == 0 and (
                    v.get("open_end") or closes(sn, pluck(sn, rake, start), rake)):
                length = L
                break
        else:
            raise ValueError(f"no closing length up to {MAX_LEN} notes for {v.get('title')}")
    if length % len(cell):
        raise ValueError(f"{v.get('title')}: length {length} is not a whole number of {len(cell)}-note patterns")
    return [cell[k % len(cell)] for k in range(length)]


def lily_source(v, notes, fingers, first=True, last=True, bar_no=1):
    """One LilyPond score. A part of a split variation (bars_per_part) sets first/last/bar_no:
    the repeat opens on the first part and closes on the last; later parts continue the bar
    numbers and drop the tempo and time signature."""
    out = []
    per_bar, n, units = v["per_bar"], len(notes), 0
    for k, note in enumerate(notes):
        if "rest" in note:
            tok = f"r{note['rest']}"
        else:
            tok = f"{note['pitch']}{v['dur']}\\{note['string_no']}"
            if note["lh"]:
                tok += f"^{note['lh']}"
        out.append(tok)
        units += note.get("units", 1)
        if units % per_bar == 0 and k != n - 1:
            out.append("|")
            if (units // per_bar) % v["bars_per_line"] == 0:
                out.append("\\break")
    beat = v.get("beat", "4")
    tempo = f'\\tempo \\markup {{ \\fontsize #-1 \\note {{{beat}}} #1 \\fontsize #-1 "= {v["tempo"]}" }}'
    if not first:
        tempo = f"\\set Score.currentBarNumber = #{bar_no} \\bar \"\""
    open_end = v.get("open_end")
    open_bar = '\\bar ".|:" ' if first and not open_end else ""
    close_bar = (' \\bar "|."' if open_end else ' \\bar ":|."') if last else ' \\bar "|"'
    staff_extra = "" if first else " \\omit TimeSignature"
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
music = {{ {open_bar}{" ".join(out)}{close_bar} }}
\score {{
  \new StaffGroup \with {{ systemStartDelimiter = #'SystemStartBrace }} <<
    \new Staff = "notes" \with {{ \omit StringNumber \numericTimeSignature \override Fingering.add-stem-support = ##t{staff_extra} }}
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


def _split(v, notes, fingers):
    """Cut a variation into parts of bars_per_part bars (default: one part).
    Returns [(notes, fingers, first_bar_number)]."""
    size = v.get("bars_per_part")
    if not size:
        return [(notes, fingers, 1)]
    parts, cur, cur_f, fi, units, start = [], [], [], iter(fingers), 0, 1
    for note in notes:
        cur.append(note)
        if "rest" not in note:
            cur_f.append(next(fi))
        units += note.get("units", 1)
        if units % (v["per_bar"] * size) == 0:
            parts.append((cur, cur_f, start))
            cur, cur_f, start = [], [], units // v["per_bar"] + 1
    if cur:
        parts.append((cur, cur_f, start))
    return parts


def render(block, out_dir):
    """Render every variation. Returns {name: ([svg_path, ...], pluck_fingers, fretting_fingers)};
    a variation with bars_per_part has one SVG per part, otherwise one."""
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    for e in block.EXERCISES:
        for k, v in enumerate(e["vars"], 1):
            name = f"ex{e['n']}_v{k}"
            notes = expand(block, v)
            rake = v.get("rake", True)
            sn = _played(notes)
            fingers = pluck(sn, rake, v.get("start", CYCLE[0]))
            if not v.get("open_end") and not closes(sn, fingers, rake):
                raise ValueError(f"{name}: plucking cycle does not close: {' '.join(fingers)}")
            units = sum(x.get("units", 1) for x in notes)
            if units % v["per_bar"]:
                raise ValueError(f"{name}: {units} beats of {v['dur']} is not a whole number of {v['per_bar']}-note bars")
            parts = _split(v, notes, fingers)
            svgs = []
            for j, (part, pf, bar_no) in enumerate(parts):
                stem = name if len(parts) == 1 else f"{name}_p{j + 1}"
                ly = out_dir / f"{stem}.ly"
                ly.write_text(lily_source(v, part, pf, first=j == 0, last=j == len(parts) - 1, bar_no=bar_no))
                run = subprocess.run([str(lilypond.executable()), "-dbackend=svg", "-dcrop", "-dno-point-and-click",
                                      "-o", str(out_dir / stem), str(ly)], capture_output=True, text=True)
                if run.returncode != 0:
                    raise RuntimeError(f"LilyPond failed on {stem}:\n{run.stderr[-2000:]}")
                svgs.append(out_dir / f"{stem}.cropped.svg")
            result[name] = (svgs, fingers, [x["lh"] for x in notes if "rest" not in x])
    return result

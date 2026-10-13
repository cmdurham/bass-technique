"""Notation + tab for a block, rendered with LilyPond to cropped SVG.

Plucking rules (fingerings are derived, never typed):
  - strict a-m-i cycle, never reset
  - rake: moving to a lower-pitched string (G->D->A->E direction), the finger
    that played the last note plays the first note on the new string, and the
    cycle continues from it
Each variation is checked so its repeat closes: the finger that would follow
the last note must equal the first finger.
"""
import pathlib, subprocess
import lilypond

TOOLS = pathlib.Path(__file__).resolve().parent
FONT_DIR = TOOLS / "fonts"          # Barlow (.woff) for the notation text
CYCLE = ["a", "m", "i"]


def fingers_for(strings, pitches, rake=True):
    out = []
    for k, s in enumerate(strings):
        if k == 0:
            out.append(CYCLE[0])
            continue
        prev_s, cur = strings[k - 1], pitches[s][1]
        if rake and cur > pitches[prev_s][1]:          # higher string number = lower-pitched string
            out.append(out[-1])
        else:
            out.append(CYCLE[(CYCLE.index(out[-1]) + 1) % 3])
    # the repeat must close
    nxt = (out[-1] if rake and pitches[strings[0]][1] > pitches[strings[-1]][1]
           else CYCLE[(CYCLE.index(out[-1]) + 1) % 3])
    assert nxt == out[0], f"repeat does not close: {strings} -> {out}"
    return out


def lily_source(v, pitches, fingers):
    notes = []
    per_bar, n = v["per_bar"], len(v["strings"])
    for k, s in enumerate(v["strings"]):
        p, string_no = pitches[s]
        notes.append(f"{p}{v['dur']}\\{string_no}")
        if (k + 1) % per_bar == 0 and k != n - 1:
            notes.append("|")
            if ((k + 1) // per_bar) % v["bars_per_line"] == 0:
                notes.append("\\break")
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
music = {{ \bar ".|:" {" ".join(notes)} \bar ":|." }}
\score {{
  \new StaffGroup \with {{ systemStartDelimiter = #'SystemStartBrace }} <<
    \new Staff = "notes" \with {{ \omit StringNumber \numericTimeSignature }}
      {{ \clef bass \time {v["time"]} {tempo} \new Voice = "v" \music }}
    \new Lyrics \with {{ \override LyricText.font-family = #'sans
                        \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #1.2 }}
      \lyricsto "v" {{ {" ".join(fingers)} }}
    \new TabStaff \with {{ stringTunings = \stringTuning <e, a, d g> }}
      {{ \clef moderntab \time {v["time"]} \music }}
  >>
  \layout {{
    \context {{ \Score \override BarNumber.font-size = #-2 \override MetronomeMark.font-family = #'sans }}
    \context {{ \TabStaff \omit TimeSignature \override TabNoteHead.font-size = #-0.5 }}
  }}
}}
'''


def render(block, out_dir):
    """Render every variation of a block module. Returns {svg_name: (svg_path, fingers)}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    for e in block.EXERCISES:
        for k, v in enumerate(e["vars"], 1):
            name = f"ex{e['n']}_v{k}"
            fingers = fingers_for(v["strings"], block.PITCHES, v.get("rake", True))
            ly = out_dir / f"{name}.ly"
            ly.write_text(lily_source(v, block.PITCHES, fingers))
            run = subprocess.run([str(lilypond.executable()), "-dbackend=svg", "-dcrop", "-dno-point-and-click",
                                  "-o", str(out_dir / name), str(ly)], capture_output=True, text=True)
            if run.returncode != 0:
                raise RuntimeError(f"LilyPond failed on {name}:\n{run.stderr[-2000:]}")
            result[name] = (out_dir / f"{name}.cropped.svg", fingers)
    return result

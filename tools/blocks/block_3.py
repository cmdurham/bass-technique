"""Block 3 — descending patterns and the rake.

The strict a-m-i cycle moving down the strings, where every move to a lower string rakes:
  1-3. string pairs in 7th position, one fixed note per string, in key (D/B, A/F, E/C),
       two, three and four notes per string
  4.   descending scales: two-note-per-string pentatonics and one-octave scales
  5.   descending two-stroke arpeggios (Block 2 Ex 4 in reverse)
Two notes per string closes after one pass, so the lead finger never changes on its own;
those variations set start= to lead from m and i.
Lengths are found automatically: the shortest whole-bar line where both the
fretting pattern and the plucking cycle close.
"""

NUMBER = 3
DRAFT = True
SUBTITLE = "Descending patterns and the rake"
FOCUS = "Both hands"
CARD = ("The a&ndash;m&ndash;i cycle moving down the strings: string pairs, descending scales and "
        "arpeggios, with a rake at every move to a lower string.")
PITCHES = {}

DESCRIPTION = [
    "Block 3 turns the cycle downhill. Every move to a lower string is a <b>rake</b>: the finger that played the "
    "last note on the higher string also plays the first note on the lower one, and the cycle continues from it. "
    "Moving down on the same string is not a rake, and neither is the jump from the bottom of a run back to the "
    "top: keep the cycle going.",
    "Exercises 1 to 3 hold one note on each string of a pair, in 7th position and in C: D and B on the G and D "
    "strings, A and F on the D and A strings, E and C on the A and E strings. The number of notes per string "
    "decides which finger leads off on each string and which finger rakes.",
    "Exercise 4 descends through scales: two-note-per-string pentatonics, then one-octave scales in the shapes "
    "from Block 2, in two positions for different string tension. Exercise 5 runs Block 2's two-stroke "
    "arpeggios from the top down.",
]

_PAIR = dict(dur="4", time="4/4", per_bar=4, bars_per_line=2, tempo="60–100")
_PAIR3 = dict(dur="4", time="3/4", per_bar=3, bars_per_line=2, tempo="60–100")
_RUN = dict(dur="4", time="4/4", per_bar=4, bars_per_line=2, tempo="60–100")
_ARP = dict(dur="8", time="4/4", per_bar=8, bars_per_line=2, tempo="60–100", beat="8")

# String pairs in 7th position, one fixed note per string: (high, low, name).
PAIRS = [
    (("G", 7), ("D", 9), "D and B (G and D strings)"),
    (("D", 7), ("A", 8), "A and F (D and A strings)"),
    (("A", 7), ("E", 8), "E and C (A and E strings)"),
]
_LEAD = {"a": "lead a", "m": "lead m", "i": "lead i"}


def _pair(hi, lo, n):
    return [hi] * n + [lo] * n


def _twice(*notes):
    """Each note plucked twice, then a quarter rest."""
    return [n for n in notes for _ in (0, 1)] + [("r", "4")]


EXERCISES = [
    dict(n=1, short="Two notes per string",
         intro="<b>Exercise 1</b> plays two notes on each string of a pair, high string first. Four notes with one "
               "rake bring the cycle back to the same finger every pass, so the lead finger never changes on its "
               "own: each pair is written three times, leading off with <b>a</b>, <b>m</b> and <b>i</b>. The "
               "repeat returns to the finger you led with. The last three variations start on the low string, so "
               "the rake comes on the return.",
         vars=[dict(title=f"{name}, {_LEAD[s]}", pattern=_pair(hi, lo, 2), position=7, start=s, length=8, **_PAIR)
               for hi, lo, name in PAIRS for s in "ami"]
              + [dict(title=f"{PAIRS[0][2].split(' (')[0]}, low string first, {_LEAD[s]}",
                      pattern=[PAIRS[0][1]] * 2 + [PAIRS[0][0]] * 2, position=7, start=s, length=8, **_PAIR)
                 for s in "ami"]),
    dict(n=2, short="Three notes per string",
         intro="<b>Exercise 2</b> plays three notes on each string. Six notes with one rake move the cycle on, so "
               "each return to the high string leads off with a new finger: <b>a</b>, <b>i</b>, <b>m</b>. Three "
               "passes, one per line, and every finger rakes once.",
         vars=[dict(title=name, pattern=_pair(hi, lo, 3), position=7, **_PAIR3) for hi, lo, name in PAIRS]),
    dict(n=3, short="Four notes per string",
         intro="<b>Exercise 3</b> plays four notes on each string. Each return to the high string leads off with a "
               "new finger: <b>a</b>, <b>m</b>, <b>i</b>. Three passes, one per line.",
         vars=[dict(title=name, pattern=_pair(hi, lo, 4), position=7, **_PAIR) for hi, lo, name in PAIRS]),
    dict(n=4, short="Descending scales",
         intro="<b>Exercise 4</b> descends through scales. The pentatonics play two notes per string and rotate: "
               "three passes, one per line, leading off with <b>a</b>, <b>m</b>, <b>i</b>. The one-octave scales "
               "use the shapes from Block 2, top down. Eight notes with two rakes bring the cycle back to "
               "<b>a</b> every pass, so they are two-bar repeats; within a pass each string leads off with a "
               "different finger. C major runs on the D, A and E strings from the 10th fret, then on the G, D and "
               "A strings from the 5th.",
         vars=[
             dict(title="C major pentatonic (10th fret, D string)",
                  pattern=[("D", 10), ("D", 7), ("A", 10), ("A", 7), ("E", 10), ("E", 8), ("r", "2")],
                  position=7, **_RUN),
             dict(title="A minor pentatonic (7th fret, D string)",
                  pattern=[("D", 7, 3), ("D", 5), ("A", 7, 3), ("A", 5), ("E", 8), ("E", 5), ("r", "2")],
                  position=5, **_RUN),
             dict(title="C major (10th fret, D string)",
                  pattern=[("D", 10), ("D", 9), ("D", 7), ("A", 10), ("A", 8), ("A", 7), ("E", 10), ("E", 8)],
                  position=7, **_RUN),
             dict(title="C major (5th fret, G string)",
                  pattern=[("G", 5), ("G", 4), ("G", 2), ("D", 5), ("D", 3), ("D", 2), ("A", 5), ("A", 3)],
                  position=2, **_RUN),
             dict(title="A minor (7th fret, D string)",
                  pattern=[("D", 7, 3), ("D", 5), ("A", 8), ("A", 7), ("A", 5), ("E", 8), ("E", 7), ("E", 5)],
                  position=5, **_RUN),
         ]),
    dict(n=5, short="Descending arpeggios",
         intro="<b>Exercise 5</b> runs Block 2's two-octave arpeggios from the high root down, plucking each note "
               "twice. At each string change, the finger that plays the second stroke of the last note on the "
               "higher string rakes to the first stroke on the lower one. Use the quarter rest to get back to the top. Three passes, one per "
               "line, leading off with <b>a</b>, <b>i</b>, <b>m</b>. The tempo is marked in eighth notes.",
         vars=[
             dict(title="C major (C, G, E)",
                  pattern=_twice(("G", 17, 4), ("G", 12, 4), ("G", 9, 1), ("D", 10, 2), ("A", 10), ("A", 7),
                                 ("E", 8)),
                  position=7, **_ARP),
             dict(title="A minor (A, E, C)",
                  pattern=_twice(("G", 14, 3), ("G", 9, 3), ("D", 10, 4), ("D", 7, 1), ("A", 7), ("E", 8),
                                 ("E", 5)),
                  position=5, **_ARP),
         ]),
]

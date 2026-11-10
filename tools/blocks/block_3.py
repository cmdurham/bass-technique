"""Block 3 — string pairs and the rake.

The strict a-m-i cycle across string pairs, high string first, so every move to the
lower string of a pair is a rake:
  1. plucking-only primer: 16th notes on the C at the 10th fret of the D string
  2. three notes per string, quarter notes in 3/4
  3. four notes per string, eighth notes
  4. two notes per string, eighth notes
Exercises 2-4 play four bars on each pair, climbing A/E, D/A, G/D and back to D/A: 16 bars.
One note per string, in key, 7th position:
  A/E: E (A7) and C (E8);  D/A: A (D7) and F (A8);  G/D: D (G7) and B (D9).
Exercises 2 and 3 don't realign the cycle in 16 bars; they are written as one pass
(open_end) and the text says to carry the cycle on. Exercise 4 closes at 16 bars.
The focus is the plucking-hand rake; fretting-hand coordination returns in Block 4.
"""

NUMBER = 3
SUBTITLE = "String pairs and the rake"
FOCUS = "Plucking hand"
CARD = ("The a&ndash;m&ndash;i cycle across string pairs, high string first: three, four and two notes per "
        "string, climbing from the A and E strings to the G and D and back.")
PITCHES = {}

DESCRIPTION = [
    "Block 3 takes the strict <b>a&ndash;m&ndash;i</b> cycle across string pairs. Each pair is played high string "
    "first, so every move to the lower string is a <b>rake</b>: the finger that played the last note on the "
    "higher string also plays the first note on the lower one, and the cycle continues from it. The move back up "
    "to the higher string is not a rake: keep the cycle going.",
    "Exercise 1 primes the plucking hand on the D string, a different gauge and tension from the earlier blocks. "
    "Exercises 2 to 4 play four bars on each pair: the A and E strings, the D and A strings, the G and D strings, "
    "then back to the D and A strings, sixteen bars in all. The fretting hand holds one note on each string, in "
    "7th position and in C: E and C, A and F, D and B.",
    "The focus this block is the rake in the plucking hand, not fretting-hand coordination; that comes in Block 4. "
    "Start slowly, and use the end of each sixteen bars as the point to raise the tempo. Two notes per string is "
    "the hardest to keep at speed.",
]

_ONE = dict(dur="16", time="4/4", per_bar=16, bars_per_line=1, tempo="60–100")
_THREE = dict(dur="4", time="3/4", per_bar=3, bars_per_line=4, tempo="60–100")
_EIGHTHS = dict(dur="8", time="4/4", per_bar=8, bars_per_line=4, tempo="60–100", beat="8")

# String pairs, high string first, climbing and back: one fixed note per string.
_PAIRS = [
    (("A", 7), ("E", 8)),     # E and C
    (("D", 7), ("A", 8)),     # A and F
    (("G", 7), ("D", 9)),     # D and B
    (("D", 7), ("A", 8)),     # back to A and F
]


def _climb(per_string, groups_per_pair):
    """Each pair: per_string notes on the high string, then on the low string, groups_per_pair times."""
    out = []
    for hi, lo in _PAIRS:
        out += ([hi] * per_string + [lo] * per_string) * groups_per_pair
    return out


EXERCISES = [
    dict(n=1, short="Right-hand primer",
         intro="<b>Exercise 1</b> is plucking only: the C at the 10th fret of the D string, in 16th notes. The D "
               "string is a different gauge and tension from the earlier blocks. Keep the rhythm even, then raise "
               "the tempo. Sixteen notes don't divide by three, so each bar starts on a different finger; the "
               "cycle realigns after three bars, and the repeat returns you to <b>a</b>. The tempo is marked in "
               "quarter notes.",
         vars=[
             dict(title="C on the D string", pattern=[("D", 10)], **_ONE),
         ]),
    dict(n=2, short="Three notes per string",
         intro="<b>Exercise 2</b> plays three notes on each string, one bar per string, high string first. Four "
               "bars on each pair, climbing from the A and E strings to the G and D strings and back to the D and "
               "A strings. The sixteen bars end with the cycle mid-way, so there is no repeat: to go round again, "
               "carry the cycle straight on without resetting to <b>a</b>, or stop and take the next pass at a "
               "faster tempo.",
         vars=[
             dict(title="E/C, A/F, D/B, A/F", pattern=_climb(3, 2), position=7, open_end=True, **_THREE),
         ]),
    dict(n=3, short="Four notes per string",
         intro="<b>Exercise 3</b> plays four notes on each string in eighth notes, so each bar is one trip across "
               "the pair. Four bars on each pair, climbing and back as in Exercise 2. As there, the sixteen bars "
               "end mid-cycle: carry the cycle straight on, or stop and raise the tempo. The tempo is marked in "
               "eighth notes.",
         vars=[
             dict(title="E/C, A/F, D/B, A/F", pattern=_climb(4, 4), position=7, open_end=True, **_EIGHTHS),
         ]),
    dict(n=4, short="Two notes per string",
         intro="<b>Exercise 4</b> plays two notes on each string in eighth notes, the same four bars on each pair. "
               "This is the hardest of the three to keep at speed. Here the cycle does realign after sixteen bars, "
               "so the repeat returns you to <b>a</b>. The tempo is marked in eighth notes.",
         vars=[
             dict(title="E/C, A/F, D/B, A/F", pattern=_climb(2, 8), position=7, **_EIGHTHS),
         ]),
]

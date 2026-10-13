"""Block 2 — fretting and plucking finger independence.

A four-note fretting shape (up two notes and back) against the three-finger
plucking cycle. Fretting fingers come from 8th-fret position, one finger per fret.
Lengths are found automatically: the shortest whole-bar line where both the
fretting pattern and the plucking cycle close (12 notes = 3 bars of quarters).
"""

NUMBER = 2
SUBTITLE = "Fretting and plucking finger independence"
FOCUS = "Both hands"
CARD = "A four-note fretting shape against the three-finger cycle, through every three-finger set of the fretting hand."
PITCHES = {}

DESCRIPTION = [
    "Block 2 adds the fretting hand. The plucking hand keeps the strict <b>a&ndash;m&ndash;i</b> cycle from "
    "Block 1, and the fretting hand plays a four-note shape that goes up and back. Four against three means the "
    "hands line up only every twelve notes, so each fretted note is played with every plucking finger before the "
    "pattern repeats.",
    "The fretting hand stays in 8th-fret position, one finger per fret: index on the 8th fret, pinky on the 11th. "
    "Fretting fingers are the numbers above the staff; plucking fingers stay between the staves.",
    "The fretting shape turns around at its top and bottom notes. The plucking cycle never does, so at those turns "
    "the hands move in opposite directions. The usual error there is a reflexive <b>m</b> where the cycle calls "
    "for <b>i</b> or <b>a</b>. Keep the cycle strict and let the hands disagree.",
]

_Q = dict(dur="4", time="4/4", per_bar=4, bars_per_line=3, tempo="60–100", position=8)


def _shape(*frets):
    """Up and back on the E string: (8, 9, 10) -> 8 9 10 9."""
    lo, mid, hi = frets
    return [("E", lo), ("E", mid), ("E", hi), ("E", mid)]


EXERCISES = [
    dict(n=1, short="Four against three",
         intro="<b>Exercise 1</b> runs a four-note fretting shape on the E string against the a&ndash;m&ndash;i "
               "cycle: C, C#, D, C#, and around again. Twelve notes, three bars of quarter notes, bring both hands "
               "back to their starting fingers, and the repeat returns you to C on <b>a</b>. Each variation moves "
               "the shape to another set of three fretting fingers. Variation #4 leaves out the index finger, so "
               "the ring and pinky carry it. Drop to half notes or a slower tempo until the cycle holds through "
               "every turn.",
         vars=[
             dict(title="Fingers 1-2-3 (C, C#, D)", pattern=_shape(8, 9, 10), **_Q),
             dict(title="Fingers 1-3-4 (C, D, D#)", pattern=_shape(8, 10, 11), **_Q),
             dict(title="Fingers 1-2-4 (C, C#, D#)", pattern=_shape(8, 9, 11), **_Q),
             dict(title="Fingers 2-3-4 (C#, D, D#)", pattern=_shape(9, 10, 11), **_Q),
         ]),
]

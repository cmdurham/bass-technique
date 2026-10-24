"""Block 2 — fretting and plucking finger independence.

The strict a-m-i cycle against a fretting hand that changes direction:
  1. plucking-only primer on the A string (same C as Block 1, different string)
  2. four-note up-and-back shapes on the E string, 8th-fret position, through every
     three-finger set of the fretting hand
  3. ascending one-octave scales, looped three times so each pass starts on a new finger
  4. ascending two-octave arpeggios, each note plucked twice, looped the same way
Nothing here descends, so there are no rakes with fretting yet; that is Block 3.
Lengths are found automatically: the shortest whole-bar line where both the
fretting pattern and the plucking cycle close.
"""

NUMBER = 2
SUBTITLE = "Fretting and plucking finger independence"
FOCUS = "Both hands"
CARD = ("The strict a&ndash;m&ndash;i cycle against a fretting hand that changes direction: up-and-back shapes, "
        "ascending scales and two-stroke arpeggios.")
PITCHES = {}

DESCRIPTION = [
    "Block 2 adds the fretting hand. The plucking hand keeps the strict <b>a&ndash;m&ndash;i</b> cycle from "
    "Block 1 while the fretting fingers move in alternating or opposite directions. The plucking direction never "
    "changes, whatever the fretting hand does.",
    "Fretting fingers are the numbers above the staff; plucking fingers stay between the staves. Exercise 2 sits "
    "in 8th-fret position, one finger per fret. The scales and arpeggios set their own positions, and the "
    "arpeggios shift; the fingering numbers show where.",
    "The traps: where the fretting hand turns around, a reflexive <b>m</b> where the cycle calls for <b>i</b> or "
    "<b>a</b>; and in the scales and arpeggios, resetting to <b>a</b> at the start of each pass. The runs don't "
    "divide by three, so every pass starts on a different finger. Keep the cycle strict and let the hands disagree.",
    "Everything in this block stays on one string or ascends. Descending work, with rakes, comes in Block 3.",
]

_Q = dict(dur="4", time="4/4", per_bar=4, bars_per_line=3, tempo="60–100")
_RUN = dict(dur="4", time="4/4", per_bar=4, bars_per_line=2, tempo="60–100", rake=False)
_ARP = dict(dur="8", time="4/4", per_bar=8, bars_per_line=2, tempo="60–100", beat="8", rake=False)


def _shape(*frets):
    """Up and back on the E string: (8, 9, 10) -> 8 9 10 9."""
    lo, mid, hi = frets
    return [("E", lo), ("E", mid), ("E", hi), ("E", mid)]


def _twice(*notes):
    """Each note plucked twice, then a quarter rest."""
    return [n for n in notes for _ in (0, 1)] + [("r", "4")]


EXERCISES = [
    dict(n=1, short="Right-hand primer",
         intro="<b>Exercise 1</b> is plucking only: the C on the A string, 3rd fret. It is the same pitch as "
               "Block 1's C on the E string, on a different string gauge and tension, so the plucking hand gets "
               "used to the new feel before the fretting hand joins in. Twelve notes, three bars, and the repeat "
               "returns you to <b>a</b>.",
         vars=[
             dict(title="C on the A string", pattern=[("A", 3)], **_Q),
         ]),
    dict(n=2, short="Alternating directionality",
         intro="<b>Exercise 2</b> runs a four-note fretting shape on the E string against the a&ndash;m&ndash;i "
               "cycle: up two notes and back. The shape turns around at its top and bottom notes; the plucking "
               "cycle never does. Four against three means each fretted note gets every plucking finger in twelve "
               "notes, three bars, and the repeat returns you to C on <b>a</b>. The variations climb the fretting "
               "hand: 1-2-3, 1-2-4, 1-3-4, then 2-3-4, which leaves out the index so the ring and pinky carry it. "
               "Drop to half notes or a slower tempo until the cycle holds through every turn.",
         vars=[
             dict(title="Fingers 1-2-3 (C, C#, D)", pattern=_shape(8, 9, 10), position=8, **_Q),
             dict(title="Fingers 1-2-4 (C, C#, D#)", pattern=_shape(8, 9, 11), position=8, **_Q),
             dict(title="Fingers 1-3-4 (C, D, D#)", pattern=_shape(8, 10, 11), position=8, **_Q),
             dict(title="Fingers 2-3-4 (C#, D, D#)", pattern=_shape(9, 10, 11), position=8, **_Q),
         ]),
    dict(n=3, short="Ascending scales",
         intro="<b>Exercise 3</b> takes the cycle into a one-octave scale, ascending only. At each string change "
               "the fretting hand resets to start the new string while the plucking cycle carries straight "
               "through, and the strings take different numbers of notes: two, three and three in the major; "
               "three, three and two in the minor. Play three passes without stopping, one per line. Eight notes "
               "don't divide by three, so the passes start on <b>a</b>, <b>i</b> and <b>m</b>. The jump from the "
               "top back to the root is not a rake: keep the cycle going.",
         vars=[
             dict(title="C major (8th fret, E string)",
                  pattern=[("E", 8), ("E", 10), ("A", 7), ("A", 8), ("A", 10), ("D", 7), ("D", 9), ("D", 10)],
                  position=7, **_RUN),
             dict(title="A minor (5th fret, E string)",
                  pattern=[("E", 5), ("E", 7), ("E", 8), ("A", 5), ("A", 7), ("A", 8), ("D", 5), ("D", 7)],
                  position=5, **_RUN),
         ]),
    dict(n=4, short="Two-stroke arpeggios",
         intro="<b>Exercise 4</b> climbs a two-octave arpeggio to the high root on the G string, plucking each note "
               "twice. The fretting hand moves on every second stroke, and the pair of plucking fingers on each "
               "note changes as the cycle runs. Each arpeggio shifts twice: the major on the D string and for the "
               "top C, the minor on the D string and for the top A. Use the quarter rest to get back to the low "
               "root. Three passes, one per line, starting on <b>a</b>, <b>i</b> and <b>m</b>. The tempo is "
               "marked in eighth notes, so the same number means the same stroke rate as the other exercises.",
         vars=[
             dict(title="C major (C, E, G)",
                  pattern=_twice(("E", 8), ("A", 7), ("A", 10), ("D", 10, 2), ("G", 9, 1), ("G", 12, 4),
                                 ("G", 17, 4)),
                  position=7, **_ARP),
             dict(title="A minor (A, C, E)",
                  pattern=_twice(("E", 5), ("E", 8), ("A", 7), ("D", 7, 1), ("D", 10, 4), ("G", 9, 3),
                                 ("G", 14, 3)),
                  position=5, **_ARP),
         ]),
]

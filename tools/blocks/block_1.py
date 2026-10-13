"""Block 1 — directional plucking and the rake.

Everything that is specific to this block lives here: the text, and the
string sequence / rhythm of every variation. Fingerings are not written here;
tools/scores.py derives them from the plucking rules.
"""

NUMBER = 1
SUBTITLE = "Directional plucking and the rake"
CARD = "The a&ndash;m&ndash;i cycle on one string, then across two with the rake."

# Fretted pitches used by this block: string name -> (LilyPond written pitch, string number).
# C = E string, 8th fret; E = A string, 7th fret.
PITCHES = {"E": ("c", 4), "A": ("e", 3)}

DESCRIPTION = [
    "Block 1 builds the three-finger plucking cycle and carries it across two strings. Every exercise uses "
    "one sequence, <b>a&ndash;m&ndash;i</b>, repeated in strict order and never reset. Three fingers do not "
    "divide evenly into four beats, so the cycle starts each bar on a different finger; each exercise is "
    "written to the length at which it realigns, and the repeat sign always returns you to <b>a</b>.",
    "The two-string exercises add the <b>rake</b>. When you move from the A string back to the E string, the "
    "finger that played the last A-string note also plays the first E-string note, and the cycle continues "
    "from that finger. A rake is shown only by the repeated finger letter.",
    "The fretting hand holds one shape throughout&mdash;C at the 8th fret of the E string, E at the 7th fret "
    "of the A string&mdash;so all of your attention stays on the plucking hand.",
]


def _rep(seq, n):
    return [s for s in seq for _ in range(n)]


# Each variation: strings = one string name per note; dur = LilyPond duration;
# per_bar = notes per bar; bars_per_line = system breaks; tempo = text after the
# beat note; beat = LilyPond duration of the tempo note.
EXERCISES = [
    dict(n=1, short="One note",
         intro="<b>Exercise 1</b> sets the a&ndash;m&ndash;i cycle on a single note: C, 8th fret on the E string. "
               "Pluck in strict order and never reset. Against 4/4 the cycle returns to <b>a</b> on the downbeat "
               "every three bars, so each variation is a three-bar repeat. Move from whole notes to half notes to "
               "quarter notes, and raise the tempo only once quarter notes are even.",
         vars=[
             dict(title="Whole Notes", strings=["E"] * 3, dur="1", time="4/4", per_bar=1, bars_per_line=3, tempo="60–100"),
             dict(title="Half Notes", strings=["E"] * 6, dur="2", time="4/4", per_bar=2, bars_per_line=3, tempo="60–100"),
             dict(title="Quarter Notes", strings=["E"] * 12, dur="4", time="4/4", per_bar=4, bars_per_line=3, tempo="60–100"),
         ]),
    dict(n=2, short="Two strings, eight notes",
         intro="<b>Exercise 2</b> takes the cycle across two strings: two bars of C on the E string, then two bars "
               "of E on the A string. The cycle carries over the string change, so the A string leads off with "
               "<b>i</b>. On the return to the E string, <b>a</b> rakes: the ring finger plays the last A-string "
               "note and the first E-string note, and the pattern starts again. The 16-note phrase always lands "
               "on <b>a</b> at that point, so this exercise trains the ring-finger rake only.",
         vars=[
             dict(title="Quarter Notes", strings=_rep(["E", "A"], 8), dur="4", time="4/4", per_bar=4, bars_per_line=4, tempo="60–100"),
         ]),
    dict(n=3, short="Two strings, four notes",
         intro="<b>Exercise 3</b> uses the same two notes but changes string every four notes. The cycle no longer "
               "lines up with the string changes, so each pass leads off with a different finger and rakes with a "
               "different finger: <b>m</b>, then <b>i</b>, then <b>a</b>. The full cycle is six groups long and "
               "covers every rake and every E-to-A crossing. Learn it in half notes before moving to quarter notes.",
         vars=[
             dict(title="Half Notes", strings=_rep(["E", "A"] * 3, 4), dur="2", time="4/4", per_bar=2, bars_per_line=6, tempo="60–100"),
             dict(title="Quarter Notes", strings=_rep(["E", "A"] * 3, 4), dur="4", time="4/4", per_bar=4, bars_per_line=6, tempo="60–100"),
         ]),
    dict(n=4, short="Two strings, three notes",
         intro="<b>Exercise 4</b> changes string every three notes. A group of three matches the length of the "
               "cycle, so each A-string group repeats the fingering of the E-string group before it, and the rake "
               "rotates through <b>i</b>, <b>m</b> and <b>a</b>. Variation #1 puts one string per bar in 3/4, so "
               "every string change falls on a downbeat. Variation #2 is the target: 12/8, the same rhythm as "
               "eighth-note triplets in 4/4. The cycle runs six beats, so it realigns with the barline every three bars.",
         vars=[
             dict(title="Quarter Notes in 3/4", strings=_rep(["E", "A"] * 3, 3), dur="4", time="3/4", per_bar=3, bars_per_line=6, tempo="60–100"),
             dict(title="Triplets in 12/8", strings=_rep(["E", "A"] * 6, 3), dur="8", time="12/8", per_bar=12, bars_per_line=1,
                  tempo="50–80", beat="4."),
         ]),
]

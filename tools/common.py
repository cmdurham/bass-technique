"""Shared constants for the Bass Technique build."""
import pathlib

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent                    # repo root = site root (/bass-technique/)
BUILD = TOOLS / ".build"               # LilyPond intermediates (gitignored)

PROGRAM = "Three-Finger Plucking Program"
PROGRAM_DIR = "three-finger-plucking"
Y = "#FFD400"
YEAR = 2026
PIMA = "p = thumb (pulgar) &middot; i = index (&iacute;ndice) &middot; m = middle (medio) &middot; a = ring (anular)"


def block_dir(n):
    return ROOT / PROGRAM_DIR / f"block-{n}"


def pdf_name(n):
    return f"three-finger-plucking-block-{n}.pdf"


def roman(n):
    out = ""
    for v, s in [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out, n = out + s, n - v
    return out

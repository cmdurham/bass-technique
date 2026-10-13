"""Build the site: notation, PDF and web page for each block, plus the index.

    python3 tools/build.py                # publish build: every non-draft block + index, into the repo
    python3 tools/build.py 2              # publish build of block 2 only (index is always rebuilt)
    python3 tools/build.py --preview      # preview build: every block INCLUDING drafts,
    python3 tools/build.py --preview 2    #   into tools/.build/site/ (gitignored), never the repo

A block file with DRAFT = True is work in progress: its source is committed, but the
publish build skips it and leaves it off the index. Remove the flag to publish it.

Requires: pip install lilypond weasyprint   (lilypond ships its own binary)
"""
import importlib, shutil, sys
from common import TOOLS, ROOT, BUILD, PROGRAM_DIR, pdf_name
import scores, pdf, web

sys.dont_write_bytecode = True
PREVIEW_ROOT = BUILD / "site"


def load_blocks():
    mods = []
    for p in sorted((TOOLS / "blocks").glob("block_*.py"), key=lambda p: int(p.stem.split("_")[1])):
        mods.append(importlib.import_module(f"blocks.{p.stem}"))
    return mods


def is_draft(block):
    return getattr(block, "DRAFT", False)


def build_block(block, out_root):
    n = block.NUMBER
    print(f"block {n}{' (draft)' if is_draft(block) else ''}: notation", flush=True)
    svgs = scores.render(block, BUILD / f"block-{n}")
    for name, (_, fingers, lh) in svgs.items():
        print(f"  {name:7s} RH {' '.join(fingers)}")
        if any(lh):
            print(f"  {'':7s} LH {' '.join(str(x or '-') for x in lh)}")
            pairs = {}
            for f, l in zip(fingers, lh):
                pairs.setdefault(l, []).append(f)
            print(f"  {'':7s} each LH finger gets: " +
                  "  ".join(f"{l}:{''.join(sorted(v, key='ami'.index))}" for l, v in sorted(pairs.items(), key=lambda x: x[0] or 0)))
    out = out_root / PROGRAM_DIR / f"block-{n}"
    out.mkdir(parents=True, exist_ok=True)
    pdf_path = out / pdf_name(n)
    print(f"block {n}: pdf", flush=True)
    pages = pdf.build(block, svgs, pdf_path)
    print(f"block {n}: web page ({pages} PDF pages)", flush=True)
    (out / "index.html").write_text(web.block_page(block, svgs, pdf_path.stat().st_size, pages))


if __name__ == "__main__":
    args = sys.argv[1:]
    preview = "--preview" in args
    only = {int(a) for a in args if a.isdigit()}
    out_root = PREVIEW_ROOT if preview else ROOT
    if preview:
        out_root.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / "style.css", out_root / "style.css")
        shutil.copytree(ROOT / "fonts", out_root / "fonts", dirs_exist_ok=True)
    blocks = load_blocks()
    for b in blocks:
        if is_draft(b) and not preview:
            stale = ROOT / PROGRAM_DIR / f"block-{b.NUMBER}"
            print(f"block {b.NUMBER}: draft, skipped" +
                  (f" -- WARNING: published pages still exist at {stale.relative_to(ROOT)}/; git rm them to unpublish"
                   if stale.exists() else ""))
            continue
        if not only or b.NUMBER in only:
            build_block(b, out_root)
    listed = [b for b in blocks if preview or not is_draft(b)]
    (out_root / "index.html").write_text(web.index_page(listed))
    print(f"index: done -> {out_root / 'index.html'}")

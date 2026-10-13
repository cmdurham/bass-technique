"""Build the site: notation, PDF and web page for each block, plus the index.

    python3 tools/build.py          # every block in tools/blocks/
    python3 tools/build.py 2        # just block 2 (index is always rebuilt)

Requires: pip install lilypond weasyprint   (lilypond ships its own binary)
"""
import importlib, sys
from common import TOOLS, ROOT, BUILD, block_dir, pdf_name
import scores, pdf, web

sys.dont_write_bytecode = True


def load_blocks():
    mods = []
    for p in sorted((TOOLS / "blocks").glob("block_*.py"), key=lambda p: int(p.stem.split("_")[1])):
        mods.append(importlib.import_module(f"blocks.{p.stem}"))
    return mods


def build_block(block):
    n = block.NUMBER
    print(f"block {n}: notation", flush=True)
    svgs = scores.render(block, BUILD / f"block-{n}")
    for name, (_, fingers) in svgs.items():
        print(f"  {name:7s} {' '.join(fingers)}")
    out = block_dir(n)
    out.mkdir(parents=True, exist_ok=True)
    pdf_path = out / pdf_name(n)
    print(f"block {n}: pdf", flush=True)
    pdf.build(block, svgs, pdf_path)
    pages = 2 + len(block.EXERCISES)          # cover + description + one page per exercise
    print(f"block {n}: web page", flush=True)
    (out / "index.html").write_text(web.block_page(block, svgs, pdf_path.stat().st_size, pages))


if __name__ == "__main__":
    blocks = load_blocks()
    only = {int(a) for a in sys.argv[1:]}
    for b in blocks:
        if not only or b.NUMBER in only:
            build_block(b)
    (ROOT / "index.html").write_text(web.index_page(blocks))
    print("index: done")

"""Web pages: one page per block, plus the section index at the repo root."""
import re
from common import PROGRAM, PROGRAM_DIR, YEAR, PIMA, LH, pdf_name, roman, legend, uses_fretting, plural

FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
           "<rect width='100' height='100' fill='%23FFD400'/><text x='50' y='70' font-size='56' text-anchor='middle' "
           "font-family='sans-serif' font-weight='bold' fill='%23111'>CD</text></svg>")


def head(title, desc, root):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{root}style.css">
<link rel="icon" href="{FAVICON}">
</head>
<body>
<header class="topbar"><div class="wrap">
<a class="home" href="/">&larr; cmdurham.com</a>
<a class="sect" href="{root}">Bass Technique</a>
</div></header>'''


def foot(right):
    return f'''<footer class="site-foot"><div class="wrap"><span>&copy; {YEAR} Chris Durham</span><span>{right}</span></div></footer>
</body>
</html>
'''


def inline_svg(path, label):
    s = path.read_text()
    s = re.sub(r'<\?xml[^>]*>\s*', "", s)
    s = re.sub(r'\swidth="[\d.]+mm"\sheight="[\d.]+mm"', "", s, count=1)   # keep viewBox; CSS sizes it
    return s.replace("<svg ", f'<svg role="img" aria-label="{label}" ', 1)


def block_page(block, svgs, pdf_bytes, pdf_pages):
    B, root = block.NUMBER, "../../"
    lh_line = f'<br><b>LH</b>{LH}' if uses_fretting(block) else ""
    toc = "".join(f'<li><a href="#ex{e["n"]}"><b>{e["n"]:02d}</b>{e["short"]}</a></li>' for e in block.EXERCISES)
    parts = [
        head(f"{PROGRAM} — Block {B} · cmdurham.com",
             f"Block {B} of a three-finger plucking program for bass: {block.SUBTITLE.lower()}. Notation, tab and a printable PDF.",
             root),
        f'''<section class="hero"><div class="wrap">
<p class="crumbs"><a href="{root}">Bass Technique</a> / Block {B}</p>
<h1>Three<br>Finger<br>Plucking</h1><div class="goth">Program</div>
<div class="tape">BLOCK {B} &mdash; {block.SUBTITLE.lower().replace(" and ", " &amp; ")}</div><br>
<a class="dl" href="{pdf_name(B)}" download>Download the PDF <small>{pdf_bytes // 1024} KB &middot; {pdf_pages} pages</small></a>
<nav class="toc" aria-label="Exercises"><ol>{toc}</ol>
<div class="legend-inline">{legend(block)}</div></nav>
</div></section>
<main class="wrap">
<section class="sec" id="about"><div class="sec-hd"><h2 class="label">Block {B}</h2><div class="g">Program</div></div>
{"".join(f"<p{' class=intro' if i == 0 else ''}>{t}</p>" for i, t in enumerate(block.DESCRIPTION))}
<div class="pima"><b>PIMA</b>{PIMA}{lh_line}</div></section>''']
    for e in block.EXERCISES:
        vs = []
        for k, v in enumerate(e["vars"], 1):
            leg = f'<div class="legend">{legend(block)}</div>' if k == 1 else ""
            svg = inline_svg(svgs[f"ex{e['n']}_v{k}"][0], f"Exercise {e['n']}, variation {k}: {v['title']}, notation and tab")
            vs.append(f'''<div class="var"><div class="var-hd"><h3>Variation #{k}: {v["title"]}</h3>{leg}</div>
<div class="score">{svg}</div>
<p class="score-hint">Scroll sideways for the full line, or use the PDF.</p></div>''')
        parts.append(f'''<section class="sec" id="ex{e['n']}"><div class="sec-hd"><h2 class="label">Exercise {e['n']}</h2><div class="g">Block {roman(B)}</div></div>
<p class="intro">{e['intro']}</p>{"".join(vs)}</section>''')
    parts += ["</main>", foot(f"{PROGRAM} &middot; Block {B}")]
    return "\n".join(parts)


def index_page(blocks):
    cards = []
    for b in blocks:
        n_ex = len(b.EXERCISES)
        cards.append(f'''<a class="card live" href="{PROGRAM_DIR}/block-{b.NUMBER}/">
<div class="meta">{getattr(b, "FOCUS", "Plucking hand")} &middot; {plural(n_ex, "exercise")} &middot; PDF</div>
<h3>Block {b.NUMBER}</h3>
<p><b>{b.SUBTITLE}.</b> {b.CARD}</p>
<span class="cta">Open Block {b.NUMBER} &rarr;</span></a>''')
    nxt = max(b.NUMBER for b in blocks) + 1
    cards.append(f'''<div class="card lab"><div class="meta">In progress</div><div class="q">?</div>
<h3>Block {nxt}</h3><p>The next block.</p></div>''')
    return "\n".join([
        head("Bass Technique · cmdurham.com",
             "Bass technique work by Chris Durham: a three-finger plucking program, block by block, with notation, tab and printable PDFs.",
             ""),
        f'''<section class="hero small"><div class="wrap">
<h1>Bass<br>Technique</h1>
<div class="tape">plucking-hand work, block by block</div>
<p class="lede">A three-finger plucking program I'm writing as I work through it. Each block is a short set of
exercises with notation, tab and a printable PDF.</p>
<div class="hero-end"></div></div></section>
<main class="wrap">
<section class="sec"><div class="sec-hd"><h2 class="label">Three-Finger Plucking</h2><div class="g">Program</div></div>
<div class="cards">
{"".join(cards)}
</div></section>
</main>''',
        foot("Bass Technique"),
    ])

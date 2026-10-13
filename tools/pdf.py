"""Printable workbook PDF for a block (US Letter), style C: yellow, Anton, tape labels."""
import pathlib, re
from weasyprint import HTML
from common import PROGRAM, PIMA, LH, ROOT, Y, roman, legend, uses_fretting

FONTS = ROOT / "fonts"
FACES = [("Anton", "anton", 400), ("Special Elite", "special-elite", 400),
         ("UnifrakturMaguntia", "unifrakturmaguntia", 400), ("Inter Tight", "inter-tight", 400),
         ("Inter Tight", "inter-tight", 600), ("Inter Tight", "inter-tight", 800)]


def faces():
    return "\n".join(f"@font-face{{font-family:'{fam}';src:url('{(FONTS / f'{slug}-latin-{w}-normal.woff2').as_uri()}');"
                     f"font-weight:{w};font-style:normal}}" for fam, slug, w in FACES)


CSS = f'''
@page {{ size: letter; margin: 0 }}
body {{ margin:0; font-family:'Inter Tight'; color:#111 }}
.page {{ width:8.5in; height:11in; position:relative; overflow:hidden; break-after:page }}
.score {{ display:block }}
/* cover */
.cover {{ background:{Y} }}
.cv {{ position:absolute; inset:.75in }}
.cv h1 {{ font-family:'Anton'; font-weight:400; font-size:118pt; line-height:.9; margin:.3in 0 0; text-transform:uppercase }}
.goth {{ font-family:'UnifrakturMaguntia'; font-size:54pt; margin-top:.05in; line-height:1 }}
.tape {{ display:inline-block; background:#111; color:{Y}; font-family:'Special Elite'; font-size:14pt;
        padding:.1in .25in; transform:rotate(-2.5deg); margin-top:.45in; letter-spacing:.02em }}
.toc {{ position:absolute; bottom:0; left:0; right:0; border-top:8pt solid #111; padding-top:.14in;
       display:grid; grid-template-columns:1.15fr 1.15fr .9fr; column-gap:.25in; font-size:9.5pt; line-height:1.55 }}
.toc b {{ font-family:'Anton'; font-weight:400; font-size:11pt; margin-right:.08in }}
.toc .leg2 {{ font-family:'Special Elite'; font-size:9.5pt; line-height:1.55 }}
/* inner pages */
.wrap {{ position:absolute; inset:.7in .75in }}
.rule {{ border-top:8pt solid #111 }}
.hd {{ display:flex; justify-content:space-between; align-items:flex-start; margin-top:.2in }}
.lbl {{ display:inline-block; background:{Y}; font-family:'Anton'; font-size:34pt; text-transform:uppercase;
       padding:.02in .22in; transform:rotate(-1.5deg); letter-spacing:.01em }}
.hd .g {{ font-family:'UnifrakturMaguntia'; font-size:22pt }}
.intro {{ font-size:10.5pt; line-height:1.45; margin:.3in 0 .3in }}
.vrow {{ display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:.06in }}
.vt {{ font-family:'Special Elite'; font-size:11.5pt }}
.leg {{ font-family:'Special Elite'; font-size:9.5pt; border:1.5pt solid #111; padding:3pt 9pt; line-height:1.45; text-align:center }}
.var {{ margin-bottom:.32in; break-inside:avoid }}
@page ex {{ margin:.7in .75in 1.02in .75in;
  @bottom-left {{ content:"{PROGRAM}"; width:50%; vertical-align:top; border-top:3pt solid #111; padding-top:.07in;
                 font-family:'Anton'; font-size:10pt; text-transform:uppercase; letter-spacing:.06em }}
  @bottom-right {{ content:string(exfoot); width:50%; text-align:right; vertical-align:top; border-top:3pt solid #111;
                  padding-top:.07in; font-family:'Anton'; font-size:10pt; text-transform:uppercase; letter-spacing:.06em;
                  }} }}
.exflow {{ page:ex; break-before:page }}
.foottag {{ string-set:exfoot content(text); height:0; overflow:hidden; font-size:1pt; color:transparent }}
.pf {{ position:absolute; bottom:0; left:0; right:0; border-top:3pt solid #111; padding-top:.07in; display:flex;
      justify-content:space-between; font-family:'Anton'; font-size:10pt; text-transform:uppercase; letter-spacing:.06em }}
.desc p {{ font-size:11pt; line-height:1.5; margin:0 0 .16in; max-width:6.2in }}
.desc .first {{ margin-top:.35in }}
.pimabox {{ position:absolute; left:0; right:0; bottom:.45in; border:1.5pt solid #111; padding:.08in .15in;
           font-family:'Special Elite'; font-size:10pt }}
.pimabox b {{ font-family:'Anton'; font-weight:400; letter-spacing:.04em; margin-right:.1in }}
'''



def score_img(svg_path, width_mm=178):
    w = float(re.search(r'width="([\d.]+)mm"', svg_path.read_text()).group(1))
    return f'<img class="score" src="{svg_path.as_uri()}" style="width:{w * width_mm / 188:.1f}mm">'


def build(block, svgs, out_pdf):
    B = block.NUMBER
    toc = [f"<div><b>{e['n']:02d}</b>{e['short']}</div>" for e in block.EXERCISES]
    half = (len(toc) + 1) // 2
    cover = f'''<section class="page cover"><div class="cv">
<h1>Three<br>Finger<br>Plucking</h1><div class="goth">Program</div>
<div class="tape">BLOCK {B} &mdash; {block.SUBTITLE.lower().replace(" and ", " &amp; ")}</div>
<div class="toc"><div>{"".join(toc[:half])}</div><div>{"".join(toc[half:])}</div>
<div class="leg2">{legend(block)}</div></div></div></section>'''
    lh_line = f'<br><b>LH</b>{LH}' if uses_fretting(block) else ""
    paras = "".join(f'<p{" class=first" if i == 0 else ""}>{t}</p>' for i, t in enumerate(block.DESCRIPTION))
    desc = f'''<section class="page desc"><div class="wrap"><div class="rule"></div>
<div class="hd"><div class="lbl">Block {B}</div><div class="g">Program</div></div>{paras}
<div class="pimabox"><b>PIMA</b>{PIMA}{lh_line}</div>
<div class="pf"><span>{PROGRAM}</span><span>Block {B}</span></div></div></section>'''
    pages = []
    for e in block.EXERCISES:
        vs = "".join(f'''<div class="var"><div class="vrow"><div class="vt">Variation #{k}: {v["title"]}</div>
{f'<div class="leg">{legend(block)}</div>' if k == 1 else ""}</div>{score_img(svgs[f"ex{e['n']}_v{k}"][0])}</div>''' for k, v in enumerate(e["vars"], 1))
        pages.append(f'''<section class="exflow"><div class="foottag">Block {B} &middot; Ex {e['n']}</div><div class="rule"></div>
<div class="hd"><div class="lbl">Exercise {e['n']}</div><div class="g">Block {roman(B)}</div></div>
<p class="intro">{e['intro']}</p>{vs}</section>''')
    html = (f"<html><head><meta charset='utf-8'><title>{PROGRAM} &ndash; Block {B}</title>"
            f"<style>{faces()}{CSS}</style></head><body>{cover}{desc}{''.join(pages)}</body></html>")
    doc = HTML(string=html).render()
    doc.write_pdf(out_pdf)
    return len(doc.pages)

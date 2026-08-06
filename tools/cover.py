#!/usr/bin/env python3
"""Generate the print-ready cover(s) for Indio Yori · Teroyokori · Negro.

Outputs (into /workspace/build):
  front_cover.pdf   front cover only, trim + bleed (vector)
  wrap_cover.pdf    full wraparound: back + spine + front, trim + bleed

Parametric on trim, bleed and spine width so it can be regenerated with the
exact numbers Bubok's "calcula las medidas de tu portada" tool reports.
Usage: cover.py [pages] [spine_mm]
"""
import sys
from weasyprint import HTML

TRIM_W = 152.4     # mm (6 in / 15.2 cm)
TRIM_H = 228.6     # mm (9 in / 22.8 cm)
BLEED = 5.0        # mm bleed on outer edges
SAFE = 12.0        # mm safety margin from trim for text/logos

PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 168
# spine estimate: leaves x caliper (90 g/m2 offset ~0.11 mm/leaf) + cover wrap.
SPINE = float(sys.argv[2]) if len(sys.argv) > 2 else round((PAGES / 2) * 0.113 + 0.5, 1)

MAGENTA = "#e5197f"
VIOLET = "#7b3fb0"
INK = "#f2f0f2"
BG = "#0c0c11"
MUTE = "#9a97a3"
FONT = '"DejaVu Sans Mono", monospace'

BASE = f"""
*{{ box-sizing:border-box; }}
html,body{{ margin:0; padding:0; }}
h1{{ font-weight:bold; }}
h1 span{{ display:block; }} h1 .hl{{ color:{MAGENTA}; }}
.kicker{{ color:{MUTE}; font-size:10pt; letter-spacing:.12em; }}
.rule{{ width:34mm; height:3pt; background:{MAGENTA}; margin:7mm 0; }}
.sub{{ color:#cbc8d0; font-size:12pt; line-height:1.5; margin:0; }}
.term{{ font-size:11pt; display:flex; align-items:center; }}
.cur{{ display:inline-block; width:3.2mm; height:4.6mm; background:{MAGENTA}; margin-right:2.4mm; }}
.foot{{ color:{MUTE}; font-size:9pt; letter-spacing:.06em; margin-top:4mm;
  border-top:1px solid rgba(255,255,255,.12); padding-top:3mm; }}
"""

def front_panel(x_left, x_right, title_pt=37):
    """returns CSS+HTML for a front panel positioned within its column.
    head anchored near vertical center; footer pinned to bottom safe line."""
    return f"""
.front-head{{ position:absolute; left:{x_left}mm; right:{x_right}mm; top:60mm; }}
.front-head h1{{ font-size:{title_pt}pt; line-height:1.05; margin:9mm 0 0 0; letter-spacing:.01em; }}
.front-foot{{ position:absolute; left:{x_left}mm; right:{x_right}mm; bottom:{BLEED+SAFE}mm; }}
.front-foot .sub{{ margin-bottom:4mm; }}
"""

def front_html(x_ok=True):
    return """
<div class="front-head">
  <div class="kicker">$ ./desinstalar --olvido</div>
  <h1><span>INDIO</span><span>YORI</span><span class="hl">TEROYOKORI</span><span>NEGRO</span></h1>
  <div class="rule"></div>
  <p class="sub">El mestizaje como software colonial<br>y las políticas del olvido</p>
</div>
<div class="front-foot">
  <div class="term"><span class="cur"></span>INDIOYORI · INVESTIGADOR</div>
  <div class="foot">FronterIA-Lab · GTEPICC—CLACSO · 2026</div>
</div>
"""

GLOW_FRONT = (f"radial-gradient(120% 55% at 24% 34%, rgba(229,25,127,.22), rgba(12,12,17,0) 60%),"
              f"radial-gradient(90% 48% at 84% 86%, rgba(123,63,176,.18), rgba(12,12,17,0) 60%)")

def build_front():
    W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
    xl = BLEED + SAFE
    css = f"""
@page {{ size:{W}mm {H}mm; margin:0; }}
{BASE}
body{{ width:{W}mm; height:{H}mm; background:{BG}; color:{INK};
  font-family:{FONT}; background-image:{GLOW_FRONT}; }}
.topbar{{ position:absolute; top:{BLEED}mm; left:{BLEED}mm; right:{BLEED}mm;
  height:2.6mm; background:linear-gradient(90deg,{MAGENTA},{VIOLET}); }}
{front_panel(xl, xl, 38)}
"""
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body><div class='topbar'></div>{front_html()}</body></html>"
    HTML(string=html).write_pdf("/workspace/build/front_cover.pdf")
    return W, H

def build_wrap():
    total_w = TRIM_W * 2 + SPINE + 2 * BLEED
    total_h = TRIM_H + 2 * BLEED
    spine_x = BLEED + TRIM_W
    front_left = spine_x + SPINE + SAFE          # from page left to front text
    front_right = BLEED + SAFE                   # from page right to front text
    back_l = BLEED + SAFE
    css = f"""
@page {{ size:{total_w}mm {total_h}mm; margin:0; }}
{BASE}
body{{ width:{total_w}mm; height:{total_h}mm; background:{BG}; color:{INK};
  font-family:{FONT};
  background-image:radial-gradient(52% 48% at 84% 32%, rgba(229,25,127,.22), rgba(12,12,17,0) 60%),
                   radial-gradient(50% 44% at 16% 82%, rgba(123,63,176,.16), rgba(12,12,17,0) 60%); }}
.topbar{{ position:absolute; top:{BLEED}mm; left:{BLEED}mm; right:{BLEED}mm;
  height:2.6mm; background:linear-gradient(90deg,{VIOLET},{MAGENTA},{VIOLET}); }}
/* FRONT (right panel) */
{front_panel(front_left, front_right, 35)}
/* SPINE */
.spine{{ position:absolute; top:{BLEED}mm; bottom:{BLEED}mm; left:{spine_x}mm; width:{SPINE}mm;
  border-left:1px solid rgba(255,255,255,.06); border-right:1px solid rgba(255,255,255,.06); }}
.spine .txt{{ position:absolute; top:50%; left:50%;
  transform:translate(-50%,-50%) rotate(90deg); white-space:nowrap;
  font-size:9.5pt; letter-spacing:.05em; }}
.spine .txt b{{ color:{INK}; font-weight:bold; }}
.spine .txt .au{{ color:{MUTE}; }}
/* BACK (left panel) */
.back-head{{ position:absolute; left:{back_l}mm; width:{TRIM_W-2*SAFE}mm; top:{BLEED+SAFE+6}mm; }}
.back .tag{{ color:{MAGENTA}; font-size:13pt; font-weight:bold; line-height:1.3; }}
.back .blurb{{ color:#cdcad3; font-size:10.5pt; line-height:1.6; margin-top:6mm; }}
.back .blurb b{{ color:{INK}; }}
.back .who{{ color:{MUTE}; font-size:9.5pt; line-height:1.55; margin-top:6mm; }}
.back-foot{{ position:absolute; left:{back_l}mm; width:{TRIM_W-2*SAFE}mm; bottom:{BLEED+SAFE}mm;
  display:flex; align-items:flex-end; justify-content:space-between; }}
.back .brand{{ color:{MUTE}; font-size:8.5pt; letter-spacing:.05em; line-height:1.5; }}
.barcode{{ width:40mm; height:22mm; background:#f2f0f2; color:#0c0c11;
  font-size:6.5pt; display:flex; align-items:flex-end; justify-content:center; padding-bottom:1.6mm; }}
"""
    body = f"""
<div class="topbar"></div>
<div class="back">
  <div class="back-head">
    <div class="tag">El mestizaje no es mezcla.<br>Es software colonial.</div>
    <div class="blurb">
      Te dijeron que el mestizaje era un abrazo. Te dieron una bandera, una escuela
      y un apellido que cabía en un formulario —y te quitaron la lengua, la tierra
      y el derecho a nombrar lo que duele. <b>Eso no es identidad: es software.</b>
      Un programa instalado hace dos siglos para fabricar población administrable
      a partir de pueblos. Este libro no te da una identidad de catálogo: te muestra
      el código —y cómo desinstalarlo.
    </div>
    <div class="who">
      Para quien salió del campo a la ciudad y aún busca el nombre de lo que le falta.
      Para el chicano, para el afromexicano, para quien la frontera le cruzó la casa.
    </div>
  </div>
  <div class="back-foot">
    <div class="brand">FronterIA-Lab · GTEPICC—CLACSO<br>Edición comercial · 2026</div>
    <div class="barcode">ISBN — código de barras</div>
  </div>
</div>
<div class="spine"><div class="txt"><b>INDIO YORI · TEROYOKORI · NEGRO</b>&nbsp;&nbsp;<span class="au">· Indioyori</span></div></div>
{front_html()}
"""
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
    HTML(string=html).write_pdf("/workspace/build/wrap_cover.pdf")
    return total_w, total_h

if __name__ == "__main__":
    fw, fh = build_front()
    tw, th = build_wrap()
    print(f"pages={PAGES} spine={SPINE}mm")
    print(f"front: {fw} x {fh} mm (trim {TRIM_W}x{TRIM_H} + {BLEED}mm bleed)")
    print(f"wrap : {tw:.1f} x {th:.1f} mm (back {TRIM_W} + spine {SPINE} + front {TRIM_W} + 2x{BLEED} bleed)")

#!/usr/bin/env python3
"""Assemble the print-ready interior HTML from the extracted model.
Front matter follows the Bubok checklist order:
 p1,p2 blank · p3 portadilla · p4 créditos · p5 dedicatoria · p6 blank · p7 índice."""
import json, re, html, unicodedata, sys, pathlib

MODEL = "/workspace/build/model.json"
CSS = pathlib.Path("/workspace/tools/style.css").read_text()
OUT = "/workspace/build/interior.html"

model = json.load(open(MODEL))["elements"]

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "sec"

# assign ids to headings (unique)
seen = {}
for e in model:
    if e["type"] in ("h1", "h2", "h3"):
        base = slug(e["text"])
        n = seen.get(base, 0)
        seen[base] = n + 1
        e["id"] = base if n == 0 else f"{base}-{n}"

CODIGO = re.compile(r"^\s*C[óo]digo fuente", re.I)

def render_body():
    out = []
    open_part = False
    for e in model:
        t = e["type"]
        if t == "h1" and e.get("kind") == "part":
            if open_part:
                out.append("</section>")
            out.append('<section class="part">')
            open_part = True
            out.append(f'<h1 class="part" id="{e["id"]}">{html.escape(e["text"])}</h1>')
        elif t == "h1":
            out.append(f'<h1 class="chapter" id="{e["id"]}">{html.escape(e["text"])}</h1>')
        elif t == "h2":
            cls = "codigo" if CODIGO.match(e["text"]) else ""
            out.append(f'<h2 class="{cls}" id="{e["id"]}">{html.escape(e["text"])}</h2>')
        elif t == "h3":
            out.append(f'<h3 id="{e["id"]}">{html.escape(e["text"])}</h3>')
        elif t == "p":
            out.append(f"<p>{e['html']}</p>")
        elif t == "quote":
            out.append(f"<blockquote><p>{e['html']}</p></blockquote>")
        elif t == "ul":
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in e["items"]) + "</ul>")
        elif t == "ol":
            out.append("<ol>" + "".join(f"<li>{i}</li>" for i in e["items"]) + "</ol>")
    if open_part:
        out.append("</section>")
    return "\n".join(out)

def render_toc():
    rows = ['<div class="toc"><h1>Índice</h1><ul>']
    for e in model:
        if e["type"] != "h1":
            continue
        title = html.escape(e["text"])
        href = "#" + e["id"]
        if e.get("kind") == "part":
            rows.append(f'<li class="part-item"><a href="{href}">{title}</a></li>')
        else:
            # opening sections (before first part) vs chapters
            cls = "chap-item"
            rows.append(
                f'<li class="{cls}"><span class="t"><a href="{href}">{title}</a>'
                f'</span><span class="leader"></span><a class="pg" href="{href}"></a></li>')
    rows.append("</ul></div>")
    return "\n".join(rows)

FRONT = f"""
<div class="blank"></div>
<div class="blank"></div>

<div class="portadilla">
  <div class="kicker">EDICIÓN COMERCIAL</div>
  <h1>Indio Yori · Teroyokori · Negro</h1>
  <div class="accent"></div>
  <div class="sub">El mestizaje como software colonial y las políticas del olvido</div>
  <div class="foot">
    Indioyori Investigador · Yoreme / Ódami<br>
    FronterIA-Lab · GTEPICC—CLACSO
  </div>
</div>

<div class="creditos">
  <div class="note">
    Este libro se reescribe desde un manuscrito de investigación y un working
    paper publicados en el ecosistema FronterIA-Lab. No sustituye al aparato
    académico: lo traduce al cuerpo del lector. Las fuentes y la cadena de
    custodia teórica viven en el glosario y en las lecturas finales.
  </div>
  <div class="push copy">
    <b>Indio Yori · Teroyokori · Negro</b><br>
    El mestizaje como software colonial y las políticas del olvido<br>
    Edición comercial · Primera edición, 2026<br><br>
    © 2026 Indioyori Investigador (Yoreme / Ódami)<br>
    © 2026 FronterIA-Lab · GTEPICC—CLACSO<br><br>
    ISBN: 000-00-0000-000-0 &nbsp;<span style="color:#777">(pendiente de asignación)</span><br>
    Depósito Legal: 0-0000-0000 &nbsp;<span style="color:#777">(pendiente de asignación)</span><br><br>
    Todos los derechos reservados. Queda prohibida la reproducción total o
    parcial de esta obra por cualquier medio sin autorización escrita del titular
    del copyright, salvo cita breve con fines de crítica o investigación.<br><br>
    Diseño y composición: FronterIA-Lab · Tipografía: DejaVu Sans Mono<br>
    Impreso bajo demanda.
  </div>
</div>

<div class="dedicatoria">
  <p>Para quien salió del campo a la ciudad<br>
  y siente que algo se quedó en el camino.<br>
  Para quien la frontera le cruzó la casa.<br>
  Esto no es nostalgia: es el código.</p>
</div>

<div class="blank"></div>

{render_toc()}
"""

doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Indio Yori · Teroyokori · Negro</title>
<style>{CSS}</style></head>
<body>
{FRONT}
{render_body()}
</body></html>"""

pathlib.Path(OUT).write_text(doc)
print("wrote", OUT, "chars", len(doc))

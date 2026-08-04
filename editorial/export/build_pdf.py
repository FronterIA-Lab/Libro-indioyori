#!/usr/bin/env python3
"""Build Gumroad-ready PDF for Indio Yori commercial edition."""

from pathlib import Path
import markdown
from weasyprint import HTML, CSS

ROOT = Path("/workspace")
SRC = ROOT / "editorial/manuscrito/completo/LIBRO-COMPLETO.md"
AVATAR = ROOT / "sitio/assets/indioyori-avatar.jpeg"
OUT_DIR = ROOT / "editorial/export"
BUILD = OUT_DIR / "build"
PDF_PATH = OUT_DIR / "IndioYori-Teroyokori-Negro.pdf"
HTML_PATH = BUILD / "libro.html"

FONT_REG = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
FONT_MED = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"
FONT_ITA = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Italic.ttf"

CSS_TEXT = f"""
@font-face {{
  font-family: 'JB Mono';
  src: url('file://{FONT_REG}');
  font-weight: 400;
  font-style: normal;
}}
@font-face {{
  font-family: 'JB Mono';
  src: url('file://{FONT_MED}');
  font-weight: 500;
  font-style: normal;
}}
@font-face {{
  font-family: 'JB Mono';
  src: url('file://{FONT_BOLD}');
  font-weight: 700;
  font-style: normal;
}}
@font-face {{
  font-family: 'JB Mono';
  src: url('file://{FONT_ITA}');
  font-weight: 400;
  font-style: italic;
}}

@page {{
  size: 5.5in 8.5in;
  margin: 0.7in 0.65in 0.75in 0.7in;
  @bottom-center {{
    content: counter(page);
    font-family: 'JB Mono', monospace;
    font-size: 8pt;
    color: #5c5a57;
  }}
}}

@page cover {{
  margin: 0;
  @bottom-center {{ content: none; }}
}}

@page front {{
  margin: 0.9in 0.75in;
  @bottom-center {{ content: none; }}
}}

:root {{
  --ink: #0a0a0a;
  --paper: #f7f5f2;
  --muted: #5c5a57;
  --magenta: #d81b7a;
  --cyan: #2ec4c6;
  --violet: #5b2c8a;
}}

html, body {{
  font-family: 'JB Mono', monospace;
  font-size: 9.5pt;
  line-height: 1.55;
  color: var(--ink);
  background: var(--paper);
}}

.cover {{
  page: cover;
  width: 5.5in;
  height: 8.5in;
  position: relative;
  background: #0a0a0a;
  color: #f7f5f2;
  overflow: hidden;
}}

.cover-img {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 62%;
  object-fit: cover;
  object-position: center top;
}}

.cover-fade {{
  position: absolute;
  left: 0; right: 0; top: 48%;
  height: 18%;
  background: linear-gradient(180deg, transparent, #0a0a0a);
}}

.cover-body {{
  position: absolute;
  left: 0.45in;
  right: 0.45in;
  bottom: 0.45in;
}}

.cover-brand {{
  font-size: 22pt;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1;
  margin: 0 0 0.2in;
}}

.cover-brand::after {{
  content: '';
  display: block;
  width: 0.7in;
  height: 3px;
  margin-top: 0.15in;
  background: linear-gradient(90deg, #d81b7a, #2ec4c6);
}}

.cover-sub {{
  font-size: 9.5pt;
  font-weight: 500;
  line-height: 1.35;
  max-width: 28ch;
  margin: 0 0 0.25in;
}}

.cover-meta {{
  font-size: 7.5pt;
  color: #bdb7ae;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}}

.cover-meta strong {{
  color: #2ec4c6;
  font-weight: 500;
}}

.frontmatter {{
  page: front;
  break-after: page;
}}

.frontmatter h1 {{
  font-size: 16pt;
  line-height: 1.2;
  margin: 0 0 0.2in;
}}

.frontmatter .rule {{
  width: 0.6in;
  height: 2.5px;
  background: #d81b7a;
  margin: 0 0 0.3in;
  border: 0;
}}

.part-break {{
  break-before: page;
  margin: 1.8in 0 1in;
  text-align: left;
}}

.part-break h1 {{
  font-size: 14pt;
  color: #d81b7a;
  margin: 0 0 0.2in;
}}

h1 {{
  font-size: 13pt;
  font-weight: 700;
  line-height: 1.25;
  margin: 0.55in 0 0.2in;
  break-after: avoid;
}}

h2 {{
  font-size: 10.5pt;
  font-weight: 700;
  margin: 0.35in 0 0.12in;
  break-after: avoid;
  color: var(--ink);
}}

h3 {{
  font-size: 9.5pt;
  font-weight: 700;
  margin: 0.28in 0 0.1in;
  break-after: avoid;
  color: var(--violet);
}}

p {{
  margin: 0 0 0.14in;
  orphans: 3;
  widows: 3;
}}

em {{
  font-style: italic;
}}

strong {{
  font-weight: 700;
}}

blockquote {{
  margin: 0.2in 0;
  padding: 0.12in 0 0.12in 0.18in;
  border-left: 2.5px solid #d81b7a;
  color: var(--muted);
}}

blockquote p {{
  margin-bottom: 0.08in;
}}

hr {{
  border: none;
  border-top: 1px solid #d9d4cc;
  margin: 0.35in 0;
}}

ul, ol {{
  margin: 0 0 0.18in;
  padding-left: 0.25in;
}}

li {{
  margin-bottom: 0.06in;
}}

code {{
  font-family: 'JB Mono', monospace;
  font-size: 8.5pt;
  color: #5b2c8a;
}}

.chapter {{
  break-before: page;
}}

.chapter > h1:first-child {{
  margin-top: 0.3in;
}}

.eyebrow {{
  font-size: 7.5pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #d81b7a;
  font-weight: 700;
  margin: 0 0 0.1in;
}}
"""


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html5",
    )


def wrap_body(md_html: str) -> str:
    # Soft chapter page breaks: h1 that look like chapters
    # markdown already gives h1/h2; we add chapter class via simple replace heuristics
    html = md_html
    # Part openers often start with <h1>Parte
    html = html.replace("<h1>Parte ", '<div class="part-break"><h1>Parte ')
    # close part-break after first blockquote or hr is hard; skip — CSS on h1 Parte is enough via .part-break only if closed
    # Simpler: just style all h1 with page break except first ones handled by cover/front
    return html


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)

    raw = SRC.read_text(encoding="utf-8")
    body = md_to_html(raw)
    # Page-break before each top-level chapter heading in body
    body = body.replace("<h1>", '<section class="chapter"><h1>')
    # close sections loosely before next — not perfect but WeasyPrint tolerates unclosed
    body = body.replace('</section><section class="chapter">', "</section><section class=\"chapter\">")

    cover = f"""
    <section class="cover">
      <img class="cover-img" src="{AVATAR.as_uri()}" alt="IndioYori" />
      <div class="cover-fade"></div>
      <div class="cover-body">
        <p class="cover-brand">INDIO YORI</p>
        <p class="cover-sub">El mestizaje como software colonial<br/>y las políticas del olvido</p>
        <p class="cover-meta"><strong>Dolores Méndez Valdez</strong> · FronterIA-Lab · 2026</p>
      </div>
    </section>
    """

    front = """
    <section class="frontmatter">
      <p class="eyebrow">Edición comercial</p>
      <h1>Indio Yori · Teroyokori · Negro</h1>
      <div class="rule"></div>
      <p><em>El mestizaje no es mezcla. Es software colonial.</em></p>
      <p>Para quien salió del campo y aún busca el nombre de lo que le falta.
      Para quien la frontera le cruzó la casa.
      Para quien el relato nacional borró.
      Para quien sabe que hay raíz y aún no decide si venderla.</p>
      <p style="margin-top:0.4in;color:#5c5a57;font-size:8.5pt;">
      Dolores Méndez Valdez · Indioyori · Yoreme / Ódami<br/>
      FronterIA-Lab · GTEPICC—CLACSO · 2026
      </p>
    </section>
    """

    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>Indio Yori · Teroyokori · Negro</title>
</head>
<body>
{cover}
{front}
{body}
</body>
</html>
"""
    HTML_PATH.write_text(doc, encoding="utf-8")
    print(f"HTML → {HTML_PATH}")

    HTML(filename=str(HTML_PATH)).write_pdf(
        str(PDF_PATH),
        stylesheets=[CSS(string=CSS_TEXT)],
    )
    size_mb = PDF_PATH.stat().st_size / (1024 * 1024)
    print(f"PDF  → {PDF_PATH} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    build()

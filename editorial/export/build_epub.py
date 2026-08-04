#!/usr/bin/env python3
"""Build Gumroad-ready EPUB from commercial manuscript."""

from pathlib import Path
import re
import markdown
from ebooklib import epub

ROOT = Path("/workspace")
SRC = ROOT / "editorial/manuscrito/completo/LIBRO-COMPLETO.md"
AVATAR = ROOT / "sitio/assets/indioyori-avatar.jpeg"
OUT = ROOT / "editorial/export/IndioYori-Teroyokori-Negro.epub"

CSS = """
@namespace epub "http://www.idpf.org/2007/ops";
body {
  font-family: "Courier New", Courier, monospace;
  line-height: 1.55;
  color: #0a0a0a;
  background: #f7f5f2;
  margin: 0.8em;
}
h1 {
  font-size: 1.45em;
  line-height: 1.25;
  margin: 1.2em 0 0.6em;
  color: #0a0a0a;
  page-break-before: always;
}
h1.part {
  color: #d81b7a;
  font-size: 1.35em;
}
h2 {
  font-size: 1.1em;
  margin: 1.1em 0 0.45em;
}
h3 {
  font-size: 1em;
  margin: 0.9em 0 0.35em;
  color: #5b2c8a;
}
p { margin: 0 0 0.75em; }
blockquote {
  margin: 0.9em 0;
  padding: 0.2em 0 0.2em 0.8em;
  border-left: 3px solid #d81b7a;
  color: #5c5a57;
}
hr {
  border: none;
  border-top: 1px solid #d9d4cc;
  margin: 1.2em 0;
}
em { font-style: italic; }
strong { font-weight: bold; }
ul, ol { margin: 0 0 0.9em 1.2em; }
li { margin-bottom: 0.35em; }
.cover {
  text-align: center;
  margin-top: 2em;
}
.cover img {
  max-width: 100%;
  height: auto;
}
.cover-brand {
  font-size: 1.8em;
  font-weight: bold;
  margin: 0.8em 0 0.3em;
}
.cover-rule {
  width: 3em;
  height: 3px;
  background: linear-gradient(90deg, #d81b7a, #2ec4c6);
  margin: 0.4em auto 0.8em;
  border: 0;
}
.cover-sub {
  color: #5c5a57;
  font-size: 0.95em;
}
.cover-meta {
  margin-top: 1.5em;
  font-size: 0.85em;
  color: #2ec4c6;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
"""


def slugify(title: str, idx: int) -> str:
    s = re.sub(r"[^a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ]+", "-", title).strip("-").lower()
    s = s.encode("ascii", "ignore").decode("ascii") or "sec"
    return f"sec-{idx:02d}-{s[:40]}.xhtml"


def split_sections(md: str):
    parts = re.split(r"(?m)^(# .+)$", md)
    # parts[0] may be empty/preamble; then title, body, title, body...
    sections = []
    if parts[0].strip():
        sections.append(("Preliminares", parts[0].strip()))
    i = 1
    while i < len(parts):
        title = parts[i].lstrip("# ").strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append((title, f"# {title}\n\n{body}"))
        i += 2
    return sections


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html5",
    )


def build():
    sections = split_sections(SRC.read_text(encoding="utf-8"))
    book = epub.EpubBook()
    book.set_identifier("indioyori-teroyokori-negro-2026")
    book.set_title("Indio Yori · Teroyokori · Negro")
    book.set_language("es")
    book.add_author("Dolores Méndez Valdez")
    book.add_metadata("DC", "publisher", "FronterIA-Lab")
    book.add_metadata(
        "DC",
        "description",
        "El mestizaje como software colonial y las políticas del olvido. Edición comercial.",
    )
    book.add_metadata("DC", "subject", "mestizaje")
    book.add_metadata("DC", "subject", "decolonial")
    book.add_metadata("DC", "date", "2026")

    # Cover image
    cover_bytes = AVATAR.read_bytes()
    book.set_cover("cover.jpg", cover_bytes)

    style = epub.EpubItem(
        uid="style",
        file_name="style/libro.css",
        media_type="text/css",
        content=CSS.encode("utf-8"),
    )
    book.add_item(style)

    # Title/cover xhtml
    cover_page = epub.EpubHtml(
        title="Portada",
        file_name="portada.xhtml",
        lang="es",
    )
    cover_page.content = f"""
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head><title>Portada</title><link rel="stylesheet" href="style/libro.css" type="text/css"/></head>
    <body>
      <div class="cover">
        <img src="cover.jpg" alt="IndioYori"/>
        <p class="cover-brand">INDIO YORI</p>
        <div class="cover-rule"></div>
        <p class="cover-sub">El mestizaje como software colonial<br/>y las políticas del olvido</p>
        <p class="cover-meta">Dolores Méndez Valdez · FronterIA-Lab · 2026</p>
      </div>
    </body></html>
    """.encode("utf-8")
    cover_page.add_item(style)
    book.add_item(cover_page)

    spine = ["nav", cover_page]
    toc = [cover_page]
    chapters = []

    for idx, (title, md) in enumerate(sections):
        html_body = md_to_html(md)
        # mark part titles
        if title.startswith("Parte "):
            html_body = html_body.replace("<h1>", '<h1 class="part">', 1)
        fname = slugify(title, idx)
        ch = epub.EpubHtml(title=title, file_name=fname, lang="es")
        ch.content = f"""<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{title}</title>
<link rel="stylesheet" type="text/css" href="style/libro.css"/>
</head>
<body>{html_body}</body></html>""".encode("utf-8")
        ch.add_item(style)
        book.add_item(ch)
        chapters.append(ch)
        spine.append(ch)
        toc.append(ch)

    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(str(OUT), book)
    mb = OUT.stat().st_size / (1024 * 1024)
    print(f"EPUB → {OUT} ({mb:.2f} MB) · {len(chapters)} sections")


if __name__ == "__main__":
    build()

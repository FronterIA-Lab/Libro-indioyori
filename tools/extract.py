#!/usr/bin/env python3
"""Extract a faithful semantic model from the source WeasyPrint PDF.

The body is left-aligned DejaVu Sans Mono (ragged right). We reconstruct
paragraphs/hard-breaks using monospace geometry, and headings from the PDF
outline (authoritative). Text is taken verbatim (no paraphrasing)."""
import fitz, json, html, re, sys, unicodedata

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/ubuntu/.cursor/projects/workspace/uploads/IndioYori-Teroyokori-Negro__SIN__b4c2.pdf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/workspace/build/model.json"

# Geometry constants measured from the source
LEFT = 56.4          # body left edge (pt)
RIGHT = 342.0        # body right edge (pt)
CHARW = 5.719        # monospace advance at 9.5pt
PARA_GAP = 20.0      # vertical gap threshold: > => paragraph/blank line
# precise x0 bands (pt) measured from the source:
#   body 56.4 · number-marker 57.2 · bullet-marker 63.0 · quote 71.2 · list-text 74.4
QUOTE_LO = 68.0      # blockquote left edge band
QUOTE_HI = 72.8
LIST_X = 73.0        # hanging-indent list body text
FOLIO_SIZE = 8.5     # spans this small that are numeric => page folio

# Front matter of the source we DROP (rebuilt separately per Bubok checklist).
# Body starts at the "Nota de posición" heading. Everything before is title/
# credits/quote pages that we regenerate. We keep from "Nota de posición" on.
BODY_START_TITLE = "Nota de posición"

doc = fitz.open(SRC)

# ---- outline: authoritative heading text + level, keyed by page ----
toc = doc.get_toc()  # [level, title, page(1-based)]
def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()
# map normalized title -> level (headings), allow multiple
heading_levels = {}
for lvl, title, pg in toc:
    heading_levels[norm(title)] = lvl

# ---- gather ordered lines across all pages ----
LineList = []  # each: dict(page, y, x0, endx, size, runs=[(text,bold,ital)])
for pno in range(doc.page_count):
    page = doc[pno]
    raw = []
    for bl in page.get_text("dict")["blocks"]:
        if "lines" not in bl:
            continue
        for ln in bl["lines"]:
            spans = ln["spans"]
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            if not text.strip():
                continue
            x0 = min(s["bbox"][0] for s in spans)
            endx = max(s["bbox"][2] for s in spans)
            y = min(s["bbox"][1] for s in spans)
            size = max(s["size"] for s in spans)
            # drop folio (small numeric, centered)
            if size <= FOLIO_SIZE and re.fullmatch(r"\d+", text.strip()):
                continue
            runs = []
            for s in spans:
                fn = s["font"]
                runs.append([s["text"], "Bold" in fn, ("Obli" in fn or "Ital" in fn)])
            raw.append(dict(page=pno, y=y, x0=x0, endx=endx, size=size, runs=runs,
                            text=text))
    raw.sort(key=lambda r: (round(r["y"], 1), r["x0"]))
    # merge fragments that share the same visual line (same y within tol):
    # WeasyPrint sometimes emits one line as several blocks at different x.
    merged_raw = []
    for r in raw:
        if merged_raw and abs(r["y"] - merged_raw[-1]["y"]) < 3.5:
            prev = merged_raw[-1]
            # keep x order (already sorted by x0)
            joiner = "" if (prev["text"].endswith(" ") or r["text"].startswith(" ")) else " "
            if joiner:
                prev["runs"].append([joiner, False, False])
            prev["runs"].extend(r["runs"])
            prev["text"] = prev["text"] + joiner + r["text"]
            prev["endx"] = max(prev["endx"], r["endx"])
        else:
            merged_raw.append(r)
    LineList.extend(merged_raw)

# ---- find body start index ----
start = 0
for i, ln in enumerate(LineList):
    if norm(ln["text"]) == BODY_START_TITLE:
        start = i
        break
LineList = LineList[start:]

# ---- helpers ----
def line_html(runs):
    """inline HTML for one line, merging adjacent same-style runs."""
    parts = []
    for text, bold, ital in runs:
        parts.append((text, bold, ital))
    # merge
    merged = []
    for t, b, i in parts:
        if merged and merged[-1][1] == b and merged[-1][2] == i:
            merged[-1][0] += t
        else:
            merged.append([t, b, i])
    out = ""
    for t, b, i in merged:
        e = html.escape(t)
        if b and i:
            out += f"<strong><em>{e}</em></strong>"
        elif b:
            out += f"<strong>{e}</strong>"
        elif i:
            out += f"<em>{e}</em>"
        else:
            out += e
    return out

def max_chars(x0):
    return (RIGHT - x0) / CHARW

def is_bullet(text):
    return text.lstrip().startswith("\u2022") or text.lstrip().startswith("•")

NUM_RE = re.compile(r"^\s*\d+\.\s+\S")
def is_num_start(l):
    return l["x0"] < 60 and NUM_RE.match(l["text"])

def strip_marker(line, pat):
    """return a copy of line with a leading marker (regex pat) removed from runs."""
    m = re.match(pat, line["text"])
    if not m:
        return line
    rem = m.end()
    out = dict(line); runs = []
    for t, b, it in line["runs"]:
        if rem <= 0:
            runs.append([t, b, it]); continue
        if len(t) <= rem:
            rem -= len(t)
        else:
            runs.append([t[rem:], b, it]); rem = 0
    out["runs"] = runs
    out["text"] = line["text"][m.end():]
    return out

def assemble(block_lines):
    """join wrapped lines: soft-wrap => space, author hard break => <br>."""
    out = ""
    for k, bl in enumerate(block_lines):
        if k > 0:
            prev = block_lines[k-1]
            prev_text = prev["text"].rstrip()
            fw = bl["text"].strip().split(" ")[0] if bl["text"].strip() else ""
            # hard break only if the next word CLEARLY would have fit on the
            # previous line (conservative: near-full lines are natural wraps).
            fits = (len(prev_text) + 1 + len(fw)) <= (max_chars(prev["x0"]) - 1.0)
            out += "<br>\n" if fits else " "
        out += line_html(bl["runs"])
    return out

# ---- group into elements ----
elements = []
i = 0
N = len(LineList)
def heading_level(text):
    n = norm(text)
    if n in heading_levels:
        return heading_levels[n]
    return None

while i < N:
    ln = LineList[i]
    text = ln["text"].strip()
    size = ln["size"]
    hl = heading_level(text)
    # ---- headings ----
    if size >= 12.5:
        parts = [ln]; j = i + 1
        while j < N and LineList[j]["size"] >= 12.5 and \
                (LineList[j]["y"] - LineList[j-1]["y"]) < PARA_GAP:
            parts.append(LineList[j]); j += 1
        full = " ".join(p["text"].strip() for p in parts)
        kind = "part" if full.lower().startswith("parte") else "chapter"
        elements.append(dict(type="h1", kind=kind, text=full))
        i = j; continue
    if size >= 10.2 and all(r[1] for r in ln["runs"] if r[0].strip()):
        parts = [ln]; j = i + 1
        while j < N and LineList[j]["size"] >= 10.2 and \
                all(r[1] for r in LineList[j]["runs"] if r[0].strip()) and \
                (LineList[j]["y"] - LineList[j-1]["y"]) < PARA_GAP:
            parts.append(LineList[j]); j += 1
        full = " ".join(p["text"].strip() for p in parts)
        elements.append(dict(type="h2", text=full))
        i = j; continue
    if hl == 3:
        elements.append(dict(type="h3", text=text)); i += 1; continue

    def gather_item(stop_marker):
        """collect a list item: current line + indented continuation lines."""
        item = [LineList[i_local[0]]]; i_local[0] += 1
        while i_local[0] < N:
            nx = LineList[i_local[0]]
            if nx["x0"] < LIST_X or nx["size"] >= 10.2:
                break
            if (nx["y"] - item[-1]["y"]) >= PARA_GAP:
                break
            item.append(nx); i_local[0] += 1
        return item
    i_local = [i]

    # ---- bullet list ----
    if is_bullet(text):
        items = []
        while i_local[0] < N and is_bullet(LineList[i_local[0]]["text"]):
            item = gather_item(True)
            item[0] = strip_marker(item[0], r"^\s*[\u2022•]\s*")
            item[0]["x0"] = LIST_X   # text really starts at the hanging indent
            items.append(assemble(item))
        elements.append(dict(type="ul", items=items)); i = i_local[0]; continue

    # ---- numbered list ----
    if is_num_start(ln):
        items = []
        while i_local[0] < N and is_num_start(LineList[i_local[0]]):
            item = gather_item(False)
            item[0] = strip_marker(item[0], r"^\s*\d+\.\s*")
            item[0]["x0"] = LIST_X   # text really starts at the hanging indent
            items.append(assemble(item))
        elements.append(dict(type="ol", items=items)); i = i_local[0]; continue

    # ---- blockquote ----
    if QUOTE_LO <= ln["x0"] <= QUOTE_HI:
        q = [ln]; i += 1
        while i < N and QUOTE_LO <= LineList[i]["x0"] <= QUOTE_HI and \
                LineList[i]["size"] < 10.2 and \
                (LineList[i]["y"] - q[-1]["y"]) < PARA_GAP:
            q.append(LineList[i]); i += 1
        elements.append(dict(type="quote", html=assemble(q))); continue

    # ---- paragraph ----
    plines = [ln]; i += 1
    while i < N:
        nx = LineList[i]; gap = nx["y"] - plines[-1]["y"]
        if nx["size"] >= 10.2 and (nx["size"] >= 12.5 or
                all(r[1] for r in nx["runs"] if r[0].strip())):
            break
        if is_bullet(nx["text"]) or is_num_start(nx):
            break
        if nx["x0"] >= QUOTE_LO:      # blockquote / list indent begins
            break
        if gap > PARA_GAP:
            break
        plines.append(nx); i += 1
    elements.append(dict(type="p", html=assemble(plines)))

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(dict(elements=elements), f, ensure_ascii=False, indent=1)

# stats
from collections import Counter
c = Counter(e["type"] for e in elements)
print("elements:", dict(c), "total", len(elements))
# word count of reconstructed body
def strip_tags(s): return re.sub(r"<[^>]+>", "", s)
words = 0
for e in elements:
    if e["type"] in ("p", "quote"):
        words += len(html.unescape(strip_tags(e["html"])).split())
    elif e["type"] in ("ul", "ol"):
        for it in e["items"]:
            words += len(html.unescape(strip_tags(it)).split())
    else:
        words += len(e["text"].split())
print("reconstructed body words:", words)

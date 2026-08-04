# ESTOS son los archivos para Gumroad

## Los dos archivos listos

En esta carpeta (`editorial/export/`):

| Archivo | Para qué |
|---|---|
| `IndioYori-Teroyokori-Negro.pdf` | Lectura fija / imprimir · 191 pp. |
| `IndioYori-Teroyokori-Negro.epub` | Celular y e-readers (lo que Gumroad recomienda) |

Ambos son la **misma edición comercial**. Sube **los dos** al mismo producto.

---

## Cómo bajarlos de GitHub

**PDF:**  
https://github.com/FronterIA-Lab/Libro-indioyori/blob/cursor/libro-comercial-indioyori-18c6/editorial/export/IndioYori-Teroyokori-Negro.pdf

**EPUB:**  
https://github.com/FronterIA-Lab/Libro-indioyori/blob/cursor/libro-comercial-indioyori-18c6/editorial/export/IndioYori-Teroyokori-Negro.epub

En cada uno: botón **Download** → cae en Descargas.

O baja todo el ZIP de la rama y entra a `editorial/export/`.

---

## Cómo subirlo a Gumroad

1. Entra a https://gumroad.com  
2. **New product** → **Digital product**  
3. Nombre: `Indio Yori · Teroyokori · Negro`  
4. Precio: `13.99` USD  
5. En **Files / Content**: sube **PDF y EPUB** (los dos)  
6. Summary + Additional details (los textos que ya te pasé)  
7. **Publish** → copia el link → pégalo en Substack  

---

## Regenerar después de editar el texto

```bash
python3 editorial/export/build_pdf.py
python3 editorial/export/build_epub.py
```

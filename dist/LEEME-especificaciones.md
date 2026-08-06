# Indio Yori · Teroyokori · Negro — Archivos listos para Bubok

Formato de impresión: **15,2 × 22,8 cm** (equivale a 6 × 9 in / 152,4 × 228,6 mm).
Tipografía: DejaVu Sans Mono. Blanco y negro con acentos en los colores del avatar
(magenta `#e5197f` y violeta `#7b3fb0`).

## 1. Interior (tripa) — subir como PDF

`IndioYori-Teroyokori-Negro_INTERIOR_15.2x22.8cm.pdf`

- Tamaño de página: 152,4 × 228,6 mm exactos (sin sangría; la tripa no lleva sangría).
- **168 páginas.**
- Márgenes **espejados** según el checklist de Bubok:
  - Interior (lomo/encuadernación): **30 mm**
  - Exterior: **20 mm**
  - Superior e inferior: **22 mm**
- Orden del principio del libro (según el checklist):
  1. y 2. en blanco
  3. portadilla interior (título, autor, editorial)
  4. créditos (ISBN, Depósito Legal, ©)
  5. dedicatoria
  6. en blanco
  7. Índice (paginado automático)
  - A continuación: Nota de posición, Manifiesto y el cuerpo del libro.
- Los folios (números de página) aparecen desde el Índice; las páginas 1–6 van sin folio.

### Falta rellenar antes de imprimir
En la página de **créditos** hay dos datos marcados en magenta como *(pendiente de asignación)*:
- **ISBN** (lo asigna Bubok o tú).
- **Depósito Legal**.
Cuando los tengas, se regeneran en segundos con `tools/build_html.py`.

## 2. Portada — subir como imagen CMYK (JPG/PNG)

Bubok pide la cubierta en **JPG o PNG en modo CMYK** (no PDF) y valida las medidas
exactas con su herramienta **"Calcula las medidas de tu portada"** del panel de autor.

Se entregan dos versiones:

- **Cubierta completa (una sola pieza)**: contraportada + lomo + portada
  `..._PORTADA-COMPLETA_lomo10mm_CMYK.jpg` (300 ppp)
  - Medidas usadas: **324,8 × 238,6 mm** = contraportada 152,4 + **lomo 10 mm** + portada 152,4 + **5 mm de sangría** por lado.
- **Portada frontal sola** (para ebook / miniatura / o si subes las piezas por separado)
  `..._PORTADA-frontal_CMYK.jpg` (162,4 × 238,6 mm, 300 ppp).

También se incluye cada portada en **PNG RGB** (color más fiel al negro profundo del
diseño) y en **PDF** vectorial, por si los necesitas.

### IMPORTANTE sobre el lomo
El grosor del lomo (**10 mm**) es una **estimación** para 168 páginas en papel offset
de ~90 g/m². **Antes de subir**, usa la calculadora de Bubok para tu papel concreto y,
si el número difiere, se regenera la cubierta con la medida exacta:

```
python tools/cover.py 168 <lomo_en_mm>
```

Zona de seguridad: todo el texto y el logo están a ≥12 mm de los cortes y del lomo.
El código de barras del ISBN va en la contraportada (hay un hueco reservado).

## Cómo se generaron (reproducible)

- `tools/extract.py` — reconstruye el contenido del PDF base de forma fiel (texto
  literal; se verificó que el conjunto de palabras es idéntico al original).
- `tools/build_html.py` + `tools/style.css` — maquetan el interior con WeasyPrint 69.0
  (el mismo motor del PDF original) al nuevo formato.
- `tools/cover.py` — genera portada frontal y cubierta completa (parametrizable).

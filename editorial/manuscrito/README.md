# Manuscrito comercial — Indio Yori

## Estado: completo (edición comercial v1)

El manuscrito comercial íntegro vive en [`completo/`](completo/):

- **Índice:** [`completo/INDICE.md`](completo/INDICE.md)
- **Libro en un solo archivo:** [`completo/LIBRO-COMPLETO.md`](completo/LIBRO-COMPLETO.md) (~28 000 palabras)

Incluye: portadilla, nota de posición, manifiesto, 5 partes (18 capítulos), glosario, lecturas y nota de autora.

### Cómo exportar

```bash
# Vista rápida
python3 -m http.server 8080 --directory editorial/manuscrito/completo

# A PDF (si tienes pandoc + weasyprint o similar)
pandoc completo/LIBRO-COMPLETO.md -o IndioYori-edicion-comercial.pdf \
  --pdf-engine=xelatex -V mainfont="IBM Plex Mono"
```

### Relación con la fuente

El PDF de 133 pp. en la raíz del repo es la **fuente maestra académica**.  
Esta carpeta es la **edición comercial**: misma tesis, voz para el mestizo de a pie, el chicano, el afromexicano y quien no se encuentra en el relato oficial.

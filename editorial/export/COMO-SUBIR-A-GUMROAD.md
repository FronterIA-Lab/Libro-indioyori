# ESTE es el archivo para Gumroad

## El PDF listo

**Archivo:** `IndioYori-Teroyokori-Negro.pdf`  
(está en esta misma carpeta: `editorial/export/`)

- 191 páginas  
- Tamaño libro 5.5 × 8.5 pulgadas  
- Portada con tu avatar  
- Letra mono, blanco/negro, detalles magenta/cian  

---

## Cómo bajarlo de GitHub (fácil)

1. Abre este enlace:

https://github.com/FronterIA-Lab/Libro-indioyori/blob/cursor/libro-comercial-indioyori-18c6/editorial/export/IndioYori-Teroyokori-Negro.pdf

2. Arriba a la derecha haz clic en el botón **Download**  
   (o el ícono de bajar / las tres rayitas → Download).

3. El PDF cae en tu carpeta **Descargas**.

---

## Cómo subirlo a Gumroad (paso a paso)

1. Entra a https://gumroad.com y crea cuenta / inicia sesión.  
2. Clic en **New product**.  
3. Tipo: **Digital product**.  
4. Nombre: `Indio Yori · Teroyokori · Negro`  
5. Precio: `13.99` (dólares) — o el equivalente a $249 MX.  
6. En **Files / Content**: clic en subir → elige  
   `IndioYori-Teroyokori-Negro.pdf`  
   (el de tu carpeta Descargas).  
7. Descripción corta (puedes copiar esta):

> El mestizaje no es mezcla: es software colonial.  
> Un libro para quien salió del campo, para el chicano,  
> para el afromexicano que el relato borró,  
> y para quien sabe que hay raíz y aún no decide si venderla.  
> Dolores Méndez Valdez · FronterIA-Lab

8. **Publish**.  
9. Copia el link que te da Gumroad.  
10. Pégalo en tu Substack: “Comprar el libro aquí”.

Listo. No necesitas más archivos para empezar a vender.

---

## Si quieres regenerar el PDF después de editar el texto

```bash
python3 editorial/export/build_pdf.py
```

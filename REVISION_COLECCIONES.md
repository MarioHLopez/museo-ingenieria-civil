# Revisión de formatos de las colecciones

Revisión realizada el 18 de noviembre de 2026.

## Archivos de los bancos de obras

| Colección | PDF | JPG | JPEG | PNG | Total |
|---|---:|---:|---:|---:|---:|
| `Dockerfile.zip` | 13 | 0 | 0 | 0 | 13 |
| `RA_2_11_3_11377_01CIVIL_20262_ARM-La regla de cálculo y el arte de resolver problemas-2835700.zip` | 13 | 7 | 7 | 2 | 29 |
| **Total** | **26** | **7** | **7** | **2** | **42** |

No se encontraron otros formatos dentro de los ZIP. El lector del catálogo importó los 42 archivos sin avisos. Se abrieron todos con PyMuPDF y se representaron sus 45 páginas a baja resolución sin errores, documentos protegidos ni documentos vacíos.

## Conversión para la exposición

Los cuatro formatos ya son compatibles con la aplicación. `renderizar()`, en `app.py`, representa la página seleccionada de cada PDF o imagen como **PNG** antes de mostrarla con Streamlit. Los PDF de varias páginas conservan la navegación entre láminas.

No es necesario convertir permanentemente los PDF ni modificar los bancos de obras. Los originales se conservan para las descargas y la agrupación de duplicados. Los 42 archivos se organizan en las 25 publicaciones existentes mediante la agrupación visual, las equivalencias confirmadas y la exclusión de la portada.

## Archivos fuera de los bancos

- `Dockerfile/`: contiene 13 archivos, todos copias exactas de archivos del primer ZIP, comprobadas mediante SHA-256. No se deben volver a importar como nuevas obras.
- `Historieta Regla de Cálculo (Arbeláez, Cortes, Nandar).pdf`: copia exacta del PDF de ese nombre en la carpeta de Valeria del primer ZIP. Es la portada que ya se excluye de la exposición.
- `DIAPOSITIVA 08 (PROGRAMACIÓN) - ESTEBAN AGUDELO.docx`: documento de Word fuera de los ZIP. La revisión del texto y de su estructura encontró ejercicios de programación y siete imágenes incrustadas. No forma parte de las colecciones de historietas y no se incorporó ni convirtió para esta exposición.

Los documentos originales no se modificaron.

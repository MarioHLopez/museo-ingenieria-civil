# Museo Aula Civil · Ideas que construyen

Museo virtual en **Streamlit** para presentar los trabajos de estudiantes de Ingeniería Civil. Lee directamente las dos colecciones locales:

- `Dockerfile.zip`: primera colección de PDF (a pesar de su nombre, no es una configuración Docker).
- `RA_2_11_3_11377_01CIVIL_20262_ARM-La regla de cálculo y el arte de resolver problemas-2835700.zip`: nueva colección de PDF e imágenes JPG, JPEG y PNG.

## Ejecutar

Requiere Python 3.10 o superior. Desde esta carpeta:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Abre **http://localhost:8501**. Para detener la aplicación, pulsa `Ctrl+C` en la terminal.

## Funciones

- Entrada arquitectónica con fachada de hormigón, ventanas, escalones y una puerta que se entreabre al pasar el cursor. El botón «Abrir la puerta» permite ingresar a la sala.
- Sala con un **feed vertical inspirado en Instagram**: una publicación por trabajo, para recorrer desplazándose hacia abajo.
- Título «Ideas que construyen» al inicio, antes de «Historias que merecen verse».
- Presentación del docente, avatar y carta de agradecimiento **al final de todas las publicaciones**, en una tarjeta del mismo ancho que los trabajos.
- Costados decorados con ilustraciones de escalímetro, escuadra, compás, teodolito, nivel y casco de obra. En pantallas pequeñas se ocultan para dejar todo el espacio a las imágenes.
- Cada publicación muestra todos los nombres encima de la imagen, sin mostrar el nombre del archivo. Los PDF de varias páginas tienen botones para pasar de lámina sin recargar todo el recorrido.
- Obras visualmente idénticas agrupadas en una sola publicación con todos los estudiantes que las entregaron.
- Descarga de cada PDF o imagen original en el apartado «Ver documento original».
- Lectura automática de ambas colecciones locales, comparando duplicados entre ellas.
- La obra compartida por Valeria y Zharick se presenta girada 90° en sentido antihorario.

## Foto o avatar del docente

Se utiliza `Avatar STEM con laptop y fórmulas.png` para **Mg. Mario Hernan Lopez Arbelaez**. También se admiten los nombres alternativos **`foto_docente.jpg`**, **`foto_docente.png`** o **`avatar.png`**, en la misma carpeta que `app.py`. La aplicación muestra el retrato automáticamente dentro del círculo de la presentación. Mientras no haya fotografía, aparece una silueta ilustrada. No hay que cargarla desde la interfaz.

El título, la asignatura, el periodo y el texto de agradecimiento están en `app.py`.

## Sobre las entregas

Las colecciones contienen **42 archivos de 39 estudiantes**: 13 archivos de la primera colección y 29 de la nueva. La exposición tiene **25 publicaciones**, tras agrupar duplicados y retirar la portada «Historieta Regla de Cálculo (Arbeláez, Cortes, Nandar).pdf».

Por equivalencia confirmada por el docente, el trabajo de Maria Del Mar Cortes Bolaños pertenece a «Historieta Pliego (Arbeláez, Cortes, Nandar).pdf», junto con Valeria Arbelaez Gallego y Zharick Sabrina Nandar Tobar. Se conserva el pliego como imagen principal y su giro de 90° antihorario.

La revisión de la nueva colección también reúne copias con diferente compresión o formato: Ana Maria Aristizabal con Juan Andres Botero; Katalina Rivera con Maria Paula Franco; Einer Villarreal con Victor Tarapues; y cada una de las dos historietas entregadas por Santiago Alexis Aguilar y Juan Nicolas Garzon. Además, la comparación automática agrupa duplicados exactos dentro de ambas colecciones y entre ellas, como Sara Nicol Moreno y Manuela Rivas.

Cada publicación incluye un apartado para descargar por separado sus entregas originales. Los nombres proceden de las carpetas de Moodle y de los integrantes adicionales indicados por el docente en `AUTORES_ADICIONALES`, en `museo.py`. El contador refleja **43 estudiantes**, incluyendo a Juan Diego Vargas y Matias Quintero Quintero en el trabajo de Diana, y a Manuela Torres y Simón Ortiz en el de Nixon. Todos los estudiantes de ambas colecciones aparecen en el recorrido.

La comparación automática representa **todas las páginas** de cada PDF o imagen a una resolución normalizada y compara sus píxeles. Así también puede agrupar documentos con la misma apariencia y diferentes metadatos. Dos PDF que solo comparten la portada, pero tienen páginas interiores diferentes, se conservan como obras distintas. Las copias con diferencias de compresión, márgenes o formato se revisaron visualmente y se registraron en `EQUIVALENCIAS`, en `app.py`; no se agrupan automáticamente por similitud aproximada.

Se admiten carpetas con el formato `NOMBRE ESTUDIANTE_123_assignsubmission_file/trabajo.pdf` y archivos PDF, JPG, JPEG o PNG. Si un archivo está en la raíz del ZIP se muestra como «Sin estudiante identificado». Los archivos no se extraen al disco ni se modifican. El límite es de 40 MB por archivo y 250 MB de entregas descomprimidas por ZIP. Las carpetas descomprimidas que estén junto a la aplicación no se importan de nuevo.

La agrupación de obras está en `museo.py`. Los colores, la fachada y el feed se ajustan en `estilos.css` y `.streamlit/config.toml`. Los instrumentos de los costados están en `instrumentos_izquierda.svg` e `instrumentos_derecha.svg`. Las fuentes de Google son opcionales: sin Internet se usan fuentes locales alternativas.

## Compartir la exposición

El repositorio es https://github.com/MarioHLopez/museo-ingenieria-civil. GitHub aloja el código; la aplicación se ejecuta en **Streamlit Community Cloud**.

1. Sube a la rama `main` los archivos `app.py`, `catalogo.py`, `museo.py`, `requirements.txt`, `estilos.css`, `.streamlit/config.toml`, los dos SVG, el avatar y ambos ZIP de entregas. Conserva sus nombres originales.
2. Entra en https://share.streamlit.io/ e inicia sesión con GitHub.
3. Pulsa **Create app** y selecciona estos valores:
   - **Repository:** `MarioHLopez/museo-ingenieria-civil`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - En **Advanced settings**, selecciona Python **3.12**.
4. Pulsa **Deploy**. Streamlit instalará `requirements.txt` y te dará una URL para compartir el museo.

Los siguientes cambios que subas a `main` se desplegarán automáticamente. Si el despliegue falla, consulta los registros en **Manage app**.

`Dockerfile.zip` es una colección de trabajos: no hay que descomprimirla ni configurar Docker para este despliegue.

"""Galería académica de Ingeniería Civil. Ejecutar: streamlit run app.py."""

from base64 import b64encode
from html import escape
from pathlib import Path
from random import sample

import pymupdf
import streamlit as st

from catalogo import cargar_entregas
from museo import agrupar_obras


BASE = Path(__file__).resolve().parent
TITULO = "Ideas que construyen"
DOCENTE = "Mg. Mario Hernan Lopez Arbelaez"
CURSO = "Programación · Ingeniería Civil"
PERIODO = "2026"
MOSTRAR_CIERRE_DOCENTE = True
MOSTRAR_ACCESO_CLASE = False
ENLACE_CLASE = "https://teams.microsoft.com/meet/271941027693903?p=gOhUIeFDUP6dyKhkFe"
ELOGIOS_OBRAS = (
    "¡Talento a prueba de sismos!",
    "¡Esto sí tiene buenos cimientos!",
    "¡Creatividad que no se agrieta!",
    "¡Una obra de alto calibre!",
    "¡Aquí sobra ingenio, no concreto!",
    "¡Nivel de obra: una berraquera!",
    "¡Más ideas que ladrillos!",
    "¡Esta obra se lleva los aplausos!",
    "¡Ingenio con casco y mucho estilo!",
    "¡Una estructura de puro talento!",
    "¡Ni el compás mide tanto talento!",
    "¡Estos trazos construyen sonrisas!",
)
ARCHIVOS_ENTREGAS = (
    "Dockerfile.zip",
    "RA_2_11_3_11377_01CIVIL_20262_ARM-La regla de cálculo y el arte de resolver problemas-2835700.zip",
)
# Ajustes de montaje de las obras; no modifican los PDF originales.
GIROS_OBRAS = {
    "39220cd8676102f35a26b7d7185c0cacf4456b36f843e371b071817dcdd60060": -90,
    "d0d2d7a945d8c3fb8dbc6878836f37575cbda5908220af324647384eb9f51637": -90,
}
# Equivalencias revisadas visualmente (origen, obra principal).
# Conservan también las entregas originales con diferencias de formato o compresión.
EQUIVALENCIAS = (
    # Maria Del Mar → pliego de Valeria y Zharick, confirmado por el docente.
    ("528277ba4503a8b5251227fea606d46ae99c70b14a245174a99528ee9fb97c64",
     "39220cd8676102f35a26b7d7185c0cacf4456b36f843e371b071817dcdd60060"),
    # Juan Andres Botero → Ana Maria Aristizabal.
    ("ab64083a6fc98eb102418657f4a0df83cd656f00f161f9d26b2c1102dad00627",
     "0df207ad7efe908b90537461c104c25b119e3b18cf697c5f9ca552de9eda9485"),
    # Santiago y Juan Nicolas: dos historietas distintas, cada una entregada por ambos.
    ("a9c7ba118d99bdc108acdfa2c601afeaf2f8c7025a43f504d10560a7423d50c7",
     "9cd06721204e13332182400c36c6cabf4c889f52913a6a92c41577ce5c1f8f20"),
    ("822e1c644b22fecd6c341f46961abec31a94bcd148f348b21a93bb1197807650",
     "7b2d4f6fa5849d7551b0b99ef80972aa613caefffacbe664c4c971cdac461943"),
    # Katalina Rivera → imagen PNG del mismo trabajo entregado por Maria Paula.
    ("630b5775852119a6bcbbd0d18d3d46a74d679a7979101430f7e2cd939c052e3a",
     "52dac79582b524121edb1367a62cfc4624843cb6af85bd2e97c62ac00167eac3"),
    # Victor Tarapues → PDF del mismo trabajo entregado por Einer Villarreal.
    ("14b03ac8adb877732b39eb18da699d0cb565b9e2b4bc25c97d8147f48ca16457",
     "a69a6667312bf36726a2e7c8cf6e03be6902e7ca08cf89e0f20d33018c9fb867"),
)
st.set_page_config(page_title="Museo Aula Civil", page_icon="🏛️", layout="wide")
st.markdown(f"<style>{(BASE / 'estilos.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False, max_entries=4)
def leer_catalogo(datos: bytes):
    return cargar_entregas(datos)


@st.cache_data(show_spinner=False, max_entries=4)
def preparar_obras(colecciones: tuple[bytes, ...]):
    entregas = [entrega for datos in colecciones for entrega in leer_catalogo(datos)[0]]
    obras = agrupar_obras(entregas)
    por_id = {obra.id: obra for obra in obras}
    for origen, destino in EQUIVALENCIAS:
        if origen in por_id and destino in por_id:
            por_id[destino].entregas.extend(por_id.pop(origen).entregas)
    # Portada de la actividad retirada de la exposición a petición del docente.
    portada = "25d5f2474ce5fbf2cd65928e6269be1c6a77f2d4e4f76f90a16bfe5f161d546f"
    return [obra for obra in por_id.values() if obra.id != portada]


@st.cache_data(show_spinner=False, max_entries=160)
def renderizar(datos: bytes, pagina: int, ancho: int, giro: int = 0, formato: str = "pdf") -> tuple[bytes, int]:
    with pymupdf.open(stream=datos, filetype=formato) as documento:
        if documento.needs_pass:
            raise ValueError("Este PDF está protegido con contraseña.")
        if not documento.page_count:
            raise ValueError("Este PDF no contiene páginas.")
        hoja = documento.load_page(min(pagina, documento.page_count - 1))
        ancho_girado = (hoja.rect * pymupdf.Matrix(1, 1).prerotate(giro)).width
        escala = min(ancho / max(ancho_girado, 1), 2.5)
        imagen = hoja.get_pixmap(matrix=pymupdf.Matrix(escala, escala).prerotate(giro), alpha=False)
        return imagen.tobytes("png"), documento.page_count


def mover(clave: str, delta: int):
    st.session_state[clave] += delta


def cambiar_sala(dentro: bool):
    st.session_state.dentro = dentro


if not st.session_state.get("dentro", False):
    st.markdown(f"""
    <div class="exterior">
      <div class="cielo"><span>MUSEO UNIVERSITARIO / {escape(PERIODO)}</span></div>
      <div class="fachada">
        <div class="rotulo">AULA CIVIL</div>
        <div class="subrotulo">INGENIERÍA · CREATIVIDAD · CONOCIMIENTO</div>
        <div class="ventana ventana-izq"></div><div class="ventana ventana-der"></div>
        <div class="marquesina">{escape(TITULO)}</div>
        <div class="portal"><div class="hoja hoja-izq"><i></i></div><div class="hoja hoja-der"><i></i></div></div>
        <div class="escalon escalon-uno"></div><div class="escalon escalon-dos"></div>
      </div>
      <div class="explanada">{escape(CURSO)}<br><span>Una exposición construida por nuestros estudiantes</span></div>
    </div>
    """, unsafe_allow_html=True)
    with st.container(key="acceso"):
        st.button("Abrir la puerta · Entrar al museo →", type="primary", on_click=cambiar_sala, args=(True,), width="stretch")
    st.stop()

try:
    colecciones = tuple((BASE / nombre).read_bytes() for nombre in ARCHIVOS_ENTREGAS)
    with st.spinner("Preparando la exposición…"):
        catalogos = [leer_catalogo(datos) for datos in colecciones]
        entregas = [entrega for catalogo, _ in catalogos for entrega in catalogo]
        avisos = [aviso for _, avisos_catalogo in catalogos for aviso in avisos_catalogo]
except (ValueError, OSError) as error:
    st.error(str(error))
    st.stop()
for aviso in avisos:
    st.warning(aviso)
if not entregas:
    st.info("No se encontraron PDF ni imágenes en los archivos de entregas.")
    st.stop()

with st.spinner("Colgando las obras y reuniendo los nombres de sus estudiantes…"):
    obras = preparar_obras(colecciones)

@st.fragment
def mostrar_publicacion(obra, numero: int):
    """Cada publicación cambia de lámina sin volver a cargar todo el recorrido."""
    clave = f"pagina-{obra.id}"
    st.session_state.setdefault(clave, 0)
    with st.container(key=f"publicacion-{obra.id}"):
        nombres = "".join(f"<li>{escape(nombre)}</li>" for nombre in obra.estudiantes)
        compartida = '<span class="post-compartida">Obra compartida</span>' if len(obra.entregas) > 1 else ""
        st.markdown(f'<div class="post-cabecera"><span class="post-avatar">{numero:02d}</span><div><span class="post-etiqueta">INGENIERÍA CIVIL · TRABAJO ESTUDIANTIL</span><span class="post-autores-etiqueta">ESTUDIANTES</span><ul class="post-autores">{nombres}</ul>{compartida}</div><span class="post-indice">{numero:02d} / {len(obras):02d}</span></div>', unsafe_allow_html=True)
        try:
            imagen, paginas = renderizar(obra.contenido, st.session_state[clave], 1300, GIROS_OBRAS.get(obra.id, 0), obra.entregas[0].formato)
            st.image(imagen, width="stretch")
            if paginas > 1:
                anterior, indicador, siguiente = st.columns([1, 1, 1])
                anterior.button("← Anterior", key=f"anterior-{obra.id}", on_click=mover,
                                args=(clave, -1), disabled=st.session_state[clave] == 0, width="stretch")
                puntos = " ".join("●" if p == st.session_state[clave] else "○" for p in range(paginas))
                indicador.markdown(f'<div class="post-paginas">{puntos}<br><small>{st.session_state[clave] + 1} / {paginas}</small></div>', unsafe_allow_html=True)
                siguiente.button("Siguiente →", key=f"siguiente-{obra.id}", on_click=mover,
                                 args=(clave, 1), disabled=st.session_state[clave] >= paginas - 1, width="stretch")
        except Exception:
            st.warning("No se puede mostrar esta lámina. El documento original está disponible abajo.")
        st.markdown('<div class="post-pie"><p>Una idea, una historia y el esfuerzo de aprender a construir.</p><span>#AulaCivil &nbsp; #TalentoEstudiantil &nbsp; #IdeasQueConstruyen</span></div>', unsafe_allow_html=True)
        with st.expander("Ver documento original"):
            for indice, entrega in enumerate(obra.entregas, 1):
                st.download_button(f"↓ Descargar original {indice:02d}", entrega.contenido,
                                   file_name=entrega.archivo, mime=entrega.mime, key=f"descarga-{entrega.id}")


st.markdown('<div class="feed-nav"><span>▱ AULA CIVIL</span><span>MUSEO DE IDEAS / 2026</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="instrumentos-lateral instrumentos-izquierda" aria-hidden="true">'
    + (BASE / "instrumentos_izquierda.svg").read_text(encoding="utf-8")
    + '</div><div class="instrumentos-lateral instrumentos-derecha" aria-hidden="true">'
    + (BASE / "instrumentos_derecha.svg").read_text(encoding="utf-8")
    + '</div>', unsafe_allow_html=True,
)
if "elogios_laterales" not in st.session_state:
    st.session_state.elogios_laterales = sample(ELOGIOS_OBRAS, 8)
for indice_lado, lado in enumerate(("izquierda", "derecha")):
    mensajes = st.session_state.elogios_laterales[indice_lado * 4:(indice_lado + 1) * 4]
    elogios = "".join(
        f'<span class="anuncio-elogio" style="animation-delay: {indice * 4}s">{escape(mensaje)}</span>'
        for indice, mensaje in enumerate(mensajes)
    )
    st.markdown(f"""
    <aside class="anuncio-clase anuncio-clase-{lado}" aria-label="Celebramos el talento de nuestros estudiantes">
      <div class="anuncio-tarjeta">
        <span class="anuncio-ventana" aria-hidden="true">AULA CIVIL.exe <b>_ □ ×</b></span>
        <span class="anuncio-contenido">
          <span class="anuncio-nuevo">★ PURO TALENTO ★</span>
          <svg class="anuncio-pc" viewBox="0 0 160 120" aria-hidden="true" fill="none">
            <path d="M20 8h120v80H20z" fill="#c0c0c0" stroke="#111" stroke-width="4"/>
            <path d="M30 18h100v58H30z" fill="#16004b" stroke="#fff" stroke-width="2"/>
            <path d="m60 38-12 10 12 10m40-20 12 10-12 10M88 30 74 66" stroke="#00ffae" stroke-width="5"/>
            <path d="M65 88v12h30V88M35 101h90l15 12H20z" fill="#c0c0c0" stroke="#111" stroke-width="4"/>
            <path d="M38 106h84" stroke="#fff" stroke-width="3"/>
            <path d="m8 23 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1zM149 65l3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z" fill="#ffff00"/>
          </svg>
          <strong class="anuncio-elogios">{elogios}</strong>
          <span class="anuncio-mensaje">100% INGENIO ESTUDIANTIL</span>
          <span class="anuncio-clic">★ APLAUSOS A ESTA OBRA ★</span>
          <span class="anuncio-pie">HECHO CON IDEAS Y CORAZÓN</span>
        </span>
      </div>
    </aside>
    """, unsafe_allow_html=True)

with st.container(key="feed"):
    st.markdown(f'<div class="feed-intro"><span>EL TALENTO DE NUESTRA AULA</span><h1>{escape(TITULO)}</h1><h2>Historias que merecen verse.</h2><p>{escape(CURSO)} · {escape(PERIODO)}</p><p>Un trabajo a la vez. Baja y recorre la exposición.</p></div>', unsafe_allow_html=True)
    for numero, obra in enumerate(obras, 1):
        mostrar_publicacion(obra, numero)

if not MOSTRAR_CIERRE_DOCENTE:
    st.stop()

with st.container(key="docente"):
    foto = next((BASE / nombre for nombre in ("Avatar STEM con laptop y fórmulas.png", "foto_docente.jpg", "foto_docente.png", "avatar.png") if (BASE / nombre).is_file()), None)
    if foto:
        mime = "image/png" if foto.suffix == ".png" else "image/jpeg"
        avatar = f'<img class="foto-docente" src="data:{mime};base64,{b64encode(foto.read_bytes()).decode()}" alt="Avatar de {escape(DOCENTE, quote=True)}">'
    else:
        avatar = '<div class="avatar-docente" role="img" aria-label="Espacio para el retrato del docente"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="34" r="17"/><path d="M18 88c0-37 64-37 64 0"/></svg></div>'
    st.markdown(f"""
    <section class="carta-docente">
      <div class="docente-etiqueta">UNA EXPOSICIÓN CON GRATITUD</div>
      {avatar}
      <span class="docente-firma">DE TU DOCENTE, PARA USTEDES</span>
      <p class="docente-nombre">{escape(DOCENTE)}</p>
      <p class="docente-curso">{escape(CURSO)} · {escape(PERIODO)}</p>
      <div class="carta-linea"></div>
      <p>A mis estudiantes:</p>
      <p>Gracias por su compromiso, su esfuerzo y, especialmente, por la disposición de estar presentes, participar y permitirse aprender durante este semestre.</p>
      <p>Quiero agradecerles también por algo que valoro profundamente: <strong>su disposición a ser enseñables</strong>. Por abrirse a nuevas ideas, cuestionar lo que creían saber, reconocer que no tenemos todas las respuestas y comprender que equivocarse también hace parte del camino.</p>
      <p>Detrás de cada trabajo hay preguntas, intentos, dificultades, aprendizajes y la valentía de seguir adelante. Esta exposición es una forma de reconocer ese proceso y celebrar lo que cada uno ha logrado construir.</p>
      <p>Me alegra haberlos acompañado, pero también agradezco lo que ustedes me han permitido aprender como docente. Porque enseñar y aprender son procesos que nos transforman a ambos.</p>
      <p>Espero que conserven la curiosidad, la humildad para seguir aprendiendo y el carácter para afrontar los desafíos que encuentren en su camino.</p>
      <p><strong>Que las ganas de aprender, de cuestionar y de construir sigan siendo los cimientos de todo lo que emprendan.</strong></p>
      <h2 class="agradecimiento-final">Gracias por construir<br>este espacio conmigo.</h2>
      <p class="carta-cierre">Con gratitud y orgullo,<br><strong>{escape(DOCENTE)}</strong><br>Su docente</p>
      <div class="docente-datos"><span><b>{len(obras)}</b> obras</span><span><b>{len({nombre for obra in obras for nombre in obra.estudiantes})}</b> estudiantes</span><span>Un semestre compartido</span></div>
      <div class="instruccion-scroll">Cada esfuerzo deja huella. Gracias por ser parte de esta historia.</div>
    </section>
    """, unsafe_allow_html=True)

if not MOSTRAR_ACCESO_CLASE:
    st.stop()

st.markdown(f"""
<a class="clase-flotante" href="{escape(ENLACE_CLASE, quote=True)}"
   target="_blank" rel="noopener noreferrer" aria-label="¡Entrar a clase! Abrir reunión de Microsoft Teams">
  <span class="clase-flotante-icono" aria-hidden="true">▶</span>
  <span class="clase-flotante-texto">
    <strong>¡Entrar a clase!</strong>
    <span class="clase-flotante-mensajes" aria-hidden="true">
      <span>¡Tu próxima gran idea empieza aquí!</span>
      <span>Del museo al aula… ¡vamos a Teams!</span>
      <span>¡Ponte el casco de las ideas y entra!</span>
    </span>
  </span>
  <span class="clase-flotante-flecha" aria-hidden="true">↗</span>
</a>
""", unsafe_allow_html=True)

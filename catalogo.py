"""Lectura de entregas Moodle desde un ZIP, sin extraer archivos al disco."""

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from pathlib import PurePosixPath
import re
import unicodedata
from zipfile import BadZipFile, ZipFile
import mimetypes


MAX_ARCHIVO = 40 * 1024 * 1024
MAX_TOTAL = 250 * 1024 * 1024


@dataclass(frozen=True)
class Entrega:
    id: str
    estudiante: str
    archivo: str
    contenido: bytes
    huella: str

    @property
    def formato(self) -> str:
        return PurePosixPath(self.archivo).suffix.lower().lstrip(".")

    @property
    def mime(self) -> str:
        return mimetypes.guess_type(self.archivo)[0] or "application/octet-stream"


def normalizar(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto.casefold())
        if unicodedata.category(c) != "Mn"
    )


def cargar_entregas(contenido: bytes) -> tuple[list[Entrega], list[str]]:
    entregas = []
    avisos = []
    total = 0
    try:
        with ZipFile(BytesIO(contenido)) as archivo_zip:
            for indice, info in enumerate(archivo_zip.infolist()):
                ruta = PurePosixPath(info.filename)
                if info.is_dir() or ruta.suffix.lower() not in {".pdf", ".jpg", ".jpeg", ".png"} or "__MACOSX" in ruta.parts:
                    continue
                if info.file_size > MAX_ARCHIVO:
                    avisos.append(f"Se omitió {ruta.name}: supera los 40 MB.")
                    continue
                total += info.file_size
                if total > MAX_TOTAL:
                    raise ValueError("Las entregas del ZIP superan el límite de 250 MB descomprimidos.")
                carpeta = ruta.parent.name
                nombre = re.sub(r"_\d+_assignsubmission_file.*$", "", carpeta)
                estudiante = nombre.replace("_", " ").strip().title() or "Sin estudiante identificado"
                try:
                    datos = archivo_zip.read(info)
                except (RuntimeError, BadZipFile, NotImplementedError) as error:
                    avisos.append(f"No se pudo leer {ruta.name}: {error}")
                    continue
                entregas.append(Entrega(
                    id=f"{indice}-{sha256(info.filename.encode()).hexdigest()[:12]}",
                    estudiante=unicodedata.normalize("NFC", estudiante),
                    archivo=unicodedata.normalize("NFC", ruta.name),
                    contenido=datos,
                    huella=sha256(datos).hexdigest(),
                ))
    except BadZipFile as error:
        raise ValueError("El archivo seleccionado no es un ZIP válido o está dañado.") from error
    return sorted(entregas, key=lambda entrega: normalizar(entrega.estudiante)), avisos

"""Agrupación de documentos por su apariencia, incluyendo todas sus páginas."""

from dataclasses import dataclass
from hashlib import sha256

import pymupdf

from catalogo import Entrega


# Integrantes adicionales confirmados por el docente para cada obra.
AUTORES_ADICIONALES = {
    "addd4eb0d8aef169fb4cdc0af5a79d3d1ff16f017cbb7b71028592467c160bd8": (
        "Juan Diego Vargas",
        "Matias Quintero Quintero",
    ),
    "e7dce95c962b7a8da3e6eb99fac5bbb52187b56f89c338a774c54699c1fa6208": (
        "Manuela Torres",
        "Simón Ortiz",
    ),
}


@dataclass
class Obra:
    id: str
    entregas: list[Entrega]

    @property
    def estudiantes(self) -> list[str]:
        nombres = [e.estudiante for e in self.entregas]
        nombres.extend(AUTORES_ADICIONALES.get(self.id, ()))
        return list(dict.fromkeys(nombres))

    @property
    def autores(self) -> str:
        return " · ".join(self.estudiantes)

    @property
    def archivo(self) -> str:
        return self.entregas[0].archivo

    @property
    def contenido(self) -> bytes:
        return self.entregas[0].contenido


def agrupar_obras(entregas: list[Entrega]) -> list[Obra]:
    grupos: dict[str, Obra] = {}
    conocidas: dict[str, str] = {}
    for entrega in entregas:
        firma = conocidas.get(entrega.huella)
        if firma is None:
            try:
                with pymupdf.open(stream=entrega.contenido, filetype=entrega.formato) as doc:
                    if doc.needs_pass or not doc.page_count:
                        raise ValueError("PDF sin páginas accesibles")
                    huella = sha256(str(doc.page_count).encode())
                    for pagina in doc:
                        escala = 900 / max(pagina.rect.width, pagina.rect.height, 1)
                        imagen = pagina.get_pixmap(matrix=pymupdf.Matrix(escala, escala), alpha=False)
                        huella.update(f"{imagen.width}x{imagen.height}:".encode())
                        huella.update(imagen.samples)
                    firma = huella.hexdigest()
            except Exception:
                # Un archivo no representable sigue disponible para descargar.
                firma = entrega.huella
            conocidas[entrega.huella] = firma
        if firma not in grupos:
            grupos[firma] = Obra(firma, [])
        grupos[firma].entregas.append(entrega)
    return list(grupos.values())

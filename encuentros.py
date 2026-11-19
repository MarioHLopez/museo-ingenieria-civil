"""Encuentros del 19 de noviembre de 2026, con horario de Colombia."""

from datetime import datetime, timedelta
from math import ceil
from zoneinfo import ZoneInfo


ZONA_COLOMBIA = ZoneInfo("America/Bogota")
CAMBIO_DE_CLASE = datetime(2026, 11, 19, 10, 59, tzinfo=ZONA_COLOMBIA)
CLASE_9 = {
    "titulo": "Clase 23 · Introducción a la Programación · 02CIVIL",
    "horario": "Jueves 19 de noviembre · 9:00–11:00 a. m. · Colombia",
    "enlace": "https://teams.microsoft.com/meet/271941027693903?p=gOhUIeFDUP6dyKhkFe",
}
CLASE_11 = {
    "titulo": "Clase 26 · Introducción a la Programación · 01CIVIL",
    "horario": "Jueves 19 de noviembre · 11:00 a. m.–1:00 p. m. · Colombia",
    "enlace": "https://teams.microsoft.com/meet/240303568231638?p=oY54dOaZZmGOk0G0dG",
}


def seleccionar_encuentro(ahora: datetime | None = None) -> dict[str, str]:
    ahora = ahora if ahora is not None else datetime.now(ZONA_COLOMBIA)
    if ahora.tzinfo is None:
        raise ValueError("La fecha debe incluir una zona horaria.")
    return CLASE_9 if ahora < CAMBIO_DE_CLASE else CLASE_11


def alerta_encuentro(ahora: datetime | None = None) -> tuple[str, str] | None:
    ahora = ahora if ahora is not None else datetime.now(ZONA_COLOMBIA)
    if ahora.tzinfo is None:
        raise ValueError("La fecha debe incluir una zona horaria.")
    segundos = (CAMBIO_DE_CLASE - ahora).total_seconds()
    if 0 < segundos <= 300:
        minutos = ceil(segundos / 60)
        return "aviso", (
            f"⏰ Cambio de clase en {minutos} min. A las 10:59 a. m. (Colombia), "
            "el acceso cambiará al grupo 01CIVIL, clase 26, de 11:00 a. m. a 1:00 p. m."
        )
    if CAMBIO_DE_CLASE <= ahora < CAMBIO_DE_CLASE + timedelta(minutes=3):
        return "cambio", "🔔 ¡Acceso actualizado! Ya puedes entrar a la clase 26 del grupo 01CIVIL, de 11:00 a. m. a 1:00 p. m."
    return None

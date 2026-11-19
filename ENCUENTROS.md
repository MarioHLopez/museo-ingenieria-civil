# Acceso a las clases del jueves 19 de noviembre de 2026

**Estado preparado: acceso oculto.** No activar hasta que Mario lo solicite.

Todos los horarios corresponden a **Colombia**, zona `America/Bogota` (UTC−5).

| Encuentro | Grupo | Horario | Enlace de Teams |
|---|---|---|---|
| Clase 23 · Introducción a la Programación | 02CIVIL | 9:00–11:00 a. m. | https://teams.microsoft.com/meet/271941027693903?p=gOhUIeFDUP6dyKhkFe |
| Clase 26 · Introducción a la Programación | 01CIVIL | 11:00 a. m.–1:00 p. m. | https://teams.microsoft.com/meet/240303568231638?p=oY54dOaZZmGOk0G0dG |

Espacio académico: **Introducción a la Programación**, código **11377**. Modalidad: encuentros sincrónicos en Microsoft Teams.

## Cuando Mario pida «poner el link de las 9»

1. En `app.py`, cambiar `MOSTRAR_ACCESO_CLASE = False` a `True`.
2. Comprobar que aparece el acceso después de la carta del docente, con el grupo y horario correctos.
3. Hacer commit de los archivos necesarios y push a `main`, como solicita Mario, para que Streamlit despliegue el cambio.

La carta del docente tiene su propio interruptor, `MOSTRAR_CIERRE_DOCENTE`.

## Cambio a la segunda clase

`encuentros.py` selecciona el primer enlace **antes del 19 de noviembre de 2026 a las 10:59 a. m.** y el segundo **a partir de ese momento**. También cambian el título, el grupo y el horario del botón.

El acceso comprueba la hora cada **15 segundos** mientras la página está abierta y activa. Una página recién cargada selecciona el enlace correspondiente a la hora actual. El cambio horario está programado en la aplicación y **no necesita otro commit ni push a las 10:59**. Una pestaña suspendida por el navegador puede necesitar recargarse al volver a ella.

### Alerta visual dentro de la aplicación

Con el acceso a clase activado, aparece una alerta junto al botón:

- **10:54–10:58:59 a. m.:** aviso con los minutos que faltan para cambiar al grupo 01CIVIL.
- **10:59–11:01:59 a. m.:** confirmación de que el acceso ya corresponde a la clase 26 del grupo 01CIVIL.

Se actualiza cada 15 segundos mientras la página está abierta y activa. Es una alerta visual, sin sonido ni notificaciones del sistema; no avisa con la página cerrada. Si la pestaña queda suspendida, se debe recargar al volver.

No hay una alarma externa ni una tarea de Git programada. La activación inicial requiere la petición de Mario y el despliegue. Después de la segunda clase, el segundo enlace sigue seleccionado hasta que se oculte el acceso o se cambie esta programación.

## Ocultar el acceso al terminar

Cambiar `MOSTRAR_ACCESO_CLASE = False` y publicar el cambio cuando Mario lo solicite.

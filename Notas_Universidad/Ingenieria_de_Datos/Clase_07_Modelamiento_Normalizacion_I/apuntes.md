# Clase 07: Modelamiento de Datos en la Empresa: Normalización (Parte I)

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Introducción a la Normalización de Bases de Datos

La normalización es un proceso crucial en el diseño de bases de datos relacionales, cuyo objetivo principal es eliminar redundancias e inconsistencias de dependencia. Un buen diseño de base de datos asegura que la información se almacena de manera eficiente y lógica, facilitando su comprensión, ampliación y mantenimiento. Es fundamental para sistemas de gestión de bases de datos (DBMS) como MySQL u Oracle.

### Formalización Cero

Una tabla se encuentra en "Formalización Cero" cuando no se ha aplicado ninguna regla de normalización. Esto típicamente resulta en:
*   **Redundancia de datos:** Información repetida en múltiples filas o columnas.
*   **Inconsistencias:** Dificultad para mantener la integridad de los datos debido a la repetición.
*   **Problemas de actualización:** Modificar un dato puede requerir cambios en múltiples lugares.
*   **Ejemplo:** Una tabla `usuarios` con campos `nombre`, `empresa`, `direccion_empresa`, `url1`, `url2`. Si un usuario tiene múltiples URLs, se añaden columnas, lo que es ineficiente y no escalable.

### Primera Forma Normal (1FN)

La Primera Forma Normal busca eliminar grupos repetitivos de datos en las tablas individuales.
**Reglas:**
1.  Eliminar todos los atributos o grupos de atributos repetidos de las tablas.
2.  Crear una tabla separada para cada grupo de datos relacionados.
3.  Identificar cada grupo de datos relacionados con una clave primaria.
**Objetivo:** Asegurar que cada celda de la tabla contenga un único valor atómico y que no haya columnas repetitivas.
**Ejemplo:** La tabla `usuarios` anterior se descompone en `usuarios` (con `userId`, `nombre`, `empresaId`, `direccion_empresaId`) y `urls` (con `urlId`, `relUserId`, `url`), eliminando `url1` y `url2` de la tabla `usuarios`.

### Segunda Forma Normal (2FN)

La Segunda Forma Normal se aplica a tablas que ya están en 1FN. Se enfoca en eliminar dependencias parciales de atributos no clave en partes de la clave primaria compuesta.
**Reglas:**
1.  Crear tablas separadas para aquellos grupos de datos que se aplican a varios registros.
2.  Relacionar estas tablas mediante una clave externa.
**Objetivo:** Asegurar que todos los atributos no clave dependan completamente de toda la clave primaria. Esto es relevante cuando la clave primaria es compuesta.
**Ejemplo:** En el ejemplo de la tabla `usuarios` del 1FN, si `empresa` y `direccion_empresa` se duplican para cada `userId` asociado a la misma empresa, separamos esto en una tabla `empresas` (`emprId`, `empresa`, `direccion_empresa`) y `usuarios` (`userId`, `nombre`, `relEmpresaId`).

### Tercera Forma Normal (3FN)

La Tercera Forma Normal se aplica a tablas que están en 2FN. Elimina atributos que no dependen directamente de la clave primaria, sino de otro atributo no clave (dependencia transitiva).
**Reglas:**
1.  Eliminar aquellos campos que no dependan directamente de la clave primaria (es decir, eliminar dependencias transitivas).
**Objetivo:** Asegurar que todos los atributos no clave dependen única y directamente de la clave primaria, eliminando redundancia y anomalías de actualización.
**Ejemplo:** La estructura de `usuarios`, `empresas`, `urls` (después de 2FN) cumple con 3FN si los atributos de `empresas` (`empresa`, `direccion_empresa`) solo dependen de `emprId`, y los atributos de `urls` (`url`) solo dependen de `urlId`.

---

## Pistas y Keywords

*   **Normalización BD:** Proceso de organización de datos para reducir redundancia e inconsistencias.
*   **Redundancia:** Datos repetidos, causa anomalías.
*   **Inconsistencia:** Datos diferentes para la misma entidad.
*   **1FN:** Atomicidad de datos, eliminación de grupos repetitivos.
*   **Clave Primaria:** Identificador único de una fila.
*   **Clave Externa:** Enlace entre tablas, referencia a una clave primaria.
*   **2FN:** Eliminación de dependencias parciales (para claves compuestas).
*   **3FN:** Eliminación de dependencias transitivas.
*   **Dependencia Funcional:** Atributo Y depende funcionalmente de X si X determina Y.

---

## Resumen Final Crítico

La normalización en bases de datos es un pilar fundamental para construir sistemas robustos y eficientes. La Formalización Cero representa un estado inicial desordenado. La Primera Forma Normal (1FN) aborda la atomicidad de los datos y la eliminación de repeticiones de grupos de valores. La Segunda Forma Normal (2FN) se ocupa de las dependencias parciales, asegurando que los atributos no clave dependan de toda la clave primaria. Finalmente, la Tercera Forma Normal (3FN) elimina las dependencias transitivas, garantizando que todos los atributos no clave dependen directamente de la clave primaria. Dominar estas tres formas es esencial para un diseño de base de datos que minimice problemas de redundancia, actualización y borrado.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Este tema se basa directamente en los fundamentos de Bases de Datos Relacionales (Clase 03) y la administración de RDBMS (Clase 04), donde se establecieron los conceptos de tablas, claves y relaciones. El modelamiento de datos introducido en clases previas se refina con las reglas de normalización.
*   **Conexiones Siguientes:** La aplicación práctica de la normalización será evidente en el diseño de esquemas de bases de datos para proyectos y en la comprensión de consultas DML (Clase 05) y consultas avanzadas (Clase 10 y 11), ya que un esquema bien normalizado facilita operaciones de inserción, actualización y recuperación de datos. Los conceptos de normalización avanzados se explorarán en la Clase 09.

# Clase 2.02: Tipos de Datos Tácticos y Constraints Avanzados

**Instructor:** Principal Data Architect & Senior DBA

## 1. Teoría de Alto Nivel: Dile Adiós al VARCHAR

En el material antiguo de 2013 (`NormalizacioBD.pdf` y `Practica_03_Sol.pdf`), veíamos el uso masivo de `VARCHAR2(50)` o `CHAR(10)` heredado fuertemente de Oracle y SQL Server.

Hoy, para ser un Data Architect especializado en PostgreSQL 15+, la selección de tipos de datos es una decisión de arquitectura de sistemas que impacta el almacenamiento, la observabilidad, la integridad legal, y la partición de grandes volúmenes.

### A. TEXT sobre VARCHAR

En PostgreSQL, bajo el capó (internals), el tipo `VARCHAR(n)` y `TEXT` son idénticos. No hay ventaja de rendimiento al usar `VARCHAR(50)`, tu única ventaja es que Postgres añadirá silenciosamente un `CHECK (length(col) <= 50)`.
En la actualidad, si no necesitas limitar un tamaño por requerimiento de UX estricto, usamos `TEXT`. ¿Por qué? Porque si mañana el negocio dicta que el `titulodistri` de la película ya no dura 50 caracteres sino 70, un `ALTER TABLE pelicula ALTER COLUMN titulodistri TYPE VARCHAR(70)` requerirá (dependiendo de tu versión/herramienta) modificar catálogos y crear puntos de fallo.

### B. El Reinado del JSONB

Los 2010s fueron la era del esquema rígido vs esquema libre (MongoDB). En los 2020s, Postgres unificó ambos con `JSONB`.

- A diferencia del antiguo tipo `JSON`, `JSONB` almacena un formato analizado binario de tu documento.
- **Permite Indexación Nativa:** Puedes usar un índice GIN en tu campo de JSONB, y consultar "buscame los tickets que dentro de su campo 'metadata' tengan una key llamada 'resolution_state' = 'open'" a velocidades extremas.
- Esto elimina la necesidad de crear tablas adicionales con estructura Clave-Valor estilo EAV (Entity Attribute Value), mejorando el rendimiento masivamente en lectura.

### C. Identificadores: De `SERIAL` al `UUID v7`

El documento de la universidad sugería identificadores autonuméricos (`ID`). Sin embargo, en arquitecturas distribuidas y microservicios, depender de la base de datos para generar IDs crea cuellos de botella y problemas de Seguridad (Los UUIDs secuenciales son predecibles y permiten el "Ataque de Enumeración de IDs").

- Usamos **UUID (_Universally Unique Identifier_)**. Pero no cualquier UUID.
- **UUID v4 (Anti-patrón):** Genera entropía totalmente aleatoria. Al ser insertado masivamente en tu Índice (B-Tree), destruye el almacenamiento. Causará miles de "Page Splits" en disco y tu caché se evaporará.
- **UUID v7 (2026):** Son UUIDs que incluyen un prefijo temporal (Time-Sorted). Son ordenables cronológicamente y aseguran inserciones secuenciales rápidas en el disco (Sequential I/O), pero ocultando la cantidad de tus clientes.

## 2. Integración SDLC: Constraints más allá del DDL básico

El 90% de los errores de datos ocurren porque la aplicación (Backend) hace la validación en el código (Node/Java/Go). Pero una base de datos puede tener múltiples clientes o ser tocada por scripts manuales.
La integridad de datos siempre debe estar garantizada por el motor a través de _Constraints_ estrictos.

**Limitaciones Antiguas:**
Conocías el `PRIMARY KEY`, el `FOREIGN KEY`, y quizás `UNIQUE`.

**Las Herramientas Modernas:**

- **EXCLUDE Constraints:** ¿Cómo evitas en la tabla `Funcion` de `Practica_03_Sol.pdf` que dos películas en la misma `Sala` se sobrepongan en horario? Si lo haces en el Backend, hay condiciones de carrera (_Race Conditions_). En PostgreSQL lo resuelves a nivel de disco con una restricción de exclusión utilizando el tipo de dato `DATERANGE` o `TSRANGE`, y el motor te garantiza que dos rangos de horas para una misma sala nunca se crucen.

## 3. Reto de Modernización Táctica (Laboratorio)

Revisemos parcialmente un extracto de diseño de tu `Practica_03_Sol.pdf` original (Modelo de Datos de 2013) sobre una tabla de `Clasificacion` de películas.

Imagina que tienes esta tabla hoy en la que almacenas la película y atributos no estructurados que cambian por cada país:

```sql
CREATE TABLE distribucion_pelicula (
    id SERIAL PRIMARY KEY,
    id_pelicula INT REFERENCES pelicula(id),
    pais VARCHAR(50),
    clasificacion_edad VARCHAR(5),
    restricciones_audiencia TEXT, -- ej. "Contains violence, strobe lights"
    censurada BOOLEAN
);
```

Este es un diseño monolítico que requerirá hacer un `ALTER TABLE` si mañana necesitas almacenar si exige "Verificación de Edad en ID para Taquilla".

**El Reto:**
Reescribe (mentalmente o en tu respuesta) esta estructura para un microservicio escalable de streaming en 2026.
Toma en consideración que:

1. Necesitas IDs seguros que generará tu aplicación de microservicios.
2. Quieres almacenar toda la compleja (y variante) metadata de restricciones del país en una sola columna dinámica pero indexable.
3. El nombre del país es dinámico, y ya no quieres lidiar con el límite de VARCHAR(50).

¿Cómo se vería tu nuevo DDL en PostgreSQL?

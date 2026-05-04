# Clase 2.04: Taller: Refactorización DDL/DML

**Instructor:** Principal Data Architect & Senior DBA

## 1. El Pasado: Modelo de Cine Complejo "Práctica Calificada #3" (2013)

Vamos a tomar el caso de tu evaluación antigua "Practica Calificada #3" (Gestión de Cine: `Pelicula`, `Director_Pelicula`, `Clasificacion`, `Actor_Pelicula`, `Cartelera`, `Semana`, etc.).

En ese momento, se diseñaba asumiendo tipos de datos primitivos (`INT`, `VARCHAR`) y llaves subrogadas triviales, forzando un esquema altamente esparcido.

Por ejemplo, teníamos tablas de intersección para "Categoría" y "Género" de la película. Si hoy lo pasamos a un `DDL` heredado en Postgres se vería así:

```sql
CREATE TABLE pelicula (
    idpelicula INT PRIMARY KEY,
    idcategoria INT REFERENCES categoria(idcategoria),
    ididioma INT REFERENCES idioma(ididioma),
    idgenero INT REFERENCES genero(idgenero),
    ficha VARCHAR(50),
    titulodistri VARCHAR(100),
    tituloorig VARCHAR(100),
    fechaestreno DATE,
    duracion NUMBER
);
```

### Consultas Problemáticas del 2013

En esa misma práctica se te pedía: "Mostrar la cantidad de películas por categoría que ha participado el actor Charlton Heston".
Esto forzaba un `JOIN` de 4 tablas por consulta (Pelicula -> Categoria -> Actor_Pelicula -> Actor).

Otro caso crítico fue la **Consulta 10**: `SELECT ... FROM BPMPORTA.HISTORICO_JBPM_TASKINSTANCE ... WHERE ID_=2096`. El EXPLAIN reportaba un infame `TABLE ACCESS FULL` con un coste astronómico porque se leía cada bloque del disco buscando el `ID_=2096`.

Tu solución dictada en clase fue añadir un índice:
`CREATE INDEX IDX_BPMPORTA.HISTORICO_JBPM... ON ... (ID_)`

## 2. El Presente: DDL Transaccional Moderno (2026)

Hoy no "parchamos" lentitud con un índice tras ver caer el sistema; **diseñamos pensando en la velocidad de lectura nativa o el Event Sourcing**.

Rediseñemos esa tabla `pelicula` y sus intersecciones (actor/director) de la Práctica 3 usando el armamento de PostgreSQL 15+. Eliminaremos la pesadilla de hacer `JOINs` para cada metadato (como idiomas o actores "de reparto" que solo se consultan al abrir la página web detallada de la película).

```sql
-- Uso de UUID v7 (generado por la app) en lugar de IDs auto incrementables vulnerables y fragmentadores
CREATE TABLE pelicula (
    id UUID PRIMARY KEY,

    -- Manejamos Text sin límites restrictivos perjudiciales
    titulo_distribucion TEXT NOT NULL,
    titulo_original TEXT,

    -- Datos temporales con zonas horarias
    fecha_estreno TIMESTAMPTZ,
    duracion_minutos INTEGER CHECK (duracion_minutos > 0 AND duracion_minutos < 1000),

    -- Reducción de JOINs (Desnormalización Controlada en JSONB):
    -- Por qué unir 4 tablas para listar al director y sus actores principales si el Streaming asume esto como Metadata no relacionable externamente
    metadata_creditos JSONB,

    -- Optimizando idiomas mediante ARRAYS nativos y Tipos Enumerados (ENUM)
    -- en vez de crear tablas de maestro/detalle 'idioma' para códigos estándar ISO
    idiomas_audio TEXT[] NOT NULL DEFAULT '{}',
    idiomas_subtitulos TEXT[] NOT NULL DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Indexando el interior del JSONB (Fast Search para buscar actores)
CREATE INDEX idx_pelicula_creditos_gin
ON pelicula USING GIN (metadata_creditos);
```

## 3. Reto Técnico de Refactorización (Final de Fase 2)

Observa el código SQL Moderno que acabo de crear para `Pelicula`. El viejo motor relacional de 2013 fue evolucionado a un híbrido (Relacional/NoSQL) gracias al campo `jsonb` y los campos de arreglos de texto `TEXT[]`.

La pregunta de la universidad decía: "Mostrar un reporte donde se visualice la cantidad de películas por categoría que ha participado el actor Charlton Heston".

**El Reto:**
Si el nombre completo del actor vive dentro de tu campo `metadata_creditos` como un arreglo JSON de strings (`["actor1", "actor2"]`), invéstigame qué **Operador Especial en PostgreSQL para el tipo JSONB o Vectores de Texto** existe para encontrar instantáneamente los registros que contienen 'Charlton Heston' SIN hacer uso del clásico operador relacional de texto `LIKE '%Heston%'` que provocaría un _Full Table Scan_ e ignoraría nuestro índice `GIN`.

_(Responde el operador o escribe el "WHERE metadata_creditos ... " simulado)._

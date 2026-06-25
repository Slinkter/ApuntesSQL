# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Que es este repositorio

ApuntesSQL — un repositorio personal de estudio sobre PostgreSQL y teoria relacional. Es **100% documental** (Markdown + HTML estatico + scripts SQL). **No hay sistema de build, ni test runner, ni linter, ni codigo de aplicacion en produccion**. No hay `package.json`, ni `requirements.txt`, ni matriz de CI mas alla del workflow de Copilot en `.github/workflows/copilot-setup-steps.yml`.

Conviven dos pistas paralelas:

- **`ULima/Apuntes/`** — Sitio del curso universitario de 16 semanas (HTML estilo Cornell, `semana_01.html` … `semana_16.html`, con `index.html` como dashboard y `master.css` + `canvas-ui.js` como assets compartidos).
- **`Lab/`** — Material moderno de laboratorio PostgreSQL con SQL ejecutable, dataset y docker-compose (referido en documentacion antigua como `SQL/` o `PostgresSQL/`; la ruta real en disco es `Lab/Lab01/` para apuntes + dataset y `Lab/Lab02/Taller/` para el taller).

Si necesitas hacer cambios, **verifica siempre la ruta en disco antes de editar** — la documentacion antigua y el workflow de GitHub hacen referencia a `PostgresSQL/`, pero ese directorio no existe en este repo. Las ubicaciones reales son `Lab/Lab01/Ejercicios/` y `Lab/Lab02/Taller/`.

## Comandos esenciales

No hay `make`, `npm test` ni comandos de lint. Los comandos accionables son:

### Levantar el laboratorio Postgres local

```bash
# Iniciar Postgres via docker-compose (pista Lab)
docker compose -f "Lab/Lab02/Taller/docker-compose/Postgres/docker-compose.yaml" up -d

# Variante alternativa de entorno (misma idea, distinto nombre)
docker compose -f "Lab/Lab02/Taller/docker-compose/Postgresenv/docker-compose.yaml" up -d

# Verificar que el contenedor arranco
docker logs -f docker_postgres_local   # nombre de contenedor desde el YAML
```

El archivo compose crea la base de datos `ecommerce` con usuario `admin`/`admin123` en el puerto `5432`. **No** carga automaticamente el dataset Northwind.

### Cargar el dataset Northwind

```bash
# Despues de que el contenedor este arriba, crear + cargar northwind manualmente:
psql -h localhost -U admin -d postgres -c "CREATE DATABASE northwind;"
psql -h localhost -U admin -d northwind -f Lab/Lab01/Ejercicios/db_northwind.sql
```

(Ajusta usuario/contrasena segun el compose que levantaste.)

### Ejecutar un solo ejercicio SQL

No hay test runner — "ejecutar un ejercicio" significa correr el bloque SQL embebido. El patron es:

```bash
psql -h localhost -U admin -d northwind -c "<pega aqui la consulta>"
# o leer desde un archivo:
psql -h localhost -U admin -d northwind -f Lab/Lab02/sql/sql1.sql
```

### Servir el sitio HTML de ULima en local

```bash
npx http-server ULima/Apuntes -p 3000 -c-1
# luego abre http://localhost:3000
```

El workflow de Copilot hace exactamente esto en CI.

## Arquitectura de alto nivel

### `ULima/Apuntes/` — Sitio del curso (metodo Cornell)

- `index.html` — dashboard con 16 tarjetas semanales y 2 tarjetas de examen (semana_08, semana_16).
- `semana_01.html` … `semana_07.html` — Fundamentos (DBMS, modelo relacional, DDL, DML, ER, normalizacion).
- `semana_08.html` — Examen parcial tipo (4 secciones + solucionario).
- `semana_09.html` … `semana_15.html` — Topicos avanzados (BCNF/4FN/5FN, JOINs, GROUP BY, PL/pgSQL, triggers, DW, HA).
- `semana_16.html` — Examen final tipo (4 secciones + solucionario).
- `extra_*.html` (8 archivos) — Contenido complementario legacy; **usa intencionalmente clases CSS antiguas que no estan en `master.css`** (ver `prompt.md` Fase 4 Puntos de atencion).
- `master.css` — Hoja de estilos unica, metodologia BEM. Variables CSS para la paleta navy/slate/azul-PostgreSQL.
- `canvas-ui.js` — Pizarra de dibujo interactiva embebida en cada `semana_*.html`.

Reglas estrictas en `semana_*.html`: cero emojis en HTML, cero clases CSS legacy (`header-box`, `cornell-container`, `keywords-sidebar`, etc.), cero estilos inline excepto el minimo indispensable en los recursos del sidebar, UTF-8 sin `�`.

### `Lab/` — Laboratorio PostgreSQL

- `Lab/Lab01/Ejercicios/`
  - `0.prerrequisitos.md` — Guia de entorno (Docker, variables de entorno, carga del dataset, intro a `EXPLAIN ANALYZE`).
  - `1.basico.md`, `2.intermedio.md`, `3.avanzado.md` — 150 ejercicios en total, ordenados basico → intermedio → avanzado. Cada ejercicio: pregunta de negocio, marco conceptual, diagrama de flujo en Mermaid, SQL ejecutable.
  - `db_northwind.sql` — Dataset canonico. **NO agregues sentencias `DROP DATABASE` / `CREATE DATABASE`** — el mecanismo de inicializacion del laboratorio espera un script solo con el dataset (ver `.github/copilot-instructions.md`).
- `Lab/Lab02/`
  - `Taller/docker-compose/{Postgres,Postgresenv,MySQL,MySQLenv}/docker-compose.yaml` — Archivos compose listos para usar.
  - `Taller/Guia/` — Guias paso a paso con imagenes (`01.jpg`…`07.jpg`).
  - `Taller/Tipos-Join/` — Diagramas de tipos de JOIN.
  - `Taller/ejemplo{1,2,3}-*.sql` — Ejemplos por dominio (cine, videojuegos, restaurantes).
  - `sql/sql1.sql` — Scripts SQL sueltos.

### `Credenciales/`

Guia de despliegue en AWS + credenciales de ejemplo. Contiene `key_u_docker.pem` y archivos `*.csv` con claves de acceso — **no commitees credenciales adicionales aqui**; esto ya es la excepcion canonica. Incluye `Guia_Despliegue_Docker_AWS.md` (Postgres en AWS EC2 via Docker) y capturas de pantalla.

### Archivos de documentacion raiz

- `README.md` — Punto de entrada en espanol, estructura del proyecto, comandos de inicio rapido, convenciones SQL.
- `GEMINI.md` — Vision del proyecto y plan de maestria de 16 semanas; stack tecnologico (Postgres 15+, SQL ANSI 2023, PL/pgSQL, Markdown + Mermaid).
- `AGENTS.md` — Guia concisa para agentes; refleja las convenciones de `prompt.md`.
- `prompt.md` — **El prompt de la persona IA ArquiDB.** Leer antes de cualquier trabajo de auditoria/refactorizacion.

## Convenciones PostgreSQL (aplican al editar cualquier `.md` o `.sql`)

Estas reglas se repiten en `prompt.md`, `GEMINI.md`, `README.md`, `AGENTS.md` y `.github/copilot-instructions.md` — son criticas para este repo:

- **Target**: PostgreSQL 15+. Marca explicitamente cualquier feature v16+.
- **Postgres idiomatico**: prefiere `RETURNING`, `ON CONFLICT` (Upsert), `JSONB` (no `JSON`), `SERIAL`/`BIGSERIAL` (o `UUID v7` para IDs no secuenciales).
- **Rendimiento**: cada consulta clave debe incluir `EXPLAIN (ANALYZE, BUFFERS)` con una interpretacion breve de I/O y costo del planner.
- **DML seguro**: `UPDATE`/`DELETE` destructivos envueltos en `BEGIN; EXPLAIN ANALYZE <DML>; ROLLBACK;` (commit solo tras verificacion manual).
- **Diagramas**: usa Mermaid (`flowchart`, `erDiagram`) para ER y flujos de datos.
- **Seguridad**: RLS, constraints correctos (`CHECK`, `FK`, `UNIQUE`), marcar funciones PL/pgSQL con `IMMUTABLE`/`STABLE`/`VOLATILE` segun corresponda.
- **Indexacion**: B-tree, GIN, GiST, BRIN — nombra la correcta para cada carga de trabajo.

## Formato de auditoria ArquiDB (de `prompt.md`)

Cuando revises o refactorices SQL/HTML, adopta la persona y el formato de informe de `prompt.md`:

```
📄 archivo: ruta/archivo
Estado: ✅ CORRECTO | ⚠️ ADVERTENCIA | ❌ INCORRECTO

Cambios recomendados (priorizados):
1. [linea o seccion] descripcion + snippet corregido
2. [linea o seccion] descripcion + snippet corregido
```

Una recomendacion accionable por item. Cuando muestres codigo legado incorrecto (ej. Oracle `VARCHAR2`), incluye el equivalente Postgres.

## Archivos a leer primero al empezar a trabajar

1. `README.md` — entrada del proyecto e inicio rapido.
2. `prompt.md` — persona ArquiDB, formato de auditoria, historial de fases de refactorizacion.
3. `GEMINI.md` — mision, stack, resumen de convenciones.
4. `AGENTS.md` — reglas cortas para agentes.
5. `.github/copilot-instructions.md` — guia especifica para Copilot (se solapa en gran parte con lo anterior).
6. `Credenciales/Guia_Despliegue_Docker_AWS.md` — referencia canonica de docker-compose + despliegue en AWS EC2.
7. `Lab/Lab01/Ejercicios/0.prerrequisitos.md` — configuracion del laboratorio local.

## Al editar contenido

- Verifica las rutas en disco antes de cambiar nada; la documentacion antigua referencia `SQL/Youtube00/` y `SQL/Youtube01/` pero esos directorios no existen. Las rutas reales estan bajo `Lab/`.
- No agregues `DROP DATABASE` / `CREATE DATABASE` a `Lab/Lab01/Ejercicios/db_northwind.sql` — lo consume `docker-entrypoint-initdb.d/` y debe seguir siendo solo un script de dataset.
- Para cambios HTML bajo `ULima/Apuntes/`: mantente dentro del vocabulario BEM de `master.css`. No introduzcas clases legacy (`header-box`, `cornell-container`, etc.) en `semana_*.html`. Los archivos `extra_*.html` estan exentos por diseno (complemento legacy).
- Sin emojis en `semana_*.html`; usa etiquetas textuales (`"Nota:"`, `"Importante:"`, `"Ejemplo:"`).
- Si modificas archivos Docker Compose, actualiza `Credenciales/Guia_Despliegue_Docker_AWS.md` para mantener sincronizados los nombres de contenedores y rutas.
- Espanol, tono de mentor/tutor; los archivos existentes son la referencia de estilo.

## CI / automatizacion de Copilot

Solo existe un workflow: `.github/workflows/copilot-setup-steps.yml`. Descarga `postgres:16-alpine`, siembra `northwind` desde `PostgresSQL/db_northwind.sql` (la ruta esta obsoleta — apunta a un directorio que no existe; si reactivas este workflow, corrige la ruta a `Lab/Lab01/Ejercicios/db_northwind.sql`), sirve `ULima/Apuntes` via `http-server` en el puerto 3000 e instala Playwright. Solo se dispara con push a si mismo o `workflow_dispatch` manual.

Si agregas tests, lint o cualquier paso de build, documenta los comandos aqui — aun no hay convencion y nada correra automaticamente.
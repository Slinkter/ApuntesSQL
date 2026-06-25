# ApuntesSQL — Agent guide

## What this is

Notas de estudio personales sobre SQL/PostgreSQL. Repositorio 100% documental (Markdown + HTML estático). No hay build system, pruebas, CI, ni dependencias de lenguaje.

## Content tracks

| Path | Content |
|------|---------|
| `SQL/1.basico.md`, `SQL/2.intermedio.md` | Refactored PostgreSQL notes with query internals, `EXPLAIN ANALYZE`, Mermaid flowcharts |
| `SQL/Youtube00/` | Tutorial series: básico → intermedio → avanzado + `db_northwind.sql` |
| `SQL/Youtube01/Taller/` | Workshop exercises with runnable SQL examples and docker-compose |
| `ULima/Apuntes/` | Legacy university HTML pages (Cornell-style), 16-week syllabus |
| `Credenciales/Guia_Despliegue_Docker_AWS.md` | End-to-end AWS EC2 + Docker deployment guide |

## Key files

- `GEMINI.md` — project vision and 16-week mastery plan
- `prompt.md` — "ArquiDB" AI auditor persona prompt (quality review standards)
- `SQL/Youtube00/db_northwind.sql` — main dataset (Northwind for PostgreSQL)
- `SQL/Youtube01/Taller/docker-compose/` — ready-to-use docker-compose files for Postgres and MySQL

## Quick start (local)

```bash
# PostgreSQL via docker-compose
docker compose -f "SQL/Youtube01/Taller/docker-compose/Postgres/docker-compose.yaml" up -d

# Load Northwind dataset
psql -h localhost -U postgres -d northwind -f SQL/Youtube00/db_northwind.sql

# Run a query
psql -h localhost -U postgres -d northwind -c "SELECT ..."
```

## PostgreSQL conventions (from prompt.md)

- Prefer PostgreSQL idioms: `RETURNING`, `ON CONFLICT`, JSONB operators, `SERIAL`/`BIGSERIAL`
- Include `EXPLAIN (ANALYZE, BUFFERS)` on key queries
- Wrap destructive DML in `BEGIN; EXPLAIN ANALYZE <DML>; ROLLBACK;`
- Target PostgreSQL 15+; note v16+ features explicitly
- Use Mermaid for ER/flow diagrams

## Content style

- Spanish, tutorial/mentor tone
- Files are standalone Markdown with embedded SQL and Mermaid
- No codegen, no build step, no formatter — just source files

## OCR workflow (added 2026-06-25)

Use Ollama + GLM-OCR for PDF→TXT transcription when needed. See `prompt.md` Fase 1b for the full workflow.


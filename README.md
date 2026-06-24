# ApuntesSQL

Notas de estudio personales sobre SQL/PostgreSQL. Repositorio 100% documental (Markdown + HTML estático).

## Content tracks

| Path | Content |
|------|---------|
| `SQL/1.basico.md`, `SQL/2.intermedio.md` | Refactored PostgreSQL notes con `EXPLAIN ANALYZE` y diagramas Mermaid |
| `SQL/Youtube00/` | Tutorial series: básico → intermedio → avanzado + `db_northwind.sql` |
| `SQL/Youtube01/Taller/` | Workshop exercises con ejemplos SQL ejecutables y docker-compose |
| `ULima/Apuntes/` | Apuntes universitarios legacy (HTML estilo Cornell), temario 16 semanas |
| `Credenciales/` | Guía de despliegue AWS EC2 + Docker |

## Quick start (local)

```bash
# PostgreSQL via docker-compose
docker compose -f "SQL/Youtube01/Taller/docker-compose/Postgres/docker-compose.yaml" up -d

# Cargar dataset Northwind
psql -h localhost -U postgres -d northwind -f SQL/Youtube00/db_northwind.sql

# Ejecutar una consulta
psql -h localhost -U postgres -d northwind -c "SELECT version();"
```

## Convenciones PostgreSQL

- Preferir `RETURNING`, `ON CONFLICT`, operadores JSONB, `SERIAL`/`BIGSERIAL`
- Incluir `EXPLAIN (ANALYZE, BUFFERS)` en queries clave
- Envolver DML destructivo en `BEGIN; EXPLAIN ANALYZE <DML>; ROLLBACK;`
- Target: PostgreSQL 15+
- Diagramas con Mermaid

# Copilot instructions for ApuntesSQL

Purpose: provide repository-specific guidance for future Copilot/Copilot CLI sessions.

## Quick commands (actual, repo-specific)
- No formal build/test/lint scripts exist (this repo is documentation, SQL and HTML).
- Docker-based lab (recommended):
  - Start lab (creates a Postgres instance and runs init SQL):
    - From PostgresSQL/Youtube01/Taller/docker-compose or PostgresSQL/Youtube01/Taller/docker-compose/Postgresenv:
      - `docker compose up -d`
      - Verify init logs: `docker logs -f pg_architect_lab` (container name defined in Credenciales/Guia_Despliegue_Docker_AWS.md)
  - Connect to DB inside container: `docker exec -it pg_architect_lab psql -U slinkter -d northwind`
  - Connect remotely (if SG/ports open): `psql -h <host> -U slinkter -d northwind`

Notes: there are no unit test runners or linters configured. If adding tests, document how to run a single test.

## High-level architecture
- ULima/: primary teaching material (HTML, indexed in ULima/Apuntes/index.html). These are the course notebooks and slides (weekly "semana_*.html").
- PostgresSQL/: lab guides and the `db_northwind.sql` dataset used for hands-on exercises.
- Credenciales/: deployment and infrastructure guides (includes `Guia_Despliegue_Docker_AWS.md`) and example Docker Compose YAMLs.

Overall repo intent: educational material + reproducible labs for PostgreSQL (v15+), not a typical application codebase.

## Key conventions and repo-specific rules
- db_northwind.sql is a canonical dataset (PostgresSQL/db_northwind.sql). It is pre-corrected: do NOT add `DROP DATABASE` / `CREATE DATABASE` lines — the init mechanism expects a dataset-only script.
- Docker initialization: lab workflows rely on mapping SQL into `/docker-entrypoint-initdb.d/` so the database is created automatically on first container start. See Credenciales/Guia_Despliegue_Docker_AWS.md for exact YAML examples.
- SQL style & pedagogy:
  - Prefer `JSONB` over `JSON` when storing semi-structured data.
  - Use `SERIAL`/`BIGSERIAL` for simple sequential IDs (or `UUID v7` if non-sequential IDs required).
  - When adding or changing SQL examples, include `EXPLAIN ANALYZE` snippets to discuss I/O and planner impact.
- Frontend notes: ULima/Apuntes uses a Cornell-style HTML layout and a shared `master.css`. The repo includes notes to apply BEM-style improvements for weekly files (see prompt.md comments).

## AI / Assistant guidance (must-read files)
- prompt.md: repository-level AI persona and audit checklist (ArquiDB). When Copilot is asked to audit or refactor SQL/HTML:
  - Adopt the ArquiDB persona: technical, mentoring, and checklist-driven.
  - Use the audit report format: `📄 archivo: <name>` then status `✅ / ⚠️ / ❌` and a short numbered list of changes with line references and corrected SQL example(s).
- GEMINI.md: project purpose, high-level plan, and conventions (JSONB preference, SERIAL vs UUID guidance, EXPLAIN_ANALYZE requirement). Incorporate its rules when updating content.

## Files to consult first for context
- README.md — project entry
- prompt.md — AI persona, audit checklist, and reporting format
- GEMINI.md — mission, architecture and conventions summary
- Credenciales/Guia_Despliegue_Docker_AWS.md — docker-compose examples and step-by-step cloud deployment notes
- PostgresSQL/db_northwind.sql — canonical dataset

## When editing content
- Keep examples executable on Postgres v15+; prefer idiomatic Postgres features (`RETURNING`, `ON CONFLICT`, `JSONB` operators).
- If modifying SQL lab scripts, preserve idempotency and ensure initialization assumptions remain (avoid adding DB-level DROP/CREATE unless intent is documented).
- Update `Guia_Despliegue_Docker_AWS.md` if adding or changing Docker Compose files or container names.

## AI assistant behavior checklist (short)
- Read prompt.md and GEMINI.md before making audit/refactor suggestions.
- Provide an audit block per file: file header, status, 1–3 concrete fixes with corrected code snippets, and one-line rationale.
- When proposing infra or docker changes, include exact docker-compose path and `docker compose` commands to validate locally.

---

If this file should include additional automation (CI/test/lint), note the desired tooling (GitHub Actions, pytest, node/npm, shellcheck, sqlfluff) so CI examples can be added.

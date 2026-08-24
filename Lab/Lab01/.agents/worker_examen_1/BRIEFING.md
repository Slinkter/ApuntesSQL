# BRIEFING — 2026-08-22T18:20:00Z

## Mission
Refine and elevate `2.Ejercicios/4.examen_entrevista.md` with 100% canonical Northwind data, exact PostgreSQL 16 outputs (including Pregunta 10 fix: FISSA & PARIS, 2 rows), rigorous 12-step PostgreSQL Logical Execution Order questions, and Senior Data Analyst / Lead Database Engineer rubrics.

## 🔒 My Identity
- Archetype: worker_examen
- Roles: implementer, qa, specialist
- Working directory: C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_examen_1
- Original parent: e5ca8185-8fd7-4a7b-92bf-072321499c97
- Milestone: milestone-1

## 🔒 Key Constraints
- Modify ONLY `2.Ejercicios/4.examen_entrevista.md`.
- No mock data (e.g. no `NWE01`, `NWE02`, no `'Alfreds Futterkiste - Actualizado'`).
- Canonical Northwind DDL execution outputs (PostgreSQL 16).
- All 30 interview questions must have exact ASCII result tables, detailed solutions, and senior/lead engineering rubrics.
- Cover the 12-step PostgreSQL Logical Execution Order deeply.
- Integrity mandate: genuine implementations, real SQL executions, no fake data.

## Current Parent
- Conversation ID: e5ca8185-8fd7-4a7b-92bf-072321499c97
- Updated: 2026-08-22T18:20:00Z

## Task Summary
- **What to build**: Comprehensive rewrite and elevation of `4.examen_entrevista.md` with 30 interview questions spanning Junior to Principal Architect, fixing Q10 (exactly 2 rows: PARIS and FISSA), purging mock records, verifying against live PostgreSQL 16 on canonical Northwind schema, incorporating 12-step engine pipeline traces, and adding Senior/Lead interview rubrics.
- **Success criteria**: 100% executable queries tested on PostgreSQL 16 container (`pg_architect_lab`), zero mock data leaks, complete 6-step analytical mental model per question, clean formatting.
- **Interface contracts**: `PROJECT.md`
- **Code layout**: `2.Ejercicios/4.examen_entrevista.md`

## Key Decisions Made
- Replaced mock entries (`NWE01`, `NWE02`) in Pregunta 10 with exact canonical output (2 rows: `PARIS` and `FISSA`).
- Cleaned `'Alfreds Futterkiste - Actualizado'` back to canonical `'Alfreds Futterkiste'` across all questions (Q1, Q21, Q25).
- Integrated the master 12-step Logical Query Processing Pipeline diagram and identifier visibility matrix in the document header.
- Added "🧠 Cómo Pensar como un Analista de Datos" 6-step reasoning framework to all questions.
- Expanded interview rubrics distinguishing Junior, Mid, Senior, and Lead/Architect responses.
- Added deep production engineering notes: covering indexes with `INCLUDE`, trigram `GIN` indexes for `%text%`, `SELECT ... FOR UPDATE` concurrency control, and Kimball dimensional modeling for `fact_ventas`.

## Artifact Index
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\4.examen_entrevista.md` — Target refined interview file
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_examen_1\handoff.md` — Handoff report

## Change Tracker
- **Files modified**: `2.Ejercicios/4.examen_entrevista.md`
- **Build status**: 30/30 queries passed live execution on PostgreSQL 16
- **Pending issues**: None

## Quality Status
- **Build/test result**: 100% pass (30/30 SQL queries validated)
- **Lint status**: Clean (balanced fences, proper details tags)
- **Tests added/modified**: Automated runner and forensic markdown audit scripts

## Loaded Skills
- **Source**: `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\postgresql-optimization\SKILL.md`
- **Local copy**: `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\postgresql-optimization\SKILL.md`
- **Core methodology**: Advanced PostgreSQL features, window functions, query optimization, EXPLAIN ANALYZE, indexing strategies, CTEs, execution order.

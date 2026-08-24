# BRIEFING — 2026-08-22T18:19:25Z

## Mission
Refine `2.Ejercicios/1.basico.md` and `2.Ejercicios/aws_ejercicio.sql` by fixing syntax bugs, eliminating mock data from ASCII tables to match canonical Northwind, enhancing pedagogical depth with analyst frameworks/analogies/execution order, and validating against live PostgreSQL engine.

## 🔒 My Identity
- Archetype: worker_basico
- Roles: implementer, qa, specialist
- Working directory: C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_basico_1
- Original parent: e5ca8185-8fd7-4a7b-92bf-072321499c97
- Milestone: Refine Basico Exercises & AWS Script

## 🔒 Key Constraints
- Genuine implementations only: no hardcoding, no dummy/facade results, no circumventing.
- Exclusively edit `2.Ejercicios/1.basico.md` and `2.Ejercicios/aws_ejercicio.sql`. Do NOT touch other worker files.
- Metadata goes ONLY in `.agents/worker_basico_1/`.
- All ASCII result tables must reflect real canonical Northwind database states (91 customers, no NWE01/NWE02, no '- Actualizado').
- Clear execution order explanation (FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT).

## Current Parent
- Conversation ID: e5ca8185-8fd7-4a7b-92bf-072321499c97
- Updated: 2026-08-22T18:19:25Z

## Task Summary
- **What to build**: Fix SQL syntax in Exercise 38, clean mock data from all ASCII tables in `1.basico.md`, update row counts, enrich pedagogical quality (mental framework, analogies, execution order), and align `aws_ejercicio.sql`.
- **Success criteria**: 0 syntax errors, 100% canonical Northwind data in ASCII tables, rich pedagogical structure, matching `aws_ejercicio.sql`.
- **Interface contracts**: `PROJECT.md`, `ORIGINAL_REQUEST.md`.
- **Code layout**: `2.Ejercicios/1.basico.md`, `2.Ejercicios/aws_ejercicio.sql`.

## Key Decisions Made
- Exercise 38 syntax bug fixed (`COALESCE(region || ', ', '') || country AS ubicacion_completa`).
- Contaminated string `'Alfreds Futterkiste - Actualizado'` and mock entries cleaned across Exercises 6, 11, 14, 21, 22, 36, 37, 47.
- Row counts in ASCII tables aligned with canonical Northwind database: Ex 14 (60 rows), Ex 21 (21 rows), Ex 22 (21 rows), Ex 37 (91 rows).
- Integrated 6-step "Cómo Pensar como un Analista de Datos" framework, "El Colador y la Lista de Compras" analogy, and PostgreSQL Engine Execution Order visibility matrix.
- Structured `aws_ejercicio.sql` with complete header comments aligned with Exercise 1.

## Artifact Index
- `.agents/worker_basico_1/DISPATCH.md` — Assignment instructions
- `.agents/worker_basico_1/BRIEFING.md` — Working memory
- `.agents/worker_basico_1/progress.md` — Liveness & heartbeat
- `.agents/worker_basico_1/verify_basico.js` — Automated database verification script
- `.agents/worker_basico_1/handoff.md` — Final 5-component handoff

## Change Tracker
- **Files modified**:
  - `2.Ejercicios/1.basico.md`: 50 exercises refined, syntax fixed, mock data removed, pedagogical frameworks integrated.
  - `2.Ejercicios/aws_ejercicio.sql`: Standardized SQL formatting and header documentation.
- **Build status**: PASS (50/50 queries executed successfully against PostgreSQL 16 `pg_architect_lab`).
- **Pending issues**: None.

## Quality Status
- **Build/test result**: PASS — 100% execution fidelity on canonical Northwind.
- **Lint status**: Clean
- **Tests added/modified**: Automated verification test suite `verify_basico.js`.

## Loaded Skills
- **Source**: `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\postgresql-optimization\SKILL.md`
- **Local copy**: `.agents/worker_basico_1/skills/postgresql-optimization/SKILL.md`
- **Core methodology**: PostgreSQL optimization, COALESCE/NULL semantics, query execution order, SARGability.

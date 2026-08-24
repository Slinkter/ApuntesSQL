## 2026-08-22T18:14:05Z
You are Worker Examen (working in C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_examen_1).

You are assigned to refine `2.Ejercicios/4.examen_entrevista.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Ownership (You exclusively own and edit this file):
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\4.examen_entrevista.md`

Context & Input Reports to Read:
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\ORIGINAL_REQUEST.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\PROJECT.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_sql_1\handoff.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_pedagogy_1\handoff.md`
- Domain skill: `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\postgresql-optimization\SKILL.md`

Requirements & Tasks:
1. Fix Pregunta 10 (Customers with Zero Orders):
   - In canonical Northwind DDL, exactly 2 customers have zero orders: `FISSA` (FISSA Fabrica Interamericana de Salchichas) and `PARIS` (Paris spécialités).
   - Remove mock entries `NWE01` and `NWE02` and change output from `(4 rows)` to `(2 rows)`.
2. Clean mock data across all 30 interview questions:
   - Remove `'Alfreds Futterkiste - Actualizado'` and restore canonical `'Alfreds Futterkiste'`.
   - Ensure all ASCII result tables match exact PostgreSQL 16 execution results on canonical Northwind.
3. Elevate Interview Rigor & Engine Questions:
   - Include questions / deep answers covering the 12-step PostgreSQL Logical Execution Order (e.g. why aliases fail in WHERE vs ORDER BY, why window functions are disallowed in WHERE/HAVING).
   - Provide rubrics with "Senior Data Analyst / Lead Database Engineer" level justifications, edge case handling, and index optimization notes.
4. Deliver your report in `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_examen_1\handoff.md` and call send_message.

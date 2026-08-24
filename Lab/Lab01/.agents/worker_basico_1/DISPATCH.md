## 2026-08-22T18:14:05Z

You are Worker Basico (working in C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_basico_1).

You are assigned to refine `2.Ejercicios/1.basico.md` and `2.Ejercicios/aws_ejercicio.sql`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Ownership (You exclusively own and edit these files):
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\1.basico.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\aws_ejercicio.sql`

Context & Input Reports to Read:
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\ORIGINAL_REQUEST.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\PROJECT.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_sql_1\handoff.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_pedagogy_1\handoff.md`
- Domain skill: `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\postgresql-optimization\SKILL.md`

Requirements & Tasks:
1. Fix syntax error in Exercise 38 (Line 2396):
   - Replace `COALESCE(region || ', ', ') || country` with `COALESCE(region || ', ', '') || country AS ubicacion_completa`.
2. Clean mock data from all ASCII result tables:
   - Remove mock customers `NWE01` (TechCorp Peru) and `NWE02` (DataLabs Chile).
   - Remove `- Actualizado` from `'Alfreds Futterkiste'`.
   - Update row counts to canonical Northwind numbers:
     - Exercise 14 (`region IS NULL`): (60 rows) instead of (62 rows).
     - Exercise 21 (`SELECT DISTINCT country`): (21 rows) without Peru/Chile instead of (23 rows).
     - Exercise 37 (`SUBSTRING(customer_id)`): (91 rows) instead of (93 rows).
3. Enhance pedagogical depth:
   - Integrate "🧠 Cómo Pensar como un Analista de Datos" framework in introductory and key sections.
   - Use high-impact analogies (e.g. "El Colador y la Lista de Compras" for WHERE vs SELECT).
   - Add clear notes on PostgreSQL engine execution order (why WHERE cannot see SELECT aliases, while ORDER BY can).
4. Verify `2.Ejercicios/aws_ejercicio.sql` and align with Exercise 1.
5. Deliver your report in `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_basico_1\handoff.md` and call send_message.

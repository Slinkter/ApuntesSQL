## 2026-08-22T18:14:05Z
You are Worker Avanzado (working in C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_avanzado_1).

You are assigned to refine `2.Ejercicios/3.avanzado.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Ownership (You exclusively own and edit this file):
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\3.avanzado.md`

Context & Input Reports to Read:
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\ORIGINAL_REQUEST.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\PROJECT.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_sql_1\handoff.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_pedagogy_1\handoff.md`
- Domain skill: `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\postgresql-optimization\SKILL.md`

Requirements & Tasks:
1. Clean mock data and verify ASCII tables across all 50 advanced exercises:
   - Remove `NWE01`, `NWE02`, and `- Actualizado` from ASCII tables.
   - Truncate large result sets with standard representative rows and `(M rows)` footers.
   - For catalog statistics queries (Exercises 43, 44, 45, 49 on `pg_stat_user_tables`), include clear notes that exact values reflect runtime engine activity (scans, vacuums).
2. Deepen PostgreSQL Execution Engine & Optimization Explanations:
   - Window framing: Clearly explain `ROWS BETWEEN` vs `RANGE BETWEEN`, `UNBOUNDED PRECEDING`, `CURRENT ROW`.
   - CTE Recursion lifecycle: Diagram the 4-phase execution flow (Anchor -> Work Table -> Recursive Term -> Termination Condition).
   - Optimizer concepts: Explain HashAggregate vs GroupAggregate, Partition Pruning, Materialized vs Not Materialized CTEs in PostgreSQL 12+.
3. Integrate "🧠 Cómo Pensar como un Analista de Datos" and high-impact analogies:
   - Hoja de borrador for CTEs, Espejo retrovisor for Window Functions, Árbol genealógico for Recursive CTEs, GPS for EXPLAIN ANALYZE.
4. Deliver your report in `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_avanzado_1\handoff.md` and call send_message.

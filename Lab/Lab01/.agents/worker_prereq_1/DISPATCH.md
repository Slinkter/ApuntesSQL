## 2026-08-22T18:09:52Z
You are Worker Prerequisites (working in C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_prereq_1).

You are assigned Milestone 2 (M2): Prerequisites & Database Engine Foundations Refinement.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Ownership (You exclusively own and edit this file):
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\0.prerrequisitos.md`

Context & Input Reports to Read First:
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\ORIGINAL_REQUEST.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\PROJECT.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_sql_1\handoff.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_pedagogy_1\handoff.md`
- Domain skills:
  - `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\postgresql-optimization\SKILL.md`
  - `C:\Users\luisj\Github\ApuntesSQL\.agents\skills\sql-optimization\SKILL.md`

Requirements & Tasks:
1. Fix all SQL and DDL constraint errors in `2.Ejercicios/0.prerrequisitos.md`:
   - Line 915: Replace `order_id = 99999` with `order_id = 20000` (respecting `smallint` max value 32767).
   - Lines 1048 & 1058: In `products` INSERT ON CONFLICT statements, include `discontinued` column: `INSERT INTO products (product_id, product_name, unit_price, discontinued) VALUES (100, 'Producto Nuevo', 15.50, 0)...` (fixing NOT NULL violation).
   - Lines 1172 & 1180: Fix query on `order_details` to join `products` for `product_name` or select valid columns (`unit_price * quantity AS total`).
   - Lines 437-488: Change markdown code fence for interactive psql sessions from ```` ```sql ```` to ```` ```text ```` or ```` ```psql ````.
   - Line 310: Fix Docker volume mount path from `aws/db_northwind.sql` to `1.Guia/Material/db_northwind.sql`.
   - Standardize container name to `pg_architect_lab` and credentials to `slinkter` / `postgres123` / `northwind`.
2. Expand Section on PostgreSQL Engine Lifecycle & Logical Processing:
   - Integrate the complete 12-step Logical Processing Pipeline ASCII diagram (`FROM` -> `ON` -> `JOIN` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `WINDOW` -> `SELECT` -> `DISTINCT` -> `SET OPS` -> `ORDER BY` -> `LIMIT/OFFSET`).
   - Integrate the Identifier & Alias Visibility Matrix across all SQL clauses.
   - Explain why `WHERE` cannot see `SELECT` aliases, why `ORDER BY` can, and where window functions are evaluated.
   - Contrast Logical Order vs Physical Query Execution Plan (`EXPLAIN (ANALYZE, BUFFERS)`).
3. Fix TOC and Section Numbering:
   - Correct duplicated Section 6 numbering (`## 6. Estrategias Avanzadas de Indexación`, `## 7. Transacciones: ACID y Niveles de Aislamiento`, `## 8. Arquitectura y Ciclo de Vida del Motor PostgreSQL`, `## 9. Convenciones y Estándares`, `## 10. Bibliografía Recomendada y Referencias de Élite`, `## 11. Banco de Preguntas Conceptuales`, `## 12. Glosario Técnico`).
   - Update Table of Contents at the top of the file to match.
   - Populate Section 10 with elite bibliography:
     - Martin Kleppmann: *Designing Data-Intensive Applications*
     - Gregory Smith: *PostgreSQL 16 High Performance*
     - Hans-Jürgen Schönig: *Mastering PostgreSQL 16*
     - Markus Winand: *SQL Performance Explained*
     - Dmitri Fontaine: *The Art of PostgreSQL*.
4. Verify your modifications and deliver your completion report in `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_prereq_1\handoff.md`, then call send_message.

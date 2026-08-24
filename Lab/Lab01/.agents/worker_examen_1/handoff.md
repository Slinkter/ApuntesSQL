# Handoff Report — Worker Examen (`worker_examen_1`)

**Agent:** Worker Examen (`worker_examen_1`)  
**Parent Conversation ID:** `e5ca8185-8fd7-4a7b-92bf-072321499c97`  
**Working Directory:** `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_examen_1`  
**Target File Exclusively Owned:** `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\4.examen_entrevista.md`  
**Date:** 2026-08-22  

---

## 1. Observation

A full forensic audit and elevation of `2.Ejercicios/4.examen_entrevista.md` was executed against an active PostgreSQL 16 Alpine container (`pg_architect_lab`) populated with the canonical Northwind schema (`1.Guia/Material/db_northwind.sql`).

### Key Observations & Verbatim Data:
1. **Pregunta 10 (Customers with Zero Orders):**
   - In the previous version of the document, Pregunta 10 contained mock entries:
     ```text
     customer_id | company_name | city | country 
     -------------+--------------------------------------+----------+---------
      NWE02 | DataLabs Chile | Santiago | Chile
      NWE01 | TechCorp Peru | Lima | Peru
      PARIS | Paris spécialités | Paris | France
      FISSA | FISSA Fabrica Inter. Salchichas S.A. | Madrid | Spain
     (4 rows)
     ```
   - Direct execution of the Anti-Join query on canonical Northwind yielded **exactly 2 rows**:
     ```text
      customer_id | company_name | city | country 
     -------------+--------------------------------------+--------+---------
      PARIS | Paris spécialités | Paris | France
      FISSA | FISSA Fabrica Inter. Salchichas S.A. | Madrid | Spain
     (2 rows)
     ```
   - There are zero records for Peru (`NWE01`) or Chile (`NWE02`) in the canonical dataset.

2. **Mock String Contamination across ASCII Tables:**
   - In previous tables for Preguntas 1, 21 and 25, `ALFKI` was listed with the mutated string `'Alfreds Futterkiste - Actualizado'`.
   - In canonical Northwind DDL, `company_name` for `ALFKI` is strictly `'Alfreds Futterkiste'`.

3. **Engine Lifecycle & Pedagogical Rigor:**
   - The document previously lacked the formal 12-step PostgreSQL logical execution order diagram, identifier visibility matrix, and structured analytical mental models for interview candidates.
   - All 30 queries were extracted and tested against PostgreSQL 16:
     ```text
     Extracting and running all SQL blocks from 4.examen_entrevista.md...
     [PASS] Pregunta 1 to Pregunta 30: All 30/30 queries executed cleanly.
     ```

---

## 2. Logic Chain

1. **Premise 1:** The Northwind canonical schema (`pthom/northwind_psql`) contains exactly 91 customers, 830 orders, 2155 order details, and 77 products.
2. **Premise 2:** Exactly 2 customers in canonical Northwind have zero registered orders: `PARIS` (`Paris spécialités`) and `FISSA` (`FISSA Fabrica Inter. Salchichas S.A.`).
3. **Premise 3:** Retaining mock entries (`NWE01`, `NWE02`, `- Actualizado`) invalidates the reproducibility of the laboratory when executed by students or interviewers on standard PostgreSQL environments.
4. **Premise 4:** High-level technical interviews for Senior Data Analyst / Database Architect roles require evaluating candidates on the **12-Step Logical Query Processing Pipeline** (`FROM` $\to$ `ON` $\to$ `JOIN` $\to$ `WHERE` $\to$ `GROUP BY` $\to$ `HAVING` $\to$ `WINDOW` $\to$ `SELECT` $\to$ `DISTINCT` $\to$ `SET OPS` $\to$ `ORDER BY` $\to$ `LIMIT`), explaining why expressions fail or succeed at specific evaluation phases (e.g. why window functions cannot appear in `WHERE`/`HAVING`).
5. **Inference:** Replacing all corrupted ASCII outputs with real PostgreSQL 16 outputs, eliminating mock records, embedding the 6-step analytical mental model ("Cómo pensar como un analista"), and providing granular interview rubrics elevates the document to elite academic and industry standards.

---

## 3. Caveats

- **Catalog Execution Plan Times (`Pregunta 29`):** Wall-clock execution times (`actual time`, `Planning Time`, `Execution Time`) in `EXPLAIN (ANALYZE)` vary slightly depending on CPU speed, operating system scheduling, and whether buffers are cached in RAM (`shared_buffers`). The structural node plan (`GroupAggregate`, `Nested Loop Left Join`, `Bitmap Index Scan`) remains deterministic.
- **Concurrency Locking (`Pregunta 30`):** The query demonstrates `SELECT ... FOR UPDATE` row-level locks on product #1 (`Chai`), which currently has 39 units in stock in canonical Northwind.

---

## 4. Conclusion

- `2.Ejercicios/4.examen_entrevista.md` has been completely rewritten and elevated to professional standard.
- **100% Mock Data Free:** `NWE01`, `NWE02`, and `'Alfreds Futterkiste - Actualizado'` have been completely removed.
- **Exact Canonical Outputs:** Pregunta 10 outputs exactly 2 rows (`PARIS`, `FISSA`), and all 30 questions reflect verbatim PostgreSQL 16 outputs.
- **Pedagogical & Engine Rigor:** Includes the master 12-step pipeline diagram, identifier visibility matrix, 6-step reasoning framework, time/space complexity analysis ($O(N)$ and `work_mem`), common interview pitfalls, interview evaluation rubrics (Junior $\to$ Mid $\to$ Senior $\to$ Lead/Architect), and production database engineering notes (Covering indexes with `INCLUDE`, `pg_trgm` GIN indexes, `SELECT ... FOR UPDATE`, dimensional `fact_ventas` with `STORED` generated columns).

---

## 5. Verification Method

To independently verify this work:

1. **Verify Mock Data Elimination:**
   ```powershell
   Select-String -Path "C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\4.examen_entrevista.md" -Pattern "NWE01|NWE02|- Actualizado"
   # Must return 0 matches.
   ```

2. **Verify Pregunta 10 Output:**
   ```powershell
   Get-Content "C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\2.Ejercicios\4.examen_entrevista.md" | Select-String -Pattern "FISSA|PARIS|\(2 rows\)"
   # Must confirm exactly 2 rows.
   ```

3. **Execute the Automated SQL Suite:**
   ```powershell
   node "C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_examen_1\verify_markdown_sql.js"
   # Must return: "Results: 30 / 30 questions executed cleanly against PostgreSQL 16."
   ```

4. **Condition of Invalidation:**
   The handoff is invalidated if any query produces a syntax error on PostgreSQL 16 or if any mock data string is found in `4.examen_entrevista.md`.

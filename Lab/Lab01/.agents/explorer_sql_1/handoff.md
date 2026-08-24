# Handoff Report — SQL & Northwind PostgreSQL Schema Deep Audit

**Agent:** Explorer SQL (`explorer_sql_1`)  
**Parent Conversation ID:** `e5ca8185-8fd7-4a7b-92bf-072321499c97`  
**Working Directory:** `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_sql_1`  
**Date:** 2026-08-22  

---

## 1. Observation

A full-engine audit was performed by loading the canonical PostgreSQL schema `1.Guia/Material/db_northwind.sql` into an isolated PostgreSQL 16 container (`postgres:16-alpine`), parsing all 217+ SQL blocks across the 6 target files, and executing every single query against the database engine with strict transaction isolation and result verification.

### File Inventory & Query Statistics

| File Path | Total SQL Blocks Audited | Engine Execution Success Rate | Discrepancies / Mismatches Detected |
|---|---|---|---|
| `2.Ejercicios/0.prerrequisitos.md` | 31 code blocks | 83.9% (26 valid, 5 errors/pseudo-code) | 5 syntax / constraint bugs |
| `2.Ejercicios/1.basico.md` | 50 exercises | 98.0% (49 valid, 1 syntax error) | 1 syntax bug, 3 row count mismatches, 7 mock data leaks |
| `2.Ejercicios/2.intermedio.md` | 50 exercises | 100.0% (50 valid) | 5 row count mismatches, 12 mock data leaks |
| `2.Ejercicios/3.avanzado.md` | 50 exercises | 100.0% (50 valid) | 4 catalog row count mismatches, 14 mock data leaks |
| `2.Ejercicios/4.examen_entrevista.md` | 35 solution queries | 100.0% (35 valid) | 1 row count mismatch (4 vs 2 rows), 9 mock data leaks |
| `2.Ejercicios/aws_ejercicio.sql` | 1 full script | 100.0% (1 valid) | 0 errors, matches Exercise 1 |

---

### Verbatim Errors & Direct File Evidence

#### A. Syntax Errors and Bugs in Exercise Files

1. **`2.Ejercicios/1.basico.md` (Line 2396, Ejercicio 38: Concatenación con `||`)**
   - **Verbatim SQL:**
     ```sql
     SELECT
         first_name || ' ' || last_name AS nombre_completo,
         title || ' - ' || city AS cargo_ubicacion,
         COALESCE(region || ', ', ') || country AS ubicacion_completa
     FROM employees
     ORDER BY last_name;
     ```
   - **Engine Error:** `ERROR: syntax error at or near ") || country"` (missing opening single quote in `')`).
   - **Fix:** `COALESCE(region || ', ', '') || country AS ubicacion_completa`

2. **`2.Ejercicios/0.prerrequisitos.md` (Lines 1172 & 1180, Sección 7.6 Orden de Ejecución Lógico)**
   - **Verbatim SQL:**
     ```sql
     SELECT
       product_name,
       unit_price * quantity AS total
     FROM order_details
     WHERE total > 100;
     ```
   - **Engine Error:** `ERROR: column "product_name" does not exist` (table `order_details` only has `order_id`, `product_id`, `unit_price`, `quantity`, `discount`).
   - **Fix:** Join `products p ON order_details.product_id = p.product_id` or remove `product_name`.

3. **`2.Ejercicios/0.prerrequisitos.md` (Line 915, Sección 6.1 Transacciones)**
   - **Verbatim SQL:**
     ```sql
     INSERT INTO orders (order_id, customer_id, employee_id, order_date)
     VALUES (99999, 'ALFKI', 1, CURRENT_DATE);
     ```
   - **Engine Error:** `ERROR: smallint out of range` because `orders.order_id` is defined as `smallint NOT NULL` (PostgreSQL smallint max is 32,767).
   - **Fix:** Use an in-range `order_id` (e.g. `20000` or `12000`).

4. **`2.Ejercicios/0.prerrequisitos.md` (Lines 1048 & 1058, Sección 7.2 ON CONFLICT)**
   - **Verbatim SQL:**
     ```sql
     INSERT INTO products (product_id, product_name, unit_price)
     VALUES (100, 'Producto Nuevo', 15.50)
     ON CONFLICT (product_id)
     DO UPDATE SET ...
     ```
   - **Engine Error:** `ERROR: null value in column "discontinued" of relation "products" violates not-null constraint`. In Northwind DDL, `products.discontinued` is `integer NOT NULL` without a default value.
   - **Fix:** Explicitly provide `discontinued`: `INSERT INTO products (product_id, product_name, unit_price, discontinued) VALUES (100, 'Producto Nuevo', 15.50, 0)...`

5. **`2.Ejercicios/0.prerrequisitos.md` (Lines 437-488, Sección 3.3)**
   - Interactive terminal sessions (`northwind=# \conninfo`, `northwind=# \dt`, `-[ RECORD 1 ]+---`) are wrapped in ```` ```sql ```` code fences, throwing syntax errors when executed as pure SQL. Should be ```` ```text ```` or ```` ```psql ````.

6. **`2.Ejercicios/0.prerrequisitos.md` (Line 310, Sección 2.3)**
   - Path in Docker run command: `-v "${PWD}/Lab/Lab01/aws/db_northwind.sql:/docker-entrypoint-initdb.d/db_northwind.sql"` points to a non-existent `aws/` directory instead of `1.Guia/Material/db_northwind.sql`.

7. **`2.Ejercicios/0.prerrequisitos.md` (Structure & TOC)**
   - Duplicate Section 6: Section 6 ("Estrategias Avanzadas de Indexación") and Section 6 ("Transacciones: BEGIN / COMMIT / ROLLBACK").
   - Empty Section 9 ("Bibliografía Recomendada y Referencias de Élite").
   - TOC lists sections 1–9, but body contains sections 1–11.

---

#### B. Mock Data Contamination & Row Count Deviations in ASCII Result Tables

In canonical `1.Guia/Material/db_northwind.sql`:
- `customers` contains **91** rows.
- `customers.company_name` for `ALFKI` is `'Alfreds Futterkiste'`.
- Countries present: **21** countries (no Chile, no Peru).
- Customers with 0 orders: exactly **2** (`FISSA` and `PARIS`).

However, across the exercise documents, the ASCII tables reflect a mutated dataset where:
1. Two mock customers were inserted: `NWE01` (`TechCorp Peru`, `Peru`) and `NWE02` (`DataLabs Chile`, `Chile`).
2. Customer `ALFKI` was updated to `'Alfreds Futterkiste - Actualizado'`.

**Direct discrepancies produced by this artifact:**

| File | Exercise / Question | ASCII Table Claim in Doc | Real Engine Output on Canonical Northwind | Root Cause |
|---|---|---|---|---|
| `1.basico.md` | Ejercicio 14 (`region IS NULL`) | `(62 rows)` | `(60 rows)` | Doc assumes 93 customers (62 nulls); canonical has 91 (60 nulls). |
| `1.basico.md` | Ejercicio 21 (`SELECT DISTINCT country`) | `(23 rows)` (includes Chile, Peru) | `(21 rows)` | Chile and Peru are mock rows absent from canonical DDL. |
| `1.basico.md` | Ejercicio 37 (`SUBSTRING(customer_id)`) | `(93 rows)` | `(91 rows)` | 91 canonical customers vs 93 with mock rows. |
| `2.intermedio.md` | Ejercicio 19 (Correlated Subquery max date) | `(93 rows)` | `(91 rows)` | 91 canonical customers. |
| `2.intermedio.md` | Ejercicio 22 (CASE Zona Logística) | `(93 rows)` (includes Peru/Chile in 'Sudamérica') | `(91 rows)` | 91 canonical customers. |
| `2.intermedio.md` | Ejercicio 26 (CASE ORDER BY) | `(93 rows)` | `(91 rows)` | 91 canonical customers. |
| `2.intermedio.md` | Ejercicio 34 (FULL OUTER JOIN) | `(834 rows)` | `(832 rows)` | 830 orders + 2 zero-order customers (`FISSA`, `PARIS`) = 832. |
| `2.intermedio.md` | Ejercicio 49 (NTILE Quartiles) | `(93 rows)` | `(91 rows)` | 91 canonical customers. |
| `4.examen_entrevista.md` | Pregunta 10 (Customers with 0 orders) | `(4 rows)` (`FISSA`, `PARIS`, `NWE01`, `NWE02`) | `(2 rows)` (`FISSA`, `PARIS`) | Only 2 customers have zero orders in Northwind. |
| Multiple Files | 43 ASCII tables | `'Alfreds Futterkiste - Actualizado'` | `'Alfreds Futterkiste'` | Stale mock update string in expected output. |

---

## 2. Logic Chain

1. **Premise 1:** PostgreSQL standards and exact reproducible academic pedagogy require 100% executable queries with zero syntax errors, type overflow, or schema mismatch against the canonical DDL.
2. **Premise 2:** In `db_northwind.sql`, `order_details` lacks `product_name`, `orders.order_id` is a `smallint` (limit 32,767), `products.discontinued` is `NOT NULL`, and `customers` has 91 records.
3. **Premise 3:** Any query referencing non-existent columns (`order_details.product_name`), violating type ranges (`order_id = 99999`), or violating NOT NULL constraints (`products.discontinued`) immediately halts execution in PostgreSQL.
4. **Premise 4:** An unterminated string literal (`COALESCE(region || ', ', ') || country`) breaks the SQL lexer and parser.
5. **Premise 5:** An ASCII result table in a reference document must correspond 1:1 to the output produced by the solution query on the provided `db_northwind.sql` script.
6. **Inference:** Correcting the 5 identified syntax/schema bugs and regenerating the 43 contaminated ASCII tables against the clean canonical DDL will bring the laboratory to 100% execution fidelity and mathematical consistency.

---

## 3. Caveats

- **PostgreSQL Catalog Statistics Queries (`3.avanzado.md` Exercises 43, 44, 45, 49):** Queries inspecting `pg_stat_user_tables` and `pg_stat_all_tables` yield row counts and metric values that depend on database activity (number of table scans executed, vacuum cycles run). The ASCII tables should clearly indicate that catalog stats are environment-dependent.
- **`aws_ejercicio.sql`:** This file contains only Exercise 1. It is valid and matches Exercise 1 of `1.basico.md`. If intended as a full lab script, it currently only holds one query.
- **No changes were made to source files directly:** In compliance with Explorer role constraints, all findings and exact proposed replacements are provided in this handoff report.

---

## 4. Conclusion

- **Overall Quality Assessment:** The core SQL queries are architecturally sound, demonstrating advanced PostgreSQL capabilities (`FILTER`, `generate_series`, Window Functions, `WITH RECURSIVE`, `MATERIALIZED / NOT MATERIALIZED` hints).
- **Required Fixes:**
  1. Fix the unterminated quote in `1.basico.md` line 2396 (`COALESCE(region || ', ', '') || country`).
  2. Fix the 4 schema/constraint/prompt errors in `0.prerrequisitos.md` (lines 915, 1048, 1172, and 437-488).
  3. Fix the Docker volume mount path in `0.prerrequisitos.md` line 310.
  4. Fix TOC and section numbering in `0.prerrequisitos.md`.
  5. Clean the mock data (`NWE01`, `NWE02`, `- Actualizado`) from all 43 ASCII result tables across `1.basico.md`, `2.intermedio.md`, `3.avanzado.md`, and `4.examen_entrevista.md`, resetting row counts to canonical Northwind numbers (91 customers, 21 countries, 2 zero-order customers).

---

## 5. Verification Method

To independently reproduce and verify this audit:

1. **Spin up a clean test container:**
   ```bash
   docker run --name pg_verify -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=northwind -d postgres:16-alpine
   ```
2. **Load the canonical DDL:**
   ```bash
   docker cp "C:/Users/luisj/Github/ApuntesSQL/Lab/Lab01/1.Guia/Material/db_northwind.sql" pg_verify:/tmp/db_northwind.sql
   docker exec pg_verify psql -U postgres -d northwind -f /tmp/db_northwind.sql
   ```
3. **Execute the automated audit suite in the workspace:**
   ```powershell
   node "C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_sql_1\deep_ascii_comparator.js"
   ```
4. **Inspect generated audit artifacts in `.agents/explorer_sql_1/`:**
   - `detailed_findings.json`
   - `clean_analysis_summary.json`
   - `style_and_syntax_findings.json`

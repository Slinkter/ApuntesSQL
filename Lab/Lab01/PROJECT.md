# Project: PostgreSQL Lab01 Refinement & Academic Polish

## Architecture & Overview
PostgreSQL Lab01 is an advanced, production-grade hands-on laboratory centered on the canonical Northwind database (`pthom/northwind_psql`). It spans two primary directories:
- `1.Guia/`: Technical infrastructure, containerization (`docker-compose.yml`, `.env`), deployment guides on AWS EC2 (Amazon Linux 2023 / Ubuntu 24.04), security best practices, and laboratory standard guidelines (`STANDARD.md`).
- `2.Ejercicios/`: Progression from fundamentals to principal data analyst interview problems (`0.prerrequisitos.md`, `1.basico.md`, `2.intermedio.md`, `3.avanzado.md`, `4.examen_entrevista.md`, `aws_ejercicio.sql`), enriched with logical query processing analysis and structured mental models.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F01 | Docker Compose & Env Specs | Create `.env.example`/`.env`, add `${VAR:-default}` fallbacks, read-only volume mounts, healthchecks, memory limits, and logging policy in `docker-compose.yml`. | M1 | Survey Infra |
| F02 | AWS EC2 Deployment Guide | Complete end-to-end EC2 deployment steps (AMI AL2023/Ubuntu, security groups port 22/5432 /32, user-data, cloud-init log check, SSH key permissions via `icacls`/`chmod 400`, teardown). | M1 | Survey Infra |
| F03 | Fix Broken Paths & Commands in Guia | Repair SCP commands pointing to `aws/...` instead of `1.Guia/Material/...`, eliminate dangerous `mv ~/.*`, fix links in `README.md`. | M1 | Survey Infra |
| F04 | Standard Guidelines Update | Update `1.Guia/STANDARD.md` with formatting rules, engine order breakdowns, and "Cómo pensar como analista" templates. | M1 | Survey Pedagogy |
| F05 | Fix Prerrequisitos Bugs & DDL Constraints | Fix `order_id` smallint overflow (99999 -> 20000), `discontinued` NOT NULL in `products` insert, `product_name` missing from `order_details`, code fence tags for psql sessions, and Docker mount path. | M2 | Survey SQL |
| F06 | Master Engine Lifecycle & Visibility Matrix | Incorporate the comprehensive 12-step logical query processing pipeline diagram and identifier/alias visibility matrix in `0.prerrequisitos.md`. | M2 | Survey Pedagogy |
| F07 | Elite Bibliography & Prerrequisitos TOC | Fix duplicated Section 6, fix TOC alignment, and populate Section 10 with elite references (Kleppmann, Smith, Schönig, Winand, Fontaine). | M2 | Survey Pedagogy |
| F08 | Fix SQL Syntax Bug in Basico | Fix unterminated single quote in `1.basico.md` Exercise 38 (`COALESCE(region || ', ', '') || country`). | M3 | Survey SQL |
| F09 | Eliminate Mock Data Contamination | Clean mock records (`NWE01`, `NWE02`, `'Alfreds Futterkiste - Actualizado'`) across 43 ASCII tables in `1.basico.md`, `2.intermedio.md`, `3.avanzado.md`, `4.examen_entrevista.md`. | M3 | Survey SQL |
| F10 | Exact Northwind Row Counts in ASCII Tables | Align row counts to canonical Northwind DDL (91 customers, 21 countries, 2 zero-order customers, 832 FULL JOIN rows). | M3 | Survey SQL |
| F11 | Truncate Massive Result Sets | Truncate oversized ASCII table dumps (>20 rows) in `2.intermedio.md` and `3.avanzado.md` with `(N rows)` summary footer for optimal readability. | M3 | Survey Pedagogy |
| F12 | Integrate "Cómo Pensar como un Analista" | Standardize the 6-step analytical mental model across key exercise blocks in `1.basico.md`, `2.intermedio.md`, `3.avanzado.md`, and `4.examen_entrevista.md`. | M4 | Survey Pedagogy |
| F13 | High-Impact Pedagogical Analogies | Enrich exercise explanations with the 8 active-learning analogies (Colador vs Lista, Cajas de mudanza, Espejo retrovisor, Árbol genealógico, etc.). | M4 | Survey Pedagogy |
| F14 | Engine Processing Order in Complex Exercises | Embed explicit step-by-step logical execution order breakdowns in intermediate, advanced, and interview questions. | M4 | Survey Pedagogy |
| F15 | Comprehensive Verification & Forensic Audit | Multi-tier validation: automated SQL engine execution tests, Reviewers approval, Challengers verification, and Forensic Auditor clean verdict. | M5 | Core Requirement |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Infrastructure & Deployment Guide | `1.Guia/*`, `docker-compose.yml`, `.env.example`, `.env`, `README.md`, `STANDARD.md` | none | DONE |
| M2 | Prerequisites & Engine Foundations | `2.Ejercicios/0.prerrequisitos.md` | M1 | DONE |
| M3 | SQL Exercises & Exact ASCII Outputs | `2.Ejercicios/1.basico.md`, `2.intermedio.md`, `3.avanzado.md`, `4.examen_entrevista.md`, `aws_ejercicio.sql` | M2 | IN_PROGRESS |
| M4 | Pedagogical Framing & Engine Order | All exercise files (`2.Ejercicios/*`) | M3 | IN_PROGRESS |
| M5 | Multi-Tier Verification & Forensic Audit | Full repository verification | M1, M2, M3, M4 | PLANNED |

## Code Layout
```
Lab/Lab01/
├── 1.Guia/
│   ├── 0.Guia_Docker_AWS.md          # Complete AWS EC2 + Docker guide
│   ├── README.md                      # Index with verified relative links
│   ├── STANDARD.md                    # Editorial and technical standard
│   └── Material/
│       ├── .env                       # Default environment variables
│       ├── .env.example               # Example template
│       ├── docker-compose.yml         # Hardened PostgreSQL 16 compose definition
│       └── db_northwind.sql           # Canonical Northwind schema and data
└── 2.Ejercicios/
    ├── 0.prerrequisitos.md            # Foundations, DDL, 12-step engine pipeline, bibliography
    ├── 1.basico.md                    # 50 basic queries, exact ASCII outputs, syntax fixed
    ├── 2.intermedio.md                # 50 intermediate queries, truncated clean ASCII outputs
    ├── 3.avanzado.md                  # 50 advanced queries (CTEs, Window, Recursion, Optimizer)
    ├── 4.examen_entrevista.md         # 30 high-level interview questions and solutions
    └── aws_ejercicio.sql              # Consolidated reference SQL script
```

## Interface Contracts
- Canonical Database Schema: `pthom/northwind_psql` (14 tables: `categories`, `customer_customer_demo`, `customer_demographics`, `customers` [91 rows], `employee_territories`, `employees` [9 rows], `order_details` [2155 rows], `orders` [830 rows], `products` [77 rows], `region` [4 rows], `shippers` [3 rows], `suppliers` [29 rows], `territories` [53 rows], `us_states` [51 rows]).
- Container Name: `pg_architect_lab` (standardized across guides, compose, and exercises).
- Default Credentials: User `slinkter`, Password `postgres123`, Database `northwind`, Port `5432`.
- Engine Execution Pipeline Standard: `FROM` -> `ON` -> `JOIN` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `WINDOW` -> `SELECT` -> `DISTINCT` -> `SET OPS` -> `ORDER BY` -> `LIMIT/OFFSET`.

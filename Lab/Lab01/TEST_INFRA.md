# E2E Test Infra: PostgreSQL Lab01 Refinement

## Test Philosophy
- Requirement-driven, multi-tier verification covering Infrastructure (R1), SQL correctness & exact outputs (R2), Logical execution engine breakdowns (R3), and Pedagogical frameworks (R4).
- Opaque-box validation against live PostgreSQL 16 container running canonical `db_northwind.sql`.

## Feature Inventory & Test Mapping
| # | Feature | Requirement | Tier 1 (Unit/Syntax) | Tier 2 (Boundaries/Schema) | Tier 3 (Cross-Doc Consistency) | Tier 4 (Full E2E Execution) |
|---|---------|-------------|:------:|:------:|:------:|:------:|
| F01 | Docker Compose & Env Specs | R1 | ✓ | ✓ | ✓ | ✓ |
| F02 | AWS EC2 Deployment Guide | R1 | ✓ | ✓ | ✓ | ✓ |
| F03 | Fix Broken Paths in Guia | R1 | ✓ | ✓ | ✓ | ✓ |
| F04 | Standard Guidelines Update | R1, R4 | ✓ | ✓ | ✓ | ✓ |
| F05 | Fix Prerrequisitos Bugs & DDL Constraints | R2 | ✓ | ✓ | ✓ | ✓ |
| F06 | Master Engine Lifecycle & Visibility Matrix | R3 | ✓ | ✓ | ✓ | ✓ |
| F07 | Elite Bibliography & Prerrequisitos TOC | R4 | ✓ | ✓ | ✓ | ✓ |
| F08 | Fix SQL Syntax Bug in Basico (Ex 38) | R2 | ✓ | ✓ | ✓ | ✓ |
| F09 | Eliminate Mock Data Contamination (43 tables) | R2 | ✓ | ✓ | ✓ | ✓ |
| F10 | Exact Northwind Row Counts in ASCII Tables | R2 | ✓ | ✓ | ✓ | ✓ |
| F11 | Truncate Massive Result Sets | R2, R4 | ✓ | ✓ | ✓ | ✓ |
| F12 | Integrate "Cómo Pensar como un Analista" | R4 | ✓ | ✓ | ✓ | ✓ |
| F13 | High-Impact Pedagogical Analogies | R4 | ✓ | ✓ | ✓ | ✓ |
| F14 | Engine Processing Order in Complex Exercises | R3 | ✓ | ✓ | ✓ | ✓ |
| F15 | Comprehensive Verification & Forensic Audit | AC 1-5 | ✓ | ✓ | ✓ | ✓ |

## Test Architecture
- Test Suite 1: Static markdown links and relative path validation.
- Test Suite 2: Docker Compose YAML linting and validation (`docker compose config`).
- Test Suite 3: SQL Extraction and Live Engine Execution (217+ queries against PostgreSQL 16 `pthom/northwind_psql`).
- Test Suite 4: ASCII Table Exact Output & Row Count Matcher.
- Test Suite 5: Pedagogical Completeness & Logical Engine Order Verification.
- Test Suite 6: Forensic Integrity Audit.

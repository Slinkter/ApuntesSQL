# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This repository is a structured knowledge base and educational resource for mastering SQL and PostgreSQL, focusing on deep internals, relational theory, and high-performance data architecture.

## Repository Structure
The content is organized into evolutionary phases, primarily within numbered directories:
- `01_Fundamentos/`: Core concepts, relational theory, database typology, and SDLC/Migrations.
- `02_Postgres_Internals/`: Deep dive into PostgreSQL internals, tactical data types, and normalization.
- `03_Escalabilidad/`: Advanced topics including specialized indexing, query planning, and HTAP architectures.
- `04_Laboratorios/`: Practical guides and deployment exercises (e.g., Docker, AWS).
- `Apuntes/`, `PostgresSQL/`, `ULima/`: Archive and supplementary study materials.

## Development Conventions
- **Content Format**: All lessons and guides are written in Markdown (`.md`).
- **Naming Convention**: Lessons typically follow the pattern `Clase_X.YY_Topic_Name.md`.
- **Style**: Technical, direct, and mentor-like tone, emphasizing engineering reality and scalability.

## Common Tasks
Since this is a documentation-centric repository, there are no build or test commands. Common operations include:
- **Adding new lessons**: Create a new `.md` file in the appropriate phase directory following the `Clase_X.YY_...` naming convention.
- **Refactoring content**: Update existing lessons to align with modern PostgreSQL versions (v15+) and industry standards.

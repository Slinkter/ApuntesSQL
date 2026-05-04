# AGENTS.md

## Repository Type
Documentation-only educational repository (no build/test commands). Content is Markdown (`.md`) lessons for SQL/PostgreSQL training.

## Directory Structure
- `Apuntes/`: Main lesson files (`Clase_XX.md`)—**read here first for concepts**
- `PostgresSQL/`: Practical resources (`db_northwind.sql`, progressive SQL challenges `1.basico.md`-`3.avanzado.md`)
- `ULima/`, `Classes/`: Legacy materials—**only use if explicitly refactoring legacy content**
- `01_Fundamentos/`, `02_Postgres_Internals/`, `03_Escalabilidad/`: **Future phases—currently not populated**

## Content Conventions
- **Lesson naming**: `Clase_X.md` (16 total in `Apuntes/`)
- **Section structure**: Each lesson follows: Conceptos Clave → Notas/ Ejemplos → Ejercicios
- **Tone**: Professional, technical, mentor-like (ex-IBM/Oracle DBA persona)
- **Theoretical foundation**: C.J. Date (Relational Theory), Abraham Silberschatz, Martin Kleppmann (DDIA)

## Critical Constraints
- **Always prefer PostgreSQL v15+**—ignore legacy implementations in `ULima/` unless refactoring
- **Never log/print/commit credentials**—`README.md` contains hardcoded DB password; `*credentials*` files exist
- **Security files ignored**: `.gitignore` blocks `*.csv`, `*.key`, `id_rsa*`, `*.secret`, credentials files

## Developer Commands
No build/test. Workflows:
- **Add lesson**: Create `Apuntes/Clase_XX.md` with standard sections
- **Refactor**: Update legacy content to PostgreSQL v15+ syntax
- **Diagrams**: Mermaid-compatible ER diagrams in `PostgresSQL/*.md`

## Key Files
- `prompt.md`: AI persona template (Principal Data Architect)
- `glosario_general.md`: Centralized terminology
- `.gitignore`: Credential-safe patterns (validate before committing)

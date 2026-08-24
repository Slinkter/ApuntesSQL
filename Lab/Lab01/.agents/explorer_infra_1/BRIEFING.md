# BRIEFING — 2026-08-22T18:04:00Z

## Mission
Investigate and analyze PostgreSQL Lab01 Infrastructure and AWS EC2 / Docker deployment materials, identifying gaps, bugs, security issues, and providing detailed recommendations.

## 🔒 My Identity
- Archetype: explorer
- Roles: investigator, synthesis
- Working directory: C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_infra_1
- Original parent: e5ca8185-8fd7-4a7b-92bf-072321499c97
- Milestone: Infrastructure & Deployment Analysis

## 🔒 Key Constraints
- Read-only investigation — do NOT implement changes in source directories directly
- Analyze Docker container setup, healthchecks, PostgreSQL version, persistent volumes, environment variables
- Analyze AWS EC2 deployment: Step-by-step commands (Ubuntu/Amazon Linux setup, installing Docker & Docker Compose, security groups for inbound port 5432 / SSH 22, pulling/running containers, loading Northwind database dump)
- Analyze missing steps, broken commands, unclear instructions, security best practices

## Current Parent
- Conversation ID: e5ca8185-8fd7-4a7b-92bf-072321499c97
- Updated: 2026-08-22T18:04:00Z

## Investigation State
- **Explored paths**:
  - `1.Guia/0.Guia_Docker_AWS.md`
  - `1.Guia/Material/docker-compose.yml`
  - `1.Guia/Material/db_northwind.sql`
  - `1.Guia/README.md`
  - `1.Guia/STANDARD.md`
  - `2.Ejercicios/0.prerrequisitos.md`
  - `2.Ejercicios/aws_ejercicio.sql`
  - `Lab/Lab01/prompt.md`
  - `Credenciales/` directory
- **Key findings**:
  1. Critical Path Mismatch: Guides reference `.\Lab\Lab01\aws\...` which does not exist; actual path is `.\Lab\Lab01\1.Guia\Material\...`.
  2. Missing `.env` / `.env.example`: Referenced in SCP commands and compose file, but missing from repository.
  3. High-Risk Troubleshooting Command: `mv ~/.* ~/postgres-lab/` in `0.Guia_Docker_AWS.md` can move `~/.ssh` and destroy SSH remote access.
  4. Docker Compose Variable Fallbacks: `docker-compose.yml` lacks default variable fallbacks (`${VAR:-default}`), risking failure if `.env` is omitted.
  5. Inconsistent Container Names: `pg_architect_lab` vs `pg_northwind_lab` across guides and exercise prerequisites.
  6. Missing Key Permissions Guidance: No `icacls` (Windows) or `chmod 400` (Linux/Mac) commands for `key_u_docker.pem`.
  7. Entrypoint Initialization Caveat: PostgreSQL entrypoint only executes `/docker-entrypoint-initdb.d/` on empty volumes; not documented.
  8. Cloud-init Asynchronous Execution: Student might log in while Docker is still installing via user-data.
  9. Network / Cost Guidance: Missing instructions on dynamic IP change upon EC2 stop/start and instance teardown.
- **Unexplored areas**: None, all infrastructure artifacts and references explored.

## Key Decisions Made
- Formulated complete 5-component handoff report detailing Docker, AWS EC2, Security, File Transfer, Verification, and Lifecycle best practices.

## Artifact Index
- C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_infra_1\DISPATCH.md — incoming dispatch records
- C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_infra_1\progress.md — heartbeat and progress tracker
- C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_infra_1\handoff.md — 5-component handoff report

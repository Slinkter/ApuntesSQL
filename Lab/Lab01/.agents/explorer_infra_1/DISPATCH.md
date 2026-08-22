## 2026-08-22T18:02:50Z
<USER_REQUEST>
You are Explorer Infra (working in C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_infra_1).

You must inspect the PostgreSQL Lab01 Infrastructure and Deployment materials:
1. Read the original request at `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\ORIGINAL_REQUEST.md`.
2. Inspect the current files in `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia`:
   - `0.Guia_Docker_AWS.md`
   - `Material/docker-compose.yml`
   - `README.md`
   - `STANDARD.md`
   - Any other scripts or material in `1.Guia` or repo root.
3. Analyze and document all gaps regarding:
   - Docker container setup, healthchecks, PostgreSQL version, persistent volumes, environment variables (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD).
   - AWS EC2 deployment: Step-by-step commands (Ubuntu/Amazon Linux setup, installing Docker & Docker Compose, security groups for inbound port 5432 / SSH 22, pulling/running containers, loading Northwind database dump).
   - Missing steps, broken commands, unclear instructions, security best practices.
4. Deliver your findings and detailed recommendations in `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_infra_1\handoff.md` and report back using send_message.
</USER_REQUEST>

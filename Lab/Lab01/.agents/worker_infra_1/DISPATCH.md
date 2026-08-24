## 2026-08-22T18:09:52Z
You are Worker Infra (working in C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_infra_1).

You are assigned Milestone 1 (M1): Infrastructure & Deployment Guide Refinement.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File Ownership (You exclusively own and edit these files):
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia\0.Guia_Docker_AWS.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia\Material\docker-compose.yml`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia\Material\.env.example`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia\Material\.env`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia\README.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\1.Guia\STANDARD.md`

Context & Input Reports to Read First:
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\ORIGINAL_REQUEST.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\PROJECT.md`
- `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\explorer_infra_1\handoff.md`

Requirements & Tasks:
1. Create `1.Guia/Material/.env.example` and `1.Guia/Material/.env` with `POSTGRES_USER=slinkter`, `POSTGRES_PASSWORD=postgres123`, `POSTGRES_DB=northwind`, `PGPORT=5432`.
2. Refactor `1.Guia/Material/docker-compose.yml`:
   - Use image `postgres:16-alpine`, container name `pg_architect_lab`, restart `unless-stopped`.
   - Environment variables with fallbacks `${POSTGRES_USER:-slinkter}`, `${POSTGRES_PASSWORD:-postgres123}`, `${POSTGRES_DB:-northwind}`.
   - Port `${PGPORT:-5432}:5432`.
   - Volume mounts: `pg_data:/var/lib/postgresql/data` and `./init/db_northwind.sql:/docker-entrypoint-initdb.d/01_db_northwind.sql:ro`.
   - Healthcheck: `test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-slinkter} -d ${POSTGRES_DB:-northwind}"]`, interval 10s, timeout 5s, retries 5, start_period 30s.
   - Memory limits (512M), json-file logging limits, dedicated bridge network `pg_network`.
3. Rewrite and perfect `1.Guia/0.Guia_Docker_AWS.md`:
   - Fix all broken SCP paths (`.\Lab\Lab01\1.Guia\Material\docker-compose.yml`, `.env`, `db_northwind.sql` uploaded directly to `~/postgres-lab/` and `~/postgres-lab/init/`).
   - Remove dangerous command `mv ~/.* ~/postgres-lab/`.
   - Include SSH key permissions instructions (`icacls` for Windows PowerShell, `chmod 400` for Linux/Mac/WSL).
   - Complete AWS EC2 deployment walkthrough: Amazon Linux 2023 and Ubuntu 24.04 AMIs, t3.micro/t2.micro, Security Group port 22 and 5432 restricted to `My IP` (`<IP>/32`), User Data scripts with cloud-init log inspection (`cat /var/log/cloud-init-output.log`), container lifecycle & entrypoint initialization rules, verification queries (`\dt`, row count tests), DBeaver/VSCode connection setup, and instance teardown/stopping instructions for cost management.
4. Update `1.Guia/README.md` repairing all broken links to `0.Guia_Docker_AWS.md`, `Material/docker-compose.yml`, `Material/db_northwind.sql`, and `../2.Ejercicios/0.prerrequisitos.md`.
5. Update `1.Guia/STANDARD.md` incorporating the 6-step "🧠 Cómo Pensar como un Analista de Datos" framework and query execution engine formatting rules.
6. Verify your changes and deliver your completion report in `C:\Users\luisj\Github\ApuntesSQL\Lab\Lab01\.agents\worker_infra_1\handoff.md`, then call send_message.

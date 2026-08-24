# Handoff Report — Milestone 1 (M1): Infrastructure & Deployment Guide Refinement

**Agent:** Worker Infra (`worker_infra_1`)  
**Role:** Implementer / QA / Specialist  
**Milestone:** M1 — Infrastructure & Deployment Guide Refinement  
**Date:** 2026-08-22  
**Handoff Type:** Hard (Task Complete)

---

## 1. Observation

During the audit and implementation of Milestone 1, the following initial state was observed and subsequently transformed:

1. **Missing `.env` and `.env.example` Files:**
   - In `1.Guia/Material/`, neither `.env` nor `.env.example` existed originally.
   - `docker-compose.yml` referenced `${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`, `${POSTGRES_DB}` without default value fallbacks (`:-`), causing empty string resolution or warnings when launched directly.

2. **`docker-compose.yml` Deficiencies:**
   - Container was configured with `restart: always` instead of `restart: unless-stopped`.
   - Lacked healthcheck (`pg_isready`), memory limits (`512M`), logging constraints (`json-file`, max 10MB, 3 files), and port variable fallbacks `${PGPORT:-5432}:5432`.
   - SQL volume was mapped as `./init/db_northwind.sql:/docker-entrypoint-initdb.d/db_northwind.sql` without read-only mode (`:ro`) and without deterministic lexicographical prefix.

3. **Broken SCP Paths and Dangerous Commands in `1.Guia/0.Guia_Docker_AWS.md`:**
   - SCP commands referenced a non-existent directory `.\Lab\Lab01\aws\...` (lines 75, 78, 81, 87, 90, 93 in the original file).
   - The troubleshooting section contained the destructive command `mv ~/.* ~/postgres-lab/`, which moves `~/.ssh/authorized_keys` and irreversibly locks out SSH sessions.
   - Missing SSH key permission hardening (`icacls` for Windows PowerShell, `chmod 400` for POSIX).
   - Missing step-by-step guidance for cloud-init log inspection (`cat /var/log/cloud-init-output.log`), container lifecycle behavior with `/docker-entrypoint-initdb.d/` on persistent volumes, row count verification queries, DBeaver connection, and EC2 stop vs terminate lifecycle management.

4. **Broken Links in `1.Guia/README.md`:**
   - Links pointed to `aws/Guia_Docker_AWS.md`, `aws/docker-compose.yml`, `aws/db_northwind.sql`, and `Ejercicios/...` instead of their valid relative paths (`0.Guia_Docker_AWS.md`, `Material/...`, `../2.Ejercicios/...`).

5. **Incomplete Standard in `1.Guia/STANDARD.md`:**
   - Lacked the 6-step "🧠 Cómo Pensar como un Analista de Datos" framework.
   - Lacked explicit logical query execution order breakdown (`FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `WINDOW` $\rightarrow$ `SELECT` $\rightarrow$ `DISTINCT` $\rightarrow$ `SET OPS` $\rightarrow$ `ORDER BY` $\rightarrow$ `LIMIT/OFFSET`).

---

## 2. Logic Chain

1. **Credential Decoupling & Compose Robustness:** By introducing `1.Guia/Material/.env.example` and `1.Guia/Material/.env` alongside default fallbacks (`${POSTGRES_USER:-slinkter}`, `${POSTGRES_PASSWORD:-postgres123}`, `${POSTGRES_DB:-northwind}`, `${PGPORT:-5432}`), Docker Compose can be run safely out of the box without environment errors. Adding `healthcheck`, `deploy.resources.limits.memory: 512M`, and `logging` prevents resource exhaustion on Free Tier EC2 instances (`t3.micro`/`t2.micro`).
2. **Direct File Transfer:** Uploading files directly via SCP to `~/postgres-lab/` and `~/postgres-lab/init/` eliminates the need for any post-upload `mv` commands, completely removing the risk of accidentally moving hidden dotfiles like `~/.ssh`.
3. **Deterministic SQL Initialization:** Mounting `./init/db_northwind.sql` to `/docker-entrypoint-initdb.d/01_db_northwind.sql:ro` guarantees read-only safety and explicit execution ordering during the initial `initdb` process.
4. **End-to-End AWS EC2 Walkthrough:** Providing exact AMIs (AL2023 & Ubuntu 24.04), User Data scripts, cloud-init log checks (`tail -f /var/log/cloud-init-output.log`), and strict Security Group ingress rules (`/32` restricted to `My IP`) ensures zero omitted steps, high security, and smooth execution for students.
5. **Navigation Integrity:** Updating all relative paths in `1.Guia/README.md` allows seamless navigation across both the `1.Guia/` and `2.Ejercicios/` directories.
6. **Pedagogical Standardization:** Embedding the 6-step analytical mental model and logical query execution order in `1.Guia/STANDARD.md` establishes a clear contract for all exercise authors (M2, M3, M4).

---

## 3. Caveats

- **Dynamic Public IPs:** If the student's local ISP changes their public IP address, the Security Group inbound rules (`/32`) on AWS must be updated to match the new public IP.
- **Persistent Volume Initialization:** The `/docker-entrypoint-initdb.d/` initialization script only executes on an empty data directory. If the container was already started before mounting the script, the volume must be wiped with `docker compose down -v`. This behavior is now explicitly documented in the guide.
- No other caveats.

---

## 4. Conclusion

Milestone 1 (M1) is 100% complete and fully verified:
- `1.Guia/Material/.env.example` and `.env` created with `POSTGRES_USER=slinkter`, `POSTGRES_PASSWORD=postgres123`, `POSTGRES_DB=northwind`, `PGPORT=5432`.
- `1.Guia/Material/docker-compose.yml` refactored and validated against Docker Compose specification with container name `pg_architect_lab`, image `postgres:16-alpine`, healthcheck, resource limits, network, and read-only volume.
- `1.Guia/0.Guia_Docker_AWS.md` completely rewritten into an end-to-end, hardened cloud deployment guide with Windows PowerShell `icacls` & Unix `chmod 400`, exact direct SCP commands, AL2023 & Ubuntu User Data, verification queries, client connection guides, and cost management.
- `1.Guia/README.md` updated with 100% valid relative links.
- `1.Guia/STANDARD.md` updated with the 6-step analytical thought process, query execution engine rules, and exercise templates.

---

## 5. Verification Method

To independently verify the changes:

1. **Docker Compose Configuration Validation:**
   ```bash
   docker compose -f "Lab/Lab01/1.Guia/Material/docker-compose.yml" config
   ```
   *Result:* Exits with code 0 and outputs valid YAML with resolved environment variables.

2. **File Existence and Relative Link Check:**
   Execute in PowerShell:
   ```powershell
   $links = @(
       "Lab\Lab01\1.Guia\0.Guia_Docker_AWS.md",
       "Lab\Lab01\1.Guia\Material\docker-compose.yml",
       "Lab\Lab01\1.Guia\Material\.env.example",
       "Lab\Lab01\1.Guia\Material\.env",
       "Lab\Lab01\1.Guia\Material\db_northwind.sql",
       "Lab\Lab01\1.Guia\STANDARD.md",
       "Lab\Lab01\2.Ejercicios\0.prerrequisitos.md",
       "Lab\Lab01\2.Ejercicios\1.basico.md",
       "Lab\Lab01\2.Ejercicios\2.intermedio.md",
       "Lab\Lab01\2.Ejercicios\3.avanzado.md",
       "Lab\Lab01\2.Ejercicios\4.examen_entrevista.md",
       "Lab\Lab01\2.Ejercicios\aws_ejercicio.sql"
   )
   $links | ForEach-Object { if (Test-Path $_) { Write-Host "OK: $_" } else { Write-Error "MISSING: $_" } }
   ```
   *Result:* All 12 files return `OK`.

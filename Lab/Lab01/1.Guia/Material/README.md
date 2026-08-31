# 📦 Directorio de Infraestructura y Material Operativo (`1.Guia/Material/`)

Este directorio contiene los artefactos de infraestructura como código (**IaC**), variables de entorno, configuración del motor relacional y el script DDL/DML canónico para desplegar **PostgreSQL 16** de forma reproducible tanto en entornos locales (**Windows / macOS / Linux**) como en la nube (**AWS EC2**).

---

## 📂 Inventario de Archivos

| Archivo | Tipo | Propósito y Descripción |
| :--- | :---: | :--- |
| **[`docker-compose.yml`](docker-compose.yml)** | YAML | Manifiesto de orquestación del contenedor `pg_architect_lab` con límites de memoria (512M), healthcheck automático (`pg_isready`), volúmenes persistentes y política de logs rotativos. |
| **[`.env`](.env)** | Config | Archivo de variables de entorno activo. Define las credenciales por defecto del laboratorio (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `PGPORT`). |
| **[`.env.example`](.env.example)** | Plantilla | Plantilla segura de variables de entorno para control de versiones y entornos de producción. |
| **[`db_northwind.sql`](db_northwind.sql)** | SQL (355 KB) | Script DDL y DML canónico de Northwind para PostgreSQL (`pthom/northwind_psql`) con las 14 tablas relacionales completas. |

---

## ⚙️ 1. Variables de Entorno y Configuración (`.env`)

El archivo `.env` controla los parámetros de inicialización del motor PostgreSQL:

```ini
# ==============================================================================
# CONFIGURACIÓN DEL MOTOR POSTGRESQL 16 (LAB01)
# ==============================================================================
POSTGRES_USER=slinkter
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=northwind
PGPORT=5432
```

> [!TIP]
> En `docker-compose.yml`, cada variable cuenta con un valor de reserva (*fallback*), por ejemplo `${POSTGRES_USER:-slinkter}`, garantizando que el contenedor arranque correctamente incluso si el archivo `.env` no es detectado.

---

## 🚀 2. Guía de Inicio Rápido (Quick Start)

### Opción A: Despliegue con Docker Compose (Recomendado)

Desde una terminal ubicada en este directorio (`1.Guia/Material/`):

```bash
# 1. Levantar el contenedor en segundo plano
docker compose up -d

# 2. Verificar el estado del servicio y el healthcheck
docker compose ps

# 3. Ver los logs de inicialización del motor
docker compose logs -f
```

---

### Opción B: Despliegue con Docker CLI Standalone

Si prefieres ejecutar el contenedor directamente sin Compose:

#### En Windows PowerShell (desde la raíz del repositorio):
```powershell
docker run --name pg_architect_lab `
  -e POSTGRES_USER=slinkter `
  -e POSTGRES_PASSWORD=postgres123 `
  -e POSTGRES_DB=northwind `
  -v "${PWD}/1.Guia/Material/db_northwind.sql:/docker-entrypoint-initdb.d/01_db_northwind.sql:ro" `
  -v "pg_data:/var/lib/postgresql/data" `
  -p 5432:5432 `
  -m 512m `
  -d postgres:16-alpine
```

#### En Linux / macOS / AWS EC2 (Bash):
```bash
docker run --name pg_architect_lab \
  -e POSTGRES_USER=slinkter \
  -e POSTGRES_PASSWORD=postgres123 \
  -e POSTGRES_DB=northwind \
  -v "$(pwd)/1.Guia/Material/db_northwind.sql:/docker-entrypoint-initdb.d/01_db_northwind.sql:ro" \
  -v "pg_data:/var/lib/postgresql/data" \
  -p 5432:5432 \
  -m 512m \
  -d postgres:16-alpine
```

---

## 🔍 3. Verificación de Salud e Integridad de Datos

Una vez iniciado el contenedor, verifica que las 14 tablas de Northwind se cargaron con sus cardinalidades canónicas:

```bash
# Conectarse a psql dentro del contenedor
docker exec -it pg_architect_lab psql -U slinkter -d northwind
```

```sql
-- Validar conteos exactos de la base de datos canónica
SELECT 
    (SELECT COUNT(*) FROM customers) AS total_customers,       -- 91
    (SELECT COUNT(*) FROM orders) AS total_orders,             -- 830
    (SELECT COUNT(*) FROM order_details) AS total_order_details, -- 2155
    (SELECT COUNT(*) FROM products) AS total_products;         -- 77
```

---

## 🛠️ 4. Parámetros de Operación y Hardening en `docker-compose.yml`

El manifiesto de Compose implementa las siguientes directivas de ingeniería:

1. **Montaje de Inicialización de Solo Lectura (`:ro`):**
   ```yaml
   - ./db_northwind.sql:/docker-entrypoint-initdb.d/01_db_northwind.sql:ro
   ```
   Garantiza que el motor lea el script SQL durante el primer arranque sin riesgo de que el proceso interno modifique o corrompa el archivo fuente en el host.

2. **Límites de Recursos de Memoria (Deploy Limits):**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
   ```
   Evita que consultas analíticas mal diseñadas consuman toda la RAM del host o de la instancia EC2 (`t3.micro` / `t2.micro`).

3. **Política de Rotación de Logs:**
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```
   Acota los logs a un máximo de 30 MB totales en disco para prevenir el agotamiento de almacenamiento.

---

## 🔄 5. Ciclo de Vida: Reinicio y Restauración Limpia

Si necesitas restablecer la base de datos a su estado original desde cero:

```bash
# 1. Detener el contenedor y eliminar volúmenes persistentes
docker compose down -v

# 2. Reconstruir e inicializar nuevamente
docker compose up -d

# 3. Validar que el healthcheck pase a 'healthy'
docker ps --filter "name=pg_architect_lab"
```

---
*Este material forma parte integral del Laboratorio PostgreSQL Lab01.*

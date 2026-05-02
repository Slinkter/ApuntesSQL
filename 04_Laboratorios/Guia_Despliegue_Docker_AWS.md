# Laboratorio: Despliegue de Arquitectura de Datos en AWS con Docker (End-to-End)

**Instructor:** Principal Data Architect
**Enfoque:** Conectividad, Persistencia y Orquestación.

---

## 1. Introducción
Este laboratorio detalla el proceso completo para llevar una base de datos local (**Northwind**) a una infraestructura de nube en **AWS EC2**, utilizando **Docker Compose** para garantizar la portabilidad y la persistencia del dato.

## 2. Requisitos Previos (Local y Nube)
*   **Local:** Archivo `db_northwind.sql` en la carpeta `PostgresSQL/` y tu llave privada de AWS (`.pem`).
*   **Nube:** Instancia EC2 Ubuntu con Docker y Docker Compose instalados.
*   **Red:** Puerto 5432 abierto en el Security Group de AWS.

> **IMPORTANTE:** El archivo `db_northwind.sql` ya está corregido (sin DROP/CREATE DATABASE). **NO** agregues estas líneas.

---

## 3. Paso 1: Configuración de Red en AWS (Security Groups)

Antes de conectar, asegúrate de que AWS permita el tráfico. De lo contrario, tu conexión será rechazada (timeout).

1.  Consola EC2 > **Security Groups** > Selecciona el grupo de seguridad asociado a tu instancia.
2.  **Inbound Rules** > **Edit inbound rules**.
3.  Haz clic en **"Add rule"** y configura lo siguiente:
    - **Type:** Selecciona `PostgreSQL` (esto pondrá automáticamente el puerto **5432**).
    - **Source:** Selecciona `My IP` (Recomendado por seguridad: solo tu computadora podrá entrar).
4.  **Limpieza:** Si ves reglas con puertos extraños o en `0`, elimínalas para evitar vulnerabilidades.
5.  Haz clic en **"Save rules"**.

---

## 4. Paso 2: Transferencia de Datos a la Nube (SCP)

> **Pre-requisito:** El archivo ya está corregido (sin DROP DATABASE). Sube el archivo tal cual.

Desde la terminal de tu **máquina local** (donde tienes el repositorio `ApuntesSQL`), envía el dataset a tu servidor.

```bash
# Formato: scp -i "tu-llave.pem" [archivo_origen] ubuntu@[ip_publica]:[destino]
scp -i "tu-llave.pem" ./PostgresSQL/db_northwind.sql ubuntu@tu-ip-publica:/home/ubuntu/
```

---

## 5. Paso 3: Conexión y Preparación del Servidor (SSH)

Conéctate a tu instancia EC2:

```bash
ssh -i "tu-llave.pem" ubuntu@tu-ip-publica
```

Ya dentro del servidor Ubuntu, prepara la estructura de directorios:

```bash
# Crear directorio del proyecto y de inicialización
mkdir -p ~/postgres-lab/init

# Mover el archivo SQL que subimos por SCP a la carpeta de inicialización
mv ~/db_northwind.sql ~/postgres-lab/init/

# Entrar a la carpeta del proyecto
cd ~/postgres-lab
```

---

## 6. Paso 4: Definición de la Infraestructura (YAML)

Crea el archivo que orquestará el motor de base de datos:

```bash
nano docker-compose.yml
```

Pega el siguiente contenido (Configuración de Arquitecto Senior):

```yaml
services:
  db:
    image: postgres:16-alpine
    container_name: pg_architect_lab
    restart: always
    environment:
      POSTGRES_USER: slinkter
      POSTGRES_PASSWORD: slinkter # <-- DEFINE UNA CLAVE SEGURA
      POSTGRES_DB: northwind
    ports:
      - "5432:5432"
    volumes:
      # Persistencia: Los datos viven en el disco del EC2, no solo en el contenedor
      - pg_data:/var/lib/postgresql/data
      # AUTOMATIZACIÓN: El SQL se ejecutará automáticamente al crear el contenedor
      # Docker mapea tu archivo local al directorio de inicio de Postgres
      - ./init/db_northwind.sql:/docker-entrypoint-initdb.d/db_northwind.sql
    networks:
      - pg_network

networks:
  pg_network:
    driver: bridge

volumes:
  pg_data:
```
*Guardar: Ctrl+O, Enter. Salir: Ctrl+X.*

---

## 7. Paso 5: Lanzamiento y Magia de Inicialización

Levanta el sistema:

```bash
docker compose up -d
```

**Súper Importante:** No necesitas ejecutar el script SQL manualmente. Gracias al volumen configurado en el YAML (`/docker-entrypoint-initdb.d/`), PostgreSQL detecta el archivo `db_northwind.sql` y lo ejecuta automáticamente durante la creación de la base de datos.

Verifica que el script se haya ejecutado correctamente mirando los logs:

```bash
docker logs -f pg_architect_lab
```
*Deberías ver una secuencia de comandos CREATE TABLE e INSERT. Al final aparecerá: `PostgreSQL init process complete; ready for start up.`*

---

## 8. Paso 6: Prueba de Integridad y Conexión

### Opción A: Acceso rápido desde la EC2 (Terminal)
Accede al motor dentro del contenedor:

```bash
docker exec -it pg_architect_lab psql -U slinkter -d northwind
```

### Opción B: Conexión desde tu PC Local (Ideal para estudiar)
Si tienes `psql` instalado en tu computadora, puedes conectarte directamente a tu servidor de AWS:

```bash
psql -h tu-ip-publica-aws -U slinkter -d northwind
```
*(Recuerda que para esto el Puerto 5432 debe estar abierto en el Security Group de AWS).*

Ejecuta estas consultas de validación:
```sql
-- Listar tablas cargadas
\dt

-- Validar conteo de registros en una tabla clave
SELECT count(*) FROM customers;

-- Salir de psql
\q
```

---

## 9. Análisis de Ingeniería Real

*   **Idempotencia:** Si borras el contenedor y lo vuelves a levantar, la data persiste gracias al volumen `pg_data`.
*   **Alpine v16:** Utilizamos la versión más ligera y reciente para optimizar recursos en la nube.
*   **Separación de Preocupaciones:** El script SQL solo se encarga de la data; el YAML se encarga de la infraestructura.

---

## 10. Conexión desde VSCode (Local)

### Instalación de la Extensión

1. Ve a `Extensions` en VSCode (Ctrl+Shift+X)
2. Busca `PostgreSQL` (extensión de `cweiln` o `mtxr`)
3. Instala la extensión

### Configuración de Conexión

1. Presiona `Ctrl+Shift+P` → "PostgreSQL: New Connection"
2. O haz clic en el icono de base de datos en la barra lateral

Configura los parámetros:

| Campo | Valor |
|------|-------|
| Server name | Tu IP pública de EC2 (ej: `18.224.200.26`) |
| Authentication Type | `Password` |
| User name | `slinkter` |
| Password | `slinkter` |
| Database | `northwind` |
| Port | `5432` |

### Solución de SSL

Si aparece error de SSL:

1. Click en **Advanced**
2. Configura:
   - **SSL:** `false` o `disable`
   - **Trust Server Certificate:** `true`

O usa Connection String:
```
postgresql://slinkter:slinkter@TU-IP:5432/northwind?sslmode=disable
```

### Verificación

Ejecuta una query de prueba:

```sql
SELECT count(*) FROM customers;
SELECT company_name, city FROM customers LIMIT 5;
```

---

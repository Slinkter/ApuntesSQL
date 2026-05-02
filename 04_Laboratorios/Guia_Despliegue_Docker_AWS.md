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

---

## 3. Paso 1: Configuración de Red en AWS (Security Groups)

Antes de conectar, asegúrate de que AWS permita el tráfico:
1.  Consola EC2 > **Security Groups** > Selecciona el de tu instancia.
2.  **Inbound Rules** > **Edit inbound rules**.
3.  Agregar: `PostgreSQL` (5432) | Source: `My IP` o `Anywhere` (0.0.0.0/0).
4.  Guardar.

---

## 4. Paso 2: Transferencia de Datos a la Nube (SCP)

Desde la terminal de tu **máquina local** (donde tienes el repositorio `ApuntesSQL`), envía el dataset a tu servidor.

```bash
# Formato: scp -i "tu-llave.pem" [archivo_origen] ubuntu@[ip_publica]:[destino]
scp -i "tu-acceso.pem" ./PostgresSQL/db_northwind.sql ubuntu@tu-ip-publica-aws:/home/ubuntu/
```

---

## 5. Paso 3: Conexión y Preparación del Servidor (SSH)

Conéctate a tu instancia EC2:

```bash
ssh -i "tu-acceso.pem" ubuntu@tu-ip-publica-aws
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
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: pg_architect_lab
    restart: always
    environment:
      POSTGRES_USER: architect
      POSTGRES_PASSWORD: your_secure_password # <-- DEFINE UNA CLAVE SEGURA
      POSTGRES_DB: northwind
    ports:
      - "5432:5432"
    volumes:
      # Persistencia: Los datos viven en el disco del EC2, no solo en el contenedor
      - pg_data:/var/lib/postgresql/data
      # Init Script: El SQL se ejecutará automáticamente al crear el contenedor
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

## 7. Paso 5: Lanzamiento y Verificación del Log

Levanta el sistema:

```bash
docker compose up -d
```

**CRUCIAL:** Verifica que el script SQL se haya ejecutado correctamente. Mira los logs del proceso de inicio:

```bash
docker logs -f pg_architect_lab
```
*Deberías ver una secuencia de comandos CREATE TABLE e INSERT. Al final aparecerá: `PostgreSQL init process complete; ready for start up.`*

---

## 8. Paso 6: Prueba de Integridad (SQL)

Accede al motor dentro del contenedor para validar que la data existe:

```bash
docker exec -it pg_architect_lab psql -U architect -d northwind
```

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

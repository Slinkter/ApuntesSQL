# Reporte de Auditoría Técnica y Recomendaciones de Infraestructura & Despliegue (PostgreSQL Lab01)

**Agente:** Explorer Infra (`explorer_infra_1`)  
**Fecha:** 2026-08-22  
**Alcance:** Docker, Docker Compose, AWS EC2 (Amazon Linux 2023 / Ubuntu 24.04), Seguridad de Red, Transferencia de Archivos, Carga de Northwind, Conectividad y Ciclo de Vida.

---

## 1. Observaciones Directas (Observations)

A partir de la inspección exhaustiva de los archivos de configuración, guías y scripts del repositorio (`Lab/Lab01/1.Guia/`, `Lab/Lab01/2.Ejercicios/` y raíz del proyecto):

### 1.1 Inconsistencia y Rutas Rotas en Comandos SCP y Guías
- **Observación 1.1.1:** En `Lab/Lab01/1.Guia/0.Guia_Docker_AWS.md` (líneas 75, 78, 81, 87, 90, 93), los comandos `scp` hacen referencia a una ruta inexistente `.\Lab\Lab01\aws\...`:
  ```powershell
  scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\aws\docker-compose.yml ec2-user@<IP_AWS_EC2>:/home/ec2-user/
  scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\aws\.env ec2-user@<IP_AWS_EC2>:/home/ec2-user/
  scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\aws\db_northwind.sql ec2-user@<IP_AWS_EC2>:/home/ec2-user/
  ```
  **Evidencia:** La estructura real del repositorio contiene los archivos en `Lab\Lab01\1.Guia\Material\docker-compose.yml` y `Lab\Lab01\1.Guia\Material\db_northwind.sql`. La carpeta `aws/` no existe.
- **Observación 1.1.2:** En `Lab/Lab01/1.Guia/README.md` (líneas 13-15) se enlazan rutas relativas rotas:
  - `[`aws/Guia_Docker_AWS.md`](aws/Guia_Docker_AWS.md)` (el archivo real es `0.Guia_Docker_AWS.md`).
  - `[`aws/docker-compose.yml`](aws/docker-compose.yml)` (el archivo real es `Material/docker-compose.yml`).
  - `[`aws/db_northwind.sql`](aws/db_northwind.sql)` (el archivo real es `Material/db_northwind.sql`).

### 1.2 Archivo `.env` Inexistente y Falta de Fallbacks en `docker-compose.yml`
- **Observación 1.2.1:** No existe ningún archivo `.env` ni `.env.example` en `Lab/Lab01/1.Guia/Material/` ni en la raíz del repositorio.
- **Observación 1.2.2:** En `Lab/Lab01/1.Guia/Material/docker-compose.yml` (líneas 7-9):
  ```yaml
  environment:
    POSTGRES_USER: ${POSTGRES_USER}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    POSTGRES_DB: ${POSTGRES_DB}
  ```
  Si el estudiante ejecuta `docker compose up -d` sin un archivo `.env` creado, Docker Compose emite advertencias de variables no definidas y PostgreSQL falla al iniciar o toma valores vacíos.

### 1.3 Comando Peligroso en Troubleshooting de la Guía
- **Observación 1.3.1:** En `Lab/Lab01/1.Guia/0.Guia_Docker_AWS.md` (línea 164), la tabla de troubleshooting sugiere:
  > `Salió el error "no such file" al mover .env` $\rightarrow$ `Prueba con mv ~/.* ~/postgres-lab/`
  
  **Riesgo Crítico:** En shells Bash/POSIX, el glob `~/.*` expande a `~/.`, `~/..`, `~/.ssh`, `~/.bashrc`, `~/.bash_profile`. Mover `~/.ssh` a un subdirectorio **elimina la llave autorizada del usuario y rompe irreversiblemente el acceso SSH** a la instancia EC2.

### 1.4 Discrepancias en Nombre de Contenedores y Credenciales
- **Observación 1.4.1:** En `Lab/Lab01/1.Guia/Material/docker-compose.yml` (línea 4) y `0.Guia_Docker_AWS.md` (línea 139) el contenedor se nombra `pg_architect_lab`.
- **Observación 1.4.2:** En `Lab/Lab01/2.Ejercicios/0.prerrequisitos.md` (líneas 306, 317, 342, 355, 406) el contenedor se nombra `pg_northwind_lab`.
- **Observación 1.4.3:** En `0.Guia_Docker_AWS.md` se usan las credenciales `POSTGRES_USER=slinkter`, `POSTGRES_PASSWORD=postgres` (o variable), mientras que en `0.prerrequisitos.md` se usan `POSTGRES_USER=postgres`, `POSTGRES_PASSWORD=postgres`.

### 1.5 Permisos de la Llave SSH Privada (`key_u_docker.pem`)
- **Observación 1.5.1:** `Credenciales/key_u_docker.pem` existe en la raíz del proyecto. Sin embargo, en Windows y Linux, los clientes OpenSSH rechazan conexiones (`UNPROTECTED PRIVATE KEY FILE!`) si los permisos del archivo permiten lectura a otros usuarios o grupos. La guía no incluye los comandos `icacls` (PowerShell) ni `chmod 400` (Linux/Mac/WSL) para asegurar la llave.

### 1.6 Comportamiento del Directorio `/docker-entrypoint-initdb.d/`
- **Observación 1.6.1:** `docker-compose.yml` mapea `./init/db_northwind.sql` a `/docker-entrypoint-initdb.d/db_northwind.sql`.
- **Observación 1.6.2:** La imagen oficial de PostgreSQL (`postgres:16-alpine`) ejecuta scripts en `/docker-entrypoint-initdb.d/` **únicamente si el directorio de datos `/var/lib/postgresql/data` está vacío (primer arranque)**. Si el contenedor se ejecuta una vez sin el archivo `.sql`, el volumen `pg_data` se inicializa y cualquier ejecución posterior ignora el script. Esta condición esencial no está explicada en la guía.

### 1.7 Scripts de User Data y Concurrencia de Arranque
- **Observación 1.7.1:** Los scripts de User Data se ejecutan de forma asíncrona mediante `cloud-init` durante el primer arranque. Si el estudiante se conecta por SSH de inmediato (en los primeros 30-60 segundos tras el aprovisionamiento), Docker o Docker Compose pueden no haber terminado de instalarse, provocando errores de `command not found` o `permission denied`.
- **Observación 1.7.2:** No se incluye la instrucción para inspeccionar el avance de `cloud-init` (`tail -f /var/log/cloud-init-output.log`).

---

## 2. Cadena Lógica (Logic Chain)

1. **Rutas e Integridad de Archivos:** Dado que `0.Guia_Docker_AWS.md` indica comandos `scp` apuntando a `.\Lab\Lab01\aws\...`, cualquier estudiante que clone el repositorio y ejecute los comandos al pie de la letra experimentará un error inmediato de archivo no encontrado (`No such file or directory`), bloqueando el laboratorio en la Fase 2.
2. **Autenticación e Inicialización de Compose:** Al carecer de `.env.example` y no definir valores por defecto en `${POSTGRES_USER:-slinkter}`, `${POSTGRES_PASSWORD:-postgres123}`, `${POSTGRES_DB:-northwind}`, Docker Compose deja variables vacías. Esto genera advertencias y crea bases de datos con configuraciones no deseadas.
3. **Seguridad y Disponibilidad del Servidor:** Sugerir `mv ~/.* ~/postgres-lab/` es una instrucción destructiva que compromete `~/.ssh/authorized_keys`. Un flujo robusto debe transferir los archivos directamente a sus directorios finales (`~/postgres-lab/` y `~/postgres-lab/init/`) sin operaciones masivas de movimiento con comodines.
4. **Seguridad de Red en AWS:** Abrir el puerto 5432 a `0.0.0.0/0` expone el motor a escaneos y ataques de fuerza bruta automatizados en Internet. El firewall (Security Group) debe restringir el puerto 22 (SSH) y 5432 (PostgreSQL) estrictamente a la IP pública del estudiante (`My IP` / `/32`). Asimismo, debe instruirse sobre el cambio de IP pública dinámica del proveedor de internet (ISP) y de la instancia EC2 tras un reinicio.
5. **Consistencia Didáctica:** Las discrepancias en nombres de contenedores (`pg_architect_lab` vs `pg_northwind_lab`) y usuarios (`slinkter` vs `postgres`) entre la guía de infraestructura y el libro de ejercicios generan fricción cognitiva y errores al ejecutar comandos `docker exec` o `psql`.

---

## 3. Salvedades y Supuestos (Caveats)

1. **Validez de Credenciales AWS:** Se asume que el usuario IAM `u_docker` tiene permisos suficientes de `ec2:RunInstances`, `ec2:DescribeInstances`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress` y acceso a la VPC por defecto en la región configurada (por ejemplo, `us-east-1`).
2. **IP Dinámica:** Si el estudiante tiene conexión residencial con IP pública dinámica, su IP cambiará al reiniciar el router, requiriendo actualizar la regla de entrada en el Security Group de AWS.
3. **IP Pública de EC2 tras Detener/Iniciar:** Al detener (`Stop`) e iniciar (`Start`) una instancia EC2 sin Elastic IP asignada, AWS asigna una nueva dirección IPv4 pública. El estudiante debe actualizar la IP en sus comandos SSH y en la conexión de VSCode.
4. **Compatibilidad de Docker en Windows/Linux/macOS:** El laboratorio soporta tanto ejecución remota en AWS EC2 como ejecución local con Docker Desktop en Windows/Mac o Docker Engine en Linux.

---

## 4. Conclusiones y Recomendaciones de Implementación

Para garantizar una experiencia 100% libre de errores, segura y profesional, se formulan las siguientes soluciones y especificaciones exactas para los implementadores:

### 4.1 Creación de `.env.example` y `.env` en `Lab/Lab01/1.Guia/Material/`
Crear el archivo `.env.example` (y `.env` por defecto) con la siguiente estructura:
```bash
# Credenciales y Configuración del Contenedor PostgreSQL
POSTGRES_USER=slinkter
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=northwind
PGPORT=5432
```

### 4.2 Optimización de `Lab/Lab01/1.Guia/Material/docker-compose.yml`
Reforzar el manifiesto con valores por defecto, directiva de solo lectura para el dump SQL, límites de memoria y política de logs:
```yaml
services:
  db:
    image: postgres:16-alpine
    container_name: pg_architect_lab
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-slinkter}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres123}
      POSTGRES_DB: ${POSTGRES_DB:-northwind}
    ports:
      - "${PGPORT:-5432}:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
      - ./init/db_northwind.sql:/docker-entrypoint-initdb.d/01_db_northwind.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-slinkter} -d ${POSTGRES_DB:-northwind}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - pg_network

networks:
  pg_network:
    driver: bridge

volumes:
  pg_data:
```

### 4.3 Estandarización de Comandos de Transferencia Directa (SCP)
Reemplazar las rutas erróneas y la técnica insegura de movimiento de archivos por la subida directa a los directorios de destino:

```powershell
# En tu terminal local (PowerShell), ubicado en la raíz del repositorio:

# 1. Asegurar permisos de la llave en Windows (si es necesario)
icacls ".\Credenciales\key_u_docker.pem" /inheritance:r
icacls ".\Credenciales\key_u_docker.pem" /grant:r "$($env:USERNAME):(R)"

# 2. Crear las carpetas de trabajo en la instancia EC2 de forma remota
ssh -i ".\Credenciales\key_u_docker.pem" ec2-user@<IP_AWS_EC2> "mkdir -p ~/postgres-lab/init"

# 3. Subir el archivo de orquestación (docker-compose.yml)
scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\1.Guia\Material\docker-compose.yml ec2-user@<IP_AWS_EC2>:~/postgres-lab/

# 4. Subir las variables de entorno (.env)
scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\1.Guia\Material\.env ec2-user@<IP_AWS_EC2>:~/postgres-lab/

# 5. Subir el script de base de datos Northwind (.sql) directamente a ~/postgres-lab/init/
scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\1.Guia\Material\db_northwind.sql ec2-user@<IP_AWS_EC2>:~/postgres-lab/init/
```

*(Para Ubuntu Server, cambiar `ec2-user` por `ubuntu`).*

### 4.4 Guía Paso a Paso de Despliegue en AWS EC2 (Sin Pasos Omitidos)

1. **Aprovisionamiento EC2:**
   - **Región:** `us-east-1` (N. Virginia).
   - **Nombre:** `postgres-docker-lab`.
   - **AMI:** Amazon Linux 2023 (`al2023-ami-*-kernel-6.1-x86_64`) o Ubuntu 24.04 LTS.
   - **Tipo de Instancia:** `t3.micro` (o `t2.micro`).
   - **Key Pair:** Seleccionar `key_u_docker`.
   - **Configuración de Red (VPC):**
     - Subred: Pública.
     - **Auto-assign Public IP:** `Enable` (**Obligatorio**).
     - **Security Group (Reglas de Entrada):**
       - Regla 1: SSH (TCP 22) $\rightarrow$ Source: `My IP` (`<Tu_IP>/32`).
       - Regla 2: Custom TCP (5432) $\rightarrow$ Source: `My IP` (`<Tu_IP>/32`).
   - **User Data (Advanced Details):**
     - Para Amazon Linux 2023:
       ```bash
       #!/bin/bash
       dnf update -y
       dnf install -y docker
       systemctl enable --now docker
       usermod -aG docker ec2-user
       mkdir -p /usr/local/lib/docker/cli-plugins
       curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m) -o /usr/local/lib/docker/cli-plugins/docker-compose
       chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
       ```
     - Para Ubuntu 24.04:
       ```bash
       #!/bin/bash
       apt-get update -y
       apt-get install -y docker.io docker-compose-v2
       usermod -aG docker ubuntu
       systemctl enable --now docker
       ```

2. **Conexión SSH y Validación de Inicialización:**
   ```bash
   # Conectar
   ssh -i ".\Credenciales\key_u_docker.pem" ec2-user@<IP_AWS_EC2>

   # Verificar que cloud-init terminó la instalación de Docker
   cat /var/log/cloud-init-output.log | grep -i "complete"
   docker --version
   docker compose version
   ```

3. **Ejecución y Verificación del Contenedor:**
   ```bash
   cd ~/postgres-lab
   docker compose up -d

   # Monitorear logs de inicialización
   docker compose logs -f db
   # Esperar mensaje: "PostgreSQL init process complete; ready for start up."
   ```

4. **Verificación de Datos Cargados:**
   ```bash
   # Conectar a psql dentro del contenedor
   docker exec -it pg_architect_lab psql -U slinkter -d northwind

   # En el prompt de psql:
   \dt
   SELECT count(*) FROM employees;   -- Retorna 9
   SELECT count(*) FROM orders;      -- Retorna 830
   SELECT count(*) FROM products;    -- Retorna 77
   SELECT count(*) FROM customers;   -- Retorna 91
   \q
   ```

5. **Conexión desde VSCode / DBeaver:**
   - **Host:** `<IP_AWS_EC2>`
   - **Port:** `5432`
   - **Database:** `northwind`
   - **Username:** `slinkter`
   - **Password:** `postgres123`
   - **SSL Mode:** `disable` o `prefer`

6. **Gestión de Costos y Apagado (Teardown):**
   - Al terminar el laboratorio:
     - Ir a consola AWS $\rightarrow$ EC2 $\rightarrow$ Instances.
     - Seleccionar la instancia $\rightarrow$ **Instance state** $\rightarrow$ **Stop instance** (para pausar sin perder configuración) o **Terminate instance** (para eliminarla por completo y liberar almacenamiento EBS).

---

## 5. Método de Verificación (Verification Method)

Para validar de forma independiente las correcciones propuestas:

1. **Verificación Local de Manifiesto Docker:**
   ```bash
   # Comprobar sintaxis de docker-compose.yml
   docker compose -f Lab/Lab01/1.Guia/Material/docker-compose.yml config
   ```
2. **Verificación de Conectividad de Red y Puertos (desde PowerShell local):**
   ```powershell
   Test-NetConnection -ComputerName <IP_AWS_EC2> -Port 22
   Test-NetConnection -ComputerName <IP_AWS_EC2> -Port 5432
   ```
3. **Verificación del Esquema Northwind:**
   Ejecutar la consulta de control de integridad de tablas:
   ```sql
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public' 
   ORDER BY table_name;
   ```
   Debe retornar exactamente las 14 tablas canónicas: `categories`, `customer_customer_demo`, `customer_demographics`, `customers`, `employee_territories`, `employees`, `order_details`, `orders`, `products`, `region`, `shippers`, `suppliers`, `territories`, `us_states`.
4. **Verificación de Manejo de Volúmenes en Reinicio:**
   ```bash
   # Reiniciar contenedor sin borrar volumen (los datos persisten)
   docker compose restart
   docker exec -it pg_architect_lab psql -U slinkter -d northwind -c "SELECT count(*) FROM orders;"
   # Debe retornar 830 inmediatamente.
   ```

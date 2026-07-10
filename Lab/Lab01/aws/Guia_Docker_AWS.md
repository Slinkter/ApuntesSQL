# 🚀 Laboratorio: Despliegue de Arquitectura de Datos en AWS con Docker (End-to-End)

**Instructor:** Principal Data Architect
**Enfoque:** Conectividad, Persistencia y Orquestación de Bases de Datos.

---

## 1. Introducción y Objetivo
Este laboratorio tiene como objetivo llevar la base de datos **Northwind** desde tu computadora local hacia una instancia de servidor en la nube (**AWS EC2**), utilizando **Docker Compose** para asegurar que la base de datos funcione exactamente igual en cualquier entorno.

Aprenderás la metodología profesional de despliegue: separar la infraestructura (`.yaml`), las credenciales (`.env`) y los datos (`.sql`).

### 🔑 Datos de Acceso a AWS
| Recurso | Valor | Notas |
| :--- | :--- | :--- |
| **Console URL** | `https://629017097739.signin.aws.amazon.com/console` | Portal de gestión de AWS |
| **User** | `u_docker` | Usuario asignado para el lab |
| **Password** | *Usa la contraseña de tu cuenta* | Requerido para entrar a la consola |

---

## 🏗️ Fase 1: Lanzamiento de la Infraestructura (AWS EC2)

### 1.1 Crear la Instancia
Desde la consola AWS, ve a **EC2 > Instances > Launch instances**.
- **Nombre:** `postgres-docker-lab`
- **AMI:** Ubuntu Server 24.04 LTS
- **Tipo de instancia:** `t3.micro` (Capa gratuita)
- **Key pair:** `key_u_docker` (Fundamental: sin esta llave no podrás entrar al servidor)

### 1.2 Configurar el Firewall (Security Group)
Para que tu computadora pueda hablar con el servidor en la nube, debes abrir los puertos correctos.
En **Network settings > Edit**:
1. **SSH (Puerto 22)** $\rightarrow$ Source: `My IP` (Permite entrar a la terminal)
2. **PostgreSQL (Puerto 5432)** $\rightarrow$ Source: `My IP` (Permite que VSCode consulte la base)

### 1.3 Instalación Automática de Docker (User Data)
En **Advanced details**, al final en **User data**, pega este script para que el servidor ya tenga Docker instalado al encender:
```bash
#!/bin/bash
sudo apt update -y
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
```

---

## 🌐 Fase 2: Transferencia de Archivos (Local $\rightarrow$ Nube)

En la industria, no escribimos archivos complejos manualmente en la terminal. Los preparamos en nuestra máquina y los "subimos" al servidor.

Utilizaremos el comando `SCP` (Secure Copy). Ejecuta estos comandos en tu terminal local (**PowerShell**), asegurándote de estar en la raíz del proyecto:

### 2.1 Subir los archivos de configuración y datos
Sube el archivo de orquestación, el de variables y el dataset desde la carpeta `aws`:

```powershell
# 1. Subir el archivo de orquestación (Infraestructura)
scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\aws\docker-compose.yml ubuntu@<IP_AWS_EC2>:/home/ubuntu/

# 2. Subir el archivo de variables (Credenciales)
scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\aws\.env ubuntu@<IP_AWS_EC2>:/home/ubuntu/

# 3. Subir el dataset (Datos)
scp -i ".\Credenciales\key_u_docker.pem" .\Lab\Lab01\aws\db_northwind.sql ubuntu@<IP_AWS_EC2>:/home/ubuntu/
```

---

## 🚀 Fase 3: Despliegue con Docker Compose (En la Nube)

Ahora que los archivos están en la nube, vamos a organizarlos y encender el motor.

### 3.1 Conexión SSH
Entra al servidor:
```powershell
ssh -i ".\Credenciales\key_u_docker.pem" ubuntu@<IP_AWS_EC2>
```

### 3.2 Organizar la Estructura de Carpetas
Postgres necesita que el archivo `.sql` esté en una carpeta específica para cargarlo automáticamente al inicio.
```bash
# Crear carpeta del proyecto y subcarpeta de inicialización
mkdir -p ~/postgres-lab/init

# Mover los archivos subidos a su lugar correspondiente
mv ~/db_northwind.sql ~/postgres-lab/init/
mv ~/docker-compose.yml ~/postgres-lab/
mv ~/.env ~/postgres-lab/

# Entrar al directorio del proyecto
cd ~/postgres-lab
```

### 3.3 Lanzamiento del Sistema
Ejecuta el orquestador. Docker Compose leerá el `.yaml` y el `.env` para levantar la base de datos:
```bash
docker compose up -d
```

### 3.4 Verificación de Carga de Datos
Sigue los logs para confirmar que el archivo `db_northwind.sql` se ejecutó correctamente:
```bash
docker logs -f pg_architect_lab
```
*   **Éxito:** Busca la línea `PostgreSQL init process complete; ready for start up`.

---

## 🖥️ Fase 4: Conexión Final desde VSCode

1.  **Extensión:** Instala **PostgreSQL** de Microsoft.
2.  **Nueva Conexión:**
    - **Server:** `<IP_AWS_EC2>`
    - **User:** El valor de `POSTGRES_USER` en tu archivo `.env` (ej: `slinkter`)
    - **Password:** El valor de `POSTGRES_PASSWORD` en tu archivo `.env`
    - **Database:** El valor de `POSTGRES_DB` en tu archivo `.env` (ej: `northwind`)
3.  **Súper Importante (SSL):** Haz clic en **Advanced** $\rightarrow$ **SSL mode** $\rightarrow$ cambiar a `disable`.

---

## 🛠️ Tabla de Troubleshooting

| Error | Causa probable | Solución |
| :--- | :--- | :--- |
| `Connection timed out` | Firewall de AWS bloqueando el puerto | Security Group $\rightarrow$ Inbound Rules $\rightarrow$ Puerto 5432 para `My IP`. |
| `Permission denied (publickey)` | Ruta de llave `.pem` incorrecta | Usa ruta completa: `.\Credenciales\key_u_docker.pem`. |
| `no pg_hba.conf entry` | Configuración de acceso interna de Postgres | Ver sección de errores avanzados en la guía. |
| `Salió el error "no such file" al mover .env` | El archivo `.env` es oculto en algunos sistemas | Prueba con `mv ~/.* ~/postgres-lab/` o verifica con `ls -a`. |

---

## 💡 Apéndice: Opción Alternativa (Método Standalone)
*Solo recomendado para pruebas rápidas donde no necesites persistencia de datos.*

Si no quieres usar Compose, puedes lanzar la base de datos con un único comando dentro del SSH:
```bash
docker run --name pg_quick_lab \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=northwind \
  -v /home/ubuntu/db_northwind.sql:/docker-entrypoint-initdb.d/db_northwind.sql \
  -p 5432:5432 \
  -d postgres:16-alpine
```

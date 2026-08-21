# Instalaciones Necesarias para el Curso de SQL

> **Analogia:** Imagina que quieres cocinar. Necesitas una cocina (Docker), ingredientes (MySQL/PostgreSQL), utensilios para servir (TablePlus/DBeaver), y un libro de recetas (VS Code). Sin estas herramientas, no podés preparar nada. Cada herramienta cumple un rol específico en tu flujo de trabajo con bases de datos.

Antes de empezar a escribir consultas SQL, necesitás tener las herramientas básicas instaladas. En esta guía te explico para qué sirve cada una y cómo verificar que todo esté funcionando correctamente.

---

#### 1. Docker

[Docker](https://www.docker.com/get-started/) es una plataforma que permite crear **contenedores** con bases de datos aisladas. En lugar de instalar MySQL o PostgreSQL directamente en tu computadora, Docker corre cada base de datos en un entorno separado que no afecta tu sistema operativo.

> **Analogia:** Docker es como una caja de herramientas portátil. Cada herramienta (base de datos) vive en su propia caja, y podés abrir o cerrar cada caja sin que interfieran entre sí.

**Por qué lo necesitás:**
- Correr múltiples versiones de MySQL o PostgreSQL sin conflictos.
- Destruir y recrear entornos de prueba en segundos.
- Trabajar de forma consistente con tu equipo.

**Verificación de instalación:**

```bash
docker --version
docker ps
```

> Si ves la versión de Docker y una tabla vacía (o contenedores corriendo), todo está bien.

#### 1.1 PostgreSQL con Docker (alternativa)

Si preferís trabajar con PostgreSQL en lugar de (o junto a) MySQL:

```bash
docker run --name postgres-sql -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres:16
```

> **Tip del Profesor:** Siempre asigná un nombre descriptivo al contenedor (`postgres-sql` en vez de algo genérico). Cuando tengas 10 contenedores, te lo vas a agradecer.

**Verificación:**

```bash
docker ps | grep postgres-sql
```

#### 1.2 MySQL con Docker

```bash
docker run --name mysql-sql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 -d mysql:8
```

**Verificación:**

```bash
docker ps | grep mysql-sql
```

> **MySQL vs PostgreSQL:** Ambos se ejecutan como contenedores de Docker de forma idéntica. La diferencia está en el motor de base de datos y la sintaxis SQL que veremos en los siguientes talleres.

---

#### 2. TablePlus / DBeaver

Estos son **clientes de bases de datos** con interfaz gráfica. Te permiten conectarte al motor (MySQL o PostgreSQL) y ejecutar consultas, ver tablas, editar datos y más.

- [TablePlus](https://tableplus.com/) - Ligero, rápido, multiplataforma. Ideal para empezar.
- [DBeaver](https://dbeaver.io/) - Gratuito, soporta decenas de bases de datos. Más completo.

> **Analogia:** TablePlus/DBeaver es como el panel de control de tu auto. Desde ahí ves todo lo que pasa dentro del motor (la base de datos): tablas, datos, relaciones, errores.

**Verificación de instalación:**
- Abrí la aplicación y creá una conexión nueva apuntando a `localhost:3306` (MySQL) o `localhost:5432` (PostgreSQL).

**Tip del Profesor:** TablePlus tiene una versión gratuita limitada. DBeaver es completamente gratuito. Si recién empezás, te recomiendo DBeaver por su amplitud de soporte.

---

#### 3. MySQL Workbench

[MySQL Workbench](https://www.mysql.com/products/workbench/) es la herramienta oficial de MySQL para diseño, administración y consultas. Incluye herramientas de modelado de esquemas y asistentes visuales.

> **Analogia:** Si TablePlus es una navaja suiza, MySQL Workbench es un taller completo de MySQL: tiene de todo, pero solo para una marca.

**Verificación de instalación:**
- Abrí Workbench y conectate con los mismos datos que usaste en TablePlus/DBeaver.

> **MySQL vs PostgreSQL:** Para PostgreSQL, la herramienta equivalente es **pgAdmin** (se instala junto con PostgreSQL o se descarga desde [pgadmin.org](https://www.pgadmin.org/)). Ambas permiten ejecutar consultas, ver esquemas y administrar usuarios.

---

#### 4. Editor de código

- [Visual Studio Code](https://code.visualstudio.com/download) es el editor más utilizado. Instalá la extensión **SQL** para syntax highlighting y autocompletado.

> **Tip del Profesor:** VS Code no ejecuta SQL directamente, pero te permite escribir archivos `.sql` con colores y ayuda. Cuando tengas archivos de varias líneas, es mucho más cómodo que escribir en la consola.

---

#### 5. Herramientas complementarias (práctica avanzada)

Estas herramientas se usan más adelante en el curso:

- [Google Chrome](https://www.google.com/intl/es_es/chrome/) - Navegador web.
- [Git](https://git-scm.com/) - Manejador de versiones para controlar cambios en tu código.
- [Postman](https://www.postman.com/downloads/) - Para probar APIs HTTP.

---

#### 6. Playground sin instalaciones

Si querés practicar SQL sin instalar nada, podés usar un playground online:

- [SQL Playground](https://runsql.com/r) - Ejecutá consultas directamente en el navegador.

> **Tip del Profesor:** Los playgrounds online son útiles para práctica rápida, pero no reemplazan un entorno local. Cuando trabajes con datos reales o múltiples tablas, necesitás Docker y un cliente de BD.

---

### Resumen de herramientas

| Herramienta | Propósito | Obligatoria |
|---|---|---|
| Docker | Correr MySQL/PostgreSQL en contenedores | Si |
| TablePlus / DBeaver | Cliente gráfico para consultar y administrar | Si |
| MySQL Workbench | Herramienta oficial de MySQL | No |
| pgAdmin | Herramienta oficial de PostgreSQL | No |
| VS Code | Editor de código `.sql` | Recomendada |
| Git | Control de versiones | Solo práctica avanzada |
| Postman | Probar APIs | Solo práctica avanzada |

> **Tip del Profesor:** Si tenés problemas con Docker, podés instalar MySQL y PostgreSQL directamente en tu sistema. Sin embargo, Docker facilita mucho la vida cuando necesitás recrear entornos o trabajar con varias versiones.

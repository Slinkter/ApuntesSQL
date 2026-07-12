# ApuntesSQL — Plan de Maestria en SQL

Repositorio de notas de estudio, laboratorios practicos y recursos para dominar **SQL** (PostgreSQL y MySQL) y la **Teoria Relacional de Bases de Datos**. Estructurado en pistas teoricas (metodo Cornell) y practicas interactivas basadas en escenarios reales.

---

## Estructura de Contenidos

| Componente | Ruta | Descripcion |
| :--- | :--- | :--- |
| **Dashboard Academico** | [ULima/Apuntes/index.html](ULima/Apuntes/index.html) | Indice interactivo con acceso a las 16 semanas de clase y examenes. |
| **Semanas Academicas** | [ULima/Apuntes/semana_01.html](ULima/Apuntes/semana_01.html) a [semana_15.html](ULima/Apuntes/semana_15.html) | Apuntes detallados en HTML estilo Cornell con widgets interactivos. |
| **Examen Parcial & Final** | [semana_08.html](ULima/Apuntes/semana_08.html) y [semana_16.html](ULima/Apuntes/semana_16.html) | Simulacros con cuestionario teorico y desarrollo practico (incluye solucionario). |
| **Lab01 — Ejercicios PostgreSQL** | [Lab/Lab01/Ejercicios/](Lab/Lab01/Ejercicios/) | 150 problemas con esquema Northwind: [basico](Lab/Lab01/Ejercicios/1.basico.md), [intermedio](Lab/Lab01/Ejercicios/2.intermedio.md), [avanzado](Lab/Lab01/Ejercicios/3.avanzado.md), [examen entrevista](Lab/Lab01/Ejercicios/4.examen_entrevista.md). |
| **Lab01 — Dataset** | [db_northwind.sql](Lab/Lab01/aws/db_northwind.sql) | Script para inicializar el esquema Northwind en PostgreSQL. |
| **Lab02 — Taller MySQL/PostgreSQL** | [Lab/Lab02/](Lab/Lab02/) | Guias de DDL/DML, JOINs, subconsultas, buenas practicas con Docker Compose. |
| **Guia de Despliegue Cloud** | [Guia_Despliegue_Docker_AWS.md](SQL/Youtube00/Guia_Despliegue_Docker_AWS.md) | Despliegue de PostgreSQL en AWS EC2 con Docker. |

---

## Cliente SQL Recomendado

Para practicar queries se recomienda **DBeaver** (gratis, multiplataforma):

| Cliente | Ventaja | Instalacion |
| :--- | :--- | :--- |
| **DBeaver** (recomendado) | Interfaz visual, auto-complete, historial, ver tablas sin escribir SELECT | [dbeaver.io](https://dbeaver.io/download/) |
| **VSCode + SQLTools** | Ya en el editor, ligero | Extencion `SQLTools` + `SQLTools PostgreSQL Driver` |
| **TablePlus** | Interfaz pulida, rapido | [tableplus.com](https://tableplus.com/) |
| **pgAdmin** | Oficial de PostgreSQL | Incluido en instaladores de PostgreSQL |

DBeaver es ideal para ver resultados, navegar el esquema visualmente, y exportar datos.

---

## Inicio Rapido (Entorno Local)

### 1. Iniciar PostgreSQL con Docker
```bash
docker compose -f "Lab/Lab02/Taller/docker-compose/Postgres/docker-compose.yaml" up -d
```

### 2. Cargar el Dataset Northwind
```bash
psql -h localhost -U postgres -d northwind -f Lab/Lab01/aws/db_northwind.sql
```

### 3. Verificar la Instalacion
```bash
psql -h localhost -U postgres -d northwind -c "SELECT version();"
```

### 4. Conectar desde DBeaver
- Host: `localhost` | Puerto: `5432` | Usuario: `postgres` | Contrasena: `postgres` | Base: `northwind`

---

## Convenciones y Buenas Practicas SQL

- **Dialecto Postgres:** Usar `RETURNING`, `ON CONFLICT` (Upsert), tipos `JSONB`, `SERIAL`/`BIGSERIAL`.
- **Analisis de Rendimiento:** Explicar costo con `EXPLAIN (ANALYZE, BUFFERS)` en consultas complejas.
- **DML Seguros:** Envolver transacciones destructivas en bloques explicitos:
  ```sql
  BEGIN;
  EXPLAIN ANALYZE <SENTENCIA_DML>;
  ROLLBACK; -- O COMMIT si el plan y resultado son correctos
  ```
- **Diseno Relacional:** Diagramas Mermaid.js para esquemas y transiciones de datos.

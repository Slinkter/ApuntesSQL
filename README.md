# ApuntesSQL — Plan de Maestría en PostgreSQL

Este repositorio contiene notas de estudio de nivel profesional, laboratorios prácticos y recursos académicos estructurados para dominar **PostgreSQL** y la **Teoría Relacional de Bases de Datos**. El proyecto se divide en dos enfoques principales: una pista teórica/académica (método Cornell) y una pista práctica interactiva y basada en escenarios reales.


---

## 📂 Estructura de Contenidos

El repositorio está organizado en las siguientes pistas de aprendizaje:

| Componente | Ruta | Descripción |
| :--- | :--- | :--- |
| **Dashboard Académico** | [ULima/Apuntes/index.html](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes/index.html) | Índice interactivo con acceso a las 16 semanas de clase y exámenes. |
| **Semanas Académicas** | [ULima/Apuntes/semana_01.html](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes/semana_01.html) a [semana_15.html](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes/semana_15.html) | Apuntes detallados en HTML estilo Cornell con widgets interactivos de dibujo y notas. |
| **Examen Parcial & Final** | [semana_08.html](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes/semana_08.html) y [semana_16.html](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes/semana_16.html) | Simulacros completos con cuestionario teórico y desarrollo práctico (incluye solucionario). |
| **Prerrequisitos & Setup** | [SQL/Youtube00/Ejercicios/0.prerrequisitos.md](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube00/Ejercicios/0.prerrequisitos.md) | Guía de entorno de desarrollo: Docker, variables de entorno, carga del dataset e introducción a `EXPLAIN ANALYZE`. |
| **Banco de Ejercicios** | [SQL/Youtube00/Ejercicios/](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube00/Ejercicios/) | 150 problemas resueltos divididos en [1.basico.md](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube00/Ejercicios/1.basico.md), [2.intermedio.md](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube00/Ejercicios/2.intermedio.md) y [3.avanzado.md](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube00/Ejercicios/3.avanzado.md). |
| **Dataset de Práctica** | [db_northwind.sql](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube00/Ejercicios/db_northwind.sql) | Script SQL para inicializar y poblar el esquema Northwind en PostgreSQL. |
| **Talleres & Laboratorios** | [SQL/Youtube01/Taller/](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube01/Taller/) | Ejercicios de taller prácticos y configuraciones listas de Docker Compose. |
| **Guía de Despliegue Cloud** | [Guia_Despliegue_Docker_AWS.md](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/SQL/Youtube00/Guia_Despliegue_Docker_AWS.md) | Manual paso a paso para desplegar PostgreSQL mediante contenedores Docker en AWS EC2. |

---

## 🎨 Estética & Diseño (Semanas Académicas)

Los documentos HTML de estudio implementan el **Método Cornell** adaptado a un diseño web moderno y responsivo:
- **Maquetación Académica:** Barra lateral (*Cue Column*) para conceptos clave e ideas fuerza, y área principal para notas detalladas de clase.
- **Canvases Interactivos:** Cada semana cuenta con una pizarra de dibujo interactiva integrada mediante [canvas-ui.js](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes/canvas-ui.js) para graficar modelos entidad-relación, flujos lógicos o tomar notas a mano alzada.
- **Arquitectura CSS Limpia:** Estilizado mediante [master.css](file:///C:/Users/LJCR/Documents/GitHub/ApuntesSQL/ULima/Apuntes/master.css) bajo la metodología BEM, libre de estilos embebidos o emojis innecesarios, garantizando legibilidad y profesionalismo.

---

## 🚀 Inicio Rápido (Entorno Local)

Para ejecutar las prácticas locales y resolver los talleres en PostgreSQL, sigue estos pasos:

### 1. Iniciar PostgreSQL mediante Docker Compose
Levanta una base de datos PostgreSQL limpia y configurada:
```bash
docker compose -f "SQL/Youtube01/Taller/docker-compose/Postgres/docker-compose.yaml" up -d
```

### 2. Cargar el Dataset de Práctica (Northwind)
Importa el esquema y los datos iniciales en la base de datos de prácticas:
```bash
psql -h localhost -U postgres -d northwind -f SQL/Youtube00/Ejercicios/db_northwind.sql
```

### 3. Ejecutar Consultas de Prueba
Conéctate al motor o ejecuta sentencias directas para verificar la instalación:
```bash
psql -h localhost -U postgres -d northwind -c "SELECT version();"
```

---

## ⚙️ Convenciones y Buenas Prácticas SQL

Para mantener un alto estándar técnico en las soluciones, todos los scripts deben cumplir las siguientes directrices:
- **Dialecto Postgres:** Aprovechar funciones específicas como `RETURNING`, `ON CONFLICT` (Upsert), tipos `JSONB` con operadores de indexación y generación de llaves auto-incrementales mediante `SERIAL`/`BIGSERIAL`.
- **Análisis de Rendimiento:** Explicar el costo de ejecución en lecturas lógicas e I/O utilizando `EXPLAIN (ANALYZE, BUFFERS)` en consultas complejas.
- **DML Seguros:** Envolver transacciones destructivas (`UPDATE`, `DELETE`) en bloques explícitos para auditoría segura:
  ```sql
  BEGIN;
  EXPLAIN ANALYZE <SENTENCIA_DML>;
  ROLLBACK; -- O COMMIT si el plan y resultado son correctos
  ```
- **Diseño Relacional:** Utilizar diagramas **Mermaid.js** para diagramar esquemas relacionales y de transiciones de datos de forma embebida.

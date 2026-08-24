# Laboratorio 01: PostgreSQL & Northwind Mastery en AWS EC2 (AI Agent-Friendly Guide)

> **Dataset:** Esquema canónico Northwind (`pthom/northwind_psql`).  
> **Motor de Base de Datos:** PostgreSQL 16 (Ejecutándose en un contenedor Docker con nombre `pg_architect_lab`).  
> **Estándar Instruccional:** Andragogía activa y el marco analítico de 6 pasos de [1.Guia/STANDARD.md](file:///C:/Users/luisj/Github/ApuntesSQL/Lab/Lab01/1.Guia/STANDARD.md).

Este archivo sirve como punto de partida y contexto operativo para futuros **agentes de Inteligencia Artificial** o desarrolladores que necesiten auditar, expandir o interactuar con este repositorio.

---

## 🗺️ Estructura del Proyecto

```
Lab/Lab01/
├── 1.Guia/
│   ├── 0.Guia_Docker_AWS.md          # Manual de infraestructura y SSH en AWS EC2
│   ├── README.md                      # Indexación detallada de la guía
│   ├── STANDARD.md                    # Normas editoriales, andragogía y orden del motor
│   └── Material/
│       ├── .env.example               # Plantilla de variables de entorno
│       ├── .env                       # Credenciales por defecto del laboratorio
│       ├── docker-compose.yml         # Contenedor de PostgreSQL 16 Alpine con healthchecks y límites
│       └── db_northwind.sql           # DDL y DML canónicos de Northwind
└── 2.Ejercicios/
    ├── 0.prerrequisitos.md            # Fundamentos de la base de datos, EXPLAIN y ciclo del motor
    ├── 1.basico.md                    # 50 ejercicios básicos (SELECT, WHERE, CASE, etc.)
    ├── 2.intermedio.md                # 50 ejercicios intermedios (GROUP BY, HAVING, JOINs)
    ├── 3.avanzado.md                  # 50 ejercicios avanzados (CTEs, recursión, Window Functions)
    ├── 4.examen_entrevista.md         # 30 preguntas de entrevista técnica y casos reales
    └── aws_ejercicio.sql              # Script consolidado de soluciones
```

---

## 🤖 Contexto y Reglas para Agentes de IA

Si eres un agente de IA que ha sido desplegado en este espacio de trabajo, ten en cuenta las siguientes directrices y decisiones de arquitectura tomadas por las ejecuciones previas:

### 1. Datos Canónicos frente a Datos Simulados (Mock Data)
- **Regla Estricta:** No debe inyectarse información ficticia en las salidas ASCII de los ejercicios (se eliminó todo rastro de códigos temporales de prueba como `NWE01`, `NWE02` o `Alfreds Futterkiste - Actualizado`). 
- **Conteos de Referencia:** Cualquier prueba de base de datos contra el esquema Northwind debe coincidir con estos valores exactos:
  - 91 clientes en la tabla `customers`.
  - 830 registros en la tabla `orders`.
  - 2155 registros en la tabla `order_details`.
  - 832 filas al realizar un `FULL JOIN` entre tablas de clientes y órdenes sin filtrar.

### 2. Formato Pedagógico (Andragogía Activa)
Cada ejercicio nuevo o modificado dentro de la serie de archivos `.md` debe contener obligatoriamente las siguientes secciones descritas en [STANDARD.md](file:///C:/Users/luisj/Github/ApuntesSQL/Lab/Lab01/1.Guia/STANDARD.md):
- **🎯 Enunciado y Caso de Uso** (con una clara justificación de negocio).
- **🎓 Explicación del Profesor** (que incluya una analogía del mundo real de alta retención).
- **🧠 Cómo Pensar como un Analista de Datos** (desglosado en KPI, Entidad, Fuentes, Filtros, Proyección y Validación).
- **⚙️ Desglose del Motor de Ejecución** (indicando explícitamente el orden lógico de procesamiento: `FROM` -> `JOIN` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `ORDER BY` -> `LIMIT`).
- **Código de Solución SQL** (con palabras clave SQL en mayúsculas).
- **Resultado Real de Ejecución** (tabla ASCII exacta, truncada a un máximo de 10-15 filas si el output original excede las 20 líneas, finalizando con la cantidad de filas en formato `(N rows)`).

---

## 🛠️ Infraestructura de Pruebas y Verificación

El proyecto cuenta con scripts de prueba en JavaScript que validan sintáctica y semánticamente el código SQL contenido dentro de los archivos markdown extrayéndolo dinámicamente y ejecutándolo contra el contenedor Docker.

Para comprobar la integridad del repositorio, ejecuta los siguientes comandos desde la raíz del laboratorio:

```bash
# Validar la estructura y sintaxis del nivel Básico
node .agents/worker_basico_1/verify_basico.js

# Validar la estructura, sintaxis y truncado de tablas ASCII en el nivel Intermedio
node .agents/worker_intermedio_1/verify_sql_in_md.js
node .agents/worker_intermedio_1/full_verification.js

# Validar el set de preguntas de Entrevista/Examen
node .agents/worker_examen_1/verify_markdown_sql.js
```

---
*Este archivo ha sido auditado y aprobado como parte de la entrega del Laboratorio 01.*

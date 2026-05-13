# ApuntesSQL - PostgreSQL Architecture & Mastery

Este proyecto es una plataforma educativa integral para la maestría en **PostgreSQL**, diseñada bajo estándares de ingeniería de alto rendimiento para el año 2026. Combina material histórico refactorizado con teoría relacional avanzada y prácticas modernas de arquitectura de datos.

## 🚀 Propósito y Filosofía
Transformar el conocimiento fragmentado en una base sólida de **Data Architecture**. El enfoque no es solo aprender SQL, sino entender los *internals* del motor (páginas de 8KB, MVCC, WAL) y la teoría relacional pura (C.J. Date).

## 🛠️ Stack Tecnológico
- **Database Engine:** PostgreSQL 15+ (v15, v16+)
- **Standards:** SQL ANSI 2023, PL/pgSQL
- **Documentation:** Markdown, Mermaid.js (ER Diagrams)
- **Frontend (Apuntes):** HTML/CSS Cornell Style para legibilidad académica.

## 📂 Estructura del Proyecto
```bash
.
├── ULima/                   # Material académico y apuntes refactorizados
│   ├── Apuntes/             # Material educativo central (HTML/Markdown)
│   │   ├── 01_Fundamentos/  # Física del dato, Teoría Relacional, SDLC
│   │   ├── 02_Postgres_Internals/ # Internals, Tipos tácticos, Normalización
│   │   └── 03_Escalabilidad/ # Indexación, Query Planner, CDC, HTAP
│   ├── Clases/              # PDFs y TXTs de sesiones originales
│   └── otros/               # Documentación complementaria y ejercicios
├── PostgresSQL/             # Recursos de laboratorio y dataset
│   ├── 1.basico.md          # Guía práctica de SQL Básico
│   ├── 2.intermedio.md      # SQL Intermedio y Agrupaciones
│   ├── 3.avanzado.md        # Ventanas, CTEs, PL/pgSQL
│   ├── db_northwind.sql     # Dataset oficial para ejercicios
│   └── Youtube01/           # Recursos adicionales de video tutoriales
├── Credenciales/            # Configuración y Guías de Despliegue
│   └── Guia_Despliegue_Docker_AWS.md # Guía de infraestructura Cloud
└── README.md                # Punto de entrada original
```

## 📖 Plan Maestro (16 Semanas)
1.  **Fundamentos (S01-S07):** DBMS, ERD, DDL, DML, Joins y Subconsultas.
2.  **Examen Parcial (S08):** Validación de fundamentos.
3.  **Avanzado (S09-S15):** Group By, CTEs, PL/pgSQL, Transacciones, Índices y Seguridad.
4.  **Examen Final (S16):** Evaluación integral.

## 🧪 Laboratorio: Northwind en PostgreSQL
El proyecto utiliza una versión adaptada de la base de datos **Northwind** para PostgreSQL.
- **Ubicación:** `PostgresSQL/db_northwind.sql`
- **Modelado:** `PostgresSQL/1.basico.md` incluye el diagrama ER en formato Mermaid.

## ⚙️ Desarrollo y Auditoría
- **Auditoría:** Se sigue el estándar definido en `prompt_auditoria.md` para garantizar calidad técnica (vía ArquiDB).
- **Convenciones:** 
    - Priorizar `JSONB` sobre `JSON`.
    - Usar `SERIAL`/`BIGSERIAL` para IDs secuenciales (o `UUID v7`).
    - Explicar siempre el impacto en I/O de cada consulta (`EXPLAIN ANALYZE`).

---
*Mantenido por el Senior Data Solutions Architect.*

# Sesion de Trabajo — Resumen para Futuras Intervenciones

**Fecha:** 2026-07-11  
**Commits:** `9028493` (Lab01 intermedio), `12562fa` (Lab02 refactor), `33b8dea` (README)

---

## Estado Actual del Proyecto

### Lab01 — Ejercicios PostgreSQL (COMPLETO)
| Archivo | Lineas | Estado |
|---------|--------|--------|
| `Lab/Lab01/Ejercicios/0.prerrequisitos.md` | ~1243 | Completo |
| `Lab/Lab01/Ejercicios/1.basico.md` | ~1441 | Completo |
| `Lab/Lab01/Ejercicios/2.intermedio.md` | ~2277 | Completo (50 analogias + 50 tips) |
| `Lab/Lab01/Ejercicios/3.avanzado.md` | ~2614 | Completo |
| `Lab/Lab01/Ejercicios/4.examen_entrevista.md` | ~1154 | Completo (28 preguntas) |
| `Lab/Lab01/aws/db_northwind.sql` | - | Dataset Northwind PostgreSQL |

**Esquema:** Northwind PostgreSQL (ver `db_northwind.sql`)  
**Dialecto:** PostgreSQL exclusivamente

### Lab02 — Taller MySQL/PostgreSQL (COMPLETO)
| Archivo | Cambios |
|---------|---------|
| `Lab/Lab02/shared.css` | NUEVO — CSS compartido (368 lineas) |
| `Lab/Lab02/shared.js` | NUEVO — Reveal buttons (17 lineas) |
| `Lab/Lab02/index.html` | Links corregidos, CSS inline eliminado |
| `Lab/Lab02/CheatSheet_SQL.html` | CSS importado, nav agregado |
| `Lab/Lab02/Guia_Estudio_Maestria_SQL_Parte1-4.html` | CSS importado, reveal buttons |
| `Lab/Lab02/Taller/` (11 guias) | Reescritas con analogias, tips, MySQL vs PostgreSQL |
| `Lab/Lab02/Taller/sql/sql1.sql` | Typos, advertencias, secciones |
| `Lab/Lab02/Taller/ejemplo1-cine.sql` | DECIMAL(2,1) corregido a (3,1) |
| `Lab/Lab02/Taller/ejemplo2-videojuegos.sql` | Fechas futuras corregidas |
| `Lab/Lab02/Taller/docker-compose/` | Healthchecks agregados en 4 archivos |

**Esquemas:** escuela (cine, videojuegos, restaurants)  
**Dialecto:** MySQL principal, notas PostgreSQL donde aplica

### Estructura de Directorios
```
ApuntesSQL/
├── Lab/
│   ├── Lab01/                    # PostgreSQL — Northwind
│   │   ├── Ejercicios/           # 5 guias markdown (150 ejercicios)
│   │   └── aws/db_northwind.sql  # Dataset
│   └── Lab02/                    # MySQL/PostgreSQL — Taller
│       ├── index.html            # Menu principal
│       ├── CheatSheet_SQL.html   # Referencia rapida
│       ├── Guia_Estudio_*.html   # Guias teoricas (4 partes)
│       ├── shared.css            # Estilos compartidos
│       ├── shared.js             # JavaScript compartido
│       ├── sql/sql1.sql          # Ejemplos practicos
│       └── Taller/               # Guias DDL/DML
│           ├── instalaciones-necesarias.md
│           ├── create-drop-db-table.md
│           ├── alter-table.md
│           ├── insert-into-select.md
│           ├── update-delete-truncate.md
│           ├── select-where-order.md
│           ├── funciones-agregacion.md
│           ├── inner-join.md
│           ├── left-right-join.md
│           ├── subconsultas-group-having-coalesce.md
│           ├── buenas-practicas.md
│           ├── ejemplo1-cine.sql
│           ├── ejemplo2-videojuegos.sql
│           ├── ejemplo3-restaurants.sql
│           └── docker-compose/   # MySQL + PostgreSQL
├── ULima/Apuntes/                # Semanas academicas (Cornell)
└── README.md                     # Actualizado
```

---

## Estilo Pedagogico Unificado

Cada ejercicio/guia sigue la estructura:
1. **Analogia** — Comparacion con la vida real (en blockquote)
2. **Definicion** — Que hace el comando y por que importa
3. **Codigo** — SQL comentado con explicacion paso a paso
4. **MySQL vs PostgreSQL** — Donde difieren los dialectos (en Lab02)
5. **Tip del Profesor** — Rendimiento, errores comunes, buenas practicas

**Reglas:**
- Sin emojis en titulos (tono profesional)
- Blockquotes para analogias y tips
- Analisis de rendimiento con `EXPLAIN ANALYZE`
- Transacciones seguras (BEGIN/ROLLBACK) en UPDATE/DELETE

---

## Observaciones Pendientes del Usuario

- El usuario menciono "varias observaciones" en Lab01 pero no las detallo
- Pregunto por cliente SQL recomendado (respuesta: DBeaver)
- Actualice README con recomendacion de DBeaver

---

## Proximos Pasos Sugeridos

1. **Lab01**: Verificar si el usuario tiene observaciones pendientes
2. **Lab01**: Considerar agregar guia de instalacion de DBeaver en `0.prerrequisitos.md`
3. **Lab02**: Las guias de `Taller/` estan reescritas pero pueden necesitar revision del usuario
4. **General**: El usuario tiene un examen pendiente — podria necesitar simulacros adicionales
5. **General**: Verificar si `ULima/Apuntes/` necesita actualizaciones

---

## Configuracion del Entorno

- **PostgreSQL**: Docker compose en `Lab/Lab02/Taller/docker-compose/Postgres/`
- **Puerto**: 5432
- **Usuario**: postgres / postgres
- **Base de datos**: northwind (Lab01), escuela (Lab02)
- **Cliente recomendado**: DBeaver (gratis)
- **VSCode**: Extencion SQLTools + SQLTools PostgreSQL Driver

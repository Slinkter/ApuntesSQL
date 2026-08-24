-- ============================================================================
-- PostgreSQL Lab01 - Script de Verificación de Conectividad (AWS EC2 / Docker)
-- ============================================================================
-- Corresponde al Ejercicio 1 (Nivel Básico): Proyección de la Fuerza de Ventas
-- Base de datos: Northwind (pthom/northwind_psql)
-- Motor: PostgreSQL 15+ / 16 Alpine
-- ============================================================================

SELECT
    employee_id,
    last_name,
    first_name,
    title
FROM employees
ORDER BY employee_id;
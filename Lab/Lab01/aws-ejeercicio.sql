SELECT
    first_name || ' ' || last_name AS empleado,
    hire_date,
    AGE(CURRENT_DATE, hire_date) AS antiguedad_intervalo,
    EXTRACT(YEAR FROM AGE(hire_date)) AS anos_en_empresa,
    CASE
        WHEN EXTRACT(YEAR FROM AGE(hire_date)) >= 10 THEN 'Veterano'
        WHEN EXTRACT(YEAR FROM AGE(hire_date)) >= 5 THEN 'Experimentado'
        ELSE 'Nuevo'
    END AS categoria
FROM employees
ORDER BY hire_date;
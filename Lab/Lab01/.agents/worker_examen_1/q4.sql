SELECT
    first_name || ' ' || last_name AS nombre_completo,
    title,
    city,
    reports_to
FROM employees
WHERE reports_to IS NOT NULL
ORDER BY reports_to, last_name;
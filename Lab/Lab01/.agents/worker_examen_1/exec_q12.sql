SELECT
    e.first_name || ' ' || e.last_name AS empleado,
    e.title AS cargo_empleado,
    COALESCE(m.first_name || ' ' || m.last_name, 'Sin jefe') AS jefe,
    COALESCE(m.title, 'N/A') AS cargo_jefe
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
ORDER BY e.employee_id;
BEGIN;
SELECT employee_id,
       last_name,
       first_name,
       title
FROM employees
ORDER BY employee_id;
;
ROLLBACK;
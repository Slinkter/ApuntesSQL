# Ejemplos - Clase 10: Consultas Avanzadas SQL I

## Ejemplos de Consultas con Subconsultas y Funciones (9 de Octubre de 2013)

Este script presenta una serie de consultas `SELECT` que demuestran el uso de subconsultas, funciones de agregación (`MAX`), funciones de cadena (`SUBSTR`, `||`) y funciones de conversión de fecha (`TO_CHAR`). Estos ejemplos son un excelente punto de partida para entender cómo construir consultas más complejas y analíticas.

```sql
-- Encontrar el salario máximo de todos los empleados
SQL> select max(salary) from hr.employees;
/*
MAX(SALARY)
-----------
      24000
*/

-- Encontrar el nombre y fecha de contratación del empleado con el salario máximo
SQL> select first_name, hire_date from hr.employees where salary=24000;
/*
FIRST_NAME           HIRE_DATE
-------------------- ---------
Steven               17-JUN-87
*/

-- Igual que el anterior, pero formateando el año de contratación
SQL> select first_name, to_char(hire_date,'YYYY') from hr.employees where salary=24000;
/*
FIRST_NAME           TO_C
-------------------- ----
Steven               1987
*/

-- Ejemplo de consulta que no devuelve filas
SQL> select first_name,salary*0.75 from hr.employees where department_id=56;
-- no rows selected

-- Uso de una subconsulta en la cláusula WHERE
-- Encontrar empleados que ganan más de la mitad del salario de 'Steven'
SQL> select first_name, salary from hr.employees where salary > (select max(salary*0.5) from hr.employees where first_name='Steven');
/*
FIRST_NAME               SALARY
-------------------- ----------
Michael                   13000
Steven                    24000
Neena                     17000
Lex                       17000
John                      14000
Karen                     13500
*/

-- Encontrar empleados sin manager (manager_id es nulo)
SQL> select first_name, last_name from hr.employees where manager_id is NULL;
/*
FIRST_NAME           LAST_NAME
-------------------- -------------------------
Steven               King
*/

-- Concatenar nombre y apellido de empleados contratados después de 2012
SQL> select first_name||' '||last_name from hr.employees where to_char(hire_date,'YYYY')>2012;
-- no rows selected

-- Uso del operador LIKE para búsqueda de patrones
-- Encontrar empleados cuyo apellido empieza con 'K' y ganan más de 1000
SQL> select first_name, last_name, salary from hr.employees where last_name like 'K%' and salary>1000;
/*
FIRST_NAME           LAST_NAME                     SALARY
-------------------- ------------------------- ----------
Payam                Kaufling                        7900
Alexander            Khoo                            3100
Janette              King                           10000
Steven               King                           24000
Neena                Kochhar                        17000
Sundita              Kumar                           6100
*/

-- Uso de la función SUBSTR para búsqueda de patrones
-- Alternativa al LIKE para encontrar empleados cuyo apellido empieza con 'K'
SQL> select first_name, last_name, salary from hr.employees where substr(last_name,1,1)='K' and salary>1000;
/*
FIRST_NAME           LAST_NAME                     SALARY
-------------------- ------------------------- ----------
Steven               King                           24000
Neena                Kochhar                        17000
Alexander            Khoo                            3100
Payam                Kaufling                        7900
Janette              King                           10000
Sundita              Kumar                           6100
*/
```
---

## Ejemplos de GROUP BY, HAVING, JOIN y Funciones Varias (14 de Octubre de 2013)

Este script profundiza en las consultas SQL avanzadas, mostrando el uso de `GROUP BY`, `HAVING`, `JOIN` (en sintaxis ANSI y antigua), y una variedad de funciones escalares como `NVL`, `ROUND`, `TRUNC`, `INSTR`, `LENGTH`, `DECODE` y `CASE`. También introduce la herramienta `EXPLAIN PLAN` para el análisis de rendimiento de consultas.

```sql
-- 1) Contar empleados por año de contratación
SQL> select to_char(hire_date,'YYYY'), count(*)
from hr.employees
group by to_char(hire_date,'YYYY')
order by 1;
/*
TO_C   COUNT(*)
---- ----------
2001          1
...
*/

-- 2) Contar empleados por la primera letra de su apellido
SQL> select substr(last_name,1,1), count(*)
from hr.employees
group by substr(last_name,1,1)
order by 1;
/*
S   COUNT(*)
- ----------
A          4
...
*/

-- 3) Salario máximo por departamento
select department_id, max(salary)
from hr.employees
group by department_id;
/*
DEPARTMENT_ID MAX(SALARY)
------------- -----------
          100       12008
...
*/

-- 4) Uso de NVL para manejar valores nulos en GROUP BY
-- NVL(valor, valor_si_es_nulo)
-- En SQL Server, su equivalente es ISNULL()
select nvl(department_id,-1), max(salary)
from hr.employees
group by department_id; -- Agrupa por el valor original
-- o, mejor:
select nvl(department_id,-1), max(salary)
from hr.employees
group by nvl(department_id,-1); -- Agrupa por el valor transformado

-- 5) Uso de HAVING para filtrar grupos
-- Departamentos cuya suma de salarios es mayor a 10000
select department_id, sum(salary)
from hr.employees
group by department_id
having sum(salary)>10000
order by 2;
/*
DEPARTMENT_ID SUM(SALARY)
------------- -----------
           20       19000
...
*/

-- 6) Cálculo de semanas de antigüedad
select first_name||' '||last_name, round((sysdate-hire_date)/7,0)
from hr.employees;

-- 7) Ejemplos de funciones ROUND y TRUNC
-- ROUND redondea al número más cercano, TRUNC trunca decimales.
round(458.12,1) -- 458.1
round(123.5678,3) -- 123.568
round(978.9,-1) -- 980

trunc(458.12,1) -- 458.1
trunc(123.5678,3) -- 123.567
trunc(978.9,-1) -- 970

-- 8) Uso de DECODE (específico de Oracle) y CASE (estándar ANSI)
-- DECODE
select
decode(length(first_name),4,-10,20,-20,30,-30,0), first_name
from hr.employees;

-- CASE
select first_name, 
 case
  when (salary<5000) then 'C'
  when (salary<10000) and (salary>=5000) then 'B'
  when (salary>=10000) then 'A'
  else 'N/A'
 end clasificacion, department_id
from hr.employees;


-- 9) JOIN en sintaxis ANSI vs. Oracle antigua
-- Sintaxis ANSI (recomendada)
select last_name, d.DEPARTMENT_NAME
from hr.employees e inner join hr.departments d 
on e.department_id = d.department_id;

-- Sintaxis Oracle antigua
select last_name, d.DEPARTMENT_NAME
from hr.employees e, hr.departments d 
where e.department_id = d.department_id;

-- 10) Join de tres tablas
select last_name, d.DEPARTMENT_NAME, l.POSTAL_CODE||', '||l.STREET_ADDRESS
from (hr.employees e inner join hr.departments d 
on e.department_id = d.department_id)
inner join hr.locations l
on d.location_id = l.location_id;


-- 11) Subconsulta en una expresión CASE
select last_name, JOB_TITLE,
 case 
  when salary>(select avg(salary) from hr.employees) then 'Y'
  else 'N'
 end rpta
from hr.employees e join hr.jobs j
on j.job_id = e.job_id;

-- 12) Agrupación con JOIN
select last_name, count(*)
from hr.employees e join hr.job_history jh
on e.employee_id = jh.employee_id
group by e.last_name;

-- 13) Costeo de consulta (EXPLAIN PLAN)
explain plan for 
 select last_name, count(*)
 from hr.employees e join hr.job_history jh
 on e.employee_id = jh.employee_id
 group by e.last_name;

-- Mostrar el plan de ejecución
set linesize 800
select * from table(dbms_xplan.display);
```
---
# Ejemplos - Clase 11: Consultas Avanzadas SQL II

## Ejemplos de Subconsultas Correlacionadas, ROWNUM y Múltiples JOINs (16 de Octubre de 2013)

Este script presenta ejemplos de consultas SQL avanzadas, incluyendo subconsultas correlacionadas para cálculos complejos, el uso de la pseudocolumna `ROWNUM` para paginación y consultas "Top-N", y el encadenamiento de múltiples `JOIN`s para combinar datos de varias tablas.

```sql
-- 1) Subconsulta correlacionada para encontrar empleados en el tercio superior de salarios
-- Para cada empleado (e1), se cuenta cuántos empleados (e2) tienen un salario menor,
-- se calcula el ratio, y se seleccionan aquellos cuyo ratio es mayor a 0.33.
select first_name,last_name
from
(
 select first_name,last_name,
 (select count(*) from 
 hr.employees e2 where 
 e1.salary > e2.salary)/
 (select count(*) from hr.employees) as ratio
 from hr.employees e1
)
where ratio>0.33;

-- 2) Uso de ROWNUM para limitar el número de filas
select rownum,last_name
from hr.employees;

select last_name
from hr.employees
where rownum<51; -- Devuelve las primeras 50 filas

-- 3) Consulta Top-N para encontrar los 5 empleados con mayor salario
-- Se debe usar una subconsulta para ordenar primero y luego filtrar por ROWNUM.
select *
from(
 select first_name, salary
 from hr.employees
 order by salary desc
)
where rownum<=5;

-- Comparación con la sintaxis de otros SGBD:
-- SQL Server:
-- select top 5 *
-- from hr.employees
-- order by salary desc;
-- MySQL:
-- select *
-- from hr.employees
-- order by salary desc
-- limit 5;


-- 4) JOIN de cuatro tablas para contar empleados por país
select country_name, count(*)
from (((hr.employees e join hr.departments d on e.department_id = d.department_id)
join hr.locations l on d.location_id = l.location_id) join hr.countries c
on c.country_id = l.country_id)
group by country_name;


-- 5) Uso de BETWEEN para filtrar por un rango de salarios
select last_name,salary
from hr.employees
where salary>=4000 and salary<=5000;

-- Equivalente a:
select last_name,salary
from hr.employees
where salary between 4000 and 5000;
```

---

## Ejemplos de JOINs, Funciones de Agrupación y SELF JOIN (21 de Octubre de 2013)

Este script proporciona una variedad de ejemplos que exploran diferentes tipos de `JOIN`s (`LEFT`, `RIGHT`, `SELF JOIN`), el comportamiento de las funciones de agrupación con valores `NULL`, y el uso de la cláusula `HAVING` para filtrar resultados agrupados.

```sql
-- 6) Diferencia entre INNER JOIN, LEFT JOIN y RIGHT JOIN
SQL> select * from t1;
/*
    CAMPO1
----------
         1
         2
         3
         1
         8
*/
SQL> select * from t2;
/*
    CAMPO2
----------
         3
       100
*/

-- INNER JOIN: Solo filas con coincidencias en ambas tablas
SQL> select campo1,campo2 from t1 join t2 on t1.campo1=t2.campo2;
/*
    CAMPO1     CAMPO2
---------- ----------
         3          3
*/

-- LEFT JOIN: Todas las filas de la tabla izquierda (t1), con NULL donde no hay coincidencia
SQL> select campo1,campo2 from t1 left join t2 on t1.campo1=t2.campo2;
/*
    CAMPO1     CAMPO2
---------- ----------
         3          3
         8
         1
         1
         2
*/

-- RIGHT JOIN: Todas las filas de la tabla derecha (t2), con NULL donde no hay coincidencia
SQL> select campo1,campo2 from t1 right join t2 on t1.campo1=t2.campo2;
/*
    CAMPO1     CAMPO2
---------- ----------
         3          3
                  100
*/

-- Comportamiento de las funciones de agrupación con NULLs
SQL> select count(campo) from demo1; -- Cuenta solo los valores no nulos
-- COUNT(CAMPO)
-- ------------
--           3

SQL> select count(*) from demo1; -- Cuenta todas las filas
--   COUNT(*)
-- ----------
--          4

SQL> select avg(campo) from demo1; -- Ignora los valores nulos para el cálculo del promedio
-- AVG(CAMPO)
-- ----------
-- 133.333333

SQL> select avg(nvl(campo,0)) from demo1; -- Incluye los NULLs como 0 en el cálculo, cambiando el resultado
-- AVG(NVL(CAMPO,0))
-- -----------------
--               100

-- 7) Uso de RIGHT JOIN para incluir todos los países, tengan o no empleados
select country_name, count(e.last_name)
from (((hr.employees e join hr.departments d on e.department_id = d.department_id)
join hr.locations l on d.location_id = l.location_id) right join hr.countries c
on c.country_id = l.country_id)
group by country_name;


-- 8) Uso de SELF JOIN (a través de LEFT JOIN) para mostrar la relación Empleado -> Gerente
column Empleado format a15
column Gerente format a15
column dept1 format a15
column dept2 format a15

select e1.first_name||' '||e1.last_name as Empleado,nvl(d1.department_name,'N/A') as dept1,
nvl(e2.first_name||' '||e2.last_name,'N/A') as Gerente, nvl(d2.department_name,'N/A')  as dept2
from (hr.employees e1 left join hr.departments d1 on e1.department_id = d1.department_id)
left join hr.employees e2 on e1.manager_id = e2.employee_id left join
hr.departments d2 on e2.department_id = d2.department_id;


-- 9) Contar el número de subordinados por gerente
select e2.first_name||' '||e2.last_name, count(e1.last_name)
from hr.employees e1 right join hr.employees e2 on e1.manager_id = e2.employee_id
group by e2.first_name||' '||e2.last_name;


-- 10) Filtrar gerentes con 5 o más subordinados
-- Usando una subconsulta (menos eficiente)
select *
from
(
 select e2.first_name||' '||e2.last_name, count(e1.last_name) as total
 from hr.employees e1 right join hr.employees e2 on e1.manager_id = e2.employee_id
 group by e2.first_name||' '||e2.last_name
)
where total>=5;

-- Usando HAVING (más eficiente)
select e2.first_name||' '||e2.last_name, count(e1.last_name) as total
from hr.employees e1 right join hr.employees e2 on e1.manager_id = e2.employee_id
group by e2.first_name||' '||e2.last_name
having count(e1.last_name)>=5;

-- Análisis del plan de ejecución para comparar ambas consultas
explain plan for
select *
from
(
 select e2.first_name||' '||e2.last_name, count(e1.last_name) as total
 from hr.employees e1 right join hr.employees e2 on e1.manager_id = e2.employee_id
 group by e2.first_name||' '||e2.last_name
)
where total>=5;
select * from table(dbms_xplan.display());

explain plan for
select e2.first_name||' '||e2.last_name, count(e1.last_name) as total
from hr.employees e1 right join hr.employees e2 on e1.manager_id = e2.employee_id
group by e2.first_name||' '||e2.last_name
having count(e1.last_name)>=5;
select * from table(dbms_xplan.display());
```
---

## Análisis del Plan de Ejecución e Índices (23 de Octubre de 2013)

Este script se enfoca en la optimización de consultas a través del análisis de planes de ejecución y la creación de índices. Demuestra cómo usar `EXPLAIN PLAN` y `DBMS_XPLAN.DISPLAY` para entender cómo Oracle ejecuta una consulta y cómo la creación de un índice puede (o no) afectar este plan.

```sql
-- Analizar el plan de ejecución de una consulta compleja
explain plan for
select first_name,last_name
from
(
 select first_name,last_name,
 (select count(*) from 
 hr.employees e2 where 
 e1.salary > e2.salary)/
 (select count(*) from hr.employees) as ratio
 from hr.employees e1
)
where ratio>0.33;

set linesize 500
select * from table(dbms_xplan.display());

-- Ejemplo 1: Consulta simple y creación de índice
explain plan for
select salary, last_name 
from hr.emp
where salary<5000;

set linesize 500
select * from table(dbms_xplan.display());

-- Creación de índices para optimizar la consulta anterior
create index hr.idx_emp_sal on hr.emp (salary);
create index hr.idx_emp_sal on hr.employees (salary desc);
create index hr.idx2 on hr.emp (salary,last_name);

-- Ejemplo 2: Cómo afectan los operadores y NULLs a los índices
-- Un índice puede no ser utilizado con el operador <>
explain plan for
select salary, last_name 
from hr.emp
where salary<>5000;

-- Un índice puede no ser utilizado para buscar valores nulos directamente
-- Nota: Los índices no almacenan valores NULL por defecto.
explain plan for
select salary, last_name 
from hr.emp
where salary is not null;

explain plan for
select salary, last_name 
from hr.emp
where salary is null;


-- Ejemplo 3: Demostración práctica del uso de índices
SQL> create table demo10 (campo1 number);
SQL> insert into demo10 values (200);
SQL> insert into demo10 values (300);
SQL> insert into demo10 values (5);
SQL> insert into demo10 values (NULL);
SQL> commit;
SQL> create index idxdemo on demo10(campo1);

-- El optimizador probablemente usará el índice aquí.
explain plan for
select * from demo10 where campo1<200;
select * from table(dbms_xplan.display());

-- El optimizador probablemente NO usará el índice aquí (Full Table Scan).
explain plan for
select * from demo10 where campo1 is NULL;
select * from table(dbms_xplan.display());

```
---
---

## Ejemplos Adicionales de `SQLQuery1.sql`

### Subconsultas con `IN`, `ANY` y `ALL`

Estos scripts demuestran cómo usar subconsultas en la cláusula `WHERE` para filtrar datos basados en un conjunto de valores devueltos por otra consulta. Se exploran los operadores `IN`, `NOT IN`, `= ANY` y `<> ALL`.

```sql
/*Script sobre Libreria4 */
create database Libreria4;
use Libreria4;
create table libros
(
id_libro int primary key,
titulo varchar(50),
num_pag int
);
-- ... (inserciones y actualizaciones) ...
select * from libros;

-- Subconsulta que devuelve un solo valor
select * from libros where id_libro = (select id_libro from libros where titulo = 'jugadores');

-- Uso de IN con un conjunto de valores explícito
select * from libros where id_libro in (2,4,6); /*Escoger por id */

-- Uso de NOT IN para exclusión
select * from libros where id_libro not in (2,4,6);/*Excepcion a 2 4 6*/

-- Uso de NOT IN con una subconsulta
select * from libros where id_libro not in (select id_libro from libros where num_pag>1000);

/*
in : = any
not in : <> all
*/

-- Uso de ANY
-- Encuentra mujeres cuya edad coincide con la edad de al menos un hombre.
use empleados;
select * from usuarios where sexo ='F' and edad = any(select edad from usuarios where sexo='M');

-- Uso de ALL
-- Encuentra mujeres cuya edad no coincide con la edad de ningún hombre.
select * from usuarios where sexo = 'F' and edad <> all (select edad from usuarios where sexo='M');

-- Actualización con subconsulta usando ANY
update usuarios set tipo_usuario = 'root'
where id_usuario = any (select id_usuario from usuarios where edad > 24);
```

### `INSERT` desde un `SELECT`

Ejemplo de cómo insertar los resultados de una consulta `SELECT` directamente en otra tabla.

```sql
create table nombres
(
nombre varchar(50)
);

insert into nombres (nombre)
select (nombre) from usuarios;

select * from nombres;
```
---

### Creación y Uso de Vistas (Scripts 45-49)

Estos scripts cubren la creación, uso y gestión de vistas en SQL. Las vistas se utilizan para simplificar consultas complejas, encapsular lógica y proporcionar una capa de seguridad.

```sql
/*Script : Video 45 :Vista*/
use empleados;
create view usuarios_view as select nombre, edad from usuarios;

select count(nombre) as 'Cantidad de usuarios' from usuarios_view;

/*Video 46 : Cifrado de vista-Seguridad*/
-- Ver el código de una vista
sp_helptext usuarios_view;

-- Crear una vista encriptada
create view usuarios_view2 with encryption as select nombre,edad from usuarios;
sp_helptext usuarios_view2; -- Error: el objeto está encriptado

/*Video 47-48 : Vistas actualizables*/
drop view usuarios_view,usuarios_view2;

create view Mujeres as select * from usuarios where sexo='F';
select * from Mujeres order by edad asc;

-- Se puede actualizar o eliminar de una vista si se basa en una sola tabla
-- y no contiene agregaciones, DISTINCT, GROUP BY, etc.
update Mujeres set tipo_usuario ='SuperUsuario' where edad>25;
delete from Mujeres where edad < 20;

/*Video 49 : Vistas con CHECK OPTION*/
-- WITH CHECK OPTION fuerza a que todas las inserciones y actualizaciones
-- a través de la vista cumplan con la condición de la cláusula WHERE de la vista.
create view copy_m as select * from usuarios where sexo ='M' with check option;

-- Esto fallaría si intentamos insertar un registro con sexo = 'F' a través de la vista copy_m
-- insert into copy_m (nombre, ..., sexo) values ('ana', ..., 'F');
```
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
---

## Ejemplos Adicionales de `SQLQuery1.sql`

### Script 10: Funciones de Agregación

Ejemplos del uso de las funciones de agregación `COUNT`, `SUM`, `MAX` y `MIN` para obtener estadísticas resumidas de un conjunto de datos.

```sql
/*Scrip 10:Libreria2*/
create database Libreria2;
use libreria2
create table libros
(
titulo varchar(50)not null,
descripción varchar(100)not null,
autor varchar(50)not null,
precio_venta int not null,
precio_compra int not null,
)
insert into libros values ('El Arbol Místico','libro de misterio','Daniel Cortez',128,111);
insert into libros values ('El Canguro Saltarín','libro infantil','Mariana Perez',189,145);
-- ... (más inserciones) ...
select * from libros;
select COUNT(*) from libros where precio_compra > 290;
select SUM(precio_venta) from libros;
select max(precio_venta) from libros;
select min(precio_venta) from libros;
```
---

### Script 15-16: Búsqueda con `LIKE` y `COUNT`

Estos scripts demuestran el uso de `NULL`, `NOT NULL`, `BETWEEN`, y el operador `LIKE` con comodines (`%`, `_`) para realizar búsquedas de patrones flexibles. También se muestra cómo contar filas con `COUNT`.

```sql
/*Scrip 15: */
-- ... (creación y alteración de tabla) ...
select * from libros where nombre is not null;
select * from libros where precio_venta between 200 and 300;

/*Scrip 15*: Usando Like */
use libreria3;
select * from libros where nombre like '%100%';
select * from libros where nombre not like '%el%';
select * from libros where nombre like 'nar%';/* buscar palabras que comienza nar....*/
select * from libros where nombre like '%nia';/* buscar palabras que terminan ....nia*/
select * from libros where nombre like '%la ma_ia de las m_tem_ticas%';

/*Scrip 16: */
select COUNT(nombre) as 'Cantidad de libros' from libros where id_libro>10;
```

### Script 17-18: Agregación con `GROUP BY` y `HAVING`

Ejemplos de cómo agrupar datos y aplicar condiciones a los grupos. Se utilizan `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` y se introduce la cláusula `HAVING` para filtrar los resultados de la agrupación.

```sql
/*Scrip 17: */
create database empleados;
use empleados;
create table usuarios(
id_usuario int identity primary key,
nombre varchar(30) not null,
usuario varchar(30) not null,
contraseña varchar(30) not null,
tipo_usuario varchar(10) not null,
edad int not null,
sexo varchar(20) not null
);
-- ... (inserciones) ...

/*count sum avg: operadorea de agrupamiento*/
select count(*) as 'Numero de usuarios' from usuarios;
select sum(edad) as 'La suma de edad  de usuarios' from usuarios;
select AVG(edad) as 'El promedio de edad de usuarios' from usuarios;
select avg(edad) from usuarios where sexo = 'M' and edad<18;

/*max min */
select min(edad) as 'Edad minima' from usuarios;
select max(edad) as 'Edad maxima' from usuarios;

/*Scrip 18:Having necesita operadores de agrupamiento*/
select nombre,AVG(edad) from usuarios where sexo ='f'
group by nombre
having avg(edad)>20;
```

### Script 20-21: `DISTINCT` y `TOP`

Uso de `DISTINCT` para eliminar filas duplicadas de un resultado y de `TOP` para limitar el número de filas devueltas.

```sql
/*Scrip 20 : Distintic*/
select distinct nombre from usuarios order by nombre;
select distinct edad from usuarios order by edad;
select sum(distinct edad) from usuarios;

/*Scrip 21 : top*/
select top 10 * from usuarios;
select top 10 * from usuarios  order by id_usuario desc;
```

### Script 22: `INNER JOIN` y `LEFT/RIGHT JOIN`

Ejemplos de cómo combinar datos de múltiples tablas utilizando diferentes tipos de `JOIN`.

```sql
/*Script 22 : inner Join*/
create database escuela;
use escuela;
CREATE TABLE CARRERA (ID_CARRERA INT PRIMARY KEY, CARRERA VARCHAR(20));
CREATE TABLE ALUMNO(ID_ALUMNO INT PRIMARY KEY, NOMBRE VARCHAR(20), APELLIDOS VARCHAR(20), ID_CARRERA INT);
CREATE table datos (ID_DATOS INT PRIMARY KEY, ID_ALUMNO INT, EMAIL VARCHAR(20), EDAD int);
-- ... (inserciones y FKs) ...

/*Inner Join */
select ALUMNO.NOMBRE, ALUMNO.APELLIDOS , datos.EDAD,datos.EMAIL 
from datos 
inner join alumno on  datos.ID_ALUMNO = alumno.ID_ALUMNO 
inner join carrera on alumno.ID_CARRERA = carrera.ID_CARRERA 
where carrera.ID_CARRERA = 1;

/*Inner join left*/
select * from datos inner join ALUMNO on datos.ID_ALUMNO = alumno.ID_ALUMNO;
select * from alumno left join datos on alumno.ID_ALUMNO = datos.ID_ALUMNO;
select * from datos right join alumno on alumno.ID_ALUMNO = datos.ID_ALUMNO;
```
---

## Ejemplos Adicionales de `SQLQuery2.sql` (Northwind)

Estos ejemplos, basados en la base de datos Northwind, demuestran una variedad de técnicas de filtrado y agrupación en T-SQL.

### `GROUP BY` con `HAVING`
```sql
use Northwind;

-- Contar compañías por país, agrupando solo los que tienen más de 2.
select country ,count(companyname) as 'Acumulado' from Customers
where country like 'A%'
group by country
having count(companyname)>2;
```

### Cláusulas de Filtrado: `BETWEEN`, `IN`, `LIKE`
```sql
-- Filtrar con BETWEEN
select productname,unitprice from Products
where UnitPrice between 25 and 30;

-- Filtrar con IN
select companyname,contactname,country from customers
where country in('USA','Canada','Mexico');

-- Filtrar con LIKE y rangos
select companyname,contactname,country from customers
where CompanyName like '[A-C]%'; -- Empieza con A, B, o C
```

### `DISTINCT` para Valores Únicos
```sql
select Distinct country from customers order by Country;
```

### Exportar a XML con `FOR XML`
```sql
-- Diferentes formatos de salida XML
select companyname,contactname,country from Customers for xml auto;
select companyname,contactname,country from Customers for xml path;
select companyname,contactname,country from Customers for xml raw;
```

### Expresión `CASE` en `SELECT`
```sql
-- Clasificar productos por su ID de categoría
select productname,unitprice,
	case categoryid
		when 1 then 'producto 1'
		when 2 then 'producto 2'
		when 3 then 'producto 3'
		else 'Otros'
	end as 'Producto'
from Products;
```

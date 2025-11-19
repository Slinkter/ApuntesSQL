# Ejemplos - Clase 05: DML y Consultas Simples

## Script de Demostración de DML, TCL y DCL (4 de Septiembre de 2013)

Este script es una demostración práctica de las operaciones DML (`INSERT`, `UPDATE`, `DELETE`, `SELECT`), junto con comandos de Control de Transacciones (`COMMIT`, `ROLLBACK`, `TRUNCATE`) y ejemplos de Control de Datos (`GRANT`). También incluye ejemplos de DDL (`CREATE TABLE`, `ALTER TABLE`) y características avanzadas de Oracle como Flashback Query y Flashback Table, lo que lo convierte en un recurso completo para entender la manipulación básica y el control de datos en SQL.

```sql
-- Creación de tabla para el ejemplo
create table TipoInfraccion(codigo number, descripcion varchar(100), importe number(6,2));
alter table TipoInfraccion add constraint PK_CODIGO primary key(codigo);

-- Las operaciones DDL (create/drop/alter) incluyen un commit implícito.
commit; -- Confirma la transacción.

-- ==================== INSERT ====================
insert into tipoinfraccion values (5,'Conductor violento',9000);
rollback; -- Esta inserción se deshará porque el commit aún no se ha ejecutado.

insert into tipoinfraccion values (6,'Peaton gracioso',40);
-- Nota: Si no hay un commit explícito después de un DDL, el DDL mismo hace un commit.
create table detalletipoInfraxPapeleta(codPapeleta number, codTipoInfraccion number, monto number);
-- Después de este CREATE TABLE, la inserción anterior (valor 6) se ha confirmado implícitamente.

-- Formato de columnas para una mejor visualización en SQL*Plus
column CODIGO format 999
column DESCRIPCION format a40
column IMPORTE format 99999,99

select * from tipoinfraccion;

insert into tipoinfraccion(codigo,importe) values (7,100); -- Inserción con valores nulos para descripción
select * from tipoinfraccion;

SQL> insert into tipoinfraccion(importe) values (9); -- Error: CODIGO no puede ser nulo (PK)
insert into tipoinfraccion(importe) values (9)
*
ERROR at line 1:
ORA-01400: cannot insert NULL into ("FRICCIO"."TIPOINFRACCION"."CODIGO")

-- ==================== UPDATE ====================
SQL> update tipoinfraccion set IMPORTE=600 where codigo=1;
-- 1 row updated. (Ejemplo teórico, ya que la tabla se crea sin datos y luego se insertan 5, 6, 7)

SQL> update tipoinfraccion set importe=importe*1.1 where codigo=2 or codigo=6;
-- 2 rows updated. (Ejemplo teórico, asumiendo datos existentes)

SQL> update tipoinfraccion set descripcion='N/C' where descripcion is NULL;
-- Esta operación actualizará la fila con codigo=7 (donde la descripción era NULL)
-- 1 row updated.

SQL> update tipoinfraccion set IMPORTE=IMPORTE*0.5, DESCRIPCION=DESCRIPCION||'('||length(DESCRIPCION)||')';
-- Actualiza todas las filas (ejemplo teórico, ya que la cláusula WHERE está ausente).
-- 5 rows updated.

-- ==================== DELETE ====================

SQL> delete from tipoinfraccion; -- Elimina todas las filas
-- 5 rows deleted.

SQL> rollback; -- Deshace el DELETE anterior, recuperando las filas.
-- Rollback complete.


SQL> delete from tipoinfraccion where importe<=100; -- Elimina filas con importe menor o igual a 100
-- 2 rows deleted.

SQL> commit; -- Confirma la eliminación.
-- Commit complete.


-- ==================== TRUNCATE ====================
-- TRUNCATE es un comando DDL que elimina todas las filas de una tabla, y no puede ser deshecho con ROLLBACK.
-- También reinicia el contador de alto nivel de la tabla (si existe).

SQL> create table ejemplo2(campo1 number);
-- Table created.

SQL> insert into ejemplo2 values (1);
-- 1 row created.

SQL> insert into ejemplo2 values (2);
-- 1 row created.

SQL> commit;
-- Commit complete.

SQL> select * from ejemplo2;
/*
    CAMPO1
----------
         1
         2
*/

SQL> truncate table ejemplo2;
-- Table truncated.

SQL> select * from ejemplo2;
-- no rows selected

SQL> rollback; -- TRUNCATE no puede ser deshecho.
-- Rollback complete. (No tiene efecto sobre el TRUNCATE)


-- ==================== SELECT ==================== 

SQL> select * from tipoinfraccion;
/*
CODIGO DESCRIPCION                              IMPORTE
------ ---------------------------------------- -------
     1 Luz roja                                     450
     2 Exceso de velocidad                          420
*/
-- Asumiendo los datos de un punto anterior.

SQL> select CODIGO,DESCRIPCION,IMPORTE from tipoinfraccion;
/*
CODIGO DESCRIPCION                              IMPORTE
------ ---------------------------------------- -------
     1 Luz roja                                     450
     2 Exceso de velocidad                          420
*/

SQL> select * from tipoinfraccion where IMPORTE>=450;
/*
CODIGO DESCRIPCION                              IMPORTE
------ ---------------------------------------- -------
     1 Luz roja                                     450
*/

SQL> select distinct descripcion from tipoinfraccion;
/*
DESCRIPCION
----------------------------------------
Luz roja
Exceso de velocidad
*/

SQL> select distinct codigo,descripcion from tipoinfraccion;
/*
CODIGO DESCRIPCION
------ ----------------------------------------
     1 Luz roja
     2 Exceso de velocidad
     3 Luz roja
*/
-- (Asumiendo que 'Luz roja' se repite con un CODIGO diferente en este punto del demo)


SQL> select count(*) from tipoinfraccion;
/*
  COUNT(*)
----------
         3
*/

-- ==================== Flashback (Solo disponible en Oracle) ====================
-- Herramientas avanzadas de recuperación de datos.

-- Flashback Query (Permite consultar datos como estaban en un momento anterior)
SQL> select * from tipoinfraccion;
/*
CODIGO DESCRIPCION                              IMPORTE
------ ---------------------------------------- -------
     1 Luz roja                                     450
     2 Exceso de velocidad                          420
     3 Luz roja                                     600
*/

SQL> select * from tipoinfraccion as of timestamp sysdate-1/24/60*90;
-- Consulta datos de 90 segundos atrás.
/*
CODIGO DESCRIPCION                              IMPORTE
------ ---------------------------------------- -------
     1 Luz roja                                     450
     2 Exceso de velocidad                          420
*/

SQL> show parameter undo;
/*
NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
undo_management                      string      AUTO
undo_retention                       integer     900
undo_tablespace                      string      UNDOTBS1
*/

-- Flashback Table (Permite revertir una tabla a un estado anterior)
SQL> delete from tipoinfraccion;
-- 3 rows deleted.

SQL> commit;
-- Commit complete.


-- 1ra solución (Recuperación manual usando Flashback Query)
insert into tipoinfraccion select * from tipoinfraccion as of timestamp sysdate-1/24/60*4;

-- 2da solución (Usando Flashback Table)
SQL> alter table tipoinfraccion enable row movement;
-- Table altered.

SQL> flashback table tipoinfraccion to timestamp sysdate-1/24/60*10;
-- Flashback complete.

SQL> alter table tipoinfraccion disable row movement;
-- Table altered.

SQL> select * from tipoinfraccion;
/*
CODIGO DESCRIPCION                              IMPORTE
------ ---------------------------------------- -------
     1 Luz roja                                     450
     2 Exceso de velocidad                          420
     3 Luz roja                                     600
*/

-- ==================== Ejemplo DCL (Data Control Language) ====================
-- Otorgar privilegios de SELECT en cualquier tabla a varios usuarios.

grant select any table to usuario1;
grant select any table to usuario2;
grant select any table to usuario3;
grant select any table to usuario4;
grant select any table to usuario5;
grant select any table to usuario6;
grant select any table to usuario7;
grant select any table to usuario8;
grant select any table to usuario9;
grant select any table to usuario10;
grant select any table to usuario11;
grant select any table to usuario12;
grant select any table to usuario13;
grant select any table to usuario14;
grant select any table to usuario15;
grant select any table to usuario16;
grant select any table to usuario17;
grant select any table to usuario18;
grant select any table to usuario19;
grant select any table to usuario20;
grant select any table to usuario21;
```
---

---

## Ejemplos Adicionales de `SQLQuery1.sql`

### Script 1-2: Creación y Eliminación de Bases de Datos y Tablas

Ejemplos básicos de DDL para crear y eliminar bases de datos y tablas.

```sql
/*Script 1*/
create database tutorial;
create database prueba;
drop database tutorial;
drop database prueba;

/*Script 2*/
create database tutorial;
use tutorial
create table usuarios2
(
id_usuario int  not null,
nombre varchar(50)
)
;
drop table usuarios2
```

### Script 3: Creación de Tabla e Inserción de Datos

Ejemplo de `CREATE TABLE` con `PRIMARY KEY` y múltiples sentencias `INSERT` para poblar la tabla. También incluye consultas `SELECT` básicas para verificar los datos.

```sql
/*Scrip 3*/
create table usuarios
(
id_usuarios int primary key,
nombre varchar(50) not null,
edad int not null
);
insert into usuarios values(1,'miguel',56);
insert into usuarios values(2,'miguel',56);
insert into usuarios values(3,'miguel',56);
insert into usuarios values(4,'miguel',41);
insert into usuarios values(5,'miguel',31);
insert into usuarios values(6,'miguel',71);
insert into usuarios values(7,'miguel',91);
select * from usuarios;
select * from usuarios where edad >50;
select * from usuarios where edad<40;
```

### Script 4: Comandos `DELETE`, `TRUNCATE` y `DROP`

Demostración de las diferencias entre `DELETE` (eliminar filas), `TRUNCATE` (resetear tabla) y `DROP` (eliminar tabla).

```sql
/*Scrip 4:*/
/*Delete : elimna una fila a mas*/
/*drop : elimna tabla*/
/**truncate: resetear toda la tabla*/
Select * from usuarios where nombre = 'Alex';
insert into usuarios values(10,'alex',23);
select * from usuarios where edad = 23;
create table pruebas(
nombre varchar(50) not null,
edad int not null
);

insert into pruebas values('david',11);
insert into pruebas values('manuel',22);
insert into pruebas values('mariana',6);

select * from pruebas;
delete from pruebas;
delete from usuarios where id_usuarios = 10;
select * from usuarios;
truncate table pruebas;
drop table pruebas;
```

### Script 5: Comando `UPDATE`

Ejemplo de cómo modificar registros existentes en una tabla usando la sentencia `UPDATE`.

```sql
/*Scrip 5*/
select * from usuarios;
update usuarios set nombre = 'alex' where id_usuarios = 2;
update usuarios set edad =23 where id_usuarios = 1;
```
---

### Script 6-8: Campos `IDENTITY` y Consultas con Expresiones

Estos scripts muestran cómo usar campos `IDENTITY` para valores autoincrementales y cómo realizar cálculos y manipulaciones de datos directamente en la sentencia `SELECT`.

```sql
/*Scrip 6 */
/*Identity*/
create table usuario2
(
id_usuario int identity ,
nombre varchar(50) not null
);

/*Scrip 7*/
insert into usuario2 values('a');
insert into usuario2 values('b');
insert into usuario2 values('c');
insert into usuario2 values('d');
insert into usuario2 values('e');
select * from usuario2;

/*Scrip 8:video 13*/
create database libreria;
use libreria;
create table libros
(
id_libro int identity primary key,
nombre varchar(50) not null,
precio_venta int not null,
precio_compra float not null
);

insert into libros values('El Lobo',115,95.23);
insert into libros values('Caperucita Roja',236,189.25);
-- ... (más inserciones) ...
select * from libros;
/*Precio de Venta - precio compra*/
select nombre, 10*(precio_venta - precio_compra) as Ganancia_10_libros from libros where id_libro >1;
/*Actualizar*/
update libros set precio_venta = precio_venta + (precio_venta*0.1) where id_libro =1;
```

### Script 9, 11, 12: Funciones de Cadena y Fecha

Ejemplos de funciones de SQL Server para manipular cadenas de texto (concatenación, mayúsculas, minúsculas, subcadenas) y para trabajar con fechas (obtener partes de una fecha, calcular diferencias).

```sql
/*Scrip 9:concatenacion*/
select 'Libros : '+nombre+' ' from libros where id_libro=1;
select precio_venta as 'Precio de venta s/.' , precio_compra as 'precio de compra S/.' from libros;

/*Scrip 11:hola a todos*/
select SUBSTRING('hola a todos ',8,1);
select STR(123);
select STUFF ('cambiando el world',14,5,'mundo');
select len ('cambiando el world');
select CHAR(78);/*codigo asci*/
select lower('MI NOMBRE ES LUIS') AS Algo;
select UPPER('     MI NOMBRE ES JHONATAN') AS ALGO;
select LTRIM('                    MI NOMBRE ES JHONATAN               ') AS ALGO;
select RTRIM('                    MI NOMBRE ES JHONATAN               ') AS ALGO;
select REPLACE('HOLA WORLD','WORLD','MUNDO');
select REVERSE('anita la tina');
select PATINDEX('%luis%','donde esta luis?');
select REPLICATE('Hola ',10);
select 'luis ' + SPACE(8) + ' jhonatan';

/*Scrip 12: FECHAS*/
select GETDATE();
select DATEPART(year,GETDATE());
select DATEPART(MONTH,GETDATE());
select DATEPART(DAY,GETDATE());
select DATENAME(MONTH,GETDATE());
select DATEDIFF(day,'2014/01/03','2017/04/03');
select DATEDIFF(MONTH,'2014/01/03','2017/04/03');
select DATEDIFF(YEAR,'2014/01/03','2017/04/03');
select YEAR(GETDATE());
```

### Script 13-14: Ordenamiento y Operadores Lógicos

Uso de `ORDER BY` para ordenar los resultados y de los operadores lógicos `NOT`, `AND`, `OR` para construir condiciones de filtrado complejas.

```sql
/*Scrip 13: Order by*/
use libreria2;
select  * from libros order by precio_venta desc;

/*Scrip 14: Operadores Negativos*/
/*
         | not | and | or |
*/
select * from libros where not titulo = 'Ladron de sueños';
select * from libros where not autor ='Karla Sanchez' and not titulo = 'Ladron de sueños';
select * from libros order by precio_compra asc;
select * from libros where precio_compra < 120;
select * from libros where precio_venta = 128 or precio_venta < 245;
```

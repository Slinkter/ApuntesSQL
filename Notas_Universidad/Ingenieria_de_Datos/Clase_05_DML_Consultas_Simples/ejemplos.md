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

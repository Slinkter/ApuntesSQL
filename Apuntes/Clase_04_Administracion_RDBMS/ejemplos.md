# Ejemplos - Clase 04: Administración de RDBMS

## Optimización de Consultas con Hints PARALLEL (2 de Septiembre de 2013)

Este script introduce el concepto de "hints" en SQL, que son directivas de compilación que influyen en el optimizador de la base de datos para ejecutar una consulta de una manera específica. Se enfoca en el hint `PARALLEL`, que permite la ejecución paralela de consultas para mejorar el rendimiento, especialmente en escenarios de grandes volúmenes de datos o reportes gerenciales.

```sql
/* Apuntes 
ps -ef => Muestra todos los procesos que estan actualmente corriendo en el sistema operativo.
ps -ef | grep oracle => Muestra todos los procesos que estan corriendo con el usuario oracle.
kill -9 # => Matamos un proceso del sistema operativo
select /*+ ... * => Definimos un hint, el cual es una directiva de compilacion.
PARALLEL(alias,#procesos_paralelo) 
=> Definimos que el query se ejecute con n procesos en paralelo, por lo cual ejecutara mas rapido el query.
	Debe usarse cuando:
		a) El proceso no es concurrente (ejemplo: Un reporte gerencial).
		b) El grado de paralelismo debe ser como maximo # de cores del servidor x 2 (Caso Intel),
                   para el caso de IBM  Power 7 (# procesos en paralelo x 4).
*/



select /*+ PARALLEL(d,6) */ * from demo1 d;

select /*+ PARALLEL(d,6) */ campo1,campo2 from demo1 d;

select /*+ PARALLEL(d1,6), PARALLEL(d2,8) */ campo1,campo2 from demo1 d1, demo2 d2;

SQL> create table demo2 (campo1 number);

Table created.

SQL> alter table demo2 parallel(degree 4);

Table altered.

-- Tarea: Como hacer insert/delete/update en paralelismo.
```
---

## Script DDL para Creación y Modificación de Tablas (26 de Agosto de 2013)

Este script demuestra una serie de comandos DDL (Data Definition Language) para la creación de esquemas de bases de datos, incluyendo la definición de tablas, claves primarias, claves foráneas, restricciones de unicidad, restricciones de verificación y valores por defecto. Es un ejemplo práctico de cómo se define la estructura lógica y física de una base de datos relacional.

```sql
-- Conexión inicial (ejemplo: sqlplus usuario1/oracle@192.168.17.40:1521/orcl)

-- ==================== CREACIÓN DE TABLAS ===================

create table CLIENTE
(
 codigo number,
 nombre varchar(20),
 numtelf varchar(9),
 direccion varchar(50),
 ciudad varchar(10)
);

create table PERRO
(
 codigo number,
 codcliente number,
 nombre varchar(10),
 sexo char(1),
 fnac date,
 codraza number
);

create table RAZA
(
 codigo number,
 nombre varchar(20)
);

create table SERVICIO
(
 codigo number,
 fechaserv date,
 pesoperro number(3,1),
 tipo number,
 precio number(5,2),
 codperro number 
);

create table OBSERVACION
(
 tipo varchar(10),
 descripcion varchar(100),
 codperro number
);

create table TIPOSERVICIO
(
 codigo number,
 descripcion varchar(20),
 TiempoRecIni interval year to month,
 TiempoRecFin interval year to month
);


-- ==================== RESTRICCIÓN NOT NULL ===================

alter table CLIENTE modify nombre not null;
alter table PERRO modify nombre not null;
alter table PERRO modify fnac not null;

-- ==================== CLAVES PRIMARIAS (PK) ===================

alter table CLIENTE add constraint PK_CLIENTE primary key (codigo);
alter table PERRO add constraint PK_PERRO primary key (codigo);
alter table RAZA add constraint PK_RAZA primary key (codigo);
alter table TIPOSERVICIO add constraint PK_TIPOSERVICIO primary key (codigo);
alter table SERVICIO add constraint PK_SERVICIO primary key (codigo);
alter table OBSERVACION add constraint PK_OBSERVACION primary key(tipo,descripcion,codperro);

-- ==================== CLAVES FORÁNEAS (FK) ===================
alter table PERRO add constraint FK_PERRO_CLIENTE foreign key (codcliente) references CLIENTE(codigo);
alter table PERRO add constraint FK_PERRO_RAZA foreign key (codraza) references RAZA(codigo);
alter table OBSERVACION add constraint FK_OBSERVACION_PERRO foreign key (codperro) references PERRO(codigo);
alter table SERVICIO add constraint FK_SERVICIO_TIPOSERVICIO foreign key (tipo) references TIPOSERVICIO(codigo);
alter table SERVICIO add constraint FK_SERVICIO_PERRO foreign key (codperro) references PERRO(codigo);

-- ==================== RESTRICCIÓN UNIQUE (UQ) ===================
alter table RAZA add constraint UQ_RAZA unique (nombre);
alter table TIPOSERVICIO add constraint UQ_TIPOSERVICIO_DESC unique (descripcion);

-- ==================== RESTRICCIONES CHECK (CC) ===================
alter table PERRO add constraint CC_PERRO_SEXO 
check (sexo in ('F','M','f','m')); -- Corregido 'f,' a 'f' y 'm,' a 'm'
alter table SERVICIO add constraint CC_SERVICIO_PRECIO check (precio>=0);
alter table SERVICIO add constraint CC_SERVICIO_PESOPERRO check (pesoperro>=0);

-- ==================== CARDINALIDAD (Implica NOT NULL en FK si es obligatoria) ===================

alter table PERRO modify codcliente not null; -- codcliente en PERRO no puede ser nulo
alter table SERVICIO modify codperro not null; -- codperro en SERVICIO no puede ser nulo

-- ==================== COMENTARIOS ===================

comment on table PERRO is 'Entidad Perro para almacenar los perros';
comment on column PERRO.sexo is 'Solo esta permitido F o M';

-- ==================== VALOR POR DEFECTO (DEFAULT) ===================

alter table PERRO modify sexo default 'F';

-- =================== ADICIONAL (Ejemplos de ALTER TABLE) ==================

-- Ejemplo de cómo añadir una columna:
-- alter table nombreTabla add nombreColumna TipoDato;
-- Ejemplo de cómo eliminar una restricción:
-- alter table OBSERVACION drop constraint PK_OBSERVACION;
```
---

## Demo y DDL Avanzado (28 de Agosto de 2013)

Este script contiene una mezcla de operaciones DDL y DML básicas, incluyendo la creación de tablas, vistas, secuencias, índices y sinónimos. También se presentan ejemplos de manipulación de tablas y, lo más notable, diversas técnicas de particionamiento de tablas, lo que lo convierte en un excelente recurso para la administración de RDBMS.

```sql
====DEMO====

SQL> create table salon (numPiso number, cod number, tipo char(1));

Table created.

SQL> insert into salon values (3,301,'C');

1 row created.

SQL> insert into salon values (4,402,'C');

1 row created.

SQL> insert into salon values (5,501,'S');

1 row created.

SQL> commit;

Commit complete.

SQL> select * from salon;

   NUMPISO        COD T
---------- ---------- -
         3        301 C
         4        402 C
         5        501 S

SQL> create view vsalon_01 as select * from salon where tipo='C';

View created.

SQL> select * from salon;

   NUMPISO        COD T
---------- ---------- -
         3        301 C
         4        402 C
         5        501 S

SQL> select * from vsalon_01;

   NUMPISO        COD T
---------- ---------- -
         3        301 C
         4        402 C


SQL>  create sequence seqSalon start with 0 increment by 2 minvalue 0;

Sequence created.


SQL> select seqSalon.nextval from dual;

   NEXTVAL
----------
         0

SQL> select seqSalon.nextval from dual;

   NEXTVAL
----------
         2


SQL> create index isalon on salon(numpiso,tipo);

Index created.


SQL> create synonym alias1 for salon;

Synonym created.

SQL> select * from alias1;

   NUMPISO        COD T
---------- ---------- -
         3        301 C
         4        402 C
         5        501 S
        -1       -101 C


====================================DDL========================================

SQL> create table persona (cod number, dni number, nombre varchar(25));

Table created.

SQL> alter table persona add edad number;

Table altered.

SQL> alter table persona drop column dni;

Table altered.

SQL> drop table persona;

Table dropped.


================================================================================

-- Creación de Tablespaces para Particionamiento
create tablespace TBSEJEMPLO1 datafile '/u01/ejemplo01.dbf' size 100M;
create tablespace TBSEJEMPLO2 datafile '/u01/ejemplo02.dbf' size 100M;
create tablespace TBSEJEMPLO3 datafile '/u01/ejemplo03.dbf' size 100M autoextend on next 200M maxsize unlimited;


-- Particionamiento por Rango (Range Partitioning)
create table SERVICIO1(
 codigo number,
 fechaserv date,
 pesoperro number(3,1),
 tipo number,
 precio number(5,2)
)
partition by range(precio)
(
 partition p1 values less than(300) tablespace TBSEJEMPLO1,
 partition p2 values less than(600) tablespace TBSEJEMPLO2,
 partition p3 values less than(999) tablespace TBSEJEMPLO3
);

-- Particionamiento por Lista (List Partitioning)
create table SERVICIO2(
 codigo number,
 fechaserv date,
 pesoperro number(3,1),
 tipo char(1),
 precio number(5,2)
)
partition by list(tipo)
(
 partition parte1 values ('C','L','P') tablespace TBSEJEMPLO1,
 partition parte2 values ('O','A') tablespace TBSEJEMPLO2
);

-- Particionamiento por Hash (Hash Partitioning)
create table SERVICIO3(
 codigo number,
 fechaserv date,
 pesoperro number(3,1),
 tipo char(1),
 precio number(5,2)
)
partition by hash(pesoperro) 
partitions 3 store in (TBSEJEMPLO1,TBSEJEMPLO2,TBSEJEMPLO3);

--> Las particiones de tipo by hash se recomienda crearlas con la formula (2^n)


-- 3 tipos de particionamiento: by range, by list, by hash => Oracle 8i


-- Sub Particionamientos (Subpartitions)
---------------------

create table SERVICIO4(
 codigo number,
 fechaserv date,
 pesoperro number(3,1),
 tipo number,
 precio number(5,2)
)
partition by range(precio) subpartition by hash(tipo)
 subpartition template(
   subpartition sp1 tablespace TBSEJEMPLO1,
   subpartition sp2 tablespace TBSEJEMPLO2
 )
 (
   partition p1 values less than (300),
   partition p2 values less than (maxvalue)
);
 
---> Migracion de tabla simple a particionada

-- 1) Crear la tabla particionada sin datos pero con otro nombre y ademas que tenga 1 
--    sola particion.

create table SERVICIO6(
 codigo number,
 fechaserv date,
 pesoperro number(3,1),
 tipo number,
 precio number(5,2),
 codperro number
)
partition by range(precio)
(
 partition p1 values less than(maxvalue) tablespace TBSEJEMPLO1
);

alter table servicio drop constraint PK_SERVICIO;

--> En esta linea se realiza la migracion, despues aqui la tabla SERVICIO ya esta particionada
alter table servicio6 exchange partition p1 with table servicio including indexes without validation;

drop table servicio;
alter table servicio6 rename to servicio;

alter table servicio split partition p1 at (500) into (partition p2, partition p3);

select PARTITION_NAME, HIGH_VALUE from dba_tab_partitions where table_owner='FRICCIO' and table_name = 'SERVICIO';

-- Ejemplo de creación de usuario y otorgamiento de privilegios (sysdba context)
sqlplus / as sysdba
create user xxx identified by tuclave;  
grant dba to xxx;
```
---

## Manejo de LOBs, Generación de DDL y Cargas Masivas (9 de Septiembre de 2013)

Este script cubre temas de administración de datos más avanzados, como el manejo de tipos de datos de objetos grandes (LOBs) para almacenar archivos multimedia (`BFILE`, `BLOB`), el uso de `DBMS_METADATA.GET_DDL` para regenerar el código fuente de los objetos de la base de datos y la utilización de la herramienta `SQL*Loader` para realizar cargas masivas de datos de manera eficiente.

```sql
/* Apuntes sobre LOBs (Large Objects)
BLOB=>El archivo multimedia esta grabado dentro de la BD.
BFILE=>Apunta a un archivo del sistema operativo.
RAW=>Similar al BLOB (guarda el contenido multimedia en la
BD, pero se utiliza para versiones 8i hacia abajo)

LOB-> BFILE o BLOB      CLOB=>texto (4gb-1bytes)
*/

-- ==================== Manejo de BFILEs ====================

SQL> create table Papeleta(cod number, fecha date default sysdate, foto bfile);
-- Table created.

-- Para usar BFILEs, se necesita subir el archivo al servidor.
-- 1. Crear un directorio en el sistema operativo del servidor:
-- [friccio@SERVIDORORACLE ~]$ cd /tmp
-- [friccio@SERVIDORORACLE tmp]$ mkdir friccio

-- 2. Subir el archivo al directorio creado (usando FTP, Samba, etc.).
/* Ejemplo de sesión FTP:
C:\Temp>ftp 192.168.17.40
Connected to 192.168.17.40.
User (192.168.17.40:(none)): friccio
Password:
230 Login successful.
ftp> cd /tmp/friccio
250 Directory successfully changed.
ftp> put foto.jpg
*/

-- 3. Crear un objeto DIRECTORY en Oracle que apunte al directorio del SO.
SQL>create or replace directory DIR_friccio as '/tmp/friccio/';

-- 4. Insertar la referencia al archivo usando la función BFILENAME.
SQL> insert into papeleta(cod,foto) values (1,BFILENAME('DIR_friccio','foto.jpg'));
-- 1 row created.

SQL> commit;
-- Commit complete.


-- ==================== Regenerar Código Fuente (DDL) ====================
-- Usar el paquete DBMS_METADATA para extraer el DDL de los objetos existentes.

set pages 999
set long 90000

-- Extraer DDL para una tabla:
select dbms_metadata.get_ddl('TABLE','PERRO','FRICCIO')
from dual;

-- Crear una vista para el ejemplo:
create view vreporte as select * from perro;

-- Extraer DDL para una vista:
select dbms_metadata.get_ddl('VIEW','VREPORTE','FRICCIO')
from dual;

-- ==================== Cargas Masivas (SQL*Loader) ====================

-- 1. Crear el archivo de datos fuente (ej. reporte.txt)
/* Contenido de reporte.txt:
01,XYZ,70
01,ABC,70
01,DEF,31
01,FGE,21
01,PLQ,73
01,XW,80
01,XYZ,6
01,XYZ,10
01,XYZ,20
01,XYZ,10
01,XYZ,90
01,XYZ,80
*/


-- 2. Crear el archivo de control (ej. control.txt)

-- Opción 1: Carga convencional
/*
LOAD DATA
INFILE 'C:\TEMP\REPORTE.TXT'
BADFILE 'C:\TEMP\REPORTE.BAD'
DISCARDFILE 'C:\TEMP\REPORTE.DIS'
INTO TABLE EMPLEADO APPEND
FIELDS TERMINATED BY ',' (COD,NOMBRE,EDAD)
*/

-- Opción 2: Carga Directa (más rápida)
/*
OPTIONS (DIRECT=TRUE)
LOAD DATA
INFILE 'C:\TEMP\REPORTE.TXT'
BADFILE 'C:\TEMP\REPORTE.BAD'
DISCARDFILE 'C:\TEMP\REPORTE.DIS'
INTO TABLE EMPLEADO APPEND
FIELDS TERMINATED BY ',' (COD,NOMBRE,EDAD)
*/
-- Nota: Con DIRECT=TRUE, la carga masiva puede ser un 50-75% más rápida,
-- pero la tabla se bloquea completamente durante la carga.

-- 3. Ejecutar SQL*Loader desde la línea de comandos del sistema operativo.
-- sqlldr userid=friccio/oracle@192.168.17.40:1521/orcl control=control.txt
```
---

## Consultas al Diccionario de Datos y Gestión de Usuarios (11 de Septiembre de 2013)

Este script muestra cómo consultar el diccionario de datos de Oracle para obtener información sobre los objetos de la base de datos, como tablas y restricciones. También incluye ejemplos de comandos de administración de usuarios y copias de seguridad lógicas (export).

```sql
-- Consultar las restricciones de una tabla
SQL> select constraint_name, constraint_type from user_constraints where table_name = 'CLIENTE';
/*
CONSTRAINT_NAME                C
------------------------------ -
PK_CLIENTE                     P
FK_CLIENTE_CIUDAD              R
SYS_C0027113                   C
SYS_C0027114                   C
*/


-- Listar todas las tablas del usuario actual
SQL> select table_name from user_tables;
/*
TABLE_NAME
------------------------------
EMPLEADO
CLIENTE_EMPLEADO
DETALLE_CUENTA
CUENTA
DETALLE_PAGO_PRESTAMO
PRESTAMO
CLIENTE_PRESTAMO
CIUDAD
ACTIVO
SUCURSAL
CLIENTE
*/

-- Ejemplo de Export (exp) - Utilidad de línea de comandos para backup lógico
C:\>exp userid=usuario3/oracle@192.168.17.40:1521/orcl file=C:\TEMP\mibk.dmp owner=usuario3 log=C:\TEMP\mibk.log

-- Ejemplo de modificación de contraseña de un usuario
alter user usuario1 identified by peru2013;
```
---

## Creación y Uso de Vistas (28 de Octubre de 2013)

Este script muestra cómo crear y utilizar vistas, que son consultas almacenadas que se comportan como tablas virtuales. Las vistas pueden simplificar consultas complejas y aplicar una capa de seguridad.

```sql
-- Crear una vista simple que muestra el total de empleados
create or replace view vTotalEmpleados
as
 select count(*) as total from hr.employees;

-- Crear una vista que muestra todos los datos de la tabla de empleados
create or replace view vEmpleado
as
 select * from hr.employees;

-- Crear una tabla para el ejemplo de vista actualizable
create table aula (cod number, seccion number);

-- Crear una vista simple sobre la tabla 'aula'
create view vaula
as
 select cod,seccion from aula;

-- Insertar datos a través de la vista (esto es posible porque la vista es simple y se basa en una sola tabla)
SQL> insert into vaula values (1,601);
-- 1 row created.

SQL> commit;
-- Commit complete.

-- Verificar que la inserción se reflejó en la tabla base
SQL> select * from aula;
/*
       COD    SECCION
---------- ----------
         1        601
*/
```
---
---

## Ejemplos Adicionales de `SQLQuery1.sql`

### Script 15: Modificación de Tablas con `ALTER TABLE`

Ejemplos de cómo añadir y eliminar columnas de una tabla existente utilizando el comando `ALTER TABLE`.

```sql
/*Scrip 15: */
create database libreria3;
use libreria3;
create table libros(
id_libro int identity primary key,
nombre varchar(50) not null,
precio_venta float not null,
precio_compra float not null
);

/*Eliminar columna */
alter table libros drop column nombre ;
alter table libros drop column precio_venta;
alter table libros drop column precio_compra;

/*Agregar columna */
alter table libros add nombre varchar(50);
alter table libros add precio_venta float  not null;
alter table libros add precio_compra float not null;
```

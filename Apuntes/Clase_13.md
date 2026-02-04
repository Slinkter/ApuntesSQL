# Clase 13: Programación en Base de Datos II: Temas Avanzados de PL/SQL

---

## 📚 Conceptos Clave

**Fecha:** Noviembre 18, 2025 (Inferido del periodo del curso)

---

## Notas Generales

### Manejo de Estructuras Complejas

PL/SQL permite la creación y manipulación de estructuras de datos más complejas que las variables escalares:

*   **Registros (Records):** Permiten agrupar un conjunto de campos de diferentes tipos de datos, similar a una estructura en otros lenguajes de programación. Pueden ser basados en tablas (`%ROWTYPE`) o definidos por el usuario.
*   **Index By Tables (Tablas Asociativas):** Arreglos unidimensionales que se indexan por un `BINARY_INTEGER`, `PLS_INTEGER` o `VARCHAR2`. Son flexibles y no requieren inicialización previa de los nodos.
*   **Nested Tables (Tablas Anidadas):** Arreglos unidimensionales que pueden ser almacenados como columnas de tabla. Se inicializan y requieren el método `EXTEND` para añadir elementos.
*   **VArrays (Vectores de Tamaño Variable):** Arreglos unidimensionales con un tamaño máximo predefinido. También pueden almacenarse como columnas de tabla y requieren `EXTEND`.

### Manejo de Cursores

Un cursor es un puntero a un área de memoria en la que se almacenan los resultados de una sentencia `SELECT`.

*   **Cursores Implícitos:** Creados automáticamente por Oracle para cada sentencia DML o `SELECT INTO`.
*   **Cursores Explícitos:** Definidos por el programador para manejar consultas `SELECT` que devuelven múltiples filas.
    *   **Ciclo de vida:** `DECLARE` (definir cursor), `OPEN` (abrir cursor), `FETCH` (obtener filas), `CLOSE` (cerrar cursor).
    *   **Atributos de Cursor:** `%ISOPEN`, `%NOTFOUND`, `%FOUND`, `%ROWCOUNT`.
    *   **Cursores con Parámetros:** Permiten reutilizar la misma definición de cursor con diferentes valores.
    *   **Cursores Genéricos (REF CURSOR):** Tipos de cursor flexibles que pueden asociarse a diferentes sentencias `SELECT` en tiempo de ejecución.
    *   **`WHERE CURRENT OF`:** Permite actualizar o borrar la fila actual apuntada por un cursor, requiere `SELECT FOR UPDATE`.

### Manipulación de Excepciones

PL/SQL proporciona un robusto mecanismo para manejar errores de tiempo de ejecución (excepciones).

*   **Bloque `EXCEPTION`:** Sección en un bloque PL/SQL donde se captura y maneja un error.
*   **Excepciones Predefinidas:** Errores comunes de Oracle (ej. `NO_DATA_FOUND`, `TOO_MANY_ROWS`).
*   **Excepciones Definidas por el Usuario:** Se pueden declarar excepciones propias y asociarlas a códigos de error Oracle (`PRAGMA EXCEPTION_INIT`).
*   **`SQLERRM` y `SQLCODE`:** Funciones que devuelven el mensaje y el código del último error.
*   **`WHEN OTHERS THEN`:** Captura cualquier excepción no manejada específicamente.
*   **`RAISE_APPLICATION_ERROR`:** Permite lanzar errores personalizados con códigos y mensajes definidos por el usuario.

### Creación de Stored Procedures y Funciones

*   **Procedimientos Almacenados:** Subprogramas que realizan acciones. Sintaxis: `CREATE OR REPLACE PROCEDURE nombre (parametros) IS ... BEGIN ... END;`. Parámetros pueden ser `IN`, `OUT`, `IN OUT`.
*   **Funciones:** Subprogramas que calculan y devuelven un valor. Sintaxis: `CREATE OR REPLACE FUNCTION nombre (parametros) RETURN tipo IS ... BEGIN ... RETURN valor; END;`.

### Creación de Paquetes

Un paquete es una agrupación lógica de variables, cursores, procedimientos y funciones relacionados.

*   **Especificación (Specification):** Define la interfaz pública del paquete (lo que es visible desde fuera).
*   **Cuerpo (Body):** Contiene la implementación de los subprogramas declarados en la especificación y puede incluir elementos privados.
*   **Beneficios:** Modularidad, ocultación de información, rendimiento (carga una vez en memoria).

### Creación de Triggers

Los triggers son subprogramas que se disparan automáticamente en respuesta a eventos de la base de datos (DML, DDL, eventos de la base de datos).

*   **Tipos:**
    *   **Triggers DML:** Se disparan en operaciones `INSERT`, `UPDATE`, `DELETE`. Pueden ser `BEFORE` o `AFTER`, y `FOR EACH ROW` (nivel de fila) o de sentencia (nivel de sentencia).
    *   **Triggers `INSTEAD OF`:** Se usan para actualizar vistas no modificables directamente.
*   **Variables de Transición:** `:NEW` (valores después de la operación), `:OLD` (valores antes de la operación).
*   **Restricciones:** No pueden crear objetos en `SYS`, ni confirmar o anular transacciones DML.

### Consideraciones en el Diseño de Código PL/SQL

*   **Ejecución de Operaciones DDL y DCL:** Se usa `EXECUTE IMMEDIATE` para ejecutar sentencias SQL dinámicas.
*   **`NOCOPY`:** Hint para pasar parámetros `OUT` e `IN OUT` por referencia, mejorando el rendimiento al evitar copias de datos grandes.
*   **`BULK COLLECT`:** Optimiza la recuperación de datos de cursores o sentencias `SELECT` al cargar múltiples filas en una colección (tabla indexada, tabla anidada, varray) con un solo "context switch".
*   **`FORALL`:** Optimiza la ejecución de sentencias DML (INSERT, UPDATE, DELETE) al aplicarlas a colecciones de datos con un solo "context switch".

### Programación Orientada a Objetos en PL/SQL

PL/SQL soporta conceptos de POO a través de **Tipos de Objeto**, que permiten definir objetos con atributos y métodos, soportando herencia (`UNDER`) y polimorfismo (`OVERRIDING`). Los objetos pueden ser almacenados en tablas.

---

## Pistas y Keywords

*   **Record (PL/SQL):** Estructura de datos para agrupar campos.
*   **%ROWTYPE:** Declaración de registro basada en una fila de tabla.
*   **Index By Table:** Arreglo asociativo indexado por BINARY_INTEGER/PLS_INTEGER/VARCHAR2.
*   **Nested Table:** Arreglo unidimensional, puede ser columna de tabla, necesita EXTEND.
*   **VArray:** Arreglo de tamaño fijo, puede ser columna de tabla, necesita EXTEND.
*   **Cursor:** Puntero a un conjunto de resultados SQL.
*   **OPEN, FETCH, CLOSE:** Ciclo de vida de un cursor explícito.
*   **%ISOPEN, %NOTFOUND, %FOUND, %ROWCOUNT:** Atributos de cursor.
*   **REF CURSOR:** Cursor genérico, flexible.
*   **EXCEPTION:** Bloque de manejo de errores.
*   **PRAGMA EXCEPTION_INIT:** Asociar excepción definida por usuario a código de error.
*   **SQLERRM, SQLCODE:** Funciones para obtener mensaje y código de error.
*   **RAISE_APPLICATION_ERROR:** Lanzar error personalizado.
*   **Stored Procedure:** Subprograma que realiza acciones.
*   **Function (PL/SQL):** Subprograma que devuelve un valor.
*   **Package:** Agrupación lógica de subprogramas y variables.
*   **Trigger:** Subprograma que se dispara por eventos (DML, DDL).
*   **:NEW, :OLD:** Variables de transición en triggers.
*   **EXECUTE IMMEDIATE:** Ejecutar SQL dinámico.
*   **NOCOPY:** Pasar parámetros por referencia.
*   **BULK COLLECT:** Optimizar FETCH múltiple de filas.
*   **FORALL:** Optimizar DML múltiple de filas.
*   **OOP PL/SQL:** Tipos de objeto, herencia, polimorfismo.

---

## Resumen Final Crítico

La segunda parte de PL/SQL profundiza en funcionalidades avanzadas que son indispensables para construir aplicaciones robustas, escalables y eficientes. El manejo de estructuras complejas (Records, colecciones), la gestión de cursores para el procesamiento de conjuntos de datos, y una sólida estrategia de manipulación de excepciones son pilares fundamentales para la fiabilidad del código. Además, la creación y organización de código a través de procedimientos, funciones, paquetes y triggers permite una modularidad y reutilización excepcionales. Finalmente, técnicas de optimización como `NOCOPY`, `BULK COLLECT` y `FORALL` son vitales para mejorar el rendimiento, mientras que la capacidad de PL/SQL para la programación orientada a objetos abre nuevas avenidas para el diseño de soluciones complejas. Dominar estos aspectos convierte a un desarrollador en un programador PL/SQL experto.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta clase es una continuación directa de los fundamentos de PL/SQL vistos en la Clase 12, construyendo sobre la sintaxis básica, la declaración de variables y las estructuras de control. También utiliza los conceptos de SQL y modelamiento de datos de clases previas para manipular y consultar la base de datos de manera programática.
*   **Conexiones Siguientes:** Los temas avanzados de PL/SQL son cruciales para el desarrollo de sistemas de Data Warehouse (Clase 14) y la implementación de soluciones en tópicos avanzados de bases de datos (Clase 15), donde la eficiencia, la automatización y la lógica de negocio compleja a menudo se implementan directamente en la capa de la base de datos.

---

## Material de Referencia

La siguiente documentación de Oracle fue utilizada como material de apoyo para esta clase. Se recomienda su revisión para una comprensión más profunda.

*   `../../Ingenieria de datos/0.Documentacion Oracle/Taller_Oracle_PLSQL_22112010.pdf`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Concepto_HA_CTG.pdf`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les01.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les02.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les03.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les04.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les05.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les06.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les07.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les08.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les09.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les10.ppt`
*   `../../Ingenieria de datos/0.Documentacion Oracle/Les11.ppt`

---

## 💡 Ejemplos Prácticos

## Ejemplos de Colecciones, Cursores, Procedimientos, Funciones y Triggers (11 de Noviembre de 2013)

Estos ejemplos cubren una amplia gama de temas avanzados de PL/SQL, incluyendo el uso de colecciones (tablas anidadas, varrays, tablas asociativas), gestión de cursores, la creación de procedimientos y funciones con diferentes tipos de parámetros, el uso de `BULK COLLECT` para rendimiento, y la implementación de triggers.

### 15. Colecciones: Tablas Anidadas (`TABLE OF`)
```sql
declare
 type tlista is table of number;
 v_lista tlista:=tlista();
begin
 for i in 1..10 loop
 	v_lista.extend;
	v_lista(i):=i*100;
 end loop;
 for i in 1..v_lista.count loop
 	dbms_output.put_line(v_lista(i));
 end loop;	
end;
/
```

### 16. Colecciones: `VARRAY`
```sql
declare
 type tlista is varray(50) of number;
 v_lista tlista:=tlista();
begin
 for i in 1..10 loop
 	v_lista.extend;
	v_lista(i):=i*100;
 end loop;
 for i in 1..v_lista.count loop
 	dbms_output.put_line(v_lista(i));
 end loop;	
end;
/
```

### 17. Colecciones: Tablas Asociativas (`INDEX BY PLS_INTEGER`)
También conocidas como "Hash Tables", no son densas y se indexan por un entero o una cadena.
```sql
declare
 type tlista is table of number index by pls_integer;
 v_lista tlista;
begin
 v_lista(2000):=60; -- Se puede asignar a un índice no secuencial
 for i in 1..10 loop
	v_lista(i):=i*100;
 end loop;
 -- dbms_output.put_line(v_lista.count); -- No se puede iterar sobre el count de esta forma
 -- Se debe usar FIRST, LAST, NEXT, PRIOR para recorrerlas si no son densas.
end;
/
```

### 19. `VARRAY` como Columna de Tabla
```sql
create type TEMAIL is varray(20) of varchar(25);
/

create table PERSONA (id number, nombre varchar(20), emails TEMAIL);

insert into PERSONA
values (1,'XYZ',TEMAIL('correo1','correo2','correo3'));

commit;

-- Actualizar un VARRAY en una tabla
declare
 v_lista TEMAIL;
 v_id number;
begin
 select id,emails
 into v_id,v_lista
 from persona where id = 1;
 
 v_lista.extend(); -- Añadir un nuevo espacio en el varray
 v_lista(v_lista.count):='correo_nuevo'; -- Asignar el nuevo valor
 
 update persona
 set emails=v_lista
 where id = v_id;
 
 commit;
end;
/
```

### 20. Cursores: Bucle Básico
```sql
declare
 cursor micursor is
	select last_name,salary from hr.employees;
 v_apellido varchar(50);
 v_salario number;
begin
 open micursor;
 loop
  fetch micursor into v_apellido,v_salario;
  exit when micursor%notfound;
  dbms_output.put_line(v_apellido||' '||v_salario);
 end loop;
 close micursor;
end;
/
```

### 21. Cursores: `FOR` Loop (más simple y seguro)
```sql
declare
 cursor micursor is
	select last_name,e.salary, department_name
        from hr.employees e join hr.departments d
        on e.department_id=d.department_id;
begin
 for c in micursor loop
  dbms_output.put_line(c.last_name||' '||c.department_name);
 end loop;
end;
/
```

### 22. Cursores con Parámetros
```sql
declare
 cursor micursor(par1 number) is
	select last_name,salary
        from hr.employees e
        where salary>par1;
begin
 for c in micursor(18000) loop
  dbms_output.put_line(c.last_name||' '||c.salary);
 end loop;
end;
/
```

### 24. Cursores y `UTL_FILE`
```sql
create or replace directory DIR_DAVID as '/tmp'; -- Asegúrate de que el directorio exista en el SO

declare
 v_archivo utl_file.file_type;
 cursor micursor(par1 number) is
	select last_name,salary
        from hr.employees e
        where salary>par1;
begin
 v_archivo:=utl_file.fopen('DIR_DAVID','friccio.txt','W');
 for c in micursor(5000) loop
  utl_file.put_line(v_archivo,c.last_name||' '||c.salary);
  dbms_output.put_line(c.last_name||' '||c.salary);
 end loop;
 utl_file.fclose(v_archivo);
end;
/
```

### 26. Procedimientos Almacenados
```sql
create or replace procedure spu_holaMundo
is
begin
 dbms_output.put_line('Hola Mundo');
end;
/

-- Para ejecutarlo:
execute spu_holaMundo;
-- o
-- begin spu_holaMundo; end; /
```

### 28. Procedimiento con Parámetro `IN`
```sql
create or replace procedure spu_listarEmpleados(ptotal number)
is
 cursor micursor(par1 number) is
	select *
	from(
	 select last_name,salary
	 from hr.employees
	 order by salary desc
	) where rownum<=par1;
begin
 for c in micursor(ptotal) loop
  dbms_output.put_line(c.last_name||' '||c.salary);
 end loop;
end;
/

-- Para ver los errores de compilación:
-- show errors
```

### 29. Procedimiento con Parámetro `OUT`
```sql
create or replace procedure spu_getSumaTotal(ptotal out number)
is
begin
 select sum(i*100) into ptotal from dual connect by level <= 10;
end;
/

declare
 v_total number;
begin
 spu_getSumaTotal(v_total);
 dbms_output.put_line(v_total);
end;
/
```

### 30. Procedimiento con Parámetro `IN OUT`
```sql
create or replace procedure spu_getSumaTotalInOut(ptotal in out number)
is
 suma_calculada number;
begin
 dbms_output.put_line('Valor Inicial = '||ptotal);
 select sum(i*100) into suma_calculada from dual connect by level <= 10;
 ptotal := ptotal + suma_calculada;
end;
/

declare
 v_total number:=10;
begin
 spu_getSumaTotalInOut(v_total);
 dbms_output.put_line('Valor Final = '||v_total);
end;
/
```

### 31. Funciones
```sql
create or replace function getSumar(px number, py number)
return number
is
 rpta number;
begin
 rpta:=px+py;
 return rpta;
end;
/

-- Usos:
select getSumar(9,2) from dual;

begin
 dbms_output.put_line(getSumar(9,2));
end;
/
```

### 33. `BULK COLLECT`
```sql
declare
 cursor micursor is
	select last_name,salary
        from hr.employees e;
 type tlista is table of micursor%rowtype;
 lista tlista:=tlista();
begin
 open micursor;
 fetch micursor bulk collect into lista;
 close micursor;
 for i in 1..lista.count loop
  dbms_output.put_line(lista(i).last_name||' '||lista(i).salary);
 end loop;
end;
/
```

### 34. `BULK COLLECT` con `LIMIT`
```sql
declare
 cursor micursor is
	select last_name,salary
        from hr.employees e;
 type tlista is table of micursor%rowtype;
 lista tlista:=tlista();
begin
 open micursor;
 loop
 	fetch micursor bulk collect into lista limit 10;
    for i in 1..lista.count loop
       dbms_output.put_line(lista(i).last_name||' '||lista(i).salary);
    end loop;
 	exit when lista.count<10; -- O también exit when micursor%notfound;
 end loop;
 close micursor;
end;
/
```

### 35-38. Triggers
```sql
-- Trigger AFTER INSERT para auditoría
create table demo (campo1 number);
create table demo_bk (campo1 number);

create or replace trigger tr_insertar_demo1
after insert on demo
for each row
declare
begin
 insert into demo_bk(campo1) values (:new.campo1);
end;
/

-- Trigger BEFORE INSERT para autogenerar PK con secuencia
create table demo10 (cod number, valor varchar(20));
create sequence seq10 start with 1 increment by 5;

create or replace trigger tr_demo10
before insert on demo10
for each row
declare
begin
 :new.cod:=seq10.nextval;
end;
/

-- Trigger compuesto con predicados INSERTING, DELETING, UPDATING
create table demo12 (campo1 number);

create or replace trigger tr_demo12
before insert or delete or update on demo12						
for each row
declare
begin
 if INSERTING then
  :new.campo1:=:new.campo1*1.1; 
 end if;
 if DELETING then
  -- Códigos de error de aplicación van de -20000 a -20999
  raise_application_error(-20000,'No puedes eliminar lo siento ...');
 end if;
 if UPDATING then
  raise_application_error(-20030,'No puedes actualizar'); 
 end if; 
end;
/
```
---
---

## Ejemplos Adicionales de T-SQL (de `SQLQuery1.sql`)

Estos ejemplos, escritos en T-SQL (SQL Server), complementan los conceptos de PL/SQL con la sintaxis y las características específicas de SQL Server para procedimientos almacenados y triggers.

### Script 58-62: Procedimientos Almacenados Avanzados

Estos scripts cubren temas más avanzados como parámetros `OUTPUT`, valores de retorno, encriptación, procedimientos almacenados anidados y el uso de procedimientos del sistema para obtener metadatos.

```sql
/*Video 58: Parámetros OUTPUT*/
create procedure algo
@edad int,
@sexo varchar(20),
@count int output
as
 set @count = (select count(id_usuario) from usuarios where edad > @edad and sexo = @sexo);
GO

declare @total int;
exec algo 18,'M', @total output;
select @total as 'Total_Hombres_Mayores_18';
GO

/*Video 59: Valores de Retorno*/
create procedure algo2
@edad int,
@sexo varchar(20)
as
if (@edad is null) or (@sexo is null)
	return 0; -- Retorna 0 si los parámetros son nulos
else
	return 1; -- Retorna 1 si son válidos
GO

declare @retorno int;
exec @retorno = algo2 null,null;
select @retorno as 'Rpta';
GO

/*Video 60: Procedimientos del Sistema*/
sp_help; -- Muestra información sobre objetos de la base de datos
sp_helptext copy_m; -- Muestra el texto de una vista o procedimiento no encriptado
sp_stored_procedures algo; -- Lista procedimientos almacenados
sp_depends copy_m; -- Muestra las dependencias de un objeto
GO

/*Video 61: Encriptación de Procedimientos*/
alter proc procedimientoEncriptado
@edad int
with  encryption
as
select * from usuarios where edad>=@edad;
GO

exec procedimientoEncriptado 18;
sp_helptext procedimientoEncriptado; -- Error: El objeto está encriptado
GO

/*Video 62: Procedimientos Anidados*/
create procedure procedimiento1
@resultado int output
as
set @resultado = (select sum (edad) from usuarios);
GO

create procedure procedimiento2
@numuero2 int output
as
begin
 declare @numero int;
 exec procedimiento1 @numero output; -- Llama a otro procedimiento
 set @numuero2 = @numero;
end;
GO

declare @num int;
exec procedimiento2 @num output;
select @num as 'Suma_Total_Edad';
GO
```

### Script 64-65: Triggers

Ejemplos de cómo crear triggers DML (`INSERT`, `UPDATE`) para ejecutar acciones automáticamente cuando los datos de una tabla son modificados.

```sql
/*video 64:trigger*/
create database Tienda;
use Tienda;
create table TablaAlmacen(
id_producto int primary key,
descripcion varchar(20),
cantidad int
);
insert into TablaAlmacen values (1,'aceite',80), (2,'refresco',60), (3,'atun',50), (4,'leche',90);

create table TablaVentas(
id_venta int primary key,
id_producto int,
cantidad int
);
create table TablaTotales(
id_insercion int primary key,
cantidad int
);
insert into TablaTotales values (1, 0); -- Inicializar la tabla de totales
GO

-- Trigger para actualizar el total de ventas en cada inserción
create trigger InsertarVentas
on TablaVentas
for insert
as
begin
	declare @total int;
	set @total = (select sum(cantidad) from TablaVentas);
	update TablaTotales
	set cantidad = @total
    where id_insercion = 1;
end;
GO

insert into TablaVentas values (1,1,20);
insert into TablaVentas values (2,2,10);
select * from TablaTotales; -- Debería mostrar 30
GO

/*Video 65: Trigger de Actualización*/
-- Este trigger parece tener una lógica incorrecta en el original.
-- Un trigger de UPDATE debería usar las tablas 'inserted' y 'deleted'.
-- A continuación, un ejemplo corregido conceptualmente:

create trigger ActualizarVenta
on TablaVentas
for update
as
begin
	declare @total int;
	set @total = (select sum(cantidad) from TablaVentas);
	update TablaTotales
	set cantidad = @total
    where id_insercion = 1;
end;
GO

update TablaVentas set cantidad = 15 where id_venta = 2;
select * from TablaTotales; -- Debería mostrar 35 (20 + 15)
GO
```

---


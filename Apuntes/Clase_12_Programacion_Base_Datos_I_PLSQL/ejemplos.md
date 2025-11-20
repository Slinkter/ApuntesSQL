# Ejemplos - Clase 12: Programación en Base de Datos I: Introducción a PL/SQL

## Ejemplos de Bloques Anónimos, Variables y Control de Flujo (11 de Noviembre de 2013)

Estos ejemplos cubren los fundamentos de la programación en PL/SQL, incluyendo la declaración de variables, el uso de `SELECT INTO`, los atributos `%TYPE` y `%ROWTYPE` para una programación más robusta, y las estructuras de control de flujo como `IF`, `LOOP`, `WHILE` y `FOR`.

### 1. "Hola Mundo" en PL/SQL
```sql
set serveroutput on
begin
 dbms_output.put_line('Hola Mundo');
end;
/
```

### 2. Declaración y Asignación de Variables
```sql
set serveroutput on
declare
 num1 number;
 num2 number;
 rpta number;
begin
 num1:=10;
 num2:=20;
 rpta:=num1+num2;
 dbms_output.put_line('La suma es: '||to_char(rpta));
end;
/
```

### 3. Uso de `SELECT INTO`
```sql
set serveroutput on
declare
 vTotal number;
begin
 select count(*) as total
 into vTotal
 from hr.employees; 
 dbms_output.put_line('El total de empleados es: '||vTotal);
end;
/
```

### 4. `SELECT INTO` con Múltiples Variables
```sql
set serveroutput on
declare
 v_apellido varchar(200);
 v_salario number;
begin
 select last_name, salary
 into v_apellido, v_salario
 from hr.employees
 where employee_id = 195;
 dbms_output.put_line(v_apellido||' '||v_salario);
end;
/
```

### 5. Uso de `%TYPE`
El atributo `%TYPE` permite declarar una variable con el mismo tipo de dato que una columna de una tabla, lo que hace el código más mantenible.
```sql
set serveroutput on
declare
 v_apellido varchar(200);
 v_salario hr.employees.salary%type;
begin
 select last_name, salary
 into v_apellido, v_salario
 from hr.employees
 where employee_id = 195;
 dbms_output.put_line(v_apellido||' '||v_salario);
end;
/
```

### 6. Uso de `%ROWTYPE`
El atributo `%ROWTYPE` permite declarar un registro (record) que tiene la misma estructura que una fila de una tabla.
```sql
set serveroutput on
declare
 v_emp hr.employees%rowtype;
begin
 select *
 into v_emp 
 from hr.employees
 where employee_id = 195;
 dbms_output.put_line(v_emp.last_name);
end;
/
```

### 7. Estructura Condicional `IF-ELSE`
```sql
declare
 vTotal number;
 vAux number:=0;
begin
 select count(*) as total
 into vTotal
 from hr.employees; 
 if (vTotal>100) then
   dbms_output.put_line('Hay mas de 100 empleados');
   vAux:=6;
 else
   dbms_output.put_line('Hay menos de 100 empleados');
 end if;
end;
/
```

### 8. Bucle Básico con `LOOP` y `EXIT WHEN`
```sql
declare
 n number:=0;
begin
 loop
  n:=n+1;   
  dbms_output.put_line(to_char(n));  
  exit when n=20 or n<0;
 end loop;
end;
/
```

### 9. Bucle `WHILE`
```sql
declare
 n number:=0;
begin
 while (n<20) loop
  n:=n+1;   
  dbms_output.put_line(to_char(n));  
 end loop;
end;
/
```

### 10. Bucles Anidados
```sql
declare
 n number:=0;
 j number:=0;
begin
 loop
  n:=n+1;   
  dbms_output.put_line(to_char(n));  
   j:=0;
   while (j<5) loop
    j:=j+1;   
    dbms_output.put_line(to_char(j));  
   end loop;
  exit when n=20 or n<0;
 end loop;
end;
/
```

### 11. Bucle `FOR`
```sql
declare
 v_max number:=10;
begin
 for i in 1..v_max loop
  dbms_output.put_line(to_char(i));   
 end loop;
end;
/
```
---
---

## Ejemplos Adicionales de T-SQL (de `SQLQuery1.sql`)

Estos ejemplos, escritos en T-SQL (SQL Server), muestran conceptos de lógica procedural que son análogos a PL/SQL, como las estructuras de control `CASE` e `IF`, y el uso de variables.

### Script 51: Expresión `CASE`

La expresión `CASE` permite una lógica condicional dentro de una sentencia `SELECT`, similar a un `switch` o una serie de `if-then-else`.

```sql
/*Video 51:Case*/
use empleados;
select id_usuario , nombre , edad_categoria =
case
	when edad <=17 then 'Menor'
	when edad >= 20 then 'Mayor'
    else 'Rango intermedio' -- Añadido para completar la lógica
end
from usuarios;
```

### Script 52: Sentencia `IF...ELSE`

La estructura `IF...ELSE` permite ejecutar bloques de código condicionalmente.

```sql
/*Video 52 : if*/
use empleados;
if exists (select * from usuarios where edad < 18)
	select * from usuarios where edad < 18;
else
	select 'No hay empleados menores de 18 años' as 'Rpta';
```

### Script 53: Declaración y Uso de Variables

Ejemplo de cómo declarar variables, asignarles un valor y usarlas en una consulta.

```sql
/*Video 53: Variable*/
use empleados;
declare @variableSexo varchar(20);
declare @variableEdad int;
set @variableSexo = 'M';
set @variableEdad = 18;

select * from usuarios where sexo = @variableSexo and edad >= @variableEdad;
```
---

### Script 54-57: Creación y Ejecución de Procedimientos Almacenados

Introducción a los procedimientos almacenados, que son bloques de código SQL precompilados y reutilizables. Se muestra cómo crearlos, ejecutarlos, eliminarlos y pasarles parámetros.

```sql
/*Video 54: procedimiento almacenado*/
/*Video 55: Creacion de procedimeinto almacenado*/
-- Procedimiento simple sin parámetros
create procedure Mujeres
as
select nombre,sexo,edad from usuarios where sexo ='F';
GO

-- Ejecutar el procedimiento
exec Mujeres;
GO

-- Procedimiento que realiza una inserción
create procedure insertarChica as
insert into usuarios values (60,'paulina' , 'paul','registrado',20,'F');
GO

/*video 56: Eliminar Procedimientos*/
drop proc insertarChica;
GO

-- Eliminar un procedimiento si existe
if object_id ('Mujeres') is not null
	drop procedure Mujeres;
else
	select 'NO EXISTE';
GO

/*Video 57: Procedimientos con Parámetros de Entrada*/
create procedure selecion
@edad int ,
@sexo varchar(20)
as
select * from usuarios where edad>=@edad and sexo=@sexo;
GO

-- Ejecutar el procedimiento con parámetros
exec selecion 18 ,'F';
```

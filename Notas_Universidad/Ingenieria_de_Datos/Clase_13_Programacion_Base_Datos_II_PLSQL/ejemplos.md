# Ejemplos - Clase 13: Programación en Base de Datos II: Temas Avanzados de PL/SQL

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
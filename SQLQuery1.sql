/*Script 1*/
create database tutorial;
create database prueba;
drop database tutorial;z
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
drop table usuarios
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
select * from usuarios
select * from usuarios where edad >50;
select * from usuarios where edad<40
/*Scrip 4:*/
/*Delete : elimna una fila a mas*/
/*drop : elimna tabla*/
/**truncate: resetear toda la tabla*/
Select * from usuarios where nombre = 'Alex'
insert into usuarios values(10,'alex',23)
select * from usuarios where edad = 23
create table pruebas(
nombre varchar(50) not null,
edad int not null
)

insert into pruebas values('david',11)
insert into pruebas values('manuel',22)
insert into pruebas values('mariana',6)

select * from pruebas
delete from pruebas
delete from usuarios where id_usuarios = 10
select * from usuarios
truncate table pruebas
drop table pruebas
/*Scrip 5*/
select * from usuarios
update usuarios set nombre = 'alex' where id_usuarios = 2
update usuarios set edad =23 where id_usuarios = 1
/*Scrip 6 */
/*Identity*/
create table usuario2
(
id_usuario int identity ,
nombre varchar(50) not null
);
/*Scrip 7*/
insert into usuario2 values('a')
insert into usuario2 values('b')
insert into usuario2 values('c')
insert into usuario2 values('d')
insert into usuario2 values('e')
select * from usuario2;

/*Scrip 8:video 13*/
create database libreria

use libreria

create table libros
(
id_libro int identity primary key,
nombre varchar(50) not null,
precio_venta int not null,
precio_compra float not null
)

insert into libros values('El Lobo',115,95.23);
insert into libros values('Caperucita Roja',236,189.25);
insert into libros values('Programación en Java',78,50.36);
insert into libros values('Programando desde cero con C',115,95.23);
insert into libros values('SQL Server 2000',454,365.56);
insert into libros values('El Codigo Da Vinci',232,199.98);
insert into libros values('Aura',147,112.31);
insert into libros values('100 Años de Soledad',166,124.23);
insert into libros values('La Fisica es Divertida',168,123.32);
insert into libros values('Calculo Integral',456,289.56);
insert into libros values('Las 20 Lenguas del Dragon',345,234.42);
insert into libros values('Narnia',100,89.36);
insert into libros values('El Señor de Los Anillos',157,123.54);
insert into libros values('Ruperth',145,123.21);
insert into libros values('Tutoriales Ankro',457,349.54);
insert into libros values('La Magia de las Matemáticas',456,345.45);
/*****************************************/
/* */
select * from libros
/*Precio de Venta - precio compra*/
select nombre, 10*(precio_venta - precio_compra) as Ganancia_10_libros from libros where id_libro >1;
/*Actualizar*/
update libros set precio_venta = precio_venta + (precio_venta*0.1) where id_libro =1
/*Scrip 9:concatenacion*/
select 'Libros : '+nombre+' ' from libros where id_libro=1
select precio_venta as 'Precio de venta s/.' , precio_compra as 'precio de compra S/.' from libros;
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
insert into libros values ('El Gran Secreto','libro de misterio','Roxana Pilar',254,212);
insert into libros values ('Ladron de sueños','libro de fantasia','Carlos Mantilla',321,231);
insert into libros values ('Programacion en PHP','libro de programación','David Hakro',256,231);
insert into libros values ('Programacion en Java','libro de programación','Tatiana Romero',411,356);
insert into libros values ('El Caracol Feliz','libro infantil','Gael Vega',123,111);
insert into libros values ('Los Misterios del Mar','libro de misterio','Pedro Arturo',232,211);
insert into libros values ('Los Lugares mas Aterradores','libro de terror','Karla Sanchez',453,321);
insert into libros values ('','','',200,145);﻿
select * from libros
select COUNT(*) from libros where precio_compra > 290
select SUM(precio_venta) from libros
select max(precio_venta) from libros
select min(precio_venta) from libros
/*Scrip 11:hola a todos*/
select SUBSTRING('hola a todos ',8,1);
select STR(123)
select STUFF ('cambiando el world',14,5,'mundo')
select len ('cambiando el world')
select CHAR(78)/*codigo asci*/
select lower('MI NOMBRE ES LUIS') AS Algo
select UPPER('     MI NOMBRE ES JHONATAN') AS ALGO
select LTRIM('                    MI NOMBRE ES JHONATAN               ') AS ALGO
select RTRIM('                    MI NOMBRE ES JHONATAN               ') AS ALGO
select REPLACE('HOLA WORLD','WORLD','MUNDO')
select REVERSE('anita la tina')
select PATINDEX('%luis%','donde esta luis?')
select REPLICATE('Hola ',10)
select 'luis ' + SPACE(8) + ' jhonatan'
/*Scrip 12: FECHAS*/
select GETDATE()
select DATEPART(year,GETDATE())
select DATEPART(MONTH,GETDATE())
select DATEPART(DAY,GETDATE())
select DATENAME(MONTH,GETDATE())
select DATEDIFF(day,'2014/01/03','2017/04/03')
select DATEDIFF(MONTH,'2014/01/03','2017/04/03')
select DATEDIFF(YEAR,'2014/01/03','2017/04/03')
select YEAR(GETDATE())
/*Scrip 13: Order by*/
use libreria2
select  * from libros order by precio_venta desc
/*Scrip 14: Operadores Negativos*/
/*
         | not | and | or |
*/
select * from libros where not titulo = 'Ladron de sueños'
select * from libros where not autor ='Karla Sanchez' and not titulo = 'Ladron de sueños'
select * from libros order by precio_compra asc
select * from libros where precio_compra < 120
select * from libros where precio_venta = 128 or precio_venta < 245
/*Scrip 15: */
create database libreria3;
use libreria3;
create table libros(
id_libro int identity primary key,
nombre varchar(50) not null,
precio_venta float not null,
precio_compra float not null
)
/*Eliminar columna */
alter table libros drop column nombre ;
alter table libros drop column precio_venta;
alter table libros drop column precio_compra;
/*Agregar columna */
alter table libros add nombre varchar(50);
alter table libros add precio_venta float  not null;
alter table libros add precio_compra float not null;

select * from libros;

insert into libros values ('el lobo',115.00,95.23);
insert into libros values ('caperusa roja',256,189.25);
insert into libros values ('programacion en java',123,101.56);
insert into libros values ('programacion desde cero con C',78,50.30);
insert into libros values ('sql server 2000',456,369.56);
insert into libros values ('el codigo de vinci',232,199.99);
insert into libros values ('auro',147,112.31);
insert into libros values ('100 años de soleda',166,124.23);
insert into libros values ('la fisica es divertida',168,123.23);
insert into libros values ('calculo integral',168,124.36);
insert into libros values (null,365,236.42);
insert into libros values ('narnia',100,89.36);
insert into libros values ('el señor de los anillos',157,123.26);
insert into libros values (null,155,123.21);
insert into libros values ('tutoriales overone',457,369.54);
insert into libros values ('la magia de las matematicas',456,345.55);

select * from libros where nombre is not null
select * from libros where not nombre is null
select * from libros where precio_venta > 200 and  precio_venta < 300
select * from libros where precio_venta between 200 and 300
/*Scrip 15*: Usando Like */
/*
      | not like | like |
*/
use libreria3
select * from libros
select * from libros where nombre like '%100%';
select * from libros where nombre not like '%el%'
select * from libros where nombre = 'narnia'
select * from libros where nombre like 'narnia'
select * from libros where nombre not like 'narnia'
select * from libros where nombre like 'nar%'/* buscar palabras que comienza nar....*/
select * from libros where nombre like '%nia'/* buscar palabras que terminan ....nia*/
select * from libros where nombre not like 'nar%'
select * from libros where nombre not like '%nia'
select * from libros where nombre like '%la magia de las matematicas%'
select * from libros where nombre like '%la ma_ia de las m_tem_ticas%'
/*Scrip 16: */
select * from libros
select COUNT(nombre) as 'Cantidad de libros' from libros where id_libro>10
select nombre as 'Cantidad de libros' from libros where id_libro>10 /*no cuenta los null*/
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
)
select *  from usuarios
insert into usuarios values('david','dav26','sdddd','registrado',22,'M');
insert into usuarios values('janeth','jan71','3e2d','registrado',23,'F');
insert into usuarios values('fany','fan22','sdcaed34','registrado',22,'F');
insert into usuarios values('ashley','ash77','34r4d','registrado',18,'F');
insert into usuarios values('karen','kar11','efaccwe','registrado',21,'F');
insert into usuarios values('manuel','man99','dsar4','registrado',25,'M');
insert into usuarios values('miguel','mig54','axcewf','registrado',21,'M');
insert into usuarios values('cinthia','cin23','efa4x','registrado',19,'F');
insert into usuarios values('jose','jos85','4rv4f','registrado',18,'M');
insert into usuarios values('carlos','car26','4tvavg','admin',17,'M');
insert into usuarios values('pedro','ped35','ujgn','registrado',22,'M');
insert into usuarios values('jorge','jor62','ev5<4','registrado',19,'M');
insert into usuarios values('julio','jul45','67B5','registrado',22,'M');
insert into usuarios values('paola','pao22','5BY67ED5','registrado',21,'F');
insert into usuarios values('carmen','car65','BYTBUJ8','admin',21,'F');
insert into usuarios values('rocio','roc25','RSGE','registrado',21,'F');
insert into usuarios values('edgar','edg35','tbrytb','registrado',25,'M');
insert into usuarios values('yared','yar52','u7tyr','admin',26,'F');
insert into usuarios values('nancy','nan26','yuftuj','registrado',21,'F');
insert into usuarios values('karla','kar47','uenyud','registrado',22,'F');
insert into usuarios values('ivonne','ivo48','ydnut','registrado',22,'F');
insert into usuarios values('celina','cel24','dynubuyt','registrado',23,'F');
insert into usuarios values('carlos','car11','yun9s','registrado',22,'M');
insert into usuarios values('guillermo','gui67','werty','registrado',20,'M');
insert into usuarios values('cynthia','cyn22','rt6rtdg','registrado',18,'F');
insert into usuarios values('ivette','ive78','rgtv6d','registrado',17,'F');
insert into usuarios values('julio','jul24','9ort65y','super_admin',22,'M');
insert into usuarios values('annie','ann34','x<dc5t','registrado',20,'F');
insert into usuarios values('david','dav12','5ty6bh6','registrado',20,'M');
insert into usuarios values('tatiana','tat46','6byh5bdv','registrado',21,'F');
insert into usuarios values('carola','car23','hmnjft','registrado',23,'F');
insert into usuarios values('jesus','jes11','gdct','registrado',25,'M');
insert into usuarios values('david','dav22','ef5v5','super_admin',25,'M');
/*count sum avg: operadorea de agrupamiento*/
use empleados;
select count(*) as 'Numero de usuarios' from usuarios /*no cuenta nulls*/
select sum(edad) as 'La suma de edad  de usuarios' from usuarios
select AVG(edad) as 'El promedio de edad de usuarios' from usuarios
select avg(edad) from usuarios where sexo = 'M' and edad<18/*sumar las edad de los hombre*/
select avg(edad) from usuarios where sexo = 'F' and edad<18
select * from usuarios order by edad asc
/*max min */
select min(edad) as 'Edad minima' from usuarios;
select max(edad) as 'Edad maxima' from usuarios;
select min(nombre) from usuarios
select max(nombre) from usuarios
/*Scrip 18:Having necesita operadores de agrupamiento*/
select nombre,AVG(edad) from usuarios where sexo ='f'
group by nombre
having avg(edad)>20
/*Scrip 19: compute*/
select nombre,edad from usuarios where sexo='f'
select min(edad) from usuarios where sexo='f'

select nombre, edad from usuarios where sexo = 'f' compute min(nombre),sum(edad)/*No funciona en 2016 .. creo si en 2008*/
/*Scrip 20 : Distintic*/
select * from usuarios
select distinct nombre from usuarios order by nombre;
select edad from usuarios order by edad;
select distinct edad from usuarios order by edad;
select sum(distinct edad) from usuarios
/*Scrip 21 : top*/
select top 10 * from usuarios
select top 10 * from usuarios  order by id_usuario desc
/*Scrip 22 : Backup*/
/*Averiguar para sql server 2016*/
/*Script 22 : inner Join*/
create database escuela
use escuela

CREATE TABLE CARRERA (
ID_CARRERA INT PRIMARY KEY NOT NULL,
CARRERA VARCHAR(20) NOT NULL
);
CREATE TABLE ALUMNO(
ID_ALUMNO INT PRIMARY KEY NOT NULL,
NOMBRE VARCHAR(20)NOT NULL,
APELLIDOS VARCHAR(20)NOT NULL,
ID_CARRERA INT NOT NULL,
FOREIGN KEY (ID_CARRERA) REFERENCES CARRERA(ID_CARRERA)
);

CREATE table datos (
ID_DATOS INT  PRIMARY KEY NOT NULL,
ID_ALUMNO INT NOT NULL,
EMAIL VARCHAR(20)NOT NULL,
EDAD int NOT NULL,
FOREIGN KEY (ID_ALUMNO) REFERENCES ALUMNO(ID_ALUMNO)
);

INSERT INTO CARRERA VALUES(1,'ING.SISTEMAS');
INSERT INTO CARRERA VALUES(2,'LIC.DERECHO');
INSERT INTO CARRERA VALUES(3,'LIC.ADMINISTRACION');

INSERT INTO ALUMNO VALUES(1,'DAVID','HERNANDEZ PEREZ',1);
INSERT INTO ALUMNO VALUES(2,'MARIANA','MARTINEZ LUNA',2);
INSERT INTO ALUMNO VALUES(3,'TATIANA','RAMIREZ RAMIREZ',1);
INSERT INTO ALUMNO VALUES(4,'JUAN','ARCILA CAMPAZ',3);

INSERT INTO DATOS VALUES(1,1,'HACKRO@YAHOO.COM',22);
INSERT INTO DATOS VALUES(2,2,'MARIANA',14);
INSERT INTO DATOS VALUES(3,3,'TATIANA',21);
INSERT INTO DATOS VALUES(4,4,'JUANDAVIDARCILA18@',21);

use escuela


select * from datos;
select * from alumno;
select * from carrera ;
/*Inner Join */
select ALUMNO.NOMBRE, ALUMNO.APELLIDOS , datos.EDAD,datos.EMAIL from datos inner join alumno on  datos.ID_ALUMNO = alumno.ID_ALUMNO inner join carrera on alumno.ID_CARRERA = carrera.ID_CARRERA where carrera.ID_CARRERA = 1;
/*Inner join left*/
select * from datos inner join ALUMNO on datos.ID_ALUMNO = alumno.ID_ALUMNO;
select * from alumno left join datos on alumno.ID_ALUMNO = datos.ID_ALUMNO;
select * from datos right join alumno on alumno.ID_ALUMNO = datos.ID_ALUMNO;
select * from datos right join ALUMNO on datos.ID_ALUMNO = ALUMNO.ID_ALUMNO;
/*Script*/
/*Group by*/
select  alumno.nombre,carrera.carrera from datos inner join alumno
on datos.id_alumno = alumno.id_alumno  inner join carrera
on carrera.ID_CARRERA= alumno.ID_CARRERA where edad>18 group by  alumno.nombre,carrera.carrera ;
/*Script*/
/*Update with inner join*/
select * from alumno inner join carrera
on alumno.id_carrera = carrera.id_carrera;

update alumno set nombre='TI'
from alumno inner join carrera
on alumno.id_carrera = carrera.id_carrera
where carrera.ID_CARRERA = 1;

delete alumno
from alumno inner join carrera
on alumno.id_carrera = carrera.id_carrera
where carrera.id_carrera=1;
/*Script */
select * from carrera ;
alter table carrera
add cupo_limitado int;

alter table carrera
drop column cupo_limitado;
/*Script*/
select  * from carrera;
alter table carrera
add cupo_minimo int;
alter table carrera
add cupo_limitado int;

alter table carrera
add resta as (cupo_minimo +100);

alter table carrera
add suma as (cupo_limitado -100);

/*Script */
/*

*/
create database Libreria4;
use Libreria4;
create table libros
(
id_libro int primary key,
titulo varchar(50),
num_pag int
)

insert into libros values (1,'100 años de soledad',789);
insert into libros values (2,'Saco de hueso',495);
insert into libros values (3,'Anu',3457);
insert into libros values (4,'Made in china',125);
insert into libros values (5,'Guerra y paz',998);
insert into libros values (6,'Estter',665);


select * from libros;
update libros set titulo ='ana Karenina'
from libros where id_libro = 3;

update libros set titulo = 'madame bovary'
from libros where id_libro = 4;

update libros set titulo = 'jugadores'
from libros where id_libro = 6
/*Script */
select * from libros where id_libro = (select id_libro from libros where titulo = 'jugadores');
select * from libros where id_libro in (2,4,6) /*Escoger por id */
select * from libros where id_libro not in (2,4,6)/*Excepcion a 2 4 6*/
select * from libros where id_libro not in (select id_libro from libros where num_pag>1000);
/*Script
in : = any
not in : <> all
 */
use empleados
select * from usuarios;
select * from usuarios where sexo ='F' and edad = any(select edad from usuarios where sexo='M')
select * from usuarios where sexo = 'F' and edad <> all (select edad from usuarios where sexo='M')
/*Script*/
update usuarios set tipo_usuario = 'root'
where id_usuario = any (select id_usuario from usuarios where edad > 24);
select * from usuarios;
select * from usuarios order by edad desc

delete usuarios
where tipo_usuario =
any (select id_usuario from usuarios where edad > 24)
/*Script */
create table nombres
(
nombre varchar(50)
)

insert into nombres (nombre)
select (nombre) from usuarios;

select * from nombres;
/*Script : Video 45 :Vista*/
use empleados/* La base de datos */
select * from usuarios /*La tabla de DB*/
use empleados
create view usuarios_view as select nombre, edad from usuarios;

select count(nombre) as 'Cantidad de usuarios' from usuarios_view
/*Video 46 : Cifrado de vista-Seguridad*/
select * from
sp_helptext usuarios_view

create view usuarios_view2 with encryption as select nombre,edad from usuarios;
select * from usuarios_view2;
sp_helptext usuarios_view2;
/*Video 47 :*/
drop table usuarios;
drop view usuarios_view,usuarios_view2
/*Video 48 :*/
select * from usuarios order by edad asc
create view Mujeres as select * from usuarios where sexo='F'
select * from Mujeres order by edad asc
update Mujeres set tipo_usuario ='SuperUsuario'
where edad>25
delete from Mujeres

/*Video 49 :*/
create database empleados
use empleados;


create table usuarios
(
id_usuario int identity primary key,
nombre varchar(30)not null,
usuario varchar(30)not null,
contrasena varchar(30)not null,
tipo_usuario varchar(10) not null,
edad int not null,
sexo varchar(20) not null
)
insert into usuarios values('david','dav26','sdddd','registrado',22,'M');
insert into usuarios values('janeth','jan71','3e2d','registrado',23,'F');
insert into usuarios values('fany','fan22','sdcaed34','registrado',22,'F');
insert into usuarios values('ashley','ash77','34r4d','registrado',18,'F');
insert into usuarios values('karen','kar11','efaccwe','registrado',21,'F');
insert into usuarios values('manuel','man99','dsar4','registrado',25,'M');
insert into usuarios values('miguel','mig54','axcewf','registrado',21,'M');
insert into usuarios values('cinthia','cin23','efa4x','registrado',19,'F');
insert into usuarios values('jose','jos85','4rv4f','registrado',18,'M');
insert into usuarios values('carlos','car26','4tvavg','admin',17,'M');
insert into usuarios values('pedro','ped35','ujgn','registrado',22,'M');
insert into usuarios values('jorge','jor62','ev5<4','registrado',19,'M');
insert into usuarios values('julio','jul45','67B5','registrado',22,'M');
insert into usuarios values('paola','pao22','5BY67ED5','registrado',21,'F');
insert into usuarios values('carmen','car65','BYTBUJ8','admin',21,'F');
insert into usuarios values('rocio','roc25','RSGE','registrado',21,'F');
insert into usuarios values('edgar','edg35','tbrytb','registrado',25,'M');
insert into usuarios values('yared','yar52','u7tyr','admin',26,'F');
insert into usuarios values('nancy','nan26','yuftuj','registrado',21,'F');
insert into usuarios values('karla','kar47','uenyud','registrado',22,'F');
insert into usuarios values('ivonne','ivo48','ydnut','registrado',22,'F');
insert into usuarios values('celina','cel24','dynubuyt','registrado',23,'F');
insert into usuarios values('carlos','car11','yun9s','registrado',22,'M');
insert into usuarios values('guillermo','gui67','werty','registrado',20,'M');
insert into usuarios values('cynthia','cyn22','rt6rtdg','registrado',18,'F');
insert into usuarios values('ivette','ive78','rgtv6d','registrado',17,'F');
insert into usuarios values('julio','jul24','9ort65y','super_admin',22,'M');
insert into usuarios values('annie','ann34','x<dc5t','registrado',20,'F');
insert into usuarios values('david','dav12','5ty6bh6','registrado',20,'M');
insert into usuarios values('tatiana','tat46','6byh5bdv','registrado',21,'F');
insert into usuarios values('carola','car23','hmnjft','registrado',23,'F');
insert into usuarios values('jesus','jes11','gdct','registrado',25,'M');
insert into usuarios values('david','dav22','ef5v5','super_admin',24,'M');

select * from usuarios
create view copy_m as select * from usuarios where sexo ='M' with check option;
select * from copy_m
drop view copy_m
select * from copy_m
delete from copy_m
/*Video 50 :*/
/*Video 51:Case*/
use empleados
select * from usuarios;
select id_usuario , nombre , edad =
case
	when edad <=17 then 'Menor'
	when edad >= 20 then 'Mayor'
end
from usuarios;
/*Video 52 : if*/
select * from usuarios
if exists (select * from usuarios where edad <18)
	select * from usuarios where edad <18
else
	select 'No hay empleados de 8 años'as 'Rpta'

/*Video 53: Variable*/
use empleados
select * from usuarios
declare @variableSexo varchar(20)
declare @variableEdad int
set @variableSexo = 'M'
set @variableEdad = 18
select * from usuarios where sexo = @variableSexo and edad>= @variableEdad
/*Video 54: procedimiento almacenado*/
/*Video 55: Creacion de procedimeinto almacenado*/
create procedure Mujeres
as
select nombre,sexo,edad from usuarios where sexo ='F'
exec Mujeres

create procedure insertarChica as
insert into usuarios values (60,'paulina' , 'paul','registrado',20,'F')

/*video 56*/
drop proc insertarChica
if object_id (Mujeres) is not nul
	drop procedure Mujeres
else
	select 'NO EXISTE'

/*Video 57*/
create procedure selecion
@edad int ,
@sexo varchar(20)
as
select * from usuarios where edad>=@edad and sexo=@sexo;
exec selecion 18 ,'F'
/*Video 58:*/
create procedure algo
@edad int,
@sexo varchar(20),
@count int output
as
 set @count = (select count(id_usuario) from usuarios where edad > @edad and sexo = @sexo)

declare @total int
exec algo 18,'M',@total output
select @total
/*Video 59*/
create procedure algo2
@edad int,
@sexo varchar(20)
as
if (@edad is null) or (@sexo is null)
	return 0
else
	return 1

declare @retorno int
exec @retorno = algo2 null,null
select @retorno as 'Rpta'

/*Video 60*/
use empleados
sp_help
sp_helptext copy_m
sp_stored_procedures algo
sp_depends copy_m
select * from sysobjects order by id
/*Video 61*/
/*Sin encriptacion*/
create proc procedimientoEncriptado
@edad int
as
select * from usuarios where edad>=@edad

exec procedimientoEncriptado 18
sp_helptext procedimientoEncriptado
/*con encriptacion*/
alter proc procedimientoEncriptado
@edad int
with  encryption
as
select * from usuarios where edad>=@edad

exec procedimientoEncriptado 18
sp_helptext procedimientoEncriptado
/*Video 62*/
create procedure procedimiento1
@resultado int output
as
set @resultado = (select sum (edad) from usuarios)

create procedure procedimiento2
@numuero2 int output
as
begin
declare @numero int
	exec procedimiento1 @numero output
	set @numuero2 = @numero
end
--Mostrar datos
declare @num int --declaro una variable
exec procedimiento2 @num output -- paso la variablde salidad
select @num --imprimir el valore
/*video 63*/
/*video 64:trigger*/
create database Tienda
use Tienda
create table TablaAlmacen(
id_producto int primary key,
descripcion varchar(20),
cantidad int
)
insert into TablaAlmacen values (1,'aceite',80)
insert into TablaAlmacen values (2,'refresco',60)
insert into TablaAlmacen values (3,'atun',50)
insert into TablaAlmacen values (4,'leche',90)
select * from TablaAlmacen

create table TablaVentas(
id_venta int primary key,
id_producto int,
cantidad int
)
insert into TablaVentas values (1,1,20)
insert into TablaVentas values (2,1,20)
insert into TablaVentas values (3,2,3)
insert into TablaVentas values (4,2,20)
select * from TablaVentas

create table TablaTotales(
id_insercion int primary key,
cantidad int
)
insert into TablaTotales values (4,63)


create trigger InsertarVentas
on TablaVentas
for insert
as
begin
	declare @total int
	set @total = (select sum(cantidad) from TablaVentas)
	update TablaTotales
	set TablaTotales.cantidad = @total
end
select * from TablaVentas
select * from TablaTotales
insert into TablaVentas values (7,2,10)

/*Video 65*/
select * from TablaAlmacen
select * from TablaVentas join TablaAlmacen
on TablaVentas.id_producto = TablaAlmacen.id_producto

--Creacion trigger--
create trigger ActualizarVenta --Asignamos un nombre al trigger
on TablaVentas --Indicamos la tabla donde se activara la accion
for update --Despues de insertar en la TablaVentas
as
	begin --Comienza las sentencias
		declare @total int --Declaramos una variable int
			set @total = (select sum(cantidad) from TablaVentas) --obtenemos la suma de las cantidades y lo asignamos a la variable
				insert into TablaTotales values(1)
	end

--Comprobamos los valores ingresados
	select * from TablaVentas
	select * from TablaTotales

--Actualizar un registro
update TablaVentas
set cantidad = 20
where TablaVentas.id_venta = 3

/*Video 66*/
/* Febrero del 2018*/
/*Video 67*/

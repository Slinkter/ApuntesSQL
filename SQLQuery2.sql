--Curso de SQL Server --
--Data Manipulation Language (DML): modifica a los datos
--	*select
--  *insert
--  *update
--  *delete
--Data Definittion Languaje(DDL): define objeto
--  *Create
--  *Alter
--  *Drop
--Data Control Languaje(DCL):Son permisos
--  *Grant
--  *Revoke
--  *Deny
--                                              --
/*Example*/

select 'Hola Mundo'
select getdate()--imprimir la fecha de la computadora

use Northwind
--Definir una variable
Declare @variable1 varchar(100)
Set @variable1 = 'SQl Server'
select @variable1/*Es necesario usar las 3 lineas*/
--Consultado una tabla
Select * from Customers
Select companyname,contactname from Customers
--variable de sistema
select @@ERROR
--Concadenar
select companyname+ ' ' + contactname from Customers
--operaciones basicas
select * from Products
select productname , unitprice , unitsInStock from Products
select productname , unitprice , unitsInStock , (unitprice*unitsInStock) as 'Total' from Products
/*
1.Select
2.from
3.where : filta antes de grupar
4.group by : Categoria
5.having :
6.orden by
*/
--Instruccion select : no utilizar en una base de datos de producci�n.
select * from Customers
where Country = 'France' or Country = 'Canada' --no usar "and "
order by Country
--Instruccion select con Group by
select country ,companyname from Customers
where country like 'A%'
--
select country ,count(companyname) as 'Acumulado' from Customers
where country like 'A%'
group by country-- obligado a contar
--
select country ,count(companyname) as 'Acumulado' from Customers
where country like 'A%'
group by country-- obligado a contar
having count(companyname)>2
-- Filtrar formando predicado -- Between
select productname,unitprice from Products
where UnitPrice between 25 and 30
-- Filtrar formando predicado -- In
select companyname,contactname,country from customers
where country in('USA','Canada','Mexico') -- where country ='USA' or country ='Canada' or country ='Mexico'
-- Filtrar formando predicado -- like
select companyname,contactname,country from customers
where CompanyName like '[A-C]%' -- 'A%' : Rango de A a C
--
select companyname,contactname,country from customers
where CompanyName not like '[A-C]%' -- : Rango de D a Z [^A-C]%
-- Filtrar DISCTINCT-- Eliminar duplicado
select country from customers order by Country
select Distinct country from customers order by Country
--xml--
select companyname,contactname,country  from Customers
for xml auto p
--
select companyname,contactname,country  from Customers
for xml path
--
select companyname,contactname,country  from Customers
for xml raw
--Filtrar Uso Case
select productname,unitprice,
	case categoryid
		when 1 then 'producto 1'
		when 2 then 'producto 2'
		when 3 then 'producto 3'
		else 'Otros'
	end as 'Producto'
from Products

/* Febrero del 2018*/

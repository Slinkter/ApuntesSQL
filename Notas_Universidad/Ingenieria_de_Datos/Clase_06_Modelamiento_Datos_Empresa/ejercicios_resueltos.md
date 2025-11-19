# Ejercicios Resueltos - Clase 06: Modelamiento de Datos en la Empresa

## Ejercicio de Examen Parcial: Diseño de Esquema de Museo (parcial-2013-1.sql)

Este script SQL representa un ejercicio práctico de diseño de base de datos para un sistema de gestión de obras de arte, probablemente como parte de un examen parcial. El ejercicio consiste en crear un esquema relacional completo, incluyendo tablas para obras, autores, museos, préstamos, etc. Se aplican una variedad de restricciones para asegurar la integridad de los datos, como claves primarias, claves foráneas, restricciones de unicidad y de verificación.

El script también incluye comentarios y preguntas del estudiante, lo que lo convierte en un excelente ejemplo de un caso de estudio real sobre cómo se aplica la teoría del modelamiento de datos en la práctica.

### Script SQL

```sql
-- ==================== CREACIÓN DE TABLAS ===================
create table OBRA
(
codigo number,
nombre varchar(20),
tipo char(1)
fech_creacion date,
fech_entrega date,
valoracion number,
codAutor number,
codEstilo number,
codPeriodo number
);

create table PERIODO
(
codigo number,
descripcion varchar(20)
);

create table ESTILO
(
codigo number,
descripcion varchar(20)
);

create table AUTOR
(
codigo number,
nombre varchar(20)
);

create table OBRA_AUTOR
(
codAutor number,
codObra number,
tipoAutor char(1)
);

create table MATERIAL
(
codigo number,
descripcion varchar(20)
);

create table TECNICA
(
codigo number,
descripcion varchar(20)
);

create table ESCULTURA
(
codObra number,
codMaterial number,
codEstilo number
);

create table CUADRO
(
codObra number,
codTecnica number,
codEstilo number
);

create table MUSEO_ASOCIADO
(
codigo number,
nombre varchar(10),
direccion varchar(20),
fech_asociado varchar(20)
);

create table SOLICITUD_PRESTAMO
(
codigo number,
fech_solicitud varchar(20),
fech_prestamo varchar(20),
numOrden number,
codMuseo number,
codObra number,
estado char(1),
);

create table PRESTAMO
(
codigo number,
codObra number,
codMuseo number,
importe number(6.2)
);

-- ==================== RESTRICCIÓN NOT NULL ===================

alter table OBRA modify nombre not null;
alter table AUTOR modify nombre not null;

-- Pregunta 1: ¿debo colocar not null, por ser una regla de negocio?
-- RPTA: Si la descripción es fundamental para la entidad, sí. Si no hay descripción, la tabla solo almacena un PK y no tendría mucho sentido.
alter table PERIODO modify descripcion not null; 

-- Pregunta 2: ¿por ser una regla de negocio?
-- RPTA: Igual que la anterior, si es un atributo esencial para la entidad.
alter table ESTILO modify descripcion not null; -- Error de sintaxis, debería ser "modify descripcion not null"

-- Corrección del error de sintaxis en MUSEO_ASOCIADO
alter table MUSEO_ASOCIADO modify nombre not null;

-- ==================== CLAVES PRIMARIAS (PK) ===================

alter table PERIODO add constraint PK_PERIODO primary key(codigo);
alter table OBRA add constraint PK_OBRA primary key (codigo);
alter table AUTOR add constraint PK_AUTOR primary key(codigo);
alter table OBRA_AUTOR add constraint PK_OBRA_AUTOR primary key(codObra,codAutor);
alter table MATERIAL add constraint PK_MATERIAL primary key (codigo);
alter table TECNICA add constraint PK_TECNICA primary key (codigo); -- Error de sintaxis, debería ser "add constraint"
alter table ESTILO add constraint PK_ESTILO primary key (codigo);
alter table ESCULTURA add constraint PK_ESCULTURA primary key (codObra);
alter table CUADRO add constraint PK_CUADRO primary key (codObra);
alter table MUSEO_ASOCIADO add constraint PK_MUSEO_ASOCIADO primary key (codigo);
alter table SOLICITUD_PRESTAMO add constraint PK_SOLICITUD primary key (codigo); -- El nombre de la tabla es SOLICITUD_PRESTAMO, no SOLICITUD
alter table PRESTAMO add constraint PK_PRESTAMO primary key (codigo);

-- ==================== CLAVES FORÁNEAS (FK) ===================

alter table OBRA add constraint FK_OBRA_PERIODO foreign key(codPeriodo) references PERIODO(codigo);
alter table OBRA add constraint FK_OBRA_AUTOR foreign key(codAutor) references AUTOR(codigo);
alter table OBRA add constraint FK_OBRA_ESTILO foreign key(codEstilo) references ESTILO(codigo);

-- Pregunta 3: ¿es correcto esto: FK_OBRA_AUTOR_OBRA?
-- RPTA: El nombre es válido y descriptivo, sí.
alter table OBRA_AUTOR add constraint FK_OBRA_AUTOR_OBRA foreign key (codObra) references OBRA(codigo); 

-- Pregunta 4: ¿es correcto esto: FK_OBRA_AUTOR_AUTOR?
-- RPTA: El nombre es válido y descriptivo, sí.
alter table OBRA_AUTOR add constraint FK_OBRA_AUTOR_AUTOR foreign key (codAutor) references AUTOR(codigo); 

alter table ESCULTURA add constraint FK_ESCULTURA_OBRA foreign key(codObra) references OBRA(codigo);
alter table ESCULTURA add constraint FK_ESCULTURA_MATERIAL foreign key(codMaterial) references MATERIAL(codigo);
alter table ESCULTURA add constraint FK_ESCULTURA_ESTILO foreign key(codEstilo) references ESTILO(codigo);
alter table CUADRO add constraint FK_CUADRO_OBRA foreign key (codObra) references OBRA(codigo);
alter table CUADRO add constraint FK_CUADRO_TECNICA foreign key (codTecnica) references TECNICA (codigo);
alter table CUADRO add constraint FK_CUADRO_ESTILO foreign key(codEstilo) references ESTILO(codigo);
alter table PRESTAMO add constraint FK_PRESTAMO_OBRA foreign key(codObra) references OBRA(codigo);
alter table PRESTAMO add constraint FK_PRESTAMO_MUSEO_ASOCIADO foreign key(codMuseo) references MUSEO_ASOCIADO(codigo);
alter table SOLICITUD_PRESTAMO add constraint FK_SOLICITUD_PRESTAMO_OBRA foreign key(codObra) references OBRA(codigo);
alter table SOLICITUD_PRESTAMO add constraint FK_SOLICITUD_PRESTAMO_MUSEO_ASOCIADO foreign key(codMuseo) references MUSEO_ASOCIADO(codigo);

-- ==================== RESTRICCIÓN UNIQUE (UQ) ===================

alter table OBRA add constraint UQ_OBRA unique(nombre);
alter table AUTOR add constraint UQ_AUTOR unique (nombre);
alter table MUSEO_ASOCIADO add constraint UQ_MUSEO_ASOCIADO unique (nombre);

-- ==================== RESTRICCIONES CHECK (CC) ===================

alter table OBRA add constraint CC_OBRA_TIPO check(tipo in ('E','C','O','e','c','o'));
alter table OBRA_AUTOR add constraint CC_OBRA_AUTOR_TIPOAUTOR check(tipoAutor in ('A','C','a','c')); -- Error de sintaxis, 'c' suelto
alter table SOLICITUD_PRESTAMO add constraint CC_SOLICITUD_PRESTAMO_ESTADO check(estado in ('D','N','d','n'));
alter table OBRA add constraint CC_OBRA_VALORACION check(valoracion>=0);
alter table PRESTAMO add constraint CC_PRESTAMO_IMPORTE check(importe>=0);

-- ==================== CARDINALIDAD (Obligatoriedad de FKs) ===================

alter table OBRA modify codAutor not null;
alter table OBRA_AUTOR modify codAutor not null; -- Error de lógica, debería ser codAutor en OBRA, no en OBRA_AUTOR.

-- ==================== VALOR POR DEFECTO (DEFAULT) ===================

alter table SOLICITUD_PRESTAMO modify estado default 'D';
alter table OBRA modify tipo default 'O';

-- ==================== FKs ADICIONALES (con preguntas del estudiante) ===================

-- Pregunta: ¿se tenía que agregar los FKs en la tabla OBRA?
-- alter table OBRA add codSolicitud number;
-- alter table OBRA add codPrestamo number;

-- RPTA: No, Cuando hay una relacion de 1 a muchos, la tabla que tiene el "muchos" recibe el PK de la otra tabla (la tabla "uno").
-- Es más, la foto (del modelo) Indica: Tabla SolicitudPrestamos tiene codObra, entonces se debe hacer un FK del campo codObra de la tabla Solicitud_Prestamo hacia el PK de la tabla Obra.
-- Sería:
-- alter table PRESTAMO add constraint FK_PRESTAMO_OBRA foreign key(codObra) references OBRA(codigo);
-- Y como necesito que sí o sí se registre la obra (no tiene sentido que se inserte NULL)
-- alter table PRESTAMO modify codObra not null;

```
---

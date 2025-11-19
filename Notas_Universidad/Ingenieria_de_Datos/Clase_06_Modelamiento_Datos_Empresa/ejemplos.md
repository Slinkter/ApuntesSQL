# Ejemplos - Clase 06: Modelamiento de Datos para la Empresa

## Caso Práctico: Diseño de Base de Datos para un Museo (Examen Parcial 2013-1)

Este script SQL es un caso práctico completo de modelamiento de datos para un museo o una colección de arte. Cubre la creación de tablas, la definición de claves primarias y foráneas, y la implementación de restricciones de negocio a través de `UNIQUE`, `CHECK`, `NOT NULL` y `DEFAULT`. Es un excelente ejemplo de cómo traducir un modelo conceptual a un esquema de base de datos físico.

```sql
create table OBRA
(
codigo number,
nombre varchar(20),
tipo char(1),
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
estado char(1)
);

create table PRESTAMO
(
codigo number,
codObra number,
codMuseo number,
importe number(6.2)
);

-- ==================== RESTRICCIONES NOT NULL ===================
alter table OBRA modify nombre not null;
alter table AUTOR modify nombre not null;
alter table PERIODO modify descripcion not null;
alter table ESTILO modify descripcion not null;
alter table MUSEO_ASOCIADO modify nombre not null;

-- ==================== CLAVES PRIMARIAS (PK) ===================
alter table PERIODO add constraint PK_PERIODO primary key(codigo);
alter table OBRA add constraint PK_OBRA primary key (codigo);
alter table AUTOR add constraint PK_AUTOR primary key(codigo);
alter table OBRA_AUTOR add constraint PK_OBRA_AUTOR primary key(codObra,codAutor);
alter table MATERIAL add constraint PK_MATERIAL primary key (codigo);
alter table TECNICA add constraint PK_TECNICA primary key (codigo);
alter table ESTILO add constraint PK_ESTILO primary key (codigo);
alter table ESCULTURA add constraint PK_ESCULTURA primary key (codObra);
alter table CUADRO add constraint PK_CUADRO primary key (codObra);
alter table MUSEO_ASOCIADO add constraint PK_MUSEO_ASOCIADO primary key (codigo);
-- alter table SOLICITUD add constraint PK_SOLICITUD primary key (codigo); -- Asumiendo que es SOLICITUD_PRESTAMO
alter table SOLICITUD_PRESTAMO add constraint PK_SOLICITUD primary key (codigo);
alter table PRESTAMO add constraint PK_PRESTAMO primary key (codigo);

-- ==================== CLAVES FORÁNEAS (FK) ===================
alter table OBRA add constraint FK_OBRA_PERIODO foreign key(codPeriodo) references PERIODO(codigo);
alter table OBRA add constraint FK_OBRA_AUTOR foreign key(codAutor) references AUTOR(codigo);
alter table OBRA add constraint FK_OBRA_ESTILO foreign key(codEstilo) references ESTILO(codigo);
alter table OBRA_AUTOR add constraint FK_OBRA_AUTOR_OBRA foreign key (codObra) references OBRA(codigo);
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
alter table SOLICITUD_PRESTAMO add constraint FK_SOLICITUD_PRESTAMO_MUSEO foreign key(codMuseo) references MUSEO_ASOCIADO(codigo);

-- ==================== RESTRICCIONES UNIQUE (UQ) ===================
alter table OBRA add constraint UQ_OBRA unique(nombre);
alter table AUTOR add constraint UQ_AUTOR unique (nombre);
alter table MUSEO_ASOCIADO add constraint UQ_MUSEO_ASOCIADO unique (nombre);

-- ==================== RESTRICCIONES CHECK (CC) ===================
alter table OBRA add constraint CC_OBRA_TIPO check(tipo in ('E','C','O','e','c','o'));
alter table OBRA_AUTOR add constraint CC_OBRA_AUTOR_TIPOAUTOR check(tipoAutor in ('A','C','a','c'));
alter table SOLICITUD_PRESTAMO add constraint CC_SOLICITUD_PRESTAMO_ESTADO check(estado in ('D','N','d','n'));
alter table OBRA add constraint CC_OBRA_VALORACION check(valoracion>=0);
alter table PRESTAMO add constraint CC_PRESTAMO_IMPORTE check(importe>=0);

-- ==================== VALORES POR DEFECTO (DEFAULT) ===================
alter table SOLICITUD_PRESTAMO modify estado default 'D';
alter table OBRA modify tipo default 'O';
```

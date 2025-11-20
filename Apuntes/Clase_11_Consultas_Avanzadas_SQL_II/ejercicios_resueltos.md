# Ejercicios Resueltos - Clase 11: Consultas Avanzadas SQL II

## Práctica Calificada #3 (Solucionario - 30 de Octubre de 2013)

Esta es la solución a una práctica calificada que evalúa la capacidad de construir consultas SQL complejas a partir de un modelo de datos dado. Los ejercicios cubren `GROUP BY`, `JOIN`s, subconsultas, `ROWNUM`, hints de paralelismo y optimización de índices.

### Modelo de Datos
*(El modelo de datos se presenta en el documento original como un diagrama de Entidad-Relación, mostrando tablas como `Pelicula`, `Categoria`, `Actor`, `Director`, `Opinion`, `Cartelera`, `Funcion`, etc.)*

---

### Consultas

**1. Mostrar la cantidad de películas que fueron estrenadas en el año 2012. Tenga en cuenta que el campo `FechaEstreno` es un tipo de dato `DATE`. Paralelizar la consulta con 4 hilos de ejecución.**
```sql
select /*+ PARALLEL(p,4) */ count(*)
from pelicula p
where to_char(fechaestreno,'YYYY')='2012';
```

**2. Mostrar un reporte donde se visualice la cantidad de películas por categoría que ha participado el actor Charlton Heston. El reporte debe mostrar la descripción de la categoría y el total de veces que el actor ha participado.**
```sql
select c.descripcion, count(*)
from pelicula p 
join categoria c on p.idcategoria = c.idcategoria
join actor_pelicula ap on ap.idpelicula = p.idpelicula
join actor a on a.idactor = ap.idactor
where a.nombreCompleto = 'Charlton Heston'
group by c.descripcion;
```

**3. Indique cual es la semana del año 2012 que ha tenido más carteleras presentadas.**
```sql
select #semana from (
    select #semana, count(*) as total
    from cartelera
    where año=2012
    group by #semana
    order by total desc
)
where rownum<=1;
```

**4. Por cada película, liste el titulo de distribución y la cantidad de directores que han participado en ella.**
```sql
select p.tituloDistri, count(*)
from pelicula p 
join director_pelicula dp on p.idpelicula = dp.idpelicula
group by p.tituloDistri;
```

**5. Liste por cada categoría, la cantidad de películas con una duración mayor a 90 minutos.**
```sql
select c.descripcion, count(*)
from categoria c 
join pelicula p on c.idcategoria = p.idcategoria
where p.duracion>=90
group by c.descripcion;
```

**6. Liste las categorías que no tienen alguna película asociada.**
```sql
select descripcion
from categoria
where idcategoria not in (select idcategoria from pelicula);
```

**7. Liste el NombreCompleto de cada actor y el personaje que ha tenido en la película cuyo Título Original es: Ben-Hur.**
```sql
select a.nombreCompleto, ap.personaje
from pelicula p 
join actor_pelicula ap on p.idpelicula = ap.idpelicula
join actor a on a.idactor = ap.idactor
where p.TituloOrig = 'Ben-Hur';
```

**8. Liste el Titulo Original de cada película del Genero 'TERROR' que haya tenido más de 5 clasificaciones con el valor de EXCELENTE.**
```sql
select p.TituloOrig, count(*)
from pelicula p 
join genero g on p.idgenero = g.idgenero
join opinion o on o.idpelicula = p.idpelicula
join clasificacion c on c.idclasificacion = o.idclasificacion
where g.descripcion = 'TERROR' and c.descripcion = 'EXCELENTE'
group by p.TituloOrig
having count(*)>5;
```

**9. Liste las películas (Titulo Original) que están disponibles para el público el día 30 de Octubre entre las 18:00 h y las 22:00 h.**
```sql
select p.tituloorig
from pelicula p 
join funcion f on p.idpelicula = f.idpelicula
where to_char(f.dia,'YYYYMMDD')='20131030' and f.horaInicio=18 and f.horaFinal=22;
```

**10. Basado en la siguiente consulta y plan de ejecución, implemente un mecanismo para mejorar el tiempo de respuesta.**
*Consulta Original:*
```sql
select historicoj_.ID_, historicoj_.PROCINST_ as "PROCINST2_169_",
...
from BPMPORTA.HISTORICO_JBPM_TASKINSTANCE historicoj_ where historicoj_.ID_= 2096;
```
*Plan de Ejecución:* Muestra un `TABLE ACCESS FULL`.

*Solución:* Crear un índice en la columna utilizada para el filtro para evitar un recorrido completo de la tabla.
```sql
create index IDX_BPMPORTA_HISTORICO_JBPM_TASKINSTANCE on BPMPORTA.HISTORICO_JBPM_TASKINSTANCE(ID_);
```
---

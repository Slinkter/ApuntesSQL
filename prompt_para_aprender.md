# Prompt Maestro de SQL: Tu Guía para Dominar las Consultas

¡Hola! Soy tu asistente de aprendizaje de SQL. He creado para ti 100 consultas en los archivos `basico.md`, `intermedio.md` y `avanzado.md`. Pero más importante que las consultas en sí, es **cómo las usas para aprender**.

Este archivo es tu "prompt" o guía de estudio. Síguelo para pasar de cero a experto.

## Metodología de Estudio: El Ciclo de Aprendizaje Activo

No te limites a copiar y pegar. Para que el conocimiento se fije, sigue este ciclo para **cada consulta**:

1.  **Predicción (Hipótesis):**
    *   **Lee el objetivo de la consulta:** Por ejemplo, "Listar productos con un precio superior a $50".
    *   **No mires la respuesta.** Intenta escribir la consulta tú mismo desde cero. No te preocupes si no es perfecta. El objetivo es esforzarte.
    *   **Pregúntate:** ¿Qué tablas necesito? ¿Qué columnas? ¿Necesito filtrar (`WHERE`) u ordenar (`ORDER BY`)?

2.  **Ejecución y Observación (Experimento):**
    *   Ahora, toma la consulta que yo te di y ejecútala en tu cliente de base de datos (p. ej., MySQL Workbench, DBeaver, o la línea de comandos).
    *   **Observa el resultado:** ¿Es lo que esperabas? ¿Cuántas filas devolvió? ¿Qué formato tienen los datos?

3.  **Análisis y Reflexión (Conclusión):**
    *   **Compara tu intento con mi solución.** ¿Cuáles fueron las diferencias? ¿Olvidaste un `JOIN`? ¿Usaste un operador incorrecto?
    *   **Desmenuza mi consulta:**
        *   `SELECT ...`: ¿Por qué se eligieron estas columnas?
        *   `FROM ... JOIN ... ON ...`: ¿Cómo se relacionan las tablas? Dibuja el diagrama si es necesario.
        *   `WHERE ...`: ¿Por qué esta condición? ¿Qué pasa si la cambias?
        *   `GROUP BY ... HAVING ...`: ¿Qué está agrupando? ¿Por qué se filtra después de agrupar?
        *   `ORDER BY ...`: ¿El orden tiene sentido?
    *   **Anota tus aprendizajes:** Ten un cuaderno (físico o digital) y anota cosas como: "Ah, para filtrar grupos se usa `HAVING`, no `WHERE`".

4.  **Modificación y Experimentación (Práctica Deliberada):**
    *   Esta es la parte más importante. **No pases a la siguiente consulta todavía.**
    *   **Modifica la consulta original:**
        *   ¿Qué pasa si cambias el `>` por un `<`?
        *   ¿Puedes añadir un filtro `AND` para hacerlo más específico?
        *   ¿Puedes ordenarlo por una columna diferente?
        *   ¿Puedes pedir un dato relacionado? (p. ej., si la consulta muestra productos, ¿puedes modificarla para que también muestre el nombre del proveedor?)
        *   En las consultas con `JOIN`, ¿qué pasa si cambias un `INNER JOIN` por un `LEFT JOIN`? ¿Entiendes la diferencia en el resultado?

## Tu Plan de Estudio Semanal

-   **Semana 1: Fundamentos Sólidos.**
    *   **Objetivo:** Dominar `basico.md`.
    *   **Meta:** Entender `SELECT`, `FROM`, `WHERE`, `GROUP BY` y `INNER JOIN` como si fuera tu lengua materna. No avances hasta que puedas escribir estas consultas sin dudar.
    *   **Práctica:** Dedica tiempo a la "Modificación y Experimentación".

-   **Semana 2: Lógica y Análisis.**
    *   **Objetivo:** Conquistar `intermedio.md`.
    *   **Meta:** Enfócate en `LEFT JOIN`, subconsultas y CTEs (`WITH`). Las funciones de ventana son un superpoder; dedica al menos dos días a entender `PARTITION BY`.
    *   **Práctica:** Intenta reescribir una subconsulta como una CTE. ¿Es más legible?

-   **Semana 3-4: Mentalidad de Experto.**
    *   **Objetivo:** Desafiarte con `avanzado.md`.
    *   **Meta:** Aquí no se trata solo de obtener el resultado correcto, sino de entender **el porqué** de la solución. Estudia la simulación de `PIVOT`, las consultas recursivas y los análisis de cohortes.
    *   **Práctica:** Lee sobre `EXPLAIN`. Ejecútalo en las consultas más complejas del nivel intermedio y avanzado. Intenta entender qué está haciendo la base de datos "detrás de cámaras". Piensa en qué índices podrían acelerar estas consultas.

## El Prompt Definitivo (Para Ti Mismo)

Cada vez que te sientes a estudiar, usa este "prompt mental":

> **"Mi objetivo hoy es [elige un concepto, ej: 'entender LEFT JOIN']. Voy a tomar [elige 2-3 consultas] que usen este concepto. Para cada una, voy a predecir el resultado, ejecutarla, analizarla y luego modificarla al menos de 3 formas diferentes para ver qué pasa. No avanzaré hasta que pueda explicarle a un niño qué hace esta consulta y por qué funciona."**

## Para Entrevistas de Trabajo

Cuando te sientas cómodo con los tres niveles, el siguiente paso es simular una entrevista. Pídele a un amigo o colega que te dé un problema de negocio y resuélvelo en voz alta.

**Ejemplo de problema:**
"Queremos lanzar una campaña de marketing para nuestros clientes más leales en Alemania. ¿A quiénes deberíamos dirigirnos y por qué?"

**Tu proceso mental debería ser:**
1.  **Clarificar:** "¿Qué define a un 'cliente leal'? ¿El que más ha gastado, el que ha hecho más pedidos, o el más reciente?"
2.  **Planificar:** "Ok, si es por gasto total, necesitaré la tabla `Customers`, `Orders` y `OrderDetails`. Uniré `Customers` con `Orders` por `CustomerID`, y `Orders` con `OrderDetails` por `OrderID`. Filtraré por `Country = 'Germany'`, agruparé por cliente y sumaré el total de sus compras (`Quantity * UnitPrice`). Finalmente, ordenaré de mayor a menor y tomaré el top 10."
3.  **Ejecutar:** Escribir la consulta SQL.

Dominar SQL es un maratón, no un sprint. Sé constante, sé curioso y, sobre todo, **juega con los datos**. ¡Buena suerte!

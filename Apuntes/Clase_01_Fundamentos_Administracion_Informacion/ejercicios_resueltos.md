# Ejercicios Resueltos - Clase 01: Fundamentos de Administración de Información

### Ejercicio 1: Identificación de Problemas en un Sistema de Ficheros Tradicional

#### Enunciado

Una pequeña empresa de ventas gestiona sus operaciones con tres departamentos: **Pedidos**, **Contabilidad** y **Nóminas**. Cada departamento ha desarrollado sus propias aplicaciones y gestiona sus propios archivos de datos, como se muestra en el siguiente diagrama (inspirado en la diapositiva 14 de la clase):

*   **Departamento de Pedidos:**
    *   Tiene una aplicación para la **Gestión de Órdenes**.
    *   Utiliza los archivos: `Customer_Master_File.dat`, `Inventory_Master_File.dat` y `Back_Order_File.dat`.

*   **Departamento de Contabilidad:**
    *   Tiene una aplicación para la **Facturación (Invoicing)**.
    *   Utiliza los archivos: `Inventory_Pricing_File.dat` y `Customer_Master_File.dat`.

*   **Departamento de Nóminas:**
    *   Tiene una aplicación para gestionar el **Pago a Empleados**.
    *   Utiliza el archivo: `Employee_Master_File.dat`.

**Preguntas:**

1.  **Redundancia de Datos:** ¿Qué archivo(s) específico(s) representa(n) un claro ejemplo de redundancia de datos en este sistema? ¿Por qué es un problema?
2.  **Inconsistencia de Datos:** Describe un escenario práctico en el que podría ocurrir una inconsistencia de datos. ¿Cuál sería el impacto en el negocio?
3.  **Dependencia Programa-Dato:** El departamento de Contabilidad decide que necesita añadir un campo "descuento_cliente" al `Customer_Master_File.dat`. ¿Qué implicaciones tiene este cambio en el sistema global?

---

#### Solución

##### 1. Redundancia de Datos

*   **Archivo Redundante:** El `Customer_Master_File.dat` es el ejemplo más claro de redundancia. Existe una copia tanto en el departamento de **Pedidos** como en el de **Contabilidad**.
*   **Problema:**
    *   **Ineficiencia de Almacenamiento:** Se está utilizando espacio en disco para guardar la misma información dos veces.
    *   **Complejidad en la Actualización:** Cualquier cambio en los datos de un cliente (ej. cambio de dirección o teléfono) debe realizarse en **ambos archivos** por separado, lo que aumenta la carga de trabajo y el riesgo de errores.
    *   **Fuente de Inconsistencias:** Es la causa directa del siguiente problema.

##### 2. Escenario de Inconsistencia de Datos

*   **Escenario:** Un cliente, "ABC Corp", llama al departamento de Pedidos para informar que ha cambiado su dirección de facturación. El empleado de Pedidos actualiza la dirección en *su* copia del `Customer_Master_File.dat`. Sin embargo, nadie notifica al departamento de Contabilidad para que actualice *su* copia del mismo archivo.
*   **Impacto en el Negocio:**
    *   Al final del mes, Contabilidad emite una factura para "ABC Corp" y la envía a la **dirección antigua**, que está en su archivo desactualizado.
    *   El cliente nunca recibe la factura, o la recibe con mucho retraso.
    *   La empresa experimenta un retraso en el cobro, lo que afecta su flujo de caja.
    *   Se proyecta una imagen poco profesional y se genera una mala experiencia para el cliente, que podría perder la confianza en la empresa.

##### 3. Implicaciones de la Dependencia Programa-Dato

*   **Implicaciones del Cambio:**
    1.  **Modificación en Contabilidad:** El equipo de desarrollo de Contabilidad debe modificar su aplicación de **Facturación** para que pueda manejar el nuevo campo "descuento_cliente" en su versión del `Customer_Master_File.dat`.
    2.  **Falla en Pedidos:** La aplicación de **Gestión de Órdenes** del departamento de Pedidos **dejará de funcionar** o funcionará incorrectamente. Su código no está preparado para leer un archivo `Customer_Master_File.dat` con una estructura diferente (el nuevo campo añadido). No sabe cómo interpretar ese dato extra.
    3.  **Necesidad de Coordinación y Doble Trabajo:** Para que el sistema vuelva a ser estable, el departamento de Pedidos también tendría que modificar su aplicación, incluso si no necesita usar el campo "descuento_cliente". Esto demuestra una fuerte **dependencia programa-dato**: un cambio en los datos obliga a realizar cambios en múltiples programas, generando costos, retrasos y una alta fragilidad en el sistema.

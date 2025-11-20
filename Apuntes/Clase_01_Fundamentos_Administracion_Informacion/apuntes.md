# Clase 01: Fundamentos de Administración de Información

**Fecha:** 2013 (Inferido de la diapositiva de presentación), Revisión 2013-1

---

## Pistas y Keywords

*   **Dato vs. Información:** El dato es objetivo, la información es subjetiva.
*   **Jerarquía del Conocimiento:** Datos -> Información -> Conocimiento.
*   **Sistemas Heredados:** Procesamiento tradicional de archivos.
*   **Problemas Clave:**
    *   Redundancia de datos.
    *   Dependencia programa-dato.
    *   Inconsistencia de datos.
*   **Solución:** Enfoque de Base de Datos.
*   **DBMS:** Sistema de Gestión de Base de Datos.
*   **Metadatos:** Datos sobre los datos.
*   **Componentes del Entorno:** CASE, Repositorio, DBMS, Base de Datos, Aplicaciones.
*   **SDLC:** Ciclo de Vida de Desarrollo de Sistemas.
*   **Evolución de BD:** Jerárquico, Redes, Relacional, Objeto-Relacional, NoSQL.
*   **SQL:** Lenguaje de Consulta Estructurado (DML, DDL, DCL).

---

## Notas Generales

### Del Dato al Conocimiento

El punto de partida de la gestión de información es la distinción entre conceptos fundamentales:

*   **Dato:** Es una representación simbólica de un hecho o mensaje, como una cifra o un nombre. Debe ser **objetivo** y tiene poco significado semántico por sí solo. (Ej: 3.50).
*   **Información:** Es el resultado de procesar y contextualizar los datos, disminuyendo la incertidumbre. Puede ser **subjetiva**, ya que su significado es percibido por el receptor. (Ej: Un reporte mostrando que el precio de un producto subió de 2.0 a 3.50).
*   **Conocimiento:** Es el entendimiento derivado de la información, que requiere reflexión y síntesis. A menudo es tácito y permite la toma de decisiones. (Ej: "Las ventas de un producto cayeron porque el precio subió, debemos ajustar la estrategia").

### El Problema: Sistemas Tradicionales de Archivos

Antes del enfoque de bases de datos, las empresas utilizaban sistemas de procesamiento de archivos. Cada aplicación (Facturación, Pedidos, Nóminas) mantenía sus propios archivos de datos privados. Este enfoque presentaba graves desventajas:

1.  **Dependencia Programa-Datos:** El código de la aplicación estaba estrechamente ligado a la estructura física de los datos. Un simple cambio en el formato de un archivo requería modificar todos los programas que lo usaban.
2.  **Redundancia de Datos:** La misma información (como los datos de un cliente) se duplicaba en múltiples archivos, desperdiciando espacio y generando un gran problema de mantenimiento.
3.  **Inconsistencia de Datos:** El principal problema de la redundancia. Si un dato se actualizaba en un archivo pero no en otro, se perdía la integridad y la confianza en la información.
4.  **Acceso Limitado y No Estándar:** No había una forma centralizada o estandarizada de consultar o compartir datos entre aplicaciones.

### La Solución: El Enfoque de Base de Datos

Para resolver estos problemas, surge el concepto de **Base de Datos (BD)**: una colección de datos lógicamente relacionados y centralizados, diseñados para ser compartidos por múltiples usuarios y aplicaciones.

Esta centralización es gestionada por un **Sistema de Gestión de Base de Datos (DBMS)**, que es un software que actúa como intermediario entre los usuarios/aplicaciones y la base de datos física.

**Ventajas del enfoque de BD:**

*   **Independencia Programa-Datos:** El DBMS maneja los metadatos (la definición de los datos). Las aplicaciones ya no necesitan conocer la estructura física de almacenamiento, lo que facilita el mantenimiento.
*   **Redundancia Mínima:** Al centralizar los datos, se reduce drásticamente la duplicación, mejorando la consistencia e integridad.
*   **Calidad y Compartición de Datos Mejoradas:** Se pueden aplicar reglas de validación y restricciones de forma centralizada. Diferentes usuarios pueden acceder a las mismas fuentes de datos.
*   **Reforzamiento de Estándares:** El acceso a los datos se realiza de manera uniforme a través del DBMS.
*   **Seguridad y Recuperación Centralizadas:** El DBMS provee mecanismos para control de acceso, backups y recuperación ante desastres.

### Componentes de un Entorno de Base de Datos

Un entorno de base de datos moderno incluye varios componentes clave que trabajan juntos:

*   **Herramientas CASE:** Para el diseño de la BD y las aplicaciones.
*   **Repositorio:** Una base de conocimientos que almacena los metadatos (definiciones, relaciones, formatos).
*   **DBMS:** El software que gestiona la base de datos.
*   **Base de Datos:** La colección de datos operativos.
*   **Aplicaciones:** Programas que interactúan con la base de datos.

### Evolución de las Bases de Datos

El modelo de bases de datos ha evolucionado a lo largo del tiempo para adaptarse a nuevas necesidades:
*   **1960s:** Modelos Jerárquicos (IMS) y de Redes (CODASYL).
*   **1980s:** Modelo Relacional (Oracle, DB2), que se convirtió en el estándar de la industria.
*   **1990s:** Modelos Orientados a Objetos y Objeto-Relacional.
*   **2000s:** Auge de las bases de datos para la Web, XML y NoSQL, diseñadas para grandes volúmenes de datos y flexibilidad.

---

## Resumen Final Crítico

Esta clase establece la justificación fundamental para la existencia de las bases de datos. La transición desde los sistemas de archivos tradicionales, plagados de redundancia, inconsistencia y altos costos de mantenimiento, hacia un enfoque centralizado gestionado por un DBMS, resolvió problemas críticos de negocio. Comprender que una base de datos no es solo un "almacén", sino un ecosistema completo (con DBMS, metadatos y herramientas) que garantiza la independencia entre datos y aplicaciones, es el pilar para construir sistemas de información robustos, consistentes y mantenibles. Este fundamento histórico y conceptual es esencial para apreciar el diseño y la función del modelo relacional y otras tecnologías de datos que se estudiarán a continuación.

---

## Conexiones con Clases Anteriores y Siguientes

*   **Conexiones Anteriores:** Esta es la clase fundacional del curso de Ingeniería de Datos.
*   **Conexiones Siguientes:** Los conceptos aquí presentados son la base para entender la **Clase 02 (Sistemas de Gestión de Base de Datos)**, donde se profundizará en el rol y la arquitectura del DBMS. También proporciona el contexto para la **Clase 03 (Bases de Datos Relacionales)**, que explora el modelo dominante que surgió como solución a los problemas aquí planteados, y para la **Clase 04 (Administración de RDBMS)**, que aborda la gestión práctica de estos sistemas.
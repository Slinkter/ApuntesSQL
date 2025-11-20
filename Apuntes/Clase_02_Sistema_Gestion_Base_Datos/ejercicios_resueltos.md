# Ejercicios Resueltos - Clase 02: Modelo Relacional

### Ejercicio 1: Identificación de Componentes Relacionales

**Enunciado:**
Dada la siguiente estructura simplificada de una tabla `EMPLEADOS` en un sistema de base de datos universitario:

**Tabla `EMPLEADOS`**

| ID_Empleado (PK) | Nombre    | Apellido  | Email                 | ID_Departamento (FK) | Fecha_Contratacion | Salario |
| :--------------- | :-------- | :-------- | :-------------------- | :------------------- | :----------------- | :------ |
| 1001             | Ana       | García    | ana.g@uni.edu         | 10                   | 2018-03-01         | 60000   |
| 1002             | Luis      | Pérez     | luis.p@uni.edu        | 20                   | 2020-07-15         | 75000   |
| 1003             | Marta     | Sánchez   | marta.s@uni.edu       | 10                   | 2019-11-01         | 62000   |
| 1004             | Pedro     | Ruíz      | pedro.r@uni.edu       | 30                   | 2021-01-20         | 80000   |

Responde las siguientes preguntas basándote en la terminología del modelo relacional:

1.  ¿Cuál es el nombre de la **Relación**?
2.  Proporciona un ejemplo de **Tupla**.
3.  Proporciona tres ejemplos de **Atributos**.
4.  Identifica la **Primary Key (PK)** y justifica por qué lo es.
5.  Identifica la **Foreign Key (FK)** y explica su propósito.

**Solución:**

1.  **Relación:** `EMPLEADOS`
2.  **Tupla:** `(1001, Ana, García, ana.g@uni.edu, 10, 2018-03-01, 60000)` (cualquier fila completa es una tupla).
3.  **Atributos:** `ID_Empleado`, `Nombre`, `Apellido`, `Email`, `ID_Departamento`, `Fecha_Contratacion`, `Salario` (cualquier tres de estos).
4.  **Primary Key (PK):** `ID_Empleado`. Es la PK porque identifica de forma única a cada empleado; no hay dos empleados con el mismo `ID_Empleado`, y cada empleado debe tener un `ID_Empleado` (no puede ser nulo).
5.  **Foreign Key (FK):** `ID_Departamento`. Su propósito es establecer una relación con la tabla `DEPARTAMENTOS` (asumiendo que existe una tabla con `ID_Departamento` como PK), indicando a qué departamento pertenece cada empleado.

### Ejercicio 2: Aplicando las Propiedades ACID

**Enunciado:**
Un banco tiene un sistema de base de datos para gestionar transferencias de dinero. Un cliente desea transferir 100 USD de su cuenta A a la cuenta B de otro cliente. Describe cómo cada una de las propiedades ACID (`Atomicidad`, `Consistencia`, `Aislamiento`, `Durabilidad`) se aplica a esta operación de transferencia.

**Solución:**

1.  **Atomicidad:** La operación de transferencia completa (restar 100 USD de la cuenta A y sumar 100 USD a la cuenta B) debe ejecutarse por completo o no ejecutarse en absoluto. Si, por ejemplo, el sistema falla después de restar el dinero de la cuenta A pero antes de sumarlo a la cuenta B, la atomicidad asegura que la base de datos se revierta a su estado original, como si la transferencia nunca hubiera ocurrido. No puede haber una situación donde el dinero se pierda en el "aire".

2.  **Consistencia:** Antes de la transferencia, la suma del dinero en cuenta A y cuenta B debe ser un valor `X`. Después de una transferencia exitosa, la suma del dinero en cuenta A (restando 100) y cuenta B (sumando 100) debe seguir siendo `X`. La base de datos debe pasar de un estado consistente a otro estado consistente. Las reglas de negocio (ej. el saldo de una cuenta no puede ser negativo) también deben mantenerse.

3.  **Aislamiento:** Si otro cliente intenta consultar el saldo de la cuenta A o la cuenta B *durante* la transferencia, no verá un estado intermedio (ej. la cuenta A con el dinero restado pero la cuenta B aún sin el dinero sumado). Las operaciones de transferencia se ejecutan de forma aislada, como si fueran la única operación en el sistema. Otros usuarios verán el estado antes de la transferencia o el estado después de que la transferencia se haya completado exitosamente.

4.  **Durabilidad:** Una vez que la transferencia de dinero ha sido confirmada como exitosa (commit), los cambios realizados (dinero restado de A, dinero sumado a B) deben ser permanentes. Incluso si el sistema sufre un fallo de energía inmediatamente después del commit, la base de datos debe ser capaz de recuperar esos cambios y asegurar que el dinero esté correctamente reflejado en ambas cuentas cuando el sistema se reinicie.

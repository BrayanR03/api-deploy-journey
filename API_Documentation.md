# API - Evaluación del Riesgo de Infarto de Miocardio

## 1. Descripción del Proyecto

API REST desarrollada con **Flask** que permite exponer un modelo de Machine Learning previamente entrenado y validado, orientado a la evaluación del riesgo de infarto de miocardio.

La aplicación proporciona una interfaz para recibir información relacionada con la salud del paciente, ejecutar predicciones mediante el modelo de clasificación y gestionar las evaluaciones realizadas.

El proyecto implementa una **arquitectura en capas (Layered Architecture)**, permitiendo separar las responsabilidades de cada componente, mejorar la mantenibilidad del código y facilitar futuras ampliaciones.

## 2. Tecnologías Utilizadas

| Tecnología | Propósito |
|---|---|
| Python | Lenguaje de programación principal |
| Flask | Desarrollo de la API REST |
| PostgreSQL | Sistema de gestión de bases de datos |
| SQLAlchemy | ORM e interacción con la base de datos |
| Flask-Migrate | Administración de migraciones |
| Alembic | Motor de migraciones utilizado por Flask-Migrate |
| PyTest | Ejecución de pruebas automatizadas |
| UV | Gestión de dependencias y entorno del proyecto |
| RandomForestClassifier | Modelo de clasificación binaria |

## 3. Características Técnicas

El proyecto incorpora los siguientes aspectos técnicos:

- **Arquitectura en capas:** Separación de responsabilidades para facilitar el mantenimiento, la escalabilidad y la organización del código.
- **Integración de Machine Learning:** Implementación de un modelo previamente entrenado y validado mediante el algoritmo Random Forest, específicamente `RandomForestClassifier`.
- **Persistencia de datos:** Integración con PostgreSQL para almacenar las evaluaciones realizadas mediante la API.
- **Gestión de migraciones:** Implementación de Flask-Migrate, que utiliza Alembic internamente para administrar los cambios en el esquema de la base de datos.
- **Pruebas automatizadas:** Utilización de PyTest para validar el comportamiento y la funcionalidad de los componentes de la API.
- **Gestión de dependencias:** Utilización de UV para administrar las dependencias y la ejecución del proyecto.

### 3.1. Modelo de Machine Learning

La API expone un modelo de clasificación binaria basado en el algoritmo Random Forest, utilizando específicamente `RandomForestClassifier`.

El modelo permite obtener dos posibles resultados:

- `1`: Alto riesgo.
- `0`: Bajo riesgo.

La predicción se realiza a partir de las características numéricas esperadas por el modelo durante su entrenamiento.

**Importante:** Los resultados representan predicciones generadas por un modelo de Machine Learning con fines demostrativos. No constituyen un diagnóstico médico ni sustituyen la evaluación de un profesional de la salud.


## 4. Endpoints Disponibles

La API dispone de los siguientes endpoints:

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Endpoint principal de la API. |
| POST | `/evaluations/evaluate` | Ejecuta una evaluación de riesgo y almacena el resultado. |
| GET | `/evaluations` | Obtiene el listado de todas las evaluaciones registradas. |
| GET | `/evaluations/<uuid_evaluation>` | Recupera una evaluación específica mediante su UUID. |
| DELETE | `/evaluations/<uuid_evaluation>` | Elimina una evaluación específica mediante su UUID. |

## 5. Datos de Prueba

A continuación, se presentan ejemplos de solicitudes que pueden utilizarse para validar la funcionalidad de predicción de la API.

Se contemplan dos representaciones de entrada:

1. **Representación numérica:** Los datos se envían utilizando directamente los valores numéricos esperados por el modelo de Machine Learning.
2. **Representación booleana:** Los datos se envían utilizando valores booleanos, que posteriormente son transformados a su representación numérica correspondiente antes de ejecutar la predicción.

### 5.1. Datos para obtener una predicción de alto riesgo

**A. Representación numérica (entrada directa al modelo)**

```json
{
  "Age": 40,
  "Sex": 1,
  "BMI": 19.05,
  "Smoker": 0,
  "PhysActivity": 1,
  "PhysHlth": 0,
  "MentHlth": 0,
  "HighChol": 1,
  "Diabetes": 2,
  "HighBP": 1
}
```

**B. Representación booleana (entrada mediante el body de la solicitud)**

```json
{
  "age": 40,
  "sex": true,
  "bmi": 19.05,
  "smoker": false,
  "physical_activity": true,
  "physical_health": 0,
  "mental_health": 0,
  "high_cholesterol": true,
  "diabetes": true,
  "high_blood_pressure": true
}
```

### 5.2. Datos para obtener una predicción de bajo riesgo

**A. Representación numérica (entrada directa al modelo)**

```json
{
  "Age": 50,
  "Sex": 0,
  "BMI": 20.00,
  "Smoker": 0,
  "PhysActivity": 0,
  "PhysHlth": 0,
  "MentHlth": 15,
  "HighChol": 0,
  "Diabetes": 0,
  "HighBP": 0
}
```

**B. Representación booleana (entrada mediante el body de la solicitud)**

```json
{
  "age": 50,
  "sex": false,
  "bmi": 20.00,
  "smoker": false,
  "physical_activity": false,
  "physical_health": 0,
  "mental_health": 15,
  "high_cholesterol": false,
  "diabetes": false,
  "high_blood_pressure": false
}
```

### 5.3. Conversión de Características Booleanas

Cuando se utiliza la representación booleana, la API realiza una transformación de los valores antes de enviarlos al modelo de Machine Learning.

La conversión aplicada es la siguiente:

| Característica | Valor `true` | Valor `false` |
|---|---:|---:|
| Sex | 1 | 0 |
| Smoker | 1 | 0 |
| PhysActivity | 1 | 0 |
| HighChol | 1 | 0 |
| HighBP | 1 | 0 |
| Diabetes | 2 | 0 |

**Consideración especial para Diabetes:**

La característica `Diabetes` utiliza una codificación particular:

- `true` se transforma en `2`.
- `false` se transforma en `0`.

Esta conversión responde a la representación numérica utilizada durante el entrenamiento del modelo y debe mantenerse para garantizar la consistencia de las características de entrada.

**Nota:** Los ejemplos numéricos y booleanos representan dos formas de enviar información a la API. Cada representación debe respetar las transformaciones correspondientes antes de ejecutar la predicción.

## 6. Autor

**Brayan Neciosup Bolaños**

Data & Cloud Engineer

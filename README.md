# API Deployment Journey

## 1. Descripción del Repositorio

**API Deployment Journey** es un proyecto orientado a documentar y poner en práctica diferentes estrategias de despliegue de una API REST, explorando las herramientas, tecnologías e infraestructuras utilizadas en cada escenario.

El proyecto toma como punto de partida una API desarrollada con Flask y utiliza una misma aplicación para experimentar con diferentes alternativas de ejecución y despliegue, desde un entorno local hasta infraestructuras basadas en servicios de nube.

Cada etapa aborda un escenario específico, documentando su arquitectura, configuración, implementación y validación.

## 2. Objetivo del Proyecto

El objetivo principal es comprender y aplicar diferentes enfoques de despliegue de aplicaciones backend, identificando los componentes involucrados y las consideraciones técnicas de cada alternativa.

A través de este recorrido se busca:

- Comprender las diferencias entre los distintos escenarios de despliegue.
- Aplicar herramientas de contenerización y orquestación.
- Explorar alternativas de infraestructura y servicios cloud.
- Documentar las configuraciones y procedimientos necesarios para cada escenario.
- Validar el funcionamiento de la API después de cada implementación.

## 3. API Utilizada

Para desarrollar este recorrido se utiliza una API REST denominada **Evaluación del Riesgo de Infarto de Miocardio**.

La aplicación está desarrollada con Flask e implementa un modelo de Machine Learning basado en Random Forest para realizar predicciones de riesgo. Asimismo, incorpora PostgreSQL para la persistencia de las evaluaciones y una arquitectura en capas para organizar sus componentes.

La API constituye la aplicación base utilizada a lo largo de las diferentes etapas del proyecto.

Para conocer su arquitectura, características técnicas, endpoints y ejemplos de solicitudes, consulta la [Documentación de la API](./API_Documentation.md).

## 4. Etapas de Despliegue

El proyecto se desarrolla progresivamente mediante diferentes etapas, cada una enfocada en una estrategia de despliegue específica.

Las etapas se documentan individualmente, incluyendo su arquitectura, herramientas utilizadas, procedimiento de implementación y pruebas de validación.


### tabla para definir cada stage ...


## 5. Estructura de la Documentación

La documentación del proyecto se organiza en dos niveles principales:

- **Documentación de la API:** describe la arquitectura, las características técnicas y el funcionamiento de la aplicación.
- **Documentación por Stage:** explica los procedimientos, configuraciones, arquitecturas y validaciones correspondientes a cada escenario de despliegue.

Esta organización permite mantener una documentación independiente para cada etapa, evitando duplicar información y facilitando la incorporación de nuevas estrategias.

## 6. Autor

**Brayan Neciosup Bolaños**

Data & Cloud Engineer

### Stage 1 — Despliegue local

Ejecución de la API directamente en un entorno local, utilizando UV para la gestión de dependencias y PostgreSQL como sistema de persistencia.

**Documentación:** [Stage 1 — Despliegue local](Stage_1_Documentation.md)

### Próximas etapas

Las siguientes etapas se incorporarán progresivamente conforme se desarrollen y validen sus respectivas implementaciones.

## 5. Tecnologías y Herramientas

El proyecto utiliza diferentes tecnologías y herramientas dependiendo del escenario de despliegue abordado.

Entre las principales tecnologías de la aplicación base se encuentran:

| Tecnología | Propósito |
|---|---|
| Python | Lenguaje de programación |
| Flask | Desarrollo de la API REST |
| PostgreSQL | Gestión de la base de datos |
| SQLAlchemy | ORM e interacción con la base de datos |
| Flask-Migrate / Alembic | Gestión de migraciones |
| PyTest | Pruebas automatizadas |
| UV | Gestión de dependencias y entorno Python |
| Random Forest | Modelo de Machine Learning |

Las herramientas adicionales de infraestructura, contenerización y servicios cloud se detallan en la documentación de cada etapa.

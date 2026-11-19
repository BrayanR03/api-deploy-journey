# Stage 1 — Despliegue Local

## 1. Descripción del Stage

En esta primera etapa se realizará el despliegue de la API en un entorno local, utilizando los recursos y herramientas necesarios para ejecutar la aplicación directamente en la máquina del desarrollador.

El objetivo es preparar el entorno de ejecución, configurar la conexión con PostgreSQL, disponer del modelo de Machine Learning y ejecutar la API para validar su funcionamiento.

## 2. Preparación del Proyecto

Para comenzar, debes clonar el repositorio desde GitHub:

```bash
git clone https://github.com/BrayanR03/api-deploy-journey.git
```

Una vez clonado, ingresa a la carpeta del proyecto.

### 2.1. Configuración de UV

El proyecto utiliza **UV** como gestor de paquetes y dependencias de Python.

Para preparar el entorno de ejecución, debes:

1. Tener instalado UV en tu máquina. Puedes consultar su documentación oficial: https://docs.astral.sh/uv/
2. Ejecutar la sincronización de las dependencias del proyecto:

```bash
uv sync
```

Este comando instalará las dependencias definidas en `pyproject.toml` y `uv.lock`, preparando el entorno necesario para ejecutar la API.


### 2.2. Obtención del modelo de Machine Learning

La API requiere disponer del modelo de Machine Learning previamente entrenado y almacenado en formato `.pkl`.

Para obtenerlo:

1. Dirígete a la carpeta `app/static/`.
2. Abre el archivo `model_mi_pkl.txt`.
3. Accede al enlace de Google Drive proporcionado.
4. Descarga el archivo del modelo en formato `.pkl`.
5. Coloca el archivo descargado dentro de `app/static/`.

Importante: El archivo descargado debe conservar exactamente su nombre original y ubicarse en app/static/, respetando la ruta esperada por la aplicación.

### 2.3. Ejecución en una carpeta independiente (Opcional)

Si deseas trabajar con la API en una carpeta independiente del repositorio original, puedes copiar únicamente los siguientes archivos y directorios:

```text
app/
migrations/
pyproject.toml
uv.lock
.python-version
.gitignore
README.md (opcional)
```

De esta manera, dispondrás de una copia independiente de la aplicación, evitando interferencias con otros archivos o componentes del repositorio original.

Considera que esta alternativa requiere conservar los recursos necesarios para ejecutar la API, incluyendo el modelo `.pkl` dentro de `app/static/`.

## 3. Configuración de la Base de Datos

La aplicación utiliza **PostgreSQL** como sistema de gestión de bases de datos relacionales para almacenar las evaluaciones realizadas mediante la API.

Para este escenario, debes tener PostgreSQL instalado y en ejecución en tu máquina local.

### 3.1. Creación de la Base de Datos

Crea una base de datos con el siguiente nombre:

```sql
CREATE DATABASE db_api_evaluate_mi;
```

La aplicación utilizará esta base de datos para almacenar los registros de las evaluaciones realizadas.

### 3.2. Configuración de las Variables de Entorno

Antes de ejecutar el proyecto, debes crear un archivo denominado `.env` en la raíz de la aplicación.

Agrega las siguientes variables de entorno iniciales:

```env
APP_ENV=development
DATABASE_URL=postgresql+psycopg://postgres:12345@localhost:5432/db_api_evaluate_mi
SECRET_KEY=TU-SECRET-KEY
```

**Consideraciones:**

- `APP_ENV`: Define el entorno de ejecución de la aplicación. Para este escenario se establece en `development`.
- `DATABASE_URL`: Cadena de conexión a PostgreSQL. Debes reemplazar el usuario, la contraseña, el host, el puerto y el nombre de la base de datos según tu configuración.
- `SECRET_KEY`: Clave secreta utilizada por Flask para gestionar operaciones que requieren protección criptográfica.

**Importante:** Los valores proporcionados son únicamente referencias iniciales. Debes reemplazarlos por los correspondientes a tu entorno local.

Asimismo, asegúrate de que `.env` esté incluido en `.gitignore` para evitar publicar credenciales o información sensible en el repositorio.

Se recomienda mantener un archivo `.env.example` con las variables necesarias y valores ilustrativos, sin incluir credenciales reales.

### 3.3 Aplicación de Migraciones
Una vez creada la base de datos y configuradas las variables de entorno, debes ejecutar las migraciones para generar la estructura correspondiente en PostgreSQL.

Desde la raíz del proyecto, ejecuta:

```bash
  uv run flask --app app.app db upgrade
```
Este comando aplica las migraciones pendientes definidas mediante Flask-Migrate, utilizando Alembic internamente, y actualiza el esquema de la base de datos.

Una vez finalizado el proceso, la base de datos estará preparada para almacenar las evaluaciones realizadas mediante la API.

## 4. Ejecución de la API

Una vez completados los pasos anteriores, puedes iniciar la aplicación desde la raíz del proyecto mediante el siguiente comando:

```bash
uv run flask --app app.app run
```

* En caso de presentarse el siguiente error (Windows) al ejecutar la API: 
   
   error: Failed to spawn: 
   flask cause: Una directiva de Control de aplicaciones 
   bloqueó este archivo. (os error 4551).

   La solución es: 
   
   ```bash
      uv run python -m flask --app app.app run   
   ```

UV ejecutará Flask utilizando el entorno y las dependencias configuradas en el proyecto.

Por defecto, Flask iniciará su servidor de desarrollo en el entorno local.

## 5. Validación del Funcionamiento

Una vez iniciada la API, corresponde realizar las pruebas funcionales para comprobar que la aplicación responde correctamente y puede interactuar con la base de datos y el modelo de Machine Learning.

Para ello:

1. Ejecuta las solicitudes correspondientes a los endpoints definidos en la documentación de la API.
2. Utiliza los ejemplos de entrada numérica y booleana proporcionados en la sección de datos de prueba.
3. Verifica que las predicciones generadas correspondan con los resultados esperados.
4. Comprueba que las evaluaciones se almacenen correctamente en PostgreSQL.
5. Valida las operaciones de consulta y eliminación de evaluaciones.

Los ejemplos de solicitudes y sus respectivos formatos de entrada se encuentran en la sección **Datos de Prueba** de [API_Documentation.md](../API_Documentation.md).

### 5.1. Evidencias de Ejecución

Las evidencias correspondientes a esta etapa se encuentran en:

```text
assets/
└── images/
    └── stage-1-local/
```

En esta ubicación se presentan capturas de pantalla que permiten visualizar los resultados obtenidos durante las pruebas de funcionamiento de la API en el entorno local.

## 6. Resultado del Stage

Al finalizar esta etapa, se debe disponer de una API REST ejecutándose correctamente en un entorno local, con PostgreSQL como sistema de persistencia y el modelo de Machine Learning integrado para realizar las evaluaciones de riesgo.

Esta implementación constituye el punto de partida para explorar otras estrategias de despliegue en las siguientes etapas del proyecto.

## 7. Autor

**Brayan Neciosup Bolaños**

Data & Cloud Engineer
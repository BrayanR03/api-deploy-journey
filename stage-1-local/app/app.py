from flask import Flask, jsonify

from app.core.config import load_settings
from app.db.db import db, migrate

# Importa aquí las extensiones adicionales cuando existan (se crean a nivel
# de módulo, igual que db y migrate):

## Registrar extensiones/librerías/módulos para Flask
def register_extensions(app: Flask) -> None:
    """Conecta cada extensión a la app con init_app."""
    db.init_app(app) ## Inicializa la app Flask
    migrate.init_app(app, db) ## Inicializa migraciones para la app Flask
    ## extensión_adicional.init_app(app) ## extensiones/librerías/módulos adicionales


## Registar blueprints (routes)
def register_blueprints(app: Flask) -> None:
    # Imports locales: evitan ciclos entre blueprints, servicios y la app.
    from app.blueprints.evaluate_user_blueprint import evaluate_user_bp
    app.register_blueprint(blueprint=evaluate_user_bp)

## Application Factory - Flask (Punto de partida de la app)
def create_app(config_name: str | None = None) -> Flask:
    settings = load_settings(config_name) ## Cargamos configuraciones

    app = Flask(__name__) ## Contexto de app Flask
    app.config.from_mapping(settings.to_flask_config()) ## Cargamos configuración flask

    register_extensions(app) ## Agregamos las extensiones

    ## Importamos los modelos para las migraciones
    from app.db import models  # noqa: F401  (registra tablas para Alembic y create_all)

    register_blueprints(app) ## Agregamos los blueprint

    ## Ruta inicial de la app
    @app.route("/")
    def main():
        return jsonify(
            {
                "info": "API para la evaluación de riesgo de Infarto de Miocardio",
                "version": "1.0.0",
                "author": "Brayan Neciosup"
            }
        ), 200

    return app ## Retornamos la app

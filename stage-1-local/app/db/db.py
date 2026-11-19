from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Session

# Define nombres explícitos para constraints. Debe fijarse ANTES de la primera
# migración: cambiarlo después genera renombres de constraints.
# Nota: la plantilla "ck" exige nombre explícito en todo CheckConstraint
# (CheckConstraint("precio > 0", name="precio_positivo")); sin nombre,
# SQLAlchemy lanza un error al crear la tabla.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


db = SQLAlchemy(model_class=Base)

# Migrate() activa render_as_batch por defecto; migrations/env.py lo
# sobrescribe según el dialecto (solo SQLite). No lo fijes aquí.
migrate = Migrate()


def get_db() -> Session:
    """Sesión síncrona actual; requiere contexto de aplicación activo."""
    return db.session()


# Flask-SQLAlchemy elimina la sesión al salir del contexto, sin hacer commit.
# Los modelos heredan de db.Model (no de Base directamente).
__all__ = ["Base", "db", "migrate", "get_db"]

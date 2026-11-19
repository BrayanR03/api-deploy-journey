import pytest

from app.db.db import db
from app.app import create_app


@pytest.fixture
def app():
    application = create_app("testing")

    # Seguro anti-desastre: nunca correr tests contra una BD real
    assert application.config["TESTING"] is True
    assert application.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"

    with application.app_context():
        db.create_all()  # BD aislada de tests; no sustituye migraciones

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    """Solo para probar repositorios directamente, sin pasar por HTTP."""
    with app.app_context():
        yield db.session
        db.session.remove()

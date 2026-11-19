import os
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Raíz del proyecto, donde vive el .env.
# Ajusta parents[2] solo si cambia la profundidad de este archivo.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
Environment = Literal["development", "testing", "production"]
VALID_ENVIRONMENTS = {"development", "testing", "production"}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        hide_input_in_errors=True,
    )

    APP_ENV: Environment
    SECRET_KEY: SecretStr = Field(min_length=32)
    DATABASE_URL: str = Field(min_length=1)
    PATH_MODEL_ML_PKL: Path

    def to_flask_config(self) -> dict[str, Any]:
        """Claves en mayúsculas listas para app.config.from_mapping()."""
        return {
            "SECRET_KEY": self.SECRET_KEY.get_secret_value(),
            "SQLALCHEMY_DATABASE_URI": self.DATABASE_URL,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True},
            "DEBUG": self.APP_ENV == "development",
            "TESTING": self.APP_ENV == "testing",
            "SESSION_COOKIE_HTTPONLY": True,
            "SESSION_COOKIE_SAMESITE": "Lax",
            "SESSION_COOKIE_SECURE": self.APP_ENV == "production",
            "PATH_MODEL_ML_PKL": self.PATH_MODEL_ML_PKL

        }


def load_settings(config_name: str | None = None) -> Settings:
    environment = (
        config_name
        if config_name is not None
        else os.environ.get("APP_ENV", "development")
    ).strip().lower()

    path_model = PROJECT_ROOT / "app" / "static" / "myocardial_infarction_model.pkl"    

    if environment not in VALID_ENVIRONMENTS:
        raise ValueError("APP_ENV debe ser development, testing o production")

    # Testing: BD aislada en memoria, sin .env ni credenciales reales.
    if environment == "testing":
        return Settings(
            _env_file=None,
            APP_ENV="testing",
            SECRET_KEY="testing-only-key-never-use-in-production",
            DATABASE_URL="sqlite:///:memory:",
            PATH_MODEL_ML_PKL = path_model
        )

    # Development lee .env; production espera variables de entorno reales.
    env_file = PROJECT_ROOT / ".env" if environment == "development" else None
    return Settings(_env_file=env_file, APP_ENV=environment, PATH_MODEL_ML_PKL= path_model)

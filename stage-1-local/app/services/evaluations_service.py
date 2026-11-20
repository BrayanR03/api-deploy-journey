from typing import Any
import uuid

from sqlalchemy.orm import Session

from ..db.models.evaluations import Evaluations
from ..repositories.evaluations_repository import evaluations_repository
from ..utils.helpers import predict_evaluation_model_ml  # ajusta al nombre/ruta real

from ..core.config import load_settings

from ..db.schemas.schema_evaluations import (
    schema_list_evaluation, schema_evaluation
)

settings = load_settings()

class ValidationError(Exception):
    """Datos inválidos. `errors` es un dict campo -> mensaje."""

    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        super().__init__(errors)


class NotFoundError(Exception):
    pass

MODEL_FIELD_NAMES = {
    "age": "Age",
    "sex": "Sex",
    "bmi": "BMI",
    "smoker": "Smoker",
    "physical_activity": "PhysActivity",
    "physical_health": "PhysHlth",
    "mental_health": "MentHlth",
    "high_cholesterol": "HighChol",
    "diabetes": "Diabetes",
    "high_blood_pressure": "HighBP",
}

ALL_FIELDS = tuple(MODEL_FIELD_NAMES)


BOOLEAN_FIELDS = (
    "sex",
    "smoker",
    "physical_activity",
    "high_cholesterol",
    "diabetes",
    "high_blood_pressure",
)

# Campos enteros con rango (mínimo, máximo)
INT_RANGES = {
    "age": (40, 100),
    "physical_health": (0, 30),
    "mental_health": (0, 30),
}

FLOAT_FIELDS = {
    "bmi": (10, 100)
}

def _is_int(value: Any) -> bool:
    """True solo si es un int real (rechaza True/False, 1.0 y "1")."""
    return type(value) is int

def _is_number(value: Any) -> bool:
    """True si es int o float (rechaza True/False y strings)."""
    return type(value) in (int, float)

def to_model_value(field: str, value: Any) -> Any:
    """Convierte un valor del front al formato con el que se entrenó el modelo."""
    if field == "diabetes":
        return 2 if value else 0  # True -> 2, False -> 0
    if field in BOOLEAN_FIELDS:
        return int(value)  # True -> 1, False -> 0
    return value  # age, bmi, physical_health, mental_health no cambian

def validate_evaluation(data: Any) -> dict[str, Any]:
    """Valida las 9 variables. Devuelve solo esos campos o lanza ValidationError."""
    if not isinstance(data, dict):
        raise ValidationError({"body": "Se esperaba un objeto JSON."})

    errors: dict[str, str] = {}

    for field in ALL_FIELDS:
        value = data.get(field)

        # 1. El campo debe venir
        if value is None:
            errors[field] = "Campo obligatorio."
        # 2. Validación según el tipo de campo
        elif field in BOOLEAN_FIELDS:
            if not isinstance(value, bool):
                errors[field] = "Debe ser un booleano (true/false)."
        elif field in FLOAT_FIELDS:
            low, high = FLOAT_FIELDS[field]
            if not _is_number(value):
                errors[field] = "Debe ser un número."
            elif not low <= value <= high:
                errors[field] = f"Debe estar entre {low} y {high}."
        else:  # age, physical_health, mental_health
            low, high = INT_RANGES[field]
            if not _is_int(value):
                errors[field] = "Debe ser un número entero."
            elif not low <= value <= high:
                errors[field] = f"Debe estar entre {low} y {high}."

    if errors:
        raise ValidationError(errors)

    # Nos quedamos solo con las 9 variables (ignora cualquier otro campo)
    return {field: data[field] for field in ALL_FIELDS}


class EvaluationsService:
    def __init__(self, repository=evaluations_repository):
        self.repository = repository

    def create(self, db: Session, payload: Any) -> Evaluations:
        # 1. Validar
        data = validate_evaluation(payload)

        # 2. Renombrar para el modelo y predecir
        features = {
            MODEL_FIELD_NAMES[field]: to_model_value(field, value)
            for field, value in data.items()
        }

        # 3. Predecir (el modelo recibe 0/1 y diabetes como 0/2, igual que en el entrenamiento)
        result = predict_evaluation_model_ml(path_model=settings.PATH_MODEL_ML_PKL ,data=features) ## Función de predicción (LOCAL)
        # 4. Registrar en la BD.
        record = {**data, "result_evaluation": result}
        return self.repository.create(db, record)

    def get(self, db: Session, evaluation_id: int) -> Evaluations:
        evaluation = self.repository.get(db, evaluation_id)
        if evaluation is None:
            raise NotFoundError(f"Evaluación {evaluation_id} no encontrada.")
        return evaluation

    def get_by_uuid(self, db: Session, uuid_evaluation: str) -> Evaluations:
        evaluation = self.repository.get_by_uuid(db, uuid_evaluation)
        if evaluation is None:
            raise NotFoundError(f"Evaluación no encontrada.")
        return schema_evaluation(evaluation=evaluation)

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[Evaluations]:
        limit = min(limit, 500)  # evita traer demasiados registros de golpe
        return schema_list_evaluation(
            self.repository.get_multi(db, skip=skip, limit=limit)
        )

    def delete(self, db: Session, uuid_evaluation: str) -> None:
        if not self.repository.delete_by_uuid(db, uuid_evaluation):
            raise NotFoundError(f"Evaluación no encontrada.")


evaluations_service = EvaluationsService()
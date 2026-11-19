
from flask import Blueprint, jsonify, request
from app.core.config import load_settings
from app.services.evaluations_service import (
    NotFoundError, ValidationError, evaluations_service
)
from app.utils.helpers import parse_uuid, InvalidUUIDError

settings = load_settings()

evaluate_user_bp = Blueprint(
    name="evaluates",
    import_name=__name__,
    url_prefix="/evaluations"
)

from app.db.db import get_db

@evaluate_user_bp.route("/evaluate", methods=["GET","POST"])
def evaluate_user():

## VALIDAR DATOS DE ENTRADA FRENTE AL MODELO DEFINIDO CON LOS ATRIBUTOS

    ## Condición método POST
    if request.method == "POST":
        evaluation = evaluations_service.create(
            db= get_db(), payload= request.get_json()
        )
        message = "Alto riesgo" if evaluation.result_evaluation == 1 else "Bajo riesgo"
        return jsonify({
            "Resultado de evaluación" : message
        }), 201

    ## Condición método GET
    else:
        return jsonify({
            "info": "Evaluate User Endpoint"
        }), 200
    
@evaluate_user_bp.route("/<uuid_evaluation>")
def get_evaluation(uuid_evaluation):
    parsed_uuid = parse_uuid(uuid_evaluation)
    evaluation = evaluations_service.get_by_uuid(get_db(), parsed_uuid)
    return evaluation


@evaluate_user_bp.route("/")
def list_evaluations():
    items = evaluations_service.list_all(get_db())
    return items

@evaluate_user_bp.route("/<uuid_evaluation>", methods=["DELETE"])
def delete_evaluation(uuid_evaluation):
    parsed_uuid = parse_uuid(uuid_evaluation)
    evaluations_service.delete(get_db(), parsed_uuid)

    return jsonify({
        "message": "Evaluación eliminada correctamente",
    }), 200

@evaluate_user_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"errors": e.errors}), 422


@evaluate_user_bp.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": str(e), "status": 404}), 404

@evaluate_user_bp.errorhandler(InvalidUUIDError)
def handle_invalid_uuid(error):
    return jsonify({"error": str(error)}), 400
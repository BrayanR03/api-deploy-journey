import uuid

import pytest

BASE_URL = "/evaluations"

# Clave con la que el service/modelo serializa el identificador.
UUID_KEY = "uuid_evaluation"

# Payload válido.
VALID_PAYLOAD = {
    "age": 45,
    "sex": True,
    "bmi": 27.5,
    "smoker": False,
    "physical_activity": True,
    "physical_health": 3,
    "mental_health": 2,
    "high_cholesterol": False,
    "diabetes": True,
    "high_blood_pressure": False,
}


# ---------------------------------------------------------------------------
# Predicción simulada.
# ---------------------------------------------------------------------------
class PredictionStub:
    def __init__(self):
        self.result = 1
        self.calls = []

    def __call__(self, path_model, data):
        self.calls.append(data)
        return self.result


@pytest.fixture
def prediction(monkeypatch):
    """
    Reemplaza la función de predicción por un stub.
    Se parchea DONDE SE USA (el módulo del service), no donde se define.
    Si tu service la llama distinto, ajusta esta ruta.
    """
    stub = PredictionStub()
    monkeypatch.setattr(
        "app.services.evaluations_service.predict_evaluation_model_ml", stub
    )
    return stub


def create_evaluation(client, payload=None):
    """Crea una evaluación por HTTP y devuelve su UUID (leyéndolo del listado)."""
    response = client.post(f"{BASE_URL}/evaluate", json=payload or dict(VALID_PAYLOAD))
    assert response.status_code == 201
    items = client.get(f"{BASE_URL}/").get_json()
    return items[-1][UUID_KEY]


# ---------------------------------------------------------------------------
# GET /evaluations/evaluate
# ---------------------------------------------------------------------------
def test_evaluate_get_returns_info(client):
    response = client.get(f"{BASE_URL}/evaluate")

    assert response.status_code == 200
    assert response.get_json() == {"info": "Evaluate User Endpoint"}


# ---------------------------------------------------------------------------
# POST /evaluations/evaluate
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "model_result, expected_message",
    [(1, "Alto riesgo"), (0, "Bajo riesgo")],
)
def test_evaluate_post_returns_risk_message(
    client, prediction, model_result, expected_message
):
    prediction.result = model_result

    response = client.post(f"{BASE_URL}/evaluate", json=VALID_PAYLOAD)

    assert response.status_code == 201
    assert response.get_json() == {"Resultado de evaluación": expected_message}


def test_evaluate_post_persists_evaluation(client, prediction):
    client.post(f"{BASE_URL}/evaluate", json=VALID_PAYLOAD)

    items = client.get(f"{BASE_URL}/").get_json()

    assert len(items) == 1


@pytest.mark.parametrize("diabetes_input, diabetes_expected", [(True, 2), (False, 0)])
def test_evaluate_post_converts_diabetes_for_the_model(
    client, prediction, diabetes_input, diabetes_expected
):
    payload = {**VALID_PAYLOAD, "diabetes": diabetes_input}

    client.post(f"{BASE_URL}/evaluate", json=payload)
    assert prediction.calls[0]["Diabetes"] == diabetes_expected


@pytest.mark.parametrize("missing_field", list(VALID_PAYLOAD))
def test_evaluate_post_missing_field_returns_422(client, prediction, missing_field):
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != missing_field}

    response = client.post(f"{BASE_URL}/evaluate", json=payload)

    assert response.status_code == 422
    assert "errors" in response.get_json()
    assert prediction.calls == []  # no se predice si la validación falla


def test_evaluate_post_empty_body_returns_422(client, prediction):
    response = client.post(f"{BASE_URL}/evaluate", json={})

    assert response.status_code == 422
    assert prediction.calls == []


# ---------------------------------------------------------------------------
# GET /evaluations/
# ---------------------------------------------------------------------------
def test_list_evaluations_empty(client):
    response = client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert response.get_json() == []


def test_list_evaluations_returns_created_items(client, prediction):
    create_evaluation(client)
    create_evaluation(client)

    response = client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert len(response.get_json()) == 2


# ---------------------------------------------------------------------------
# GET /evaluations/<uuid>
# ---------------------------------------------------------------------------
def test_get_evaluation_returns_existing(client, prediction):
    uuid_evaluation = create_evaluation(client)

    response = client.get(f"{BASE_URL}/{uuid_evaluation}")

    assert response.status_code == 200
    assert response.get_json()[UUID_KEY] == uuid_evaluation


def test_get_evaluation_not_found_returns_404(client):
    response = client.get(f"{BASE_URL}/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.get_json()["status"] == 404


def test_get_evaluation_invalid_uuid_returns_400(client):
    response = client.get(f"{BASE_URL}/no-es-un-uuid")

    assert response.status_code == 400
    assert "error" in response.get_json()


# ---------------------------------------------------------------------------
# DELETE /evaluations/<uuid>
# ---------------------------------------------------------------------------
def test_delete_evaluation_success(client, prediction):
    uuid_evaluation = create_evaluation(client)

    response = client.delete(f"{BASE_URL}/{uuid_evaluation}")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Evaluación eliminada correctamente"}
    # ya no existe
    assert client.get(f"{BASE_URL}/{uuid_evaluation}").status_code == 404


def test_delete_evaluation_not_found_returns_404(client):
    response = client.delete(f"{BASE_URL}/{uuid.uuid4()}")

    assert response.status_code == 404


def test_delete_evaluation_invalid_uuid_returns_400(client):
    response = client.delete(f"{BASE_URL}/no-es-un-uuid")

    assert response.status_code == 400
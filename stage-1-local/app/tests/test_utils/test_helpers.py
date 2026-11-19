import pickle
import uuid

import pytest

from app.utils.helpers import (
    InvalidUUIDError,
    parse_uuid,
    predict_evaluation_model_ml,
)


# ---------------------------------------------------------------------------
# Modelo falso para no depender del .pkl real
# ---------------------------------------------------------------------------
class FakeModel:
    """Siempre predice el valor indicado y guarda el DataFrame recibido."""

    last_df = None

    def __init__(self, prediction=1):
        self.prediction = prediction

    def predict(self, df):
        FakeModel.last_df = df
        return [self.prediction]


@pytest.fixture
def make_model_file(tmp_path):
    """Crea un .pkl temporal con un FakeModel y devuelve su ruta."""

    def _make(prediction):
        path = tmp_path / "model.pkl"
        with open(path, "wb") as f:
            pickle.dump(FakeModel(prediction), f)
        return path

    return _make


# ---------------------------------------------------------------------------
# predict_evaluation_model_ml
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("prediction", [0, 1])
def test_predict_returns_int_from_model(make_model_file, prediction):
    path = make_model_file(prediction)

    result = predict_evaluation_model_ml(path, {"age": 40, "smoker": 1})

    assert result == prediction
    assert isinstance(result, int)


def test_predict_builds_dataframe_with_one_row_and_same_columns(make_model_file):
    path = make_model_file(1)
    data = {"age": 40, "smoker": 1, "diabetes": 2}

    predict_evaluation_model_ml(path, data)

    df = FakeModel.last_df
    assert list(df.columns) == ["age", "smoker", "diabetes"]
    assert len(df) == 1
    assert df.iloc[0].to_dict() == data


def test_predict_raises_if_model_file_does_not_exist(tmp_path):
    with pytest.raises(FileNotFoundError):
        predict_evaluation_model_ml(tmp_path / "no_existe.pkl", {"age": 40})


# ---------------------------------------------------------------------------
# parse_uuid
# ---------------------------------------------------------------------------
def test_parse_uuid_valid_returns_uuid_object():
    value = "123e4567-e89b-12d3-a456-426614174000"

    parsed = parse_uuid(value)

    assert isinstance(parsed, uuid.UUID)
    assert str(parsed) == value


def test_parse_uuid_accepts_uppercase():
    value = "123E4567-E89B-12D3-A456-426614174000"

    assert parse_uuid(value) == uuid.UUID(value)


@pytest.mark.parametrize(
    "invalid_value",
    [
        "abc",                                          # texto cualquiera
        "",                                             # vacío
        "123",                                          # muy corto
        "123e4567e89b12d3a456426614174000",             # sin guiones
        "{123e4567-e89b-12d3-a456-426614174000}",       # con llaves
        "urn:uuid:123e4567-e89b-12d3-a456-426614174000",  # con prefijo urn
        None,                                           # tipo incorrecto
        123,                                            # tipo incorrecto
    ],
)
def test_parse_uuid_invalid_raises_error(invalid_value):
    with pytest.raises(InvalidUUIDError):
        parse_uuid(invalid_value)
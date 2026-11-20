# Funciones auxiliares compartidas por servicios y blueprints.

import pandas as pd
import pickle
import uuid

## Función de predicción (LOCAL)
def predict_evaluation_model_ml(path_model, data: dict)->int:

    ## Valores que el usuario envía mediante request (diccionario)
    values = list(data.values()) ## Extraemos valores
    columns = list(data.keys())  ## Extraemos columnas

    ## Convertimos a un Dataframe
    df = pd.DataFrame(data=[values], columns=columns)

    ## Leemos el .pkl en formato binary
    with open(file=path_model, mode="rb") as ml:
        model_data = pickle.load(ml)

    ## Utilizamos la función interina .predict()
    """
    .predict() evalúa los datos enviados por el usuario y,
     gracias al proceso de entrenamiento y validación del ML.
    
    Se retorna un valor: [1] - Alto riesgo // [0] - Bajo Riesgo
    """
    result = int(model_data.predict(df)[0])    

    ## Retornamos el resultado
    return result 

## Clase para el manejo de errores con UUID
class InvalidUUIDError(ValueError):
    """El identificador enviado no tiene formato UUID válido."""

## Función para validar el formato del UUID
def parse_uuid(value: str) -> uuid.UUID:
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError, TypeError):
        raise InvalidUUIDError("El identificador no es un UUID válido")

    # uuid.UUID acepta variantes (sin guiones, con llaves, prefijo urn:).
    # Si quieres aceptar solo el formato estándar con guiones:
    if str(parsed) != value.lower():
        raise InvalidUUIDError("El identificador no es un UUID válido")
    return parsed

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "info": "API para la evaluación de riesgo de Infarto de Miocardio",
        "version": "1.0.0",
        "author": "Brayan Neciosup"
    }

from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (organização)

    response = client.get("/")  # Act (ação)

    # Assert (verificação)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}

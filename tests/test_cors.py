from fastapi.testclient import TestClient

from src.turplanlegger.main import app

client = TestClient(app)


def test_invalid_origin():
    headers = {'Origin': 'http://localhost:1337', 'Access-Control-Request-Method': 'GET'}

    response = client.options('/v1', headers=headers)
    assert response.status_code == 400


def test_valid_origin():
    headers = {'Origin': 'http://localhost:3000', 'Access-Control-Request-Method': 'GET'}

    response = client.options('/v1', headers=headers)
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == 'http://localhost:3000'

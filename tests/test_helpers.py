from fastapi.testclient import TestClient
from src.turplanlegger.main import app

client = TestClient(app)


def test_read_main():
    response = client.get('/v1')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}


def test_read_test():
    response = client.get('/v1/test')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

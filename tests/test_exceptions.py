from uuid import uuid4

from fastapi.testclient import TestClient
from pytest import fixture

from src.turplanlegger.main import app
from src.turplanlegger.sql.crud import delete_all_users

from pprint import pprint

client = TestClient(app)

def GET_USER_PRIVATE():
    return {
        'id': str(uuid4()),
        'first_name': 'Petter',
        'last_name': 3,
        'email': 'petter@smart.no',
        'auth_method': 'basic',
        'password': 'test123',
        'private': True,
    }

@fixture()
def clean_users_table():
    yield
    delete_all_users()

def test_create_private_user(clean_users_table):
    USER_PRIVATE = GET_USER_PRIVATE()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    data = response.json()
    print('###############################')
    print('###############################')
    print('###############################')
    pprint(data)
    assert response.status_code == 200

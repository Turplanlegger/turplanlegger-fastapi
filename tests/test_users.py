from uuid import uuid4

from fastapi.testclient import TestClient
from pytest import fixture

from src.turplanlegger.main import app
from src.turplanlegger.sql.crud import delete_all_users

client = TestClient(app)


def GET_USER_PRIVATE():
    return {
        'id': str(uuid4()),
        'first_name': 'Petter',
        'last_name': 'Smart',
        'email': 'petter@smart.no',
        'auth_method': 'basic',
        'password': 'test123',
        'private': True,
    }


def GET_USER_PUBLIC():
    return {
        'id': str(uuid4()),
        'first_name': 'Martin',
        'last_name': 'Harepus',
        'email': 'Martin@harehula.no',
        'auth_method': 'basic',
        'password': 'gulrot',
        'private': False,
    }


@fixture()
def clean_users_table():
    yield
    delete_all_users()


def test_create_private_user(clean_users_table):
    USER_PRIVATE = GET_USER_PRIVATE()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == USER_PRIVATE.get('id')
    assert data['first_name'] == USER_PRIVATE.get('first_name')
    assert data['last_name'] == USER_PRIVATE.get('last_name')
    assert data['email'] == USER_PRIVATE.get('email')
    assert data['private'] == USER_PRIVATE.get('private')
    assert data['deleted'] is False
    assert data.get('delete_time') is None


def test_create_public_user(clean_users_table):
    USER_PUBLIC = GET_USER_PUBLIC()
    response = client.post('/v1/users/', json=USER_PUBLIC)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == USER_PUBLIC.get('id')
    assert data['first_name'] == USER_PUBLIC.get('first_name')
    assert data['last_name'] == USER_PUBLIC.get('last_name')
    assert data['email'] == USER_PUBLIC.get('email')
    assert data['private'] is USER_PUBLIC.get('private')
    assert data['deleted'] is False
    assert data.get('delete_time') is None


def test_create_duplicate_user(clean_users_table):
    USER_PRIVATE = GET_USER_PRIVATE()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 200

    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'User exists'


def test_get_all_users(clean_users_table):
    USER_PUBLIC = GET_USER_PUBLIC()
    response = client.post('/v1/users/', json=USER_PUBLIC)
    assert response.status_code == 200
    USER_PRIVATE = GET_USER_PRIVATE()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 200

    response = client.get('/v1/users/')
    assert response.status_code == 200
    data = response.json()

    assert data[0]['id'] == USER_PUBLIC.get('id')
    assert data[0]['first_name'] == USER_PUBLIC.get('first_name')
    assert data[0]['last_name'] == USER_PUBLIC.get('last_name')
    assert data[0]['email'] == USER_PUBLIC.get('email')
    assert data[0]['private'] is USER_PUBLIC.get('private')
    assert data[0]['deleted'] is False
    assert data[0].get('delete_time') is None

    assert data[1]['id'] == USER_PRIVATE.get('id')
    assert data[1]['first_name'] == USER_PRIVATE.get('first_name')
    assert data[1]['last_name'] == USER_PRIVATE.get('last_name')
    assert data[1]['email'] == USER_PRIVATE.get('email')
    assert data[1]['private'] is USER_PRIVATE.get('private')
    assert data[1]['deleted'] is False
    assert data[1].get('delete_time') is None


def test_delete_user(clean_users_table):
    USER_PUBLIC = GET_USER_PUBLIC()
    response = client.post('/v1/users/', json=USER_PUBLIC)
    assert response.status_code == 200
    USER_PRIVATE = GET_USER_PRIVATE()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 200

    response = client.delete(f"/v1/users/{USER_PRIVATE.get('id')}")
    assert response.status_code == 200

    response = client.get('/v1/users/')
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]['id'] == USER_PUBLIC.get('id')
    assert data[0]['first_name'] == USER_PUBLIC.get('first_name')
    assert data[0]['last_name'] == USER_PUBLIC.get('last_name')
    assert data[0]['email'] == USER_PUBLIC.get('email')
    assert data[0]['private'] is USER_PUBLIC.get('private')
    assert data[0]['deleted'] is False
    assert data[0].get('delete_time') is None


def test_update_user(clean_users_table):
    USER_PUBLIC = GET_USER_PUBLIC()
    response = client.post('/v1/users/', json=USER_PUBLIC)
    assert response.status_code == 200

    response = client.put(
        f"/v1/users/{USER_PUBLIC.get('id')}",
        json={
            'first_name': 'Martin',
            'last_name': 'Haremann',
            'email': None,  # Not updated
            'private': None,  # Not updated
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == USER_PUBLIC.get('id')
    assert data['first_name'] == USER_PUBLIC.get('first_name')
    assert data['last_name'] == 'Haremann'
    assert data['email'] == USER_PUBLIC.get('email')
    assert data['private'] is USER_PUBLIC.get('private')
    assert data['deleted'] is False
    assert data.get('delete_time') is None


def test_get_user(clean_users_table):
    USER_PRIVATE = GET_USER_PRIVATE()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 200
    id = response.json().get('id')

    response = client.get(f'/v1/users/{id}')
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == USER_PRIVATE.get('id')
    assert data['first_name'] == USER_PRIVATE.get('first_name')
    assert data['last_name'] == USER_PRIVATE.get('last_name')
    assert data['email'] == USER_PRIVATE.get('email')
    assert data['private'] == USER_PRIVATE.get('private')
    assert data['deleted'] is False
    assert data.get('delete_time') is None

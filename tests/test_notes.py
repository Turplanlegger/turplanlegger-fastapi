from uuid import uuid4

from fastapi.testclient import TestClient
from pytest import fixture

from src.turplanlegger.main import app
from src.turplanlegger.sql.crud import delete_all_users, delete_all_notes

client = TestClient(app)

USER_PRIVATE = {
        'id': str(uuid4()),
        'first_name': 'Petter',
        'last_name': 'Smart',
        'email': 'petter@smart.no',
        'auth_method': 'basic',
        'private': True,
    }

def GET_NOTE_SHORT():
    return {
        'owner': USER_PRIVATE.get('id'),
        'name': 'Short note',
        'content': 'This is not a long note Petter'
    }


def GET_NOTE_LONG():
    return {
        'owner': USER_PRIVATE.get('id'),
        'name': 'Long note',
        'content': 'This is a long note, it has many many characters. Many more than I can be bothered to write right now'
    }

def GET_NOTE_PUBLIC():
    return {
        'owner': USER_PRIVATE.get('id'),
        'name': 'Private note',
        'content': 'Martin, ensure that this is a private note!!! 🔥🔥',
        'private': False
    }

@fixture(scope="session", autouse=True)
def my_fixture():
    delete_all_users()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 200
    yield
    delete_all_users()

@fixture()
def clean_notes_table():
    yield
    delete_all_notes()


def test_create_short_note(clean_notes_table):
    NOTE = GET_NOTE_SHORT()
    response = client.post('/v1/notes/', json=NOTE)

    data = response.json()
    
    assert response.status_code == 200
    assert isinstance(data['id'], str)
    assert data['content'] == NOTE.get('content')
    assert data['name'] == NOTE.get('name')
    assert data['private'] is True
    assert data['deleted'] is False
    assert data.get('delete_time') is None

def test_create_long_note(clean_notes_table):
    NOTE = GET_NOTE_LONG()
    response = client.post('/v1/notes/', json=NOTE)

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data['id'], str)
    assert data['content'] == NOTE.get('content')
    assert data['name'] == NOTE.get('name')
    assert data['private'] is True
    assert data['deleted'] is False
    assert data.get('delete_time') is None

def test_create_public_note(clean_notes_table):
    NOTE = GET_NOTE_PUBLIC()
    response = client.post('/v1/notes/', json=NOTE)

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data['id'], str)
    assert data['content'] == NOTE.get('content')
    assert data['name'] == NOTE.get('name')
    assert data['private'] is False
    assert data['deleted'] is False
    assert data.get('delete_time') is None
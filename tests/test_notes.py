from uuid import uuid4

from fastapi.testclient import TestClient
from pytest import fixture

from src.turplanlegger.main import app
from src.turplanlegger.sql.crud import delete_all_notes, delete_all_users

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

def GET_NOTE_UPDATES():
    return {
        'name': 'I have a new name',
        'content': 'And a brand new content. And if you watch closely the private key has also been changed 🥸',
        'private': False
    }

@fixture(scope='session', autouse=True)
def my_fixture():
    delete_all_notes()
    delete_all_users()
    response = client.post('/v1/users/', json=USER_PRIVATE)
    assert response.status_code == 200
    yield
    delete_all_notes()
    delete_all_users()

@fixture(scope='function')
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



def test_get_all_notes(clean_notes_table):
    NOTE_SHORT = GET_NOTE_SHORT()
    response = client.post('/v1/notes/', json=NOTE_SHORT)
    assert response.status_code == 200

    NOTE_LONG = GET_NOTE_LONG()
    response = client.post('/v1/notes/', json=NOTE_LONG)
    assert response.status_code == 200

    NOTE_PUBLIC = GET_NOTE_PUBLIC()
    response = client.post('/v1/notes/', json=NOTE_PUBLIC)
    assert response.status_code == 200

    response = client.get('/v1/notes/')
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3

    assert isinstance(data[0]['id'], str)
    assert data[0]['content'] == NOTE_SHORT.get('content')
    assert data[0]['name'] == NOTE_SHORT.get('name')
    assert data[0]['private'] is True
    assert data[0]['deleted'] is False
    assert data[0]['delete_time'] is None

    assert isinstance(data[1]['id'], str)
    assert data[1]['content'] == NOTE_LONG.get('content')
    assert data[1]['name'] == NOTE_LONG.get('name')
    assert data[1]['private'] is True
    assert data[1]['deleted'] is False
    assert data[1]['delete_time'] is None

    assert isinstance(data[2]['id'], str)
    assert data[2]['content'] == NOTE_PUBLIC.get('content')
    assert data[2]['name'] == NOTE_PUBLIC.get('name')
    assert data[2]['private'] is False
    assert data[2]['deleted'] is False
    assert data[2]['delete_time'] is None

def test_get_single_note(clean_notes_table):
    NOTE = GET_NOTE_SHORT()
    response = client.post('/v1/notes/', json=NOTE)

    data = response.json()

    assert response.status_code == 200
    note_id = data['id']

    response = client.get(f'/v1/notes/{note_id}')

    assert response.status_code == 200
    assert isinstance(data['id'], str)
    assert data['content'] == NOTE.get('content')
    assert data['name'] == NOTE.get('name')
    assert data['private'] is True
    assert data['deleted'] is False
    assert data.get('delete_time') is None


def test_get_deleted_note(clean_notes_table):
    NOTE = GET_NOTE_SHORT()

    response = client.post('/v1/notes/', json=NOTE)
    data = response.json()

    assert response.status_code == 200
    note_id = data['id']

    response = client.get(f'/v1/notes/{note_id}')
    assert response.status_code == 200

    response = client.delete(f'/v1/notes/{note_id}')
    assert response.status_code == 204

    response = client.get(f'/v1/notes/{note_id}')
    assert response.status_code == 404

def test_update_note(clean_notes_table):
    NOTE = GET_NOTE_SHORT()
    NOTE_UPDATES = GET_NOTE_UPDATES()

    response = client.post('/v1/notes/', json=NOTE)
    data = response.json()

    assert response.status_code == 200
    note_id = data['id']

    response = client.put(f'/v1/notes/{note_id}', json=NOTE_UPDATES)
    assert response.status_code == 200

    data = response.json()

    assert data['id'] == note_id
    assert data['content'] == NOTE_UPDATES.get('content')
    assert data['name'] == NOTE_UPDATES.get('name')
    assert data['private'] is NOTE_UPDATES.get('private')
    assert data['deleted'] is False
    assert data.get('delete_time') is None

def test_update_note_content(clean_notes_table):
    NOTE = GET_NOTE_SHORT()
    CONTENT = 'A newer version of content, but only content'

    response = client.post('/v1/notes/', json=NOTE)
    data = response.json()

    assert response.status_code == 200
    note_id = data['id']

    response = client.put(
        f'/v1/notes/{note_id}',
        json={
            'content': CONTENT
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == note_id
    assert data['content'] == CONTENT
    assert data['name'] == NOTE.get('name')
    assert data['private'] is True
    assert data['deleted'] is False
    assert data.get('delete_time') is None

def test_update_note_name(clean_notes_table):
    NOTE = GET_NOTE_SHORT()
    NAME = 'A newer version of title, but only title'

    response = client.post('/v1/notes/', json=NOTE)
    data = response.json()

    assert response.status_code == 200
    note_id = data['id']

    response = client.put(
        f'/v1/notes/{note_id}',
        json={
            'name': NAME
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == note_id
    assert data['content'] == NOTE.get('content')
    assert data['name'] == NAME
    assert data['private'] is True
    assert data['deleted'] is False
    assert data.get('delete_time') is None

def test_update_note_remove_attr(clean_notes_table):
    NOTE = GET_NOTE_SHORT()
    NAME = 'A newer version of title, but only title'

    response = client.post('/v1/notes/', json=NOTE)
    data = response.json()

    assert response.status_code == 200
    note_id = data['id']

    response = client.put(
        f'/v1/notes/{note_id}',
        json={
            'content': None,
            'name': None
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == note_id
    assert data['content'] is None
    assert data['name'] is None
    assert data['private'] is True
    assert data['deleted'] is False
    assert data.get('delete_time') is None

def test_update_note_set_public_private(clean_notes_table):
    NOTE_PRIVATE = GET_NOTE_SHORT()
    NOTE_PUBLIC = GET_NOTE_PUBLIC()

    response = client.post('/v1/notes/', json=NOTE_PRIVATE)
    data = response.json()
    assert response.status_code == 200
    note_id = data['id']

    response = client.put(
        f'/v1/notes/{note_id}',
        json={
            'private': False
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == note_id
    assert data['content'] == NOTE_PRIVATE.get('content')
    assert data['name'] == NOTE_PRIVATE.get('name')
    assert data['private'] is False
    assert data['deleted'] is False
    assert data.get('delete_time') is None

    response = client.post('/v1/notes/', json=NOTE_PUBLIC)
    data = response.json()
    assert response.status_code == 200
    note_id = data['id']

    response = client.put(
        f'/v1/notes/{note_id}',
        json={
            'private': True
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == note_id
    assert data['content'] == NOTE_PUBLIC.get('content')
    assert data['name'] == NOTE_PUBLIC.get('name')
    assert data['private'] is True
    assert data['deleted'] is False
    assert data.get('delete_time') is None

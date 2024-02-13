from fastapi.testclient import TestClient
from turplanlegger.main import app
from turplanlegger.sql.models import Users

from sqlmodel import Session, select
from uuid import uuid4

client = TestClient(app)

def test_sql_users():
    user1 = Users(
        id=uuid4(),
        first_name='Martin',
        last_name='MyMan',
        email='myman@martin.com',
    )

    session = client.app.state.db_session
    session.add(user1)
    session.commit()

    statement = select(Users)
    result = session.exec(statement)
    for user in result:
        assert user.first_name == 'Martin'
        assert user.last_name == 'MyMan'
        assert user.email == 'myman@martin.com'

from fastapi.testclient import TestClient
from turplanlegger.main import app
from turplanlegger.sql.database import engine
from turplanlegger.sql.schemas import Users

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
    print(user1)

    session = Session(engine)
    session.add(user1)
    session.commit()

    statement = select(Users)
    print(session.exec(statement))
    assert False
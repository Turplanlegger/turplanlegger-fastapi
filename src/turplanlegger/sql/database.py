
from typing import Optional
from sqlmodel import delete, SQLModel, Session, create_engine


DATABASE_URI = 'postgresql+psycopg://turadm:passord@localhost:5432/turplanlegger?connect_timeout=10&application_name=turplanlegger-fastapi'
DEBUG = True

engine = create_engine(DATABASE_URI, echo=DEBUG)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def empty_table(model: str):
    with Session(engine) as session:
        statement = delete(model)
        result = session.exec(statement)
        session.commit()

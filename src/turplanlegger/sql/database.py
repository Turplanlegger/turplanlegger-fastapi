
from os import environ

from sqlmodel import Session, SQLModel, create_engine, delete

from turplanlegger.utils.config import get_settings

config = get_settings()
DATABASE_URI = config.DATABASE_URI
DEBUG = config.DATABASE_DEBUG

engine = create_engine(DATABASE_URI, echo=DEBUG)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def empty_table(model: type) -> None:
    with Session(engine) as session:
        statement = delete(model)
        session.exec(statement)
        session.commit()

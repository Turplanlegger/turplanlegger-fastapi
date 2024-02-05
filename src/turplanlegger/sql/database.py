from typing import Optional
from sqlmodel import SQLModel, create_engine
from turplanlegger.sql import models

class Database:
  def connect(self):
    engine = create_engine(
      'postgresql+psycopg://turadm:passord@localhost:5432/turplanlegger?connect_timeout=10&application_name=turplanlegger-api',
      echo=True
    )
    SQLModel.metadata.create_all(engine)
    return engine

engine = Database().connect()

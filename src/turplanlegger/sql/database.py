from typing import Optional
from sqlmodel import SQLModel, Session, create_engine
from turplanlegger.sql import models

class Database:
  def __init__(self):
    self.uri = 'postgresql+psycopg://turadm:passord@localhost:5432/turplanlegger?connect_timeout=10&application_name=turplanlegger-fastapi'
    self.debug = True

  def connect(self):
    engine = create_engine(
      self.uri,
      echo=self.debug
    )
    SQLModel.metadata.create_all(engine)
    return engine
  
  def session(self, engine):
    return Session(engine)

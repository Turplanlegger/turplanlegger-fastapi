from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
from schemas import *

class Database:
  def __init__(self,app=None):
    self.app = None
    if app:
      self.init_db

  def connect(self, app):
    engine = create_engine(app.config.get('DATABASE_URI'))
    SQLModel.metadata.create_all(engine)
    

  def _log(self, func_name, query, vars):
    self.logger.debug('\n{stars} {func_name} {stars}\n{query}'.format(
      stars='*' * 20,func_name=func_name, query=self.cur.mogrify(query, vars)))


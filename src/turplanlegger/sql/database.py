from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Database:
  def __init__(self,app=None):
    self.app = None
    if app:
      self.init_db

  def connect(self, app):
    DATABASE_URI = app.config.get('DATABASE_URI')
    engine = create_engine(
      DATABASE_URI, connect_args={"check_same_thread": False}
      )
    SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)
  

  def _log(self, func_name, query, vars):
    self.logger.debug('\n{stars} {func_name} {stars}\n{query}'.format(
      stars='*' * 20,func_name=func_name, query=self.cur.mogrify(query, vars)))

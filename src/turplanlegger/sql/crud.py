from sqlmodel import Session, delete

from .database import engine
from .models import User


def delete_all_users():
    with Session(engine) as session:
        statement = delete(User)
        session.exec(statement)
        session.commit()

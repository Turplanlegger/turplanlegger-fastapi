from sqlmodel import Session, delete, select

from .database import engine
from .models import User


def delete_all_users():
    with Session(engine) as session:
        statement = delete(User)
        session.exec(statement)
        session.commit()


def get_user(db: Session, user_id: str):
    statement = select(User).where(User.id == user_id)
    return db.exec(statement).one_or_none()

def get_user_by_email(db: Session, email: str):
    statement = select(User).where(User.email == email)
    return db.exec(statement).one_or_none()


def delete_user(db: Session, user: User):
    db.delete(user)

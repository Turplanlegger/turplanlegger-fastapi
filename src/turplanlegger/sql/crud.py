from sqlmodel import Session, delete, select

from .database import engine
from .models import User
from .schemas import UserUpdate


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


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def update_user(db: Session, db_user: User, user_updates: UserUpdate):
    updated = False

    for attr_name, attr_value in user_updates.__dict__.items():
        if attr_value is not None and getattr(db_user, attr_name) != attr_value:
            setattr(db_user, attr_name, attr_value)
            updated = True

    if updated is True:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user

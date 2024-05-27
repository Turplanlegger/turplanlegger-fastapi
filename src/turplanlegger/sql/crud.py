from datetime import datetime, UTC
from typing import Sequence
from uuid import UUID

from sqlmodel import Session, delete, select

from .database import engine
from .models import User, UserCreate, UserUpdate, Note, NoteCreate, NoteUpdate

# Users
def delete_all_users() -> None:
    with Session(engine) as session:
        statement = delete(User)
        session.exec(statement)  # type: ignore [call-overload]
        session.commit()


def get_all_users(db: Session) -> Sequence[User]:
    statement = select(User)
    return db.exec(statement).all()


def get_user(db: Session, user_id: UUID) -> User | None:
    statement = select(User).where(User.id == user_id)
    return db.exec(statement).one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.exec(statement).one_or_none()


def create_user(db: Session, user: UserCreate) -> User | None:
    db_user = User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def update_user(db: Session, db_user: User, user_updates: UserUpdate) -> User | None:
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

# Notes
def delete_all_notes() -> None:
    with Session(engine) as session:
        statement = delete(Note)
        session.exec(statement)  # type: ignore [call-overload]
        session.commit()

def create_note(db: Session, note: NoteCreate) -> Note | None:
    db_note = Note.model_validate(note)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_all_notes(db: Session) -> Sequence[Note]:
    statement = select(Note)
    return db.exec(statement).all()

# Remeber to only deliver notes beloging to the requesting user
def get_note(db: Session, note_id: UUID) -> Note | None:
    statement = select(Note).where(Note.id == note_id)
    return db.exec(statement).one_or_none()

def update_note(db: Session, db_note: Note, note_update: NoteUpdate) -> Note | None:
    updated = False

    updated_attrs = note_update.model_dump(exclude_unset=True)

    for attr, value in updated_attrs.items():
        setattr(db_note, attr, value)
        updated = True

    if updated is True:
        setattr(db_note, 'update_time', datetime.now(UTC))
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

    return db_note

def delete_note(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()


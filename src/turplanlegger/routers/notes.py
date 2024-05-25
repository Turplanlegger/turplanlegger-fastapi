from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from pprint import pprint


from ..sql import crud
from ..sql.database import get_session
from ..sql.models import NoteCreate, NoteRead

router = APIRouter(
    tags=['notes'],
    prefix='/notes',
    responses={404: {'description': 'Not found'}},
)


@router.get('/', description='Get all notes', response_model=list[NoteRead])
def all_notes(session: Session = Depends(get_session)):
    db_notes = crud.get_all_notes(session)

    if not db_notes:
        raise HTTPException(status_code=404, detail='No notes found')
    return db_notes


@router.post('/', description='Create a new note', response_model=NoteRead)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    db_note = crud.create_note(db=session, note=note)
    return db_note

@router.get('/{note_id}', description='Get a single note by id', response_model=NoteRead)
def get_note(note_id: UUID, session: Session = Depends(get_session)):
    db_note = crud.get_note(session, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail='Note not found')
    return db_note


# @router.get('/{user_id}', description='Get user by id', response_model=UserRead)
# def get_user(user_id: UUID, session: Session = Depends(get_session)):
#     db_user = crud.get_user(session, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail='User not found')
#     return db_user


# @router.get('/query/', description='Query user by email', response_model=UserRead)
# def query_user(email: str, session: Session = Depends(get_session)):
#     db_user = crud.get_user_by_email(session, email=email)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail='User not found')
#     return db_user


# @router.delete('/{user_id}', description='Delete user by id', status_code=HTTPStatus.NO_CONTENT)
# def delete_user(user_id: UUID, session: Session = Depends(get_session)) -> Response:
#     db_user = crud.get_user(session, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail='User not found')

#     crud.delete_user(session, db_user)

#     return Response(status_code=HTTPStatus.NO_CONTENT.value)


# @router.put('/{user_id}', description='Update user by id', response_model=UserRead)
# def update_user(user_id: UUID, user_updates: UserUpdate, session: Session = Depends(get_session)):
#     db_user = crud.get_user(session, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail='User not found')

#     updated_user = crud.update_user(session, db_user, user_updates)

#     return updated_user

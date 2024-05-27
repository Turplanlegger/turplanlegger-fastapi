from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from ..sql import crud
from ..sql.database import get_session
from ..sql.models import NoteCreate, NoteRead, NoteUpdate

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


@router.delete('/{note_id}', description='Delete single note by id', status_code=HTTPStatus.NO_CONTENT)
def delete_note(note_id: UUID, session: Session = Depends(get_session)) -> Response:
    db_note = crud.get_note(session, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail='Note not found')

    crud.delete_note(session, db_note)

    return Response(status_code=HTTPStatus.NO_CONTENT.value)


@router.put('/{note_id}', description='Update Note by id', response_model=NoteRead)
def update_note(note_id: UUID, note_updates: NoteUpdate, session: Session = Depends(get_session)):
    db_note = crud.get_note(session, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail='Note not found')

    updated_note = crud.update_note(session, db_note, note_updates)

    return updated_note

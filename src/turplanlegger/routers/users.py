from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from ..sql import crud
from ..sql.database import get_session
from ..sql.models import UserCreate, UserRead, UserUpdate

router = APIRouter(
    tags=['users'],
    prefix='/users',
    responses={404: {'description': 'Not found'}},
)


@router.get('/', description='Get all users')
def all_users(session: Session = Depends(get_session)) -> list[UserRead]:
    db_users = crud.get_all_users(session)
    if not db_users:
        raise HTTPException(status_code=404, detail='No users found')
    return db_users


@router.post('/', description='Create a new user')
def create_user(user: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    db_user = crud.get_user_by_email(session, email=user.email)
    if db_user is not None:
        raise HTTPException(status_code=400, detail='User exists')

    db_user = crud.create_user(db=session, user=user)
    return db_user


@router.get('/{user_id}', description='Get user by id')
def get_user(user_id: UUID, session: Session = Depends(get_session)) -> UserRead:
    db_user = crud.get_user(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.get('/query/', description='Query user by email')
def query_user(email: str, session: Session = Depends(get_session)) -> UserRead:
    db_user = crud.get_user_by_email(session, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.delete('/{user_id}', description='Delete user by id', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: UUID, session: Session = Depends(get_session)) -> Response:
    db_user = crud.get_user(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    crud.delete_user(session, db_user)

    return Response(status_code=HTTPStatus.NO_CONTENT.value)


@router.put('/{user_id}', description='Update user by id')
def update_user(user_id: UUID, user_updates: UserUpdate, session: Session = Depends(get_session)) -> UserRead:
    db_user = crud.get_user(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    updated_user = crud.update_user(session, db_user, user_updates)

    return updated_user

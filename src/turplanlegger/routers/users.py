from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel import Session

from ..sql.models import User
from ..sql.database import get_session
from ..__about__ import __version__

router = APIRouter(
    tags=['users'],
    prefix='/users',
    responses={404: {'description': 'Not found'}},
)

@router.get('/', description='Get all users', response_model=list[User])
async def all_users(session: Session = Depends(get_session)):
    result = session.exec(select(User))
    return [
        User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            private=user.private,
            create_time=user.create_time,
            deleted=user.deleted,
            delete_time=user.delete_time
        ) for user in result
    ]

@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        auth_method=user.auth_method,
        hashed_password=user.password,
        private=user.private
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

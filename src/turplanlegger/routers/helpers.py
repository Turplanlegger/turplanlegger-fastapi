from fastapi import APIRouter

from ..__about__ import __version__

router = APIRouter(
    tags=['helpers'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', description='Nothing to see here')
async def root():
    return {'message': 'Hello World'}


@router.get('/test', description='Test if the API replies')
async def test():
    return {'status': 'ok'}


@router.get('/version', description='Gets the current version of the API')
async def get_version():
    return {'version': __version__}

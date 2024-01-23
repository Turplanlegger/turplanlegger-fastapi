from fastapi import APIRouter
from turplanlegger.__about__ import __version__


router = APIRouter(
    prefix="",
    tags=["helpers"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", description="Nothing to see here")
async def root():
    return {"message": "Hello World"}

@router.get('/test', description="Returns OK if API is running")
async def test():
    return {"status": "ok"}


@router.get('/version', description="Gets the current version of the API")
async def get_version():
    return {"version": __version__}

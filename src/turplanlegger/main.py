from fastapi import FastAPI

from .__about__ import __version__
from .routers import helpers, users
from .sql.database import init_db


def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version=__version__,
    )

    app_.include_router(helpers.router, prefix='/v1')
    app_.include_router(users.router, prefix='/v1')

    init_db()


app = create_app()

import fastapi
from fastapi import FastAPI
from .__about__ import __version__
from .routers import helpers


def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version=__version__,
    )
    init_routers(app_=app_)

    return app_


def init_routers(app_: FastAPI):
    app_.include_router(
        helpers.router,
        prefix='/v1'
    )


app = create_app()

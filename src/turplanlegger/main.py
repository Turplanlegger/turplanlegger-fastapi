import fastapi
from fastapi import FastAPI
from functools import lru_cache
from turplanlegger.__about__ import __version__
from turplanlegger.config.config import Settings
from turplanlegger.routers import helpers



def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version=__version__,
    )
    init_routers(app_=app_)

    return app_


def init_routers(app_: fastapi):
    app_.include_router(
        helpers.router,
        prefix='/v1'
    )

@lru_cache
def get_settings():
    return Settings()

app = create_app()

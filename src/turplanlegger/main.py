import fastapi
from fastapi import FastAPI
<<<<<<< HEAD
from functools import lru_cache
from turplanlegger.__about__ import __version__
from turplanlegger.routers import helpers

from turplanlegger.config.config import Settings


=======
from turplanlegger.__about__ import __version__
from turplanlegger.routers import helpers

>>>>>>> main

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

<<<<<<< HEAD
@lru_cache
def get_settings():
    return Settings()
=======
>>>>>>> main

app = create_app()

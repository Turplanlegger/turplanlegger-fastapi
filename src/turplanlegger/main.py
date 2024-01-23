from fastapi import FastAPI
import fastapi

from turplanlegger.routers import helpers
from turplanlegger.__about__ import __version__

def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version=__version__,
    )
    init_routers(app_=app_)

    return app_

def init_routers(app_: fastapi):
    app_.include_router(helpers.router)


app = create_app()


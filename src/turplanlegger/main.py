from fastapi import FastAPI
import fastapi

from turplanlegger.routers import helpers

def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version='1.0.0',
    )
    init_routers(app_=app_)

    return app_

def init_routers(app_: fastapi):
    app_.include_router(helpers.router)


app = create_app()


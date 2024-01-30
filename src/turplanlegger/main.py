import fastapi
from fastapi import FastAPI
from turplanlegger.__about__ import __version__
from turplanlegger.routers import helpers


from turplanlegger.config.config import Settings



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

settings =  Settings()
print(settings.DATABASE_URI)

app = create_app()

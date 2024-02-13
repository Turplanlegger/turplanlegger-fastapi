import fastapi
from fastapi import FastAPI
from sqlmodel import SQLModel
from turplanlegger.__about__ import __version__
from turplanlegger.routers import helpers
from turplanlegger.sql.database import Database


def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version=__version__,
    )
    init_routers(app_=app_)
    init_db(app_=app_)

    return app_


def init_routers(app_: fastapi):
    app_.include_router(
        helpers.router,
        prefix='/v1'
    )

def init_db(app_: fastapi):
    db = Database()

    app_.state.db_engine = db.connect()
    app_.state.db_session = db.session(app_.state.db_engine)


app = create_app()

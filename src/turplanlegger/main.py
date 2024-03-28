from fastapi import FastAPI

from .__about__ import __version__
from .routers import helpers, users
from .sql.database import init_db
from .exception import register_problem_exception_handler


def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version=__version__,
    )

    register_problem_exception_handler(app_)

    app_.include_router(helpers.router, prefix='/v1')
    app_.include_router(users.router, prefix='/v1')

    init_db()

    return app_


app = create_app()

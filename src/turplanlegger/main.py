from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.config import get_settings
from .__about__ import __version__
from .routers import helpers, users
from .sql.database import init_db

config = get_settings()

def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Turplanlegger',
        description='Turplanlegger API',
        version=__version__,
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app_.include_router(helpers.router, prefix='/v1')
    app_.include_router(users.router, prefix='/v1')

    init_db()

    return app_


app = create_app()

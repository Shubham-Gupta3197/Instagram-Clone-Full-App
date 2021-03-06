from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.config import settings
from db.session import engine
from db.base_class import Base
from api.base import api_routers


def configure_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount('/images', StaticFiles(directory='images'), name='images')
    app.include_router(api_routers)
    Base.metadata.create_all(bind=engine)
    return app


app = configure_application()

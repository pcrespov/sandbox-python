from fastapi import FastAPI
from pydantic import BaseSettings
from . import api
from .settings import AppSettings


# application.py ---

def create_app():
    app = FastAPI(docs_url="/", title="API concept for dynamic-sidecar")
    app.include_router(api.router)

    app.state.settings = AppSettings()
    
    return app
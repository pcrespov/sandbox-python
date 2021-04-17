from fastapi import FastAPI
from pydantic import BaseSettings
from . import api

# settings.py ----
class AppSettings(BaseSettings):
    debug: bool = False

    # etc
    class Config:
        case_sensitive = False
        env_prefix = "DYNAMIC_SIDECAR_"


# application.py ---


def create_app():
    app = FastAPI(docs_url="/", title="API concept for dynamic-sidecar")
    app.include_router(api.router)

    app.state.settings = AppSettings()

    return app

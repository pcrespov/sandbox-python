from fastapi import Request, FastAPI
from fastapi.applications import State
from fastapi.param_functions import Depends
from .settings import AppSettings


def get_app(request: Request) -> FastAPI:
    return request.app


def get_app_state(app: FastAPI = Depends(get_app)) -> State:
    return app.state


def get_settings(app_data: State = Depends(get_app_state)) -> AppSettings:
    return app_data.settings

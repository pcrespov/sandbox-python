import logging
from typing import Optional
from pydantic import BaseSettings
from fastapi import Depends, FastAPI, HTTPException, Request, status
from server_utils import log_fun, emulate

import asyncio

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def get_app(request: Request) -> FastAPI:
    return request.app


class Settings(BaseSettings):
    ON_STARTUP_IS_HEALTHY: bool = True
    ON_STARTUP_RAISE_ERROR: bool = False
    ON_STARTUP_DELAY: int = 0
    ON_STARTUP_ORPHAN_TASK: str = ""

    ON_SHUTDOWN_RAISE_ERROR: bool = False
    ON_SHUTDOWN_DELAY: int = 0
    ON_SHUTDOWN_ORPHAN_TASK: str = ""


app = FastAPI()

settings = Settings()
log.info(settings.json(indent=2))


# events ---------------------------------------


@app.on_event("startup")
@log_fun(log.info)
async def startup_event():
    await emulate(
        raise_error=settings.ON_STARTUP_RAISE_ERROR,
        delay=settings.ON_STARTUP_DELAY,
        orphan_task=settings.ON_STARTUP_ORPHAN_TASK,
    )
    app.state.is_healthy = settings.ON_STARTUP_IS_HEALTHY


@app.on_event("shutdown")
@log_fun(log.info)
async def shutdown_event():
    await emulate(
        raise_error=settings.ON_SHUTDOWN_RAISE_ERROR,
        delay=settings.ON_SHUTDOWN_DELAY,
        orphan_task=settings.ON_SHUTDOWN_ORPHAN_TASK,
    )


# routes ----------------------------------------
#
# unknown route -> auto respond 404
#


@app.get("/")
def get_healthcheck(request: Request):
    if not request.app.state.is_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="ko"
        )
    return "ok"


@app.get("/hi")
def get_salute():
    return "hoi zaeme"


@app.post("/error")
def create_error(code: Optional[int] = None):
    if code is None:
        raise RuntimeError()  # Automatically translates into 500
    raise HTTPException(code=status)


@app.post("/state")
def set_state(is_healthy: bool, app: FastAPI = Depends(get_app)):
    app.state.is_healthy = is_healthy

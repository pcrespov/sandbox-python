#
# unknown path -> automatically into 404
#
from functools import wraps

from fastapi import Depends, FastAPI, HTTPException, Request, status
from server_utils import print_start_and_end


def get_app(request: Request) -> FastAPI:
    return request.app


app = FastAPI()

# events ---------------------------------------
@app.on_event("startup")
@print_start_and_end
async def startup_event():
    app.state.is_healthy = False


@app.on_event("shutdown")
@print_start_and_end
async def shutdown_event():
    ...


# routes ----------------------------------------
@app.get("/")
def get_healthcheck(request: Request):
    if not request.app.state.is_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="ko"
        )
    return "ok"


@app.get("/hi")
def get_hoi():
    return "hoi zaeme"


@app.post("/raise")
def raise_unhandle_exception():
    # Automatically translates into 500
    raise RuntimeError("failed")


@app.post("/state")
def set_state(is_healthy: bool, app: Depends(get_app)):
    app.state.is_healthy = is_healthy

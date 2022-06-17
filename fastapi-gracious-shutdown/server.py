#
# unknown path -> automatically into 404
#
from functools import wraps

from fastapi import Depends, FastAPI, HTTPException, Request, status


def print_start_and_end(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Starting {func.__name__:r} ...")
        try:
            res = await func(*args, **kwargs)
        finally:
            print(f"Completed {func.__name__:r}")
        return res

    return wrapper


def get_app(request: Request) -> FastAPI:
    return request.app


app = FastAPI()

# events ---------------------------------------
@app.on_event("startup")
@print_start_and_end
async def startup_event():
    app.state.is_infected = False


@app.on_event("shutdown")
@print_start_and_end
async def shutdown_event():
    ...


# routes ----------------------------------------
@app.get("/")
def get_healthcheck(request: Request):
    if request.app.state.is_infected:
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
def set_state(is_infected: bool, app: Depends(get_app)):
    app.state.is_infected = is_infected

from dataclasses import dataclass
from typing import Dict, Callable

from fastapi import Depends, FastAPI, Request

app = FastAPI()
app.state.foo = {"x": 33, "y": 55}


# cache??
# https://github.com/tiangolo/fastapi/issues/1635#issuecomment-739537045
#
# That cache is only used per-request. It only avoids, for example, getting the user from DB several times in dependencies and sub-dependencies to handle a single request.
#
# But all that will be executed again for the next request. So it's fine to leave it. You should set use_cache=False only when you have some specific reason to make a dependency function execute more than once in a single request.
#
# In fact, I have never found a real use case for it. I thought there would be one at some point, but it hasn't happened so far. 🤷
#

def get_app(request: Request):
    return request.app


def get_app_value() -> Callable:
    print("get_app_value")
    def _get():
        return {"x": 33, "y": 55}
    return _get

def get_value() -> Dict:
    print("get_value")
    return {"x": 33, "y": 55}


@app.get("/it")
async def getit(
    data: Dict = Depends(get_value), same: Dict = Depends(get_value), 
):
    # is it always the same instance PER request !
    print("data", data, ":", id(data))
    print("same", same, ":", id(same))

    assert id(data) == id(same)
    assert data is same
    assert data is not {"x": 33, "y": 55}

# uvicorn dependency_injection_caching:app --reload

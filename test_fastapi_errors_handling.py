#
# https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
#

import http
from typing import Any

import pytest
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


class ErrorModel(BaseModel):
    name: str = Field(..., description="Standarized error name/code")
    detail: Any | None = Field(None, description="Further details on the error")
    message: str = Field(..., description="Human readable error message")


#
# Exception Handers: handler exception and return a Response
#


async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    error = ErrorModel(
        name=f"{exc.status_code}",
        message=exc.headers.get("X-Message")
        or http.HTTPStatus(exc.status_code).description,
        detail=exc.detail,
    )
    return JSONResponse(jsonable_encoder(error), status_code=exc.status_code)


app = FastAPI()

# register them in the app
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_event_handler(UnicornException, unicorn_exception_handler)


@app.get("/error")
async def _fail():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="A conflict",
        headers={"X-Error": "There goes my error"},
    )


@app.get("/code/{code}")
async def _code(code: int):
    raise HTTPException(
        status_code=code, detail={"code": code, "message": "Failed with code"}
    )
    # When raising an HTTPException, you can pass any value that can be converted to JSON as the parameter detail, not only str.
    # You could pass a dict, a list, etc. They are handled automatically by FastAPI and converted to JSON.


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


def test_handling_unicorn_exception():
    with TestClient(app) as client:
        response = client.get("/unicorns/yolo")
        assert response.status_code == status.HTTP_418_IM_A_TEAPOT


@pytest.mark.skip
@pytest.mark.parametrize("code", [e.value for e in http.HTTPStatus])
def test_handling_http_exception_raised(code: int):
    with TestClient(app) as client:
        response = client.get(f"/code/{code}")

        assert response.status_code == code
        model = ErrorModel(**response.json())

        assert model.name == f"{code}"

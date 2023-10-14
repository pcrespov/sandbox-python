import http
from typing import Any

import pytest
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class DefaultErrorModel(BaseModel):
    error: str = Field(..., description="Standarized error name/code")
    detail: Any | None = Field(None, description="Further details")
    message: str = Field(..., description="Human readable error message")


async def http_exception_as_json_response(
    request: Request, exc: HTTPException
) -> JSONResponse:
    status_code = http.HTTPStatus(exc.status_code)
    assert (
        status_code.phrase == exc.detail
    )  # defined in starlette.exceptions.HTTPException

    error = DefaultErrorModel(
        error=f"{exc.status_code}",
        message=status_code.description,
        detail=exc.detail,
    )
    return JSONResponse(jsonable_encoder(error), status_code=exc.status_code)


app = FastAPI()
app.add_exception_handler(HTTPException, http_exception_as_json_response)


@app.get("/error")
async def _fail():
    raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@app.get("/code/{code}")
async def _code(code: int):
    raise HTTPException(status_code=code)


@pytest.mark.parametrize("code", [e.value for e in http.HTTPStatus])
def test_it(code: int):
    with TestClient(app) as client:
        response = client.get(f"/code/{code}")

        assert response.status_code == code
        model = DefaultErrorModel(**response.json())

        assert model.error == f"{code}"

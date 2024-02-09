#
# https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
#

import http
from typing import Any, Iterator

import pytest
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from toolz.dicttoolz import get_in


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


class ResponseErrorModel(BaseModel):
    name: str | None = Field(None, description="Error code to completent status code")
    detail: Any | None = Field(None, description="Further details on the error")


#
# Exception Handers: handler exception and return a Response
#


async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # the idea here is to return in `got` the value that failed or nothing if e.g. it was missing
    detail = []
    for err in exc.errors():
        _param, *_path = err["loc"]
        match _param:
            case "body":
                err["got"] = get_in(_path, exc.body)
            case "query":
                err["got"] = get_in(_path, request.query_params)
            case "path":
                err["got"] = get_in(_path, request.path_params)
        detail.append(err)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": detail}, exclude_none=True),
    )


class Item(BaseModel):
    title: str
    size: int


app = FastAPI()

# register them in the app
app.add_exception_handler(UnicornException, unicorn_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


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


@app.post("/items/")
async def create_item(item: Item, q: int | None = None):
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="Nope! I don't like 3."
        )
    return {"item_id": item_id}


######################


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as _client:
        yield _client


@pytest.mark.skip
def test_validation_exception_handler_with_body_info(client: TestClient):

    response = client.get("/items/3")
    assert response.status_code == status.HTTP_418_IM_A_TEAPOT

    response = client.get("/items/fooo")
    error = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert error["detail"][0] == {
        "got": "fooo",
        "loc": ["path", "item_id"],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    }
    assert error.get("body") is None

    # cannot process one or more parts of the request
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # how many?
    assert len(error["detail"]) == 1

    # path, query or body?
    assert get_in(["detail", 0, "loc", 0], error) == "path"

    # which parameter?
    assert get_in(["detail", 0, "loc", 1], error)

    # what type of error and what happen?
    assert get_in(["detail", 0, "type"], error)
    assert get_in(["detail", 0, "msg"], error)


def test_multiple_errors(client: TestClient):
    response = client.post("/items/", json={"size": 33}, params={"q": "wrong"})
    error = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # how many?
    assert len(error["detail"]) == 2

    # path, query or body?
    for err in error["detail"]:
        match err["loc"][0]:
            case "body":
                assert err == {
                    "loc": ["body", "title"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            case "query":
                assert err == {
                    "loc": ["query", "q"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                    "got": "wrong",
                }
            case _:
                assert False, f"{err}"


def test_type_error_in_body(client: TestClient):
    response = client.post("/items/", json="not_json")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error = response.json()
    assert len(error["detail"]) == 1
    assert get_in(["detail", 0], error) == {
        "loc": ["body"],
        "msg": "value is not a valid dict",
        "type": "type_error.dict",
        "got": "not_json",
    }


def test_missing_body(client: TestClient):
    response = client.post("/items/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error = response.json()
    assert len(error["detail"]) == 1
    assert get_in(["detail", 0], error) == {
        "loc": ["body"],
        "msg": "field required",
        "type": "value_error.missing",
    }


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
        model = ResponseErrorModel(**response.json())

        assert model.name == f"{code}"

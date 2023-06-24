from typing import Annotated

import httpx
import uvicorn
from faker import Faker
from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination, paginate
from fastapi_pagination.limit_offset import LimitOffsetPage, LimitOffsetParams

# Includes HATEOAS https://apiguide.readthedocs.io/en/latest/build_and_publish/hateos.html
from fastapi_pagination.links import Page
from pydantic import BaseModel, Field

app = FastAPI()


class UserOut(BaseModel):
    name: str = Field(..., example="Steve")
    surname: str = Field(..., example="Rogers")


faker = Faker()

users = [  # create some data
    # ...
    UserOut(name=faker.first_name(), surname=faker.last_name())
    for n in range(500)
]


@app.get("/users", response_model=Page[UserOut])
async def get_users_with_page_number():
    """Uses page-number pagination: fixed pages"""
    return paginate(users)  # use paginate function to paginate your data


@app.get("/users2", response_model=LimitOffsetPage[UserOut])
async def get_users_with_limit_and_offset():
    """Uses limit-offset pagination: link a moving window"""
    return paginate(users)  # use paginate function to paginate your data


@app.get("/users3", response_model=LimitOffsetPage[UserOut])
async def get_users_from_users2(page_params: Annotated[LimitOffsetParams, Depends()]):
    print(page_params)
    page = httpx.get("http://127.0.0.1:8000/users2")
    print(page)


add_pagination(app)  # important! add pagination to your app


if __name__ == "__main__":
    # uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)

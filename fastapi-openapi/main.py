from typing import Annotated

from fastapi import Depends, FastAPI, Query
from pydantic import AnyUrl, BaseModel, Field, conint

# from pydantic.utils import generate_model_signature
# generate_model_signature(ParamsModel)


class BodyModel(BaseModel):
    """Describes Model"""

    foo: int


class StuffGet(BaseModel):
    """Describes response"""

    number: conint(gt=33)
    link: AnyUrl  # <<<---- ISSUE with these types


def get_model(
    param: Annotated[int, Query(description="describes param", le=3)] = 2,
    query: Annotated[int, Query(description="describes query", ge=2)] = 3,
):
    return None


class ParamsModel(BaseModel):
    param: Annotated[int, Field(description="describes param", le=3)] = 2
    query: Annotated[int, Query(description="describes query", ge=2)] = 3


app = FastAPI()


@app.post("/stuff", response_model=StuffGet)
async def get_stuff(
    body: BodyModel,
    # params=Depends(get_model),
    params: Annotated[ParamsModel, Depends()],
):
    print(f"{params=}")
    # print(f"{query=}")
    print(f"{body=}")

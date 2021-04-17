from fastapi import FastAPI, APIRouter

from pydantic import BaseModel
from typing import Dict, Any


# models ---------------


class ComposeFile(BaseModel):
    # https://docs.docker.com/compose/compose-file/
    # https://github.com/compose-spec/compose-spec/blob/master/spec.md
    #
    # SEE https://github.com/compose-spec/compose-spec/blob/master/schema/compose-spec.json
    #
    # https://github.com/docker/compose
    #
    __root__: Dict[str, Any]


# routes ---------------

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    responses={404: {"description": "Container not found"}},
)

## standard: https://cloud.google.com/apis/design/standard_methods

@router.post("/")
def create(docker_compose: Dict):
    print(f"docker-compose config -f |< {docker_compose}")
    print(f"docker-compose config -f {docker_compose}")


@router.get("/")
def list_():
    pass


@router.get("/{id}")
def read(id):
    pass


@router.patch("/{id}", include_in_schema=False)
def update(id):
    pass


@router.delete("/{id}", include_in_schema=False)
def delete(id):
    pass


## custom: https://cloud.google.com/apis/design/custom_methods

@router.post("/{id}:up")
def up(id):
    print("(pull containers)")
    print("create containers")
    print("start containers")


@router.post("/{id}:down")
def down(id):
    print("stop containers")
    print("remove containers")



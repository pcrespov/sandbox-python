from typing import Dict, List, Optional

from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp_swagger import setup_swagger
from pydantic import BaseModel

routes = web.RouteTableDef()


# TODO: template create from openapi specs
#
# Here we explore different ways to doc the aiohttp
#  - could start with OAS, copy reqs and then implement them ...
#


class User(BaseModel):
    id: int
    name: str
    surname: str


def ping_impl(user_id: int) -> User:
    return User(id=user_id, name="pedro", surname="crespo")


@routes.get("/user/{user_id}", name=f"{__name__}.get_user")
async def get_user(request):
    """Below is like a pieces of the OAS in yaml
    ---
    title: Get User
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: int
    responses:
        "200":
          description: returns user if found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
    """
    user_id = request.match_info["user_id"]
    body = ping_impl(user_id)
    return json_response(body.dict())


@routes.get("/ping/default", name=f"{__name__}.ping_default")
@routes.get("/ping/{id}", name=f"{__name__}.ping")
async def ping(request):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """
    return web.Response(text=f"pong { request.match_info.get('id', 'default') }")


models_classes = [
    User,
]


app = web.Application()
app.add_routes(routes)

setup_swagger(
    app,
    swagger_url="/dev/doc",
    # does not require file. can deduce from app
    ui_version=3,
    definitions={m.__name__: m.schema() for m in models_classes},
)

web.run_app(app, port=5000)

from uuid import UUID

import aiohttp_debugtoolbar
from aiohttp import web
from pydantic import BaseModel, ValidationError

RQT_USERID_KEY = f"{__name__}.user_id"
APP_KEYS_MAP = {"user_id": RQT_USERID_KEY}


class BaseRequestParametersModel(BaseModel):
    @classmethod
    def from_request(cls, request: web.Request, app_keys_map: dict[str, str]):
        """
        :raises HTTPErrors if validation fails
        """
        data = {
            **request.match_info,
            **request.query,
            **{
                field_name: request.app[app_key]
                for field_name, app_key in app_keys_map.items()
            },
        }
        try:
            return cls.parse_obj(data)
        except ValidationError as err:
            # TODO: impove error. which parameter failed and why?
            # NOTE: user_id should not be raised as badrequest
            raise web.HTTPBadRequest(reason=f"Invalid query parameters: {err}")


class _TestParameters(BaseRequestParametersModel):
    user_id: int
    project_uuid: UUID
    is_ok: bool = True


async def handler(request: web.Request):
    __doc__ = _TestParameters.schema_json()

    p = _TestParameters.from_request(request, app_keys_map=APP_KEYS_MAP)

    print(p)
    return web.Response( body=p.json(exclude={"user_id"}) )



app = web.Application()
aiohttp_debugtoolbar.setup(app)

app[RQT_USERID_KEY] = 0

app.add_routes([web.get("/test/{project_uuid}", handler)])


if __name__ == "__main__":
    print("SEE http://localhost:8000/_debugtoolbar")
    web.run_app(app)

    
# https://github.com/aio-libs/aiohttp-devtools
# adev runserver <app-path>

import inspect

from aiohttp import web
from aiohttp.web_middlewares import middleware
from aiohttp.web_routedef import route

# import aiohttp_debugtoolbar


routes = web.RouteTableDef()


@routes.get("/", name="home")
async def home(request):
    return web.Response(text="hoi zaeme")


@routes.get("/prj/{pid}", name="get_prj")
async def get_prj(request: web.Request):
    data = {"pid": request.match_info["pid"]}
    print(inspect.currentframe().f_code.co_name, request, "with", data)
    return web.json_response(data)


@routes.post("/prj/{pid}", name="set_prj")
async def set_prj(request: web.Request):
    data = {"pid": request.match_info["pid"]}
    print(inspect.currentframe().f_code.co_name, request, "with", data)
    return web.json_response(data)


@middleware
async def pid_resolver(request: web.Request, handler):
    if str(request.rel_url).startswith("/prj"):
        # change pid
        new_pid = int(request.match_info["pid"]) + 1
        request.match_info["pid"] = str(new_pid)
        # change request
        # new_url = request.match_info.route.get_info()["formatter"].format(pid=new_pid)
        # request = request.clone(rel_url=new_url)
    return await handler(request)


app = web.Application(middlewares=[pid_resolver])
# aiohttp_debugtoolbar.setup(app)

app.add_routes(routes)

# app.add_routes(
#     [
#         web.get("/", home, name="home"),
#         web.get("/one/{pid}", two, name="two"),
#         # web.get("/projects/{pid}", two, name="projects"),
#     ]
# )

if __name__ == "__main__":
    web.run_app(app)

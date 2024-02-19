import socketio
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/home")
async def home(request: web.Request):
    assert request
    return web.Response(text="Home")


def create_app():
    # SEE https://python-socketio.readthedocs.io/en/latest/server.html#aiohttp
    sio = socketio.AsyncServer(
        async_mode="aiohttp",
        cors_allowed_origins=[
            "http://0.0.0.0:8080",
            "https://admin.socket.io",
        ],
    )
    sio.instrument(
        auth={
            "username": "admin",
            "password": "adminadmin",
        }
    )

    app = web.Application()
    app.router.add_routes(routes)
    sio.attach(app, socketio_path="socket.io")
    return app


if __name__ == "__main__":
    print("Open https://admin.socket.io")
    print("user=admin, password=adminadmin")
    web.run_app(create_app())

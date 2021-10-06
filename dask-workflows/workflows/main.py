# Emulate a workflows service

import json
from collections import defaultdict
from contextlib import suppress
from datetime import datetime

import dask
from dask.distributed import Client
from services import add, dec, inc

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import FileResponse, PlainTextResponse

# DATA persists model states
flows = defaultdict(dict)  # flows[session_id][flow_id] = collection of dask.delayed
runs = defaultdict(lambda: defaultdict(list))  # runs[session_id][flow_id][idx]


# workflow business logic
def create_workflow(workbench=None):
    x = dask.delayed(inc)(1)
    y = dask.delayed(dec)(2)
    z = dask.delayed(add)(x, y)
    flow = [x, y, z]
    # WARNING: notice that we keep these in memory!
    # which means that the data is kept. Perhaps that could
    # be the difference between a run and a flow?
    return flow


# http API
router = APIRouter()


def get_app(request: Request) -> FastAPI:
    return request.app


@router.get("/", response_class=PlainTextResponse)
async def health(app: FastAPI = Depends(get_app)):
    return f"{datetime.now().isoformat()}@{__file__}"


@router.get("/meta")
async def meta(app: FastAPI = Depends(get_app)):
    info = {
        "file": __file__,
        "snapshot": datetime.now().isoformat(),
    }
    with suppress(AttributeError):
        c = app.state.dask_client
        info["dashboard-link"] = c.dashboard_link
        info["installed"] = await c.get_versions()

    return info


@router.post("/workflow")
def create(user_id: int, project_id: str):
    flow = create_workflow(workbench=None)
    flows[user_id][project_id] = flow


@router.get("/workflow/{workflow_id}")
def get(user_id: int, workflow_id: str):
    flow = flows[user_id][workflow_id]


@router.get("/workflow/{workflow_id}/view")
def graph_view(user_id: int, workflow_id: str):
    flow = flows[user_id][workflow_id]
    dask.visualize(flow, filename="tmp.png", rankdir="LR", verbose=True)
    return FileResponse("tmp.png")


@router.post("/workflow/{workflow_id}:run")
def run(user_id: int, workflow_id: str):
    flow = flows[user_id][workflow_id]
    run = dask.persist(*flow)
    runs[user_id][workflow_id].append(run)
    return {"count": len(runs[user_id][workflow_id])}


# MAIN -----
app = FastAPI()


@app.on_event("startup")
async def setup_dask():
    with suppress(OSError):
        client = await Client(asynchronous=True)

    # TODO: should be session-based ??
    # with suppress(Exception):
    #     # client = await Client(asynchronous=True)
    #     client = await Client(
    #         name=f"app.state.dask_client", asynchronous=True
    #     )
    #     print(await client.get_versions(check=True))
        app.state.dask_client = client


@app.on_event("shutdown")
def teardown_dask():
    if getattr(app.state, "dask_client", None):
        print("done")
        app.state.dask_client.close()


app.include_router(router)

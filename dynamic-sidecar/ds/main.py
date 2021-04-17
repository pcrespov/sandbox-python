from fastapi import FastAPI, APIRouter

from . import containers



## uvicorn ds.main:app --reload --host=0.0.0.0
app = FastAPI(docs_url="/dev/doc")
app.include_router(containers.router)

from fastapi import FastAPI, Routes

routes = Routes()

@routes.get("/health")
async def health():
    return None

@routes.get("/status")
async def status():
    return None



app = FastAPI()
app.add_route(routes)

# uvicorn api-server:app --host 0.0.0.0
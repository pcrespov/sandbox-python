from fastapi import FastAPI, Path, Query

from typing import Optional

app = FastAPI()


@app.get("/catalog/services/sleeper/2.0.1")
def get_sleeper():
    pass






@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
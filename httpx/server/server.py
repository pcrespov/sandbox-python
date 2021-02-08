import asyncio
from pathlib import Path

from fastapi import FastAPI
from starlette.background import BackgroundTask

from fastapi.responses import FileResponse
import aiofiles
import aiofiles.os
from fastapi import UploadFile, File



app = FastAPI(debug=True)


@app.get("/delay")
async def delay():
    print("before")
    await asyncio.sleep(10)
    print("after")


### ----------------------------------------------------


async def create_file(file_path: Path, size_bytes=1024 * 1024):
    aiofiles.os.mkdir(file_path.parent)
    async with aiofiles.open(file_path, "wt") as fh:
        await fh.truncate(size_bytes)

    stat_res = await aiofiles.os.stat(file_path)
    print("Size OK?", stat_res.st_size == size_bytes, file_path)
    print("Created file of", stat_res.st_size / 1024 / 1024, "MB")


async def delete_file(file_path):
    stat_res = await aiofiles.os.stat(file_path)
    print("Deleting", stat_res.st_size / 1024 / 1024, "MB")
    await aiofiles.os.remove(file_path)


@app.get(
    "/large-file",
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"}
                },
            },
            "description": "Returns a arbitrary binary data",
        }
    },
)
async def get_large_file():
    large_file = Path("../ignore/large-file.txt")
    await create_file(large_file, size_bytes=15 * 1024 ** 2)

    stats = await aiofiles.os.stat(large_file)
    return FileResponse(
        path=large_file,
        filename=large_file.name,
        stat_result=stats,
        background=BackgroundTask(delete_file, large_file),
    )



@app.put("/file/content")
async def upload_file(file: UploadFile = File(...)):
    pass    
    


@app.get("/file/content",
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"}
                },
            },
            "description": "Returns a arbitrary binary data",
        }
    },
)
async def download_file():
    pass

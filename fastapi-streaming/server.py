# https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse

import pdb
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
import httpx
import aiofiles
from starlette.requests import Request
from starlette.responses import RedirectResponse
import tempfile
import os
from mimetypes import guess_type
from fastapi import UploadFile, File
import aiofiles

app = FastAPI()


@app.get("/")
def hi():
    return "Hello world"


async def iter_stream():
    print("Starting streaming")
    for i in range(100_000):
        yield b"some fake video bytes"


@app.get("/stream")
async def stream():
    return StreamingResponse(iter_stream(), media_type="application/octet-stream")


from pathlib import Path

data_folder = Path(__file__).resolve().parent.parent / "ignore"
data_folder.mkdir(exist_ok=True, parents=True)


@app.put("/upload")
async def upload(file: UploadFile = File(...)):
    chunk_size = 2**4
    async with aiofiles.open(data_folder / file.filename, "wb") as fh:
        more_data = True
        while more_data:
            chunk = await file.read(chunk_size)
            print(len(chunk))

            more_data = len(chunk) == chunk_size
            await fh.write(chunk)


@app.get("/download")
async def download():

    # 1 GB = 10^9 B. 1 GiB = 2^30 B
    # with tempfile.TemporaryFile()
    # file_size = 2**20
    # filepath="sample.data"
    # with open(filepath, "wb") as f:
    #     f.seek(file_size-1)
    #     f.write(b"\0")

    print("Downloading ....")
    FileResponse.chunk_size = 2**5
    return FileResponse(
        path=__file__,
        media_type=guess_type(__file__)[0],
        filename=os.path.basename(__file__),
    )


@app.get("/redownload")
async def redownload():
    async def _download():
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", "http://127.0.0.1:8000/download") as resp:
                # yield resp.headers
                # import pdb; pdb.set_trace()
                async for chunk in resp.aiter_bytes():
                    print(len(chunk))
                    yield chunk
                    print(".")

    # headers = await _download().__anext__()
    # headers = dict(headers)
    # headers.pop("server")
    # headers.pop("date")

    return StreamingResponse(_download())  # , headers=dict(headers))


@app.get(
    "/file/content",
    response_class=FileResponse,
)
async def redirect_to_download(request: Request):
    return RedirectResponse(request.url_for("download"))


@app.put(
    "/file/content",
    response_class=FileResponse,
)
async def redirect_to_upload(request: Request, file: UploadFile = File(...)):

    return RedirectResponse(request.url_for("upload"))

    # attach download stream to the streamed response
    # def _build_headers() -> Dict:
    #     # Adapted from from starlatte/responses.py::FileResponse.__init__
    #     content_disposition_filename = quote(meta.filename)
    #     if content_disposition_filename != meta.filename:
    #         content_disposition = "attachment; filename*=utf-8''{}".format(
    #             content_disposition_filename
    #         )
    #     else:
    #         content_disposition = 'attachment; filename="{}"'.format(meta.filename)
    #     return {"content-disposition": content_disposition}

    # return StreamingResponse(
    #     _download_stream(), media_type=meta.content_type, headers=_build_headers()
    # )

    # return RedirectResponse(presigned_download_link)


# uvicorn streaming_server:app --reload

from fastapi import FastAPI

app = FastAPI()


@app.post("/upload")
def upload_file():
    pass


@app.post("/download")
def download_file():
    pass

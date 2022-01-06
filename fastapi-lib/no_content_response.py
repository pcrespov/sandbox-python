from fastapi import FastAPI, Response, status


app = FastAPI()


@app.get("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def no_content():
    print("no_content")


@app.get("/info")
async def info():
    return {"version": 1.0}


"""
# server
uvicorn no_content_response:app --reload


# client
wget localhost:8000/
--2022-01-06 23:12:46--  http://localhost:8000/
Resolving localhost (localhost)... 127.0.0.1
Connecting to localhost (localhost)|127.0.0.1|:8000... connected.
HTTP request sent, awaiting response... 204 No Content
2022-01-06 23:12:46 (0.00 B/s) - ‘index.html’ saved [0]

"""

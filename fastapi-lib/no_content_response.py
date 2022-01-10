from fastapi import FastAPI, Response, status

app = FastAPI()


# start as
# $ uvicorn no_content_response:app --reload

@app.get("/nc", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def no_content():
    print("no_content")

@app.get("/nc2", status_code=status.HTTP_204_NO_CONTENT)
async def no_content_w_content_type():
    print("no_content_w_content_type")

@app.get("/")
async def root():
    return {"__file__": __file__}



# # client

# $ curl -v localhost:8000/  
#     *   Trying 127.0.0.1:8000...
#     * TCP_NODELAY set
#     * Connected to localhost (127.0.0.1) port 8000 (#0)
#     > GET / HTTP/1.1
#     > Host: localhost:8000
#     > User-Agent: curl/7.68.0
#     > Accept: */*
#     > 
#     * Mark bundle as not supporting multiuse
#     < HTTP/1.1 200 OK
#     < date: Mon, 10 Jan 2022 01:30:15 GMT
#     < server: uvicorn
#     < content-length: 84
#     < content-type: application/json
#     < 
#     * Connection #0 to host localhost left intact
#     {"__file__":"/home/crespo/devp/sandbox-python/fastapi-lib/./no_content_response.py"}%         


# $ curl -v localhost:8000/nc
#     *   Trying 127.0.0.1:8000...
#     * TCP_NODELAY set
#     * Connected to localhost (127.0.0.1) port 8000 (#0)
#     > GET /nc HTTP/1.1
#     > Host: localhost:8000
#     > User-Agent: curl/7.68.0
#     > Accept: */*
#     > 
#     * Mark bundle as not supporting multiuse
#     < HTTP/1.1 204 No Content
#     < date: Mon, 10 Jan 2022 01:30:21 GMT
#     < server: uvicorn
#     * Connection #0 to host localhost left intact


# $ curl -v localhost:8000/nc2
#     *   Trying 127.0.0.1:8000...
#     * TCP_NODELAY set
#     * Connected to localhost (127.0.0.1) port 8000 (#0)
#     > GET /nc2 HTTP/1.1
#     > Host: localhost:8000
#     > User-Agent: curl/7.68.0
#     > Accept: */*
#     > 
#     * Mark bundle as not supporting multiuse
#     < HTTP/1.1 204 No Content
#     < date: Mon, 10 Jan 2022 01:30:23 GMT
#     < server: uvicorn
#     < content-length: 4
#     < content-type: application/json
#     < 
#     * Excess found: excess = 4 url = /nc2 (zero-length body)
#     * Connection #0 to host localhost left intact


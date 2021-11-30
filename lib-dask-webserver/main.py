from fastapi import FastAPI


def fib(n):
    if n<2:
        return n
    else:
        return fib(n-1) + fib(n-2)



app = FastAPI()


@app.get("/fib")
def eval_fib(n: int):
    result = fib(n)
    return result


@app.get("/fast")
def hi():
    return "hoi zaeme"

# uvicorn main:app
# SEE http://127.0.0.1:8000/docs
import time
from celery import Celery
import json
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


app = Celery(
    "tasks",
    broker=f"pyamqp://{os.getenv('RABBIT_USER')}:{os.getenv('RABBIT_PASSWORD')}@{os.getenv('RABBIT_HOST')}:{os.getenv('RABBIT_PORT')}//",
    backend="rpc://",
)
app.conf.update({"task_annotations": {"tasks.add": {"rate_limit": "10/m"}}})
pprint(app.conf)


@app.task
def hello():
    return "hello world"


@app.task
def add(x, y):
    return x + y


@app.task
def fail():
    raise ValueError("fail task")


@app.task
def slow(nap: int = 2):
    print("I will take a nap of %d secs" % nap)
    time.sleep(nap)
    return nap

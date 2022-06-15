from dataclasses import dataclass, field
import queue
from uuid import UUID
from typing import Optional


class Task:
    def __init__(self) -> None:
        pass


class Lock:
    def __init__(self) -> None:
        pass


class LockWithSchedulerData:
    def __init__(self) -> None:
        pass


from fastapi import FastAPI

import asyncio


@dataclass
class A:
    x: int


@dataclass
class DynamicSidecarsScheduler:
    app: FastAPI

    _lock: Lock = field(default_factory=Lock)
    _to_observe: dict[str, LockWithSchedulerData] = field(default_factory=dict)
    _keep_running: bool = False
    _inverse_search_mapping: dict[UUID, str] = field(default_factory=dict)
    _scheduler_task: Optional[Task] = None
    _trigger_observation_queue_task: Optional[Task] = None
    _trigger_observation_queue: asyncio.Queue = field(default_factory=asyncio.Queue)


def test_it():
    a = A(x=3)

    assert isinstance(a, A)

    b = DynamicSidecarsScheduler(app=FastAPI())
    assert isinstance(b, DynamicSidecarsScheduler)


import httpx


def test_httpx():

    timeout = httpx.Timeout(1, read=1)
    client = httpx.Client(timeout=timeout)

    response = client.get("https://httpbin.org/status/204")
    assert response.status_code == 204
    assert not response.content

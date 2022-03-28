import getpass
import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

import httpx
import pandas as pd
from pydantic import AnyUrl, BaseModel, Field, NonNegativeInt, conint
from pydantic.generics import GenericModel

ItemT = TypeVar("ItemT")
DataT = TypeVar("DataT")


class Meta(BaseModel):
    limit: NonNegativeInt
    total: NonNegativeInt
    offset: NonNegativeInt
    count: NonNegativeInt


class Page(GenericModel, Generic[ItemT]):
    _meta: Meta
    data: List[ItemT]


class Envelope(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    error: Optional[Any]

    @classmethod
    def parse_data(cls, obj):
        return cls.parse_obj({"data": obj})


class CheckPoint(BaseModel):
    id: NonNegativeInt
    checksum: str
    tag: Optional[str] = None
    message: Optional[str] = None
    parent: Optional[NonNegativeInt] = None
    created_at: datetime


class ProjectRepo(BaseModel):
    project_uuid: UUID
    url: AnyUrl


class ParentMetaProjectRef(BaseModel):
    project_id: UUID
    ref_id: NonNegativeInt


class ProjectIteration(BaseModel):
    name: str
    parent: ParentMetaProjectRef
    iteration_index: NonNegativeInt
    workcopy_project_id: UUID


NodeIDStr = str
OutputIDStr = str
Outputs = Dict[OutputIDStr, Any]


class ExtractedResults(BaseModel):
    progress: Dict[NodeIDStr, conint(ge=0, le=100)] = Field(
        ..., description="Progress in each computational node"
    )
    labels: Dict[NodeIDStr, str] = Field(
        ..., description="Maps captured node with a label"
    )
    values: Dict[NodeIDStr, Outputs] = Field(
        ..., description="Captured outputs per node"
    )


class ProjectIterationResultItem(ProjectIteration):
    results: ExtractedResults


if __name__ == "__main__":

    password = os.environ.get("USER_PASS")
    user = getpass.getuser() + "@itis.swiss"

    if password is None:
        password = getpass.getpass()
        os.environ.setdefault("USER_PASS", password)

    print(user)

    with httpx.Client(base_url="http://127.0.0.1.nip.io:9081/v0") as client:
        r = client.get("/")
        print(r.status_code, r.json())

        r = client.post(
            "/auth/login",
            json={
                "email": user,
                "password": password,
            },
        )
        print(r.status_code, r.json())

        r = client.get("/me")
        assert r.status_code == 200

        r = client.get("/repos/projects")
        repos = Page[ProjectRepo].parse_obj(r.json())
        project_id = repos.data[0].project_uuid

        r = client.get(f"/repos/projects/{project_id}/checkpoints")
        checkpoints = Page[CheckPoint].parse_raw(r.text)

        r = client.get(f"/repos/projects/{project_id}/checkpoints/HEAD")
        checkpoint = Envelope[CheckPoint].parse_obj(r.json()).data

        r = client.get(f"/projects/{project_id}/checkpoint/{checkpoint.id}/iterations")
        iterations = Page[ProjectIteration].parse_obj(r.json()).data

        r = client.get(
            f"/projects/{project_id}/checkpoint/{checkpoint.id}/iterations/-/results"
        )
        results_page = Page[ProjectIterationResultItem].parse_obj(r.json())

        data = defaultdict(list)
        for iteration in results_page.data:

            for node_id, progress in iteration.results.progress.items():
                data[node_id].append(progress)

            for node_id, label in iteration.results.labels.items():
                data[node_id].extend(list(iteration.results.values[node_id].values()))

        df = pd.DataFrame(data)
        print(df)

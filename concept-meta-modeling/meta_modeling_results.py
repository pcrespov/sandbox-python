import getpass
import itertools
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Generic, Iterator, List, Optional, Type, TypeVar
from uuid import UUID

import httpx
import matplotlib.pyplot as plt
import pandas as pd
from httpx import HTTPStatusError
from pydantic import AnyHttpUrl, AnyUrl, BaseModel, Field, NonNegativeInt, conint
from pydantic.generics import GenericModel

ItemT = TypeVar("ItemT")
DataT = TypeVar("DataT")


class Meta(BaseModel):
    limit: NonNegativeInt
    total: NonNegativeInt
    offset: NonNegativeInt
    count: NonNegativeInt


class PageLinks(BaseModel):
    self: AnyHttpUrl
    first: AnyHttpUrl
    prev: Optional[AnyHttpUrl]
    next: Optional[AnyHttpUrl]
    last: AnyHttpUrl


class Page(GenericModel, Generic[ItemT]):
    meta: Meta = Field(..., alias="_meta")
    data: List[ItemT]
    links: PageLinks = Field(..., alias="_links")


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


def ping(client):
    r = client.get("/")
    print(r.status_code, r.json())


def discover_user_and_pass():
    user = os.environ.get("USER_EMAIL", getpass.getuser() + "@itis.swiss")
    password = os.environ.get("USER_PASS", getpass.getpass())
    return user, password


def login(client, user, password):

    r = client.post(
        "/auth/login",
        json={
            "email": user,
            "password": password,
        },
    )
    try:
        r.raise_for_status()
    except HTTPStatusError as err:
        raise RuntimeError(err.response["error"])

    return r.json()


def get_profile(client):
    r = client.get("/me")
    assert r.status_code == 200
    return r.json()["data"]


def iter_page_items(
    client: httpx.Client, url_path: str, item_cls: Type[ItemT]
) -> Iterator[ItemT]:
    r = client.get(url_path)
    r.raise_for_status()

    page = Page[item_cls].parse_raw(r.text)
    for item in page.data:
        yield item

    while page.links.self != page.links.last:
        next_url = page.links.next.path.replace(client.base_url.path, "")

        r = client.get(next_url)
        r.raise_for_status()

        page = Page[item_cls].parse_raw(r.text)
        for item in page.data:
            yield item


# ------------------------------------------------------------------------------------

if __name__ == "__main__":

    with httpx.Client(base_url="http://127.0.0.1.nip.io:9081/v0") as client:
        ping(client)

        login(client, *discover_user_and_pass())
        assert get_profile(client)

        repos: List[ProjectRepo] = list(
            iter_page_items(client, f"/repos/projects", ProjectRepo)
        )

        project_id = repos[0].project_uuid

        for checkpoint in iter_page_items(
            client,
            f"/repos/projects/{project_id}/checkpoints",
            CheckPoint,
        ):
            print(checkpoint.json(exclude_unset=True, indent=1))

        r = client.get(f"/repos/projects/{project_id}/checkpoints/HEAD")
        head = Envelope[CheckPoint].parse_obj(r.json()).data

        for project_iteration in iter_page_items(
            client,
            f"/projects/{project_id}/checkpoint/{head.id}/iterations",
            ProjectIteration,
        ):
            print(project_iteration.json(exclude_unset=True, indent=1))

        #  results
        data = defaultdict(list)
        columns = []
        index = []

        for row in iter_page_items(
            client,
            f"/projects/{project_id}/checkpoint/{head.id}/iterations/-/results",
            ProjectIterationResultItem,
        ):
            # projects/*/checkpoints/*/iterations/*
            # index.append(
            #    f"/p/{project_id}/c/{checkpoint.id}/i/{iteration.iteration_index}"
            # )
            index.append(row.iteration_index)

            data["progress"].append(
                sum(row.results.progress.values()) / len(row.results.progress)
            )

            for node_id, label in row.results.labels.items():
                data[label].extend(list(row.results.values[node_id].values()))

        df = pd.DataFrame(data, index=pd.Series(index))
        print(df.head())
        print(df.describe())
        print(df.sort_values(by="f2(X)"))

        # plt.close("all")
        # plt.figure()
        # df[1:].plot()
        # plt.show()

        df.to_csv(f"projects_{project_id}_checkpoint_{checkpoint.id}.csv")

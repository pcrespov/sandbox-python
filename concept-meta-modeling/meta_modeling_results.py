import getpass
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Generic, Iterator, List, Optional, Type, TypeVar
from uuid import UUID

import httpx
import pandas as pd
from httpx import HTTPStatusError
from pydantic import AnyHttpUrl, AnyUrl, BaseModel, Field, NonNegativeInt, conint
from pydantic.generics import GenericModel

# pip install pydantic, httpx, pandas, tabulate

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
        assert err.response.is_error  # nosec
        raise RuntimeError(err.response.json.get("error", err.response.text))

    return r.json()


def get_profile(client):
    r = client.get("/me")
    assert r.status_code == 200
    return r.json()["data"]


def iter_items(
    client: httpx.Client, url_path: str, item_cls: Type[ItemT]
) -> Iterator[ItemT]:
    """iterates items returned by a List std-method

    SEE https://google.aip.dev/132
    """

    def _relative_url_path(page_link: Optional[AnyHttpUrl]) -> Optional[str]:
        if page_link:
            return f"{page_link.path}".replace(client.base_url.path, "")
        return None

    next_url = url_path
    last_url = None

    while next_url and next_url != last_url:

        r = client.get(next_url)
        r.raise_for_status()

        page = Page[item_cls].parse_raw(r.text)
        for item in page.data:
            yield item

        next_url = _relative_url_path(page.links.next)
        last_url = _relative_url_path(page.links.last)


# ------------------------------------------------------------------------------------

if __name__ == "__main__":

    with httpx.Client(base_url="http://127.0.0.1.nip.io:9081/v0") as client:
        ping(client)

        login(client, *discover_user_and_pass())
        assert get_profile(client)

        for repo in iter_items(client, f"/repos/projects", ProjectRepo):

            project_id = repo.project_uuid

            r = client.get(f"/repos/projects/{project_id}/checkpoints/HEAD")
            head = Envelope[CheckPoint].parse_obj(r.json()).data
            assert head  # nosec

            for project_iteration in iter_items(
                client,
                f"/projects/{project_id}/checkpoint/{head.id}/iterations",
                ProjectIteration,
            ):
                print(project_iteration.json(exclude_unset=True, indent=1))

            #  results
            data = defaultdict(list)
            columns = []
            index = []

            for row in iter_items(
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
                    for port_name, value in row.results.values[node_id].items():
                        data[f"{label}[{port_name}]"].append(value)

            # Le'ts transform it into pandas --------
            df = pd.DataFrame(data, index=pd.Series(index))
            print(end="\n" * 2)
            print(df.head())
            print(end="\n" * 2)
            print(df.describe())
            # print(df.sort_values(by="f2(X)"))

            # plt.close("all")
            # plt.figure()
            # df[1:].plot()
            # plt.show()

            df.to_csv(f"projects_{project_id}_checkpoint_{head.id}.csv")
            df.to_markdown(f"projects_{project_id}_checkpoint_{head.id}.md")

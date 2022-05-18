from uuid import *
import re
from pydantic import BaseModel, constr
from pydantic.fields import ModelField


UserID = int
NodeID = ProjectID = UUID
ServiceKeyStr = str
ServiceVersionStr = str


TYPE2RE = {
    UUID: r"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b"
}


class DaskJobData(BaseModel):
    service_key: ServiceKeyStr
    service_version: ServiceVersionStr
    user_id: UserID
    project_id: ProjectID
    node_id: NodeID
    uuid: UUID


GOOD = r"[^:]+"  # exclude


def eval_regex(field: ModelField) -> str:
    return field.field_info.regex or TYPE2RE.get(field.type_) or GOOD


formatter = "{service_key}:{service_version}:userid_{user_id}:projectid_{project_id}:nodeid_{node_id}:uuid_{uuid}"
pattern = formatter.format(
    **{
        f.name: "(?<{}>{})".format(f.name, eval_regex(f))
        for f in DaskJobData.__fields__.values()
    }
)


assert (
    pattern
    == "(?<service_key>[^:]+):(?<service_version>[^:]+):userid_(?<user_id>[^:]+):projectid_(?<project_id>\\b[0-9a-f]{8}\\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\\b[0-9a-f]{12}\\b):nodeid_(?<node_id>\\b[0-9a-f]{8}\\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\\b[0-9a-f]{12}\\b):uuid_(?<uuid>\\b[0-9a-f]{8}\\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\\b[0-9a-f]{12}\\b)'"
)


compiled = re.compile(pattern)


def test_it():

    model = DaskJobData(
        service_key="simcore/services/comp/isolve-gpu",
        service_version="2.0.84",
        user_id=3,
        project_id="32130480-fe9a-11eb-92d3-02420a0b00bd",
        node_id="b022b49c-8c42-4014-9f47-9c5c3f687fea",
        uuid=uuid4(),
    )

    jobid = formatter.format(**model.dict())
    m = compiled.match(jobid)
    assert m

    print(m.groupdict())

    m2 = DaskJobData.parse_obj(m.groupdict())


import pytest


@pytest.mark.parametrize(
    "comp_task_row",
    [
        # v1
        {
            "task_id": "919171",
            "project_id": "32130480-fe9a-11eb-92d3-02420a0b00bd",
            "node_id": "b022b49c-8c42-4014-9f47-9c5c3f687fea",
            "job_id": "5f46614f-156a-48dc-b3a1-d18ea081552e",
        },
        # v2
        {
            "task_id": "1460960",
            "project_id": "ac064134-4306-11ec-a206-02420a0b2350",
            "node_id": "e0788777-a386-4f9b-bbc3-a2fb7c3cdfcc",
            "job_id": "simcore/services/comp/osparc-python-runner-tensorflow_1.0.4__projectid_ac064134-4306-11ec-a206-02420a0b2350__nodeid_e0788777-a386-4f9b-bbc3-a2fb7c3cdfcc__098b8416-44f3-4146-8b5c-be4361b896a1",
        },
        # v3
        {
            "task_id": "1801993",
            "project_id": "febe4179-fa0b-410f-a8e4-20e71c6e37c2",
            "node_id": "7a00525c-f213-5271-8e2d-a20f944f8dd6",
            "job_id": "simcore/services/comp/latex-compile:1.3.0:userid_21790:projectid_febe4179-fa0b-410f-a8e4-20e71c6e37c2:nodeid_7a00525c-f213-5271-8e2d-a20f944f8dd6:uuid_c3cdf06c-26e3-4ae0-b20f-21e2abd30017",
        },
    ],
)
def test_backwards_compatibility_parse_dask_job_id(comp_task_row: dict[str, str]):

    #     "(?P<{}>{})".format(match.group("var"), self.GOOD)

    _, _, project_id, node_id, _ = parse_dask_job_id(comp_task_row["job_id"])
    assert project_id == comp_task_row["project_id"]
    assert node_id == comp_task_row["node_id"]

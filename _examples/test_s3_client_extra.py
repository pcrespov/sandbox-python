# pylint: disable=no-name-in-module
# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import asyncio
import time
from collections.abc import Callable
from pathlib import Path

import pytest
from aiohttp import web
from models_library.basic_types import IDStr
from pydantic import parse_obj_as
from pytest_mock import MockerFixture
from pytest_simcore.helpers.monkeypatch_envs import load_dotenv, setenvs_from_dict
from pytest_simcore.helpers.typing_env import EnvVarsDict
from servicelib.aiohttp.application import APP_CONFIG_KEY
from settings_library.s3 import S3Settings
from simcore_service_storage import application, settings
from simcore_service_storage.s3 import get_s3_client
from simcore_service_storage.settings import Settings


@pytest.fixture(scope="session")
def external_environment(request: pytest.FixtureRequest) -> EnvVarsDict:
    """
    If a file under test folder prefixed with `.env-secret` is present,
    then this fixture captures it.

    This technique allows reusing the same tests to check against
    external development/production servers
    """
    envs = {}
    if envfile := request.config.getoption("--external-envfile"):
        assert isinstance(envfile, Path)
        print("🚨 EXTERNAL: external envs detected. Loading", envfile, "...")
        envs = load_dotenv(envfile)
        assert "S3_ACCESS_KEY" in envs
        assert "S3_BUCKET_NAME" in envs
    return envs


@pytest.fixture
def mock_config(
    monkeypatch: pytest.MonkeyPatch,
    external_environment: EnvVarsDict,
) -> None:
    # NOTE: override services/storage/tests/conftest.py::mock_config

    if external_environment:
        print("WARNING: be careful with running tests that")

    setenvs_from_dict(monkeypatch, {**external_environment})
    print(
        "Tests below will be using the following S3 settings:",
        S3Settings.create_from_envs().json(indent=1),
    )


@pytest.fixture
def app(
    mock_config: None,
    is_pdb_enabled: bool,
    mocker: MockerFixture,
    event_loop: asyncio.AbstractEventLoop,
    aiohttp_client: Callable,
    unused_tcp_port_factory: Callable[..., int],
) -> web.Application:

    for module in (
        "simcore_service_storage.application.setup_db",
        "simcore_service_storage.application.setup_rest_api_long_running_tasks",
        "simcore_service_storage.application.setup_rest",
        "simcore_service_storage.application.setup_dsm",
        "simcore_service_storage.application.setup_redis",
        "simcore_service_storage.application.setup_dsm_cleaner",
        "simcore_service_storage.application.setup_monitoring",
    ):
        mocker.patch(module, return_value=None)

    app_under_test = application.create(settings.Settings.create_from_envs())

    _ = event_loop.run_until_complete(
        aiohttp_client(
            app_under_test, server_kwargs={"port": unused_tcp_port_factory()}
        )
    )
    return app_under_test


@pytest.fixture
def simcore_bucket_name(app: web.Application) -> IDStr:
    settings = app[APP_CONFIG_KEY]
    assert isinstance(settings, Settings)
    assert settings.STORAGE_S3
    return parse_obj_as(IDStr, settings.STORAGE_S3.S3_BUCKET_NAME)


async def test_copy_directory_from_s3_to_s3(
    mock_config: None,
    app: web.Application,
    mocker: MockerFixture,
    simcore_bucket_name: IDStr,
):
    bytes_transfered_cb = mocker.MagicMock()

    # src_fmd_object_name = (
    #     "d2504240-cf63-11ee-bf70-02420a0b0228"  # andreas example (s4lio)
    # )
    # src_fmd_object_name = (
    #     "502fd316-8a9e-11ee-a81b-02420a0b173b"  # taylor example (NIH prod)
    #  )

    src_fmd_object_name = "c79379b4-3d48-11ef-b472-02420a00f1d5"  # MY example (master)
    new_fmd_object_name = "pytest_destination3"
    assert app
    s3_client = get_s3_client(app)

    tic = time.time()
    await s3_client.copy_objects_recursively(
        bucket=simcore_bucket_name,
        src_prefix=src_fmd_object_name,
        dst_prefix=new_fmd_object_name,
        bytes_transfered_cb=bytes_transfered_cb,
    )
    elapsed = time.time() - tic

    dst_metadata = await s3_client.get_directory_metadata(
        bucket=simcore_bucket_name, prefix=new_fmd_object_name
    )

    print(
        "Copied",
        src_fmd_object_name,
        f"{dst_metadata=}",
        f"{elapsed=:3.2f}",
        "secs",
    )
    assert bytes_transfered_cb.called

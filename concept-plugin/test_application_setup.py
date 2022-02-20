# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name

from typing import Dict
from unittest.mock import Mock

import pytest
from aiohttp import web
from application_setup import (
    APP_SETTINGS_KEY,
    DependencyError,
    ModuleCategory,
    SkipModuleSetup,
    app_module_setup,
    is_setup_completed,
    _SetupFunc,
)
from pydantic import BaseSettings

log = Mock()


class ApplicationSettings(BaseSettings):
    APP_BAR: bool = True
    APP_FOO: bool = True
    APP_ZEE: bool = True
    APP_FOO_EXT: bool = True


@app_module_setup("APP_BAR", ModuleCategory.ADDON, logger=log)
def setup_bar(app: web.Application, arg1, *, raise_skip: bool = False):
    return True


@app_module_setup("APP_FOO", ModuleCategory.SYSTEM, logger=log)
def setup_foo(app: web.Application, arg1, kargs=33, *, raise_skip: bool = False):
    if raise_skip:
        raise SkipModuleSetup(reason="explicit skip")
    return True


@app_module_setup("APP_ZEE", ModuleCategory.ADDON, logger=log)
def setup_zee(app: web.Application, arg1, kargs=55):
    return True


@app_module_setup(
    "APP_FOO_EXT",
    ModuleCategory.ADDON,
    depends=[
        setup_foo,
    ],
    logger=log,
)
def setup_foo_extension(app: web.Application, arg1, kargs=55):
    return True


@app_module_setup("NOT_A_SETUP", ModuleCategory.ADDON, logger=log)
def setup_not_a_setup():
    return True


@pytest.fixture
def environment_vars(monkeypatch) -> Dict:
    monkeypatch.setenv("APP_BAR", "1")
    monkeypatch.setenv("APP_FOO", "1")
    monkeypatch.setenv("APP_ZEE", "1")
    monkeypatch.setenv("APP_FOO_EXT", "1")


@pytest.fixture
def app(environment_vars) -> web.Application:
    _app = web.Application()
    _app[APP_SETTINGS_KEY] = ApplicationSettings()
    return _app


# -----------------------------------------------------------------------------------------------


def test_init_app(app):
    settings = app[APP_SETTINGS_KEY]

    setup_bar(app)
    setup_foo(app)
    setup_zee(app)
    setup_foo_extension(app)


@pytest.mark.skip(reason="DEV")
def test_setup_config_enabled(app):
    assert setup_zee(app, 1)

    assert setup_zee.metadata()["config_enabled"] == "main.zee_enabled"
    assert not setup_zee(app, 2)


@pytest.mark.skip(reason="DEV")
def test_setup_dependencies(app):

    with pytest.raises(DependencyError):
        setup_foo_extension(app, 1)

    assert setup_foo(app, 1)
    assert setup_foo_extension(app, 2)

    assert setup_foo_extension.metadata()["dependencies"] == [
        setup_foo.metadata()["module_name"],
    ]


@pytest.mark.skip(reason="DEV")
def test_marked_setup(app):
    assert setup_foo(app, 1)

    assert setup_foo.metadata()["module_name"] == "package.foo"
    assert is_setup_completed(setup_foo.metadata()["module_name"], app)

    app_config["foo"]["enabled"] = False
    assert not setup_foo(app, 2)


@pytest.mark.skip(reason="DEV")
def test_skip_setup(app):
    try:
        log.reset_mock()

        assert not setup_foo(app, 1, raise_skip=True)

        # FIXME: mock logger
        # assert log.warning.called
        # warn_msg = log.warning.call_args()[0]
        # assert "package.foo" in warn_msg
        # assert "explicit skip" in warn_msg

        assert setup_foo(app, 1)
    finally:
        log.reset_mock()

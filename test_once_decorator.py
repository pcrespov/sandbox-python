#
# TODO: compare with
# services/api-server/src/simcore_service_api_server/utils/app_data.py
# services/api-server/src/simcore_service_api_server/utils/client_base.py

import functools
import logging

import httpx
import pytest
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from simcore_service_payments.utils.http_client import AppStateMixin, BaseHttpApi


def run_once(*, raise_for_rerun: bool = False):
    def _decorator(class_method):
        def _wrapper(cls, *args, **kwargs):
            if not _wrapper.has_run:
                _wrapper.has_run = True
                return class_method(cls, *args, **kwargs)

            msg = f"{class_method.__name__} has already been executed and will not run again."
            if raise_for_rerun:
                raise RuntimeError(msg)
            logging.warning(msg)
            return None

        _wrapper.has_run = False
        return functools.wraps(_wrapper)

    return _decorator


class _AppStateParams:
    __slots__ = (
        "name",
        "repr",
        "eq",
        "order",
        "unsafe_hash",
        "frozen",
    )

    def __init__(self, name, frozen):
        self.name = name
        self.frozen = frozen

    def __repr__(self):
        return "_AppStateParams(" f"name={self.name!r}," f"frozen={self.frozen!r}" ")"


# STUDY https://github.com/python/cpython/blob/main/Lib/dataclasses.py#L1243-L1271
#


def create_app_state(name, *, frozen: bool = False):
    def _decorator(cls):
        # requirements
        assert hasattr(cls, "create")  # nosec
        assert hasattr(cls, "start")  # nosec
        assert hasattr(cls, "close")  # nosec

        def _get_state(app):
            try:
                return getattr(app.state, name)
            except AttributeError:
                if raise_if_undefined:
                    raise
            return None

        def get_from_state(cls, app: FastAPI):
            assert cls  # nosec
            return _get_state(app)

        def set_to_state(cls, app: FastAPI):
            if exists := _get_state(app):
                logging.warning(
                    "%s already setup in app.state.%s=%s", type(cls), name, exists
                )
                return

            # create and set-state
            api = cls.create(app)
            setattr(app.state, name, api)

            # define lifespam
            app.add_event_handler("startup", api.start)
            app.add_event_handler("shutdown", api.close)

        cls.get_from_state = classmethod(get_from_state)
        cls.set_to_state = classmethod(set_to_state)

        return cls

    return _decorator


def test_base_http_api():
    class MyAppSettings(BaseModel):
        MY_BASE_URL: HttpUrl = "https://test_base_http_api"

    # @create_app_state("my_client_api", raise_if_undefined=True)
    class MyClientApi(BaseHttpApi, AppStateMixin):
        app_state_name: str = "my_client_api"
        raise_if_undefined: bool = True

    app = FastAPI()
    app.state.settings = MyAppSettings()

    with pytest.raises(AttributeError):
        MyClientApi.load_from_state(app)

    api = MyClientApi(
        client=httpx.AsyncClient(
            base_url=app.state.settings.MY_BASE_URL,
        )
    )
    api.save_to_state(app)

    assert MyClientApi.load_from_state(app) == api

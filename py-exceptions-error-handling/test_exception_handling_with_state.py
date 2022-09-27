import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import pytest

log = logging.getLogger(__name__)


class NetworkConnectionError(Exception):
    pass


class NetworkConnectionErrorHandler:
    """
    Ignores exception within a ignore_interval since the first failure
    and then raises when it is over.

    """

    def __init__(self, ignore_for_s: int):
        self._ignore_delta = timedelta(seconds=ignore_for_s)

        self._ignore_until: Optional[datetime] = None
        self._number_of_failures: int = 0  # mostly to have a nice message

    def _set_first_failure(self):
        self._ignore_until = datetime.utcnow() + self._ignore_delta
        self._number_of_failures = 1

    def passed(self):
        self._ignore_until = None
        self._number_of_failures = 0

    def failed(self, exc: NetworkConnectionError):
        if self._number_of_failures == 0:
            assert self._ignore_until is None
            self._set_first_failure()

        elif self._ignore_until < datetime.utcnow():
            assert self._number_of_failures > 0
            raise exc

        else:
            assert self._ignore_until is not None
            self._number_of_failures += 1

        log.warning("Skipping exception %d times: %s", self._number_of_failures, exc)


# --------------------------


def test_handler():

    error_handler = NetworkConnectionErrorHandler(ignore_for_s=1)

    # ignores consecutive failures
    error_handler.failed(NetworkConnectionError())
    time.sleep(0.1)
    error_handler.failed(NetworkConnectionError())
    time.sleep(1.0)

    # will always raise
    with pytest.raises(NetworkConnectionError):
        error_handler.failed(NetworkConnectionError())

    with pytest.raises(NetworkConnectionError):
        error_handler.failed(NetworkConnectionError())

    # this will reset
    error_handler.passed()
    error_handler.failed(NetworkConnectionError())
    error_handler.failed(NetworkConnectionError())


def test_usage():
    def _connect(i):
        if i < 3:
            raise NetworkConnectionError(f"{i+1}th connection error")
        print(f"Connected with {i=}")

    # Every sidecar's state should have one instanace of this
    error_handler = NetworkConnectionErrorHandler(ignore_for_s=1)

    for i in range(5):
        try:
            _connect(i)

        except NetworkConnectionError as err:
            error_handler.failed(err)
        else:
            assert error_handler._number_of_failures in (3, 0)
            error_handler.passed()
            assert error_handler._number_of_failures == 0

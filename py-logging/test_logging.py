#
# https://docs.python.org/3/library/logging.html#logging.basicConfig
#

import logging
import time
from contextlib import contextmanager
from typing import Any

import pytest


@contextmanager
def log_context(logger: logging.Logger, level: int, msg: str, *args, **kwargs):
    # NOTE: keeps same signature as https://docs.python.org/3/library/logging.html#logging.Logger.log
    logger.log(level, "Starting " + msg, *args, **kwargs)
    yield
    logger.log(level, "Completed " + msg, *args, **kwargs)


def test_log_context():
    user_id = 42
    value = 3.14

    logger = logging.getLogger("test-log-context-logger")
    logger.setLevel(logging.INFO)

    extras: dict[str, Any] = {"user_id": user_id}
    with log_context(
        logger, logging.INFO, " %s with %s ", f"{user_id=}", f"{value=}", extra=extras
    ):
        for n in range(3):
            time.sleep(0.5)
            logger.info("Going so far good %d", n)

    with log_context(
        logger,
        logging.INFO,
        " %s with %s %s",
        f"{user_id=}",
        f"{value=}",
        extras,
        extra=extras,
    ):
        for n in range(3):
            time.sleep(0.5)
            logger.info("Going so far good %d", n)
        logger.warning("Something went wrong, but we can continue")
        extras["error_code"] = "OEC:12345678"


def logit(log):
    print("{:*^100}".format(str(log)))

    if log is not logging:
        print(log.handlers)

    log.critical("Really bad")
    log.error("Bad")
    log.warning("Careful")
    log.info("FYI")
    log.debug("BTW")


@pytest.mark.skip(reason="DEV")
def test_logging_lib():

    # logging.basicConfig(level=logging.DEBUG)
    # Normal usage of logging.basicConfig:
    #
    # It is a convenience method intended for use by simple scripts to do one-shot configuration of the logging package.
    #
    # ===> This function DOES NOTHING if the root logger already has handlers  configured

    assert logging.root == logging.getLogger()
    assert not logging.root.handlers
    # logging.basicConfig(level=logging.DEBUG)

    # setting level DOES NOT creates handler
    assert not logging.root.handlers
    logging.root.setLevel(logging.DEBUG)  # ensures root level
    assert not logging.root.handlers

    logit(logging)  # lazy generation of handlers as soon as a log is written
    assert len(logging.root.handlers) == 1
    # import pdb; pdb.set_trace()
    assert logging.root.level == logging.DEBUG

    # therefore thisone DOES NOTHING
    logging.basicConfig(level=logging.CRITICAL)

    logit(logging.root)
    ## logging.root.setLevel(logging.DEBUG)
    logit(logging.getLogger("A"))
    logit(logging.getLogger("A.B"))
    logit(logging.getLogger("A.C"))

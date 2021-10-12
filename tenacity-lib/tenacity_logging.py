import json
import logging
import sys
from functools import wraps
from typing import Any, Callable, Counter, Dict

from tenacity import *
from tenacity import RetryCallState

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logger = logging.getLogger("MY-LOGGER")


class MyException(Exception):
    pass


def log_success(fun, log: logging.Logger = logger):
    if hasattr(fun, "retry"):
        if not fun.retry.statistics:
            print("this function was never called")

        if fun.retry.statistics.get("attempt_number", 0) > 1:
            print("this function was retried more than once and now it went thru")

            print(json.dumps(fun.retry.statistics, indent=2))
            print("Finally went through!!")


def create_before_sleep_policy(custom_logger):
    def _policy(retry_state: RetryCallState):
        # increases level with number of attempts
        if retry_state.attempt_number < 3:
            loglevel = logging.INFO
        else:
            loglevel = logging.WARNING

        custom_logger.log(
            loglevel,
            "Retrying %s: attempt %s ended with: %s",
            retry_state.fn.__name__,
            retry_state.attempt_number,
            retry_state.outcome,
        )

    return _policy


RETRY_POLICY = dict(
    wait=wait_fixed(0.1),
    stop=stop_after_attempt(5),
    reraise=True,
    # logs before/after retrying (because it failed)
    # before=before_log(logger, logging.DEBUG),
    # after=after_log(logger, logging.DEBUG),
    before_sleep=create_before_sleep_policy(logger),
)


@retry(**RETRY_POLICY)
def always_fails():
    # Allways faile
    raise MyException("Fail")


_count = 0


@retry(**RETRY_POLICY)
def fails_and_then_succeeds():
    global _count
    _count += 1
    if _count != 3:
        raise MyException("Fail")


@retry(**RETRY_POLICY)
def simply_succeed():
    return 1


if __name__ == "__main__":
    try:
        print("-" * 100)
        always_fails()
    except MyException as err:
        print(f"finished because of {err}")
        print(always_fails.retry.statistics)

    print("-" * 100)
    fails_and_then_succeeds()
    log_success(fails_and_then_succeeds)

    print("-" * 100)
    simply_succeed()
    log_success(simply_succeed)

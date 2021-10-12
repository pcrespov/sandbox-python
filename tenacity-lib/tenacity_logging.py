import logging
import sys
from functools import wraps
from typing import Callable, Counter

from tenacity import *
from tenacity import RetryCallState

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logger = logging.getLogger("MY-LOGGER")


class MyException(Exception):
    pass


def log_success(wrapped: Callable):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        res = wrapped(*args, **kwargs)
        logger.info("I went through")
        return res

    return wrapper


def my_before_sleep(retry_state: RetryCallState):
    # increases level with number of attempts
    if retry_state.attempt_number < 3:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    logger.log(
        loglevel,
        "Retrying %s: attempt %s ended with: %s",
        retry_state.fn.__name__,
        retry_state.attempt_number,
        retry_state.outcome,
    )


RETRY_POLICY = dict(
    wait=wait_fixed(0.1),
    stop=stop_after_attempt(5),
    reraise=True,
    # logs before/after retrying (because it failed)
    # before=before_log(logger, logging.DEBUG),
    # after=after_log(logger, logging.DEBUG),
    before_sleep=my_before_sleep,
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


if __name__ == "__main__":
    try:
        print("-" * 100)
        always_fails()
    except MyException as err:
        print(f"finished because of {err}")
        print(always_fails.retry.statistics)

    print("-" * 100)
    fails_and_then_succeeds()
    print(fails_and_then_succeeds.retry.statistics)

from tenacity import RetryError, TryAgain, retry
from tenacity.stop import stop_after_attempt


class SomeBaseException(BaseException):
    """This is NOT caught by retry!
    Thankfully since asyncio.CancelleError is
    """


class MyException(Exception):
    ...


@retry(reraise=False, stop=stop_after_attempt(3))
def raise_my_exception():
    print("attempt")
    raise MyException("Fail")
    raise TryAgain("try again")


try:
    raise_my_exception()

except MyException as err:
    print(err)
except RetryError as err:
    print(err)
    print(f"{err.last_attempt.failed=} after {err.last_attempt.attempt_number=}")

except TryAgain as err:
    print("I tried", err)

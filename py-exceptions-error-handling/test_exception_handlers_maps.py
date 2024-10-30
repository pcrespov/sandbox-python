from contextlib import contextmanager
from typing import Callable


@contextmanager
def exception_context(
    exception_type: type[BaseException] | tuple[type[BaseException], ...],
    exception_handler: Callable,
):
    try:
        yield
    except exception_type as e:
        # the `exception_handler` customizes how an `exception_type` is handled when it raises within the exception context
        # - `exception_handler` returns
        #   - an exception (new or same as e) to raise: exception transformation. Useful to map errors between APIs
        #   - None
        # - must not raise!
        #
        if exc := exception_handler(e):
            assert isinstance(exc, BaseException)
            raise exc from e


def test_it():
    def print_and_ignore_exception(exc):
        print(f"Caught an exception of type {type(exc).__name__}: {exc}")
        return None

    def print_and_reraise_exception(exc):
        print(f"Reraising {type(exc).__name__}: {exc}")
        return exc

    with exception_context((ZeroDivisionError, ValueError), print_and_ignore_exception):
        raise ZeroDivisionError("this should be handled")

    with exception_context((ZeroDivisionError, ValueError), print_and_ignore_exception):
        with exception_context(
            (ZeroDivisionError, ValueError), print_and_reraise_exception
        ):
            raise ZeroDivisionError("this should be  handled at the top")

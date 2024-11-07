import contextlib
from contextlib import contextmanager
from typing import Callable


@contextmanager
def handled_exception_context(
    exception_type: type[BaseException] | tuple[type[BaseException], ...],
    exception_handler: Callable,
    **forward_ctx,
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
        if exc := exception_handler(e, **forward_ctx):
            assert isinstance(exc, BaseException)
            raise exc from e


# handler systems


def print_and_ignore_exception(exc):
    print(f"Caught an exception of type {type(exc).__name__}: {exc}")
    return None


def print_and_reraise_exception(exc):
    print(f"Reraising {type(exc).__name__}: {exc}")
    return exc


def test_basics():

    with handled_exception_context(
        (ZeroDivisionError, ValueError), print_and_ignore_exception
    ):
        raise ZeroDivisionError("this should be handled")

    with handled_exception_context(
        (ZeroDivisionError, ValueError), print_and_ignore_exception
    ):
        with handled_exception_context(
            (ZeroDivisionError, ValueError), print_and_reraise_exception
        ):
            raise ZeroDivisionError("this should be  handled at the top")


def rest_handler(request):
    return request


def middleware(request):
    with handled_exception_context(
        ValueError, print_and_ignore_exception, request=request
    ):
        response = rest_handler(request)
        return response


def configurable_middleware(request, error_handlers):
    with contextlib.ExitStack() as stack:
        # SEE https://docs.python.org/3/library/contextlib.html#supporting-a-variable-number-of-context-managers
        for exc_t, exc_h in error_handlers:
            stack.enter_context(
                handled_exception_context(exc_t, exc_h, request=request)
            )
        response = rest_handler(request)
        return response


def test_middleware():
    ...

# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import contextlib
from contextlib import contextmanager
from typing import Callable

import pytest


@contextmanager
def _handle_by_mapping(
    catch_exc: type[Exception] | tuple[type[Exception]],
    reraise_exc: type[Exception],
    msg_template: str,
):
    # CONCEPT!
    try:
        yield
    except catch_exc as exc:
        msg = msg_template.format_map(exc.__dict__)
        raise reraise_exc(msg) from exc


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


def test_exception_context():
    # SEE https://docs.python.org/3/library/exceptions.html#exception-context

    def _raise():
        raise ValueError("Error from _foo")

    with pytest.raises(ValueError) as err_info:
        _raise()

    exc1 = err_info.value
    # these object provide information about the context in which the exception was raised:
    assert exc1.__cause__ is None
    assert exc1.__context__ is None
    assert exc1.__suppress_context__ is False

    def _chain_and_reraise():
        try:
            _raise()
        except Exception as exc:
            msg = "Error from _bar"
            # explicitly chained exception
            raise RuntimeError(msg) from exc

    with pytest.raises(RuntimeError) as err_info:
        _chain_and_reraise()

    exc2 = err_info.value
    # The expression following from must be an exception or None. It will be set as __cause__ on the raised exception
    assert isinstance(exc2.__cause__, ValueError)
    assert (
        exc2.__suppress_context__ is True
    )  # Setting __cause__ also implicitly sets the __suppress_context__ attribute to True
    assert exc2.__context__ == exc2.__cause__

    # Using raise new_exc from None effectively replaces the old exception with the new one for display purposes
    # (e.g. converting KeyError to AttributeError),
    #  while leaving the old exception available in __context__ for introspection when debugging.
    def _replace_and_reraise():
        try:
            _raise()
        except Exception:
            msg = "Error from _bar"
            raise RuntimeError(msg) from None

    with pytest.raises(RuntimeError) as err_info:
        _replace_and_reraise()

    exc3 = err_info.value
    # The expression following from must be an exception or None. It will be set as __cause__ on the raised exception
    assert isinstance(exc3.__cause__, type(None))
    assert isinstance(exc3.__context__, ValueError)
    # assert exc3.__suppress_context__ is True # NOT TOTALLY CLEAR! ?????


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

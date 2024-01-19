import logging

logger = logging.getLogger(__name__)



def fun1():
    values = {}
    return values["invalidkey"]

def fun2():
    return fun1()

def fun3():
    return fun2() * 10

def fun4():
    return fun3() + 1

def fun5():
    return 2* fun4() + fun3()


def test_logging_errors():
    try:
        x = fun5()
    except KeyError as err:

        logger.warning("Error in fun 5 as warning with exc_info", exc_info=True)
        logger.exception("Error in fun 5 as exception")

        # live log call -----------------
        # WARNING  test_exceptions_logging:test_exceptions_logging.py:28 Error in fun 5 as warning with exc_info
        # Traceback (most recent call last):
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 26, in test_logging_errors
        #     x = fun5()
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 21, in fun5
        #     return 2* fun4() + fun3()
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 18, in fun4
        #     return fun3() + 1
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 15, in fun3
        #     return fun2() * 10
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 12, in fun2
        #     return fun1()
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 9, in fun1
        #     return values["invalidkey"]
        # KeyError: 'invalidkey'
        # ERROR    test_exceptions_logging:test_exceptions_logging.py:29 Error in fun 5 as exception
        # Traceback (most recent call last):
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 26, in test_logging_errors
        #     x = fun5()
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 21, in fun5
        #     return 2* fun4() + fun3()
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 18, in fun4
        #     return fun3() + 1
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 15, in fun3
        #     return fun2() * 10
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 12, in fun2
        #     return fun1()
        #   File "/home/crespo/devp/sandbox-python/py-exceptions-error-handling/test_exceptions_logging.py", line 9, in fun1
        #     return values["invalidkey"]
        # KeyError: 'invalidkey'

        logger.warning("Error in fun 5 as warning with exc_info+stack_info", exc_info=True, stack_info=True)
        # Appends to the log text above ...
        #
        # Stack (most recent call last):
        # File "/home/crespo/.pyenv/versions/3.9.12/lib/python3.9/runpy.py", line 197, in _run_module_as_main
        # return _run_code(code, main_globals, None,

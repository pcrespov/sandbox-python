# testing aiolib

## async fixtures and ``pytest-aiohttp``

``pytest-aiohttp`` plugin has a mechanism to run async fixtures that can be found in
 [aiohttp.pytest_plugin.pytest_fixture_setup](https://github.com/aio-libs/aiohttp/blob/master/aiohttp/pytest_plugin.py#L56)


It seems:

1. ``aiohttp.pytest_plugin`` is the place where async fixtures are executed
   -  It seems ``pytest`` does not know how to run async fixtures
1. it hooks into ``pytest`` implementing ``pytest_fixture_setup``
   - that explains why our ``session_loop`` was completely ignored
1. it runs async fixtures as we were suggesting ie. with ``loop.run_until_complete``
1. it uses the loop defined in the [fixture named ``loop``](https://github.com/aio-libs/aiohttp/blob/master/aiohttp/pytest_plugin.py#L92). Otherwise it raises an exception
1. if the async fixture has a ``yield`` (i.e. async generator) then it is treated in two runs .. one to start and one to finalize.


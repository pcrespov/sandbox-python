# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pytest",
#     "pytest-ascynio",
# ]
# ///

# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements
# pylint: disable=unused-argument
# pylint: disable=unused-variable

# SEE https://pytest-asyncio.readthedocs.io/en/stable/

#
# pytest --asyncio-mode=auto -s -vvv test_asyncio_pytest.py
#

import pytest
import asyncio


# pytestmark = pytest.mark.asyncio(loop_scope="module")


pytest_plugins = [
    ]

_all_loop_ids = set()

@pytest.fixture
def value_fixture():
    # This is a placeholder for a fixture that could be used in tests
    return "fixture_value"

async def test_async(value_fixture):

    global _all_loop_ids
    loop_id = id(asyncio.get_running_loop())
    is_shared = loop_id in _all_loop_ids
    print(f"\n{loop_id=}, {is_shared=}")
    _all_loop_ids.add(loop_id)

    # This is just a placeholder for another test
    async def some_async_function():
        await asyncio.sleep(1)

    await some_async_function()
    assert True  # Replace with actual test logic


def test_sync():
    # This is a synchronous test, not using aiohttp
    assert 1 + 1 == 2  # Replace with actual test logic 




async def test_remember_loop():
    global _all_loop_ids
    loop_id = id(asyncio.get_running_loop())
    is_shared = loop_id in _all_loop_ids
    print(f"\n{loop_id=}, {is_shared=}")
    _all_loop_ids.add(loop_id)

@pytest.mark.asyncio(loop_scope="module")
async def test_runs_in_a_loop():
    global _all_loop_ids
    loop_id = id(asyncio.get_running_loop())
    is_shared = loop_id in _all_loop_ids
    print(f"\n{loop_id=}, {is_shared=}")
    _all_loop_ids.add(loop_id)

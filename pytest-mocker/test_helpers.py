# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
import asyncio
from unittest.mock import call
import helpers


async def foo(n=1):
    for i in range(n):
        assert await helpers.coro(i) == 6


async def test_with_async_patches(mocker, loop):
    mock = mocker.patch("helpers.coro", return_value=6, autospec=True)

    assert mock == helpers.coro

    await foo(3)

    assert mock.call_count == 3

    assert mock.called
    mock.assert_called()
    mock.assert_awaited()


async def doit(engine):
    async with engine.acquire() as conn:
        await conn.scalar()
        await conn.execute()


async def test_with_context_manager(mocker, loop):
    connection = mocker.AsyncMock(name="Connection")

    mc = mocker.Mock(name="ManagedConnection")
    mc.__aenter__ = mocker.AsyncMock(name="Enter", return_value=connection)
    mc.__aexit__ = mocker.AsyncMock(name="Exit", return_value=False)

    engine = mocker.Mock(name="Engine")
    engine.acquire.return_value = mc

    await doit(engine)

    connection.scalar.assert_awaited()
    connection.execute.assert_awaited()

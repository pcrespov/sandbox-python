import psycopg2
import pytest

from aiopg.sa import Engine, create_engine

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


async def test_engine_when_pg_not_reachable(loop):

    with pytest.raises((psycopg2.OperationalError,)) as excinfo:
        await create_engine(
            DSN.format(
                database="db", user="foo", password="foo", host="localhost", port=123
            ),
            application_name=None,
            minsize=1,
            maxsize=4,
        )


        # FIXME: ONLY in github-actions raises FileNotFoundError while tear-down engine
        # aiopg.connection executes self._waiter ---> loop.remove_writer() which raises FileNotFoundError

    assert "could not connect to server" in str(excinfo.value)

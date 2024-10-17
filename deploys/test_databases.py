import socket
from pathlib import Path

import pytest
import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# secrets aggregated from multiple deploys' repo.config files
params_path = Path("param.secrets.yml").resolve()
_skip_reason = f"{params_path} not present in cwd={params_path.parent}"
try:
    params = yaml.safe_load(params_path.read_text())
except FileNotFoundError:
    params = {}


@pytest.mark.skipif(not params, reason=_skip_reason)
@pytest.mark.parametrize(
    "host, port",
    [
        pytest.param(d["host"], d["port"], id=d["id"])
        for d in params.get("databases", [])
    ],
)
def test_database_tcp_reachability(host, port):
    try:
        # Establish a TCP connection to the host and port
        with socket.create_connection((host, port), timeout=5) as sock:
            assert sock is not None, f"Failed to connect to {host}:{port}"

    except (socket.timeout, OSError) as e:
        pytest.fail(f"Could not reach the database service at {host}:{port}: {e}")


@pytest.mark.skipif(not params, reason=_skip_reason)
@pytest.mark.parametrize(
    "user, password, host, port, database",
    [
        pytest.param(
            d["user"], d["password"], d["host"], d["port"], d["database"], id=d["id"]
        )
        for d in params.get("databases", [])
    ],
)
def test_database_readiness(user, password, host, port, database):
    database_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(database_url, echo=True, connect_args={"connect_timeout": 5})

    try:
        # Establish connection and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1, "Database did not return expected result"

    except OperationalError as e:
        pytest.fail(f"Could not connect to the database {database}: {e}")

    finally:
        engine.dispose()

from pathlib import Path

import pytest
import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# secrets aggregated from multiple deploys' repo.config files
params_path = Path("param.secrets.yml").resolve()
try:
    params = yaml.safe_load(params_path.read_text())
except FileNotFoundError:
    params = {}


@pytest.mark.skipif(
    not params, reason=f"{params_path} not present in cwd={params_path.parent}"
)
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

    engine = create_engine(database_url, echo=True, connect_args={"connect_timeout": 2})

    try:
        # Establish connection and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1, "Database did not return expected result"

    except OperationalError as e:
        pytest.fail(f"Could not connect to the database {database}: {e}")

    finally:
        engine.dispose()

import os
from textwrap import dedent

from faker import Faker
import pytest


@pytest.fixture(scope="module")
def service_environ():
    prev = None
    #pylint: disable=W0212
    if "PASSWORD" in os.environ:
        prev = os.environ["PASSWORD"]
    os.environ["PASSWORD"] = "secret-password"

    yield os.environ

    if prev:
        os.environ["PASSWORD"] = prev
    else:
        del os.environ["PASSWORD"]


def test_config_file(cli, tmpdir, service_environ):    
    config_path = tmpdir/"config.yaml"
    
    with open(config_path, "wt") as fh:
        fh.write(dedent("""
        postgres:
          database: aiohttpdemo
          user: aiohttpdemo_user
          password: ${PASSWORD}
          host: localhost
          port: 5432
          maxsize: 5

        host: 127.0.0.1
        port: 8080
        """))
    
    cmd = "-c {}".format(config_path)
    #cmd += " --print-config-vars"
    #cmd += " --print-config"
    cmd += " --check-config"
        
    config = cli(cmd.split())
    print(config)


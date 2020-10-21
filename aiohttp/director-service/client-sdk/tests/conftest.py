import pytest

from director import main

@pytest.fixture(scope="module")
def cli():
    def _main(argv):
        config = {}
        try:
            config = main.main(argv)
        except SystemExit as err:
            if err.code!=0:
                raise err
        return config
    return _main

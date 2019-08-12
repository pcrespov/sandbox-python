# pylint:disable=wildcard-import
# pylint:disable=unused-import
# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name

import pytest

import sys
import os
from os.path import join, relpath
from pathlib import Path
import shutil

@pytest.fixture(scope="session")
def here():
    return Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent


@pytest.fixture(scope="session")
def specs_dir(here):
    specsdir = here.parent / "specs"
    assert specsdir.exists()
    return Path(specsdir)


def list_specs(wildcard):
    return list(map(str, specs_dir(here()).rglob(wildcard)))

@pytest.fixture(scope="module",
                params= list_specs("*.y*ml") + \
                        list_specs("*.json"))
def api_spec_file(request, specs_dir):
    specs_path = request.param
    assert os.path.exists(specs_path)
    return relpath(specs_path, specs_dir)


from itertools import chain

@pytest.fixture("module")
def api_spec_tails(specs_dir):
    """ Returns spec files path relative to specs_dir """
    tails = []
    for fpath in chain(*[specs_dir.rglob(wildcard) for wildcard in ("*.json", "*.y*ml")]):
        tail = relpath(fpath, specs_dir)
        tails.append( Path(tail) )
    return tails


    # for basedir, files, dirs in os.walk(specs_dir):
    #     spec_files = [ n for n in files if n.endswith((".yaml", ".yml", ".json")) ]
    #     if spec_files:
    #         newbase = Path(relpath(basedir, specs_dir) )
    #         _spec_files.extend( [ newbase / n for n in spec_files] )

    #     dirs[:] = [ d for d in dirs if not d.startswith((".", "_")) ]
    # return _spec_files


@pytest.fixture("module")
def specs_testdir(here, specs_dir, api_spec_tails, tmpdir_factory):
    # Copies all test
    testdir = Path( tmpdir_factory.mktemp("new-specs-dir") )
    for tail in api_spec_tails:
        dstdir = testdir / tail.parent
        os.makedirs(dstdir, exist_ok=True)
        shutil.copy(specs_dir/tail, dstdir)

    return testdir



def test_it(specs_testdir, api_spec_file):
    specs_path = specs_testdir / api_spec_file
    print(specs_path)
    assert specs_path.exists()

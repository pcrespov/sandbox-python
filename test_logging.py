# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import logging

import pytest


def set_parent_module_log_level(module_name, level):
    logger = logging.getLogger(module_name)
    parent_logger = logging.getLogger(module_name.split(".")[0])
    logger.setLevel(level)
    parent_logger.setLevel(level)


def test_set_parent_module_log_level(caplog: pytest.LogCaptureFixture):
    caplog.clear()
    # emulates service logger
    logging.root.setLevel(logging.WARNING)

    parent = logging.getLogger("parent")
    child = logging.getLogger("parent.child")

    assert parent.level == logging.NOTSET
    assert child.level == logging.NOTSET

    parent.debug("parent debug")
    child.debug("child debug")

    parent.info("parent info")
    child.info("child info")

    parent.warning("parent warning")
    child.warning("child warning")

    assert "parent debug" not in caplog.text
    assert "child debug" not in caplog.text

    assert "parent info" not in caplog.text
    assert "child info" not in caplog.text

    assert "parent warning" in caplog.text
    assert "child warning" in caplog.text

    caplog.clear()
    set_parent_module_log_level("parent.child", logging.INFO)

    assert parent.level == logging.INFO
    assert child.level == logging.INFO

    parent.debug("parent debug")
    child.debug("child debug")

    parent.info("parent info")
    child.info("child info")

    parent.warning("parent warning")
    child.warning("child warning")

    assert "parent debug" not in caplog.text
    assert "child debug" not in caplog.text

    assert "parent info" in caplog.text
    assert "child info" in caplog.text

    assert "parent warning" in caplog.text
    assert "child warning" in caplog.text

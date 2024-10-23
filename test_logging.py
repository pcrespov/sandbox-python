# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import logging

import pytest


def set_logger_level(logger_name: str, level: int):
    """
    Sets the logging level for a specific logger by name.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False  # Optional: Disable propagation if needed


# Map of logger names to their desired levels
LOGGER_LEVEL_MAP = {
    "a": logging.WARNING,
    "a.b": logging.DEBUG,
    "a.b.c": logging.INFO,  # Overriding 'a.b' for 'a.b.c'
}


def set_logger_level(logger_name: str, level: int):
    """
    Sets the logging level for a specific logger by name and adds a handler.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False  # Optional: Disable propagation if needed

    # Add handler to ensure logs are captured by caplog
    if not logger.hasHandlers():  # To avoid adding duplicate handlers
        handler = logging.StreamHandler()
        logger.addHandler(handler)


@pytest.mark.parametrize(
    "logger_name, level, message, expected_in_logs",
    [
        (
            "a",
            logging.DEBUG,
            "This should not appear.",
            False,
        ),  # DEBUG not expected in 'a'
        (
            "a",
            logging.WARNING,
            "This is a warning from logger a.",
            True,
        ),  # WARNING expected in 'a'
        (
            "a.b",
            logging.DEBUG,
            "This is a debug message from logger a.b.",
            True,
        ),  # DEBUG expected in 'a.b'
        (
            "a.b.c",
            logging.DEBUG,
            "This debug message should not appear from logger a.b.c.",
            False,
        ),  # DEBUG not expected in 'a.b.c'
        (
            "a.b.c",
            logging.INFO,
            "This is an info message from logger a.b.c.",
            True,
        ),  # INFO expected in 'a.b.c'
    ],
)
def test_configure_loggers(logger_name, level, message, expected_in_logs, caplog):
    """
    Configures the loggers based on the LOGGER_LEVEL_MAP and tests using caplog.
    """
    # Set up log levels for each logger in the map
    for logger_name_in_map, level_in_map in LOGGER_LEVEL_MAP.items():
        set_logger_level(logger_name_in_map, level_in_map)

    # Use caplog to capture the logs
    with caplog.at_level(
        logging.DEBUG
    ):  # Capture logs at DEBUG level to cover all levels
        logger = logging.getLogger(logger_name)
        logger.log(level, message)

    # Check if the message is found in captured logs
    if expected_in_logs:
        assert message in caplog.text, f"Expected log message '{message}' in logs"
    else:
        assert (
            message not in caplog.text
        ), f"Did not expect log message '{message}' in logs"


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

import datetime
import os

import pytest

# Dictionary to store start times of tests
_test_start_times = {}


def _utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def _construct_graylog_url(
    api_host: str, start_time: datetime.datetime, end_time: datetime.datetime
) -> str:
    """
    Construct a Graylog URL for the given time interval.
    """
    # NOTE: this depends on ops! How do i guarantee that this does not change?
    base_url = api_host.replace("api.", "monitoring.", 1).rstrip("/")
    url = f"{base_url}/graylog/search"

    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return f"{url}?from={start_time_str}&to={end_time_str}"


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    Hook to capture the start time of each test.
    """
    _test_start_times[item.name] = _utc_now()


# SEE https://docs.pytest.org/en/7.1.x/example/simple.html


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to add extra information when a test fails.
    """
    outcome = yield
    rep = outcome.get_result()

    if call.when == "call" and rep.failed:
        test_name = item.name
        test_location = item.location
        api_host = os.environ.get("OSPARC_API_HOST", "")

        diagnostics = {
            "test_name": test_name,
            "test_location": test_location,
            "api_host": api_host,
        }

        # Get the start and end times of the test
        start_time = _test_start_times.get(test_name)
        end_time = _utc_now()

        if start_time:
            diagnostics["graylog_url"] = _construct_graylog_url(
                api_host, start_time, end_time
            )
            diagnostics["duration"] = str(end_time - start_time)

        # Print the diagnostics
        print(f"\nDiagnostics for {test_name}:\n")
        for key, value in diagnostics.items():
            print("  ", key, ":", value)

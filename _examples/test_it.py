import json
import logging
import sys
from pathlib import Path
from threading import Thread

import pytest
from pytest_mock import MockerFixture, MockType
from tenacity import Retrying, TryAgain
from tenacity.before import before_log
from tenacity.wait import wait_fixed

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logger = logging.getLogger(__name__)


def check_file_and_execute(state, input3: Path):

    for attempt in Retrying(
        wait=wait_fixed(state.check_interval),
        before=before_log(logger, logging.INFO),
        reraise=True,
    ):
        with attempt:

            input_3_sim_state_file = list(input3.glob("*.json"))

            if input_3_sim_state_file:
                state.sim_status = json.loads(input_3_sim_state_file[0].read_text())
                if not (
                    state.sim_status["isotropic"]["empty"]
                    and state.sim_status["anisotropic"]["empty"]
                ):
                    state.elec_select.disabled = True
                    break  # STOP!

            raise TryAgain


@pytest.fixture
def personalizer_gui_self(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.check_interval = 0.1
    mock.elec_select.disabled = False
    return mock


def test_it(tmp_path: Path, personalizer_gui_self: MockType):

    input_file = tmp_path / "input.json"
    input_file.write_text(
        json.dumps(
            {
                "isotropic": {
                    "empty": False,
                },
                "anisotropic": {
                    "empty": True,
                },
            },
        )
    )

    check_file_and_execute(personalizer_gui_self, input_file.parent)

    assert personalizer_gui_self.elec_select.disabled == True


def test_that(tmp_path: Path, personalizer_gui_self: MockType):
    input_file = tmp_path / "input.json"
    input_file.write_text(
        json.dumps(
            {
                "isotropic": {
                    "empty": True,
                },
                "anisotropic": {
                    "empty": True,
                },
            },
        )
    )

    th = Thread(
        target=check_file_and_execute, args=(personalizer_gui_self, input_file.parent)
    )
    th.start()

    assert th.is_alive()

    th.join(timeout=1)
    assert personalizer_gui_self.elec_select.disabled == True

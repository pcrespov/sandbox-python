import json
import logging

from tenacity import Retrying
from tenacity.before_sleep import before_sleep_log
from tenacity.stop import stop_after_delay
from tenacity.wait import wait_random

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


def main():

    for attempt in Retrying(
        wait=wait_random(0.5, 1),
        stop=stop_after_delay(5),
        reraise=True,
        before_sleep=before_sleep_log(log, logging.WARNING),
    ):
        with attempt:

            if attempt.retry_state.attempt_number < 5:
                raise ValueError("error, please retry")

            # if it reaches this point, it is because it was not raised
            # and therefore the attmpt succeded
            # WARNING: it needs to be inside of the context !!!
            log.info(
                "Some stats of what happened: %s",
                json.dumps(attempt.retry_state.retry_object.statistics, indent=2),
            )


if __name__ == "__main__":
    main()

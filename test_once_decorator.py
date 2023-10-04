#
# TODO: compare with
# services/api-server/src/simcore_service_api_server/utils/app_data.py
# services/api-server/src/simcore_service_api_server/utils/client_base.py

import functools
import logging


def run_once(*, raise_for_rerun: bool = False):
    def _decorator(class_method):
        def _wrapper(cls, *args, **kwargs):
            if not _wrapper.has_run:
                _wrapper.has_run = True
                return class_method(cls, *args, **kwargs)

            msg = f"{class_method.__name__} has already been executed and will not run again."
            if raise_for_rerun:
                raise RuntimeError(msg)
            logging.warning(msg)
            return None

        _wrapper.has_run = False
        return functools.wraps(_wrapper)

    return _decorator

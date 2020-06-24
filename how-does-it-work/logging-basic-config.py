#
# https://docs.python.org/3/library/logging.html#logging.basicConfig
#

import logging

# Normal usage of logging.basicConfig:
#
# It is a convenience method intended for use by simple scripts to do one-shot configuration of the logging package.
#
# ===> This function DOES NOTHING if the root logger already has handlers  configured

assert logging.root == logging.getLogger()
assert not logging.root.handlers
# logging.basicConfig(level=logging.DEBUG)


def logit(log):
    print("{:*^100}".format(str(log)))

    if log is not logging:
        print(log.handlers)

    log.critical("Really bad")
    log.error("Bad")
    log.warning("Careful")
    log.info("FYI")
    log.debug("BTW")


def main():

    # logging.basicConfig(level=logging.DEBUG)

    # setting level DOES NOT creates handler
    assert not logging.root.handlers
    logging.root.setLevel(logging.DEBUG)  # ensures root level
    assert not logging.root.handlers

    logit(logging)  # lazy generation of handlers as soon as a log is written
    assert len(logging.root.handlers) == 1
    # import pdb; pdb.set_trace()
    assert logging.root.level == logging.DEBUG

    # therefore thisone DOES NOTHING
    logging.basicConfig(level=logging.CRITICAL)

    logit(logging.root)
    ## logging.root.setLevel(logging.DEBUG)
    logit(logging.getLogger("A"))
    logit(logging.getLogger("A.B"))
    logit(logging.getLogger("A.C"))


main()

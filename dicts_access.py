#
# Q? what is more convenent to access a dict
#
# Based on https://github.com/ITISFoundation/osparc-simcore/pull/2582#discussion_r727763772
#
#
#
# SEE  https://towardsdatascience.com/when-and-why-to-use-over-in-python-b91168875453
#

#
# Q: two options, which one is the most convenient and when?
#


def if_colon_eq_then_safe_get(key, data):
    if value := data.get(key):
        return value


def if_contains_and_get(key, data):
    if key in data:
        return data[key]


DATA = {k: k for k in range(10_000_000)}


if __name__ == "__main__":
    import timeit
    import dis

    for fun in (if_contains_and_get, if_colon_eq_then_safe_get):
        print("---------" * 10)
        print(dis.code_info(fun))

        print("bytecode", "---------")
        dis.dis(fun)

        print("timeit", "---------")
        code = (
            f"from dicts_access import {fun.__name__}, DATA;"
            f" {fun.__name__}(1234, DATA) == 1234"
        )
        print(f"test code: '{code}'")
        print(
            "Took",
            timeit.timeit(code),
            "secs",
        )

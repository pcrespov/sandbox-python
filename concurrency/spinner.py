import functools
import itertools
import sys
import threading
import time


class Signal:
    go: bool = True


BACKSPACE = "\x08"


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        snapshot = char + " " + msg
        write(snapshot)
        flush()
        write(BACKSPACE * len(snapshot))
        time.sleep(0.1)
        if not signal.go:
            break
    write(" " * len(snapshot) + BACKSPACE * len(snapshot))


def monitor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        signal = Signal()
        spinner = threading.Thread(target=spin, args=("bhat are u zinking!", signal))
        spinner.start()
        try:
            result = func(*args, **kwargs)
        finally:
            signal.go = False
            spinner.join()
        return result

    return wrapper


@monitor
def slow_function():
    time.sleep(3)
    return True


def main():
    res = slow_function()
    print("slept", res)



if __name__ == "__main__":
    main()
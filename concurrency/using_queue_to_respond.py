#
# SEE examples in https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
#
#

import multiprocessing as mp
import time


def print_symbols(symbol, repeat_count=1):
    for n in range(repeat_count):
        time.sleep(1)
        print(symbol)


def worker_func(reply_queue, repeat_print: int):
    print("WORKER: started")

    print_symbols(".", repeat_count=repeat_print)

    # replies and continue working
    reply_queue.put("Done with all '.', now I print 'o'")

    print_symbols("o", repeat_count=repeat_print)
    print("WORKER: done")


def main():
    print("MAIN: started")

    # ---
    reply_queue = mp.Queue()

    mp.Process(target=worker_func, args=(reply_queue, 3), daemon=True).start()

    response = (
        reply_queue.get()
    )  # unblocks as soon as it gets a reply, but worker can continue executing until it finishes

    # ---
    print(f"MAIN: worker said '{response}', now I print 'x' ")
    print_symbols("x", 10)

    print("MAIN: done")


if __name__ == "__main__":
    main()

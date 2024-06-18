import multiprocessing
import time
from contextlib import contextmanager, suppress
from multiprocessing import shared_memory

_the_shared_memory_name = "field_loader_shm"


@contextmanager
def semaphore_guard(semaphore: multiprocessing.Semaphore):
    acquired = semaphore.acquire(block=False)
    try:
        yield acquired
    finally:
        if acquired:
            semaphore.release()


def is_unique_shared_memory_allocated() -> bool:
    try:
        shm = shared_memory.SharedMemory(name=_the_shared_memory_name, create=False)
        shm.close()
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False


@contextmanager
def unique_shared_memory_lifespan(size):
    shm = shared_memory.SharedMemory(
        name=_the_shared_memory_name, create=True, size=size
    )
    try:
        yield shm
    finally:
        with suppress(Exception):
            shm.close()
            shm.unlink()
            print("deallocating")


def task(semaphore, task_id):
    with semaphore_guard(semaphore) as is_green:
        if is_green:
            print(task_id, "running")
            with unique_shared_memory_lifespan(size=10000000) as shm:
                print(shm.name, len(shm.buf))

                assert is_unique_shared_memory_allocated()

                time.sleep(10)

            assert not is_unique_shared_memory_allocated()
        else:
            print(task_id, "skipping")


def run_concurrent_tasks(num_tasks):
    the_semaphore = multiprocessing.Semaphore(1)
    processes = []

    for i in range(num_tasks):
        p = multiprocessing.Process(target=task, args=(the_semaphore, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    run_concurrent_tasks(num_tasks=10)

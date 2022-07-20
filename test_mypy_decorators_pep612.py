## https://peps.python.org/pep-0612/


from typing import Awaitable, Callable, TypeVar
import asyncio


R = TypeVar("R")


def sleep_n_run(delay: int):
    def decorator(f: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        async def inner(*args: object, **kwargs: object) -> R:
            await asyncio.sleep(delay)
            return await f(*args, **kwargs)

        return inner

    return decorator


@sleep_n_run(2)
async def takes_int_str(x: int, y: str) -> int:
    return x + 7


async def test_it():
    await takes_int_str(1, "A")
    await takes_int_str("B", 2)  # fails at runtime



    with tempfile.TemporaryDirectory(prefix=f"{__name__}_") as tmpdir:
        compose_path = Path(tmpdir) / "docker-compose.yml"
        compose_path.write_text(yaml_content)

        cmd = command.format(file_path=compose_path)

        logger.info("Runs %s ...\n%s", cmd, yaml_content)
        result = await async_command(
            command=cmd,
            timeout=process_termination_timeout,
        )
        logger.info("Done %s", pformat(deepcopy(result._asdict())))

        return result

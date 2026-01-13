
.PHONY: test1 test2

test1:
	pytest --asyncio-mode auto  test_aiohttp_with_pytest_asyncio.py > $@.log 2>&1

test2:
	pytest --asyncio-mode strict  test_aiohttp_with_pytest_asyncio.py > $@.log 2>&1

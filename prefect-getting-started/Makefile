.PHONY: install up

install:
	pip install pip-tools
	pip-sync requirements.txt

demo:
	prefect backend server
	prefect server start

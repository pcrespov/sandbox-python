.PHONY: install up

install:
	pip install pip-tools
	pip-sync requirements.txt

up:
	uvicorn ds.main:the_app --host 0.0.0.0 --reload --reload-dir ds 

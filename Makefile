SHELL := /bin/bash
.DEFAULT_GOAL := help


REPO_BASE_DIR := $(shell git rev-parse --show-toplevel)


.PHONY: devenv
devenv: .venv ## Creates a python virtual environment in .venv and installs development tools (pip, pylint, ...)
.venv:
	@python3 -m venv .venv
	@.venv/bin/pip3 install --upgrade pip wheel setuptools
	@.venv/bin/pip3 install -r requirements.txt
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


include Makefile.common
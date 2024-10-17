SHELL := /bin/bash
.DEFAULT_GOAL := help


REPO_BASE_DIR := $(shell git rev-parse --show-toplevel)


.PHONY: devenv
.venv:
	# create virtualenv
	uv venv
	# upgrade packages tools
	uv pip install --upgrade pip wheel setuptools

devenv: .venv ## create a python virtual environment with dev tools (e.g. linters, etc)
	# Install tooling
	uv pip install -r requirements.txt
	# Installing pre-commit hooks in current .git repo
	uvx pre-commit install
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


include Makefile.common

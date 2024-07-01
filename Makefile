SHELL := /bin/bash
.DEFAULT_GOAL := help


REPO_BASE_DIR := $(shell git rev-parse --show-toplevel)


.PHONY: devenv
.venv:
	# create virtualenv
	python3 -m venv .venv
	# upgrade packages tools
	.venv/bin/pip3 install --upgrade pip wheel setuptools

devenv: .venv ## create a python virtual environment with dev tools (e.g. linters, etc)
	# Install tooling
	$</bin/pip3 install -r requirements.txt
	# Installing pre-commit hooks in current .git repo
	@$</bin/pre-commit install
	@$</bin/pip3 list -v
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


include Makefile.common

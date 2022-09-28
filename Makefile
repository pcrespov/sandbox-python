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
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


.PHONY: autoformat
autoformat: ## runs black python formatter on this service's code. Use AFTER make install-*
	# sort imports
	@python3 -m isort --atomic -rc $(CURDIR)
	# auto formatting with black
	@python3 -m black --verbose \
		--exclude "/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist|migration|client-sdk|generated_code)/" \
		$(CURDIR)



# CLEAN

.PHONY: clean .check-clean

.check-clean:
	@git clean -ndxf -e .vscode/
	@echo -n "$(shell whoami) are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean-hooks: ## Uninstalls git pre-commit hooks
	@-pre-commit uninstall 2> /dev/null || rm .git/hooks/pre-commit


clean:.check-clean  ## Cleans all unversioned files in project
	@git clean -dxf -e .vscode/


# HELP

.PHONY: help
help: ## This nice help (thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

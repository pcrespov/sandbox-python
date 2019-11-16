SHELL := /bin/bash


.PHONY: help
help: ## This nice help (thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help


.PHONY: devenv
devenv: .venv ## Creates a python virtual environment in .venv and installs development tools (pip, pylint, ...)
.venv:
	@python3 -m venv .venv
	@.venv/bin/pip3 install --upgrade pip wheel setuptools
	@.venv/bin/pip3 install -r requirements.txt
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


.PHONY: clean .check-clean

.check-clean:
	@git clean -ndxf -e .vscode/
	@echo -n "$(shell whoami) are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean:.check-clean  ## Cleans all unversioned files in project
	@git clean -dxf -e .vscode/
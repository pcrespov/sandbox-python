# Recipes to build and run pytest-fixture-tools in a container
#
#
# SEE https://github.com/pytest-dev/pytest-fixture-tools
#

REPODIR:=$(abspath $(CURDIR)/../..)
IMAGE_NAME:=local/pytest-fixture-tools:latest


.PHONY: build
build: ## builds image with pytest tooling
	docker build --tag $(IMAGE_NAME) .


.PHONY: shell
shell: ## opens a shell to run pytest-fixture-tools (e.g. pytest --fixture-graph -s)
	docker run -it \
		--workdir="/home/$(USER)" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
		--volume="/etc/shadow:/etc/shadow:ro" \
		--volume=$(REPODIR):/home/$(USER) \
		--user=$(shell id -u):$(shell id -g) \
		--entrypoint=/bin/bash \
		$(IMAGE_NAME)


# NOTE: this container needs to install python as the host does.
# - needs to be able to install package/service and all its dependencies
# - some tests need e.g. access to the docker  etc
# - host enforces using a virtualenv
# - Ideally this is somethign that can be added in the test stage!
# - For the moment is should only be used to reference graphviz

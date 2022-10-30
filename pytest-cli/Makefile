



.PHONY: build
build:
	docker build -t local/pytest-cli:latest .


.PHONY: shell
shell:
	docker run -it \
	--volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --user="$(shell id --user "$(USER)")":"$(shell id --group "$(USER)")" \
	--entrypoint bash local/pytest-cli:latest

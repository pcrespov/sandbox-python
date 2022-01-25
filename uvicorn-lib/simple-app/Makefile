

.PHONY: build
build:
	docker build -t local/simple-app:latest .


.PHONY: shell
shell:
	docker run -it \
		--workdir="/home/$(USER)/requirements/tools" \
		--volume="/etc/group:/etc/group:ro" \
    	--volume="/etc/passwd:/etc/passwd:ro" \
		--volume=$(CURDIR):/home/$(USER) \
		--user=$(shell id -u):$(shell id -g) \
		local/simple-app:latest \
		bash
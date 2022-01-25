

.PHONY: build
build:
	docker build -t local/simple-app:latest .


.PHONY: shell
shell:
	docker run -it --user $(shell id -u):$(shell id -g) -v $(CURDIR):/devel --workdir /devel local/simple-app:latest bash
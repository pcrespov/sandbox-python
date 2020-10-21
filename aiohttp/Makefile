clean:
	@rm -rf `find . -name __pycache__`
	@git clean -dXf

.venv:
	python3 -m venv .venv
	.venv/bin/pip3 install --upgrade pip wheel setuptools
	@echo "To activate the venv, execute 'source .venv/bin/activate'"

# FIXME: build with context in repo
#images:
#	docker build -t swagger-codegen-test -f modules/swagger-codegen-cli/Dockerfile https://github.com/swagger-api/swagger-codegen.git
# or??
# 	docker build -t swagger-codegen-test -f modules/swagger-codegen-cli/Dockerfile https://github.com/swagger-api/swagger-codegen/archive/v2.3.1.tar.gz

.PHONY: clean images

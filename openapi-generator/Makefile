
GENERATOR_NAME :=python-experimental
USERID         := $(shell stat --format=%u "$(CURDIR)")
GROUPID        := $(shell stat --format=%g "$(CURDIR)")
CONFIG_FILE    := additionalProperties_${GENERATOR_NAME}.yml

# FIXME: replaces automatically $PWD by /local so it maps correctly in the container
#PATTERN=s+$PWD+/local+
#CMD=$(echo "$@" | sed $PATTERN)

# TODO: check SAME digest. Perhaps push into itisfoundation repo?
# openapitools/openapi-generator-cli   v4.2.3   sha256:c90e7f2d63340574bba015ad88a5abb55d5b25ab3d5460c02e14a566574e8d55

.PHONY: help
help:
	@docker run --rm \
		--user "${USERID}:${GROUPID}" \
		openapitools/openapi-generator-cli help

.PHONY: version
version:
	@docker run --rm \
		--user "${USERID}:${GROUPID}" \
		openapitools/openapi-generator-cli version

.PHONY: shell
shell:
	# NOTE: use '/usr/local/bin/docker-entrypoint.sh' to run openapi-generator-cli
	@docker run -it \
		--user "${USERID}:${GROUPID}" \
		--volume "$(CURDIR)":/local \
		--workdir /local \
		--env PYTHON_POST_PROCESS_FILE=black \
		--entrypoint bash \
		openapitools/openapi-generator-cli



.PHONY: list
list:
	## List of the available generators
	@docker run --rm \
		--user "${USERID}:${GROUPID}" \
		openapitools/openapi-generator-cli list \
		--short \
		| tr ',' '\n' \
		| grep python


.PHONY: config-help
config-help:
	@docker run --rm \
		--user "${USERID}:${GROUPID}" \
		openapitools/openapi-generator-cli config-help \
		--full-details \
		--generator-name ${GENERATOR_NAME}


${CONFIG_FILE}:
	@docker run --rm \
		--user "${USERID}:${GROUPID}" \
		--volume "$(CURDIR)":/local \
		openapitools/openapi-generator-cli config-help \
		--full-details \
		--format yamlsample \
		--generator-name ${GENERATOR_NAME} \
		--output /local/$@


petstore.json:
	wget https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.json



.PHONY: generate
generate: petstore.json ${CONFIG_FILE}
	# SEE https://openapi-generator.tech/docs/usage#generate
	# auto-generate
	docker run --rm \
		--user "${USERID}:${GROUPID}" \
		--volume "$(CURDIR)":/local \
		--env PYTHON_POST_PROCESS_FILE=black \
		openapitools/openapi-generator-cli generate \
		--api-name-suffix api\
		--config /local/${CONFIG_FILE} \
		--generator-name ${GENERATOR_NAME} \
		--git-host github.com \
		--git-repo-id sandbox-python \
		--git-user-id pcrespov \
		--global-property verbose=true \
		--global-property apiDocs=false \
		--global-property apiTests=false \
		--global-property modelTests=false \
		--http-user-agent "osparc/{packageVersion}/{language}" \
		--input-spec /local/petstore.json \
		--output /local/out/${GENERATOR_NAME}

	# auto-format
	find ./out -type f -name "*.py" | xargs black


.PHONY: template
template: petstore.json ${CONFIG_FILE}
	# auto-generate
	docker run --rm \
		--user "${USERID}:${GROUPID}" \
		--volume "$(CURDIR)":/local \
		openapitools/openapi-generator-cli author template \
		-g ${GENERATOR_NAME} \
		--verbose \
		-o /local/template/${GENERATOR_NAME}



.PHONY: clean
clean:
	git clean -xfd $(CURDIR)

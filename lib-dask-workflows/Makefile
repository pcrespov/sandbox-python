include ../Makefile

.PHONY: install up

install: ## pip-syncs requirements
	pip install pip-tools
	pip-sync requirements.txt

# 
STACKNAME:=osparc_dask
export ${STACKNAME}

init:
	docker swarm init

up:
	docker stack deploy --compose-file docker-compose.yml ${STACKNAME}
down:
	docker stack rm ${STACKNAME}
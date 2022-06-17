
# LOCAL DEV --------------------

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: start
start:
	uvicorn server:app --reload


# CONTAINERS --------------------
NAME_PREFIX:=$(notdir $(CURDIR))

.PHONY: build up down 
build:
	docker-compose build
up:
	docker-compose up
down:
	docker-compose down


.PHONY: shell
shell:
	docker-compose exec app bash

.PHONY: info-%
info-specs:
	# services compose-specs
	@cat docker-compose.yml | yq ".services"

CONTAINER_ID = $(shell docker ps -q -f  "name=${NAME_PREFIX}_myapp*")

info-run:
	# config 
	-@docker inspect ${CONTAINER_ID} | jq ".[0].Config"
	# state
	-@docker inspect ${CONTAINER_ID} | jq ".[0].State"


# SERVICES --------------------
SWARM_HOSTS  = $(shell docker node ls --format="{{.Hostname}}" 2>/dev/null)
SWARM_STACK_NAME = ${NAME_PREFIX}
SERVICE_ID = $(shell docker service ls -q -f  "name=${NAME_PREFIX}_myapp")


.PHONY: .init-swarm leave stack remove

.init-swarm:
	# Ensures swarm is initialized
	$(if $(SWARM_HOSTS),,docker swarm init)

stack: .init-swarm ## Deploys services stack
	docker stack deploy --with-registry-auth -c docker-compose.yml ${SWARM_STACK_NAME}

stack-rm: ## Stops and removes services stack
	# Removing stacks in reverse order to creation
	-@$(foreach stack,\
		$(shell docker stack ls --format={{.Name}} | tac),\
		docker stack rm $(stack);)

swarm-leave: ## Forces to stop all services, networks, etc by the node leaving the swarm
	-docker swarm leave -f


info-service:
	docker service inspect ${SERVICE_ID} | jq '.[0] | keys'
	docker service inspect  ${SERVICE_ID} | jq '.[0].Spec'
	docker service inspect  ${SERVICE_ID} | jq '.[0].UpdateStatus'




info-swarm: ## displays info about stacks and networks
ifneq ($(SWARM_HOSTS), )
	# Stacks in swarm
	@docker stack ls
	# Containers (tasks) running in '$(SWARM_STACK_NAME)' stack
	-@docker stack ps $(SWARM_STACK_NAME)
	# Services in '$(SWARM_STACK_NAME)' stack
	-@docker stack services $(SWARM_STACK_NAME)
	# Networks
	@docker network ls
endif

# APP TESTS --------------------
# can also be down via http://localhost:8000/docs

.PHONY: test-%
test-hi:
	# SEE  http://localhost:8000/docs
	curl -v http://localhost:8000/hi

test-raise:
	# SEE  http://localhost:8000/docs
	curl -v -X POST http://localhost:8000/raise



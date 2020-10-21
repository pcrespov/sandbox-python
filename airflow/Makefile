export AIRFLOW_HOME := $(CURDIR)

.venv:
	python3 -m venv .venv
	pip install -U pip setuptools wheel

.PHONY: devenv
devenv: .venv
	@.venv/bin/pip --quiet install -r requirements.txt
	@echo Type 'source .venv/bin/activate'

.PHONY: _check_venv_active
_check_venv_active:
	# checking whether virtual environment was activated
	@python3 -c "import sys; assert sys.base_prefix!=sys.prefix"

.PHONY: autoformat
autoformat: _check_venv_active ## cause I am an elegant coder ;-)
	isort --atomic . 
	black .


# airflow ------
dags = $(wildcard dags/*.py)

.PHONY: init
init: .venv
	@echo "Airflow version" $(shell .venv/bin/airflow version)
	# init db
	airflow initdb
	
.PHONY: register
register: $(dags)
	# registering some dags
	$(foreach d,$(dags),python3 $(d);)

.PHONY: check
check: _check_venv_active ## validation
	# list of active DAGs
	@airflow list_dags

.PHONY: webserver
webserver: _check_venv_active
	@airflow webserver --debug
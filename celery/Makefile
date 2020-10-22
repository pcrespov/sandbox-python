

.PHONY: install
install:
	pip install -r requirements.txt


.PHONY: up
up:
	# deploying broker, results backend and some monitoring sugar
	docker-compose up


.PHONY: workers
workers:
	# starts two workers on normal queue
	celery --app tasks worker --concurrency 2 --loglevel INFO

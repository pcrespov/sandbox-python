include ../Makefile.common


.PHONY: openapi openapi.json
openapi: openapi.json ## generates OAS
openapi.json: 
	# generating $@
	python create_openapi.py

.PHONY: auto-models auto_models.py
auto-models: auto_models.py ## auto-generates models from OAS
auto_models.py: openapi.json
	datamodel-codegen \
		--input $< \
		--output $@ \
		--field-constraints \
		--reuse-model \
		--enum-field-as-literal=all

	# formats
	@black $@

test: ## tests auto-generated model
	python -c "import auto_models"
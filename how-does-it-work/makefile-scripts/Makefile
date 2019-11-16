SHELL = /bin/bash

MSG = $(shell bash helpers-w-entrypoint.sh get_message)
MSG2 = $(shell source helpers.sh && get_message)


.PHONY: test
test:
	@echo $(MSG)
	@echo $(MSG2)

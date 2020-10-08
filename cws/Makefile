
run1:
	cd 1; cwl-runner --debug 1st-tool.cwl echo-job.yml 


run2:
	cd 2; touch whale.txt; \
	cwl-runner --debug input.cwl input-job.yml

run3:
	cd 3; \
	touch hello.txt && tar -cvf hello.tar hello.txt; \
	cwl-runner --debug tar.cwl tar-job.yml

run4:
	cd 4; \
	cwl-runner --debug stdout.cwl echo-job.yml
.venv:
	python3 -m venv .venv
	.venv/bin/pip install -U pip setuptools wheel

.PHONY: devenv
devenv: .venv
	.venv/bin/pip install -r requirements.txt
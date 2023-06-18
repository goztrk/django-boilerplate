SHELL := /bin/bash # Use bash syntax
ARG := $(word 2, $(MAKECMDGOALS) )

clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete

compile_install_requirements:
	@echo 'Installing pip-tools...'
	export PIP_REQUIRE_VIRTUALENV=true; \
	pip install pip-tools
	@echo 'Compiling requirements...'
	pip-compile --resolver=backtracking --output-file requirements.txt
	pip-compile --resolver=backtracking requirements-dev.in --output-file requirements-dev.txt
	@echo 'Installing requirements...'
	pip install -r requirements.txt && pip install -r requirements-dev.txt

upgrade: ## update the requirements*.txt files with the latest packages satisfying requirements*.in
	pip install -U -q pip-tools
	pip-compile --upgrade -o requirements-dev.txt requirements-dev.in
	pip-compile --upgrade -o requirements.txt requirements.in
	# Make everything =>, not ==
	sed 's/==/>=/g' requirements.txt > requirements.tmp
	mv requirements.tmp requirements.txt

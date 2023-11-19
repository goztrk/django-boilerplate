SHELL := /bin/bash # Use bash syntax
ARG := $(word 2, $(MAKECMDGOALS) )
SCSS=core/scss
STATIC=static

clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete

compile-scss:
	pysassc $(SCSS)/style.scss $(STATIC)/css/style.css -s compressed

compile-scss-debug:
	pysassc $(SCSS)/style.scss $(STATIC)/css/style.css --sourcemap

watch-scss:
	watchmedo shell-command --patterns=*.scss --ignore-patterns="node_modules/*" --recursive --ignore-directories --command="make compile-scss-debug"

compile-install-requirements:
	@echo 'Installing pip-tools...'
	export PIP_REQUIRE_VIRTUALENV=true; \
	./venv/bin/pip install pip-tools
	@echo 'Compiling requirements...'
	./venv/bin/pip-compile --resolver=backtracking --output-file requirements.txt
	./venv/bin/pip-compile --resolver=backtracking requirements-dev.in --output-file requirements-dev.txt
	@echo 'Installing requirements...'
	./venv/bin/pip install -r requirements.txt && pip install -r requirements-dev.txt

upgrade: ## update the requirements*.txt files with the latest packages satisfying requirements*.in
	./venv/bin/pip install -U -q pip-tools
	./venv/bin/pip-compile --upgrade -o requirements-dev.txt requirements-dev.in
	./venv/bin/pip-compile --upgrade -o requirements.txt requirements.in
	# Make everything =>, not ==
	sed 's/==/>=/g' requirements.txt > requirements.tmp
	mv requirements.tmp requirements.txt

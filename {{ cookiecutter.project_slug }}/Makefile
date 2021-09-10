.PHONY: help
SHELL := /bin/bash
PROJECT_NAME = {{ cookiecutter.project_slug }}
SHARED_FOLDER=/tmp/shared-docker-$(shell date +%Y%m%d_%H%M%S)

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, optimized files, logs, cache, coverage...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -fr .pytest_cache/
	@rm -f coverage.xml
	@rm -f *.log
	@find . -name "celerybeat-schedule*" | xargs rm -rf

init-env:  ## create a .env file with the environment variables.
	@cp etc/env.sample .env
	@echo '.env file initialized at the project root. Customize it as you may.'

requirements:  ## Install pip requirements
	@pip install --upgrade pip
	@pip install -r requirements.txt

runserver-dev:  ## Run flask development server
	set -a && source .env && set +a && python dev-server.py

runserver: init-env ## Run gunicorn production server
	 # Gunicorn needs to bind to 0.0.0.0 so to be able to receive requests from the docker network,
	 # otherwise it will only receive them locally. With '-' logs are redirected to stdout (because containers)
	 # /dev/shm tells to the workers to use shared memory, and in-memory filesystem, instead of
	 # using files, which are slower and can degrade performance - and are not a good practice for
	 # containers anyhow, since they must redirect all of theirs logs to stdout/stderr.
	 set -a && source .env && set +a && gunicorn --worker-tmp-dir /dev/shm -c gunicorn_settings.py {{ cookiecutter.project_slug }}:app -b 0.0.0.0:5000 --log-level INFO  --access-logfile '-' --error-logfile '-'

shell:  ## initialize a shell
	 set -a && source .env && set +a && flask shell

routes:  ## show all configured api routes
	 set -a && source .env && set +a && flask routes

api-test:  ## make a request with curl to check the app is responding
	@curl -i -L http://localhost:5000/welcome/you

style:	## Run isort and black auto formatting code style in the project
	@echo 'running isort...'
	@isort -m 3 --trailing-comma --use-parentheses --honor-noqa .
	@echo 'running black...'
	@black -S -t py39 -l 79 $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|build|dist)/'

style-check:  ## Run isort and black check code style
	@echo 'isort check...'
	@isort -v --check -m 3 --trailing-comma --use-parentheses --honor-noqa --color .
	@echo 'black check...'
	@black -S -t py37 -l 79 --check $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|build|dist)/'

docker-build-local-app: clean  ## Build local docker image (app)
	@./scripts/build-docker-image.sh $(PROJECT_NAME)

docker-run-local-app-container: clean  ## Run the app docker image locally
	echo "You can exchange files with the container on the directory $(SHARED_FOLDER) on the host and /shared on the container."
	@mkdir -p $(SHARED_FOLDER)
	$(eval IMAGE_NAME=$(shell bash -c "docker images| grep $(PROJECT_NAME)| grep `cat VERSION` | grep -v slim | cut -d ' ' -f 1"))
	@echo "IMAGE_NAME=$(IMAGE_NAME)"
	@echo '---'
	@echo 'Below is the CONTAINER_ID:'
	@docker run --rm -d -p 5000:5000 --name {{ cookiecutter.project_slug }} --env-file .env --network bridge ${IMAGE_NAME}

podman-build-local-app: clean  ## Build local podman image (app)
	@./scripts/build-podman-image.sh $(PROJECT_NAME)

podman-run-local-app-container: clean  ## Run the app podman image locally
	echo "You can exchange files with the container on the directory $(SHARED_FOLDER) on the host and /shared on the container."
	@mkdir -p $(SHARED_FOLDER)
	$(eval IMAGE_NAME=$(shell bash -c "podman images| grep $(PROJECT_NAME)| grep `cat VERSION` | grep -v slim | cut -d ' ' -f 1"))
	@echo "IMAGE_NAME=$(IMAGE_NAME)"
	@echo '---'
	@echo 'Below is the CONTAINER_ID:'
	@podman run --rm -d -p 5000:5000 --name {{ cookiecutter.project_slug }} --network bridge ${IMAGE_NAME}

lint:  ## Run the linter to enforce our coding practices
	@printf '\n --- \n >>> Running linter...<<<\n'
	@pylint --rcfile=.pylintrc $(PROJECT_NAME)/*
	@printf '\n FINISHED! \n --- \n'

test: clean  ## Run the test suite
	@cd $(PROJECT_NAME) && py.test -s -vvv

coverage: clean  ## Run the test coverage report
	@py.test --cov-config .coveragerc --cov $(PROJECT_NAME) $(PROJECT_NAME) --cov-report term-missing

local-healthcheck-readiness:  ## Run curl to make sure the app/worker is ready
	@curl http://localhost:5000/health-check/readiness

local-healthcheck-liveness:  ## Run curl to make sure the app/worker is live
	@curl http://localhost:5000/health-check/liveness

api-docs:  ## Show api docs (must be run on a desktop linux machine, with the app running locally)
	@xdg-open http://localhost:5000/apidocs



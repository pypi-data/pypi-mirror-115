
.PHONY: all

-include .env

SHELL=/bin/bash -e

.DEFAULT_GOAL := all

DOCKER_COMPOSE_DIR=`pwd`/docker-compose
DOCKER_COMPOSE_FILE=${DOCKER_COMPOSE_DIR}/docker-compose.yml
DOCKER_COMPOSE_CMD=docker-compose
PROJECT=django-absractions
IMAGE=${PROJECT}:latest


help:
	cat README.md

#####################
### Docker config ###
#####################

build_image:
	@echo "Build docker image ${IMAGE}"
	docker build --network host -t ${IMAGE} .

build:
	@echo "Build docker for testing compose"
	${DOCKER_COMPOSE_CMD} -f ${DOCKER_COMPOSE_FILE} -p ${PROJECT} build

clean_test:
	@echo "clean after testing"
	@${DOCKER_COMPOSE_CMD} -f ${DOCKER_COMPOSE_FILE} -p ${PROJECT} down -v

run:
	# уже есть проверка на готовность базы данных. Ждать не нужно.
	@${DOCKER_COMPOSE_CMD} -f ${DOCKER_COMPOSE_FILE} -p ${PROJECT} run web bash -c 'pytest --migrations -vvv -W ignore::pytest.PytestDeprecationWarning'

run_analyzer:
	@${DOCKER_COMPOSE_CMD} -f ${DOCKER_COMPOSE_FILE} -p ${PROJECT} run web flake8 -v

clean:
	@echo "Clean data"
	@${DOCKER_COMPOSE_CMD} -f ${DOCKER_COMPOSE_FILE} -p ${PROJECT} down -v

docker_up:  ## Up the local config
	@docker-compose -f docker-compose.yml  up -d --remove-orphans


docker_down:  ## Stop containers
	@docker-compose -f docker-compose.yml down

purge_images:
	@docker rmi $(docker images -a -q)

docker_rm_dc:
	@docker rm $(docker ps --filter status=exited -q)



##################
### Local work ###
##################

flake8:
	@flake8 -v

test:
	@coverage run -m pytest


migrations:
	@python ./manage.py makemigrations
	@python ./manage.py migrate

create_cache_table:
	@python ./manage.py createcachetable

git_current_branch_tab_show:
	@git describe --exact-match --tags 2> /dev/null || git rev-parse --short HEAD

#################
### Packages ###
#################


requirements_install:
	@pip install -r requirements.txt

requirements_uninstall:
	@pip freeze | grep -v "pkg-resources" | grep -v "github.com" | xargs -r pip uninstall -y


requirements_dev_install:
	@pip install -r dev.requirements.txt


requirements_freeze:
	@pip freeze > ./requirements.txt
	@cat ./requirements.txt

publish:
	@rm -f  ./dist/*
	@python setup.py sdist bdist_wheel --universal
	@pip install twine
	twine upload dist/* -u riros -p ${TWINE_PASSWORD}

#################
### Shortcuts ###
#################

requirements_upgrade: requirements_uninstall requirements_dev_install requirements_freeze

docker_update: docker_down docker_up
all: build_image build run run_analyzer clean



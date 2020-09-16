NAME=$(shell basename $(PWD))
PYTHON:=3.7

DOCKER=docker run \
	   --rm -it \
	   --name $(NAME)-tests \
	   -v $(PWD):/$(NAME) \
	   --rm $(NAME):latest

.PHONY: black
black:
	poetry run black --check .

.PHONY: docker
docker:
	docker build \
	--build-arg PYTHON=$(PYTHON) \
	--build-arg NAME=$(NAME) \
	-t $(NAME):latest \
	-f Dockerfile \
	.

.PHONY:docker-tests
docker-tests: docker
	$(DOCKER) make tests

.PHONY: mypy
mypy:
	poetry run mypy .

.PHONY: pylama
pylama:
	poetry run pylama .

.PHONY: pytest
pytest:
	poetry run pytest


.PHONY: tests
tests: black pylama mypy pytest


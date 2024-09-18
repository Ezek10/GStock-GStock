.PHONY: help run  black flake pylint test docker-up


help:
	@echo "run: run the project locally"
	@echo "black: format code"
	@echo "flake: lint the code"
	@echo "pylint: lint the code"
	@echo "test: run the tests"
	@echo "docker-up: run docker"

run:
	uvicorn src.main.app:app --reload --env-file .env

black:
	black src

flake:
	flake8 src

pylint:
	pylint src

test:
	pytest --cov --cov-config=.coveragerc --cov-report=html

install:
	pip install -r requirements.txt

docker-up:
	docker-compose up -d

docker-push:
	docker build -t ezemarcel/gstock-users-api:1.1 .
	docker push ezemarcel/gstock-users-api:1.1

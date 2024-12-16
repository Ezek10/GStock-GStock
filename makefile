.PHONY: help run  black flake pylint test docker-up


help:
	@echo "run: run the project locally"
	@echo "lint: run linters"
	@echo "test: run the tests"
	@echo "docker-up: run docker"

run:
	uvicorn src.main.app:app --reload --env-file .env

lint:
	ruff check
	ruff format

test:
	pytest --cov --cov-config=.coveragerc --cov-report=html

install:
	pip install -r requirements.txt

docker-up:
	docker-compose up -d

docker-push:
	docker build -t ezemarcel/gstock-gstock-api:1.2 .
	docker push ezemarcel/gstock-gstock-api:1.2

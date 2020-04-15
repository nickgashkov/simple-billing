build:
	@docker-compose build

run: build migrate
	docker-compose up api

shell:
	@docker-compose run --rm api bash

lock:
	@docker-compose run --rm api pip-compile requirements/base.in
	@docker-compose run --rm api pip-compile requirements/dev.in

isort:
	@docker-compose run --rm api isort -rc .

lint:
	@docker-compose run --rm api flake8 .

mypy:
	@docker-compose run --rm api mypy .

test:
	@docker-compose run --rm api pytest

validate: build isort lint mypy test

migration:
	@docker-compose run --rm api dbmate -d "./billing/migrations" -s "./billing/migrations/schema.sql" -e BILLING_DB_DSN new $(message)

migrate:
	@docker-compose run --rm api dbmate -d "./billing/migrations" -s "./billing/migrations/schema.sql" -e BILLING_DB_DSN up

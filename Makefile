build:
	@docker-compose build

shell:
	@docker-compose run --rm api sh

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

validate:
	@make build
	@make isort
	@make lint
	@make mypy
	@make test

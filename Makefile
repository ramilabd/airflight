install:
	poetry install

start-app: selfcheck lint test
	@export FLASK_APP=airflight/app;	export FLASK_ENV=development;	poetry run python -m airflight.app

lint:
	poetry run flake8 airflight tests

test:
	poetry run pytest -v

test-coverage:
	poetry run pytest --cov=airflight tests/

selfcheck:
	poetry check

.PHONY: install test tests lint selfcheck check
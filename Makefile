install:
	poetry install

start-app: selfcheck lint test
	@export FLASK_APP=airflight/app;	export FLASK_ENV=development;	poetry run python -m airflight.app

test:
	poetry run pytest -v

lint:
	poetry run flake8 airflight tests

selfcheck:
	poetry check

.PHONY: install test tests lint selfcheck check
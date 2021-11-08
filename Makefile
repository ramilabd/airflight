install:
	poetry install

start-app: selfcheck lint test
	@export FLASK_APP=airflights/app;	export FLASK_ENV=development;	poetry run python -m airflights.app

lint:
	poetry run flake8 airflights tests

test:
	poetry run pytest -v

test-coverage:
	poetry run pytest --cov=airflights --cov-report xml tests/

selfcheck:
	poetry check

.PHONY: install test tests lint selfcheck check
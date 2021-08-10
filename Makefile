install:
	poetry install

start-app:
	@export FLASK_APP=airflight/app;	export FLASK_ENV=development;	poetry run python -m airflight.app

.PHONY: test
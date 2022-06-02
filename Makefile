lint:
	flake8 src tests
	isort src tests
	black src tests
test:
	pytest tests
run:
	ENV="dev" APP_VERSION="v0.1.0" python src/main.py

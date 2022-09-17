pylint:
	poetry run pylint differences_between_two_images

mypy:
	poetry run mypy differences_between_two_images

black:
	poetry run black .

pre-commit-install:
	poetry run pre-commit install

tests:
	poetry run pytest

check:
	black pylint mypy tests

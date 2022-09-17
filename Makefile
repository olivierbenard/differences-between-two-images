ping:
	echo "pong"

pylint:
	poetry run pylint

mypy:
	poetry run mypy

black:
	poetry run black

tests:
	poetry run pytest

check:
	black pylint mypy tests
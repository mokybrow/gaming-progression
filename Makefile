SOURCE_DIR_API=gaming_progression_api
TESTS_DIR=tests
LINE_LENGTH=120

pre-commit:
	pre-commit run --show-diff-on-failure

checks:
	poetry run isort ${TESTS_DIR}
	poetry run isort ${SOURCE_DIR_API}

	poetry run black ${TESTS_DIR}
	poetry run black ${SOURCE_DIR_API}

	poetry run mypy ${TESTS_DIR}
	poetry run mypy ${SOURCE_DIR_API}

	poetry run pytest -vv ${TESTS_DIR}

test:
	poetry run pytest -vv -s --disable-warnings ${TESTS_DIR}
run:
	poetry run python -m $(SOURCE_DIR_API)

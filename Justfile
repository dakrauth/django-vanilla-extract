# Display recipe listings
help:
    @just --list

# Initial development,test, and example environment
init:
    uv sync --dev

# Run example project
example: init
    uv run -- example/manage.py migrate
    uv run -- example/manage.py runserver

# Run basic test
test: init
    uv run pytest

# Run all supported test environments via tox
test-all:

    @echo ===========
    @echo Python 3.10
    @echo ===========
    uv run --with "Django~=4.2" --python 3.10 pytest
    uv run --with "Django~=5.2" --python 3.10 pytest

    @echo ===========
    @echo Python 3.11
    @echo ===========
    uv run --with "Django~=4.2" --python 3.11 pytest
    uv run --with "Django~=5.2" --python 3.11 pytest

    @echo ===========
    @echo Python 3.12
    @echo ===========
    uv run --with "Django~=4.2" --python 3.12 pytest
    uv run --with "Django~=5.2" --python 3.12 pytest
    uv run --with "Django~=6.0" --python 3.12 pytest

    @echo ===========
    @echo Python 3.13
    @echo ===========
    uv run --with "Django~=5.2" --python 3.13 pytest
    uv run --with "Django~=6.0" --python 3.13 pytest

    @echo ===========
    @echo Python 3.14
    @echo ===========
    uv run --with "Django~=5.2" --python 3.14 pytest
    uv run --with "Django~=6.0" --python 3.14 pytest


# Remove all dev, build and test artifacts
clean:
    rm -rf .pytest_cache
    rm -rf .ruff_cache
    rm -rf .venv
    rm -rf example/sqlite3.db
    rm -rf src/django_vanilla_extract.egg-info

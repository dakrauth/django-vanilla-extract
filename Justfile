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

# Generate HTML documention
docs *args:
    python scripts/tools.py mkdocs {{args}}


# Run all supported test environments via tox
test-all:
    #!/usr/bin/env bash
    python scripts/tools.py permute '--with "Django~={4.2.0,5.2.0}" --python 3.{10,11}' | while IFS= read -r line
    do
        echo uv run "${line}" pytest
    done
    echo uv run '--with "Django~=4.2.0" --python 3.12' pytest
    python scripts/tools.py permute '--with "Django~={5.2.0,6.0.0}" --python 3.{12,13,14}' | while IFS= read -r line
    do
        echo uv run "${line}" pytest
    done


# Remove all dev, build and test artifacts
clean:
    rm -rf .pytest_cache
    rm -rf .ruff_cache
    rm -rf .venv
    rm -rf example/sqlite3.db
    rm -rf src/django_vanilla_extract.egg-info

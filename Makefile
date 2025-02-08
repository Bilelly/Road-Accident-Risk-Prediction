all: setup-git-hooks install check test 

check: check-format check-lint

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

dataset:
	uv run python src/prediction_profils_accidents_graves/create_dataset.py

install:
	uv lock
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

semantic-release:
	uv run semantic-release version --no-changelog --no-push --no-vcs-release --skip-build --no-commit --no-tag
	uv lock
	git add pyproject.toml uv.lock
	git commit --allow-empty --amend --no-edit 

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	chmod +x hooks/post-commit
	git config core.hooksPath hooks

test:
	uv run pytest -v --cov=src --cov-report=xml

upgrade-dependencies:
	uv lock --upgrade

.PHONY: all check check-format check-lint dataset install lint semantic-release setup-git-hooks test upgrade-dependencies
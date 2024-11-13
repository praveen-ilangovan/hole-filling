##################
###   INSTALL  ###
.PHONY: install
install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using poetry"
	@poetry install

##################
##  PRECOMMIT  ###
.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Linting code: Running ruff"
	@poetry run ruff check hole_filling/
	@echo "🚀 Formatting code: Running ruff"
	@poetry run ruff format hole_filling/
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy hole_filling/

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest

##################
#####  HELP  #####
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

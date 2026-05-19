.PHONY: clean-pyc clean-build help test
.DEFAULT_GOAL := help

help: ## print this help screen
	@perl -nle'print $& if m{^[a-zA-Z0-9_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc
	@echo "all clean now .."

clean-build: ## remove build artifacts
	@rm -fr build/
	@rm -fr dist/
	@rm -fr htmlcov/
	@rm -fr *.egg-info
	@rm -rf .coverage
	@rm -rf my_secrets

clean-pyc: ## remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*.orig' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

init: ## create virtualenv for python3
	uv sync

lint: ## check style with ruff
#	@echo "\nlooking for lints .."
#	@echo "===================="
	@uv run ruff check django_secrets

test: clean lint ## run testsuite
	@printf '\n' | env -u SECRET_KEY SECOND_SECRET=blub uv run python manage.py test

coverage: clean  ## test and generate coverage data
	@printf '\n' | env -u SECRET_KEY SECOND_SECRET=blub uv run coverage run manage.py test
	@uv run coverage report -m
	@make lint

view-coverage: coverage ## open coverage report in the browser
	@uv run coverage html
	@open htmlcov/index.html

release: clean ## package and upload a release (working dir must be clean)
	@while true; do \
		CURRENT=`uv run python -c "import django_secrets; print(django_secrets.__version__)"`; \
		echo ""; \
		echo "=== The current version is $$CURRENT - what's the next one?"; \
		echo "==========================================================="; \
		echo "1 - new major version"; \
		echo "2 - new minor version"; \
		echo "3 - patch"; \
		echo ""; \
		read yn; \
		case $$yn in \
			1 ) uv run bump-my-version bump major || exit $$?; break;; \
			2 ) uv run bump-my-version bump minor || exit $$?; break;; \
			3 ) uv run bump-my-version bump patch || exit $$?; break;; \
			* ) echo "Please answer 1-3.";; \
		esac \
	done
	@uv build
	@uv publish

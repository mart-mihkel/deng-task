.PHONY: help
# show avalable commands
help:
	@printf "\ndevelopment commands:\n\n"
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{printf "  \033[36m%-20s\033[0m %s\n", substr($$1,1,index($$1,":")-1),c}1{c=0}' $(MAKEFILE_LIST)
	@printf "\n"

.PHONY: setup
# setup development environment
setup:
	@uv sync

.PHONY: test
# run tests
test:
	@uv run coverage run -m pytest

.PHONY: format
# run formatter
format:
	@uv run ruff format

.PHONY: lint
# run linter
lint:
	@uv run ruff check

.PHONY: clean
# delete docker containers and temporary files
clean:
	@docker compose down --volumes
	@docker compose -f compose.dev.yml down --volumes
	@rm -rfv .coverage .pytest_cache flaskr/__pycache__

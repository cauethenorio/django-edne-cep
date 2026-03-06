.DEFAULT_GOAL := list
.PHONY: test test-matrix test-cov lint fmt cov-report cov-xml cov list

#: run tests
test:
	uv run pytest tests

#: run tests across Python x Django matrix
test-matrix:
	uv run --python 3.10 --with 'django~=4.2.0' pytest tests
	uv run --python 3.10 --with 'django~=5.2.0' pytest tests
	uv run --python 3.11 --with 'django~=4.2.0' pytest tests
	uv run --python 3.11 --with 'django~=5.2.0' pytest tests
	uv run --python 3.12 --with 'django~=4.2.0' pytest tests
	uv run --python 3.12 --with 'django~=5.2.0' pytest tests
	uv run --python 3.12 --with 'django~=6.0.0' pytest tests
	uv run --python 3.13 --with 'django~=5.2.0' pytest tests
	uv run --python 3.13 --with 'django~=6.0.0' pytest tests
	uv run --python 3.14 --with 'django~=5.2.0' pytest tests
	uv run --python 3.14 --with 'django~=6.0.0' pytest tests

#: run tests with coverage
test-cov:
	uv run coverage run -m pytest tests

#: generate coverage report
cov-report:
	uv run coverage combine
	uv run coverage html

#: generate coverage xml report (for CI)
cov-xml:
	uv run coverage combine
	uv run coverage xml

#: run tests with coverage and generate report
cov: test-cov cov-report

#: run linter checks
lint:
	uv run ruff check .
	uv run ruff format --diff .

#: format code
fmt:
	uv run ruff format .
	uv run ruff check --fix .

#: list all available commands
list:
	@grep -B1 -E "^[a-zA-Z0-9_-]+\:([^\=]|$$)" Makefile \
	 | grep -v -- -- \
	 | sed 'N;s/\n/###/' \
	 | sed -n 's/^#: \(.*\)###\(.*\):.*/make \2###\1/p' \
	 | column -t  -s '###'

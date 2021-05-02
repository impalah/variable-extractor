# Variables definition

## Should be increased on each build
PACKAGE_VERSION := 0.0.1

.PHONY: virtual dev-install update-requirements dev-clean build clean

# Creates an isolated python 3 environment
virtual: .venv/bin/pip

# Creates an isolated python 3 environment
.venv/bin/pip:
	python3 -m venv .venv
	.venv/bin/pip install wheel

# Install the defined requirements
dev-install:
	.venv/bin/pip install -Ur requirements.txt

# Build virtual environment
dev: virtual dev-install

# Updates the requirement file
update-requirements:
	.venv/bin/pip freeze | grep -v "pkg-resources" > requirements.txt

# Clean the virtualenv folder
dev-clean:
	rm -rf .venv

build-converter:
	docker build -t pdf-converter -f DockerfilePdf2txt .

build-analyzer:
	docker build -t text-analyzer -f DockerfileAnalyzer .


# # Execute tests (deactivated, only for pytest)
# test:
# 	pytest tests/

# # Execute test coverage (deactivated, only for pytest)
# coverage:
# 	pytest --cov=. --cov-report term-missing  tests/

# Generates a salt
salt:
	@python -c "import crypt;print(str(crypt.mksalt(method=crypt.METHOD_SHA256)))"

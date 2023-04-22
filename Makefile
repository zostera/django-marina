PROJECT_DIR := src/django_marina
PYTHON_SOURCES := ${PROJECT_DIR} tests *.py

.PHONY: test
test:
	coverage run manage.py test
	coverage report

.PHONY: tox
tox:
	rm -rf .tox
	tox

.PHONY: reformat
reformat:
	autoflake -ir --remove-all-unused-imports ${PYTHON_SOURCES}
	isort ${PYTHON_SOURCES}
	docformatter -ir --pre-summary-newline --wrap-summaries=0 --wrap-descriptions=0 ${PYTHON_SOURCES}
	black .

.PHONY: lint
lint:
	flake8 ${PYTHON_SOURCES}
	pydocstyle ${PYTHON_SOURCES}

.PHONY: docs
docs:
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

.PHONY: porcelain
porcelain:
ifeq ($(shell git status --porcelain),)
	@echo "Working directory is clean."
else
	@echo "Error - working directory is dirty. Commit those changes!";
	@exit 1;
endif

.PHONY: branch
branch:
ifeq ($(shell git rev-parse --abbrev-ref HEAD),main)
	@echo "On branch main."
else
	@echo "Error - Not on branch main!"
	@exit 1;
endif

.PHONY: build
build: docs
	rm -rf build dist *.egg-info
	python -m build .

.PHONY: publish
publish: porcelain branch build
	twine upload dist/*
	rm -rf build dist *.egg-info

.PHONY: check-description
check-description:
	rm -rf build-check-description
	pip wheel -w build-check-description --no-deps .
	twine check build-check-description/*
	rm -rf build-check-description

.PHONY: check-manifest
check-manifest:
	check-manifest --verbose

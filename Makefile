.PHONY: develop test coverage tox reformat lint docs porcelain branch build publish

PROJECT_DIR=src/django_marina
PYTHON_SOURCES=${PROJECT_DIR} tests *.py

develop:
	pip install -U pip -r requirements/dev.txt
	pip install .

test:
	python manage.py test

coverage:
	coverage run --source=${PROJECT_DIR} manage.py test
	coverage report

tox:
	rm -rf .tox
	tox

reformat:
	autoflake -ir --remove-all-unused-imports ${PYTHON_SOURCES}
	isort -rc ${PYTHON_SOURCES}
	docformatter -ir --pre-summary-newline --wrap-summaries=0 --wrap-descriptions=0 ${PYTHON_SOURCES}
	black .

lint:
	flake8 ${PYTHON_SOURCES}
	pydocstyle --add-ignore=D1,D202,D301,D413 ${PYTHON_SOURCES}

docs:
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

porcelain:
ifeq ($(shell git status --porcelain),)
	@echo "Working directory is clean."
else
	@echo "Error - working directory is dirty. Commit those changes!";
	@exit 1;
endif

branch:
ifeq ($(shell git rev-parse --abbrev-ref HEAD),main)
	@echo "On branch main."
else
	@echo "Error - Not on branch main!"
	@exit 1;
endif

build: docs
	pip wheel . -w dist

#publish: porcelain branch build
publish: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

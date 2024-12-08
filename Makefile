VERSION := $(shell sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml)

.PHONY: test
test:
	coverage run manage.py test
	coverage report

.PHONY: tests
tests:
	tox

.PHONY: reformat
reformat:
	ruff format .
	ruff check . --fix

.PHONY: lint
lint:
	ruff check .

.PHONY: docs
docs: clean
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

.PHONY: example
example:
	cd example && python manage.py runserver


.PHONY: publish
publish: porcelain branch docs build
	twine upload dist/*
	git tag -a v${VERSION} -m "Release ${VERSION}"
	git push origin --tags

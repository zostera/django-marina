VERSION := $(shell sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml)

.PHONY: test
test:
	coverage run manage.py test
	coverage report



.PHONY: example
example:
	cd example && python manage.py runserver


.PHONY: publish
publish: porcelain branch docs build
	twine upload dist/*
	git tag -a v${VERSION} -m "Release ${VERSION}"
	git push origin --tags

SOURCES = src tests

.PHONY: all

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean - shortcut to run clean-build and clean-pyc
	@echo "reformat - reformat code"
	@echo "lint - check style"

clean: clean-build clean-pyc clean-tox

clean-build:
	rm -rf build/
	rm -rf _dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-tox:
	rm -rf .tox

black:
	black .

isort:
	for src in $(SOURCES) ; do \
		isort -rc $$src ; \
	done

autoflake:
	autoflake -ir $(SOURCES) --remove-all-unused-imports

lint:
	flake8 $(SOURCES)

reformat: autoflake isort black

test: lint
	python runtests.py

tox: clean-tox
	tox

coverage: lint
	coverage run --source chartit runtests.py demoproject
	coverage report -m

coverage-html: coverage
	coverage html
	open htmlcov/index.html

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean
	python setup.py sdist
	ls -l _dist/

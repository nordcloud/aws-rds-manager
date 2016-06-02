install: clean
	pip install -e .

build:
	python setup.py sdist bdist_wheel

release-test: clean build
	twine upload -r pypitest dist/aws*

release: clean build
	twine upload -r pypi dist/aws*

test: clean
	tox

clean:
	rm -rf dist build *.egg-info MANIFEST .tox .eggs .tox .coverage

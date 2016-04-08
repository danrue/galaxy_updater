# This just tests with one version of python
test:
	py.test
	# py.test -s # full output

release_patch:
	bumpversion patch
	git push --tags

lint:
	env MYPYPATH=stubs mypy pygammon --strict-optional

test:
	python -m unittest discover -s tests

tags:
	ctags -R pygammon

.PHONY: activate lint test tags

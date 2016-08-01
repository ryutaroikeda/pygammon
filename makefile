analyze: type lint test

type:
	env MYPYPATH=stubs mypy pygammon --strict-optional

lint:
	pylint pygammon

test:
	python -m unittest discover -s tests

tags:
	ctags -R pygammon

install:
	pip install -r requirements.txt

.PHONY: type lint test tags install

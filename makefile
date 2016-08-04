analyze: type lint test

type:
	env MYPYPATH=stubs mypy pygammon --strict-optional --disallow-untyped-calls \
		--disallow-untyped-defs --check-untyped-defs --warn-redundant-casts
	env MYPYPATH=stubs mypy tests --strict-optional --disallow-untyped-calls \
		--check-untyped-defs --warn-redundant-casts

lint:
	pylint pygammon
	pylint tests

test:
	python -m unittest discover -s tests

tags:
	ctags -R pygammon

install:
	pip install -r requirements.txt

.PHONY: type lint test tags install

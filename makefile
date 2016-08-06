PYGAMMON_SRC := $(wildcard pygammon/*.py)
TESTS_SRC := $(wildcard tests/*.py)

all: .analyze_pygammon .analyze_tests test

.analyze_pygammon: $(PYGAMMON_SRC)
	env MYPYPATH=stubs mypy pygammon --strict-optional \
		--disallow-untyped-calls --disallow-untyped-defs \
		--check-untyped-defs --warn-redundant-casts
	pylint pygammon
	touch "$@"

.analyze_tests: $(TESTS_SRC)
	env MYPYPATH=stubs mypy tests --strict-optional \
		--disallow-untyped-calls --check-untyped-defs \
		--warn-redundant-casts
	pylint tests
	touch "$@"

test:
	python -m unittest discover -s tests

tags: $(PYGAMMON_SRC)
	ctags -R pygammon

install:
	pip install -r requirements.txt

.PHONY: test install

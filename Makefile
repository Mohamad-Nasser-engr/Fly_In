PY = python3
MAIN = main
FILE_PATH = maps/challenger/01_the_impossible_dream.txt

install:
	pip install -r requirements.txt

run:
	$(PY) -m $(MAIN) $(FILE_PATH)

debug:
	$(PY) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	$(PY) -m flake8 .
	$(PY) -m mypy . --warn-return-any \
	        --warn-unused-ignores \
	        --ignore-missing-imports \
	        --disallow-untyped-defs \
	        --check-untyped-defs

lint-strict:
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict
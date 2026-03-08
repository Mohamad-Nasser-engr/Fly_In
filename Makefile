PY = python3
MAIN = main

# install:
# 	pip install -r requirements.txt

run:
	$(PY) -m $(MAIN)

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
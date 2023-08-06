HERE = $(shell pwd)
BIN = $(HERE)/bin
PYTHON = $(BIN)/python
BUILD_DIRS = bin build include lib lib64 man share
VIRTUALENV = virtualenv
SYSTEM_PYTHON = python3.10

.PHONY: all test build clean docs

all: build

$(PYTHON):
	$(SYSTEM_PYTHON) -m venv .
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) setup.py develop
	$(BIN)/pip install tox
	$(BIN)/pip install twine

clean:
	rm -rf $(BUILD_DIRS)

test: $(PYTHON)
	$(BIN)/tox

docs:  $(PYTHON)
	$(BIN)/tox -e docs

lint: $(PYTHON)
	$(BIN)/tox -e flake8




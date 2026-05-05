# Testing Guide

This project uses `pytest` for test execution, `coverage` for coverage report and `uv` for environment management.

## Prerequisites

Install project dependencies first:

```bash
uv sync
```

## Run All Tests

Run the full test suite with:

```bash
uv run pytest
```

## Run a Specific Test File

To run one test file only:

```bash
uv run pytest tests/test_example.py
```

## Useful Options

- Show extra output:

```bash
uv run pytest -v
```

- Run tests with coverage:

```bash
uv run coverage run -m pytest
uv run coverage report -m
```

## Notes

- Place test files inside the `tests/` directory.
- Use filenames prefixed with test_ such as `test_example.py` so `pytest` can discover them automatically.

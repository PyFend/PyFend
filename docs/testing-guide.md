# Testing Guide

This project uses `pytest` for test execution, `coverage` for coverage
reports, and `uv` for workspace and environment management.

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
uv run pytest tests/core/hash_probe/test_hash_probe.py
```

Tests mirror the package boundary:

```text
tests/
├── core/
│   └── hash_probe/
└── cli/
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
- Put core-library tests under `tests/core/`.
- Put command-line tests under `tests/cli/`.
- Prefix test filenames with `test_` so `pytest` can discover them.

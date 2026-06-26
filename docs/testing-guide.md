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
uv run pytest packages/core/tests/hash_probe/test_hash_probe.py
```

Tests mirror the package boundary:

```text
packages/
├── core/
│   └── tests/
│       └── hash_probe/
└── cli/
    └── tests/
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

- Place test files inside the package that owns the tested code.
- Put core-library tests under `packages/core/tests/`.
- Put command-line tests under `packages/cli/tests/`.
- Prefix test filenames with `test_` so `pytest` can discover them.

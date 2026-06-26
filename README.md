# PyFend

PyFend is a Python 3.12 cybersecurity toolkit for command-line workflows
and library use.

## Requirements

- Python 3.12 or newer
- `uv`
- Rust and Cargo for core package builds
- Git

Install Rust and Cargo from the official Rustup docs:
[rustup.rs](https://rustup.rs/).

## Packages

- `packages/core`: `pyfend`, the core library package. It includes hash
  utilities, port scanner code, and a small Rust extension built with maturin.
- `packages/cli`: `pyfend-cli`, the command-line package that depends on
  `pyfend`.

## Development setup

Install `uv` from the
[official uv docs](https://docs.astral.sh/uv/getting-started/installation/),
then run:

```bash
uv sync
uv run pre-commit install
```

Use the locked CI dependency set when needed:

```bash
uv sync --locked --group dev
```

## Checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv build --all-packages
uv run mkdocs build
```

Run one test file:

```bash
uv run pytest packages/core/tests/hash_probe/test_hash_probe.py
```

Run coverage:

```bash
uv run coverage run -m pytest
uv run coverage report -m
```

Tests live beside their package:

- `packages/core/tests`
- `packages/cli/tests`

## Git workflow

1. Branch from `dev`.
2. Open feature pull requests into `dev`.
3. Run checks and review on `dev`.
4. Merge `dev` into `main` only for release-ready changes.

Do not merge feature branches directly into `main`.

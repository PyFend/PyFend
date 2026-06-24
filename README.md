# PyFend

PyFend is a collection of cybersecurity tools for command-line workflows
and Python library integration.

## Workspace layout

The repository is a `uv` workspace with two independently buildable
packages:

```text
pyfend/
├── core/
│   ├── hash_probe/
│   ├── port_scanner/
│   └── pyproject.toml
└── cli/
    ├── __main__.py
    ├── hash_probe.py
    └── pyproject.toml
```

The `pyfend` distribution is built from `pyfend/core`. The CLI package
depends on that primary package. Development dependencies,
workspace membership, lint configuration, and test configuration live in
the root `pyproject.toml`.

## Development setup

If you do not have `uv` installed, follow the
[official installation guide](https://docs.astral.sh/uv/getting-started/installation/).
Then run:

```bash
uv sync
uv run pre-commit install
```

## Usage

Run the CLI:

```bash
uv run pyfend --help
```

Import the core library:

```python
from pyfend.core.hash_probe import crack
```

Build both distributions:

```bash
uv build --all-packages
```

## Documentation

- [Git Flow](docs/gitflow.md)
- [Testing Guide](docs/testing-guide.md)

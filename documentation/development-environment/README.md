# Development environment

## Requirements

- Python 3.12 (see `.python-version`)
- [uv](https://github.com/astral-sh/uv) for dependency management
- Docker Desktop (or Docker Engine with Compose)

Verify the installation:

```bash
python --version
uv --version
docker --version
```

## Install uv

```bash
pip install uv
```

## Set up the project

```bash
uv sync
source .venv/bin/activate
cp env.example .env
```

`uv sync` installs all workspace members (`apps/*`) and the development dependency group used by the notebooks.

## Notebooks

Notebooks run in VS Code, Cursor, PyCharm or JupyterLab. To start JupyterLab:

```bash
uv run --with jupyter jupyter lab
```

Select the `.venv` interpreter as the notebook kernel. To strip outputs before committing:

```bash
make clean-notebook-outputs
```

## Local stack

```bash
make run-docker-compose
```

This starts the Streamlit UI, the FastAPI service, Qdrant and Postgres. Local data is stored in `qdrant_data/` and `postgres_data/`, both git-ignored.

# Development Guide

## Installation

### Using uv (recommended)

```bash
uv add langgraph-a2a-client
```

### Using pip

```bash
pip install langgraph-a2a-client
```

### From source

```bash
git clone https://github.com/5enxia/langgraph-a2a-client.git
cd langgraph-a2a-client
uv sync
```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup development environment

1. Clone the repository:
```bash
git clone https://github.com/5enxia/langgraph-a2a-client.git
cd langgraph-a2a-client
```

2. Install dependencies with uv:
```bash
uv sync --all-extras
```

### Running tests

```bash
uv run pytest
```

With coverage:
```bash
uv run pytest --cov=langgraph_a2a_client --cov-report=html
```

### Code formatting and linting

Format code:
```bash
uv run ruff format .
```

Lint code:
```bash
uv run ruff check .
```

Fix linting issues automatically:
```bash
uv run ruff check --fix .
```

## Building the package

```bash
uv build
```

This will create distribution files in the `dist/` directory.

## Publishing to PyPI

```bash
uv publish
```

Make sure you have configured your PyPI credentials before publishing.

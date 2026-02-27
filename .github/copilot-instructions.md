# Copilot Instructions

## Repository Overview

`aepp` (Adobe Experience Platform Python) is a Python wrapper for the Adobe Experience Platform (AEP) REST APIs. It simplifies authentication and interaction with AEP services such as Schema Registry, Query Service, Catalog, Segmentation, Identity, Data Access, and many more.

## Project Structure

- `aepp/` — Main package source code. Each AEP service has its own module (e.g., `schema.py`, `catalog.py`, `queryservice.py`).
  - `connector.py` — Handles HTTP requests, token management, and retry logic via `AdobeRequest`.
  - `configs.py` / `config.py` — Configuration and connection object handling.
  - `cli/` — Command-line interface entry point.
  - `*manager.py` — Higher-level manager classes (e.g., `SchemaManager`, `FieldGroupManager`) that wrap lower-level API classes.
- `tests/` — Unit tests using `unittest` and `unittest.mock`.
- `docs/` — Markdown documentation per module.
- `notebooks/` — Jupyter notebooks demonstrating usage.

## Key Conventions

- **Python 3.10+** is required.
- **Type hints** should be used for all function parameters and return values. Use `typing` imports (`Union`, `Optional`, `Dict`, etc.).
- **Docstrings** follow a custom format with `Arguments:` and `Returns:` sections listing each parameter name, `OPTIONAL`/`REQUIRED`, and a short description.
- All source files begin with the **Adobe copyright header**:
  ```python
  #  Copyright 2023 Adobe. All rights reserved.
  #  This file is licensed to you under the Apache License, Version 2.0 (the "License");
  #  ...
  ```
- **Imports** are grouped as: internal modules, then external modules.
- Each top-level API class stores a `connector` (instance of `AdobeRequest`) and `header` for making authenticated requests.
- Methods that make HTTP requests delegate to `self.connector.getData(...)`, `self.connector.postData(...)`, `self.connector.patchData(...)`, `self.connector.putData(...)`, or `self.connector.deleteData(...)`.
- Pagination is typically handled with `limit` and `start` (or `continuation`) parameters.
- Use `deepcopy` when returning or modifying mutable defaults (e.g., headers, dicts).
- Logging uses the standard `logging` module; classes expose a `loggingEnabled` flag.

## Build and Test

Install dependencies:
```shell
pip install -r requirements.txt
pip install -e .
```

Run the tests:
```shell
pytest tests/
```

## Adding a New API Module

1. Create `aepp/<service>.py` with the Adobe copyright header.
2. Import `aepp`, `connector`, and relevant `configs` items.
3. Define a class that accepts a `config` / `ConnectObject` and initializes `self.connector = connector.AdobeRequest(...)`.
4. Add corresponding tests in `tests/<service>_test.py` using `unittest.TestCase` and `unittest.mock`.
5. Add documentation in `docs/<service>.md`.
6. Export the class from `aepp/__init__.py` if applicable.

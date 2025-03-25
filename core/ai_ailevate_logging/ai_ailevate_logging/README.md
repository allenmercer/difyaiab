This Library allows for a centralized logging service for all services in the monorepo

---

## Installation
install it as an **editable dependency**:

manually add it to your `pyproject.toml`:
```toml
[tool.poetry.dependencies]
core-library-ai-logging = { path = "../core/library_ai_logging", develop = true }
```
Run:
```sh
poetry install
```
---

## Import and Using the Library ##

```python
from ai_ailevate_logging.logger import Logger

logger = Logger("Dify-POC-Agent")

log.info("Hello")
```


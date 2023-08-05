### meh-logging-python

#### Creating a build

Install the prerequisite packages.

```sh
python -m pip install build twine
```

Run the build command

```sh
python -m build
```

Run a test deployment to TestPyPi

```sh
python -m twine upload --repository testpypi dist/*
```

Run a final deployment to PyPi

```sh
python -m twine upload --repository pypi dist/*
```

#### Usage

```python
from meh_logging import logger

# Log some info
logger.info("hello world")
logger.debug("hello world")
logger.error("hello world")

try:
    1 / 0
except Exception as e:
    logger.exception(e)
```

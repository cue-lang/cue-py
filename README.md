# cue-py use CUE from Python

This is a work in progress, expect constant churn and breakage.

## Installation

Install a platform wheel. Wheels bundle the `libcue` shared library, so users
do not need Go, the CUE CLI, or a dynamic-library search-path setting. Source
installs remain supported when `libcue` is already installed in the system
library search path.

Source distributions intentionally do not download build tools or source code.
To build a wheel locally, first obtain a compatible checkout of
[`cue-lang/libcue`](https://github.com/cue-lang/libcue) and install Go, then run:

```
python scripts/build_libcue.py /path/to/libcue
python -m build --wheel
```

## Development setup

```
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Test

```
pytest --mypy
```

## Using

TODO.

## Issue tracking

Please raise all issues in
[the main CUE repository](https://github.com/cue-lang/cue/issues),
giving the title of the issue a `cue-py: ` prefix.

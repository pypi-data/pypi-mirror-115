# Notes for Developers

or myself in the future.

This document describes how to maintain the Python package code. (2021-07-06)


## Set up venv

    % git clone https://example.com/PROJECT.git
    % cd PROJECT
    PROJECT % python3 -m venv .venv
    PROJECT % source .venv/bin/activate
    (.venv) PROJECT % pip install -e .


## Build


### Install build tools

    (.venv) PROJECT % pip install build

The [`build`](https://pypi.org/project/build/) package reads
`pyproject.toml` and build the package with specified build tools
in the file.

FYI: `pyproject.toml` is for `build` and `setup.cfg` is for `setuptools`.

### Build dist archives

    (.venv) PROJECT % python -m build

This creates a sdist tarball and a wheel archive under the `build`
directory.


## Release

### Install release tools

    (.venv) PROJECT % pip install twine


### Release to PyPI

    (.venv) PROJECT % twine upload dist/*


## Versioning

The version numbers for the package is automatically decided with git
tags (e.g. `rel-1.0`) and [`setuptools-scm`](https://pypi.org/project/setuptools-scm/)
package. You shouldn't write it manually into the code.

# Overview
This small CLI tool, written in Python, is designed to convert Databricks notebooks to regular Python modules. The need for it arose when we started moving a large legacy codebase consisting of Databricks notebooks, which relied on manual deployment, into a new Python package, which was easier to assemble, version and deploy. At the time, there were few tools for the job, but [convert-py-2-databricks](https://github.com/aless10/convert-py-2-databricks) served as the foundation.

This tool can perform some simple tasks to alleviate much of the straightforward manual conversion labor, and should be followed by human review. It takes a path to either a directory containing Databricks notebooks, or a single Databricks notebook, and produces Python modules. All notebooks must be in the `source` format (not IPython).

Features include:
* Convert Python Databricks notebooks into regular Python files, ignoring any other files
* Process any arbitrarily nested directory structure, creating output directories only when not empty
* Convert file names to snake case, aborting in case of file name collisions
* Convert magic `run` commands into imports, with support for user-specified path mapping
* Generate a `requirements.txt` file from `pip install` commands and from any existing `requirements.txt` files
* If a notebook contains widgets, wrap contents of the notebook in a class and convert widgets to `__init__()` params, preserving docstrings and any default values
* Convert cell titles and markdown cells into comments
* Strip Databricks notebook directive formatting (like command cell separators)
* Comment out unsupported magic or unexpected lines

Support for conversion of Python files to Databricks notebooks has been carried over from the foundational project, but was never updated with additional features, so may not work as expected.

# Usage
To view usage information, run:
* `python -m databricks_converter [--help]`
* `python -m databricks_converter <command> --help`

Commands:
* `to-db` - convert Python modules to Databricks notebooks.
* `to-py` - convert Databricks notebooks to Python modules.

Common options:
* `--help` - show the help message and exit.
* `-d` - destination dir, absolute or relative to the current dir (default: `out`, relative to the current dir). The last dir in this path will be used as the root package name in absolute imports.
* `-o` - overwrite the existing destination dir (default: abort if destination dir exists). With this option, the destination dir is not deleted, so if the source changed, only conflicting paths will be overwritten, leaving the rest as is.

## Databricks to Python
To convert Databricks notebooks to Python modules, run:
```
python -m databricks_converter to-py <source/dir/or/file> [-d <destination/dir>] [-o] [-i "</notebook/path=package.module [, ...]>"]
```

Options:
* `-i` - mapping of notebook `%run` paths to package imports. This is necessary for absolute paths (imports outside the converted package), and also works for relative paths (which would normally become local imports) in case they must be overridden.

### Example
```
python -m databricks_converter to-py example/src -d example/out -o -i "/Workspace/External/Notebook=external.package"
```

## Python to Databricks
To convert Python modules to Databricks notebooks, run:
```
python -m databricks_converter to-db <source/dir/or/file> [-d <destination/dir>] [-o]
```

### Example
First, run the example above to create some Python modules, then run:
```
python -m databricks_converter to-db example/out -d example/out2 -o
```

# Future ideas
* Add tests
* Publish to PyPi
* Databricks to Python
    * Add imports for stock Databricks packages (`pyspark`, `databricks-sdk`, etc.)
    * Implement handling of functionality from the `dbutils` package, especially
        * `dbutils.widgets.getArgument`
        * `dbutils.notebook.run`
        * Possibly handle `dbutils.widgets.remove` and `dbutils.widgets.removeAll` using built-in `del`
    * Implement support for [widget values in %run cells](https://docs.databricks.com/aws/en/notebooks/widgets#use-databricks-widgets-with-run)
    * Implement handling of `%sql` cells by wrapping their contents in `_sqldf = spark.sql("""`...`""")`
    * Possibly implement support for other `MAGIC`s
    * Add an option for tailoring the converted modules to run in a Databricks environment (e.g., import `dbutils` instead of converting its functionality)
    * Add an option for copying non-Python files to the output dir instead of ignoring them
    * Add an option for creating empty dirs
* Python to Databricks
    * Bring up to feature parity

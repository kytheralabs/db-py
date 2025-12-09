import os.path

import click

from databricks_converter.constants import TO_DATABRICKS, TO_PY
from databricks_converter.converter.converter import Converter


@click.group()
def cli1():
    pass


@cli1.command()
@click.argument('filename')
@click.option('--destination', default=os.path.dirname(__file__), help='Path to save the output file')
def to_databricks(filename, destination):
    databricks_converter = Converter(TO_DATABRICKS, destination)
    databricks_converter.convert(filename)


@click.group()
def cli2():
    pass


@cli2.command()
@click.argument('filename')
@click.option('--destination', default=os.path.dirname(__file__), help='Path to save the output file')
def to_py(filename, destination):
    print(f"Convert from databricks to python {filename} - {destination}")
    python_converter = Converter(TO_PY, destination)
    python_converter.convert(filename)


main = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    main()

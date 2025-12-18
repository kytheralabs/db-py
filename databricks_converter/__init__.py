import click

from databricks_converter.db_to_py_converter import DbToPyConverter
from databricks_converter.py_to_db_converter import PyToDbConverter


@click.group()
def db_to_py():
    pass


@db_to_py.command()
@click.argument("source", type=click.Path())
@click.option(
    "-d",
    "--destination",
    type=click.Path(file_okay=False),
    default="out",
    show_default=True,
    help="Output destination dir.",
)
@click.option(
    "-o",
    "--overwrite",
    type=bool,
    is_flag=True,
    flag_value=True,
    help="Overwrite the destination dir.",
)
@click.option(
    "-i",
    "--import-mapping",
    type=str,
    help='Mappings of %run paths to import packages, delimited with "=" and separated with ",". Ex.: "/Notebook_1=utils.module1,/Core/Notebook 2=utils.core.module2".',
)
def to_py(source, destination, overwrite, import_mapping):
    DbToPyConverter(source, destination, overwrite, import_mapping).convert()


@click.group()
def py_to_db():
    pass


@py_to_db.command()
@click.argument("source", type=click.Path())
@click.option(
    "-d",
    "--destination",
    type=click.Path(file_okay=False),
    default="out",
    show_default=True,
    help="Output destination dir.",
)
@click.option(
    "-o",
    "--overwrite",
    type=bool,
    is_flag=True,
    flag_value=True,
    help="Overwrite the destination dir.",
)
def to_db(source, destination, overwrite):
    PyToDbConverter(source, destination, overwrite).convert()


main = click.CommandCollection(sources=[db_to_py, py_to_db])

if __name__ == "__main__":
    main()

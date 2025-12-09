import filecmp
import os
import tempfile

from databricks_converter.databricks2py.converter import convert as databricks_convert
from databricks_converter.py2Databricks.converter import convert as python_convert


def test_from_databricks_to_databricks():
    origin = os.path.join(os.path.dirname(__file__), "test_files/databricks.py")
    with open(origin) as file_origin:
        data = file_origin.readlines()
    python_data = databricks_convert(data)
    databricks_data = python_convert(python_data)
    test_converted_file = tempfile.NamedTemporaryFile("w")
    with open(test_converted_file.name, "w") as converted_file:
        converted_file.writelines(databricks_data)
        converted_file.seek(0)
        assert filecmp.cmp(test_converted_file.name, origin)


def test_from_python_to_python():
    origin = os.path.join(os.path.dirname(__file__), "test_files/python.py")
    with open(origin) as file_origin:
        data = file_origin.readlines()
    databricks_data = python_convert(data)
    python_data = databricks_convert(databricks_data)
    test_converted_file = tempfile.NamedTemporaryFile("w")
    with open(test_converted_file.name, "w") as converted_file:
        converted_file.writelines(python_data)
        converted_file.seek(0)
        assert filecmp.cmp(test_converted_file.name, origin)

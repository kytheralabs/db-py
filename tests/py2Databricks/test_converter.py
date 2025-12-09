import filecmp
import os
import tempfile

from databricks_converter.py2Databricks.converter import convert


def test_convert():
    origin = os.path.join(os.path.dirname(__file__), "test_files/python.py")
    destination = os.path.join(os.path.dirname(__file__), "test_files/databricks.py")
    with open(origin) as file_origin:
        data = file_origin.readlines()
    new_data = convert(data)
    test_converted_file = tempfile.NamedTemporaryFile("w")
    with open(test_converted_file.name, "w") as converted_file:
        converted_file.writelines(new_data)
        converted_file.seek(0)
        assert filecmp.cmp(test_converted_file.name, destination)

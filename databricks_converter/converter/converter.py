import enum
import os

from databricks_converter.constants import TO_PY, TO_DATABRICKS
from databricks_converter.py2Databricks.converter import convert as convert_to_databricks
from databricks_converter.databricks2py.converter import convert as convert_to_python


class ConvertStrategy(str, enum.Enum):
    TO_PYTHON = TO_PY, convert_to_python
    TO_DATABRICKS = TO_DATABRICKS, convert_to_databricks

    def __new__(cls, value, fn):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.fn = fn
        return obj


class Converter:

    def __init__(self, strategy, destination):
        self.strategy = ConvertStrategy(strategy)
        self.destination = destination

    @staticmethod
    def read_file(filename):
        with open(filename) as file_origin:
            return file_origin.readlines()

    @staticmethod
    def get_file_name_without_extension(filename):
        return os.path.splitext(filename)[0]

    def write_file(self, lines, filename):
        with open(os.path.join(self.destination,
                               f"{self.get_file_name_without_extension(filename)}_{self.strategy.value}.py"),
                  "w") as converted_file:
            converted_file.writelines(lines)

    def convert_file(self, filename):
        print(filename)
        lines = self.read_file(filename)
        converted_lines = self.strategy.fn(lines)
        self.write_file(converted_lines, filename)

    def convert(self, source):
        abs_source = os.path.abspath(source)
        print(abs_source)
        if os.path.isfile(abs_source):
            self.convert_file(abs_source)
        else:
            for f in os.listdir(abs_source):
                print(f)
                self.convert(os.path.join(abs_source, f))

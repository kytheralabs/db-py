import os
from abc import abstractmethod, ABC

from databricks_converter import constants as const, utils


def read_file(filepath):
    with open(filepath) as f:
        return f.readlines()


def write_file(filepath, lines):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.writelines(lines)


def pythonize_path(filepath):
    filepath_parts = os.path.splitext(filepath)
    return os.sep.join(utils.to_snake_case(part) for part in filepath_parts[0].split(os.sep)) + filepath_parts[1]


class BaseConverter(ABC):
    def __init__(self, source, destination, overwrite):
        self.strategy = None
        # Absolute path of the source
        self.source = os.path.abspath(os.path.expanduser(source))
        # Absolute path of the source dir (used for keeping track of nested dirs)
        self.source_base_dir = self.source if os.path.isdir(self.source) else os.path.dirname(self.source)
        # Absolute path of the destination dir (what was passed on command line)
        self.destination_base_dir = os.path.abspath(os.path.expanduser(destination))
        self.overwrite = overwrite
        self.root_package = os.path.basename(self.destination_base_dir)
        if not self.root_package:
            # May happen if destination is e.g. "/"
            print(
                "ERROR: destination path does not end in a dir which can be used as the root package name - specify a different destination dir."
            )
            exit(1)
        self.requirements = set()
        self.converted_filepaths = set()
        try:
            # Create destination dir; will fail if it already exists and overwrite is False, safeguarding against
            # accidental overwriting
            os.makedirs(self.destination_base_dir, exist_ok=self.overwrite)
        except FileExistsError:
            print(
                "ERROR: destination path already exists - add the '--overwrite' option or specify a different destination dir."
            )
            exit(1)

    def get_destination_filepath(self, source_filepath):
        return str(
            os.path.join(
                self.destination_base_dir,
                pythonize_path(source_filepath.removeprefix(self.source_base_dir).removeprefix(os.sep)),
            )
        )

    @abstractmethod
    def convert_lines(self, lines, source_filepath) -> tuple[list[str], set[str]]:
        pass

    def convert_file(self, source_filepath, destination_filepath):
        if destination_filepath in self.converted_filepaths:
            print("ERROR: destination path already exists - change the source paths to avoid snake-cased collisions.")
            exit(1)
        lines = read_file(source_filepath)
        converted_lines, requirements = self.convert_lines(lines, source_filepath)
        self.requirements = self.requirements.union(requirements)
        write_file(destination_filepath, converted_lines)
        self.converted_filepaths.add(destination_filepath)

    def convert_source(self, source):
        if os.path.isfile(source):
            destination_filepath = self.get_destination_filepath(source)
            # Convert only Python files
            if os.path.splitext(source)[1].lower() == ".py":
                print(f"[CONVERT] {source} -> {destination_filepath}")
                self.convert_file(source, destination_filepath)
            # Add dependencies from the requirements file
            elif os.path.basename(source).lower() == const.REQUIREMENTS_FILENAME:
                print(f"[ADD REQS] {source}")
                self.requirements = self.requirements.union(read_file(source))
            # Ignore all other files
            else:
                print(f"[IGNORE] {source}")
        elif os.path.isdir(source):
            # Process each dir recursively
            for f in os.listdir(source):
                self.convert_source(os.path.join(source, f))
        else:
            print(f"ERROR: bad path: {source}")

    def convert(self):
        self.convert_source(self.source)
        # Write all the dependencies to the requirements file
        if self.requirements:
            write_file(self.get_destination_filepath(const.REQUIREMENTS_FILENAME), sorted(self.requirements))

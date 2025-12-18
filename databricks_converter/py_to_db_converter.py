from databricks_converter import constants as const
from databricks_converter.base_converter import BaseConverter


def add_prefix(line, prefix):
    return f"{prefix}{line}"


def convert_to_md(line):
    if line.startswith(const.MAGIC_TEXT_PLACEHOLDER):
        line = line.replace(const.MAGIC_TEXT_PLACEHOLDER, "")
    return add_prefix(line, const.MAGIC_MD_PREFIX)


def convert_to_run(line):
    import_prefix = const.DATABRICKS_RELATIVE_IMPORT
    if "." in line:
        import_prefix = "/"
        line = line.replace(".", "/")
    line = f"{import_prefix}{line.replace(const.PYTHON_IMPORT, '')}"
    return add_prefix(line, const.MAGIC_RUN_PREFIX)


class PyToDbConverter(BaseConverter):
    def __init__(self, source, destination, overwrite):
        super().__init__(source, destination, overwrite)
        self.strategy = const.TO_DB
        print(f"[{self.strategy}]: {self.source} -> {self.destination_base_dir}")

    def convert_lines(self, lines, source_filepath):
        newline_counter = 0
        converted_lines = [const.FIRST_LINE]
        for line in lines:
            if line.startswith("#"):
                converted_lines.append(convert_to_md(line))
                newline_counter = 0
            elif line.startswith(const.PYTHON_IMPORT):
                converted_lines.append(const.CELL_SEPARATOR)
                converted_lines.append("\n")
                converted_lines.append(convert_to_run(line))
                newline_counter = 0
            elif line.startswith("\n"):
                if newline_counter == 2:
                    pass
                else:
                    newline_counter += 1
                    converted_lines.append(line)
            elif line.startswith("def") or line.startswith("class"):
                converted_lines.append(const.CELL_SEPARATOR)
                converted_lines.append("\n")
                converted_lines.append(line)
                newline_counter = 0
            else:
                if newline_counter > 1:
                    converted_lines.append(const.CELL_SEPARATOR)
                    converted_lines.append("\n")
                converted_lines.append(line)
                newline_counter = 0
        return converted_lines, set()

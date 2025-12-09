from databricks_converter.constants import COMMAND
from databricks_converter.databricks2py.utils import MAGIC_MD_PREFIX, convert_md, MAGIC_IMPORT_PREFIX, convert_imports


def convert(lines):
    newline_counter = 0
    new_lines = []
    for row in lines[1:]:
        if row.startswith(MAGIC_MD_PREFIX):
            new_lines.append(convert_md(row))
            newline_counter = 0
        elif row.startswith(MAGIC_IMPORT_PREFIX):
            new_lines.append(convert_imports(row))
            newline_counter = 0
        elif row.startswith(COMMAND):
            pass
        elif row.startswith("\n"):
            if newline_counter == 2:
                pass
            else:
                newline_counter += 1
                new_lines.append(row)
        elif row.startswith("def") or row.startswith("class"):
            new_lines.append(row)
            newline_counter = 0
        else:
            new_lines.append(row)
            newline_counter = 0
    return new_lines

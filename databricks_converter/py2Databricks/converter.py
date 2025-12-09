from databricks_converter.constants import PYTHON_IMPORT, FIRST_ROW, COMMAND
from databricks_converter.py2Databricks.utils import convert_to_md, convert_to_run


def convert(lines):
    newline_counter = 0
    new_lines = [FIRST_ROW]
    for row in lines:
        if row.startswith("#"):
            new_lines.append(convert_to_md(row))
            newline_counter = 0
        elif row.startswith(PYTHON_IMPORT):
            new_lines.append(COMMAND)
            new_lines.append("\n")
            new_lines.append(convert_to_run(row))
            newline_counter = 0
        elif row.startswith("\n"):
            if newline_counter == 2:
                pass
            else:
                newline_counter += 1
                new_lines.append(row)
        elif row.startswith("def") or row.startswith("class"):
            new_lines.append(COMMAND)
            new_lines.append("\n")
            new_lines.append(row)
            newline_counter = 0
        else:
            if newline_counter > 1:
                new_lines.append(COMMAND)
                new_lines.append("\n")
            new_lines.append(row)
            newline_counter = 0
    return new_lines

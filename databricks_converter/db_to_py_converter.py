import os
import re

from databricks_converter import constants as const, utils
from databricks_converter.base_converter import BaseConverter
from databricks_converter.widget import Widget, get_widget_name_from_getter


def convert_title(line):
    return "# " + line.removeprefix(const.CELL_TITLE_PREFIX)


def remove_magic(line):
    return line.removeprefix(const.MAGIC_PREFIX + " ")


def remove_re_prefix(line, re_prefix):
    return re.sub(re_prefix, "", line)


def convert_magic_to_comment(line):
    return "# " + remove_magic(line)


def convert_md(line):
    return "#" + remove_re_prefix(line, const.MAGIC_MD_PREFIX_RE)


def convert_pip_install(line):
    return {el + "\n" for el in remove_re_prefix(line, const.PIP_INSTALL_PREFIX_RE).strip().split(" ") if el}


def pythonize_import(notebook_path):
    return ".".join(utils.to_snake_case(part) for part in notebook_path.split(os.sep))


def get_class_declaration(source_filepath):
    class_name = utils.to_snake_case(os.path.splitext(os.path.basename(source_filepath))[0]).title().replace("_", "")
    return f"class {class_name}:\n"


def convert_widgets(lines):
    return [
        Widget(widget_definition.strip())
        for widget_definition in " ".join(lines).split(const.WIDGET_PREFIX)
        if widget_definition.strip()
    ]


def convert_code(line):
    # May have magic prefix if in a cell beginning with e.g. "%pip"
    converted_line = remove_magic(line)
    # If non-comment, convert widget getter calls (if any)
    if not line.strip().startswith("#"):
        converted_line = converted_line.replace(const.WIDGET_GET_ALL_CALL, "self.__dict__")
        match = re.search(const.WIDGET_GET_CALL_RE, line)
        if match:
            converted_line = line.replace(match.group(0), get_widget_name_from_getter(match.group(0)))
    return converted_line


class DbToPyConverter(BaseConverter):
    def __init__(self, source, destination, overwrite, import_mapping):
        super().__init__(source, destination, overwrite)
        self.strategy = const.TO_PY

        # Initialize import mappings
        self.import_dict = {}
        if import_mapping:
            for mapping in import_mapping.split(","):
                k, v = mapping.strip().split("=")
                self.import_dict[k.strip()] = v.strip()

        print(f"[{self.strategy}]: {self.source} -> {self.destination_base_dir}")

    def convert_run(self, line, source_filepath):
        notebook_path = remove_magic(remove_re_prefix(line, const.MAGIC_RUN_PREFIX_RE)).strip('\r\n\t\f\v "')

        # First check the import mapping
        import_package = self.import_dict.get(notebook_path)
        if import_package:
            return "from " + import_package + " import *\n"

        # Absolute path, and the mapping was not found above
        elif os.path.isabs(notebook_path):
            print("WARNING: unmapped import:", notebook_path)
            return "# [UNMAPPED IMPORT] from '" + notebook_path + "' import *\n"

        # Relative path - figure out the local import path
        else:
            source_filepath_dir = os.path.dirname(source_filepath)
            abs_source_filepath = os.path.normpath(os.path.join(source_filepath_dir, notebook_path))
            rel_source_filepath = abs_source_filepath.removeprefix(self.source_base_dir).removeprefix(os.sep)
            return "from " + self.root_package + "." + pythonize_import(rel_source_filepath) + " import *\n"

    def convert_lines(self, lines, source_filepath):
        is_new_cell = False
        converted_lines = []
        current_cell_type = const.CellType.NONE
        is_widget_definition_in_progress = False
        widget_definition_lines = []
        widget_definition_position = None
        indent_level = 0
        requirements = set()

        # Discard the first line, which is a static comment in all DB notebooks
        for line in lines[1:]:
            # PREPROCESSING: each line doesn't directly end up in converted_lines, each if / elif ends with continue

            # Strip any whitespaces, including indentation and trailing newline
            line_stripped = line.strip()

            # Cell separator - reset current_cell_type
            if line == const.CELL_SEPARATOR:
                current_cell_type = const.CellType.NONE
                is_new_cell = True
                continue

            # Ignore the newline immediately following the cell separator
            elif line == "\n" and is_new_cell:
                is_new_cell = False
                continue

            # Suppress widget remove calls
            elif line_stripped.startswith(const.WIDGET_REMOVE_CALL_PREFIX):
                continue

            # Process widget definitions
            elif re.match(const.WIDGET_DEFINITION_PREFIX_RE, line_stripped) or is_widget_definition_in_progress:
                if widget_definition_position is None:
                    # Add class declaration
                    converted_lines.append(get_class_declaration(source_filepath))
                    # Save the position where processed widget definitions will be inserted later
                    widget_definition_position = len(converted_lines)
                    # Set indent, as everything that follows is being added inside class > __init__
                    indent_level = 2
                widget_definition_lines.append(line_stripped)
                is_widget_definition_in_progress = not line_stripped.endswith(")")
                continue

            # REGULAR PROCESSING: each line is added to converted_lines, converted as necessary

            # Strip any trailing whitespaces and ensure there is a newline at the end
            line = line.rstrip() + "\n"

            # Cell title -> comment
            if line.startswith(const.CELL_TITLE_PREFIX):
                converted_lines.append(utils.indent_line(convert_title(line), indent_level))

            # Empty magic line in any magic cell (will also catch "# MAGIC" comments because it's sometimes impossible
            # to distinguish between regular and magic code cells (those starting with "%pip"))
            elif line == const.MAGIC_PREFIX + "\n":
                converted_lines.append("\n")

            # Empty MD line, possibly MD cell
            elif re.match(const.MAGIC_MD_PREFIX_RE + "$", line):
                # If not already a different type, set type to MD and move on
                if current_cell_type == const.CellType.NONE:
                    current_cell_type = const.CellType.MD
                # Otherwise, convert to comment
                else:
                    converted_lines.append(utils.indent_line(convert_magic_to_comment(line), indent_level))

            # Empty RUN line, possibly RUN cell
            elif re.match(const.MAGIC_RUN_PREFIX_RE + "$", line):
                # If not already a different type, set type to RUN and move on
                if current_cell_type == const.CellType.NONE:
                    current_cell_type = const.CellType.RUN
                # Otherwise, convert to comment
                else:
                    converted_lines.append(utils.indent_line(convert_magic_to_comment(line), indent_level))

            # MD prefix, possibly MD cell
            elif re.match(const.MAGIC_MD_PREFIX_RE, line):
                # If not already a different type, set type to MD and convert MD
                if current_cell_type == const.CellType.NONE:
                    current_cell_type = const.CellType.MD
                    # Only the first MD prefix in an MD cell needs to be converted, all others are text
                    converted_lines.append(utils.indent_line(convert_md(line), indent_level))
                # Otherwise, convert to comment
                else:
                    converted_lines.append(utils.indent_line(convert_magic_to_comment(line), indent_level))

            # RUN prefix, possibly RUN cell
            elif re.match(const.MAGIC_RUN_PREFIX_RE, line):
                # If not already a different type, set type to RUN
                if current_cell_type == const.CellType.NONE:
                    current_cell_type = const.CellType.RUN
                # RUN cell
                if current_cell_type == const.CellType.RUN:
                    converted_lines.append(utils.indent_line(self.convert_run(line, source_filepath), indent_level))
                # RUN prefix in a cell of different type - convert to comment
                else:
                    converted_lines.append(utils.indent_line(convert_magic_to_comment(line), indent_level))

            # PIP prefix, most likely a regular/magic CODE cell
            elif re.match(const.PIP_PREFIX_RE, line):
                # If not already a different type, set type to CODE
                if current_cell_type == const.CellType.NONE:
                    current_cell_type = const.CellType.CODE
                # PIP install in a regular/magic CODE cell
                if current_cell_type == const.CellType.CODE and re.match(const.PIP_INSTALL_PREFIX_RE, line):
                    requirements = requirements.union(convert_pip_install(line))
                # Otherwise, convert to comment
                else:
                    converted_lines.append(utils.indent_line(convert_magic_to_comment(line), indent_level))

            # Some magic cell - use current_cell_type to determine how to convert
            elif line.startswith(const.MAGIC_PREFIX):
                # Some other magic prefix - if not already a different type, set type to OTHER
                if re.match(const.MAGIC_SYMBOL_PREFIX_RE, line) and current_cell_type == const.CellType.NONE:
                    current_cell_type = const.CellType.OTHER

                # NONE - should not be possible
                if current_cell_type == const.CellType.NONE:
                    print("WARNING: undetermined cell type:", line)
                # CODE - strip any magic prefix (if in a PIP cell)
                elif current_cell_type == const.CellType.CODE:
                    converted_lines.append(utils.indent_line(convert_code(line), indent_level))
                # MD or other magic -> comment
                elif current_cell_type == const.CellType.MD or current_cell_type == const.CellType.OTHER:
                    converted_lines.append(utils.indent_line(convert_magic_to_comment(line), indent_level))
                # RUN -> import
                elif current_cell_type == const.CellType.RUN:
                    converted_lines.append(utils.indent_line(self.convert_run(line, source_filepath), indent_level))

            # Any other line (code) - as is
            else:
                converted_lines.append(utils.indent_line(convert_code(line), indent_level))

        # All lines processed

        # Process widget definition lines
        if widget_definition_lines and widget_definition_position is not None:
            widgets = convert_widgets(widget_definition_lines)
            init_line = "def __init__(self"
            docstring = utils.indent_line('"""\n', indent_level)
            assignments = ""
            for widget in widgets:
                init_line += ", " + widget.get_arg()
                docstring += utils.indent_line(widget.get_docstring(), indent_level)
                assignments += utils.indent_line(widget.get_assignment(), indent_level)
            init_line += "):\n"
            docstring += utils.indent_line('"""\n', indent_level)
            converted_lines.insert(widget_definition_position, utils.indent_line(init_line, indent_level - 1))
            converted_lines.insert(widget_definition_position + 1, docstring)
            converted_lines.insert(widget_definition_position + 2, assignments)

        # Remove any empty lines at the end (file writer will add one empty line)
        while converted_lines:
            if not converted_lines[-1].strip():
                converted_lines.pop()
            else:
                break

        return converted_lines, requirements

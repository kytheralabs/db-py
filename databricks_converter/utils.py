import re

from databricks_converter import constants as const

_snake_case_pattern = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def to_snake_case(value: str) -> str:
    """
    Converts a string to snake_case, intelligently adding underscores only where necessary and replacing non-word
    characters with underscores
    :param value: A string
    :return: The string in snake case
    """
    return re.sub(r"\W", "_", _snake_case_pattern.sub("_", value).lower().replace(" ", "_"))


def indent_line(line, indent_level):
    return (indent_level * const.INDENT) + line if line.strip() else line

from enum import Enum


class CellType(Enum):
    NONE = ""
    CODE = "code"
    MD = "md"
    RUN = "run"
    OTHER = "other"


TO_PY = "to_py"
TO_DB = "to_db"

REQUIREMENTS_FILENAME = "requirements.txt"

CELL_SEPARATOR = "# COMMAND ----------\n"
CELL_TITLE_PREFIX = "# DBTITLE 1,"

MAGIC_PREFIX = "# MAGIC"
MAGIC_SYMBOL_PREFIX_RE = "^" + MAGIC_PREFIX + r"\s+%"
MAGIC_MD_PREFIX_RE = "^" + MAGIC_PREFIX + r"\s+%md"
MAGIC_RUN_PREFIX_RE = "^" + MAGIC_PREFIX + r"\s+%run"
PIP_PREFIX_RE = "^(?:" + MAGIC_PREFIX + r"\s+)?\s*%pip"
PIP_INSTALL_PREFIX_RE = PIP_PREFIX_RE + r"\s+install\s+"

WIDGET_TYPES = ["combobox", "dropdown", "multiselect", "text"]
WIDGET_PREFIX = "dbutils.widgets."
WIDGET_DEFINITION_PREFIX_RE = r"^dbutils\s*\.\s*widgets\s*\.\s*(?:" + "|".join(WIDGET_TYPES) + r")\s*\("
WIDGET_GET_CALL_RE = r"(dbutils\s*\.\s*widgets\s*\.\s*get\s*\(.+?\))"
WIDGET_GET_ALL_CALL = "dbutils.widgets.getAll()"
WIDGET_REMOVE_CALL_PREFIX = "dbutils.widgets.remove"
INDENT = 4 * " "

# Python to DB
MAGIC_MD_PREFIX = MAGIC_PREFIX + " %md"
MAGIC_RUN_PREFIX = MAGIC_PREFIX + " %run"
DATABRICKS_RELATIVE_IMPORT = "./"
FIRST_LINE = "# Databricks notebook source\n"
MAGIC_TEXT_PLACEHOLDER = "# {text} "
PYTHON_IMPORT = "import "

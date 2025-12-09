from databricks_converter.constants import MAGIC_MD_PREFIX, MAGIC_TEXT_PLACEHOLDER, MAGIC_IMPORT_PREFIX, PYTHON_IMPORT


def remove_magic_str(row, prefix):
    return row.replace(prefix, "")


def convert_md(row):
    no_magic = remove_magic_str(row, MAGIC_MD_PREFIX)
    return no_magic if no_magic.startswith("#") else f"{MAGIC_TEXT_PLACEHOLDER}{no_magic}"


def convert_imports(row):
    no_magic = remove_magic_str(row, MAGIC_IMPORT_PREFIX)
    if no_magic.startswith("/"):
        no_magic = no_magic[1:]
    else:
        no_magic = no_magic[2:]
    return f'{PYTHON_IMPORT}{no_magic.replace("/", ".")}'

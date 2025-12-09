from databricks_converter.constants import MAGIC_IMPORT_PREFIX, PYTHON_IMPORT, MAGIC_TEXT_PLACEHOLDER, MAGIC_MD_PREFIX, \
    DATABRICKS_RELATIVE_IMPORT


def add_magic_str(row, prefix):
    return f"{prefix}{row}"


def convert_to_md(row):
    if row.startswith(MAGIC_TEXT_PLACEHOLDER):
        row = row.replace(MAGIC_TEXT_PLACEHOLDER, "")
    return add_magic_str(row, MAGIC_MD_PREFIX)


def convert_to_run(row):
    import_prefix = DATABRICKS_RELATIVE_IMPORT
    if "." in row:
        import_prefix = "/"
        row = row.replace(".", "/")
    row = f'{import_prefix}{row.replace(PYTHON_IMPORT, "")}'
    return add_magic_str(row, MAGIC_IMPORT_PREFIX)

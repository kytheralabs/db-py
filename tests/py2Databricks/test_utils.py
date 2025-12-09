from databricks_converter.py2Databricks.utils import add_magic_str, convert_to_md, convert_to_run


def test_add_magic_str():
    row = "row"
    prefix = "prefix"
    expected = "prefixrow"
    assert add_magic_str(row, prefix) == expected


def test_convert_to_md_row():
    row = "# Some markdown title"
    expected = "# MAGIC %md # Some markdown title"
    assert convert_to_md(row) == expected


def test_convert_to_md_row_normal_text():
    row = "# {text} Some markdown text"
    expected = "# MAGIC %md Some markdown text"
    assert convert_to_md(row) == expected


def test_convert_to_run():
    import_row = "import rootPath.notebook"
    expected = "# MAGIC %run /rootPath/notebook"
    assert convert_to_run(import_row) == expected


def test_relative_convert_imports():
    import_row = "import local_notebook"
    expected = "# MAGIC %run ./local_notebook"
    assert convert_to_run(import_row) == expected

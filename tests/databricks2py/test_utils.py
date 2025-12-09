from databricks_converter.databricks2py.utils import convert_imports, convert_md


def test_convert_absolute_imports():
    absolute_import_row = "# MAGIC %run /rootPath/notebook"
    expected = "import rootPath.notebook"
    assert convert_imports(absolute_import_row) == expected


def test_relative_convert_imports():
    absolute_import_row = "# MAGIC %run ./local_notebook"
    expected = "import local_notebook"
    assert convert_imports(absolute_import_row) == expected


def test_relative_multiple_convert_imports():
    absolute_import_row = "# MAGIC %run ./local_folder/local_notebook"
    expected = "import local_folder.local_notebook"
    assert convert_imports(absolute_import_row) == expected


def test_convert_md_row():
    md_row = "# MAGIC %md # Some markdown title"
    expected = "# Some markdown title"
    assert convert_md(md_row) == expected


def test_convert_md_row_normal_text():
    md_row = "# MAGIC %md Some markdown text"
    expected = "# {text} Some markdown text"
    assert convert_md(md_row) == expected

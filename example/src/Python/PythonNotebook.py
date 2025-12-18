# Databricks notebook source
# DBTITLE 1,Cell 1 title
print('code cell 1 content')

# COMMAND ----------

   
print('cell without title and blank first line')

# COMMAND ----------

# DBTITLE 1,Widgets
display(dbutils.widgets)
#dbutils.widgets.isGetAllEnabled  # True
#dbutils.widgets.displayHTML("<div style='color:red'>DIV</div>")

# COMMAND ----------

# DBTITLE 1,Widgets create 1
# Single line, keyword
dbutils.widgets.combobox(name="combo", defaultValue="x", choices=["a", "2", ",", '"', "'", "III"], label="Combo box")
dbutils.widgets.dropdown(label="Dropdown box", choices=["a", "2", ",", '"', "'", "III"], defaultValue="2", name="drop")
dbutils.widgets.multiselect(name="multi", defaultValue="III", choices=["a", "2", ",", '"', "'", "III"], label="Multiselect box")

# Single line, positional
dbutils.widgets.multiselect("multi2", "III", ["a", "2", ",", '"', "'", "III"], "Multiselect box 2")
dbutils.widgets.text("text2", "def", "Text box 2")

# Multiline, keyword
dbutils.widgets.combobox(
  label="Combo box 2",
  choices=["a", "2", ",", '"', "'", "III"],
  defaultValue="x",
  name="combo2",
)

# Multiline, positional
dbutils.widgets.dropdown(
  "drop2",
  "2",
  ["a", "2", ",", '"', "'", "III"],
  "Dropdown box 2")

# COMMAND ----------

# DBTITLE 1,Widgets create 2
dbutils.widgets.text(name="text", defaultValue="def", label="Text box")
# Not in UI, but works as normal
#dbutils.widgets.text('', 'asd')

# COMMAND ----------

# DBTITLE 1,Widgets create 3
dbutils.widgets.combobox(name="combo3", defaultValue="x", choices=["a", "b", "c"], label="Combo box")
dbutils.widgets.multiselect("multi3", "a", ["a", "b", "c"], "some_var")
dbutils.widgets.text("text3", defaultValue="Text box 2")
dbutils.widgets.dropdown( "drop3",  " 2", label ='Dropdown box 2',   choices = [ "a",   "b", "c" ], )
dbutils.widgets.text("text4", label="Text box", defaultValue="def", )

# COMMAND ----------

# DBTITLE 1,Widgets get
combo = dbutils.widgets.get(name="combo")
dropdown = dbutils.widgets.get("drop")
multi = dbutils.widgets.get(name="multi")  # Ordered string (not list): 'III,2', 'III,,,a'
text = dbutils . widgets . get ( "text" )
text1 = dbutils . widgets . get ( name = "text1" )  # Nonexistent raises an exception
#text_unnamed = dbutils.widgets.get('')

all_widgets = dbutils.widgets.getAll()
dbutils.widgets.getAll()
# dbutils.widgets.getAll()

#dbutils.widgets.getArgument(name="text", defaultValue="test")  # If widget by this name exists, returns its value (defaultValue doesn't do anything even if the value is falsy) and removes its label
#dbutils.widgets.getArgument(name="text1", defaultValue="test")  # If widget by this name does not exist, creates a new widget, initialized to defaultValue

# COMMAND ----------

# DBTITLE 1,Widgets remove
dbutils.widgets.remove(name="text")
# dbutils.widgets.remove(name="multi")
dbutils.widgets.removeAll()

# COMMAND ----------

 
# code cell without title and with blank first line
if 1:
  print("indented 1")
else:
  if 0:
    print("indented 2")

# COMMAND ----------

# MAGIC %md Markdown

# COMMAND ----------

# DBTITLE 1,MD cell title
# MAGIC
# MAGIC   %md  
# MAGIC # TITLE
# MAGIC  
# MAGIC Regular text
# MAGIC
# MAGIC %md Regular text with %md prefix

# COMMAND ----------

# DBTITLE 1,Run cell with absolute path
# MAGIC  %run " /Workspace/External/Notebook "

# COMMAND ----------

# DBTITLE 1,Multiline run cell with blank first line, relative path
# MAGIC
# MAGIC %run
# MAGIC
# MAGIC  "../CORE/Core Notebook"

# COMMAND ----------

# DBTITLE 1,From the above notebook
print(core_x)

# COMMAND ----------

# DBTITLE 1,Pip install cell
# MAGIC %pip install package1 package2

# COMMAND ----------

# DBTITLE 1,Pip install cell with blank first line
# MAGIC
# MAGIC  %pip install another-package

# COMMAND ----------

# DBTITLE 1,Pip list with regular code cell
# MAGIC  %pip list -q
# MAGIC  print('a')
# MAGIC %pip list
# MAGIC b = 1
# MAGIC print(f"{b}")

# COMMAND ----------

# DBTITLE 1,Pip list with regular code cell 2
print('a')
%pip list
# MAGIC
%pip list -q

# COMMAND ----------

# DBTITLE 1,Shell cell
# MAGIC %sh
# MAGIC
# MAGIC ls -al
# MAGIC python -V

# COMMAND ----------

# DBTITLE 1,SQL cell
# MAGIC %sql
# MAGIC
# MAGIC select count(*)
# MAGIC from hive_metastore.example.samples;

# COMMAND ----------

# DBTITLE 1,Magics
# MAGIC %%!
# MAGIC ls -al
# MAGIC
# MAGIC #%ls -al

# COMMAND ----------

# DBTITLE 1,Magic HTML
# MAGIC %%HTML
# MAGIC <div style='color:red'>DIV</div>

# COMMAND ----------

# DBTITLE 1,Magic JS
# MAGIC %%js
# MAGIC console.log('test')

# COMMAND ----------

# DBTITLE 1,Cell with % and 3 empty lines at the end
# MAGIC
# MAGIC %
# MAGIC
# MAGIC  %
# MAGIC
# MAGIC  
# MAGIC
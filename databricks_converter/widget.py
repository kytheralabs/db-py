import ast

from databricks_converter import constants as const


def get_widget_name_from_getter(getter_call):
    try:
        tree = ast.parse(getter_call.strip(), mode="eval")
    except SyntaxError:
        raise ValueError("Unable to parse widget getter call: " + getter_call)

    if not isinstance(tree.body, ast.Call) or not isinstance(tree.body.func, ast.Attribute):
        raise ValueError("Incorrect widget getter call: " + getter_call)

    positional_args = [ast.literal_eval(arg) for arg in tree.body.args]
    named_args = {kw.arg: ast.literal_eval(kw.value) for kw in tree.body.keywords}

    name = named_args["name"] if "name" in named_args else positional_args[0] if len(positional_args) > 0 else ""
    if not name:
        raise ValueError("Widget name is required")
    return f"self.{name}"


class Widget:
    def __init__(self, definition):
        self.definition = definition.strip()
        self.widget_type = ""
        self.name = ""
        self.default_value = ""
        self.choices = None
        self.label = ""
        self.parse()

    def __repr__(self):
        name = self.name.replace('"', r"\"") if self.name else ""
        default_value = self.default_value.replace('"', r"\"") if self.default_value else ""
        choices = (", choices=" + self.choices) if self.choices is not None else ""
        label = self.label.replace('"', r"\"") if self.label else ""
        return f'{self.widget_type}(name="{name}", default_value="{default_value}{choices}, label="{label}")'

    def parse(self):
        # Parse the input into an AST node
        try:
            tree = ast.parse(self.definition.strip(), mode="eval")
        except SyntaxError:
            raise ValueError("Unable to initialize widget: " + self.definition)

        # Ensure the tree's body is a Call node
        if not isinstance(tree.body, ast.Call) or not isinstance(tree.body.func, ast.Name):
            raise ValueError("Incorrect widget initialization: " + self.definition)

        # Ensure the widget type is supported
        self.widget_type = tree.body.func.id
        if self.widget_type not in const.WIDGET_TYPES:
            raise ValueError("Unsupported widget type: " + self.widget_type)

        # Extract positional and keyword arguments
        positional_args = [ast.literal_eval(arg) for arg in tree.body.args]
        named_args = {kw.arg: ast.literal_eval(kw.value) for kw in tree.body.keywords}

        self.name = (
            named_args["name"] if "name" in named_args else positional_args[0] if len(positional_args) > 0 else ""
        )
        if not self.name:
            raise ValueError("Widget name is required")
        self.default_value = (
            named_args["defaultValue"]
            if "defaultValue" in named_args
            else positional_args[1]
            if len(positional_args) > 1
            else ""
        )
        self.choices = (
            named_args["choices"]
            if "choices" in named_args
            else positional_args[2]
            if len(positional_args) > 2 and self.widget_type in const.WIDGET_TYPES[:-1]
            else None
        )
        self.label = (
            named_args["label"]
            if "label" in named_args
            else positional_args[3]
            if len(positional_args) > 3 and self.widget_type in const.WIDGET_TYPES[:-1]
            else positional_args[2]
            if len(positional_args) > 2 and self.widget_type in const.WIDGET_TYPES[-1]
            else ""
        )

    def get_arg(self):
        return self.name + '="' + self.default_value + '"'

    def get_docstring(self):
        return (
            ":param "
            + self.name
            + ": "
            + ((repr(self.choices) + " ") if self.choices is not None else "")
            + self.label
            + "\n"
        )

    def get_assignment(self):
        return f"self.{self.name} = {self.name}\n"

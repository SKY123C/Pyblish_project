import importlib
import os

from util import utility

current_path = os.path.dirname(__file__)
path_name = os.path.basename(current_path)
for file_name in os.listdir(current_path):
    name, file_type = os.path.splitext(file_name)
    validation = utility.get_validation_name()
    if file_type.endswith('.py') and name != "__init__":
        module = importlib.import_module(f".{name}", package=f"{validation}.{path_name}")
        importlib.reload(module)


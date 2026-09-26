import os
import importlib.util

folder = "my_folder"

for filename in os.listdir(folder):
    if filename.endswith(".py"):
        path = os.path.join(folder, filename)
        module_name = filename[:-3]

        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

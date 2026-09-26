import os
import importlib

for filename in os.listdir("folder"):
    if filename.endswith(".py") and filename != "__init__.py":
        importlib.import_module(f"Cards.{filename[:-3]}")

import os
import importlib

"""
for filename in os.listdir("folder"):
    if filename.endswith(".py") and filename != "__init__.py":
        importlib.import_module(f"Cards.{filename[:-3]}")
"""

if __name__ == "__main__":
    for filename in os.listdir("Cards"):
        if filename.endswith(".py") and filename != "__init__.py":
            importlib.import_module(f"Cards.{filename[:-3]}")

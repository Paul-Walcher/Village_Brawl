import os
import sys
import importlib
import terminal_functions as terminal






if __name__ == "__main__":

    import_folder = "import_test_folder.test_folder"
    module = importlib.import_module(f"{import_folder}.test")
    globals()["test"] = module
    globals()["hi"] = test.hi
    module = importlib.import_module(f"{import_folder}.test2")
    globals()["test2"] = module


    hi()

    for name, module in sys.modules.items():
        print(name)

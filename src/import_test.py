import os
import sys
import importlib
import terminal_functions as terminal






if __name__ == "__main__":

    head, tail = os.path.split(os.path.abspath(__file__))
    import_folder = os.path.join(head, "import_test_folder")
    filename = "test.py"
    module = importlib.import_module(f"import_test_folder.test")
    globals()[filename[:-3]] = module


    test.hi()

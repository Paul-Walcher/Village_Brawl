
"""
Used for loading a playset.
"""
import os
import sys
import importlib

import time

import constants


def load_playset(context):

    modules = context.modules

    playset_path = constants.PLAYSETS_FOLDER + "." + context.gameinfo.current_playset
    #loading the explorer
    enums_module = importlib.import_module(f"{playset_path}.enums")
    modules.enums_module = enums_module
    #
    explorer_module = importlib.import_module(f"{playset_path}.explorer")
    modules.explorer_module = explorer_module
    #
    mappings_module = importlib.import_module(f"{playset_path}.mappings")
    modules.mappings_module = mappings_module

    modules.create_refs()


    if constants.__EXTRA_LOAD_TIME__:
        time.sleep(3)

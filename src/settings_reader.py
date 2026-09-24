"""
Reads the settings definition
provided by settings.json
"""
from __future__ import annotations
from typing import Callable

import json
import sys

from global_context import Global_Context

SETTINGS_FILE: str = "settings.json"

def read_settings(global_context: Global_Context):

    local_context = global_context.copy()

    try:

        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)

            local_context.settings.monochrome_assets = data["monochrome_assets"]
            local_context.settings.full_color = data["full_color"]
            local_context.settings.low_res = data["low_res"]
            local_context.settings.mid_res = data["mid_res"]
            local_context.settings.high_res = data["high_res"]
            local_context.settings.very_high_res = data["very_high_res"]

    except Exception as e:

        print(5*"\n"+"Could not load settings. Aborting..."+"\n"*5)
        sys.exit()


    return local_context

"""
Reads the settings definition
provided by settings.json
"""
from __future__ import annotations
from typing import Callable

import json

from global_context import Global_Context

SETTINGS_FILE: str = "settings.json"

def read_settings(global_context: Global_Context):

    local_context = global_context.copy()

    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)

        local_context.settings.monochrome_assets = data["monochrome_assets"]
        local_context.settings.full_color = data["full_color"]

    return local_context

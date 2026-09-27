import os
import sys

import assets.ascii_assets as ascii_assets
import terminal_functions as terminal
import colorama
import constants
import logic
from logic import Zoomrestore
import global_context
from gamestatehandler import GamestateHandler


colorama.init()

if not terminal.terminal_is_maximized():
    terminal.toggle_terminal_size()

if not constants.__DEBUG__:
    terminal.disable_scrollback()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

handler = GamestateHandler()
handler.run()

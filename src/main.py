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

terminal.disable_scrollback()

handler = GamestateHandler()
handler.run()

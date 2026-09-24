import assets.ascii_assets as ascii_assets
import terminal_functions as terminal
import colorama
import constants
import logic
from logic import Zoomrestore
import global_context


context = global_context.Global_Context()

colorama.init()

if not terminal.terminal_is_maximized():
    terminal.toggle_terminal_size()

context = logic.intro(context)
#now the selection of save or new game
with Zoomrestore(context):
    logic.new_game_or_save_selection(context)

logic.finish(context)

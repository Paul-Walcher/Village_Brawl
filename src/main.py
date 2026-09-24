import assets.ascii_assets as ascii_assets
import terminal_functions as terminal
import colorama
import constants
import logic
import global_context


context = global_context.Global_Context()

colorama.init()

if not terminal.terminal_is_maximized():
    terminal.toggle_terminal_size()

logic.intro(context)

logic.finish(context)

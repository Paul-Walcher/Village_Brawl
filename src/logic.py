"""
Several functions for
logic.
"""
import os
import sys
import random

import constants
import global_context
import graphics
import terminal_functions as terminal
import settings_reader

def intro(context):

    terminal.clear()

    #reading settings
    context = settings_reader.read_settings(context)

    files = list(os.listdir(constants.STANDARD_IMAGE_PATH))

    chosen_image = random.choice(files)
    chosen_image_fullpath = os.path.join(constants.STANDARD_IMAGE_PATH, chosen_image)

    graphics.print_intro(context, chosen_image_fullpath)
    terminal.scroll_up(10)


    input()

def finish(context):

    #clear text
    terminal.clear()
    #first toggle back into minimized window
    if terminal.terminal_is_maximized():
        terminal.toggle_terminal_size()

    #do other stuff

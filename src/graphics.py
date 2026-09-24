"""
Defines several functions for printing.
"""
import random

import terminal_functions as terminal
import global_context
import constants

def print_intro(context, intro_image_path):

    print("\n"*2)
    terminal.text_rgb(255, 0, 0)
    headline = terminal.ansi_shadow("Village Brawl")
    terminal.print_centered(headline)
    terminal.color_reset()

    #image printing
    resolution = context.settings.mid_res

    image = terminal.image_to_ascii_from_context(intro_image_path, resolution, context)

    terminal.print_centered(image)
    print("Press any Key to continue...")

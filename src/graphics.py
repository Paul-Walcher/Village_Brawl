"""
Defines several functions for printing.
"""
import os
import random

import terminal_functions as terminal
import global_context
import constants
import states
import time

def print_intro(context, intro_image_path):


    print("\n"*2)
    terminal.text_rgb(255, 0, 0)
    terminal.print_figlet("Village Brawl", "ansi_shadow")
    terminal.color_reset()

    #image printing
    resolution = context.settings.mid_res

    image = terminal.image_to_ascii_from_context(intro_image_path, resolution, context)

    terminal.print_centered(image)
    print("Press enter to continue...")

def print_new_game_or_save_selection(context, selection_state):

    #for highlighting the current option
    def print_highlighted(text):

        terminal.print_centered(text, text_color=(255, 255, 0))
        terminal.color_reset()
        print()

    terminal.clear()
    terminal.hide_cursor(context)

    print("\n"*5)

    if selection_state == states.New_Game_Or_Save_Selection_Enum.New_Game:
        print_highlighted("New Game")
    else:
        print("New Game")
    if selection_state == states.New_Game_Or_Save_Selection_Enum.Load_Save:
        print_highlighted("Load Save")
    else:
        print("Load Save")
    if selection_state == states.New_Game_Or_Save_Selection_Enum.Go_Back:
        print_highlighted("Go Back")
    else:
        print("Go Back")

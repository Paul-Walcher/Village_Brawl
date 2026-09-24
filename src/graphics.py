"""
Defines several functions for printing.
"""
import os
import random

import terminal_functions as terminal
import global_context
import constants
import states

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

def print_new_game_or_save_selection(context, selection_state):


    #for highlighting the current option
    def print_highlighted(text):

        terminal.text_rgb(0, 0, 0)
        terminal.background_rgb(255, 255, 255)
        print(text, end="")
        terminal.color_reset()
        print()

    terminal.clear()
    terminal.hide_cursor(context)

    terminal.zoom_in(context, 5)

    if selection_state == states.New_Game_Or_Save_Selection_Enum.New_Game:
        print_highlighted("New Game")
    else:
        print("New Game")
    if selection_state == states.New_Game_Or_Save_Selection_Enum.Load_Save:
        print_highlighted("Load_Save")
    else:
        print("Load_Save")
    if selection_state == states.New_Game_Or_Save_Selection_Enum.Go_Back:
        print_highlighted("Go Back")
    else:
        print("Go Back")

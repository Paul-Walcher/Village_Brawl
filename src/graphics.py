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
import io
import sys

class NewPage:


    def __init__(self):
        self.old_stdout = None
        self.buffer = io.StringIO()

    def redraw(self):
        sys.stdout.write(
            "\x1b[2J\x1b[H"  # clear screen + move cursor home
            + self.buffer.getvalue()
        )
        sys.stdout.flush()

    def __enter__(self):

        self.old_stdout = sys.stdout
        sys.stdout = self.buffer

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        sys.stdout = self.old_stdout
        self.redraw()

        return False


def box(text, margin=2):

    """
    Puts a box of | around the text.
    """
    lines = text.splitlines()
    longest_line = max([len(line) for line in lines])

    box_width = 2 + 2*margin + longest_line

    boxed_text = ""
    boxed_text += "-" * (2 + margin + margin + longest_line) + "\n"

    for line in lines:
        size = len(line)
        boxed_text += "|"
        boxed_text += " " * margin
        boxed_text += line
        boxed_text += " " * (box_width - (2 + margin + len(line)))
        boxed_text += "|\n"

    boxed_text += "-" * (margin + margin + longest_line) + "\n"

    return boxed_text



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

def print_new_game(context, savefile_name, selection_state):

    old_stdout = sys.stdout
    buffer = io.StringIO()

    HIGHLIGHT_COLOR = (255, 255, 0)
    #for highlighting the current option
    def print_highlighted(text):

        terminal.print_centered(text, text_color=HIGHLIGHT_COLOR)
        terminal.color_reset()
        print()

    with NewPage():

        terminal.print_centered("Choose a name for your savefile:")
        print("\n"*3)

        #selection states:
        #0: savefile_name
        #1: back
        #2: start

        if selection_state == 0:
            print_highlighted(savefile_name)

        else:
            terminal.print_centered(savefile_name)

        if not savefile_name:

            print()

        print("\n"*8)

        if selection_state == 1:
            terminal.text_rgb(*HIGHLIGHT_COLOR)
            print("Back", end="")
            terminal.color_reset()

        else:
            print("Back", end="")

        dist = 39

        print(" "*dist, end="")

        if selection_state == 2:

            terminal.text_rgb(*HIGHLIGHT_COLOR)
            print("Playset Selection")
            terminal.color_reset()

        else:

            print("Playset Selection")

def print_select_playset(local_object):

    HIGHLIGHT_COLOR = (255, 255, 0)
    #for highlighting the current option
    def print_highlighted(text):

        terminal.print_centered(text, text_color=HIGHLIGHT_COLOR)
        terminal.color_reset()

    objects_shown = local_object.objects_shown
    playsets = local_object.found_playsets
    selection_state = local_object.selection_state

    with NewPage():

        print("\n"*5)
        select_text = terminal.render_text("ansi_shadow", "Playset")
        terminal.print_centered(select_text, text_color=(43,220,221))
        print("\n"*4)

        if len(playsets) > 0:

            min_print = len(playsets) - local_object.scroll - 1
            min_print = (min_print if min_print > 0 else 0)

            if (selection_state == 1):
                print_highlighted(playsets[local_object.scroll])
            else:
                terminal.print_centered(playsets[local_object.scroll])

            for i in range(min(objects_shown, min_print)):
                terminal.print_centered(playsets[local_object.scroll + i + 1])

            if (min_print < objects_shown):

                print("\n" * (objects_shown-min_print - 1))

        print("\n"*2)
        backtext = terminal.render_text("ANSI Compact", "Back")
        if (selection_state == 0):
            terminal.text_rgb(255, 255, 0)
            print(backtext, end="")
            terminal.color_reset()
            print()
        else:
            terminal.text_rgb(*(43,220,221))
            print(backtext, end="")
            terminal.color_reset()
            print()

def print_loading_screen(dots):

    with NewPage():

        print("\n"*20)
        text = "Loading ." + "." * dots
        text = terminal.render_text("ansi_shadow", text)
        terminal.print_centered(text)

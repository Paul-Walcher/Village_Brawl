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
import keyboard
import states


class Zoomrestore:

    zoom_saves = {}
    zoom_savenumber = 1

    @staticmethod
    def zoom_snapshot(context):
        snapshot_index = Zoomrestore.zoom_savenumber
        Zoomrestore.zoom_savenumber += 1

        Zoomrestore.zoom_saves[snapshot_index] = context.current_zoom

        return snapshot_index

    @staticmethod
    def restore_zoom(context, snapshot_index):
        if snapshot_index not in Zoomrestore.zoom_saves:
            raise RuntimeError("The Zoom snapshot does not exist")

        saved_zoom = Zoomrestore.zoom_saves.pop(snapshot_index)

        terminal.zoom_to(context, saved_zoom)

    def __init__(self, context):
        self.context = context
        self.snapshot = None

    def __enter__(self):
        self.snapshot = Zoomrestore.zoom_snapshot(self.context)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        Zoomrestore.restore_zoom(self.context, self.snapshot)
        return False

def intro(context):

    terminal.clear()

    #reading settings
    context = settings_reader.read_settings(context)

    files = list(os.listdir(constants.STANDARD_IMAGE_PATH))
    files = [file for file in files if file.endswith(".png") or file.endswith(".jpg")  or file.endswith(".jpeg")]

    chosen_image = random.choice(files)
    chosen_image_fullpath = os.path.join(constants.STANDARD_IMAGE_PATH, chosen_image)

    graphics.print_intro(context, chosen_image_fullpath)
    terminal.scroll_up(10)


    input()

def finish(context):

    #clear text
    terminal.clear()
    #zooming to normal
    if context.current_zoom > 0:
        terminal.zoom_out(context.current_zoom)
    elif context.current_zoom < 0:
        terminal.zoom_in(abs(context.current_zoom))


    context.current_zoom = 0
    #first toggle back into minimized window
    if terminal.terminal_is_maximized():
        terminal.toggle_terminal_size()

    #do other stuff


def new_game_or_save_selection(context):

    #for either selecting a new game or
    #going to the savestates

    #selection state
    selection_state = states.New_Game_Or_Save_Selection_Enum.New_Game

    num_encoding = {    0: states.New_Game_Or_Save_Selection_Enum.New_Game,
                        1: states.New_Game_Or_Save_Selection_Enum.Load_Save,
                        2: states.New_Game_Or_Save_Selection_Enum.Go_Back
                    }

    current_encoding = 0


    graphics.print_new_game_or_save_selection(context, selection_state)

    w_pressed = False
    s_pressed = False

    quit = False

    while not quit:

        if keyboard.is_pressed("w") and not w_pressed:
            w_pressed = True
            current_encoding -= 1
            current_encoding %= 3
            selection_state = num_encoding[current_encoding]
            graphics.print_new_game_or_save_selection(context, selection_state)

        if not keyboard.is_pressed("w") and w_pressed:
            w_pressed = False

        if keyboard.is_pressed("s") and not s_pressed:
            s_pressed = True
            current_encoding += 1
            current_encoding %= 3
            selection_state = num_encoding[current_encoding]
            graphics.print_new_game_or_save_selection(context, selection_state)

        if not keyboard.is_pressed("s") and s_pressed:
            s_pressed = False
        if keyboard.is_pressed("esc"):
            quit = True
            selection_state = "ESCAPE"
            continue

    if selection_state == "ESCAPE":
        return

"""
Several functions for
logic.
"""
import os
import sys
import random
import time

import constants
import global_context
import graphics
import terminal_functions as terminal
import settings_reader
import keyboard
import states
from states import Gamestates


KEY_RELEASE_BUFEER = 0.5

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

def intro(gamestatehandler):

    context = gamestatehandler.context

    terminal.clear()

    #reading settings
    context = settings_reader.read_settings(context)

    gamestatehandler.context = context

    chosen_image = random.choice(constants.INTRO_IMAGES)
    chosen_image_fullpath = os.path.join(constants.STANDARD_IMAGE_PATH, chosen_image)

    graphics.print_intro(context, chosen_image_fullpath)
    terminal.scroll_up(2)

    time.sleep(KEY_RELEASE_BUFEER)

    terminal.wait_for_key("enter")

    return Gamestates.NEW_GAME_OR_LOAD_SAVE

def finish(gamestatehandler):

    context = gamestatehandler.context

    #clear text
    terminal.clear()

    #first toggle back into minimized window
    if terminal.terminal_is_maximized():
        terminal.toggle_terminal_size()


    terminal.reset_zoom(context)

    terminal.clear_keyboard_buffer()
    #do other stuff
    return Gamestates.EXIT

def new_game_or_save_selection(gamestatehandler):

    #for either selecting a new game or
    #going to the savestates

    context = gamestatehandler.context
    #selection state
    selection_state = states.New_Game_Or_Save_Selection_Enum.New_Game

    num_encoding = {    0: states.New_Game_Or_Save_Selection_Enum.New_Game,
                        1: states.New_Game_Or_Save_Selection_Enum.Load_Save,
                        2: states.New_Game_Or_Save_Selection_Enum.Go_Back
                    }

    current_encoding = 0

    terminal.zoom_in(context, 20)


    graphics.print_new_game_or_save_selection(context, selection_state)

    terminal.zoom_out(context, 5)

    w_pressed = False
    s_pressed = False

    quit = False

    while not quit:

        if keyboard.is_pressed("w") and not w_pressed:
            w_pressed = True
            current_encoding -= 1
            current_encoding %= 3
            selection_state = num_encoding[current_encoding]
            with Zoomrestore(context):
                graphics.print_new_game_or_save_selection(context, selection_state)

        if not keyboard.is_pressed("w") and w_pressed:
            w_pressed = False

        if keyboard.is_pressed("s") and not s_pressed:
            s_pressed = True
            current_encoding += 1
            current_encoding %= 3
            selection_state = num_encoding[current_encoding]
            with Zoomrestore(context):
                graphics.print_new_game_or_save_selection(context, selection_state)

        if not keyboard.is_pressed("s") and s_pressed:
            s_pressed = False
        if keyboard.is_pressed("esc"):
            quit = True
            selection_state = "ESCAPE"
            continue

        if keyboard.is_pressed("enter"):
            break

    if selection_state == "ESCAPE":
        return Gamestates.FINISH

    if selection_state == states.New_Game_Or_Save_Selection_Enum.Go_Back:

        return Gamestates.INTRO

    else:

        return Gamestates.FINISH

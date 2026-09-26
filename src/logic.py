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
    terminal.reset_zoom(context)

    #reading settings
    context = settings_reader.read_settings(context)

    gamestatehandler.context = context

    chosen_image = random.choice(constants.INTRO_IMAGES)
    chosen_image_fullpath = os.path.join(constants.STANDARD_IMAGE_PATH, chosen_image)

    graphics.print_intro(context, chosen_image_fullpath)
    terminal.scroll_up(2)

    time.sleep(KEY_RELEASE_BUFEER)

    terminal.wait_for_key("enter")

    #gamestates
    #current state is intro
    gamestatehandler.state_stack.pop()
    #pushing new state
    gamestatehandler.state_stack.push(Gamestates.NEW_GAME_OR_LOAD_SAVE)

def finish(gamestatehandler):

    context = gamestatehandler.context

    terminal.enable_scrollback()

    #cleaning up all open terminals
    for handle in context.terminal_handles:
        terminal.close(context, handle)
        time.sleep(0.1)

    #clear text
    terminal.clear()

    #first toggle back into minimized window
    if terminal.terminal_is_maximized():
        terminal.toggle_terminal_size()


    terminal.reset_zoom(context)

    terminal.clear_keyboard_buffer()

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

    focus_zoom = 0
    defocus_zoom = 0

    terminal.zoom_to(context, 20)

    graphics.print_new_game_or_save_selection(context, selection_state)

    w_pressed = False
    s_pressed = False
    enter_pressed = False

    quit = False
    handle = None

    if "RUNNING" not in context.misc:
        context.misc["RUNNING"] = False
    if "HANDLE" not in context.misc:
        context.misc["HANDLE"] = None

    gamestatehandler.state_stack.pop()


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

        if keyboard.is_pressed("enter") and not enter_pressed:

            if selection_state == "ESCAPE":
                gamestatehandler.state_stack.push(Gamestates.FINISH)
                quit = True

            elif selection_state == states.New_Game_Or_Save_Selection_Enum.Go_Back:

                gamestatehandler.state_stack.push(Gamestates.INTRO)
                quit = True

            elif selection_state == states.New_Game_Or_Save_Selection_Enum.New_Game:

                gamestatehandler.state_stack.push(Gamestates.NEW_GAME)
                quit = True

            else:

                if not context.misc["RUNNING"]:
                    args = [os.path.join(constants.STANDARD_IMAGE_PATH, "Wood.png"), str(context.settings.mid_res),
                            str(int(context.settings.full_color)), str(int(context.settings.monochrome_assets))]
                    context.misc["HANDLE"] = terminal.split_horizontally(context, "split_terminal_files/draw_image.py", args)
                    context.misc["RUNNING"] = True

                    time.sleep(0.3)

                    terminal.focus_prev(context)
                    graphics.print_new_game_or_save_selection(context, selection_state)

                else:
                    terminal.close(context, context.misc["HANDLE"])
                    time.sleep(0.1)
                    terminal.focus_prev(context)
                    context.misc["RUNNING"] = False

            enter_pressed = True

        if not keyboard.is_pressed("enter") and enter_pressed:
            enter_pressed = False



def new_game(gamestatehandler):

    gamestatehandler.state_stack.pop()

    context = gamestatehandler.context

    class LocalObject:

        def __init__(self, ctxt, gsh):
            self.quit = False
            self.gamestatehandler = gsh
            self.context = ctxt
            self.selection_state =  0
            self.save_name = ""


    def esc_pressed(key, local_object):
        local_object.quit = True
        local_object.gamestatehandler.state_stack.push(states.Gamestates.FINISH)

    def key_pressed(key, local_object):

        if keyboard.is_pressed("left") or keyboard.is_pressed("right"):
            return

        if key in constants.VALID_SYMBOLS:

            if keyboard.is_pressed("-") and keyboard.is_pressed("shift"):
                key = "_"

            local_object.save_name += key
            local_object.selection_state = 0
            graphics.print_new_game(local_object.context, local_object.save_name, local_object.selection_state)

    def delete_last_character(key, local_object):

        if local_object.save_name:
            local_object.save_name = local_object.save_name[:-1]
            graphics.print_new_game(local_object.context, local_object.save_name, local_object.selection_state)

    def left_pressed(key, local_object):

        local_object.selection_state += 1
        local_object.selection_state %= 3
        graphics.print_new_game(local_object.context, local_object.save_name, local_object.selection_state)

    def right_pressed(key, local_object):

        local_object.selection_state -= 1
        local_object.selection_state %= 3
        graphics.print_new_game(local_object.context, local_object.save_name, local_object.selection_state)

    def enter_pressed(key, local_object):

        #back
        if local_object.selection_state == 1:
            local_object.quit = True
            local_object.gamestatehandler.state_stack.push(states.Gamestates.NEW_GAME_OR_LOAD_SAVE)

        elif local_object.selection_state == 2:
            if local_object.save_name:
                local_object.context.gameinfo.savefile_name = local_object.save_name
                local_object.quit = True
                local_object.gamestatehandler.state_stack.push(states.Gamestates.SELECT_PLAYSET)





    local_object = LocalObject(context, gamestatehandler)

    keycallback = terminal.KeyCallback()
    keycallback.register_key("esc", esc_pressed)
    keycallback.register_key("backspace", delete_last_character)
    keycallback.register_key("left", left_pressed)
    keycallback.register_key("right", right_pressed)
    keycallback.register_key("enter", enter_pressed)
    for symbol in constants.VALID_SYMBOLS:
        keycallback.register_key(symbol, key_pressed)

    #zooming
    terminal.zoom_to(context, 25)
    #printing
    graphics.print_new_game(context, local_object.save_name, local_object.selection_state)

    while not local_object.quit:

        keycallback.check_presses(local_object)

def select_playset(gamestatehandler):


    gamestatehandler.state_stack.pop()
    context = gamestatehandler.context

    terminal.clear()
    terminal.zoom_to(context, 25)

    #reading playset folder
    found_playsets = [dir for dir in os.listdir(constants.PLAYSETS_PATH) if os.path.isdir(os.path.join(constants.PLAYSETS_PATH, dir))]


    class LocalObject:

        def __init__(self):

            self.quit = False
            self.state_stack = None
            self.context = None
            #0: Back, 1: Playset
            self.selection_state = 1
            self.num_playsets = None
            self.found_playsets = None
            self.scroll = 0
            self.redraw = None
            self.objects_shown = 5



    local_object = LocalObject()
    local_object.context = context
    local_object.state_stack = gamestatehandler.state_stack
    local_object.found_playsets = found_playsets.copy()
    local_object.num_playsets = len(local_object.found_playsets)

    def esc_pressed(key, local_object):

        local_object.quit = True
        local_object.state_stack.push(states.Gamestates.FINISH)

    def enter_pressed(key, local_object):

        if local_object.selection_state == 0:
            local_object.quit = True
            local_object.state_stack.push(states.Gamestates.NEW_GAME_OR_LOAD_SAVE)


    def s_pressed(key, local_object):

        if (local_object.scroll < local_object.num_playsets - 1 - local_object.objects_shown):
            local_object.scroll += 1
            graphics.print_select_playset(local_object)

    def w_pressed(key, local_object):

        if (local_object.scroll > 0):
            local_object.scroll -= 1
            graphics.print_select_playset(local_object)

    def a_pressed(key, local_object):

        local_object.selection_state += 1
        local_object.selection_state %= 2
        graphics.print_select_playset(local_object)

    def d_pressed(key, local_object):

        local_object.selection_state += 1
        local_object.selection_state %= 2
        graphics.print_select_playset(local_object)


    keycallback = terminal.KeyCallback()
    keycallback.register_key("esc", esc_pressed)
    keycallback.register_key("enter", enter_pressed)
    keycallback.register_key("w", w_pressed)
    keycallback.register_key("s", s_pressed)
    keycallback.register_key("a", a_pressed)
    keycallback.register_key("d", d_pressed)

    graphics.print_select_playset(local_object)

    while not local_object.quit:

        keycallback.check_presses(local_object)

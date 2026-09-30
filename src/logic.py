"""
Several functions for
logic.
"""
import os
import sys
import random
import time
import threading

import constants
import global_context
import graphics
import terminal_functions as terminal
import settings_reader
import keyboard
import states
from states import Gamestates
import playset_loader
import phases
import cv2

KEY_RELEASE_BUFEER = 0.5

class Stack:

    def __init__(self):

        self.stack = []

    def size(self):
        return len(self.stack)

    def top(self):

        if self.size() > 0:
            return self.stack[-1]
        else:
            return None

    def push(self, obj):

        self.stack.append(obj)

    def pop(self):
        return self.stack.pop()


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

class Clock:

    def __init__(self):
        self.start_time = 0

    def start(self):
        #in ms
        self.start_time = time.perf_counter() * 10E6

    def elapsed(self):

        return (time.perf_counter() * 10E6) - self.start_time

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
    terminal.zoom_to(context, 10)

    #reading playset folder
    found_playsets = [dir for dir in os.listdir(constants.PLAYSETS_FOLDER_PATH) if os.path.isdir(os.path.join(constants.PLAYSETS_FOLDER_PATH, dir))]


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
        elif local_object.selection_state == 1:
            local_object.quit = True
            local_object.context.gameinfo.current_playset = local_object.found_playsets[local_object.scroll]
            local_object.state_stack.push(states.Gamestates.LOAD_PLAYSET)


    def s_pressed(key, local_object):

        if (local_object.scroll < local_object.num_playsets - 1):
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

def load_playset(gamestatehandler):

    gamestatehandler.state_stack.pop()
    terminal.clear()


    terminal.zoom_to(gamestatehandler.context, 0)

    graphics.print_loading_screen(0)

    lock = threading.Lock()

    class LocalObject:

        def __init__(self):

            self.gamestatehandler = None
            self.lock = None
            self.loading_finished = False
            self.clock = None
            self.dots = 0

    local_object = LocalObject()
    local_object.gamestatehandler = gamestatehandler
    local_object.lock = lock
    local_object.clock = Clock()

    def loading_rendering(local_object):

        context = local_object.gamestatehandler.context
        clock = local_object.clock
        lock = local_object.lock

        update_time = 0.5 * 10E6
        max_dots = 4

        quit = False

        clock.start()

        while not quit:

            with lock:
                if local_object.loading_finished:
                    quit = True

            if clock.elapsed() > update_time:

                local_object.dots += 1
                local_object.dots %= max_dots
                clock.start()

            graphics.print_loading_screen(local_object.dots)


    def loading_playset(local_object):

        context = local_object.gamestatehandler.context
        playset_loader.load_playset(context)

        with local_object.lock:

            local_object.loading_finished = True

    t1 = threading.Thread(target=loading_rendering, args=(local_object,))
    t2 = threading.Thread(target=loading_playset, args=(local_object,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    gamestatehandler.state_stack.push(states.Gamestates.CHOOSE_EXPLORER)

def choose_explorer(gamestatehandler):

    gamestatehandler.state_stack.pop()
    context = gamestatehandler.context
    modules = context.modules

    explorers = list(modules.explorer_mappings.keys())

    terminal.clear()
    terminal.zoom_to(context, -1)

    class LocalObject:

        def __init__(self):

            self.gamestatehandler = None
            self.context = None
            self.modules = None
            self.explorers = None
            self.explorer_index = 0
            self.show_info = False
            self.quit = False

            #img_handle
            self.img_handle = None

            #states
            self.explorer_preview = 0
            self.explorer_hd = 1

            self.current_state = self.explorer_preview

            self.zoom = 20




    local_object = LocalObject()
    local_object.gamestatehandler = gamestatehandler
    local_object.context = context
    local_object.modules = modules
    local_object.explorers = explorers

    graphics.print_explorer(local_object)

    def enter_pressed(key, local_object):
        local_object.quit = True

    def real_image_pressed(key, local_object):

        terminal.show_real_image(constants.STANDARD_IMAGE_PATH + "\\" + "Twig.png")

    def ultra_hd_key_pressed(key, local_object):

        context = local_object.context
        if local_object.current_state == local_object.explorer_preview:
            terminal.zoom_to(context, -10)
            graphics.print_ultra_hd_explorer(local_object)
            local_object.current_state = local_object.explorer_hd
        elif local_object.current_state == local_object.explorer_hd:
            terminal.zoom_to(context, -1)
            graphics.print_explorer(local_object)
            local_object.current_state = local_object.explorer_preview


    keycallback = terminal.KeyCallback()
    keycallback.register_key("enter", enter_pressed)
    keycallback.register_key(context.settings.ultra_hd_image_key, ultra_hd_key_pressed)
    keycallback.register_key(context.settings.real_image_key, real_image_pressed)

    while not local_object.quit:

        keycallback.check_presses(local_object)



    gamestatehandler.state_stack.push(states.Gamestates.FINISH)

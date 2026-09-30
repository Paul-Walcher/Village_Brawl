"""
Global context to be given to each function
dealing with interactions.
"""

import playset_loader
import cv2
import constants
import terminal_functions as terminal
from states import SplitscreenState

class Settings:

    def __init__(self):

        self.monochrome_assets = True
        self.full_color = False

        #for images, secifies the columns used for the ascii transform
        self.low_res = 50
        self.mid_res = 100
        self.high_res = 125
        self.very_high_res = 150
        self.HD = 200
        self.Ultra_HD = 400
        self.ascii_art = False

        self.ultra_hd_image_key = "alt"
        self.real_image_key = "#"
        self.info_key = "i"

    def copy(self):

        settings_copy = Settings()
        settings_copy.monochrome_assets = self.monochrome_assets
        settings_copy.full_color = self.full_color

        settings_copy.low_res = self.low_res
        settings_copy.mid_res = self.mid_res
        settings_copy.high_res = self.high_res
        settings_copy.very_high_res = self.very_high_res
        settings_copy.HD = self.HD
        settings_copy.Ultra_HD = self.Ultra_HD
        settings_copy.ascii_art = self.ascii_art
        settings_copy.ultra_hd_image_key = self.ultra_hd_image_key
        settings_copy.real_image_key = self.real_image_key
        settings_copy.info_key = self.info_key

        return settings_copy


"""
Contains all playinfo
"""

class Gameinfo:

    def __init__(self):

        self.savefile_name = None
        self.current_playset = None

    def copy(self):

        gameinfo_copy = Gameinfo()
        gameinfo_copy.savefile_name = self.savefile_name
        gameinfo_copy.current_playset = self.current_playset

        return gameinfo_copy

    def load_from(self, other_gameinfo):

        #savefile name
        self.savefile_name = other_gameinfo.savefile_name
        self.current_playset = other_gameinfo.current_playset

class Modules:

    def __init__(self):

        self.explorer_module = None
        self.explorer_mappings_module = None

        #refs
        self.explorer_mappings = None
        self.explorer_enums = None

    def create_refs(self):

        if (self.explorer_mappings_module is not None):

            self.explorer_mappings = self.explorer_mappings_module.explorer_mappings
            self.explorer_enums = self.explorer_mappings_module.ExplorerMappingsEnum


    def copy(self):

        modules_copy = Modules()
        modules_copy.explorer_module = self.explorer_module
        modules_copy.explorer_mappings_module = self.explorer_mappings_module

        modules_copy.create_refs()

        return modules_copy



class Global_Context:

    def __init__(self):

        self.settings = Settings()
        self.gameinfo = Gameinfo()
        self.modules = Modules()

        self.current_zoom = 0 #positive means zoomed in, negative means zoomed out
        self.current_scroll = 0
        self.max_scroll = 0
        self.cursor_visible = True
        self.terminal_handles = {} #handels for terminals
        self.misc = {} # Miscellaneous
        self.splitscreen_state = SplitscreenState.NORMAL

    def copy(self):

        context_copy = Global_Context()


        settings_copy = self.settings.copy()
        gameinfo_copy = self.gameinfo.copy()
        modules_copy = self.modules.copy()

        context_copy.settings = settings_copy
        context_copy.gameinfo = gameinfo_copy
        context_copy.modules = modules_copy

        context_copy.current_zoom = self.current_zoom
        context_copy.current_scroll = self.current_scroll
        context_copy.cursor_visible = self.cursor_visible
        context_copy.terminal_handles = self.terminal_handles #intentional reference copy
        context_copy.misc = self.misc
        context_copy.splitscreen_state = self.splitscreen_state

        return context_copy

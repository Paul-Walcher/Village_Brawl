"""
Global context to be given to each function
dealing with interactions.
"""

class Settings:

    def __init__(self):

        self.monochrome_assets = True
        self.full_color = False

        #for images, secifies the columns used for the ascii transform
        self.low_res = 50
        self.mid_res = 100
        self.high_res = 200
        self.very_high_res = 400

    def copy(self):

        settings_copy = Settings()
        settings_copy.monochrome_assets = self.monochrome_assets
        settings_copy.full_color = self.full_color

        settings_copy.low_res = self.low_res
        settings_copy.mid_res = self.mid_res
        settings_copy.high_res = self.high_res
        settings_copy.very_high_res = self.very_high_res

        return settings_copy


"""
Contains all playinfo
"""

class Gameinfo:

    def __init__(self):

        self.savefile_name = None

    def copy(self):

        gameinfo_copy = Gameinfo()
        gameinfo_copy.savefile_name = self.savefile_name

        return gameinfo_copy

    def load_from(self, other_gameinfo):

        #savefile name
        self.savefile_name = other_gameinfo.savefile_name


class Global_Context:

    def __init__(self):

        self.settings = Settings()
        self.gameinfo = Gameinfo()

        self.current_zoom = 0 #positive means zoomed in, negative means zoomed out
        self.current_scroll = 0
        self.max_scroll = 0
        self.cursor_visible = True
        self.terminal_handles = {} #handels for terminals
        self.misc = {} # Miscellaneous

    def copy(self):

        context_copy = Global_Context()


        settings_copy = self.settings.copy()
        gameinfo_copy = self.gameinfo.copy()

        context_copy.settings = settings_copy
        context_copy.gameinfo = gameinfo_copy
        context_copy.current_zoom = self.current_zoom
        context_copy.current_scroll = self.current_scroll
        context_copy.cursor_visible = self.cursor_visible
        context_copy.terminal_handles = self.terminal_handles #intentional reference copy
        context_copy.misc = self.misc

        return context_copy

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

class Global_Context:

    def __init__(self):

        self.settings = Settings()
        self.current_zoom = 0 #positive means zoomed in, negative means zoomed out

    def copy(self):

        context_copy = Global_Context()

        settings_copy = self.settings.copy()
        context_copy.settings = settings_copy
        context_copy.current_zoom = self.current_zoom


        return context_copy

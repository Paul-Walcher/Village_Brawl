"""
Global context to be given to each function
dealing with interactions.
"""

class Settings:

    def __init__(self):

        self.monochrome_assets = True
        self.full_color = False

    def copy(self):

        settings_copy = Settings()
        settings_copy.monochrome_assets = self.monochrome_assets
        settings_copy.full_color = self.full_color

        return settings_copy

class Global_Context:

    def __init__(self):

        self.settings = Settings()

    def copy(self):

        context_copy = Global_Context()

        settings_copy = self.settings.copy()
        context_copy.settings = settings_copy


        return context_copy

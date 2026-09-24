"""
Global context to be given to each function
dealing with interactions.
"""

class Global_Context:

    def __init__(self):

        self.monochrome_assets = True
        self.full_color = False

    def copy(self):

        context = Global_Context()

        context.monochrome_assets = self.monochrome_assets
        context.full_color = self.full_color

        return context

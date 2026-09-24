
"""
The main class for handling gamestates
"""

from enum import Enum, auto

import sys
import logic
from logic import Zoomrestore
from global_context import Global_Context
from states import Gamestates
import terminal_functions as terminal


class GamestateHandler:


    state_to_function = {
                            Gamestates.INTRO: logic.intro,
                            Gamestates.NEW_GAME_OR_LOAD_SAVE: logic.new_game_or_save_selection,
                            Gamestates.FINISH: lambda x: Gamestates.FINISH,
                            Gamestates.EXIT: lambda x: Gamestates.EXIT
                        }


    def __init__(self):

        self.context = Global_Context()
        self.state = Gamestates.INTRO

        terminal.reset_zoom(self.context)

    def run(self):

        """
        Calls the appropriate functions
        """

        while 1:

            with Zoomrestore(self.context):
                self.state = GamestateHandler.state_to_function[self.state](self)
                if self.state == Gamestates.FINISH:
                    self.finish()
                    break
                if self.state == Gamestates.EXIT:
                    self.exit()
                    break

    def finish(self):
        #ending activity
        logic.finish(self)

    def exit(self):
        #ending activity
        logic.finish(self)

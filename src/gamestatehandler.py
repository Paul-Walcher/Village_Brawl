
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

class GamestateHandler:


    state_to_function = {
                            Gamestates.INTRO: logic.intro,
                            Gamestates.NEW_GAME_OR_LOAD_SAVE: logic.new_game_or_save_selection,
                            Gamestates.FINISH: lambda x: Gamestates.FINISH,
                            Gamestates.EXIT: lambda x: Gamestates.EXIT
                        }


    def __init__(self):

        self.context = Global_Context()
        self.state_stack = Stack()
        self.state_stack.push(Gamestates.INTRO)

        terminal.reset_zoom(self.context)

    def run(self):

        """
        Calls the appropriate functions
        """

        quit = False
        next_state = None
        while not quit:

            next_state = self.state_stack.top()

            if next_state is None:
                next_state = Gamestates.EXIT
                break

            #firing the function
            with Zoomrestore(self.context):
                GamestateHandler.state_to_function[next_state](self)

            if next_state == Gamestates.FINISH:
                quit = True
            if next_state == Gamestates.EXIT:
                quit = True

        if next_state == Gamestates.FINISH:
            self.finish()
        elif next_state == Gamestates.EXIT:
            self.exit()


    def finish(self):
        #ending activity
        logic.finish(self)

    def exit(self):
        #ending activity
        logic.finish(self)

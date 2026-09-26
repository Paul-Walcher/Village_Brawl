"""
enums for specific states
"""
from enum import Enum, auto

class New_Game_Or_Save_Selection_Enum(Enum):

    New_Game = auto()
    Load_Save = auto()
    Go_Back = auto()

class Gamestates(Enum):

    INTRO = auto()
    NEW_GAME_OR_LOAD_SAVE = auto()
    NEW_GAME = auto()

    FINISH = auto()
    EXIT = auto()

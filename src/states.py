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
    SELECT_PLAYSET = auto()
    LOAD_PLAYSET = auto()
    CHOOSE_EXPLORER = auto()

    FINISH = auto()
    EXIT = auto()

class ActivationLocation(Enum):

    HAND = auto()
    FIELD = auto()
    DISCARD_PILE = auto()
    VOID = auto()
    WAVE_VOID = auto()
    ROUND_VOID = auto()

class ActivationResult(Enum):

    SUCCESS = auto()
    FAILURE = auto()

    WRONG_PHASE = auto()
    NOT_ENOUGH_RESOURCES = auto()

class SplitscreenState(Enum):

    NORMAL = auto()
    SPLIT_HORIZONTALLY = auto()

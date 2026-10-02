"""
Deck class, contains cards.
"""
from enum import Enum, auto

class ActivationLocation(Enum):

    HAND = auto()
    FIELD = auto()
    DISCARD_PILE = auto()
    VOID = auto()
    WAVE_VOID = auto()
    ROUND_VOID = auto()

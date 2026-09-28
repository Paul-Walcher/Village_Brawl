from enum import Enum, auto

class Phases(Enum):

    START_OF_GAME = auto()
    START_OF_ROUND = auto()
    END_OF_ROUND = auto()
    BEFORE_BIOME_CARD_REVEAL = auto()
    AFTER_BIOME_CARD_REVEAL = auto()
    START_OF_WAVE_BEFORE_DRAW = auto()
    START_OF_WAVE_AFTER_DRAW = auto()
    BEFORE_BATTLE = auto()
    AFTER_BATTLE = auto()
    #gets the information of the card activation, village or explorer
    AT_CARD_ACTIVATION = auto()
    AT_ENEMY_CARD_ACTIVATION = auto()
    #gets the information of the enemy ability
    AT_ENEMY_ABILITY_ACTIVATION = auto()

    #Village
    BEFORE_VILLAGE_PHASE = auto()
    BEFORE_BUILDING_ACTIVATION = auto()
    AFTER_BUILDNG_ACTIVATION = auto()
    BEFORE_OBJECTIVE = auto()
    AFTER_OBJECTIVE = auto()

    #misc
    BEFORE_OPENING_PACK = auto()
    AFTER_OPENING_PACK = auto()
    BEFORE_USING_ITEM = auto()
    AFTER_USING_ITEM = auto()
    BEFORE_CRAFTING = auto()
    AFTER_CRAFTING = auto()


all_phases = list(Phases)

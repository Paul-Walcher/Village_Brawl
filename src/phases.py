from enum import Enum, auto

class Phases(Enum):

    self.START_OF_GAME = auto()
    self.START_OF_ROUND = auto()
    self.END_OF_ROUND = auto()
    self.BEFORE_BIOME_CARD_REVEAL = auto()
    self.AFTER_BIOME_CARD_REVEAL = auto()
    self.START_OF_WAVE_BEFORE_DRAW = auto()
    self.START_OF_WAVE_AFTER_DRAW = auto()
    self.BEFORE_BATTLE = auto()
    self.AFTER_BATTLE = auto()
    #gets the information of the card activation, village or explorer
    self.AT_CARD_ACTIVATION = auto()
    self.AT_ENEMY_CARD_ACTIVATION = auto()
    #gets the information of the enemy ability
    self.AT_ENEMY_ABILITY_ACTIVATION = auto()

    #Village
    self.BEFORE_VILLAGE_PHASE = auto()
    self.BEFORE_BUILDING_ACTIVATION = auto()
    self.AFTER_BUILDNG_ACTIVATION = auto()
    self.BEFORE_OBJECTIVE = auto()
    self.AFTER_OBJECTIVE = auto()

    #misc
    self.BEFORE_OPENING_PACK = auto()
    self.AFTER_OPENING_PACK = auto()
    self.BEFORE_USING_ITEM = auto()
    self.AFTER_USING_ITEM = auto()
    self.BEFORE_CRAFTING = auto()
    self.AFTER_CRAFTING = auto()

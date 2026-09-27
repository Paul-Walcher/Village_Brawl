
"""
Template for any explorer.
"""
from abc import ABC, abstractmethod
from enum import Enum, auto


class Explorer(ABC):

    def __init__(self,  name: str,
                        description: str,
                        ability_name: str = "",
                        card_image_path: str = "",
                        standard_image_path: str = "",
                        lives: int = 5,
                        ability_activation_phases = None
                        inventory_size: float = 10.0,
                        starting_items: dict = None,
                        starting_cards: dict = None,
                        starting_packs: dict = None):

        #name
        self.name = name
        #description
        self.description = description
        #card image path
        self.card_image_path = card_image_path
        #standard image path
        self.standard_image_path = standard_image_path
        #starting items. these need to be the enums from items_mappings.
        #starting items are {name_enum: amount}
        self.starting_items = (starting_items if starting_items is not None else {})
        #starting cards
        #{card_enum: amount}
        self.starting_cards = (starting_cards if starting_cards is not None else {})
        #starting_packs
        #starting packs. these need to be the enums from pack_mappings
        #starting packs are {name_enum: amount}
        self.starting_packs = (starting_packs if starting_packs is not None else {})

        #stats
        #lives
        self.lives = lives
        #inventory size
        self.inventory_size = inventory_size
        #ability_activation_phases
        self.ability_activation_phases = (ability_activation_phases if ability_activation_phases is not None else [])

    @abstractmethod
    def activate_ability(self, phase, context):
        pass

"""
Explorer definitions
"""
import os
import importlib
from enum import Enum, auto


from templates.explorer_template import Explorer_Template
import terminal_functions as terminal
import constants

playset_path = os.path.dirname(os.path.abspath(__file__))
playset_name = os.path.basename(playset_path)
asset_path = os.path.join(playset_path, "assets")
standard_asset_path = os.path.join(asset_path, "standard_assets")
card_asset_path = os.path.join(asset_path, "card_assets")

class ExplorerEnum(Enum):

    BASIC_EXPLORER = auto()

class Basic_Explorer(Explorer_Template):

    def __init__(self):

        super().__init__()

        self.name = "Basic Explorer"
        self.name_color = (255, 144, 0)
        self.explorer_enum = ExplorerEnum.BASIC_EXPLORER
        self.description = terminal.text_rgb_string(0, 204, 0) + "Basic Explorer. Has no special abilities." + terminal.color_reset_string()

        self.ability_name = "-"
        self.ability_activation_phases = []

        self.card_image_path = os.path.join(card_asset_path, "Basic_Explorer_Card.png")
        self.standard_image_path = os.path.join(standard_asset_path, "Basic_Explorer_Standard.png")

        self.lives = 10
        self.inventory_size = 10.0

        self.starting_items = {}
        self.starting_supporters = {}
        self.starting_cards = {}
        self.starting_blueprints = {}
        self.starting_packs = {}

        self.starting_buildings = {}
        self.starting_villagers = {}

    def activate_ability(self, phase, context):
        pass

explorer_mappings = {
                        ExplorerEnum.BASIC_EXPLORER: Basic_Explorer()
                    }

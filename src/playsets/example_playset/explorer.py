"""
Explorer definitions
"""
import os

from templates.explorer_template import Explorer_Template
import terminal_functions as terminal



asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
standard_asset_path = os.path.join(asset_path, "standard_assets")
card_asset_path = os.path.join(asset_path, "card_assets")

class Basic_Explorer(Explorer_Template):

    def __init__(self):

        super().__init__()

        self.name = "Basic Explorer"
        self.name_color = (255, 144, 0)
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

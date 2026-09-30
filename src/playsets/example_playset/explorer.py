"""
Explorer definitions
"""
import os

from templates.explorer_template import Explorer_Template




asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
standard_asset_path = os.path.join(asset_path, "standard_assets")
card_asset_path = os.path.join(asset_path, "card_assets")

class Basic_Explorer(Explorer_Template):

    def __init__(self):

        super().__init__()

        self.name = "Basic Explorer"
        self.name_color = (255, 144, 0)
        self.description = "Basic Explorer. Has no special abilities."

        self.ability_name = "-"
        self.ability_activation_phases = []

        self.card_image_path = os.path.join(card_asset_path, "Basic_Explorer_Card.png")
        self.standard_image_path = os.path.join(standard_asset_path, "Basic_Explorer_Standard.png")

        self.lives = 10
        self.inventory_size = 10.0

        self.starting_items = {}
        self.starting_supporters = {}
        self.starting_cards = {}
        self.starting_packs = {}

    def activate_ability(self, phase, context):
        pass

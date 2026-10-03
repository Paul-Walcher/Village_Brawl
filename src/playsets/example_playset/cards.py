"""
Card definitions
"""
import os
import importlib
from enum import Enum, auto
import constants

from templates.card_template import Card_Template, CardInfo
import terminal_functions as terminal
import constants
import deck

playset_path = os.path.dirname(os.path.abspath(__file__))
playset_name = os.path.basename(playset_path)
asset_path = os.path.join(playset_path, "assets")
standard_asset_path = os.path.join(asset_path, "standard_assets")
card_asset_path = os.path.join(asset_path, "card_assets")


enums = importlib.import_module(f"{constants.PLAYSETS_FOLDER}.example_playset.enums")


class CardTag:
    pass

class Small_Rest(Card_Template):

    def __init__(self):

        super().__init__()

        self.name = "Small Rest"
        self.name_color = constants.Colors.WHITE

        self.card_enum = enums.CardEnums.SMALL_REST
        self.description = ""


"""
Constants used in the  program
"""

import os

__DEBUG__ = True

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images")
STANDARD_IMAGE_PATH = os.path.join(IMAGE_PATH, "standard_images")
CARD_IMAGE_PATH = os.path.join(IMAGE_PATH, "card_images")
PLAYSETS_FOLDER = "playsets"
PLAYSETS_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), PLAYSETS_FOLDER)

INTRO_IMAGES = ["Wood.png", "Twig.png", "Stone.png", "Pebble.png"]

SCRIPT_DIR = lambda: os.path.dirname(os.path.abspath(__file__))

VALID_SYMBOLS = [chr(x) for x in range(97, 97+26)] + [chr(x) for x in range(48, 58)] + ["_", "#"]

PAGE_CORRECTION_FACTOR_WIDTH = 0.9
PAGE_CORRECTION_FACTOR_HEIGHT = 0.9


"""
Constants used in the  program
"""

import os

IMAGE_PATH = os.path.join("assets", "images")
STANDARD_IMAGE_PATH = os.path.join(IMAGE_PATH, "standard_images")
CARD_IMAGE_PATH = os.path.join(IMAGE_PATH, "card_images")
PLAYSETS_PATH = "playsets"

INTRO_IMAGES = ["Wood.png", "Twig.png", "Stone.png", "Pebble.png"]

SCRIPT_DIR = lambda: os.path.dirname(os.path.abspath(__file__))

VALID_SYMBOLS = [chr(x) for x in range(97, 97+26)] + [chr(x) for x in range(48, 58)] + ["_", "#"]

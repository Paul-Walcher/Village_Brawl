
"""
Constants used in the  program
"""

import os

IMAGE_PATH = os.path.join("assets", "images")
STANDARD_IMAGE_PATH = os.path.join(IMAGE_PATH, "standard_images")
CARD_IMAGE_PATH = os.path.join(IMAGE_PATH, "card_images")

INTRO_IMAGES = ["Wood.png", "Twig.png", "Stone.png", "Pebble.png"]

SCRIPT_DIR = lambda: os.path.dirname(os.path.abspath(__file__))

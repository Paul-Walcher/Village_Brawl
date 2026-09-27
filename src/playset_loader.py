
"""
Used for loading a playset.
"""
import os
import time

import constants


def load_playset(context):

    playset_path = os.path.join(constants.PLAYSETS_PATH, context.gameinfo.current_playset)

    time.sleep(5)

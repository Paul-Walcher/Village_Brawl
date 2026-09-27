"""
Various setup functions.
These are called between state switches.
"""
import gamestatehandler as gamestatehandler_module

def pre_explorer_choosing(gamestatehandler):
    """
    Is called immediately after loading the playset,
    and before choosing the explorer.
    """
    pass

def post_explorer_choosing(gamestatehandler):
    """
    Is called immediately after having chosen the explorer,
    and before choosing the village.
    """
    pass

def pre_village_choosing(gamestatehandler):
    """
    Is called immediately before choosing the village.
    """
    pass

def post_village_choosing(gamestatehandler):
    """
    Is called immediately after having chosen a village.
    """
    pass
